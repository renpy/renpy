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

import renpy.script
import renpy.execution
import renpy.python
import renpy.config

# The basepath. Everything that is loaded is relative to this, at least
# until we get around to implementing archive files.
basepath = None

# A Script object, giving the script of the currently executing game.
script = None

# The store is where Ren'Py python results are stored. We first need
# to import in the module, and then we use the module's dictionary
# directly.
store = None

# A stack of execution contexts.
contexts = [ ]

# The interface that the game uses to interact with the user.
interface = None

# Are we still running init blocks?
init_phase = True

# The RollbackLog that keeps track of changes to the game state
# and to the store.
log = None

def context(index=-1):
    """
    Return the current execution context, or the context at the
    given index if one is specified.
    """

    return contexts[index]

class RestartException(Exception):
    """
    This class will be used to convey to the system that the context has
    been changed, and therefore execution needs to be restarted.
    """
    
def main(basepath_):
    global script
    global contexts
    global interface
    global basepath
    global store
    global init_phase
    global log

    basepath = basepath_

    # Finish loading the config.
    renpy.config.finish()

    # Load the script.
    script = renpy.script.load_script(basepath)

    # Initialize the store.
    import renpy.store as store
    store.store = store
    store = vars(renpy.store)

    # Initialize the log.
    log = renpy.python.RollbackLog()

    # Run init code in its own context. (Don't log.)
    contexts = [ renpy.execution.Context(False) ]

    # Run the init code.
    for i in script.initcode:
        context().run(i)

    # We're done running the initialization code.
    init_phase = False

    # Switch contexts, begin logging.
    contexts = [ renpy.execution.Context(True) ]

    # Initialize graphics.
    import renpy.display.core as dcore
    interface = dcore.Interface()

    # TODO: Make a clean copy of the store, for saving.
    
    context().goto_label('start')

    while True:

        # We first try running the script.
        try:
            context().run()
            break

        # We get this when the context has changed, and so we go and
        # start running from the new context.
        except RestartException, e:
            pass


    # And, we're done.
