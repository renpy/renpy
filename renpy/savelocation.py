# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This contains code for different save locations. A save location is a place
# where we store save data, and can retrieve it from.
#
# The current save location is stored in the location variable in loadsave.py.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import os
import zipfile
import json

import renpy
import threading

from renpy.loadsave import clear_slot, safe_rename
import shutil

disk_lock = threading.RLock()

# A suffix used to disambguate temporary files being written by multiple
# processes.
import time
tmp = "." + str(int(time.time())) + ".tmp"


# The number of times pause_syncfs has been called, without a corresponding
# resume_syncfs
pause_syncfs_count = 0

def pause_syncfs():
    """
    Pauses the filesystem sync. This should be called before doing a large
    number of file operations.
    """

    global pause_syncfs_count
    pause_syncfs_count += 1


def resume_syncfs():
    """
    Resumes the filesystem sync. This should be called after a corresponding
    pause_syncfs.
    """

    global pause_syncfs_count
    pause_syncfs_count -= 1

    if pause_syncfs_count == 0:
        syncfs()


class SyncfsLock(object):
    """
    Context to pause then resume the filesystem sync.
    """
    def __enter__(self):
        pause_syncfs()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        resume_syncfs()


def syncfs():
    """
    Syncs the filesystem.
    """

    if pause_syncfs_count > 0:
        return

    if renpy.emscripten:
        import emscripten # type: ignore
        emscripten.syncfs()


class FileLocation(object):
    """
    A location that saves files to a directory on disk.
    """

    def __init__(self, directory):
        self.directory = directory

        # Make the save directory.
        try:
            os.makedirs(self.directory)
        except Exception:
            pass

        renpy.util.expose_directory(self.directory)

        # Try to write a test file.
        try:
            fn = os.path.join(self.directory, "text.txt")

            with open(fn, "w") as f:
                f.write("Test.")

            os.unlink(fn)

            self.active = True
        except Exception:
            self.active = False

        # A map from slotname to the mtime of that slot.
        self.mtimes = { }

        # The persistent file.
        self.persistent = os.path.join(self.directory, "persistent")

        # The mtime of the persistent file.
        self.persistent_mtime = 0

        # The data loaded from the persistent file.
        self.persistent_data = None

    def filename(self, slotname):
        """
        Given a slot name, returns a filename.
        """

        return os.path.join(self.directory, renpy.exports.fsencode(slotname + renpy.savegame_suffix))

    def sync(self):
        """
        Called to indicate that the HOME filesystem was changed.
        """

        syncfs()

    def scan(self):
        """
        Scan for files that are added or removed.
        """

        if not self.active:
            return

        with disk_lock:

            old_mtimes = self.mtimes
            new_mtimes = { }

            suffix = renpy.savegame_suffix
            suffix_len = len(suffix)

            for fn in os.listdir(self.directory):
                if not fn.endswith(suffix):
                    continue

                slotname = fn[:-suffix_len]

                try:
                    new_mtimes[slotname] = os.path.getmtime(os.path.join(self.directory, fn))
                except Exception:
                    pass

            self.mtimes = new_mtimes

            for slotname, mtime in new_mtimes.items():
                if old_mtimes.get(slotname, None) != mtime:
                    clear_slot(slotname)

            for slotname in old_mtimes:
                if slotname not in new_mtimes:
                    clear_slot(slotname)

            for pfn in [ self.persistent + ".new", self.persistent ]:
                if os.path.exists(pfn):
                    mtime = os.path.getmtime(pfn)

                    if mtime != self.persistent_mtime:
                        data = renpy.persistent.load(pfn)
                        if data is not None:
                            self.persistent_mtime = mtime
                            self.persistent_data = data
                            break

    def save(self, slotname, record):
        """
        Saves the save record in slotname.
        """

        filename = self.filename(slotname)

        with disk_lock:
            record.write_file(filename)

        renpy.util.expose_file(filename)

        self.sync()
        self.scan()

    def list(self):
        """
        Returns a list of all slots with savefiles in them, in arbitrary
        order.
        """

        return list(self.mtimes)

    def list_files(self):
        """
        Returns a list of all the actual save files.
        """

        rv = [ ]

        for slotname in self.list():
            rv.append(self.filename(slotname))

        return rv

    def mtime(self, slotname):
        """
        For a slot, returns the time the object was saved in that
        slot.

        Returns None if the slot is empty.
        """

        return self.mtimes.get(slotname, None)

    def path(self, filename):
        """
        Returns the mtime and path of the given filename, or (0, None) if
        the file does not exist.
        """

        with disk_lock:

            fn = os.path.join(self.directory, filename)

            try:
                return os.path.getmtime(fn), fn
            except Exception:
                return 0, None

    def json(self, slotname):
        """
        Returns the JSON data for slotname.

        Returns None if the slot is empty.
        """

        with disk_lock:

            try:
                filename = self.filename(slotname)
                with zipfile.ZipFile(filename, "r") as zf:
                    try:
                        data = zf.read("json")
                        data = json.loads(data)
                        return data
                    except Exception:
                        pass

                    try:
                        extra_info = zf.read("extra_info").decode("utf-8")
                        return { "_save_name" : extra_info }
                    except Exception:
                        pass

                    return { }
            except Exception:
                return None

    def screenshot(self, slotname):
        """
        Returns a displayable that show the screenshot for this slot.

        Returns None if the slot is empty.
        """

        with disk_lock:

            mtime = self.mtime(slotname)

            if mtime is None:
                return None

            try:
                filename = self.filename(slotname)
                with zipfile.ZipFile(filename, "r") as zf:
                    try:
                        png = False
                        zf.getinfo('screenshot.tga')
                    except Exception:
                        png = True
                        zf.getinfo('screenshot.png')
            except Exception:
                return None

            if png:
                screenshot = renpy.display.im.ZipFileImage(filename, "screenshot.png", mtime)
            else:
                screenshot = renpy.display.im.ZipFileImage(filename, "screenshot.tga", mtime)

            return screenshot

    def load(self, slotname):
        """
        Returns the log and signature components of the file found in `slotname`
        """

        with disk_lock:

            filename = self.filename(slotname)

            with zipfile.ZipFile(filename, "r") as zf:
                log = zf.read("log")

                try:
                    token = zf.read("signatures").decode("utf-8")
                except:
                    token = ''

            return log, token

    def unlink(self, slotname):
        """
        Deletes the file in slotname.
        """

        with disk_lock:

            filename = self.filename(slotname)
            if os.path.exists(filename):
                os.unlink(filename)

            self.sync()
            self.scan()

    def rename(self, old, new):
        """
        If old exists, renames it to new.
        """

        with disk_lock:

            old = self.filename(old)
            new = self.filename(new)

            if not os.path.exists(old):
                return

            old_tmp = old + tmp
            safe_rename(old, old_tmp)
            safe_rename(old_tmp, new)
            renpy.util.expose_file(new)

            self.sync()
            self.scan()

    def copy(self, old, new):
        """
        Copies `old` to `new`, if `old` exists.
        """

        with disk_lock:
            old = self.filename(old)
            new = self.filename(new)

            if not os.path.exists(old):
                return

            shutil.copyfile(old, new)
            renpy.util.expose_file(new)

            self.sync()
            self.scan()

    def load_persistent(self):
        """
        Returns a list of (mtime, persistent) tuples loaded from the
        persistent file. This should return quickly, with the actual
        load occuring in the scan thread.
        """

        if self.persistent_data:
            return [ (self.persistent_mtime, self.persistent_data) ]
        else:
            return [ ]

    def save_persistent(self, data):
        """
        Saves `data` as the persistent data. Data is a binary string giving
        the persistent data in python format.
        """

        with disk_lock:

            if not self.active:
                return

            fn = self.persistent
            fn_tmp = fn + tmp
            fn_new = fn + ".new"

            pause_syncfs()

            with open(fn_tmp, "wb") as f:
                f.write(data)

            safe_rename(fn_tmp, fn_new)
            safe_rename(fn_new, fn)

            # Prevent persistent from unpickle just after save
            self.persistent_mtime = os.path.getmtime(fn)

            renpy.util.expose_file(fn)

            resume_syncfs()

    def unlink_persistent(self):

        if not self.active:
            return

        try:
            os.unlink(self.persistent)

            self.sync()
        except Exception:
            pass

    def __eq__(self, other):
        if not isinstance(other, FileLocation):
            return False

        return self.directory == other.directory

    def __ne__(self, other):
        return not (self == other)


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
        mtime. Returns None if the slot is empty.
        """

        if not renpy.config.save:
            return None

        mtime = -1
        location = None

        for l in self.locations:
            if not l.active:
                continue

            slot_mtime = l.mtime(slotname)

            if slot_mtime is not None:
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

        if not renpy.config.save:
            return

        saved = False

        with SyncfsLock():
            for l in self.active_locations():
                l.save(slotname, record)
                saved = True

        if not saved:
            raise Exception("Not saved - no valid save locations.")

    def list(self):
        if not renpy.config.save:
            return [ ]

        rv = set()

        for l in self.active_locations():
            rv.update(l.list())

        return list(rv)

    def list_files(self):

        if not renpy.config.save:
            return [ ]

        rv = [ ]

        for l in self.active_locations():
            rv.extend(l.list_files())

        return rv

    def path(self, filename):

        results = [ ]

        for i in self.active_locations():
            results.append(i.path(filename))

        if not results:
            return 0, None

        results.sort()
        return results[-1]

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

    def load(self, slotname):
        l = self.newest(slotname)
        return l.load(slotname) # type: ignore

    def unlink(self, slotname):
        if not renpy.config.save:
            return

        with SyncfsLock():
            for l in self.active_locations():
                l.unlink(slotname)

    def rename(self, old, new):
        if not renpy.config.save:
            return

        with SyncfsLock():
            for l in self.active_locations():
                l.rename(old, new)

    def copy(self, old, new):
        if not renpy.config.save:
            return

        with SyncfsLock():
            for l in self.active_locations():
                l.copy(old, new)

    def load_persistent(self):
        rv = [ ]

        for l in self.active_locations():
            rv.extend(l.load_persistent())

        return rv

    def save_persistent(self, data):
        with SyncfsLock():
            for l in self.active_locations():
                l.save_persistent(data)

    def unlink_persistent(self):
        with SyncfsLock():
            for l in self.active_locations():
                l.unlink_persistent()

    def scan(self):
        # This should scan everything, as a scan can help decide if a
        # location should become active or inactive.

        for l in self.locations:
            l.scan()

    def __eq__(self, other):
        if not isinstance(other, MultiLocation):
            return False

        return self.locations == other.locations

    def __ne__(self, other):
        return not (self == other)


# The thread that scans locations every few seconds.
scan_thread = None

# True if we should quit the scan thread.
quit_scan_thread = False

# The condition we wait on.
scan_thread_condition = threading.Condition()


def run_scan_thread():
    global quit_scan_thread

    quit_scan_thread = False

    while not quit_scan_thread:

        try:
            renpy.loadsave.location.scan() # @UndefinedVariable
        except Exception:
            pass

        with scan_thread_condition:
            scan_thread_condition.wait(5.0)


def quit(): # @ReservedAssignment
    global quit_scan_thread

    with scan_thread_condition:
        quit_scan_thread = True
        scan_thread_condition.notify_all()

    if scan_thread is not None:
        scan_thread.join()


def init():
    global scan_thread
    global quit_scan_thread

    quit()
    quit_scan_thread = False

    location = MultiLocation()

    # 1. User savedir.
    location.add(FileLocation(renpy.config.savedir))

    # 2. Game-local savedir.
    if (not renpy.mobile) and (not renpy.macapp):
        path = os.path.join(renpy.config.gamedir, "saves")
        location.add(FileLocation(path))

    # 3. Extra savedirs.
    for i in renpy.config.extra_savedirs:
        location.add(FileLocation(i))

    # Scan the location once.
    location.scan()

    renpy.loadsave.location = location

    if not renpy.emscripten:
        scan_thread = threading.Thread(target=run_scan_thread)
        scan_thread.start()


def zip_saves():
    """
    This is called directly from Javascript, to zip up the savegames
    to /savegames.zip.
    """

    import zipfile
    import pathlib

    p = pathlib.Path(renpy.config.savedir)  # type: ignore

    with zipfile.ZipFile("savegames.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for fn in p.rglob("*"):
            zf.write(fn, fn.relative_to(p))

    return True


def unzip_saves():

    import zipfile
    import pathlib

    p = pathlib.Path(renpy.config.savedir)  # type: ignore

    with zipfile.ZipFile("savegames.zip", "r") as zf:

        for i in zf.infolist():
            if "/" not in i.filename:
                filename = i.filename
            else:
                prefix, _, filename = i.filename.partition("/")

                if (not renpy.config.save_directory) or (prefix != renpy.config.save_directory):
                    continue

            data = zf.read(i)

            with open(p / filename, "wb") as f:
                f.write(data)

    return True
