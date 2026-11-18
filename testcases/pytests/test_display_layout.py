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

"""
Tests for AlphaMask's size and for how it places its child and mask.
"""

import pickle

import pytest

import renpy
from renpy.display.displayable import Displayable
from renpy.display.layout import AlphaMask
from renpy.display.render import Render


class Probe(Displayable):
    """
    A displayable of a fixed size that remembers the render it returned and the events it received, so a test can see
    where it was drawn and which coordinates its events arrived at.
    """

    def __init__(self, size, **properties):
        super().__init__(**properties)

        self.size = size
        self.rendered = None
        self.available = None
        self.events = []

    def render(self, width, height, st, at):
        self.available = (width, height)
        self.rendered = Render(*self.size)
        self.rendered.add_focus(self, None, 0, 0, *self.size)
        return self.rendered

    def event(self, ev, x, y, st):
        self.events.append((x, y))


@pytest.fixture(autouse=True)
def draw(mocker):
    """Replaces the display's draw object, so rendering doesn't touch a real graphics device."""

    rv = mocker.patch.object(renpy.display, "draw", mocker.Mock())
    rv.draw_to_virt.transform.return_value = (1, 1)

    return rv


@pytest.fixture(autouse=True)
def default_style(mocker):
    """
    Defines the default style, which rendering reads and which is normally created by renpy/common/00style.rpy, a file
    the pytest engine doesn't run. Both the registry and the shared style object are patched, so that a style built
    against the stand-in doesn't outlive the test.
    """

    mocker.patch.dict(renpy.style.styles, {("default",): renpy.style.Style(None, {"xminimum": 0, "yminimum": 0})})
    mocker.patch.object(renpy.display.displayable, "default_style", renpy.style.Style("default"))


def drawn_at(render, target, x=0, y=0):
    """
    Returns the position of `target` in `render`'s coordinates, without depending on how many intermediate renders
    AlphaMask uses. Returns None if `target` isn't in the tree.
    """

    if render is target:
        return (x, y)

    for child, child_x, child_y, _focus, _main in render.children:
        if isinstance(child, Render):
            found = drawn_at(child, target, x + child_x, y + child_y)

            if found is not None:
                return found

    return None


def render_mask(displayable, width=1000, height=1000):
    """Renders `displayable` in a large area, so a test can tell the area offered from the size of the result."""

    return renpy.display.render.render(displayable, width, height, 0, 0)


@pytest.mark.parametrize(
    "child_size, mask_size, expected",
    [
        ((100, 50), (100, 50), (100, 50)),
        ((100, 50), (200, 80), (200, 80)),
        ((200, 80), (100, 50), (200, 80)),
        # Each dimension is independent, so neither displayable is the larger one in both.
        ((100, 80), (200, 50), (200, 80)),
    ],
)
def test_size_is_the_larger_of_child_and_mask(child_size, mask_size, expected):
    """The AlphaMask is as wide as the wider of its displayables, and as tall as the taller."""

    assert render_mask(AlphaMask(Probe(child_size), Probe(mask_size), place_child=True)).get_size() == expected


def test_mask_is_offered_the_size_of_the_child():
    """
    A mask that fills the space it's offered must fill the child, not the area offered to the AlphaMask. Without this,
    a Solid or Frame mask would make the AlphaMask as big as the screen.
    """

    child = Probe((100, 50))
    mask = Probe((100, 50))

    render_mask(AlphaMask(child, mask, place_child=True))

    assert child.available == (1000, 1000)
    assert mask.available == (100, 50)


def test_filling_mask_takes_the_size_of_the_child():
    """A real displayable that fills its available space doesn't enlarge the AlphaMask."""

    assert render_mask(AlphaMask(Probe((100, 50)), renpy.display.imagelike.Solid("#fff"), place_child=True)).get_size() == (100, 50)


@pytest.mark.parametrize(
    "properties, expected",
    [
        ({"xoffset": -10, "yoffset": 20}, (-10, 20)),
        ({"xpos": 30, "ypos": 40}, (30, 40)),
        # Aligning is relative to the AlphaMask, which the mask makes larger than the child.
        ({"xalign": 1.0, "yalign": 0.5}, (100, 15)),
    ],
)
def test_child_position_properties_are_honored(properties, expected):
    """The child's position properties place it inside the AlphaMask, where the mask stays still."""

    child = Probe((100, 50), **properties)
    mask = Probe((200, 80))

    rv = render_mask(AlphaMask(child, mask, place_child=True))

    assert drawn_at(rv, child.rendered) == expected
    assert drawn_at(rv, mask.rendered) == (0, 0)


def test_mask_position_is_relative_to_the_alphamask():
    """A mask is placed in the AlphaMask's area, and its offsets don't change the size of the AlphaMask."""

    child = Probe((100, 50))
    mask = Probe((60, 50), xalign=1.0, yoffset=25)

    rv = render_mask(AlphaMask(child, mask, place_child=True))

    assert rv.get_size() == (100, 50)
    assert drawn_at(rv, mask.rendered) == (40, 25)


def test_events_use_the_position_of_the_child():
    """A child that has moved must get events in its own coordinates, or its buttons would be in the wrong place."""

    child = Probe((100, 50), xoffset=30, yoffset=40)
    alpha_mask = AlphaMask(child, Probe((200, 80)), place_child=True)

    render_mask(alpha_mask)
    alpha_mask.event(None, 35, 47, 0)

    assert child.events == [(5, 7)]


def test_focus_uses_the_subpixel_position_of_the_child():
    """A subpixel child is drawn at a fractional position, so its focus area must be there too, not truncated."""

    child = Probe((10, 10), xoffset=0.75, subpixel=True)

    rv = render_mask(AlphaMask(child, Probe((100, 100)), place_child=True))

    assert rv.focus_at_point(0.5, 5, None) is None
    assert rv.focus_at_point(10.5, 5, None) is not None


@pytest.mark.parametrize("arguments", [{}, {"place_child": False}])
def test_default_layout_ignores_the_position_of_the_child(arguments):
    """Unless asked to, the child's size is used, its position is ignored, and the mask is cropped to it."""

    child = Probe((100, 50), xoffset=30, yoffset=40)
    mask = Probe((200, 80), xoffset=5)
    alpha_mask = AlphaMask(child, mask, **arguments)

    rv = render_mask(alpha_mask)
    alpha_mask.event(None, 35, 47, 0)

    assert rv.get_size() == (100, 50)
    assert drawn_at(rv, child.rendered) == (0, 0)
    assert drawn_at(rv, mask.rendered) == (5, 0)
    assert child.events == [(35, 47)]


def test_old_pickle_gets_the_default():
    """An AlphaMask saved before place_child existed must load and keep the layout it was saved with."""

    alpha_mask = AlphaMask(renpy.display.layout.Null(100, 50), renpy.display.layout.Null(200, 80))
    del alpha_mask.place_child

    loaded = pickle.loads(pickle.dumps(alpha_mask))

    assert render_mask(loaded).get_size() == (100, 50)
