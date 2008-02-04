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
import renpy.game as game
import os
import sys
import time
import zipfile
from cPickle import loads, dumps, HIGHEST_PROTOCOL
import __main__

def save_persistent():

    try:
        f = file(renpy.config.savedir + "/persistent", "wb")
        f.write(dumps(game.persistent).encode("zlib"))
        f.close()
    except:
        if renpy.config.debug:
            raise
        

def run(restart=False):
    """
    This is called during a single run of the script. Restarting the script
    will cause this to change.
    """

    # Reset the store to a clean version of itself.
    store = renpy.store.__dict__
    store.clear()
    store.update(renpy.game.clean_store)

    # Note that this is a restart.
    renpy.store._restart = restart

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
    if renpy.game.options.warp:
        label = renpy.warp.warp(renpy.game.options.warp)

        if not label:
            raise Exception("Could not find line to warp to.")

        game.context().goto_label(label)

        if game.script.has_label('after_warp'):
            game.context().call('after_warp')

        renpy.game.options.warp = None

    # Run the game.
    while True:

        renpy.exports.log("--- " + time.ctime())
        renpy.exports.log("")

        # We run until we get an exception.
        try:
            game.context().run()
            game.context().pop_all_dynamic()
            break

        # We get this when the context has changed, and so we go and
        # start running from the new context.
        except game.RestartException, e:
            renpy.game.contexts = e.contexts

            label = e.label

            if label:
                if game.script.has_label(label):
                    game.context().call(label)

            continue
            
    # And, we're done.

def load_rpe(fn):

    zfn = zipfile.ZipFile(fn)
    autorun = zfn.read("autorun.py")
    zfn.close()

    sys.path.insert(0, fn)
    exec autorun in dict()
        
def main():

    renpy.game.exception_info = 'Before loading the script.'

    # Init the config after load.
    renpy.config.init()

    # Note the game directory.
    game.basepath = renpy.config.gamedir
    renpy.config.searchpath = [ renpy.config.gamedir ]

    # Find the common directory.
    commondir = __main__.path_to_common(renpy.config.renpy_base)

    if os.path.isdir(commondir):
        renpy.config.searchpath.append(commondir)
        renpy.config.commondir = commondir
    else:
        renpy.config.commondir = None

    # Load Ren'Py extensions.
    for dir in renpy.config.searchpath:
        for fn in os.listdir(dir):
            if fn.lower().endswith(".rpe"):
                load_rpe(dir + "/" + fn)

        
    # The basename is the final component of the path to the gamedir.

    basename = renpy.config.gamedir
    if basename[-1] == '/':
        basename = basename[:-1]
    basename = os.path.basename(basename)

    # Look for an archived game.
    renpy.config.archives = [ ]

    for i in basename, "game", "data":

        if i in renpy.config.archives:
            continue
        
        try:
            renpy.loader.transfn(i + ".rpa")
            renpy.config.archives.append(i)
            continue
        except:
            continue

    # Note the profile option.
    if renpy.game.options.profile:
        renpy.config.profile = True

    # Initialize archives.
    renpy.loader.index_archives()

    # Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Find the save directory.
    renpy.config.savedir = __main__.path_to_saves(renpy.config.gamedir)

    if renpy.game.options.savedir:
        renpy.config.savedir = renpy.game.options.savedir
    
    # Initialize the store.
    renpy.store.store = renpy.store

    # Load the script.
    renpy.game.exception_info = 'While loading the script.'
    game.script = renpy.script.load_script()

    if renpy.parser.report_parse_errors():
        raise renpy.game.ParseErrorException()
    
    renpy.game.exception_info = 'After loading the script.'

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

    # Set up styles.
    renpy.style.reset()
    game.style = renpy.style.StyleManager()
    renpy.store.style = game.style

    renpy.game.exception_info = 'While executing init code:'

    # Run init code in its own context. (Don't log.)
    game.contexts = [ renpy.execution.Context(False) ]

    # Run the init code.
    game.init_phase = True

    for prio, node in game.script.initcode:
        game.context().run(node)

    game.init_phase = False
    
    renpy.game.exception_info = 'After initialization, but before game start.'

    # Save the bytecode in a cache.
    renpy.game.script.save_bytecode()
    
    # Rebuild the various style caches.
    renpy.style.build_styles()

    # Index the archive files. We should not have loaded an image
    # before this point. (As pygame will not have been initialized.)
    # We need to do this again because the list of known archives
    # may have changed.
    renpy.loader.index_archives()

    # Make a clean copy of the store.
    game.clean_store = renpy.store.__dict__.copy()

    if renpy.game.options.compile:
        return

    if renpy.game.options.lint:
        try:
            renpy.lint.lint()
            return
        except:
            raise

    # Remove the list of all statements from the script.
    game.script.all_stmts = None

    # (Perhaps) Initialize graphics.
    if not game.interface:
        game.interface = renpy.display.core.Interface()


    # Start things running.
    restart = None

    renpy.game.exception_info = 'While running game code:'

    while True:
        try:
            try:
                run(restart)
            finally:
                restart = "end_game"
                save_persistent()
                
        except game.QuitException, e:
            break
        except game.FullRestartException, e:
            restart = e.reason
