# This module is intended to be used as a singleton object.
# It's purpose is to store in one global all of the data that would
# be to annoying to lug around otherwise. 
#
# Many modules will probablt want to import this using a command like:
#
# import renpy.game as game
#
# These modules will then be able to access the various globals defined
# in this module as fields on game.

import renpy
import renpy.game as game
import os
from pickle import loads, dumps, HIGHEST_PROTOCOL

def run(restart=False, lint=False):
    """
    This is called during a single run of the script. Restarting the script
    will cause this to change.
    """

    renpy.game.exception_info = 'While beginning to run the game.'

    # Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Reload some things, in case this is a restart.
    renpy.store.reload()
    renpy.config.reload()

    # Note that this is a restart.
    renpy.store._restart = restart

    renpy.config.savedir = game.basepath + "/saves"

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
    
    # Clear the list of seen statements in this game.
    game.seen_session = { }

    # Initialize the preferences.
    if not game.persistent._preferences:
        game.persistent._preferences = game.Preferences()

    game.preferences = game.persistent._preferences

    # Initialize the store.
    renpy.store.store = renpy.store
    renpy.store.persistent = game.persistent
    renpy.store._preferences = game.preferences

    # Set up styles.
    renpy.style.reset()
    game.style = renpy.style.StyleManager()
    renpy.store.style = game.style

    # Run init code in its own context. (Don't log.)
    game.contexts = [ renpy.execution.Context(False) ]

    # Run the init code.
    game.init_phase = True

    for prio, node in game.script.initcode:
        game.context().run(node)

    game.init_phase = False

    renpy.game.exception_info = 'After initialization, but before game start.'

    # Rebuild the various style caches.
    renpy.style.build_styles()

    # Index the archive files. We should not have loaded an image
    # before this point. (As pygame will not have been initialized.)
    renpy.loader.index_archives()

    # Make a clean copy of the store.
    game.clean_store = vars(renpy.store).copy()

    if lint:
        renpy.lint.lint()
        return

    # Remove the list of all statements from the script.
    game.script.all_stmts = None

    # Re-Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Switch contexts, begin logging.
    game.contexts = [ renpy.execution.Context(True) ]

    # (Perhaps) Initialize graphics.
    if not game.interface:
        game.interface = renpy.display.core.Interface()

    # Jump to an appropriate start label.
    if game.script.has_label("_start"):
        game.context().goto_label('_start')
    else:
        game.context().goto_label('start')

    try:
        while True:

            # We first try running the script.
            try:
                game.context().run()
                break

            # We get this when the context has changed, and so we go and
            # start running from the new context.
            except game.RestartException, e:
                renpy.game.contexts = e.args[0]
                continue

            except game.QuitException, e:
                break
    finally:
        f = file(renpy.config.savedir + "/persistent", "wb")
        f.write(dumps(game.persistent).encode("zlib"))
        f.close()


    # And, we're done.
    
def main(basepath, lint=False):

    renpy.game.exception_info = 'While loading the script.'

    game.basepath = basepath
    renpy.config.searchpath = [ "common", basepath ]

    renpy.config.backup()

    # Load the script.
    game.script = renpy.script.load_script()

    # Start things running.

    restart = False

    while True:
        try:
            run(restart, lint=lint)
            break
        except game.FullRestartException, e:
            restart = True
            pass
