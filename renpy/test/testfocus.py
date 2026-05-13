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

import random

import renpy
from renpy.display.focus import Focus
from renpy.display.displayable import Displayable
from renpy.test.types import Position


def find_focus(pattern: str, raw: bool) -> Focus | None:
    """
    Finds the focus with the shortest alt text containing `pattern`.
    Returns the Focus if found, else None.
    """

    pattern = pattern.casefold()
    candidates: list[tuple[int, Focus]] = []

    for focus in renpy.display.focus.focus_list:
        if focus.x is None:
            text = _get_default_focus_text(raw)
        else:
            text = focus.widget._tts_all(raw)

        if pattern in text.casefold():
            candidates.append((len(text), focus))

    return min(candidates, key=lambda x: x[0], default=(None, None))[1]


def _get_default_focus_text(raw: bool) -> str:
    """
    Searches for the current say node, and if found, uses its text.
    If not found, falls back to using TTS text from the root widget.
    """
    current_node = renpy.game.script.lookup(renpy.game.context().current)

    if not isinstance(current_node, renpy.ast.TranslateSay):
        return renpy.display.tts.root._tts_all(raw)

    untranslated_node: renpy.ast.TranslateSay = renpy.game.script.translator.default_translates[current_node.identifier]
    if raw:
        return untranslated_node.what
    return renpy.substitutions.substitute(untranslated_node.what, None)[0]


def relative_to_absolute(posx: int | float, width: int) -> int:
    if isinstance(posx, float):
        return int(posx * (width - 1))
    else:
        return posx


def find_position(f: Focus | Displayable | None, position: Position | tuple[None, None]) -> tuple[int, int]:
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

    if f is None:
        # No target, avoid moving the mouse when unnecessary.
        if posx is not None:
            x = relative_to_absolute(posx, renpy.config.screen_width)
        elif renpy.test.testmouse.mouse_pos is not None:
            x = renpy.test.testmouse.mouse_pos[0]
        else:
            x = random.randrange(renpy.config.screen_width)

        if posy is not None:
            y = relative_to_absolute(posy, renpy.config.screen_height)
        elif renpy.test.testmouse.mouse_pos is not None:
            y = renpy.test.testmouse.mouse_pos[1]
        else:
            y = random.randrange(renpy.config.screen_height)

        return x, y

    orig_f = f

    # Check for the default widget.
    if f.x is None:
        f = f.copy()
        f.x = 0
        f.y = 0
        f.w = renpy.config.screen_width
        f.h = renpy.config.screen_height
    else:
        f = f.copy()
        f.x = int(f.x)
        f.y = int(f.y)
        f.w = int(f.w)
        f.h = int(f.h)

    for _i in range(renpy.test.testsettings._test.focus_trials):
        # Randomize position if not specified
        if posx is not None:
            x = relative_to_absolute(posx, f.w) + f.x
        else:
            x = random.randrange(f.x, f.x + f.w)

        if posy is not None:
            y = relative_to_absolute(posy, f.h) + f.y
        else:
            y = random.randrange(f.y, f.y + f.h)

        nf = renpy.display.render.focus_at_point(x, y)  # type: ignore

        if nf is None:
            if orig_f.x is None:
                return x, y
        else:
            if (nf.widget == f.widget) and (nf.arg == f.arg):
                return x, y

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
    stack = [(renpy.display.render.screen_render, 0, 0, None)]  # type: ignore
    while stack:
        r, x, y, screen = stack.pop()

        if not isinstance(r, renpy.display.render.Render):  # type: ignore
            continue

        if d in r.render_of:
            return Focus(widget=d, arg=None, x=x, y=y, w=r.width, h=r.height, screen=screen)

        if r.render_of and isinstance(r.render_of[0], renpy.display.screen.ScreenDisplayable):
            screen = r.render_of[0]

        for r in r.children:
            ## We care about the absolute position of the displayable, not the position relative to the parent.
            stack.append((r[0], x + r[1], y + r[2], screen))

    return None
