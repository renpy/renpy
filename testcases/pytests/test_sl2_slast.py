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


"""Tests for screen-language execution that do not need a running game."""

import pytest

import renpy
from renpy.display.screen import ScreenNotFound
from renpy.sl2.slast import SLContext, SLUse


def test_missing_screen_restores_ui_stack():
    """
    Using a screen that does not exist raises ScreenNotFound without leaving a partial entry on
    renpy.ui.stack.

    execute_use_screen pushes the context before calling use_screen and pops it in a finally block, so the
    stack must be unchanged after the exception. Compares stack identity, not only length, so that a
    push/pop pair replacing an entry is still caught.
    """

    node = SLUse(("test_slparser.py", 1), "slparser_missing_screen", None, None, None, None)
    old_stack = list(renpy.ui.stack)

    with pytest.raises(ScreenNotFound):
        node.execute_use_screen(SLContext())

    assert len(renpy.ui.stack) == len(old_stack)
    assert all(a is b for a, b in zip(renpy.ui.stack, old_stack))
