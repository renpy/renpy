# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# This module is intended to be used as a singleton object.
# It's purpose is to store in one global all of the data that would
# be to annoying to lug around otherwise.

import renpy.display

# The basepath.
basepath = None

# A list of paths that we search to load things. This is searched for
# everything that can be loaded, before archives are used.
searchpath = [ ]

# The options that were read off the command line.
args = None

# The game's script.
script = None

# A stack of execution contexts.
contexts = [ ]

# The interface that the game uses to interact with the user.
interface = None

# Are we inside lint?
lint = False

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

# True if we're in the first interaction after a rollback or rollforward.
after_rollback = False

# Code that's run after the init code.
post_init = [ ]

# Should we attempt to run in a mode that uses less memory?
less_memory = False

# Should we attempt to run in a mode that minimizes the number
# of screen updates?
less_updates = False

# Should we never show the mouse?
less_mouse = False

# Should we not imagedissiolve?
less_imagedissolve = False

# The persistent data that's kept from session to session
persistent = None

# The current preferences.
preferences = None

class RestartContext(Exception):
    """
    Restarts the current context. If `label` is given, calls that label
    in the restarted context.
    """

    def __init__(self, label):
        self.label = label

class RestartTopContext(Exception):
    """
    Restarts the top context. If `label` is given, calls that label
    in the restarted context.
    """

    def __init__(self, label):
        self.label = label

class FullRestartException(Exception):
    """
    An exception of this type forces a hard restart, completely
    destroying the store and config and so on.
    """

    def __init__(self, reason="end_game"): # W0231
        self.reason = reason

class UtterRestartException(Exception):
    """
    An exception of this type forces an even harder restart, causing
    Ren'Py and the script to be reloaded.
    """

class QuitException(Exception):
    """
    An exception of this class will let us force a safe quit, from
    anywhere in the program.

    `relaunch`
        If given, the program will run another copy of itself, with the
        same arguments.

    `status`
        The status code Ren'Py will return to the operating system.
    """

    def __init__(self, relaunch=False, status=0):
        Exception.__init__(self)
        self.relaunch = relaunch
        self.status = status

class JumpException(Exception):
    """
    This should be raised with a label as the only argument. This causes
    the current statement to terminate, and execution to be transferred
    to the named label.
    """

class JumpOutException(Exception):
    """
    This should be raised with a label as the only argument. This exits
    the current context, and then raises a JumpException.
    """

class CallException(Exception):
    """
    Raise this exception to cause the current statement to terminate,
    and control to be transferred to the named label.
    """

    def __init__(self, label, args, kwargs):
        Exception.__init__(self)

        self.label = label
        self.args = args
        self.kwargs = kwargs

class EndReplay(Exception):
    """
    Raise this exception to end the current replay (the current call to
    call_replay).
    """

class ParseErrorException(Exception):
    """
    This is raised when a parse error occurs, after it has been
    reported to the user.
    """

# A tuple of exceptions that should not be caught by the
# exception reporting mechanism.
CONTROL_EXCEPTIONS = (
    RestartContext,
    RestartTopContext,
    FullRestartException,
    UtterRestartException,
    QuitException,
    JumpException,
    JumpOutException,
    CallException,
    EndReplay,
    ParseErrorException,
    KeyboardInterrupt,
    )


def context(index=-1):
    """
    Return the current execution context, or the context at the
    given index if one is specified.
    """

    return contexts[index]

def invoke_in_new_context(callable, *args, **kwargs): #@ReservedAssignment
    """
    :doc: label

    This pushes the current context, and invokes the given python
    function in a new context. When that function returns or raises an
    exception, it removes the new context, and restores the current
    context.

    Additional arguments and keyword arguments are passed to the
    callable.

    Please note that the context so created cannot execute renpy
    code. So exceptions that change the flow of renpy code (like
    the one created by renpy.jump) cause this context to terminate,
    and are handled by the next higher context.

    If you want to execute renpy code from the function, you can call
    it with renpy.call_in_new_context.

    Use this to begin a second interaction with the user while
    inside an interaction.
    """

    context = renpy.execution.Context(False, contexts[-1], clear=True)
    contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    try:

        return callable(*args, **kwargs)

    except renpy.game.JumpOutException, e:

        raise renpy.game.JumpException(e.args[0])

    finally:

        contexts.pop()
        contexts[-1].do_deferred_rollback()

        if interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None



def call_in_new_context(label, *args, **kwargs):
    """
    :doc: label

    This code creates a new context, and starts executing code from
    that label in the new context. Rollback is disabled in the
    new context. (Actually, it will just bring you back to the
    real context.)

    Use this to begin a second interaction with the user while
    inside an interaction.
    """

    context = renpy.execution.Context(False, contexts[-1], clear=True)
    contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    if args:
        renpy.store._args = args
    else:
        renpy.store._args = None

    if kwargs:
        renpy.store._kwargs = renpy.python.RevertableDict(kwargs)
    else:
        renpy.store._kwargs = None

    try:

        context.goto_label(label)
        return renpy.execution.run_context(False)

    except renpy.game.JumpOutException, e:

        raise renpy.game.JumpException(e.args[0])

    finally:

        contexts.pop()
        contexts[-1].do_deferred_rollback()

        if interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None

def call_replay(label, scope={}):
    """
    :doc: replay

    Calls a label as a memory.

    Keyword arguments are used to set the initial values of variables in the
    memory context.
    """

    renpy.game.log.complete()

    old_log = renpy.game.log
    renpy.game.log = renpy.python.RollbackLog()

    sb = renpy.python.StoreBackup()
    renpy.python.clean_stores()

    context = renpy.execution.Context(True)
    contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    for k, v in scope.iteritems():
        setattr(renpy.store, k, v)

    renpy.store._in_replay = label

    try:

        context.goto_label("_start_replay")
        renpy.execution.run_context(False)

    except EndReplay:
        pass

    finally:
        contexts.pop()
        renpy.game.log = old_log
        sb.restore()

        if interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None


# Type information.
if False:
    script = renpy.script.Script()
    interface = renpy.display.core.Interface()
    log = renpy.python.RollbackLog()
    preferences = renpy.preferences.Preferences()
