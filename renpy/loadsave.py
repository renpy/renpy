# This file contains functions that load and save the game state.

from pickle import dumps, loads, HIGHEST_PROTOCOL
import cStringIO
import zipfile
import time
import os

import renpy


# This is used as a quick and dirty way of versioning savegame
# files.
savegame_suffix = renpy.savegame_suffix

def debug_dump(prefix, o, seen):

    if isinstance(o, (int, str, float, bool)):
        print prefix, o
        return

    if id(o) in seen:
        print prefix, "@%x" % id(o)
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
        zf.writestr("extra_info", extra_info)

        # print
        # print "Debug Dump!"
        # debug_dump("", renpy.game.log, { })

        # The actual game.
        zf.writestr("log", dumps(renpy.game.log, HIGHEST_PROTOCOL))

        zf.close()
    finally:              
        renpy.game.log.discard_freeze()



def saved_games():
    """
    This scans the savegames that we know about and returns
    information about them. Specifically, it returns tuple containing
    a savelist and the filename of the newest save file (or None if no
    save file exists).

    The savelist, in turn, is a list of tuples, with each tuple containing
    the filename of the saved game, a Displayable containing a screenshot,
    and a string giving the extra data of that save.
    """

    files = os.listdir(renpy.config.savedir)
    files.sort()
    files = [ i for i in files if i.endswith(savegame_suffix) ]

    if not files:
        newest = None
    else:
        datefiles = [ (os.stat(renpy.config.savedir + "/" + i).st_mtime, i) for i in files ]
        datefiles.sort()
        newest = datefiles[-1][1]
        newest = newest[:-len(savegame_suffix)]

    saveinfo = { }

    for f in files:

        try:

            zf = zipfile.ZipFile(renpy.config.savedir + "/" + f, "r")
            extra_info = zf.read("extra_info")
            sio = cStringIO.StringIO(zf.read("screenshot.tga"))
            zf.close()

            screenshot = renpy.display.image.UncachedImage(sio, "screenshot.tga", False)

            f = f[:-len(savegame_suffix)]

            saveinfo[f] = screenshot, extra_info

        except:
            if renpy.config.debug:
                raise Exception

    if newest not in saveinfo:
        newest = None

    return saveinfo, newest
    
def load(filename):
    """
    Loads the game from the given file. This function never returns.
    """
    
    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename + savegame_suffix, "r")
    log = loads(zf.read("log"))
    zf.close()
    log.unfreeze()
