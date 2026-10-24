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

from types import SimpleNamespace

import pytest

from renpy.display.ime import IMECandidates, place_candidates


def test_from_event():
    """A candidates event becomes an IMECandidates with the list as a tuple, the selection, and the layout."""

    ev = SimpleNamespace(candidates=["a", "b", "c"], selected=1, horizontal=True)
    assert IMECandidates.from_event(ev) == IMECandidates(("a", "b", "c"), 1, True)


def test_from_event_empty():
    """
    An event with an empty candidate list, or with no candidate attributes at all, produces None so that
    no candidate window is shown.
    """

    assert IMECandidates.from_event(SimpleNamespace(candidates=[], selected=-1, horizontal=False)) is None
    assert IMECandidates.from_event(SimpleNamespace()) is None


@pytest.mark.parametrize("selected", [-1, 3, 12])
def test_from_event_out_of_range_selection(selected):
    """
    A selected index outside the candidate list becomes -1 (no selection).

    SDL may report an index that is not on the current page of candidates. Parametrized over "no
    selection", one past the end, and far past the end.
    """

    ev = SimpleNamespace(candidates=["a", "b", "c"], selected=selected, horizontal=False)
    assert IMECandidates.from_event(ev).selected == -1


def test_below():
    """When there's room, the candidate window goes directly below the text rectangle, left-aligned with it."""

    assert place_candidates((100, 100, 10, 20), (50, 40), (800, 600)) == (100, 120)


def test_flip_above():
    """When the window would run off the bottom of the screen, it is placed directly above the text instead."""

    assert place_candidates((100, 570, 10, 20), (50, 40), (800, 600)) == (100, 530)


def test_clamp_right():
    """A window that would run off the right edge is shifted left to fit on the screen."""

    assert place_candidates((780, 100, 10, 20), (50, 40), (800, 600)) == (750, 120)


def test_clamp_when_no_room_above_or_below():
    """
    A window too tall to fit either above or below the text stays below it, clamped so its bottom is at
    the bottom of the screen. It overlaps the text, but stays visible.
    """

    assert place_candidates((100, 20, 10, 20), (50, 590), (800, 600)) == (100, 10)
