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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Optional

import renpy
import os
import os.path
import sys
import types
import threading
import zlib
import re
import io
import unicodedata

from pygame_sdl2.rwobject import RWopsIO

from renpy.compat.pickle import loads
from renpy.webloader import DownloadNeeded

# Ensure the utf-8 codec is loaded, to prevent recursion when we use it
# to look up filenames.
u"".encode(u"utf-8")

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

apks = [ ]
game_apks = [ ]

if renpy.android:
    import android.apk # type: ignore

    if renpy.config.renpy_base == renpy.config.basedir:
        # Read the game data from the APK.

        apks.append(android.apk.APK(prefix='assets/x-game/'))
        game_apks.append(apks[0])

    apks.append(android.apk.APK(prefix='assets/x-renpy/x-common/'))


# Files on disk should be checked before archives. Otherwise, among
# other things, using a new version of bytecode.rpyb will break.
archives = [ ]

# The value of renpy.config.archives the last time index_archives was
# run.
old_config_archives = None

# A map from lower-case filename to regular-case filename.
lower_map = { }

# A list containing archive handlers.
archive_handlers = [ ]


class RPAv3ArchiveHandler(object):
    """
    Archive handler handling RPAv3 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [ ".rpa" ]

    @staticmethod
    def get_supported_headers():
        return [ b"RPA-3.0 " ]

    @staticmethod
    def read_index(infile):
        l = infile.read(40)
        offset = int(l[8:24], 16)
        key = int(l[25:33], 16)
        infile.seek(offset)
        index = loads(zlib.decompress(infile.read()))

        def start_to_bytes(s):
            if not s:
                return b''

            if not isinstance(s, bytes):
                s = s.encode("latin-1")

            return s

        # Deobfuscate the index.

        for k in index.keys():

            if len(index[k][0]) == 2:
                index[k] = [ (offset ^ key, dlen ^ key) for offset, dlen in index[k] ]
            else:
                index[k] = [ (offset ^ key, dlen ^ key, start_to_bytes(start)) for offset, dlen, start in index[k] ]

        return index


archive_handlers.append(RPAv3ArchiveHandler)


class RPAv2ArchiveHandler(object):
    """
    Archive handler handling RPAv2 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [ ".rpa" ]

    @staticmethod
    def get_supported_headers():
        return [ b"RPA-2.0 " ]

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
        return [ ".rpi" ]

    @staticmethod
    def get_supported_headers():
        return [ b"\x78\x9c" ]

    @staticmethod
    def read_index(infile):
        return loads(zlib.decompress(infile.read()))


archive_handlers.append(RPAv1ArchiveHandler)


def index_archives():
    """
    Loads in the indexes for the archive files. Also updates the lower_map.
    """

    # Index the archives.

    global old_config_archives

    if old_config_archives == renpy.config.archives:
        return

    old_config_archives = renpy.config.archives[:]

    # Update lower_map.
    lower_map.clear()

    cleardirfiles()

    global archives
    archives = [ ]

    max_header_length = 0
    for handler in archive_handlers:
        for header in handler.get_supported_headers():
            header_len = len(header)
            if header_len > max_header_length:
                max_header_length = header_len

    archive_extensions = [ ]
    for handler in archive_handlers:
        for ext in handler.get_supported_extensions():
            if not (ext in archive_extensions):
                archive_extensions.append(ext)

    for prefix in renpy.config.archives:
        for ext in archive_extensions:
            fn = None
            f = None
            try:
                fn = transfn(prefix + ext)
                f = open(fn, "rb")
            except Exception:
                continue
            with f:
                file_header = f.read(max_header_length)
                for handler in archive_handlers:
                    archive_handled = False
                    for header in handler.get_supported_headers():
                        if file_header.startswith(header):
                            f.seek(0, 0)
                            index = handler.read_index(f)
                            archives.append((prefix + handler.archive_extension, index))
                            archive_handled = True
                            break
                    if archive_handled == True:
                        break

    for _dir, fn in listdirfiles():
        lower_map[unicodedata.normalize('NFC', fn.lower())] = fn

    for fn in remote_files:
        lower_map[unicodedata.normalize('NFC', fn.lower())] = fn


def walkdir(dir): # @ReservedAssignment
    rv = [ ]

    if not os.path.exists(dir) and not renpy.config.developer:
        return rv

    for i in os.listdir(dir):
        if i[0] == ".":
            continue

        try:
            i = renpy.exports.fsdecode(i)
        except Exception:
            continue

        if os.path.isdir(dir + "/" + i):
            for fn in walkdir(dir + "/" + i):
                rv.append(i + "/" + fn)
        else:
            rv.append(i)

    return rv


# A list of files that make up the game.
game_files = [ ]

# A list of files that are in the common directory.
common_files = [ ]

# A map from filename to if the file is loadable.
loadable_cache = { }

# A map from filename to if the file is downloadable.
remote_files = { }


def cleardirfiles():
    """
    Clears the lists above when the game has changed.
    """

    global game_files
    global common_files

    game_files = [ ]
    common_files = [ ]


# A list of callbacks to fill out the lists above.
scandirfiles_callbacks = [ ]


def scandirfiles():
    """
    Scans directories, archives, and apks and fills out game_files and
    common_files.
    """

    seen = set()

    def add(dn, fn, files, seen):

        fn = unicode(fn)

        if fn in seen:
            return

        if fn.startswith("cache/"):
            return

        if fn.startswith("saves/"):
            return

        files.append((dn, fn))
        seen.add(fn)
        loadable_cache[unicodedata.normalize('NFC', fn.lower())] = True

    for i in scandirfiles_callbacks:
        i(add, seen)


def scandirfiles_from_apk(add, seen):
    """
    Scans apks and fills out game_files and common_files.
    """

    for apk in apks:

        if apk not in game_apks:
            files = common_files # @UnusedVariable
        else:
            files = game_files # @UnusedVariable

        for f in apk.list():

            # Strip off the "x-" in front of each filename, which is there
            # to ensure that aapt actually includes every file.
            f = "/".join(i[2:] for i in f.split("/"))

            add(None, f, files, seen)


if renpy.android:
    scandirfiles_callbacks.append(scandirfiles_from_apk)


def scandirfiles_from_remote_file(add, seen):
    """
    Fills out game_files from renpyweb_remote_files.txt.
    """

    # HTML5 remote files
    index_filename = os.path.join(renpy.config.gamedir, 'renpyweb_remote_files.txt')
    if os.path.exists(index_filename):
        files = game_files
        with open(index_filename, 'r') as remote_index:
            while True:
                f = remote_index.readline()
                metadata = remote_index.readline()
                if f == '' or metadata == '': # end of file
                    break

                f = f.rstrip("\r\n")
                metadata = metadata.rstrip("\r\n")
                (entry_type, entry_size) = metadata.split(' ')
                if entry_type == 'image':
                    entry_size = [int(i) for i in entry_size.split(',')]

                add('/game', f, files, seen)
                remote_files[f] = {'type':entry_type, 'size':entry_size}


if renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False):
    scandirfiles_callbacks.append(scandirfiles_from_remote_file)


def scandirfiles_from_filesystem(add, seen):
    """
    Scans directories and fills out game_files and common_files.
    """

    for i in renpy.config.searchpath:

        if (renpy.config.commondir) and (i == renpy.config.commondir):
            files = common_files # @UnusedVariable
        else:
            files = game_files # @UnusedVariable

        i = os.path.join(renpy.config.basedir, i)
        for j in walkdir(i):
            add(i, j, files, seen)


scandirfiles_callbacks.append(scandirfiles_from_filesystem)


def scandirfiles_from_archives(add, seen):
    """
    Scans archives and fills out game_files.
    """

    files = game_files

    for _prefix, index in archives:
        for j in index:
            add(None, j, files, seen)


scandirfiles_callbacks.append(scandirfiles_from_archives)


def listdirfiles(common=True):
    """
    Returns a list of directory, file tuples known to the system. If
    the file is in an archive, the directory is None.
    """

    if (not game_files) and (not common_files):
        scandirfiles()

    if common:
        return game_files + common_files
    else:
        return list(game_files)



open_file = RWopsIO # type: ignore

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
file_open_callbacks = [ ]


def load_core(name):
    """
    Returns an open python file object of the given type.
    """

    name = lower_map.get(unicodedata.normalize('NFC', name.lower()), name)

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
    for prefix, index in archives:
        if not name in index:
            continue

        afn = transfn(prefix)

        data = [ ]

        # Direct path.
        if len(index[name]) == 1:

            t = index[name][0]
            if len(t) == 2:
                offset, dlen = t
                start = b''
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

                return io.BufferedReader(RWopsIO.from_buffer(b''.join(data), name=name))

    return None


file_open_callbacks.append(load_from_archive)


def load_from_apk(name):
    """
    Returns an open python file object of the given type from the apk.
    """

    for apk in apks:
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
        raise DownloadNeeded(relpath=name, rtype=remote_files[name]['type'], size=remote_files[name]['size'])

    return None


if renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False):
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

    rv = [ ]

    if tl:
        language = renpy.game.preferences.language # type: ignore
    else:
        language = None

    for prefix in renpy.config.search_prefixes:

        if language is not None:
            rv.append(renpy.config.tl_directory + "/" + language + "/" + prefix)

        rv.append(prefix)

    if directory is not None:

        if language is not None:
            rv.append(renpy.config.tl_directory + "/" + language + "/" + directory + "/")

        rv.append(directory + "/")

    return rv


def load(name, directory=None, tl=True):

    if renpy.display.predict.predicting: # @UndefinedVariable
        if threading.current_thread().name == "MainThread":
            if not (renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False)):
                raise Exception("Refusing to open {} while predicting.".format(name))

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    name = re.sub(r'/+', '/', name).lstrip('/')

    for p in get_prefixes(directory=directory, tl=tl):
        rv = load_core(p + name)
        if rv is not None:
            return rv

    raise IOError("Couldn't find file '%s'." % name)


def loadable_core(name):
    """
    Returns True if the name is loadable with load, False if it is not.
    """

    name = lower_map.get(unicodedata.normalize('NFC', name.lower()), name)

    if name in loadable_cache:
        return loadable_cache[name]

    try:
        transfn(name)
        loadable_cache[name] = True
        return True
    except Exception:
        pass

    for apk in apks:
        prefixed_name = "/".join("x-" + i for i in name.split("/"))
        if prefixed_name in apk.info:
            loadable_cache[name] = True
            return True

    for _prefix, index in archives:
        if name in index:
            loadable_cache[name] = True
            return True

    if name in remote_files:
        loadable_cache[name] = True
        return name

    loadable_cache[name] = False
    return False


def loadable(name, directory=None):

    name = name.lstrip('/')

    if (renpy.config.loadable_callback is not None) and renpy.config.loadable_callback(name):
        return True

    for p in get_prefixes(directory=directory):
        if loadable_core(p + name):
            return True

    return False


def transfn(name):
    """
    Tries to translate the name to a file that exists in one of the
    searched directories.
    """

    name = name.lstrip('/')

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    name = lower_map.get(unicodedata.normalize('NFC', name.lower()), name)

    if isinstance(name, bytes):
        name = name.decode("utf-8")

    for d in renpy.config.searchpath:
        fn = os.path.join(renpy.config.basedir, d, name)

        add_auto(fn)

        if os.path.isfile(fn):
            return fn

    raise Exception("Couldn't find file '%s'." % name)


hash_cache = {}


def get_hash(name): # type: (str) -> int
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

# Module Loading


class RenpyImporter(object):
    """
    An importer, that tries to load modules from the places where Ren'Py
    searches for data files.
    """

    def __init__(self, prefix=""):
        self.prefix = prefix

    def translate(self, fullname, prefix=None): # type: (str, Optional[str]) -> str|None

        if prefix is None:
            prefix = self.prefix

        try:
            if not isinstance(fullname, str):
                fullname = fullname.decode("utf-8")

            fn = prefix + fullname.replace(".", "/")

        except Exception:
            # raise Exception("Could importer-translate %r + %r" % (prefix, fullname))
            return None

        if loadable(fn + ".py"):
            return fn + ".py"

        if loadable(fn + "/__init__.py"):
            return fn + "/__init__.py"

        return None

    def find_module(self, fullname, path=None):
        if path is not None:
            for i in path:
                if self.translate(fullname, i):
                    return RenpyImporter(i)

        if self.translate(fullname):
            return self

    def load_module(self, fullname, mode="full"):
        """
        Loads a module. Possible modes include "is_package", "get_source", "get_code", or "full".
        """

        filename = self.translate(fullname, self.prefix)

        if mode == "is_package":
            return filename.endswith("__init__.py")

        pyname = pystr(fullname)

        mod = sys.modules.setdefault(pyname, types.ModuleType(pyname))
        mod.__name__ = pyname
        mod.__file__ = renpy.config.gamedir + "/" + filename
        mod.__loader__ = self

        if filename.endswith("__init__.py"):
            mod.__package__ = pystr(fullname)
        else:
            mod.__package__ = pystr(fullname.rpartition(".")[0])

        if mod.__file__.endswith("__init__.py"):
            mod.__path__ = [ mod.__file__[:-len("__init__.py")] ]

        for encoding in [ "utf-8", "latin-1" ]:

            try:

                source = load(filename).read().decode(encoding)
                if source and source[0] == u'\ufeff':
                    source = source[1:]

                if mode == "get_source":
                    return source

                code = compile(source, filename, 'exec', renpy.python.old_compile_flags, 1)

                break

            except Exception:
                if encoding == "latin-1":
                    raise

        if mode == "get_code":
            return code # type: ignore

        exec(code, mod.__dict__) # type: ignore

        return sys.modules[fullname]

    def is_package(self, fullname):
        return self.load_module(fullname, "is_package")

    def get_source(self, fullname):
        return self.load_module(fullname, "get_source")

    def get_code(self, fullname):
        return self.load_module(fullname, "get_code")

    def get_data(self, filename):

        filename = os.path.normpath(filename).replace('\\', '/')

        _check_prefix = "{0}/".format(
            os.path.normpath(renpy.config.gamedir).replace('\\', '/')
        )
        if filename.startswith(_check_prefix):
            filename = filename[len(_check_prefix):]

        return load(filename).read()


meta_backup = [ ]


def add_python_directory(path):
    """
    :doc: other

    Adds `path` to the list of paths searched for Python modules and packages.
    The path should be a string relative to the game directory. This must be
    called before an import statement.
    """

    if path and not path.endswith("/"):
        path = path + "/"

    sys.meta_path.insert(0, RenpyImporter(path)) # type: ignore
    # per: https://docs.python.org/3/library/sys.html#sys.meta_path,
    # objects in sys.meta_path may have just find_module, and find_spec
    # is synthesized.


def init_importer():
    meta_backup[:] = sys.meta_path

    add_python_directory("python-packages/")
    add_python_directory("")


def quit_importer():
    sys.meta_path[:] = meta_backup

# Auto-Reload


# A list of files for which autoreload is needed.
needs_autoreload = set()

# A map from filename to mtime, or None if the file doesn't exist.
auto_mtimes = { }

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
    starts/stops existing, we trigger a reload.
    """

    fn = fn.replace("\\", "/")

    if not renpy.autoreload:
        return

    if (fn in auto_mtimes) and (not force):
        return

    for e in renpy.config.autoreload_blacklist:
        if fn.endswith(e):
            with auto_lock:
                auto_mtimes[fn] = auto_blacklisted
            return

    mtime = auto_mtime(fn)

    with auto_lock:
        auto_mtimes[fn] = mtime


def auto_thread_function():
    """
    This thread sets need_autoreload when necessary.
    """

    while True:

        with auto_lock:

            auto_lock.wait(1.5)

            if auto_quit_flag:
                return

            items = list(auto_mtimes.items())

        for fn, mtime in items:

            if mtime is auto_blacklisted:
                continue

            if auto_mtime(fn) != mtime:

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


def check_autoreload():
    """
    Checks to see if autoreload is required.
    """

    # Defer loading while the git index lock is present.
    if needs_autoreload and check_git_index_lock():
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
