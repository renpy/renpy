# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains functions that load and save the game state.

import io
import zipfile
import re
import threading
import shutil
import os
import time

import renpy
from json import dumps as json_dumps

from renpy.compat.pickle import dump, loads, dump_paths, find_bad_reduction


# This is used as a quick and dirty way of versioning savegame
# files.
savegame_suffix = renpy.savegame_suffix

################################################################################
# Saving
################################################################################

# Used to indicate an aborted save, due to the game being mutated
# while the save is in progress.


class SaveAbort(Exception):
    pass


def safe_rename(old, new):
    """
    Safely rename old to new.
    """

    if os.path.exists(new):
        os.unlink(new)

    try:
        os.rename(old, new)
    except Exception:
        # If the rename failed, try again.
        try:
            os.unlink(new)
            os.rename(old, new)
        except Exception:
            # If it fails a second time, give up.
            try:
                os.unlink(old)
            except Exception:
                pass


class SaveRecord(object):
    """
    This is passed to the save locations. It contains the information that
    goes into a save file in uncompressed form, and the logic to save that
    information to a Ren'Py-standard format save file.
    """

    def __init__(self, screenshot, extra_info, json, log):
        self.screenshot = screenshot
        self.extra_info = extra_info
        self.json = json
        self.log = log

        self.first_filename = None

    def write_file(self, filename):
        """
        This writes a standard-format savefile to `filename`.
        """

        filename_new = filename + ".new"

        # For speed, copy the file after we've written it at least once.
        if self.first_filename is not None:
            try:
                shutil.copyfile(self.first_filename, filename_new)
            except OSError as e:
                if renpy.config.developer:
                    raise e
            else:
                safe_rename(filename_new, filename)
                return

        with zipfile.ZipFile(filename_new, "w", zipfile.ZIP_DEFLATED) as zf:
            # Screenshot.
            if self.screenshot is not None:
                zf.writestr("screenshot.png", self.screenshot)

            # Extra info.
            zf.writestr("extra_info", self.extra_info.encode("utf-8"))

            # Json
            zf.writestr("json", self.json)

            # Version.
            zf.writestr("renpy_version", renpy.version)

            # The actual game.
            zf.writestr("log", self.log)

            # The signatures.
            zf.writestr("signatures", renpy.savetoken.sign_data(self.log))

        safe_rename(filename_new, filename)

        self.first_filename = filename


def save(slotname, extra_info="", mutate_flag=False, include_screenshot=True, extra_json=None):
    """
    :doc: loadsave
    :args: (filename, extra_info='', *, extra_json=None)

    Saves the game to the slot identified by `filename`.

    `filename`
        A string giving the name of a save slot. Despite the variable name,
        this corresponds only loosely to filenames (e.g. '3-2' for page 3, slot 2)

    `extra_info`
        A string stored as the ``_save_name`` field in the save file’s metadata. This can be retrieved via
        :func:`renpy.slot_json` (using the "_savename" key, :func:`FileJson` (with ``key=None`` or ``key="_save_name"``),
        or as the ``extra_info`` field in :func:`renpy.list_saved_games`. It is typically used with the global
        :var:`save_name` variable (e.g., ``"Chapter 1"``). If empty, ``_save_name`` will be an empty string.

    `extra_json`
        A dictionary of additional metadata to be stored in the save file. This is merged with the default metadata
        and the metadata from :var:`config.save_json_callbacks`.

    Example::
        $ save_name = "Chapter 1"
        $ renpy.save("1-1", extra_info=save_name)

    To store additional or complex metadata, use :var:`config.save_json_callbacks` to add custom fields to the metadata dictionary.

    :func:`renpy.take_screenshot` should be called before this function.
    """

    if not renpy.config.save:
        return

    # Update persistent file, if needed. This is for the web and mobile
    # platforms, to make sure the persistent file is updated whenever the
    # game is saved. (But not auto-saved, for performance reasons.)
    if not mutate_flag:
        renpy.persistent.update()

    if mutate_flag:
        renpy.revertable.mutate_flag = False

    roots = renpy.game.log.freeze(None)

    if renpy.config.save_dump:
        dump_paths("save_dump.txt", **{"renpy.game.log": renpy.game.log}, **roots)

    logf = io.BytesIO()
    try:
        dump((roots, renpy.game.log), logf)
    except Exception as e:
        if mutate_flag:
            raise

        try:
            if bad := find_bad_reduction(**{"renpy.game.log": renpy.game.log}, **roots):
                e.add_note(f"Perhaps bad reduction in {bad}")
        except Exception:
            pass

        raise

    if mutate_flag and renpy.revertable.mutate_flag:
        raise SaveAbort()

    if include_screenshot:
        screenshot = renpy.game.interface.get_screenshot()
    else:
        screenshot = None

    json = {
        "_save_name": extra_info,
        "_renpy_version": list(renpy.version_tuple),
        "_version": renpy.config.version,
        "_game_runtime": renpy.exports.get_game_runtime(),
        "_ctime": time.time(),
    }

    for i in renpy.config.save_json_callbacks:
        i(json)

    if extra_json is not None:
        json.update(extra_json)

    json = json_dumps(json)

    sr = SaveRecord(screenshot, extra_info, json, logf.getvalue())
    location.save(slotname, sr)

    location.scan()
    clear_slot(slotname)


# The thread used for autosave.
autosave_thread = None

# Flag that lets us know if an autosave is in progress.
autosave_not_running = threading.Event()
autosave_not_running.set()

# The number of times autosave has been called without a save occurring.
autosave_counter = 0

# True if a background autosave has finished.
did_autosave = False


def autosave_thread_function(take_screenshot):
    global autosave_counter
    global did_autosave

    if renpy.config.autosave_prefix_callback:
        prefix = renpy.config.autosave_prefix_callback()
    else:
        prefix = "auto-"

    try:
        with renpy.savelocation.SyncfsLock():
            if renpy.config.auto_save_extra_info:
                extra_info = renpy.config.auto_save_extra_info()
            else:
                extra_info = ""

            if take_screenshot:
                renpy.exports.take_screenshot(background=True)

            save("_auto", mutate_flag=True, extra_info=extra_info)
            cycle_saves(prefix, renpy.config.autosave_slots)
            rename_save("_auto", prefix + "1")

            autosave_counter = 0
            did_autosave = True

    except Exception:
        pass

    finally:
        autosave_not_running.set()


def autosave():
    global autosave_counter

    if not renpy.config.autosave_frequency:
        return

    if not renpy.config.has_autosave:
        return

    # That is, autosave is running.
    if not autosave_not_running.is_set():
        return

    if renpy.config.skipping:
        return

    if len(renpy.game.contexts) > 1:
        return

    autosave_counter += 1

    if autosave_counter < renpy.config.autosave_frequency:
        return

    if renpy.store.main_menu:
        return

    if not renpy.store._autosave:
        return

    force_autosave(True)


# This assumes a screenshot has already been taken.
def force_autosave(take_screenshot=False, block=False):
    """
    :doc: other

    Forces a background autosave to occur.

    `take_screenshot`
        If True, a new screenshot will be taken. If False, the existing
        screenshot will be used.

    `block`
        If True, blocks until the autosave completes.
    """

    global autosave_thread

    if not renpy.config.has_autosave:
        return

    if renpy.game.after_rollback or renpy.exports.in_rollback():
        return

    if not renpy.store._autosave:
        return

    # That is, autosave is running.
    if not autosave_not_running.is_set():
        return

    # Join the autosave thread to clear resources.
    if autosave_thread is not None:
        autosave_thread.join()
        autosave_thread = None

    # Do not save if we're in the main menu.
    if renpy.store.main_menu:
        return

    # Do not save if we're in a replay.
    if renpy.store._in_replay:
        return

    if block:
        if renpy.config.auto_save_extra_info:
            extra_info = renpy.config.auto_save_extra_info()
        else:
            extra_info = ""

        if renpy.config.autosave_prefix_callback:
            prefix = renpy.config.autosave_prefix_callback()
        else:
            prefix = "auto-"

        cycle_saves(prefix, renpy.config.autosave_slots)

        if take_screenshot:
            renpy.exports.take_screenshot()

        save(prefix + "1", extra_info=extra_info)

        return

    autosave_not_running.clear()

    if not renpy.emscripten:
        autosave_thread = threading.Thread(target=autosave_thread_function, args=(take_screenshot,))
        autosave_thread.daemon = True
        autosave_thread.start()
    else:
        autosave_thread_function(take_screenshot)


################################################################################
# Loading and Slot Manipulation
################################################################################


def scan_saved_game(slotname):
    c = get_cache(slotname)

    mtime = c.get_mtime()

    if mtime is None:
        return None

    json = c.get_json()
    if json is None:
        return None

    extra_info = json.get("_save_name", "")  # type: ignore

    screenshot = c.get_screenshot()

    if screenshot is None:
        return None

    return extra_info, screenshot, mtime


def list_saved_games(regexp=r".", fast=False):
    """
     :doc: loadsave

     Lists the save games. For each save game, returns a tuple containing:

     * The filename of the save.
     * The extra_info that was passed in.
     * A displayable that, when displayed, shows the screenshot that was
       used when saving the game.
     * The time the game was stayed at, in seconds since the UNIX epoch.

     `regexp`
         A regular expression to filter save slot names. If ``None``, all slots are included.

     `fast`
         If fast is true, only a list with matching filenames is returned instead of the list of tuples, making it equivalent to :func:`list_slots`

     Unless ``fast=True``, returns a list of tuples, each containing:
     - The slot name (e.g., ``"1-1"``).
     - ``extra_info``, the ``_save_name`` field from the save file’s metadata, set by the ``extra_info`` argument of :func:`renpy.save`.
     - ``time``, the modification time of the save file, in seconds since the epoch (equivalent to ``_ctime`` in :func:`renpy.slot_json` or :func:`FileJson`).
     - ``screenshot``, a displayable (or ``None``) for the save’s screenshot, accessible via :func:`FileScreenshot`.

     To access other metadata fields (e.g., ``_renpy_version``, ``_version``, ``_game_runtime``, custom fields), use :func:`renpy.slot_json` or, for built-in fields only, :func:`FileJson`.

     Example::

        screen save_list():
            vbox:
                for name, extra_info, time, screenshot in renpy.list_saved_games(fast=False):
                    textbutton "[name]: [extra_info]" action FileLoad(name)

     Ren'Py save slots follow naming conventions: manual saves use the format ``page-slot`` (e.g., ``1-1``, ``2-3``), autosaves use ``auto-slot`` (e.g., ``auto-1``), and quicksaves use ``quick-slot`` (e.g., ``quick-1``). The ``regexp`` parameter can filter these slots using Python regular expressions.

    Useful Regular Expressions:

    - ``r"^(\\d+|auto|quick)-\\d+$"``: Matches all manual (e.g., ``1-1``), auto (e.g., ``auto-1``), and quick (e.g., ``quick-1``) saves. Intentionally listing the types you need avoids encountering built-in save types like ``_reload-1``
    - ``r"^\\d+-\\d+$"``: Matches manual saves (e.g., ``1-1``, ``2-3``).
    - ``r"^auto-\\d+$"``: Matches autosaves (e.g., ``auto-1``, ``auto-2``).
    - ``r"^quick-\\d+$"``: Matches quicksaves (e.g., ``quick-1``, ``quick-2``).

    """

    # A list of save slots.
    slots = location.list()

    if regexp is not None:
        slots = [i for i in slots if re.match(regexp, i)]

    slots.sort()

    if fast:
        return slots

    rv = []

    for s in slots:
        c = get_cache(s)

        if c is not None:
            json = c.get_json()
            if json is not None:
                extra_info = json.get("_save_name", "")  # type: ignore
            else:
                extra_info = ""

            screenshot = c.get_screenshot()
            mtime = c.get_mtime()

            rv.append((s, extra_info, screenshot, mtime))

    return rv


def list_slots(regexp=None):
    """
    :doc: loadsave

    Returns a list of non-empty save slots. If `regexp` exists, only slots
    that begin with `regexp` are returned. The slots are sorted in
    string-order.

    For a list of useful regular expressions, see :func:`list_saved_games`
    """

    # A list of save slots.
    slots = location.list()

    if regexp is not None:
        slots = [i for i in slots if re.match(regexp, i)]

    slots.sort()

    return slots


# The set of slots that have been accessed, such that clearing the slot
# should restart the interaction.
accessed_slots = set()

# A cache for newest slot info.
newest_slot_cache = {}


def newest_slot(regexp=None):
    """
    :doc: loadsave

    Returns the name of the newest save slot (the save slot with the most
    recent modification time), or None if there are no (matching) saves.

    If `regexp` exists, only slots that begin with `regexp` are returned.

    For a list of useful regular expressions, see :func:`list_saved_games`
    """

    rv = newest_slot_cache.get(regexp, unknown)
    if rv is unknown:
        max_mtime = 0
        rv = None

        slots = location.list()

        for i in slots:
            if (regexp is not None) and (not re.match(regexp, i)):
                continue

            mtime = get_cache(i).get_mtime()
            if mtime is None:
                continue

            if mtime >= max_mtime:  # type: ignore
                rv = i
                max_mtime = mtime

    newest_slot_cache[regexp] = rv
    return rv


def slot_mtime(slotname):
    """
    :doc: loadsave

    Returns the modification time for `slot`, or None if the slot is empty.
    """

    accessed_slots.add(slotname)

    return get_cache(slotname).get_mtime()


def slot_json(slotname):
    """
    :doc: loadsave

    Returns a dictionary containing the metadata of the save file in `slotname`, including ``_save_name``, ``_renpy_version``, ``_version``, ``_game_runtime``, ``_ctime``, and any custom fields added via :var:`config.save_json_callbacks` at the time of saving. If the slot is empty, `None` is returned. For save/load screen actions, :func:`FileJson` provides a subset of these fields (excluding custom fields).

    Example::

        def show_game_runtime(slot):
            metadata = renpy.slot_json(slot)
            name = metadata.get('_save_name', '')
            runtime = metadata.get('_game_runtime', 0)
            hours = int(runtime // 3600)
            minutes = int((runtime % 3600) // 60)
            seconds = int(runtime % 60)
            runtime_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            renpy.notify("Save Name: [name], Game Runtime: [runtime_formatted]")
    """

    accessed_slots.add(slotname)

    return get_cache(slotname).get_json()


def slot_screenshot(slotname):
    """
    :doc: loadsave

    Returns a display that can be used as the screenshot for `slotname`,
    or None if the slot is empty.
    """

    accessed_slots.add(slotname)

    return get_cache(slotname).get_screenshot()


def can_load(filename, test=False):
    """
    :doc: loadsave

    Returns true if `filename` (e.g. '3-2' for page 3, slot 2) exists as a save slot, and False otherwise.
    """

    accessed_slots.add(filename)

    c = get_cache(filename)

    if c.get_mtime():
        return True
    else:
        return False


def load(filename):
    """
    :doc: loadsave

    Loads the game state from the save slot `filename` (e.g. '3-2' for page 3, slot 2). If the file is loaded
    successfully, this function never returns.
    """

    log_data, signature = location.load(filename)

    if not renpy.savetoken.check_load(log_data, signature):
        return

    try:
        json = slot_json(filename)
    except Exception as e:
        json = {}

    renpy.session["traceback_load"] = "_traceback" in json

    renpy.exports.call_in_new_context("_before_load")

    roots, log = loads(log_data)

    log.unfreeze(roots, label="_after_load")


def get_save_data(filename):
    """
    :doc: loadsave

    This loads a game's data from the save slot `filename` (e.g. '3-2' for page 3, slot 2), without
    actually changing the game state. It returns a dictionary containing variable names relative to
    the default store, mapped to the value of those variables at the time of the save.
    """
    log_data, signature = location.load(filename)

    if not renpy.savetoken.check_load(log_data, signature):
        return

    roots, log = loads(log_data)

    return {k[6:]: v for k, v in roots.items() if k.startswith("store.")}


def unlink_save(filename):
    """
    :doc: loadsave

    Deletes the save slot with the given name (e.g. '3-2' for page 3, slot 2).
    """

    location.unlink(filename)
    clear_slot(filename)


def rename_save(old, new):
    """
    :doc: loadsave

    Renames a save from `old` to `new`. (Does nothing if `old` does not
    exist.)
    """

    location.rename(old, new)

    clear_slot(old)
    clear_slot(new)


def copy_save(old, new):
    """
    :doc: loadsave

    Copies the save at `old` to `new`. (Does nothing if `old` does not
    exist.)
    """

    location.copy(old, new)
    clear_slot(new)


def cycle_saves(name, count):
    """
    :doc: loadsave

    Rotates the first `count` saves beginning with `name`.

    For example, if the name is auto- and the count is 10, then
    auto-9 will be renamed to auto-10, auto-8 will be renamed to auto-9,
    and so on until auto-1 is renamed to auto-2.
    """

    for i in range(count - 1, 0, -1):
        rename_save(name + str(i), name + str(i + 1))


################################################################################
# Cache
################################################################################


# None is a possible value for some of the attributes.
unknown = renpy.object.Sentinel("unknown")


def wrap_json(d):
    if isinstance(d, list):
        return [wrap_json(i) for i in d]
    if isinstance(d, dict):
        return renpy.revertable.RevertableDict({k: wrap_json(v) for k, v in d.items()})
    else:
        return d


class Cache(object):
    """
    This represents cached information about a save slot.
    """

    def __init__(self, slotname):
        self.slotname = slotname
        self.clear()

    def clear(self):
        # The time the save was created.
        self.mtime = unknown

        # The json object loaded from the save slot.
        self.json = unknown

        # The screenshot associated with the save slot.
        self.screenshot = unknown

    def get_mtime(self):
        rv = self.mtime

        if rv is unknown:
            rv = self.mtime = location.mtime(self.slotname)

        return rv

    def get_json(self):
        rv = self.json

        if rv is unknown:
            rv = self.json = location.json(self.slotname)

        return wrap_json(rv)

    def get_screenshot(self):
        rv = self.screenshot

        if rv is unknown:
            rv = self.screenshot = location.screenshot(self.slotname)

        return self.screenshot

    def preload(self):
        """
        Preloads all the save data (that won't take up a ton of memory).
        """

        self.get_mtime()
        self.get_json()
        self.get_screenshot()


# A map from slotname to cache object. This is used to cache savegame scan
# data until the slot changes.
cache = {}


def get_cache(slotname):
    rv = cache.get(slotname, None)

    if rv is None:
        rv = cache[slotname] = Cache(slotname)

    return rv


def clear_slot(slotname):
    """
    Clears a single slot in the cache.
    """

    get_cache(slotname).clear()

    newest_slot_cache.clear()

    if slotname in accessed_slots:
        accessed_slots.discard(slotname)
        renpy.exports.restart_interaction()


def clear_cache():
    """
    Clears the entire cache.
    """

    accessed_slots.clear()

    for c in cache.values():
        c.clear()

    newest_slot_cache.clear()

    renpy.exports.restart_interaction()


def init():
    """
    Scans all the metadata from the save slot cache.
    """

    for i in list_slots():
        if not i.startswith("_"):
            get_cache(i).preload()


# Save locations are places where saves are saved to or loaded from, or a
# collection of such locations. This is the default save location.
location = None

if 1 == 0:
    location = renpy.savelocation.FileLocation("blah")
