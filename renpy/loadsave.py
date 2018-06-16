# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

import pickle
import cPickle

from cStringIO import StringIO

import zipfile
import re
import threading
import types
import shutil
import os
import sys

import renpy

from json import dumps as json_dumps

# Dump that chooses which pickle to use:


def dump(o, f):
    if renpy.config.use_cpickle:
        cPickle.dump(o, f, cPickle.HIGHEST_PROTOCOL)
    else:
        pickle.dump(o, f, pickle.HIGHEST_PROTOCOL)


def dumps(o):
    if renpy.config.use_cpickle:
        return cPickle.dumps(o, cPickle.HIGHEST_PROTOCOL)
    else:
        return pickle.dumps(o, pickle.HIGHEST_PROTOCOL)


def loads(s):
    if renpy.config.use_cpickle:
        return cPickle.loads(s)
    else:
        return pickle.loads(s)


# This is used as a quick and dirty way of versioning savegame
# files.
savegame_suffix = renpy.savegame_suffix


def save_dump(roots, log):
    """
    Dumps information about the save to save_dump.txt. We dump the size
    of the object (including unique children), the path to the object,
    and the type or repr of the object.
    """

    o_repr_cache = { }

    def visit(o, path):
        ido = id(o)

        if ido in o_repr_cache:
            f.write("{0: 7d} {1} = alias {2}\n".format(0, path, o_repr_cache[ido]))
            return 0

        if isinstance(o, (int, float, types.NoneType, types.ModuleType, types.ClassType)):
            o_repr = repr(o)

        elif isinstance(o, (str, unicode)):
            if len(o) <= 80:
                o_repr = repr(o).encode("utf-8")
            else:
                o_repr = repr(o[:80] + "...").encode("utf-8")

        elif isinstance(o, (tuple, list)):
            o_repr = "<" + o.__class__.__name__ + ">"

        elif isinstance(o, dict):
            o_repr = "<" + o.__class__.__name__ + ">"

        elif isinstance(o, types.MethodType):
            o_repr = "<method {0}.{1}>".format(o.im_class.__name__, o.im_func.__name__)

        elif isinstance(o, object):
            o_repr = "<{0}>".format(type(o).__name__)

        else:
            o_repr = "BAD TYPE <{0}>".format(type(o).__name__)

        o_repr_cache[ido] = o_repr

        if isinstance(o, (int, float, types.NoneType, types.ModuleType, types.ClassType)):
            size = 1

        elif isinstance(o, (str, unicode)):
            size = len(o) / 40 + 1

        elif isinstance(o, (tuple, list)):
            size = 1
            for i, oo in enumerate(o):
                size += 1
                size += visit(oo, "{0}[{1!r}]".format(path, i))

        elif isinstance(o, dict):
            size = 2
            for k, v in o.iteritems():
                size += 2
                size += visit(v, "{0}[{1!r}]".format(path, k))

        elif isinstance(o, types.MethodType):
            size = 1 + visit(o.im_self, path + ".im_self")

        else:

            try:
                reduction = o.__reduce_ex__(2)
            except:
                reduction = [ ]
                o_repr = "BAD REDUCTION " + o_repr

            # Gets an element from the reduction, or o if we don't have
            # such an element.
            def get(idx, default):
                if idx < len(reduction) and reduction[idx] is not None:
                    return reduction[idx]
                else:
                    return default

            # An estimate of the size of the object, in arbitrary units. (These units are about 20-25 bytes on
            # my computer.)
            size = 1

            state = get(2, { })
            if isinstance(state, dict):
                for k, v in state.iteritems():
                    size += 2
                    size += visit(v, path + "." + k)
            else:
                size += visit(state, path + ".__getstate__()")

            for i, oo in enumerate(get(3, [])):
                size += 1
                size += visit(oo, "{0}[{1}]".format(path, i))

            for i in get(4, []):

                if len(i) != 2:
                    continue

                k, v = i

                size += 2
                size += visit(v, "{0}[{1!r}]".format(path, k))

        f.write("{0: 7d} {1} = {2}\n".format(size, path, o_repr_cache[ido]))

        return size

    f = file("save_dump.txt", "w")

    visit(roots, "roots")
    visit(log, "log")

    f.close()


def find_bad_reduction(roots, log):
    """
    Finds objects that can't be reduced properly.
    """

    seen = set()

    def visit(o, path):
        ido = id(o)

        if ido in seen:
            return

        seen.add(ido)

        if isinstance(o, (int, float, types.NoneType, types.ClassType)):
            return

        if isinstance(o, (tuple, list)):
            for i, oo in enumerate(o):
                rv = visit(oo, "{0}[{1!r}]".format(path, i))
                if rv is not None:
                    return rv

        elif isinstance(o, dict):
            for k, v in o.iteritems():
                rv = visit(v, "{0}[{1!r}]".format(path, k))
                if rv is not None:
                    return rv

        elif isinstance(o, types.MethodType):
            return visit(o.im_self, path + ".im_self")

        elif isinstance(o, types.ModuleType):

            return "{} = {}".format(path, repr(o)[:160])

        else:

            try:
                reduction = o.__reduce_ex__(2)
            except:

                import copy

                try:
                    copy.copy(o)
                    return None
                except:
                    pass

                return "{} = {}".format(path, repr(o)[:160])

            # Gets an element from the reduction, or o if we don't have
            # such an element.
            def get(idx, default):
                if idx < len(reduction) and reduction[idx] is not None:
                    return reduction[idx]
                else:
                    return default

            state = get(2, { })
            if isinstance(state, dict):
                for k, v in state.iteritems():
                    rv = visit(v, path + "." + k)
                    if rv is not None:
                        return rv
            else:
                rv = visit(state, path + ".__getstate__()")
                if rv is not None:
                    return rv

            for i, oo in enumerate(get(3, [])):
                rv = visit(oo, "{0}[{1}]".format(path, i))
                if rv is not None:
                    return rv

            for i in get(4, []):

                if len(i) != 2:
                    continue

                k, v = i

                rv = visit(v, "{0}[{1!r}]".format(path, k))
                if rv is not None:
                    return rv

        return None

    for k, v in roots.items():
        rv = visit(v, k)
        if rv is not None:
            return rv

    return visit(log, "renpy.game.log")


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
    except:

        # If the rename failed, try again.
        try:
            os.unlink(new)
            os.rename(old, new)
        except:

            # If it fails a second time, give up.
            try:
                os.unlink(old)
            except:
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
            shutil.copyfile(self.first_filename, filename_new)
            safe_rename(filename_new, filename)
            return

        zf = zipfile.ZipFile(filename_new, "w", zipfile.ZIP_DEFLATED)

        # Screenshot.
        zf.writestr("screenshot.png", self.screenshot)

        # Extra info.
        zf.writestr("extra_info", self.extra_info.encode("utf-8"))

        # Json
        zf.writestr("json", self.json)

        # Version.
        zf.writestr("renpy_version", renpy.version)

        # The actual game.
        zf.writestr("log", self.log)

        zf.close()

        safe_rename(filename_new, filename)

        self.first_filename = filename


def save(slotname, extra_info='', mutate_flag=False):
    """
    :doc: loadsave
    :args: (filename, extra_info='')

    Saves the game state to a save slot.

    `filename`
        A string giving the name of a save slot. Despite the variable name,
        this corresponds only loosely to filenames.

    `extra_info`
        An additional string that should be saved to the save file. Usually,
        this is the value of :var:`save_name`.

    :func:`renpy.take_screenshot` should be called before this function.
    """

    if mutate_flag:
        renpy.python.mutate_flag = False

    roots = renpy.game.log.freeze(None)

    if renpy.config.save_dump:
        save_dump(roots, renpy.game.log)

    logf = StringIO()
    try:
        dump((roots, renpy.game.log), logf)
    except:

        t, e, tb = sys.exc_info()

        if mutate_flag:
            raise t, e, tb

        try:
            bad = find_bad_reduction(roots, renpy.game.log)
        except:
            raise t, e, tb

        if bad is None:
            raise t, e, tb

        e.args = ( e.args[0] + ' (perhaps {})'.format(bad), ) + e.args[1:]
        raise t, e, tb

    if mutate_flag and renpy.python.mutate_flag:
        raise SaveAbort()

    screenshot = renpy.game.interface.get_screenshot()

    json = { "_save_name" : extra_info }

    for i in renpy.config.save_json_callbacks:
        i(json)

    json = json_dumps(json)

    sr = SaveRecord(screenshot, extra_info, json, logf.getvalue())
    location.save(slotname, sr)

    location.scan()
    clear_slot(slotname)


# Flag that lets us know if an autosave is in progress.
autosave_not_running = threading.Event()
autosave_not_running.set()

# The number of times autosave has been called without a save occuring.
autosave_counter = 0


def autosave_thread(take_screenshot):

    global autosave_counter

    try:

        try:

            cycle_saves("auto-", renpy.config.autosave_slots)

            if renpy.config.auto_save_extra_info:
                extra_info = renpy.config.auto_save_extra_info()
            else:
                extra_info = ""

            if take_screenshot:
                renpy.exports.take_screenshot(background=True)

            save("auto-1", mutate_flag=True, extra_info=extra_info)
            autosave_counter = 0

        except:
            pass

    finally:
        autosave_not_running.set()


def autosave():
    global autosave_counter

    if not renpy.config.autosave_frequency:
        return

    # That is, autosave is running.
    if not autosave_not_running.isSet():
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

    force_autosave(True)


# This assumes a screenshot has already been taken.
def force_autosave(take_screenshot=False):
    """
    :doc: other

    Forces a background autosave to occur.

    `take_screenshot`
        If True, a new screenshot will be taken. If False, the existing
        screenshot will be used.
    """

    # That is, autosave is running.
    if not autosave_not_running.isSet():
        return

    # Do not save if we're in the main menu.
    if renpy.store.main_menu:
        return

    # Do not save if we're in a replay.
    if renpy.store._in_replay:
        return

    autosave_not_running.clear()
    t = threading.Thread(target=autosave_thread, args=(take_screenshot,))
    t.daemon = True
    t.start()


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

    extra_info = json.get("_save_name", "")

    screenshot = c.get_screenshot()

    if screenshot is None:
        return None

    return extra_info, screenshot, mtime


def list_saved_games(regexp=r'.', fast=False):
    """
    :doc: loadsave

    Lists the save games. For each save game, returns a tuple containing:

    * The filename of the save.
    * The extra_info that was passed in.
    * A displayable that, when displayed, shows the screenshot that was
      used when saving the game.
    * The time the game was stayed at, in seconds since the UNIX epoch.

    `regexp`
        A regular expression that is matched against the start of the
        filename to filter the list.

    `fast`
        If fast is true, the filename is returned instead of the
        tuple.
    """

    # A list of save slots.
    slots = location.list()

    if regexp is not None:
        slots = [ i for i in slots if re.match(regexp, i) ]

    slots.sort()

    if fast:
        return slots

    rv = [ ]

    for s in slots:

        c = get_cache(s)

        if c is not None:
            json = c.get_json()
            if json is not None:
                extra_info = json.get("_save_name", "")
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
    """

    # A list of save slots.
    slots = location.list()

    if regexp is not None:
        slots = [ i for i in slots if re.match(regexp, i) ]

    slots.sort()

    return slots


# A cache for newest slot info.
newest_slot_cache = { }


def newest_slot(regexp=None):
    """
    :doc: loadsave

    Returns the name of the newest save slot (the save slot with the most
    recent modification time), or None if there are no (matching) saves.

    If `regexp` exists, only slots that begin with `regexp` are returned.
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

            if mtime >= max_mtime:
                rv = i
                max_mtime = mtime

    newest_slot_cache[regexp] = rv
    return rv


def slot_mtime(slotname):
    """
    :doc: loadsave

    Returns the modification time for `slot`, or None if the slot is empty.
    """

    return get_cache(slotname).get_mtime()


def slot_json(slotname):
    """
    :doc: loadsave

    Returns the json information for `slotname`, or None if the slot is
    empty.
    """

    return get_cache(slotname).get_json()


def slot_screenshot(slotname):
    """
    :doc: loadsave

    Returns a display that can be used as the screenshot for `slotname`,
    or None if the slot is empty.
    """

    return get_cache(slotname).get_screenshot()


def can_load(filename, test=False):
    """
    :doc: loadsave

    Returns true if `filename` exists as a save slot, and False otherwise.
    """

    c = get_cache(filename)

    if c.get_mtime():
        return True
    else:
        return False


def load(filename):
    """
    :doc: loadsave

    Loads the game state from the save slot `filename`. If the file is loaded
    successfully, this function never returns.
    """

    roots, log = loads(location.load(filename))
    log.unfreeze(roots, label="_after_load")


def unlink_save(filename):
    """
    :doc: loadsave

    Deletes the save slot with the given name.
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

        return rv

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
cache = { }


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

    renpy.exports.restart_interaction()


def clear_cache():
    """
    Clears the entire cache.
    """

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

if False:
    location = renpy.savelocation.FileLocation("blah")
