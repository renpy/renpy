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

# This file contains functions that load and save the game state.

import pickle
import cPickle

import StringIO
import cStringIO

import zipfile
import time
import os
import os.path
import re
import threading

import renpy

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

# def debug_dump(prefix, o, seen):

#     if isinstance(o, (int, str, float, bool)):
#         print prefix, o
#         return

#     if id(o) in seen:
#         print prefix, "@%x" % id(o), type(o)
#         return

#     seen[id(o)] = True

#     if isinstance(o, tuple):
#         print prefix, "("
#         for i in o:
#             debug_dump(prefix + "  ", i, seen)
#         print prefix, ")"

#     elif isinstance(o, list):
#         print prefix, "["
#         for i in o:
#             debug_dump(prefix + "  ", i, seen)
#         print prefix, "]"

#     elif isinstance(o, dict):
#         print prefix, "{"
#         for k, v in o.iteritems():
#             print prefix, repr(k), "="
#             debug_dump(prefix + "    ", v, seen)
#         print prefix, "}"

#     elif isinstance(o, renpy.style.Style):
#         print "<style>"
    
#     elif hasattr(o, "__dict__"):

#         ignored = getattr(o, "nosave", [ ])

#         print prefix, repr(o), "{{"
#         for k, v in vars(o).iteritems():
#             if k in ignored:
#                 continue

#             print prefix, repr(k), "="
#             debug_dump(prefix + "    ", v, seen)
#         print prefix, "}}"

#     else:
#         print prefix, repr(o)


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
         file=file, StringIO=cStringIO.StringIO,
         mutate_flag=False, wait=None):
    """
    Saves the game in the given filename. This will save the game
    along with a screnshot and the given extra_info, which is just
    serialized.

    It's expected that a screenshot will be taken (with
    renpy.take_screenshot) before this is called.
    """

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

    rf = file(renpy.config.savedir + "/" + filename, "wb")
    zf = zipfile.ZipFile(rf, "w", zipfile.ZIP_DEFLATED)

    # Screenshot.
    zf.writestr("screenshot.tga", renpy.game.interface.get_screenshot())

    # Extra info.
    zf.writestr("extra_info", extra_info.encode("utf-8"))


    # The actual game.
    zf.writestr("log", logf.getvalue())

    zf.close()
    rf.close()
    

def scan_saved_game(name):

    try:
        f = name + savegame_suffix
    
        zf = zipfile.ZipFile(renpy.config.savedir + "/" + f, "r")

        # Fail early if screenshot.tga doesn't exist.
        zf.getinfo('screenshot.tga')
        
        extra_info = zf.read("extra_info").decode("utf-8")
        zf.close()
       
        mtime = os.path.getmtime(renpy.config.savedir + "/" + f)
        screenshot = renpy.display.im.ZipFileImage(renpy.config.savedir + '/' + f, "screenshot.tga", mtime)
        
        return extra_info, screenshot, mtime
    except:
        return None
    
    

def list_saved_games(regexp=r'.'):
    """
    This scans the savegames that we know about and returns
    information about them. It returns a list of tuples, where each
    tuple represents one savegame and consists of:
    
    - The filename of the save.
    - The extra_info that was passed to renpy.save.
    - A displayable, the screenshot used to show the game.
    - The time the game was saved at, seconds since 1/1/1970 UTC.
    
    The regexp matches at the start of the filename, and filters the list.
    """

    try:
        files = os.listdir(renpy.config.savedir)
    except:
        return [ ]

    files.sort()
    files = [ i[:-len(savegame_suffix)]
              for i in files
              if i.endswith(savegame_suffix) and re.match(regexp, i) ]

    rv = [ ]

    for f in files:

        info = scan_saved_game(f)

        if info is not None:
            extra_info, screenshot, mtime = info        
            rv.append((f, extra_info, screenshot, mtime))

    return rv

def can_load(filename):
    """
    Returns true if we can load the given savegame file, False otherwise.
    """

    try:
        zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename + savegame_suffix, "r")
        zf.close()
        return True
    except:
        return False
    

def load(filename):
    """
    Loads the game from the given file. This function never returns.
    """
    
    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename + savegame_suffix, "r")
    roots, log = loads(zf.read("log"))
    zf.close()

    log.unfreeze(roots, label="_after_load")

def rename_save(old, new):
    unlink_save(new)
    os.rename(renpy.config.savedir + "/" + old + savegame_suffix, 
              renpy.config.savedir + "/" + new + savegame_suffix)
    

def unlink_save(filename):
    if os.path.exists(renpy.config.savedir + "/" + filename + savegame_suffix):
        os.unlink(renpy.config.savedir + "/" + filename + savegame_suffix)


def cycle_saves(name, count):

    for count in range(1, count + 1):
        if not os.path.exists(renpy.config.savedir + "/" + name + str(count) + savegame_suffix):
            break
        
    for i in range(count - 1, 0, -1):
        rename_save(name + str(i), name + str(i + 1))
        

# Flag that lets us know if an autosave is in progress.
autosave_in_progress = False

# The number of times autosave has been called without a save occuring.
autosave_counter = 0
        
def autosave_thread():

    global autosave_in_progress
    global autosave_counter
    
    renpy.display.core.cpu_idle.wait()
    cycle_saves("auto-", renpy.config.autosave_slots)
    
    renpy.display.core.cpu_idle.wait()
    if renpy.config.auto_save_extra_info:
        extra_info = renpy.config.auto_save_extra_info()
    else:
        extra_info = ""
        
    try:
        try:
            
            renpy.exports.take_screenshot()
            save("auto-1", file=IdleFile, StringIO=IdleStringIO, mutate_flag=True, wait=renpy.display.core.cpu_idle.wait, extra_info=extra_info)
            autosave_counter = 0
            
        except SaveAbort:
            pass

    finally:
        autosave_in_progress = False
    

def autosave():
    global autosave_counter
    global autosave_in_progress
    
    if not renpy.config.autosave_frequency:
        return 
    
    if autosave_in_progress:
        return

    if renpy.config.skipping:
        return
    
    if len(renpy.game.contexts) > 1:
        return

    autosave_counter += 1

    if autosave_counter < renpy.config.autosave_frequency:
        return
    
    autosave_in_progress = True
    threading.Thread(target=autosave_thread).start()
    
    
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
            os.rename(fm + ".new", fn)
            
def MultiPersistent(name):

    if not renpy.game.init_phase:
        raise Exception("MultiPersistent objects must be created during the init phase.")
    
    if os.name == 'nt':
        fn = os.path.expanduser("~/RenPy/Persistent")
    else:
        fn = os.path.expanduser("~/.renpy/persistent")

    try:
        os.makedirs(fn)
    except:
        pass

    fn = fn + "/" + name

    try:
        rv = loads(file(fn).read())
    except:
        rv = _MultiPersistent()

    rv._filename = fn
    return rv
