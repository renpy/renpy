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

# The basepath.
basepath = None

# A list of paths that we search to load things. This is searched for
# everything that can be loaded, before archives are used.
searchpath = [ ]

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

# The set of statements we've seen in this session.
seen_session = { }

# The set of statements we've ever seen.
seen_ever = { }

# The class that's used to hold the persistent data.
class Persistent(object):

    def __setstate__(self, data):
        vars(self).update(data)

    def __getstate__(self):
        return vars(self)

    # Undefined attributes return None.
    def __getattr__(self, attr):
        return None
        
# The persistent data that's kept from session to session
persistent = None

class Preferences(object):
    """
    Stores preferences that will one day be persisted.
    """
    def reinit(self):
        self.fullscreen = False
        self.music = True
        self.skip_unseen = False

        # 2 - All transitions.
        # 1 - Only non-default transitions.
        # 0 - No transitions.
        self.transitions = 2

    def __setstate__(self, state):
        self.reinit()
        vars(self).update(state)

    def __init__(self):
        self.reinit()

# The current preferences.
preferences = None

class RestartException(Exception):
    """
    This class will be used to convey to the system that the context has
    been changed, and therefore execution needs to be restarted.
    """

class FullRestartException(Exception):
    """
    An exception of this type forces a hard restart, completely
    destroying the store and config and so on.
    """

class QuitException(Exception):
    """
    An exception of this class will let us force a safe quit, from
    anywhere in the program. Do not pass go, do not collect $200.
    """

class JumpException(Exception):
    """
    This should be raised with a label as the only argument. This causes
    the current statement to terminate, and execution to be transferred
    to the named label.
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
