# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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


"""Tests for renpy.jump_out_of_context and ui.jumpsoutofcontext, which leave a menu context for a label."""

import pytest

import renpy

JUMPERS = [
    pytest.param(renpy.exports.jump_out_of_context, id="jump_out_of_context"),
    pytest.param(lambda label: renpy.ui.jumpsoutofcontext(label)(), id="ui.jumpsoutofcontext"),
]


@pytest.mark.parametrize("jump", JUMPERS)
def test_jump_out_of_outermost_context_is_an_error(mocker, jump):
    """
    In the outermost context, nothing catches JumpOutException, so it used to end the game with an uncaught
    control exception. It must raise an ordinary error instead, which Ren'Py reports and lets the player ignore.

    renpy.game.contexts is replaced because the test process has no running game; only its length matters.
    """

    mocker.patch.object(renpy.game, "contexts", [object()])

    with pytest.raises(Exception, match="'start'") as excinfo:
        jump("start")

    assert not isinstance(excinfo.value, renpy.game.CONTROL_EXCEPTIONS)


@pytest.mark.parametrize("jump", JUMPERS)
def test_jump_out_of_menu_context(mocker, jump):
    """
    In a nested context, such as the main menu, the jump still raises JumpOutException with the label, which
    invoke_in_new_context and call_in_new_context turn into a jump in the parent context.
    """

    mocker.patch.object(renpy.game, "contexts", [object(), object()])

    with pytest.raises(renpy.game.JumpOutException) as excinfo:
        jump("start")

    assert excinfo.value.args == ("start",)
