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
from renpy.exports.commonexports import renpy_pure


def imagemap(ground, selected, hotspots, unselected=None, overlays=False,
             style='imagemap', mouse='imagemap', with_none=None, **properties):
    """
    :undocumented: Use screens already.

    Displays an imagemap. An image map consists of two images and a
    list of hotspots that are defined on that image. When the user
    clicks on a hotspot, the value associated with that hotspot is
    returned.

    @param ground: The name of the file containing the ground
    image. The ground image is displayed for areas that are not part
    of any hotspots.

    @param selected: The name of the file containing the selected
    image. This image is displayed in hotspots when the mouse is over
    them.

    @param hotspots: A list of tuples defining the hotspots in this
    image map. Each tuple has the format (x0, y0, x1, y1, result).
    (x0, y0) gives the coordinates of the upper-left corner of the
    hotspot, (x1, y1) gives the lower-right corner, and result gives
    the value returned from this function if the mouse is clicked in
    the hotspot.

    @param unselected: If provided, then it is the name of a file
    containing the image that's used to fill in hotspots that are not
    selected as part of any image. If not provided, the ground image
    is used instead.

    @param overlays: If True, overlays are displayed when this imagemap
    is active. If False, the overlays are suppressed.

    @param with_none: If True, performs a with None after the input. If None,
    takes the value from config.implicit_with_none.
    """

    renpy.exports.mode('imagemap')

    renpy.ui.imagemap_compat(ground, selected, hotspots, unselected=unselected,
                             style=style, **properties)

    roll_forward = renpy.exports.roll_forward_info()
    if roll_forward not in [ result for _x0, _y0, _x1, _y1, result in hotspots]:
        roll_forward = None

    if renpy.exports.in_fixed_rollback() and renpy.config.fix_rollback_without_choice:
        renpy.ui.saybehavior()

    rv = renpy.ui.interact(suppress_overlay=(not overlays),
                           type='imagemap',
                           mouse=mouse,
                           roll_forward=roll_forward)

    renpy.exports.checkpoint(rv)

    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv


def pause(delay=None, music=None, with_none=None, hard=False, predict=False, checkpoint=None, modal=None):
    """
    :doc: se_pause
    :args: (delay=None, *, predict=False, modal=True, hard=False)

    Causes Ren'Py to pause. Returns true if the user clicked to end the pause,
    or false if the pause timed out or was skipped.

    `delay`
        If given, the number of seconds Ren'Py should pause for.

    The following should be given as keyword arguments:

    `predict`
        If True, when all prediction - including prediction scheduled with
        :func:`renpy.start_predict` and :func:`renpy.start_predict_screen` - has
        been finished, the pause will be ended.

        This also causes Ren'Py to prioritize prediction over display smoothness
        for the duration of the pause. Because of that, it's recommended to not
        display animations during prediction.

        The pause will still end by other means - when the user clicks or skips,
        or when the delay expires (if any).

    `modal`
        If True, a timed pause will not end (it will hold) when a modal screen
        is being displayed.
        If False, the pause will end while a modal screen is being displayed.

    `hard`
        When True, Ren'Py may prevent the user from clicking to interrupt the
        pause. If the player enables skipping, the hard pause will be skipped.
        There may be other circumstances where the hard pause ends early or
        prevents Ren'Py from operating properly, these will not be treated as
        bugs.

        In general, using hard pauses is rude. When the user clicks to advance
        the game, it's an explicit request - the user wishes the game to
        advance. To override that request is to assume you understand what the
        player wants more than the player does.

        tl;dr - Don't use renpy.pause with hard=True.

    Calling renpy.pause guarantees that whatever is on the screen will be
    displayed for at least one frame, and hence has been shown to the
    player.
    """

    if renpy.config.skipping == "fast":
        return False

    if checkpoint is None:
        if delay is not None:
            checkpoint = False
        else:
            checkpoint = True

    roll_forward = renpy.exports.roll_forward_info()

    if type(roll_forward) not in (bool, renpy.game.CallException, renpy.game.JumpException):
        roll_forward = None

    if (delay is not None) and renpy.game.after_rollback and not renpy.config.pause_after_rollback:

        rv = roll_forward
        if rv is None:
            rv = False

        if checkpoint:
            renpy.exports.checkpoint(rv, keep_rollback=True, hard=False)

        return rv

    renpy.exports.mode('pause')

    if music is not None:
        newdelay = renpy.audio.music.get_delay(music)

        if newdelay is not None:
            delay = newdelay

    if (delay is not None) and renpy.game.after_rollback and roll_forward is None:
        delay = 0

    if delay is None:
        afm = " "
    else:
        afm = None

    if hard or not renpy.store._dismiss_pause:
        renpy.ui.saybehavior(afm=afm, dismiss='dismiss_hard_pause', dismiss_unfocused=[])
    else:
        renpy.ui.saybehavior(afm=afm)

    if predict:
        renpy.display.interface.force_prediction = True
        renpy.ui.add(renpy.display.behavior.PredictPauseBehavior())

    try:
        rv = renpy.ui.interact(mouse='pause', type='pause', roll_forward=roll_forward, pause=delay, pause_modal=modal)
    except (renpy.game.JumpException, renpy.game.CallException) as e:
        rv = e

    if checkpoint:
        renpy.exports.checkpoint(rv, keep_rollback=True, hard=renpy.config.pause_after_rollback or (delay is None))

    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    if isinstance(rv, (renpy.game.JumpException, renpy.game.CallException)):
        raise rv

    return rv


def with_statement(trans, always=False, paired=None, clear=True):
    """
    :doc: se_with
    :name: renpy.with_statement
    :args: (trans, always=False)

    Causes a transition to occur. This is the Python equivalent of the
    with statement.

    `trans`
        The transition.

    `always`
        If True, the transition will always occur, even if the user has
        disabled transitions.

    This function returns true if the user chose to interrupt the transition,
    and false otherwise.
    """

    if renpy.game.context().init_phase:
        raise Exception("With statements may not run while in init phase.")

    if renpy.config.skipping:
        trans = None

    if not (renpy.game.preferences.transitions or always): # type: ignore
        trans = None

    renpy.exports.mode('with')

    if isinstance(trans, dict):

        for k, v in trans.items():
            if k is None:
                continue

            renpy.exports.transition(v, layer=k)

        if None not in trans:
            return

        trans = trans[None]

    return renpy.game.interface.do_with(trans, paired, clear=clear)


def jump(label):
    """
    :doc: se_jump

    Causes the current statement to end, and control to jump to the given
    label.
    """

    raise renpy.game.JumpException(label)


def call(label, *args, **kwargs):
    """
    :doc: se_call
    :args: (label, *args, from_current=False, **kwargs)

    Causes the current Ren'Py statement to terminate, and a jump to a
    `label` to occur. When the jump returns, control will be passed
    to the statement following the current statement.

    The label must be either of the form "global_name" or "global_name.local_name".
    The form ".local_name" is not allowed.

    `from_current`
        If true, control will return to the current statement, rather than
        the statement following the current statement. (This will lead to
        the current statement being run twice. This must be passed as a
        keyword argument.)
    """

    from_current = kwargs.pop("from_current", False)
    raise renpy.game.CallException(label, args, kwargs, from_current=from_current)


def return_statement(value=None):
    """
    :doc: se_call

    Causes Ren'Py to return from the current Ren'Py-level call.
    """

    renpy.store._return = value
    jump("_renpy_return")


def call_screen(_screen_name, *args, **kwargs):
    """
    :doc: screens
    :args: (_screen_name, *args, _with_none=True, _mode="screen", **kwargs)

    The programmatic equivalent of the call screen statement.

    This shows `_screen_name` as a screen, then causes an interaction
    to occur. The screen is hidden at the end of the interaction, and
    the result of the interaction is returned.

    Positional arguments, and keyword arguments that do not begin with
    _ are passed to the screen.

    If `_with_none` is false, "with None" is not run at the end of end
    of the interaction.

    If `_mode` is passed, it will be the mode of this interaction,
    otherwise the mode will be "screen".
    """

    mode = kwargs.pop("_mode", "screen")
    renpy.exports.mode(mode)

    with_none = kwargs.pop("_with_none", renpy.config.implicit_with_none)

    renpy.exports.show_screen(_screen_name, *args, _transient=True, **kwargs)

    roll_forward = renpy.exports.roll_forward_info()

    # If roll
    can_roll_forward = renpy.display.screen.get_screen_roll_forward(_screen_name)

    if can_roll_forward is None:
        can_roll_forward = renpy.config.call_screen_roll_forward

    if not can_roll_forward:
        roll_forward = None

    try:
        rv = renpy.ui.interact(mouse="screen", type="screen", roll_forward=roll_forward)
    except (renpy.game.JumpException, renpy.game.CallException) as e:
        rv = e

    renpy.exports.checkpoint(rv)

    if with_none:
        renpy.game.interface.do_with(None, None)

    if isinstance(rv, (renpy.game.JumpException, renpy.game.CallException)):
        raise rv

    return rv


def execute_default_statement(start=False):
    """
    :undocumented:

    Executes the default statement.

    `start`
        This is true at the start of the game, and false at other
        times.
    """

    for i in renpy.ast.default_statements:
        i.execute_default(start)

    for i in renpy.config.after_default_callbacks:
        i()
