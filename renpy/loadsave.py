# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import pickle
import cPickle

from cStringIO import StringIO

import zipfile
import os
import re
import threading
import types
import shutil
import json

import renpy.display

# Dump that chooses which pickle to use:
def dump(o, f):
    if renpy.config.use_cpickle:
        cPickle.dump(o, f, cPickle.HIGHEST_PROTOCOL)
    else:
        pickle.dump(o, f, pickle.HIGHEST_PROTOCOL)

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

################################################################################
# Saving
################################################################################

# Used to indicate an aborted save, due to the game being mutated
# while the save is in progress.
class SaveAbort(Exception):
    pass

class SaveRecord(object):
    """
    This is passed to the save locations. It contains the information that
    goes into a save file in uncompressed form, and the logic to save that
    information to a Ren'Py-standard format save file.
    """

    def __init__(self, screenshot, extra_info, log):
        self.screenshot = screenshot
        self.extra_info = extra_info
        self.log = log

        self.first_filename = None

    def write_file(self, filename):
        """
        This writes a standard-format savefile to `filename`.
        """

        # For speed, copy the file after we've written it at least once.
        if self.first_filename is not None:
            shutil.copy(self.first_filename, filename)

        self.first_filename = filename

        zf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)

        # Screenshot.
        zf.writestr("screenshot.png", self.screenshot)

        # Extra info.
        zf.writestr("extra_info", self.extra_info.encode("utf-8"))

        # Version.
        zf.writestr("renpy_version", renpy.version)

        # The actual game.
        zf.writestr("log", self.log)

        zf.close()


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

    get_cache(slotname).clear()

    if mutate_flag:
        renpy.python.mutate_flag = False

    roots = renpy.game.log.freeze(None)

    logf = StringIO()
    dump((roots, renpy.game.log), logf)

    if mutate_flag and renpy.python.mutate_flag:
        raise SaveAbort()

    if renpy.config.save_dump:
        save_dump(roots, renpy.game.log)

    screenshot = renpy.game.interface.get_screenshot()

    sr = SaveRecord(screenshot, extra_info, logf.getvalue())
    location.save(slotname, sr)



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

    if renpy.game.context()._main_menu:
        return

    force_autosave(True)


# This assumes a screenshot has already been taken.
def force_autosave(take_screenshot=False):

    # That is, autosave is running.
    if not autosave_not_running.isSet():
        return

    autosave_not_running.clear()
    threading.Thread(target=autosave_thread, args=(take_screenshot,)).start()


################################################################################
# Loading and Slot Manipulation
################################################################################

def scan_saved_game(slotname):

    c = get_cache(slotname)

    mtime = c.get_mtime()

    if mtime is None:
        return None

    extra_info = c.get_json().get("_extra_info", "")
    screenshot = c.get_screenshot()

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

        extra_info = c.get_json().get("_extra_info", "")
        screenshot = c.get_screenshot()
        mtime = c.get_mtime()

        rv.append((s, extra_info, screenshot, mtime))

    return rv

def can_load(filename, test=False):
    """
    :doc: loadsave

    Returns true if `filename` exists as a save file, and False otherwise.
    """

    fn = renpy.config.savedir + "/" + filename + savegame_suffix
    return os.path.exists(fn)


def load(filename):
    """
    :doc: loadsave

    Loads the game state from `filename`. This function never returns.
    """

    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename + savegame_suffix, "r")
    roots, log = loads(zf.read("log"))
    zf.close()

    log.unfreeze(roots, label="_after_load")

def rename_save(old, new):
    """
    :doc: loadsave

    Renames a save from `old` to `new`.
    """

    unlink_save(new)
    os.rename(renpy.config.savedir + "/" + old + savegame_suffix,
              renpy.config.savedir + "/" + new + savegame_suffix)

    cache.pop(old, None)
    cache.pop(new, None)

def unlink_save(filename):
    """
    :doc: loadsave

    Deletes the save with the given `filename`.
    """

    if os.path.exists(renpy.config.savedir + "/" + filename + savegame_suffix):
        os.unlink(renpy.config.savedir + "/" + filename + savegame_suffix)

    cache.pop(filename, None)


def cycle_saves(name, count):
    """
    :doc: loadsave

    Rotates the first `count` saves beginning with `name`.

    For example, if the name is auto and the count is 10, then
    auto-9 will be renamed to auto-9, auto-8 will be renamed to auto-9,
    and so on until auto-1 is renamed to auto-2.
    """

    for count in range(1, count + 1):
        if not os.path.exists(renpy.config.savedir + "/" + name + str(count) + savegame_suffix):
            break

    for i in range(count - 1, 0, -1):
        rename_save(name + str(i), name + str(i + 1))

################################################################################
# Cache
################################################################################

# None is a possible value for some of the attributes.
unknown = object()

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

        if self.mtime is unknown:
            self.mtime = location.mtime(self.slotname)

        return self.mtime

    def get_json(self):

        if self.json is unknown:
            self.json = location.json(self.slotname)

        return self.json

    def get_screenshot(self):

        if self.screenshot is unknown:
            self.screenshot = location.screenshot(self.slotname)

        return self.screenshot

# A map from slotname to cache object. This is used to cache savegame scan
# data until the slot changes.
cache = { }

def get_cache(slotname):
    if slotname in cache:
        return cache[slotname]

    rv = Cache(slotname)
    cache[slotname] = rv
    return rv


################################################################################
# Save Locations
################################################################################


# Save locations are places where saves are saved to or loaded from, or a
# collection of such locations.

# The default location.
location = None

class FileLocation(object):
    """
    A location that saves files to a directory on disk.
    """

    def __init__(self, directory):
        self.directory = directory

        # Make the save directory.
        try:
            os.makedirs(self.directory)
        except:
            pass

        # Try to write a test file.
        try:
            fn = os.path.join(self.directory, "text.txt")

            with open(fn, "w") as f:
                f.write("Test.")

            os.unlink(fn)

            self.active = True
        except:
            self.active = False

    def filename(self, slotname):
        """
        Given a slot name, returns a filename.
        """

        return os.path.join(self.directory, slotname + renpy.savegame_suffix)

    def save(self, slotname, record):
        """
        Saves the save record in slotname.
        """

        filename = self.filename(slotname)

        try:
            os.unlink(filename)
        except:
            pass

        record.write_file(filename)

    def list(self):
        """
        Returns a list of all slots with savefiles in them, in arbitrary
        order.
        """

        rv = [ ]

        suffix = renpy.savegame_suffix
        suffix_len = len(suffix)

        for i in os.listdir(self.directory):
            if not i.endswith(suffix):
                continue

            rv.append(i[:-suffix_len])

        return rv

    def mtime(self, slotname):
        """
        For a slot, returns the time the object was saved in that
        slot.

        Returns None if the slot is empty.
        """

        filename = self.filename(slotname)

        try:
            return os.path.getmtime(filename)
        except:
            return None


    def json(self, slotname):
        """
        Returns the JSON data for slotname.

        Returns None if the slot is empty.
        """


        try:
            filename = self.filename(slotname)
            zf = zipfile.ZipFile(filename, "r")
        except:
            return None

        try:

            try:
                data = zf.read("json")
                data = json.loads(data)
                return data
            except:
                pass

            try:
                extra_info = zf.read("extra_info").decode("utf-8")
                return { "_save_name" : extra_info }
            except:
                pass

            return { }

        finally:
            zf.close()


    def screenshot(self, slotname):
        """
        Returns a displayable that show the screenshot for this slot.

        Returns None if the slot is empty.
        """

        mtime = self.mtime(slotname)

        if mtime is None:
            return None

        filename = self.filename(slotname)

        zf = zipfile.ZipFile(filename, "r")

        try:
            png = False
            zf.getinfo('screenshot.tga')
        except:
            png = True
            zf.getinfo('screenshot.png')

        zf.close()

        if png:
            screenshot = renpy.display.im.ZipFileImage(filename, "screenshot.png", mtime)
        else:
            screenshot = renpy.display.im.ZipFileImage(filename, "screenshot.tga", mtime)

        return screenshot




    def __eq__(self, other):
        if not isinstance(other, FileLocation):
            return False

        return self.directory == other.directory

class MultiLocation(object):
    """
    A location that saves in multiple places. When loading or otherwise
    accessing a file, it loads the newest file found for the given slotname.
    """

    def __init__(self):
        self.locations = [ ]

    def active_locations(self):
        return [ i for i in self.locations if i.active ]

    def newest(self, slotname):
        """
        Returns the location containing the slotname with the newest
        mtime. Returns None of the slot is empty.
        """

        mtime = -1
        location = None

        for l in self.locations:
            if not l.active:
                continue

            slot_mtime = l.mtime(slotname)

            if slot_mtime > mtime:
                mtime = slot_mtime
                location = l

        return location

    def add(self, location):
        """
        Adds a new location.
        """

        if location in self.locations:
            return

        self.locations.append(location)

    def save(self, slotname, record):

        saved = False

        for l in self.active_locations():
            l.save(slotname, record)
            saved = True

        if not saved:
            raise Exception("Not saved - no valid save locations.")

    def list(self):
        rv = set()

        for l in self.active_locations():
            rv.update(l.list())

        return list(rv)

    def mtime(self, slotname):
        l = self.newest(slotname)

        if l is None:
            return None

        return l.mtime(slotname)

    def json(self, slotname):
        l = self.newest(slotname)

        if l is None:
            return None

        return l.json(slotname)


    def screenshot(self, slotname):
        l = self.newest(slotname)

        if l is None:
            return None

        return l.screenshot(slotname)

    def __eq__(self, other):
        if not isinstance(other, MultiLocation):
            return False

        return self.locations == other.locations


def init_location():
    global location

    location = MultiLocation()

    # 1. User savedir.
    location.add(FileLocation(renpy.config.savedir))

    # 2. Game-local savedir. (TODO: Check to see if writable.)
    path = os.path.join(renpy.config.gamedir, "saves")
    location.add(FileLocation(path))


