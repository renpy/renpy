# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import *

import renpy
import os.path
import sys
import types
import threading
import zlib
import re
import io
import unicodedata

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
    except:
        pass

    return fn

# Asset Loading


if renpy.android:
    import android.apk

    expansion = os.environ.get("ANDROID_EXPANSION", None)
    if expansion is not None:
        print("Using expansion file", expansion)

        apks = [
            android.apk.APK(apk=expansion, prefix='assets/x-game/'),
            android.apk.APK(apk=expansion, prefix='assets/x-renpy/x-common/'),
            ]

        game_apks = [ apks[0] ]

    else:
        print("Not using expansion file.")

        apks = [
            android.apk.APK(prefix='assets/x-game/'),
            android.apk.APK(prefix='assets/x-renpy/x-common/'),
            ]

        game_apks = [ apks[0] ]

else:
    apks = [ ]
    game_apks = [ ]

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

        # Deobfuscate the index.

        for k in index.keys():

            if len(index[k][0]) == 2:
                index[k] = [ (offset ^ key, dlen ^ key) for offset, dlen in index[k] ]
            else:
                index[k] = [ (offset ^ key, dlen ^ key, start) for offset, dlen, start in index[k] ]
        return index

archive_handlers.append(RPAv3ArchiveHandler)

class RPAv2ArchiveHandler(object):
    """
    Archive handler handling RPAv2 archives.
    """

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
            except:
                continue
            with f:
                file_header = f.read(max_header_length)
                for handler in archive_handlers:
                    try:
                        archive_handled = False
                        for header in handler.get_supported_headers():
                            if file_header.startswith(header):
                                f.seek(0, 0)
                                index = handler.read_index(f)
                                archives.append((prefix + ext, index))
                                archive_handled = True
                                break
                        if archive_handled == True:
                            break
                    except:
                        raise

    for dir, fn in listdirfiles(): # @ReservedAssignment
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
        except:
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
        with open(index_filename, 'rb') as remote_index:
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


class SubFile(object):

    def __init__(self, fn, base, length, start):
        self.fn = fn

        self.f = None

        self.base = base
        self.offset = 0
        self.length = length
        self.start = start

        if not self.start:
            self.name = fn
        else:
            self.name = None

    def open(self):
        self.f = open(self.fn, "rb")
        self.f.seek(self.base)

    def __enter__(self):
        return self

    def __exit__(self, _type, value, tb):
        self.close()
        return False

    def read(self, length=None):

        if self.f is None:
            self.open()

        maxlength = self.length - self.offset

        if length is not None:
            length = min(length, maxlength)
        else:
            length = maxlength

        rv1 = self.start[self.offset:self.offset + length]
        length -= len(rv1)
        self.offset += len(rv1)

        if length:
            rv2 = self.f.read(length)
            self.offset += len(rv2)
        else:
            rv2 = ""

        return (rv1 + rv2)

    def readline(self, length=None):

        if self.f is None:
            self.open()

        maxlength = self.length - self.offset
        if length is not None:
            length = min(length, maxlength)
        else:
            length = maxlength

        # If we're in the start, then read the line ourselves.
        if self.offset < len(self.start):
            rv = ''

            while length:
                c = self.read(1)
                rv += c
                if c == '\n':
                    break
                length -= 1

            return rv

        # Otherwise, let the system read the line all at once.
        rv = self.f.readline(length)

        self.offset += len(rv)

        return rv

    def readlines(self, length=None):
        rv = [ ]

        while True:
            l = self.readline(length)

            if not l:
                break

            if length is not None:
                length -= len(l)
                if l < 0:
                    break

            rv.append(l)

        return rv

    def xreadlines(self):
        return self

    def __iter__(self):
        return self

    def __next__(self): # @ReservedAssignment
        rv = self.readline()

        if not rv:
            raise StopIteration()

        return rv

    next = __next__

    def flush(self):
        return

    def seek(self, offset, whence=0):

        if self.f is None:
            self.open()

        if whence == 0:
            offset = offset
        elif whence == 1:
            offset = self.offset + offset
        elif whence == 2:
            offset = self.length + offset

        if offset > self.length:
            offset = self.length

        self.offset = offset

        offset = offset - len(self.start)
        if offset < 0:
            offset = 0

        self.f.seek(offset + self.base)

    def tell(self):
        return self.offset

    def close(self):
        if self.f is not None:
            self.f.close()
            self.f = None

    def write(self, s):
        raise Exception("Write not supported by SubFile")


open_file = open

if "RENPY_FORCE_SUBFILE" in os.environ:

    def open_file(name, mode):
        f = open(name, mode)

        f.seek(0, 2)
        length = f.tell()
        f.seek(0, 0)

        return SubFile(f, 0, length, '')

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
        except:
            pass

    return None

file_open_callbacks.append(load_from_filesystem)

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

            rv = SubFile(afn, offset, dlen, start)

        # Compatibility path.
        else:
            with open(afn, "rb") as f:
                for offset, dlen in index[name]:
                    f.seek(offset)
                    data.append(f.read(dlen))

                rv = io.BytesIO(b''.join(data))

        return rv

    return None

file_open_callbacks.append(load_from_archive)

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


def get_prefixes(tl=True):
    """
    Returns a list of prefixes to search for files.
    """

    rv = [ ]

    if tl:
        language = renpy.game.preferences.language # @UndefinedVariable
    else:
        language = None

    for prefix in renpy.config.search_prefixes:

        if language is not None:
            rv.append(renpy.config.tl_directory + "/" + language + "/" + prefix)

        rv.append(prefix)

    return rv


def load(name, tl=True):

    if renpy.display.predict.predicting: # @UndefinedVariable
        if threading.current_thread().name == "MainThread":
            if not (renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False)):
                raise Exception("Refusing to open {} while predicting.".format(name))

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    name = re.sub(r'/+', '/', name).lstrip('/')

    for p in get_prefixes(tl):
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
    except:
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


def loadable(name):

    name = name.lstrip('/')

    if (renpy.config.loadable_callback is not None) and renpy.config.loadable_callback(name):
        return True

    for p in get_prefixes():
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


hash_cache = dict()


def get_hash(name):
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

    except:
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

    def translate(self, fullname, prefix=None):

        if prefix is None:
            prefix = self.prefix

        try:
            if not isinstance(fullname, str):
                fullname = fullname.decode("utf-8")

            fn = prefix + fullname.replace(".", "/")

        except:
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

    def load_module(self, fullname):

        filename = self.translate(fullname, self.prefix)

        pyname = pystr(fullname)

        mod = sys.modules.setdefault(pyname, types.ModuleType(pyname))
        mod.__name__ = pyname
        mod.__file__ = filename
        mod.__loader__ = self

        if filename.endswith("__init__.py"):
            mod.__path__ = [ filename[:-len("__init__.py")] ]

        for encoding in [ "utf-8", "latin-1" ]:

            try:

                source = load(filename).read().decode(encoding)
                if source and source[0] == u'\ufeff':
                    source = source[1:]
                source = source.encode("raw_unicode_escape")
                source = source.replace(b"\r", b"")

                code = compile(source, filename, 'exec', renpy.python.old_compile_flags, 1)
                break
            except:
                if encoding == "latin-1":
                    raise

        exec(code, mod.__dict__)

        return sys.modules[fullname]

    def get_data(self, filename):
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

    sys.meta_path.insert(0, RenpyImporter(path))


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
    except:
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

    global needs_autoreload

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


def check_autoreload():
    """
    Checks to see if autoreload is required.
    """

    while needs_autoreload:
        fn = next(iter(needs_autoreload))
        mtime = auto_mtime(fn)

        with auto_lock:
            needs_autoreload.discard(fn)
            auto_mtimes[fn] = mtime

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
