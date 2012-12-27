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

import renpy.display
import renpy.game as game
import os
import sys
import time
import zipfile
import subprocess
from cPickle import loads, dumps
import __main__


def save_persistent():
    
    try:
        f = file(renpy.config.savedir + "/persistent", "wb")
        f.write(dumps(game.persistent).encode("zlib"))
        f.close()
    except:
        if renpy.config.debug:
            raise
        

def run(restart):
    """
    This is called during a single run of the script. Restarting the script
    will cause this to change.
    """

    # Reset the store to a clean version of itself.
    renpy.python.clean_stores()

    # Re-Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Switch contexts, begin logging.
    game.contexts = [ renpy.execution.Context(True) ]

    # Jump to an appropriate start label.
    if game.script.has_label("_start"):
        start_label = '_start'
    else:
        start_label = 'start'

    game.context().goto_label(start_label)

    # Perhaps warp.
    warp_label = renpy.warp.warp() 
    
    if warp_label is not None:

        game.context().goto_label(warp_label)

        if game.script.has_label('after_warp'):
            game.context().call('after_warp')

        renpy.config.skipping = None

    try:
        renpy.exports.log("--- " + time.ctime())
        renpy.exports.log("")
    except:
        pass

    # Note if this is a restart.
    renpy.store._restart = restart
    restart = None
    
    # We run until we get an exception.
    renpy.execution.run_context(True)
    

def load_rpe(fn):

    zfn = zipfile.ZipFile(fn)
    autorun = zfn.read("autorun.py")
    zfn.close()

    sys.path.insert(0, fn)
    exec autorun in dict()
        
def choose_variants():

    if "RENPY_VARIANT" in os.environ:
        renpy.config.variants = list(os.environ["RENPY_VARIANT"].split()) + [ None ]
    else:
        renpy.config.variants = [ None ]
    
    if renpy.android: #@UndefinedVariable
        import android #@UnresolvedImport
        import math
        import pygame
        
        pygame.display.init()
        
        info = pygame.display.Info()        
        diag = math.hypot(info.current_w, info.current_h) / android.get_dpi()
        
        print "Screen diagonal is", diag, "inches."
        
        renpy.config.variants.insert(0, 'touch')
        
        if diag >= 6:
            renpy.config.variants.insert(0, 'tablet')
        else:
            renpy.config.variants.insert(0, 'phone')
        
    else:
        renpy.config.variants.insert(0, 'pc')
    
        
def main():

    renpy.game.exception_info = 'Before loading the script.'

    # Get ready to accept new arguments.
    renpy.arguments.pre_init()

    # Init the config after load.
    renpy.config.init()

    # Set up variants.
    choose_variants()
    
    # Note the game directory.
    game.basepath = renpy.config.gamedir
    renpy.config.searchpath = [ renpy.config.gamedir ]

    # Find the common directory.
    commondir = __main__.path_to_common(renpy.config.renpy_base) # E1101 @UndefinedVariable

    if os.path.isdir(commondir):
        renpy.config.searchpath.append(commondir)
        renpy.config.commondir = commondir
    else:
        renpy.config.commondir = None
        
    # Load Ren'Py extensions.
    for dir in renpy.config.searchpath: #@ReservedAssignment
        for fn in os.listdir(dir):
            if fn.lower().endswith(".rpe"):
                load_rpe(dir + "/" + fn)

        
    # The basename is the final component of the path to the gamedir.
    for i in sorted(os.listdir(renpy.config.gamedir)):

        if not i.endswith(".rpa"):
            continue

        i = i[:-4]
        renpy.config.archives.append(i)
        
    renpy.config.archives.reverse()

    # Initialize archives.
    renpy.loader.index_archives()

    # Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Initialize the store.
    renpy.store.store = sys.modules['store']

    # Set up styles.
    renpy.style.reset()
    game.style = renpy.style.StyleManager()
    renpy.store.style = game.style

    # Run init code in its own context. (Don't log.)
    game.contexts = [ renpy.execution.Context(False) ]
    game.contexts[0].init_phase = True

    # Load the script.
    renpy.game.exception_info = 'While loading the script.'
    renpy.game.script = renpy.script.Script()

    # Set up error handling.
    renpy.exports.load_module("_errorhandling")
    renpy.style.build_styles(early=True)
    
    # Load all .rpy files.    
    renpy.game.script.load_script() # sets renpy.game.script.

    renpy.game.exception_info = 'After loading the script.'

    # Find the save directory.
    if renpy.config.savedir is None:
        renpy.config.savedir = __main__.path_to_saves(renpy.config.gamedir) # E1101 @UndefinedVariable

    if renpy.game.args.savedir: #@UndefinedVariable
        renpy.config.savedir = renpy.game.args.savedir #@UndefinedVariable
    
    # Make the save directory.
    try:
        os.makedirs(renpy.config.savedir)
    except:
        pass

    # Unserialize the persistent data.
    try:
        f = file(renpy.config.savedir + "/persistent", "rb")
        s = f.read().decode("zlib")
        f.close()
        game.persistent = loads(s)
    except:
        game.persistent = game.Persistent()

    # Initialize the set of statements seen ever.
    if not game.persistent._seen_ever:
        game.persistent._seen_ever = { }

    game.seen_ever = game.persistent._seen_ever

    # Initialize the set of images seen ever.
    if not game.persistent._seen_images:
        game.persistent._seen_images = { }

    # Initialize the set of chosen menu choices.
    if not game.persistent._chosen:
        game.persistent._chosen = { }

    if not game.persistent._seen_audio:
        game.persistent._seen_audio = { }
        
    # Clear the list of seen statements in this game.
    game.seen_session = { }

    # Initialize the preferences.
    if not game.persistent._preferences:
        game.persistent._preferences = game.Preferences()

    game.preferences = game.persistent._preferences

    # Initialize persistent variables.
    renpy.store.persistent = game.persistent
    renpy.store._preferences = game.preferences

    if renpy.parser.report_parse_errors():
        raise renpy.game.ParseErrorException()

    renpy.game.exception_info = 'While executing init code:'

    for _prio, node in game.script.initcode:
        game.context().run(node)

    renpy.game.exception_info = 'After initialization, but before game start.'

    # Save the bytecode in a cache.
    renpy.game.script.save_bytecode()

    # Check if we should simulate android.
    renpy.android = renpy.android or renpy.config.simulate_android #@UndefinedVariable
    
    # Run the post init code, if any.
    for i in renpy.game.post_init:
        i()
        
    # Init translation.
    renpy.translation.init_translation()
        
    # Rebuild the various style caches.
    renpy.style.build_styles()

    # Index the archive files. We should not have loaded an image
    # before this point. (As pygame will not have been initialized.)
    # We need to do this again because the list of known archives
    # may have changed.
    renpy.loader.index_archives()

    # Check some environment variables.
    renpy.game.less_memory = "RENPY_LESS_MEMORY" in os.environ
    renpy.game.less_mouse = "RENPY_LESS_MOUSE" in os.environ
    renpy.game.less_updates = "RENPY_LESS_UPDATES" in os.environ

    renpy.dump.dump(False)

    # Handle arguments and commands. 
    if not renpy.arguments.post_init():
        return

    # Remove the list of all statements from the script.
    game.script.all_stmts = None

    # Make a clean copy of the store.
    renpy.python.make_clean_stores()

    # Initialize image cache.
    renpy.display.im.cache.init()
    
    # (Perhaps) Initialize graphics.
    if not game.interface:
        renpy.display.core.Interface()

    # Start things running.
    restart = None

    renpy.game.exception_info = 'While running game code:'
    renpy.first_utter_start = False

    while True:
        try:
            try:
                run(restart)
            finally:
                restart = (renpy.config.end_game_transition, "_invoke_main_menu", "_main_menu")
                save_persistent()
                
        except game.QuitException, e:
            
            if e.relaunch:
                if renpy.windows and sys.argv[0].endswith(".exe"):
                    subprocess.Popen(sys.argv)
                else:
                    subprocess.Popen([sys.executable, "-OO"] + sys.argv)
            
            break

        except game.FullRestartException, e:
            restart = e.reason

        finally:
            renpy.display.core.cpu_idle.set()
            renpy.loadsave.autosave_not_running.wait()
            
    # This is stuff we do on a normal, non-error return.
    if not renpy.display.error.error_handled:
        renpy.display.render.check_at_shutdown()

