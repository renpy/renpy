# This file contains functions that load and save the game state.

from cPickle import dumps, loads, HIGHEST_PROTOCOL
import cStringIO
import renpy
import zipfile
import time
import os

def save(filename, extra_info=''):
    """
    Saves the game in the given filename. This will save the game
    along with a screnshot and the given extra_info, which is just
    serialized.

    It's expected that a screenshot will be taken (with
    renpy.take_screenshot) before this is called.

    If the filename is None, one is automatically generated based
    on the current time.
    """

    if filename == None:
        filename = str(time.time()) + ".save"

    try:
        os.unlink(renpy.config.savedir + "/" + filename)
    except:
        pass

    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename,
                         "w", zipfile.ZIP_DEFLATED)
    
    # Screenshot.
    zf.writestr("screenshot.tga", renpy.game.interface.get_screenshot())

    # Extra info.
    zf.writestr("extra_info", extra_info)
    
    # The actual game.
    renpy.game.log.freeze()
    zf.writestr("log", dumps(renpy.game.log, HIGHEST_PROTOCOL))
    renpy.game.log.discard_freeze()

    zf.close()

def saved_game_filenames():
    """
    Returns a list of savegame files.
    """
    
    files = os.listdir(renpy.config.savedir)
    files.sort()
    return [ i for i in files if i.endswith(".save") ]

def newest_save_game():
    """
    Returns the name of the newest savegame file.
    """
    
    files = os.listdir(renpy.config.savedir)
    files = [ i for i in files if i.endswith(".save") ]

    if not files:
        return None

    datefiles = [ (os.stat(renpy.config.savedir + "/" + i).st_mtime, i) for i in files ]
    datefiles.sort()

    return datefiles[-1][1]
    
def load_extra_info(filename):
    """
    Returns the extra_info string that was saved in a savegame file.
    """

    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename, "r")
    rv = zf.read("extra_info")
    zf.close()

    return rv

def load_screenshot(filename, scale=None):
    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename, "r")
    sio = cStringIO.StringIO(zf.read("screenshot.tga"))
    zf.close()
    
    return renpy.display.image.UncachedImage(sio, "screenshot.tga", scale)
    
def load(filename):
    """
    Loads the game from the given file. This function never returns.
    """
    
    zf = zipfile.ZipFile(renpy.config.savedir + "/" + filename, "r")
    log = loads(zf.read("log"))
    zf.close()
    log.unfreeze()
