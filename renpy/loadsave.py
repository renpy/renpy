# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
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

import StringIO
import cStringIO

import zipfile
import os
import re
import threading
import sys
import platform
import types

import renpy.display

# This is used to cache information about saved games.
cache = { }


# Dump that choses which pickle to use:
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
                
            for k, v in get(4, []):
                size += 2
                size += visit(v, "{0}[{1!r}]".format(path, k))

            
        f.write("{0: 7d} {1} = {2}\n".format(size, path, o_repr_cache[ido]))
        
        return size

    f = file("save_dump.txt", "w")

    visit(roots, "roots")
    visit(log, "log")

    f.close()

# A file that can only be written to while the cpu is idle.
class IdleFile(file):

    def write(self, s):
        renpy.display.core.cpu_idle.wait()
        return file.write(self, s)

# A similar StringIO.
class IdleStringIO(StringIO.StringIO):

    def write(self, s):
        renpy.display.core.cpu_idle.wait()
        return StringIO.StringIO.write(self, s)

# Used to indicate an aborted save, due to the game being mutated
# while the save is in progress.
class SaveAbort(Exception):
    pass

def save(filename, extra_info='',
         file=file, StringIO=cStringIO.StringIO, #@ReservedAssignment
         mutate_flag=False, wait=None):
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

    cache.pop(filename, None)
    
    filename = filename + savegame_suffix

    try:
        os.unlink(renpy.config.savedir + "/" + filename)
    except:
        pass

    if mutate_flag:
        renpy.python.mutate_flag = False
    
    roots = renpy.game.log.freeze(wait)

    logf = StringIO()
    dump((roots, renpy.game.log), logf)

    if mutate_flag and renpy.python.mutate_flag:
        raise SaveAbort()

    if renpy.config.save_dump:
        save_dump(roots, renpy.game.log)

    rf = file(renpy.config.savedir + "/" + filename, "wb")
    zf = zipfile.ZipFile(rf, "w", zipfile.ZIP_DEFLATED)

    # Screenshot.
    zf.writestr("screenshot.png", renpy.game.interface.get_screenshot())

    # Extra info.
    zf.writestr("extra_info", extra_info.encode("utf-8"))

    # Version.
    zf.writestr("renpy_version", renpy.version)

    # The actual game.
    zf.writestr("log", logf.getvalue())

    zf.close()
    rf.close()
    

def scan_saved_game(name):

    if name in cache:
        return cache[name]
            
    try:
        f = name + savegame_suffix
    
        zf = zipfile.ZipFile(renpy.config.savedir + "/" + f, "r")

        try:
            png = False
            zf.getinfo('screenshot.tga')
        except:
            png = True
            zf.getinfo('screenshot.png')
            
            
        extra_info = zf.read("extra_info").decode("utf-8")
        zf.close()
       
        mtime = os.path.getmtime(renpy.config.savedir + "/" + f)

        if png:
            screenshot = renpy.display.im.ZipFileImage(renpy.config.savedir + '/' + f, "screenshot.png", mtime)
        else:
            screenshot = renpy.display.im.ZipFileImage(renpy.config.savedir + '/' + f, "screenshot.tga", mtime)
                    
        rv = extra_info, screenshot, mtime

    except:
        rv = None

    cache[name] = rv
    return rv
    
    

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

    try:
        files = os.listdir(renpy.config.savedir)
    except:
        return [ ]

    files.sort()
    files = [ i[:-len(savegame_suffix)]
              for i in files
              if i.endswith(savegame_suffix) and re.match(regexp, i) ]

    if fast:
        return files

    rv = [ ]

    for f in files:

        info = scan_saved_game(f)

        if info is not None:
            extra_info, screenshot, mtime = info        
            rv.append((f, extra_info, screenshot, mtime))

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
        

# Flag that lets us know if an autosave is in progress.
autosave_not_running = threading.Event()
autosave_not_running.set()

# The number of times autosave has been called without a save occuring.
autosave_counter = 0
        
def autosave_thread(take_screenshot):

    global autosave_counter

    try:
        
        try:
    
            renpy.display.core.cpu_idle.wait()
            cycle_saves("auto-", renpy.config.autosave_slots)
        
            renpy.display.core.cpu_idle.wait()
            if renpy.config.auto_save_extra_info:
                extra_info = renpy.config.auto_save_extra_info()
            else:
                extra_info = ""
    
            if take_screenshot:
                renpy.exports.take_screenshot(background=True)
            save("auto-1", file=IdleFile, StringIO=IdleStringIO, mutate_flag=True, wait=renpy.display.core.cpu_idle.wait, extra_info=extra_info)
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
    
    force_autosave(True)


# This assumes a screenshot has already been taken.
def force_autosave(take_screenshot=False):

    # That is, autosave is running.
    if not autosave_not_running.isSet():
        return
    
    autosave_not_running.clear()
    threading.Thread(target=autosave_thread, args=(take_screenshot,)).start()
    
    
class _MultiPersistent(object):

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_filename']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, name):

        if name.startswith("__") and name.endswith("__"):
            raise AttributeError()
        
        return None

    def save(self):
        
        fn = self._filename
        f = file(fn + ".new", "wb")
        dump(self, f)
        f.close()

        try:
            os.rename(fn + ".new", fn)
        except:
            os.unlink(fn)
            os.rename(fn + ".new", fn)


def MultiPersistent(name):

    if not renpy.game.context().init_phase:
        raise Exception("MultiPersistent objects must be created during the init phase.")
    
    if sys.platform == 'win32':
        files = [ os.path.expanduser("~/RenPy/Persistent") ]

        if 'APPDATA' in os.environ:
            files.append(os.environ['APPDATA'] + "/RenPy/persistent")
            
    elif platform.mac_ver()[0]:
        files = [ os.path.expanduser("~/.renpy/persistent"),
                  os.path.expanduser("~/Library/RenPy/persistent") ]
    else:
        files = [ os.path.expanduser("~/.renpy/persistent") ]

    # Make the new persistent directory, why not?
    try:
        os.makedirs(files[-1])
    except:
        pass

    fn = "" # prevent a warning from happening.

    # Find the first file that actually exists. Otherwise, use the last
    # file.
    for fn in files:
        fn = fn + "/" + name
        if os.path.exists(fn):
            break

    try:
        rv = loads(file(fn).read())
    except:
        rv = _MultiPersistent()

    rv._filename = fn # W0201
    return rv
