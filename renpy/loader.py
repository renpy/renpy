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

from typing import Iterable, Literal, NamedTuple

import renpy
import os
import os.path
import sys
import threading
import zlib
import re
import io
import unicodedata
import time
import pathlib
import contextlib
import functools


from renpy.pygame.rwobject import RWopsIO

from renpy.compat.pickle import loads
from renpy.webloader import DownloadNeeded

from bisect import bisect_left, bisect_right
from pathlib import Path, PosixPath, PurePosixPath, _make_selector
from typing import Generator, IO, Any, Iterator


# Ensure the utf-8 codec is loaded, to prevent recursion when we use it
# to look up filenames.
"".encode("utf-8")

# Physical Paths


def get_path(fn):
    """
    Returns the path to `fn` relative to the gamedir. If any of the directories
    leading to `fn` do not exist, tries to create them.

    This always returns a path, but the path may or may not be writable.
    """

    fn = os.path.join(renpy.config.gamedir, fn)
    dn = os.path.dirname(fn)

    try:
        if not os.path.exists(dn):
            os.makedirs(dn)
    except Exception:
        pass

    return fn


# Asset Loading

apks = []
game_apks = []
split_apks = []

def find_apks() -> None:
    """
    Finds APKs to load data from, and adds them to apks, game_apks, and
    split_apks.
    """

    if apks:
        return

    import android.apk  # type: ignore

    packs = [
        os.environ[i]
        for i in ["ANDROID_PACK_FF" + str(j + 1) for j in range(4)]
        if i in os.environ and os.environ[i].endswith(".apk")
    ]

    if renpy.config.renpy_base == renpy.config.basedir:
        # Read the game data from the APKs.

        apks.append(android.apk.APK(prefix="assets/x-game/"))
        game_apks.append(apks[-1])
        for i in packs:
            apks.append(android.apk.APK(apk=i, prefix="assets/game/"))
            game_apks.append(apks[-1])
            split_apks.append(apks[-1])

    apks.append(android.apk.APK(prefix="assets/x-renpy/x-common/"))
    for i in packs:
        apks.append(android.apk.APK(apk=i, prefix="assets/renpy/common/"))
        split_apks.append(apks[-1])


# Files on disk should be checked before archives. Otherwise, among
# other things, using a new version of bytecode.rpyb will break.
archives = []

# A map from lower-case filename to regular-case filename.
lower_map: dict[str, str] = {}


class ArchiveHandlers:
    def __init__(self):
        self.exts = {}
        self.peek = {}

    def append(self, handler):
        candidates = []
        header_sizes = []

        for header in handler.get_supported_headers():
            candidates.append((header, handler))
            header_sizes.append(len(header))

        peek = max(header_sizes)

        for ext in handler.get_supported_extensions():
            self.exts.setdefault(ext, []).extend(candidates)
            self.peek[ext] = max(self.peek.get(ext, 0), peek)

    def spec(self, ext):
        return self.peek[ext], self.exts[ext]


# A list containing archive handlers.
archive_handlers = ArchiveHandlers()


class RPAv3ArchiveHandler(object):
    """
    Archive handler handling RPAv3 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [".rpa"]

    @staticmethod
    def get_supported_headers():
        return [b"RPA-3.0 "]

    @staticmethod
    def read_index(infile):
        l = infile.read(40)
        offset = int(l[8:24], 16)
        key = int(l[25:33], 16)
        infile.seek(offset)
        index = loads(zlib.decompress(infile.read()))

        def start_to_bytes(s):
            if not s:
                return b""

            if not isinstance(s, bytes):
                s = s.encode("latin-1")

            return s

        # Deobfuscate the index.

        for k in index.keys():
            if len(index[k][0]) == 2:
                index[k] = [(offset ^ key, dlen ^ key) for offset, dlen in index[k]]
            else:
                index[k] = [(offset ^ key, dlen ^ key, start_to_bytes(start)) for offset, dlen, start in index[k]]

        return index


archive_handlers.append(RPAv3ArchiveHandler)


class RPAv2ArchiveHandler(object):
    """
    Archive handler handling RPAv2 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [".rpa"]

    @staticmethod
    def get_supported_headers():
        return [b"RPA-2.0 "]

    @staticmethod
    def read_index(infile):
        l = infile.read(24)
        offset = int(l[8:], 16)
        infile.seek(offset)
        index = loads(zlib.decompress(infile.read()))

        return index


archive_handlers.append(RPAv2ArchiveHandler)


class RPAv1ArchiveHandler(object):
    """
    Archive handler handling RPAv1 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [".rpi"]

    @staticmethod
    def get_supported_headers():
        return [b"\x78\x9c"]

    @staticmethod
    def read_index(infile):
        return loads(zlib.decompress(infile.read()))


archive_handlers.append(RPAv1ArchiveHandler)


def index_files():
    """
    Bootstraps the various file indexes.
    """

    arc_files.clear()
    common_files.clear()
    game_files.clear()
    lower_map.clear()

    if renpy.android:
        find_apks()

    for _dir, fn in listdirfiles():
        lower_map[unicodedata.normalize("NFC", fn.lower())] = fn

    for fn in remote_files:
        lower_map[unicodedata.normalize("NFC", fn.lower())] = fn


def index_archives():
    """
    Loads in the indexes for the archive files.
    """

    arc_files.sort(reverse=True)

    archives.clear()
    renpy.config.archives.clear()

    for stem, ext, fn in arc_files:
        with open(fn, "rb") as f:
            peek, handlers = archive_handlers.spec(ext)
            file_header = f.read(peek)

            for header, handler in handlers:
                if not file_header.startswith(header):
                    continue

                f.seek(0, 0)
                index = handler.read_index(f)
                archives.append((fn, index))
                break

        renpy.config.archives.append(stem)


def walkdir(path, elide=None):
    if elide is None:
        # Only existence check the top level for speed.
        if not os.path.exists(path) and not renpy.config.developer:
            return

        path = os.path.normpath(path)
        elide = len(path) + 1

    for de in os.scandir(path):
        if de.name[0] == ".":
            continue

        if de.is_dir():
            yield from walkdir(de.path, elide)
        else:
            yield de.path[elide:].replace("\\", "/")


# A list of files that are recognised as archives.
arc_files = []

# A list of files that are in the common directory.
common_files: list[tuple[str, str]] = []

# A list of files that make up the game.
game_files: list[tuple[str, str]] = []

# A map from filename to if the file is loadable.
loadable_cache = {}

# A map from filename to if the file is downloadable.
remote_files = {}


# A list of callbacks to fill out the lists above.
scandirfiles_callbacks = []


type TreeEntry = dict[str, "TreeEntry"] | Literal[True]
tree: TreeEntry = {}
"""This is a tree of files and directories, used to allow resource traversal. directories are represented as
   dicts, and files as True."""


def scandirfiles():
    """
    Scans directories, archives, and apks and fills out game_files and
    common_files.
    """

    seen = set()

    def add(dn, fn, files, seen):
        fn = str(fn)

        if fn in seen:
            return

        if fn.startswith("cache/"):
            return

        if fn.startswith("saves/"):
            return

        files.append((dn, fn))
        seen.add(fn)
        loadable_cache[unicodedata.normalize("NFC", fn.lower())] = True

        # Build the tree used to traverse files.

        parts = fn.split("/")
        rest = parts[-1]
        first = parts[:-1]

        t = tree
        for i in first:
            assert t is not True

            if (i not in t) or (t[i] is True):
                t[i] = {}

            t = t[i]

        assert t is not True
        t[rest] = True

    for i in scandirfiles_callbacks:
        i(add, seen)

    from operator import itemgetter
    def rpy_path_normalize_file_list(fn):
        return tuple(sorted(map(normalize_renpy_path, map(itemgetter(1), fn))))

    RenpyPath._paths = rpy_path_normalize_file_list(game_files)
    RenpyCommonPath._paths = rpy_path_normalize_file_list(common_files)
    pos = bisect_left(RenpyPath._paths, RenpyCommonPath._paths[0])
    RenpyAllPath._paths = RenpyPath._paths[:pos] + RenpyCommonPath._paths + RenpyPath._paths[pos:]


def scandirfiles_from_apk(add, seen):
    """
    Scans apks and fills out game_files and common_files.
    """

    for apk in apks:
        if apk not in game_apks:
            files = common_files
        else:
            files = game_files

        for f in apk.list():
            # Strip off the "x-" in front of each filename, which is there
            # to ensure that aapt actually includes every file.
            if apk not in split_apks:
                f = "/".join(i[2:] for i in f.split("/"))

            add(None, f, files, seen)


if renpy.android:
    scandirfiles_callbacks.append(scandirfiles_from_apk)


def scandirfiles_from_remote_file(add, seen):
    """
    Fills out game_files from renpyweb_remote_files.txt.
    """

    # HTML5 remote files
    index_filename = os.path.join(renpy.config.gamedir, "renpyweb_remote_files.txt")
    if os.path.exists(index_filename):
        files = game_files
        with open(index_filename, "r") as remote_index:
            while True:
                f = remote_index.readline()
                metadata = remote_index.readline()
                if f == "" or metadata == "":  # end of file
                    break

                f = f.rstrip("\r\n")
                metadata = metadata.rstrip("\r\n")
                (entry_type, entry_size) = metadata.split(" ")
                if entry_type == "image":
                    entry_size = [int(i) for i in entry_size.split(",")]

                add("/game", f, files, seen)
                remote_files[f] = {"type": entry_type, "size": entry_size}


if renpy.emscripten or os.environ.get("RENPY_SIMULATE_DOWNLOAD", False):
    scandirfiles_callbacks.append(scandirfiles_from_remote_file)


def scandirfiles_from_filesystem(add, seen):
    """
    Scans directories and fills out arc_files, game_files, and common_files.
    """

    exts = archive_handlers.exts

    for i in renpy.config.searchpath:
        if i == renpy.config.commondir:
            files = common_files
        else:
            files = game_files

        i = os.path.join(renpy.config.basedir, i)

        for j in walkdir(i):
            # Use rpartition as much faster than pathlib and splitext.
            stem, _, ext = j.rpartition(".")
            ext = "." + ext

            if ext in exts:
                arc_files.append((stem, ext, f"{i}/{j}"))
            else:
                add(i, j, files, seen)


scandirfiles_callbacks.append(scandirfiles_from_filesystem)


def scandirfiles_from_archives(add, seen):
    """
    Scans archives and fills out game_files.
    """

    if arc_files and not archives:
        index_archives()

    files = game_files

    for _fn, index in archives:
        for j in index:
            add(None, j, files, seen)


scandirfiles_callbacks.append(scandirfiles_from_archives)


def listdirfiles(common=True, game=True):
    """
    Returns a list of directory, file tuples known to the system. If
    the file is in an archive, the directory is None.
    """

    if (not game_files) and (not common_files):
        scandirfiles()

    rv = []

    if common:
        rv.extend(common_files)
    if game:
        rv.extend(game_files)

    return rv


open_file = RWopsIO  # type: ignore

if "RENPY_TEST_RWOPS" in os.environ:

    def open_file(name, mode):
        with RWopsIO(name, mode) as f:
            data = f.read(1024)
            f.seek(0, 2)
            length = f.tell()

        try:
            a = RWopsIO.from_buffer(data, name=name)

            if length <= 1024:
                return a

            b = RWopsIO(name, mode, base=1024, length=length - 1024)
            rv = RWopsIO.from_split(a, b, name=name)
            return rv

        except Exception:
            import traceback

            traceback.print_exc()


# A list of callbacks to open an open python file object of the given type.
file_open_callbacks = []


def load_core(name):
    """
    Returns an open python file object of the given type.
    """

    name = lower_map.get(unicodedata.normalize("NFC", name.lower()), name)

    for i in file_open_callbacks:
        rv = i(name)
        if rv is not None:
            return rv

    return None


def load_from_file_open_callback(name):
    """
    Returns an open python file object of the given type from the file open callback.
    """

    if renpy.config.file_open_callback:
        return renpy.config.file_open_callback(name)

    return None


file_open_callbacks.append(load_from_file_open_callback)


def load_from_filesystem(name):
    """
    Returns an open python file object of the given type from the filesystem.
    """

    if not renpy.config.force_archives:
        try:
            fn = transfn(name)
            return open_file(fn, "rb")
        except Exception:
            pass

    return None


file_open_callbacks.append(load_from_filesystem)


def load_from_archive(name):
    """
    Returns an open python file object of the given type from an archive file.
    """
    for afn, index in archives:
        if not name in index:
            continue

        data = []

        # Direct path.
        if len(index[name]) == 1:
            t = index[name][0]
            if len(t) == 2:
                offset, dlen = t
                start = b""
            else:
                offset, dlen, start = t

            if start == None or len(start) == 0:
                rv = RWopsIO(afn, "rb", base=offset, length=dlen)
                return io.BufferedReader(rv)
            else:
                a = RWopsIO.from_buffer(start, name=name)
                b = RWopsIO(afn, "rb", base=offset, length=dlen)
                rv = RWopsIO.from_split(a, b, name=name)
                rv = io.BufferedReader(rv)

        # Compatibility path.
        else:
            with open(afn, "rb") as f:
                for offset, dlen in index[name]:
                    f.seek(offset)
                    data.append(f.read(dlen))

                return io.BufferedReader(RWopsIO.from_buffer(b"".join(data), name=name))

    return None


file_open_callbacks.append(load_from_archive)


def load_from_apk(name):
    """
    Returns an open python file object of the given type from the apk.
    """

    for apk in apks:
        prefixed_name = name
        if apk not in split_apks:
            prefixed_name = "/".join("x-" + i for i in name.split("/"))

        try:
            return apk.open(prefixed_name)
        except IOError:
            pass

    return None


if renpy.android:
    file_open_callbacks.append(load_from_apk)


def load_from_remote_file(name):
    """
    Defer loading a file if it has not been downloaded yet but exists on the remote server.
    """

    if name in remote_files:
        raise DownloadNeeded(relpath=name, rtype=remote_files[name]["type"], size=remote_files[name]["size"])

    return None


if renpy.emscripten or os.environ.get("RENPY_SIMULATE_DOWNLOAD", False):
    file_open_callbacks.append(load_from_remote_file)


def check_name(name):
    """
    Checks the name to see if it violates any of Ren'Py's rules.
    """

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    if renpy.config.reject_relative:
        split = name.split("/")

        if ("." in split) or (".." in split):
            raise Exception("Filenames may not contain relative directories like '.' and '..': %r" % name)


def get_prefixes(tl=True, directory=None):
    """
    Returns a list of prefixes to search for files.
    """

    rv = []

    if tl:
        language = renpy.game.preferences.language  # type: ignore
    else:
        language = None

    for prefix in renpy.config.search_prefixes:
        if language is not None:
            rv.append(renpy.config.tl_directory + "/" + language + "/" + prefix)

        rv.append(prefix)

    if directory is not None:

        for mapped_directory in renpy.config.special_directory_map.get(directory, [ directory ]):

            if language is not None:
                rv.append(renpy.config.tl_directory + "/" + language + "/" + mapped_directory + "/")

            rv.append(mapped_directory + "/")

    return rv


def load(name, directory=None, tl=True):
    if renpy.display.predict.predicting:
        if threading.current_thread().name == "MainThread":
            if not (renpy.emscripten or os.environ.get("RENPY_SIMULATE_DOWNLOAD", False)):
                raise Exception("Refusing to open {} while predicting.".format(name))

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    name = re.sub(r"/+", "/", name).lstrip("/")

    for p in get_prefixes(directory=directory, tl=tl):
        rv = load_core(p + name)
        if rv is not None:
            return rv

    raise FileNotFoundError("Couldn't find file '%s'." % name)


def loadable_core(name):
    """
    Returns True if the name is loadable with load, False if it is not.
    """

    name = lower_map.get(unicodedata.normalize("NFC", name.lower()), name)

    if name in loadable_cache:
        return loadable_cache[name]

    try:
        transfn(name)
        loadable_cache[name] = True
        return True
    except Exception:
        pass

    for apk in apks:
        prefixed_name = name
        if apk not in split_apks:
            prefixed_name = "/".join("x-" + i for i in name.split("/"))
        if prefixed_name in apk.info:
            loadable_cache[name] = True
            return True

    for _fn, index in archives:
        if name in index:
            loadable_cache[name] = True
            return True

    if name in remote_files:
        loadable_cache[name] = True
        return name

    loadable_cache[name] = False
    return False


def loadable(name, tl=True, directory=None):
    name = name.lstrip("/")

    if (renpy.config.loadable_callback is not None) and renpy.config.loadable_callback(name):
        return True

    for p in get_prefixes(tl=tl, directory=directory):
        if loadable_core(p + name):
            return True

    return False


def transpath(path: str) -> str|None:
    """
    Translates `path` to a name that exists in one of the searched directories,
    or to None if it does not exist.
    """

    path = path.lstrip("/")
    path = lower_map.get(unicodedata.normalize("NFC", path.lower()), path)

    for d in renpy.config.searchpath:
        fn = os.path.join(renpy.config.basedir, d, path)

        if os.path.isfile(fn):
            return fn


def transfn(name: bytes|str) -> str:
    """
    Tries to translate the name to a file that exists in one of the
    searched directories.
    """

    if isinstance(name, bytes):
        name = name.decode("utf-8")

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    path = transpath(name)

    if path is not None:
        add_auto(path)
        return path

    raise Exception("Couldn't find file '%s'." % name)


hash_cache = {}


def get_hash(name):  # type: (str) -> int
    """
    Returns the time the file m was last modified, or 0 if it
    doesn't exist or is archived.
    """

    rv = hash_cache.get(name, None)
    if rv is not None:
        return rv

    rv = 0

    try:
        f = load(name)

        while True:
            data = f.read(1024 * 1024)

            if not data:
                break

            rv = zlib.adler32(data, rv)

    except Exception:
        pass

    hash_cache[name] = rv

    return rv



# Auto-Reload


# A list of files for which autoreload is needed.
needs_autoreload = set()

# A map from filename to mtime, or None if the file doesn't exist.
auto_mtimes = {}

# The thread used for autoreload.
auto_thread = None

# True if auto_thread should run. False if it should quit.
auto_quit_flag = True

# The lock used by auto_thread.
auto_lock = threading.Condition()

# Used to indicate that this file is blacklisted.
auto_blacklisted = renpy.object.Sentinel("auto_blacklisted")


def auto_mtime(fn):
    """
    Gets the mtime of fn, or None if the file does not exist.
    """

    try:
        return os.path.getmtime(fn)
    except Exception:
        return None


def add_auto(fn, force=False):
    """
    Adds fn as a file we watch for changes. If it's mtime changes or the file
    stops existing, we trigger a reload.
    """

    if not renpy.autoreload:
        return

    if (fn in auto_mtimes) and (not force):
        return

    fn = fn.replace("\\", "/")

    if renpy.config.commondir and pathlib.Path(fn).is_relative_to(renpy.config.commondir):
        return

    for e in renpy.config.autoreload_blacklist:
        if fn.endswith(e):
            with auto_lock:
                auto_mtimes[fn] = auto_blacklisted
            return

    mtime = auto_mtime(fn)

    with auto_lock:
        auto_mtimes[fn] = mtime


max_mtime = 0


def auto_thread_function():
    """
    This thread sets need_autoreload when necessary.
    """

    global max_mtime

    while True:
        with auto_lock:
            auto_lock.wait(1.5)

            if auto_quit_flag:
                return

            items = list(auto_mtimes.items())

        for fn, mtime in items:
            if mtime is auto_blacklisted:
                continue

            new_mtime = auto_mtime(fn)

            if new_mtime is not None:
                max_mtime = max(max_mtime, new_mtime)

            if new_mtime != mtime:
                with auto_lock:
                    if auto_mtime(fn) != auto_mtimes[fn]:
                        needs_autoreload.add(fn)


def check_git_index_lock():
    """
    Checks to see if the git index lock is present.
    """

    to_check = set(os.path.dirname(i) for i in needs_autoreload)
    added = set(to_check)

    while to_check:
        dn = to_check.pop()

        if os.path.exists(os.path.join(dn, ".git", "index.lock")):
            return True

        parent = os.path.dirname(dn)
        if parent not in added:
            added.add(parent)
            to_check.add(os.path.dirname(dn))

    return False


# Are we actively reloading?
reloading = False


def check_autoreload():
    """
    Checks to see if autoreload is required.
    """

    global reloading

    if reloading:
        return

    # Defer loading while the git index lock is present.
    if needs_autoreload and check_git_index_lock():
        return

    if time.time() - max_mtime < 0.050:
        return

    while needs_autoreload:
        fn = next(iter(needs_autoreload))
        mtime = auto_mtime(fn)

        with auto_lock:
            needs_autoreload.discard(fn)
            auto_mtimes[fn] = mtime

        if not renpy.autoreload:
            return

        for regex, func in renpy.config.autoreload_functions:
            if re.search(regex, fn, re.I):
                fn = os.path.relpath(fn, renpy.config.gamedir).replace("\\", "/")
                func(fn)
                break
        else:
            reloading = True
            renpy.exports.reload_script()


def auto_init():
    """
    Starts the autoreload thread.
    """

    global auto_thread
    global auto_quit_flag
    global needs_autoreload

    needs_autoreload = set()

    if not renpy.autoreload:
        return

    auto_quit_flag = False

    if not renpy.emscripten:
        auto_thread = threading.Thread(target=auto_thread_function)
        auto_thread.daemon = True
        auto_thread.start()


def auto_quit():
    """
    Terminates the autoreload thread.
    """
    global auto_quit_flag

    if auto_thread is None:
        return

    auto_quit_flag = True

    with auto_lock:
        auto_lock.notify_all()

    auto_thread.join()


_FILE_SEPARATOR = '\x00'
_DIR_SEPARATOR = '\x01'

def normalize_renpy_path(path: str) -> str:
    """Convert unix path to alphabetically sortable path: 'a/b/c.txt' -> 'a\\x01b\\x00c.txt'"""
    parent, separator, name = path.rpartition('/')
    return parent.replace('/', _DIR_SEPARATOR) + _FILE_SEPARATOR + name

def denormalize_renpy_path(path: str) -> str:
    """Convert from alphabetically sortable path back to unix format: 'a\\x01b\\x00c.txt' -> 'a/b/c.txt'"""
    parent, separator, name = path.rpartition(_FILE_SEPARATOR)
    if not separator:
        return name.replace(_DIR_SEPARATOR, '/')
    if parent:
        return parent.replace(_DIR_SEPARATOR, '/') + '/' + name
    return name



class RenpyPathDirEntry:
    """Lightweight directory entry, analogous to os.DirEntry."""
    __slots__ = ('name', '_raw_path', '_is_dir', '_path')

    def __init__(self, raw_path: str, range_start: int, range_end: int, is_dir: bool, child_prefix_len: int, parent_prefix_len: int) -> None:
        self._raw_path = raw_path
        self._is_dir = is_dir
        self.name = raw_path[parent_prefix_len:]

    @property
    def path(self) -> str:
        try:
            return self._path
        except AttributeError:
            self._path = denormalize_renpy_path(self._raw_path)
            return self._path

    def is_dir(self, *, follow_symlinks: bool = True) -> bool:
        return self._is_dir

    def is_file(self, *, follow_symlinks: bool = True) -> bool:
        return not self._is_dir

    def is_symlink(self) -> bool:
        return False

    def __fspath__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"<VirtualDirEntry '{self.name}'>"



@functools.lru_cache(maxsize=32768, typed=True)
def _compile_pattern(pat, case_sensitive):
    from fnmatch import translate
    import re
    flags = re.NOFLAG if case_sensitive else re.IGNORECASE
    return re.compile(translate(pat), flags).match


type RenpyLoadableMode = Literal["r", "rb", "br"]

class RenpyPath(PurePosixPath):
    __slots__ = ('_range_start', '_range_end', '_is_dir', '_prefix_length', '_as_path')

    _paths: tuple[str, ...]
    _base = renpy.config.gamedir


    def _create(self, raw_path: str, range_start: int, range_end: int, is_dir: bool, child_prefix_len: int, parent_prefix_len: int | None = None) -> 'RenpyPath':

        if parent_prefix_len is not None:
            instance = self._from_parsed_parts('', '', self._tail_cached + [raw_path[parent_prefix_len:]])
        else:
            instance = self.with_segments(denormalize_renpy_path(raw_path))
        instance._range_start = range_start
        instance._range_end = range_end
        instance._is_dir = is_dir
        instance._prefix_length = child_prefix_len
        return instance

    @staticmethod
    def _detangle_tail(tail: list[str]) -> list[str]:
        skip_count = 0
        rv = []
        for e in tail[::-1]:
            if e == '..':
                skip_count += 1
            elif e == '.':
                continue
            elif skip_count > 0:
                skip_count -= 1
            else:
                rv.append(e)
        if skip_count > 0:
            return []

        rv.reverse()
        return rv


    def _find_ranges(self) -> None:
        tail = self._tail

        if '.' in tail or '..' in tail:
            tail = self._detangle_tail(tail)

        if len(tail) < 2 and (len(tail) == 0 or tail[0] == ''):
            self._prefix_length = 0
            self._range_start = 0
            self._range_end = len(self._paths)
            self._is_dir = True
            return

        file_key = _DIR_SEPARATOR.join(tail[:-1]) + _FILE_SEPARATOR + tail[-1]

        self._prefix_length = len(file_key.lstrip(_FILE_SEPARATOR))
        self._is_dir = False

        self._range_start = bisect_left(self._paths, file_key)
        try:
            if self._paths[self._range_start] == file_key:
                self._range_end = self._range_start + 1
                return
        except IndexError:
            self._range_end = self._range_start
            return

        dir_key = _DIR_SEPARATOR.join(tail)
        self._range_start = bisect_left(self._paths, dir_key + _FILE_SEPARATOR, self._range_start)
        self._range_end = bisect_right(self._paths, dir_key + '\x02', self._range_start)
        self._is_dir = self._range_start < self._range_end


    def exists(self, *, follow_symlinks: bool = True) -> bool:
        try:
            return self._range_start < self._range_end
        except AttributeError:
            self._find_ranges()
            return self._range_start < self._range_end

    def is_dir(self) -> bool:
        try:
            return self._is_dir
        except AttributeError:
            self._find_ranges()
            return self._is_dir

    def is_file(self) -> bool:
        try:
            return not self._is_dir and self._range_start + 1 == self._range_end
        except AttributeError:
            self._find_ranges()
            return not self._is_dir and self._range_start + 1 == self._range_end

    def is_remote_file(self):
        if not self.is_file():
            return False
        tail = self._tail
        if '.' in tail or '..' in tail:
            tail = self._detangle_tail(tail)
        return '/'.join(tail) in remote_files

    def samefile(self, other):
        try:
            # Ranges are fastest to compare but slowest to calculate
            return self is other or (
                self._range_start == other._range_start and
                self._range_end == other._range_end and
                self._prefix_length == other._prefix_length
            )
        except AttributeError:
            if self._raw_paths == other._raw_paths:
                return True
            return self.resolve()._tail == other.resolve()._tail


    def _iter_children(self, create):
        if not self.exists():
            raise FileNotFoundError(f"No such file or directory: '{self}'")
        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: '{self}'")

        prefix_length = self._prefix_length
        _paths = self._paths

        # Files: fn[prefix_length] == FILE_SEPARATOR
        file_i = self._range_start
        for file_i, fn in enumerate(_paths[self._range_start:self._range_end], start=self._range_start):
            if fn[prefix_length] != _FILE_SEPARATOR:
                break
            yield create(fn, file_i, file_i + 1, False, prefix_length, prefix_length + 1)

        if prefix_length:
            prefix_length += 1

        # Directories
        while file_i < self._range_end:
            fn = _paths[file_i]
            slash_pos = fn.find(_DIR_SEPARATOR, prefix_length)
            if slash_pos == -1:
                slash_pos = fn.find(_FILE_SEPARATOR, prefix_length)
                if slash_pos == -1:
                    break
            child_path = fn[:slash_pos]
            child_range_end = bisect_left(_paths, child_path + '\x02', file_i, self._range_end)
            yield create(child_path, file_i, child_range_end, True, len(child_path), prefix_length)
            file_i = child_range_end

    def iterdir(self) -> Generator['RenpyPath', None, None]:
        yield from self._iter_children(self._create)

    @contextlib.contextmanager
    def scandir(self) -> Generator[Iterator[RenpyPathDirEntry], None, None]:
        yield self._iter_children(RenpyPathDirEntry)

    _scandir = scandir

    def walk(self, top_down: bool = True, on_error=None, follow_symlinks: bool = False):
        if not self.is_dir():
            return

        dir_paths: list[RenpyPath] = []
        dir_names: list[str] = []
        file_names: list[str] = []

        for child in self.iterdir():
            if child.is_dir():
                dir_paths.append(child)
                dir_names.append(child.name)
            else:
                file_names.append(child.name)

        if top_down:
            yield self, dir_names, file_names
        for d in dir_paths:
            yield from d.walk(top_down=True, on_error=on_error)
        if not top_down:
            yield self, dir_names, file_names

    _make_child_relpath = Path._make_child_relpath

    def glob(self, pattern: str, *, case_sensitive: bool | None = None) -> Generator['RenpyPath', None, None]:
        if not self.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{self}'")
        if pattern == '*':
            yield from self.iterdir()
        elif pattern in ('**', '**/*'):
            yield from self.rglob('*', case_sensitive=case_sensitive)
        elif '*' not in pattern and '?' not in pattern:
            child = self / pattern
            if child.exists():
                yield child
        elif '**' not in pattern and '/' not in pattern:
            matcher = _compile_pattern(pattern, case_sensitive)
            with self.scandir() as entries:
                for entry in entries:
                    if matcher(entry.name):
                        yield self / entry.name
        else:
            yield from _make_selector(tuple(pattern.split('/')), self._flavour, case_sensitive).select_from(self)


    def rglob(self, pattern: str, *, case_sensitive: bool | None = None) -> Generator['RenpyPath', None, None]:
        """Direct tuple slice iteration - cache friendly and fast."""
        import fnmatch

        if not self.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{self}'")

        yield from _make_selector(("**",) + tuple(pattern.split('/')), self._flavour, case_sensitive).select_from(self)


    def is_absolute(self) -> bool:
        return False

    def as_path(self) -> Path:
        try:
            return self._as_path
        except AttributeError:
            pass

        # similar to transpath but not using transpath because requires support to directories
        path = str(self)
        path = Path(lower_map.get(unicodedata.normalize("NFC", path.lower()), path))
        base_path = Path(renpy.config.basedir)

        for d in renpy.config.searchpath:
            file_path = base_path / d / path

            if file_path.exists():
                self._as_path = file_path
                return self._as_path

        self._as_path = Path(self._base) / self
        return self._as_path


    def open(self, mode: RenpyLoadableMode = "r", *args, tl=False, **kwargs) -> io.BufferedReader | io.TextIOWrapper:  # type:ignore[reportIncompatibleMethodOverride]
        """
        Opens the resource for reading.
        """

        if not self.is_file():
            raise IsADirectoryError(f"Only files may be opened. A directory was provided instead: {str(self)}")

        f = renpy.loader.load(str(self), tl=tl)

        if 'b' in mode:
            return f
        else:
            return io.TextIOWrapper(f, *args, **kwargs)


    def read_text(self, encoding=None) -> str:
        with self.open("r", encoding=encoding) as f:
            assert isinstance(f, io.TextIOWrapper)
            return f.read()

    def read_bytes(self) -> bytes:
        with self.open("rb") as f:
            assert isinstance(f, io.BufferedReader)
            return f.read()

    def resolve(self, strict=False):
        tail = self._tail
        if '.' not in tail and '..' not in tail:
            return self

        tail = self._detangle_tail(tail)
        resolved_path: RenpyPath = self._from_parsed_parts('', '', tail)
        if not strict or os.path.ALLOW_MISSING:
            return resolved_path

        if not resolved_path.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{resolved_path}'")

        return resolved_path



    @classmethod
    def current_path_line(cls):
        from renpy.exports.debugexports import get_filename_line
        fn, line = get_filename_line()
        path = cls._from_parsed_parts('', '', os.path.split(fn))
        return path, line

    def rpy_path(self):
        if self.is_dir():
            raise IsADirectoryError(f"Directories are not python files and can't be rpyc. '{str(self)}' is a directory")

        if self.suffix in ('.rpy', '.rpym') or self.name.endswith('_ren.py'):
            return self

        if self.suffix not in (".rpyc", ".rpymc"):
            raise Exception(f"Only rpyc/rpymc files can have rpy/rpym/_ren.py counter-parts. '{str(self)}' is none of those")

        as_ren_py = self.with_name(self.stem + '_ren.py')

        if as_ren_py.exists():
            return as_ren_py

        without_c = self.with_suffix(self.suffix[:-1])
        return without_c

    def rpyc_path(self):

        if self.is_dir():
            raise IsADirectoryError(f"Directories are not python files and can't be rpy. '{str(self)}' is a directory")

        if self.suffix in ('.rpyc', '.rpymc'):
            return self

        name = self.name
        if self.suffix not in (".rpy", ".rpym") or not name.endswith('_ren.py'):
            raise Exception(f"Only rpy/rpym/_ren.py files can have rpyc counter-parts. '{str(self)}' is none of those")

        if name.endswith('_ren.py'):
            name = name[:-7] + '.rpy'

        return name + "c"

    def build_classify(self, file_list):
        from renpy import store

        pattern = '/'.join(self._parts)

        if self.is_dir():
            pattern += '/**'

        store.build.classify(pattern, file_list)


class RenpyCommonPath(RenpyPath):
    _base = renpy.config.commondir

class RenpyAllPath(RenpyPath):
    _base = renpy.config.basedir
