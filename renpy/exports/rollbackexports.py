# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import renpy


def roll_forward_info():
    """
    :doc: rollback

    When in rollback, returns the data that was supplied to :func:`renpy.checkpoint`
    the last time this statement executed. Outside of rollback, returns None.
    """

    if not renpy.game.context().rollback:
        return None

    return renpy.game.log.forward_info()


def roll_forward_core(value=None):
    """
    :undocumented:

    To cause a roll_forward to occur, return the value of this function
    from an event handler.
    """

    if value is None:
        value = roll_forward_info()
    if value is None:
        return

    renpy.game.interface.suppress_transition = True
    renpy.game.after_rollback = True
    renpy.game.log.rolled_forward = True

    return value


def in_rollback():
    """
    :doc: rollback

    Returns true if the game has been rolled back.
    """

    return renpy.game.log.in_rollback() or renpy.game.after_rollback


def can_rollback():
    """
    :doc: rollback

    Returns true if we can rollback.
    """

    if not renpy.config.rollback_enabled:
        return False

    if not renpy.store._rollback:
        return False

    if not renpy.game.context().rollback:
        return False

    return renpy.game.log.can_rollback()


def in_fixed_rollback():
    """
    :doc: blockrollback

    Returns true if rollback is currently occurring and the current
    context is before an executed renpy.fix_rollback() statement.
    """

    return renpy.game.log.in_fixed_rollback()


def checkpoint(data=None, keep_rollback=None, hard=True):
    """
    :doc: rollback
    :args: (data=None, *, hard=True)

    Makes the current statement a checkpoint that the user can rollback to. Once
    this function has been called, there should be no more interaction with the
    user in the current statement.

    This will also clear the current screenshot used by saved games.

    `data`
        This data is returned by :func:`renpy.roll_forward_info` when the
        game is being rolled back.

    `hard`
        If true, this is a hard checkpoint that rollback will stop at. If false,
        this is a soft checkpoint that will not stop rollback.
    """

    if keep_rollback is None:
        keep_rollback = renpy.config.keep_rollback_data

    renpy.game.log.checkpoint(data, keep_rollback=keep_rollback, hard=renpy.store._rollback and hard)

    if renpy.store._rollback and renpy.config.auto_clear_screenshot:
        renpy.game.interface.clear_screenshot = True


def block_rollback(purge=False):
    """
    :doc: blockrollback
    :args: ()

    Prevents the game from rolling back to before the current
    statement.
    """

    renpy.game.log.block(purge=purge)


def suspend_rollback(flag):
    """
    :doc: rollback
    :args: (flag)

    Rollback will skip sections of the game where rollback has been
    suspended.

    `flag`:
        When `flag` is true, rollback is suspended. When false,
        rollback is resumed.
    """

    renpy.game.log.suspend_checkpointing(flag)


def fix_rollback():
    """
    :doc: blockrollback

    Prevents the user from changing decisions made before the current
    statement.
    """
    renpy.game.log.fix_rollback()


def retain_after_load():
    """
    :doc: retain_after_load

    Causes data modified between the current statement and the statement
    containing the next checkpoint to be retained when a load occurs.
    """

    renpy.game.log.retain_after_load()



def rollback(force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=True, current_label=None):
    """
    :doc: rollback
    :args: (force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=True)

    Rolls the state of the game back to the last checkpoint.

    `force`
        If true, the rollback will occur in all circumstances. Otherwise,
        the rollback will only occur if rollback is enabled in the store,
        context, and config.

    `checkpoints`
        Ren'Py will roll back through this many calls to renpy.checkpoint. It
        will roll back as far as it can, subject to this condition.

    `defer`
        If true, the call will be deferred until control returns to the main
        context.

    `greedy`
        If true, rollback will finish just after the previous checkpoint.
        If false, rollback finish just before the current checkpoint.

    `label`
        If not None, a label that is called when rollback completes.

    `abnormal`
        If true, the default, script executed after the transition is run in
        an abnormal mode that skips transitions that would have otherwise
        occured. Abnormal mode ends when an interaction begins.
    """

    if defer and not renpy.game.log.log:
        return

    if defer and len(renpy.game.contexts) > 1:
        renpy.game.contexts[0].defer_rollback = (force, checkpoints)
        return

    if not force:

        if not renpy.store._rollback:
            return

        if not renpy.game.context().rollback:
            return

        if not renpy.config.rollback_enabled:
            return

    renpy.config.skipping = None
    renpy.game.log.complete()
    renpy.game.log.rollback(checkpoints, greedy=greedy, label=label, force=(force is True), abnormal=abnormal, current_label=current_label)


def get_roll_forward():
    return renpy.game.interface.shown_window


def get_identifier_checkpoints(identifier):
    """
    :doc: rollback

    Given a rollback_identifier from a HistoryEntry object, returns the number
    of checkpoints that need to be passed to :func:`renpy.rollback` to reach
    that identifier. Returns None of the identifier is not in the rollback
    history.
    """

    return renpy.game.log.get_identifier_checkpoints(identifier)
