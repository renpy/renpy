# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Optional, Any

import renpy

# The basepath.
basepath = None

# A list of paths that we search to load things. This is searched for
# everything that can be loaded, before archives are used.
searchpath = [ ]

# The options that were read off the command line.
args = None # type: Any

# The game's script.
script = None # type: Optional[renpy.script.Script]

# A stack of execution contexts.
contexts = [ ]

# The interface that the game uses to interact with the user.
interface = None # type: Optional[renpy.display.core.Interface]

# Are we inside lint?
lint = False

# The RollbackLog that keeps track of changes to the game state
# and to the store.
log = None # type: renpy.rollback.RollbackLog|None

# Some useful additional information about program execution that
# can be added to the exception.
exception_info = ''

# Used to store style information.
style = None

# The set of statements we've seen in this session.
seen_session = { }

# The number of entries in persistent._seen_translates that are also in
# the current game.
seen_translates_count = 0

# The number of new translates we've seen today.
new_translates_count = 0

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
persistent = None # type: Any

# The current preferences.
preferences = None # type: Any

# Current id of the AST node in script initcode
initcode_ast_id = 0


class ExceptionInfo(object):
    """
    Context manager that sets exception_info iff an exception occurs.

    `s`
        A percent-format string to use.
    `args`
        The arguments that are percent-formatted with `s`.
    """

    def __init__(self, s, args):
        self.s = s
        self.args = args

    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            renpy.game.exception_info = self.s % self.args

        return False


class RestartContext(Exception):
    """
    Restarts the current context. If `label` is given, calls that label
    in the restarted context.
    """


class RestartTopContext(Exception):
    """
    Restarts the top context. If `label` is given, calls that label
    in the restarted context.
    """


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

    from_current = False

    def __init__(self, label, args, kwargs, from_current=False):
        Exception.__init__(self)

        self.label = label
        self.args = args
        self.kwargs = kwargs
        self.from_current = from_current

    def __reduce__(self):
        return (CallException, (self.label, self.args, self.kwargs, self.from_current))


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


def invoke_in_new_context(callable, *args, **kwargs): # @ReservedAssignment
    """
    :doc: context

    This function creates a new context, and invokes the given Python
    callable (function) in that context. When the function returns
    or raises an exception, control returns to the the original context.
    It's generally used to call a Python function that needs to display
    information to the player (like a confirmation prompt) from inside
    an event handler.

    Additional arguments and keyword arguments are passed to the
    callable.

    A context created with this function cannot execute Ren'Py script.
    Functions that would change the flow of Ren'Py script, like
    :func:`renpy.jump`, are handled by the outer context. If you want
    to call Ren'Py script rather than a Python function, use
    :func:`renpy.call_in_new_context` instead.
    """

    restart_context = False

    renpy.display.focus.clear_focus()

    context = renpy.execution.Context(False, contexts[-1], clear=True)
    contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    try:

        return callable(*args, **kwargs)

    except renpy.game.RestartContext:
        restart_context = True
        raise

    except renpy.game.RestartTopContext:
        restart_context = True
        raise

    except renpy.game.JumpOutException as e:

        contexts[-2].force_checkpoint = True
        contexts[-2].abnormal = True
        raise renpy.game.JumpException(e.args[0])

    finally:

        if not restart_context:
            context.pop_all_dynamic()

        contexts.pop()
        contexts[-1].do_deferred_rollback()

        if interface and interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None


def call_in_new_context(label, *args, **kwargs):
    """
    :doc: context

    This creates a new context, and then starts executing Ren'Py script
    from the given label in that context. Rollback is disabled in the
    new context, and saving/loading will occur in the top level
    context.

    Use this to begin a second interaction with the user while
    inside an interaction.
    """

    renpy.display.focus.clear_focus()

    context = renpy.execution.Context(False, contexts[-1], clear=True)
    contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    if args:
        renpy.store._args = args
    else:
        renpy.store._args = None

    if kwargs:
        renpy.store._kwargs = renpy.revertable.RevertableDict(kwargs)
    else:
        renpy.store._kwargs = None

    try:

        context.goto_label(label)
        return renpy.execution.run_context(False)

    except renpy.game.JumpOutException as e:
        contexts[-2].force_checkpoint = True
        contexts[-2].abnormal = True
        raise renpy.game.JumpException(e.args[0])

    finally:

        contexts.pop()
        contexts[-1].do_deferred_rollback()

        if interface and interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None


def call_replay(label, scope={}):
    """
    :doc: replay

    Calls a label as a memory.

    The `scope` argument is used to set the initial values of variables in the
    memory context.
    """

    renpy.display.focus.clear_focus()

    renpy.game.log.complete()

    old_log = renpy.game.log
    renpy.game.log = renpy.python.RollbackLog()

    sb = renpy.python.StoreBackup()
    renpy.python.clean_stores()

    context = renpy.execution.Context(True)
    contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    # This has to be here, to ensure the scope stuff works.
    renpy.exports.execute_default_statement()

    for k, v in renpy.config.replay_scope.items():
        setattr(renpy.store, k, v)

    for k, v in scope.items():
        setattr(renpy.store, k, v)

    renpy.store._in_replay = label

    try:

        context.goto_label("_start_replay")
        renpy.execution.run_context(False)

    except EndReplay:
        pass

    finally:

        context.pop_all_dynamic()

        contexts.pop()
        renpy.game.log = old_log
        sb.restore()

        if interface and interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None

        renpy.config.skipping = None

    if renpy.config.after_replay_callback:
        renpy.config.after_replay_callback()


# Type information.
if False:
    script = renpy.script.Script()
    interface = renpy.display.core.Interface()
    log = renpy.python.RollbackLog()
    preferences = renpy.preferences.Preferences()
