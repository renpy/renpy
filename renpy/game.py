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

# The basepath. Everything that is loaded is relative to this, at least
# until we get around to implementing archive files.
basepath = None

# A Script object, giving the script of the currently executing game.
script = None

# The store is where Ren'Py python results are stored. We first need
# to import in the module, and then we use the module's dictionary
# directly.
store = None

# A shallow copy of the store made at the end of the init phase. If
# a key in here points to the same value here as it does in the store,
# it is not saved.
clean_store = None

# A stack of execution contexts.
contexts = [ ]

# The interface that the game uses to interact with the user.
interface = None

# Are we still running init blocks?
init_phase = True

# The RollbackLog that keeps track of changes to the game state
# and to the store.
log = None

# Some useful additional information about program execution that
# can be added to the exception.
exception_info = ''

# Used to store style information.
style = None

class RestartException(Exception):
    """
    This class will be used to convey to the system that the context has
    been changed, and therefore execution needs to be restarted.
    """

class QuitException(Exception):
    """
    An exception of this class will let us force a safe quit, from
    anywhere in the program. Do not pass go, do not collect $200.
    """

def context(index=-1):
    """
    Return the current execution context, or the context at the
    given index if one is specified.
    """

    return contexts[index]

def call_in_new_context(label):
    """
    This code creates a new context, and starts executing code from
    that label in the new context. Rollback is disabled in the
    new context. (Actually, it will just bring you back to the
    real context.)
    """

    context = renpy.execution.Context(False, contexts[-1])
    contexts.append(context)

    context.goto_label(label)
    context.run()

    contexts.pop()
    interface.redraw(0)
