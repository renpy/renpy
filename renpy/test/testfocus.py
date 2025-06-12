# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

import random
import renpy
from renpy.display.focus import Focus
from renpy.display.displayable import Displayable
from renpy.test.types import Position


def find_focus(pattern: str | None) -> Focus | None:
    """
    Tries to find the focus with the shortest alt text containing `pattern`.
    If found, returns a random coordinate within that displayable.

    If `pattern` is None, returns a random coordinate that will trigger the
    default focus.

    If `pattern` could not be found, returns None.
    """

    if pattern is not None:
        pattern = pattern.casefold()

    def match(f: Focus) -> str | None:

        if pattern is None:
            if f.x is None:
                # one focus, at most, ever branches here
                # the main "click to continue" one
                # it's the only one, if any, to be retained in the matching list
                return "default"
            else:
                return None

        if f.x is None:
            t = renpy.display.tts.root._tts_all()
        else:
            t = f.widget._tts_all()

        if pattern in t.casefold():
            return t
        else:
            return None

    # A list of alt_text, focus pairs.
    matching: list[tuple[str, Focus]] = []

    for f in renpy.display.focus.focus_list:
        alt = match(f)

        if alt is not None:
            matching.append((alt, f))

    # This gets the matching displayable with the shortest alt text, which
    # is likely what we want.
    matching.sort(key=lambda a: (len(a[0]), a[0]))
    return matching[0][1]


def relative_position(x: int, posx: int | float | None, width: int) -> float:
    if posx is not None:
        if type(posx) is float:
            return posx * (width - 1)
        else:
            return posx

    return x


def find_position(
    f: Focus | Displayable | None,
    position: Position | tuple[None, None]
) -> tuple[int, int]:
    """
    Returns the virtual position of a coordinate located within focus `f`.
    If position is (None, None) returns the current mouse position (if in
    the focus), or a random position.

    If `f` is None, returns a position relative to the screen as a whole.
    """
    f_original = f

    if isinstance(f, Displayable):
        f = focus_from_displayable(f)

    posx, posy = position

    # Avoid moving the mouse when unnecessary.
    if renpy.test.testmouse.mouse_pos is not None:
        x, y = renpy.test.testmouse.mouse_pos
    else:
        x = random.randrange(renpy.config.screen_width)
        y = random.randrange(renpy.config.screen_height)

    if f is None:
        return (
            int(relative_position(x, posx, renpy.config.screen_width)),
            int(relative_position(y, posy, renpy.config.screen_height)),
            )

    orig_f = f

    # Check for the default widget.
    if f.x is None:
        f = f.copy()
        f.x = 0
        f.y = 0
        f.w = renpy.config.screen_width
        f.h = renpy.config.screen_height

    x = relative_position(x-f.x, posx, f.w) + f.x
    y = relative_position(y-f.y, posy, f.h) + f.y

    for _i in range(renpy.test.testast._test.focus_trials):
        x = int(x)
        y = int(y)

        nf = renpy.display.render.focus_at_point(x, y)

        if nf is None:
            if orig_f.x is None:
                return x, y
        else:
            if (nf.widget == f.widget) and (nf.arg == f.arg):
                return x, y

        x = random.randrange(int(f.x), int(f.x + f.w))
        y = random.randrange(int(f.y), int(f.y + f.h))

    if isinstance(f_original, Displayable):
        ## It's not guaranteed that the displayable is in the focus list, so we
        ## return our best guess.
        return f.x, f.y

    raise Exception("Could not locate the displayable.")


def focus_from_displayable(d: Displayable) -> Focus | None:
    """
    Returns a Focus object for the given displayable `d`.

    If the displayable is not in the focus list, we create a Focus object for
    it from the render tree,
    """

    for f in renpy.display.focus.focus_list:
        if f.widget == d:
            return f

    ## If we reach here, the displayable is not in the focus list.
    ## Search the render tree for it.
    stack = [(renpy.display.render.screen_render, 0, 0, None)]
    while stack:
        r, x, y, screen = stack.pop()

        if not isinstance(r, renpy.display.render.Render):
            continue

        if d in r.render_of:
            return Focus(widget=d, arg=None, x=x, y=y, w=r.width, h=r.height, screen=screen)

        if r.render_of and isinstance(r.render_of[0], renpy.display.screen.ScreenDisplayable):
            screen = r.render_of[0]

        for r in r.children:
            ## We care about the absolute position of the displayable, not the position relative to the parent.
            stack.append((r[0], x + r[1], y + r[2], screen))

    return None