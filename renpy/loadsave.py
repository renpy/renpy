# This file contains functions that load and save the game state.

from pickle import dumps, loads, HIGHEST_PROTOCOL
import cStringIO
import zipfile
import time
import os
import os.path
import re

import renpy


# This is used as a quick and dirty way of versioning savegame
# files.
savegame_suffix = renpy.savegame_suffix

def debug_dump(prefix, o, seen):

    if isinstance(o, (int, str, float, bool)):
        print prefix, o
        return

    if id(o) in seen:
        print prefix, "@%x" % id(o), type(o)
        return

    seen[id(o)] = True

    if isinstance(o, tuple):
        print prefix, "("
        for i in o:
            debug_dump(prefix + "  ", i, seen)
        print prefix, ")"

    elif isinstance(o, list):
        print prefix, "["
        for i in o:
            debug_dump(prefix + "  ", i, seen)
        print prefix, "]"

    elif isinstance(o, dict):
        print prefix, "{"
        for k, v in o.iteritems():
            print prefix, repr(k), "="
            debug_dump(prefix + "    ", v, seen)
        print prefix, "}"

    elif isinstance(o, renpy.style.Style):
        print "<style>"
    
    elif hasattr(o, "__dict__"):

        ignored = getattr(o, "nosave", [ ])

        print prefix, repr(o), "{{"
        for k, v in vars(o).iteritems():
            if k in ignored:
                continue

            print prefix, repr(k), "="
            debug_dump(prefix + "    ", v, seen)
        print prefix, "}}"

    else:
        print prefix, repr(o)

    

def save(filename, extra_info=''):
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


    renpy.game.log.freeze()


    try:
        zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename,
                             "w", zipfile.ZIP_DEFLATED)

        # Screenshot.
        zf.writestr("screenshot.tga", renpy.game.interface.get_screenshot())

        # Extra info.
        zf.writestr("extra_info", extra_info.encode("utf-8"))

        # print
        # print "Debug Dump!"
        # if os.environ['RENPY_DEBUG_DUMP']:

        # renpy.config.debug = True
        # debug_dump("", renpy.game.log, { })

        # The actual game.
        zf.writestr("log", dumps(renpy.game.log, HIGHEST_PROTOCOL))

        zf.close()
    finally:              
        renpy.game.log.discard_freeze()



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

    files = os.listdir(renpy.config.savedir)
    files.sort()
    files = [ i for i in files if i.endswith(savegame_suffix) and re.match(regexp, i) ]

    rv = [ ]

    for f in files:

        try:

            zf = zipfile.ZipFile(renpy.config.savedir + "/" + f, "r")
            sio = cStringIO.StringIO(zf.read("screenshot.tga"))
            extra_info = zf.read("extra_info").decode("utf-8")
            zf.close()

            screenshot = renpy.display.image.UncachedImage(sio, "screenshot.tga", False)
            mtime = os.path.getmtime(renpy.config.savedir + "/" + f)
            f = f[:-len(savegame_suffix)]

            rv.append((f, extra_info, screenshot, mtime))

        except:
            if renpy.config.debug:
                raise Exception

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
    log = loads(zf.read("log"))
    zf.close()

    log.unfreeze(label="after_load")


class _MultiPersistent(object):

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_filename']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, name):
        return None

    def save(self):
        
        fn = self._filename
        f = file(fn + ".new", "wb")
        f.write(dumps(self))
        f.close()

        os.rename(fn + ".new", fn)

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
