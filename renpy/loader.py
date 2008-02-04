# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

import renpy
import os
import os.path
from pickle import loads
from cStringIO import StringIO
import sys
import types
import codecs

# Files on disk should be checked before archives. Otherwise, among
# other things, using a new version of bytecode.rpb will break.

archives = [ ]

# The value of renpy.config.archives the last time index_archives was
# run.
old_config_archives = None

def index_archives():
    """
    Loads in the indexes for the archive files.
    """

    global old_config_archives

    if old_config_archives == renpy.config.archives:
        return

    old_config_archives = renpy.config.archives[:]
    
    global archives
    archives = [ ]

    for prefix in renpy.config.archives:

        fn = transfn(prefix + ".rpa")

        try:
            fn = transfn(prefix + ".rpa")
            f = file(fn, "rb")
            l = f.readline()

            # 3.0 Branch.
            if l.startswith("RPA-3.0 "):
                offset = int(l[8:24], 16)
                key = int(l[25:33], 16)
                f.seek(offset)
                index = loads(f.read().decode("zlib"))

                # Deobfuscate the index.

                for k in index.keys():
                    index[k] = [ (offset ^ key, dlen ^ key) for offset, dlen in index[k] ]

                archives.append((prefix, index))
                
                f.close()
                continue

            # 2.0 Branch.
            if l.startswith("RPA-2.0 "):
                offset = int(l[8:], 16)
                f.seek(offset)
                index = loads(f.read().decode("zlib"))
                archives.append((prefix, index))
                f.close()
                continue

            # 1.0 Branch.
        
            f.close()
            
            fn = transfn(prefix + ".rpi")
            index = loads(file(fn, "rb").read().decode("zlib")) 
            archives.append((prefix, index))
        except:
            if renpy.config.debug:
                raise

def walkdir(dir):
    rv = [ ]

    for i in os.listdir(dir):
        if i[0] == ".":
            continue

        if os.path.isdir(dir + "/" + i):
            for fn in walkdir(dir + "/" + i):
                rv.append(i + "/" + fn)
        else:
            rv.append(i)

    return rv
        
    
def listdirfiles():
    """
    Returns a list of directory, file tuples known to the system. If
    the file is in an archive, the directory is None.
    """

    rv = [ ]

    for i in renpy.config.searchpath:
        i = os.path.join(renpy.config.basedir, i)
        for j in walkdir(i):
            rv.append((i, j))

    for prefix, index in archives:
        for j in index.iterkeys():
            rv.append((None, j))

    return rv
    

class SubFile(object):

    def __init__(self, f, base, length):
        self.f = f
        self.base = base
        self.offset = 0
        self.length = length

        self.f.seek(self.offset + self.base)

    def read(self, length=None):

        maxlength  = self.length - self.offset
        if length is not None:
            length = min(length, maxlength)
        else:
            length = maxlength

        rv = self.f.read(length)
        
        self.offset += len(rv)

        return rv

    def readline(self, length=None):

        maxlength  = self.length - self.offset
        if length is not None:
            length = min(length, maxlength)
        else:
            length = maxlength

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

    def next(self):
        rv = self.readline()

        if not rv:
            raise StopIteration()

        return rv
    
    def flush(self):
        return

    
    def seek(self, offset, whence=0):

        if whence == 0:
            self.offset = offset
        elif whence == 1:
            self.offset = self.offset + offset
        elif whence == 2:
            self.offset = self.length + offset

        self.f.seek(self.offset + self.base)

    def tell(self):
        return self.offset

    def close(self):
        self.f.close()

    def write(self, s):
        raise Exception("Write not supported by SubFile")
    

def load(name):
    """
    Returns an open python file object of the given type.
    """
    
    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    # Look for the file directly.
    if not renpy.config.force_archives:

        try:
            fn = transfn(name)
            return file(fn, "rb")
        except:
            pass

    # Look for it in archive files.
    for prefix, index in archives:
        if not name in index:
            continue

        f = file(transfn(prefix + ".rpa"), "rb")

        data = [ ]

        # Direct path.
        if len(index[name]) == 1:
            offset, dlen = index[name][0]
            rv = SubFile(f, offset, dlen)

        # Compatability path.
        else:
            for offset, dlen in index[name]:           
                f.seek(offset)
                data.append(f.read(dlen))

            rv = StringIO(''.join(data))
            f.close()
            
        return rv

    raise Exception("Couldn't find file '%s'." % name)

def loadable(name):
    """
    Returns True if the name is loadable with load, False if it is not.
    """

    try:
        transfn(name)
        return True
    except:
        pass

    for prefix, index in archives:
        if name in index:
            return True

    return False
    

def transfn(name):
    """
    Tries to translate the name to a file that exists in one of the
    searched directories.
    """

    if renpy.config.reject_backslash and "\\" in name:
        raise Exception("Backslash in filename, use '/' instead: %r" % name)

    for d in renpy.config.searchpath:
        fn = os.path.join(renpy.config.basedir, d, name)

        if os.path.exists(fn):
            return fn

    raise Exception("Couldn't find file '%s'." % name)



class RenpyImporter(object):
    """
    An importer, that tries to load modules from the places where Ren'Py
    searches for data files.
    """

    def translate(self, fullname):
        
        fn = fullname.replace(".", "/") + ".py"
        if loadable(fn):
            return fn

        fn = fullname.replace(".", "/") + "/__init__.py"

        if loadable(fn):
            return fn

        return None

    def find_module(self, fullname, path=None):
        if self.translate(fullname):
            return self

    def load_module(self, fullname):

        filename = self.translate(fullname)
        
        mod = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        mod.__file__ = filename
        mod.__loader__ = self
        mod.__path__ = [ ]

        source = load(filename).read().decode("utf8")
        if source[0] == u'\ufeff':
            source = source[1:]
        source = source.encode("raw_unicode_escape")
        
        source = source.replace("\r", "")
        code = compile(source, filename, 'exec')
        exec code in mod.__dict__
        return mod

    def get_data(self, filename):
        return load(filename).read()

sys.meta_path.append(RenpyImporter())
