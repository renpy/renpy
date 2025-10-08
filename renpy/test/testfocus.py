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

import random

import renpy
from renpy.display.focus import Focus
from renpy.display.displayable import Displayable
from renpy.test.types import Position


def find_focus(pattern: str, translate: bool = True, substitute: bool = True) -> Focus | None:
    """
    Tries to find the focus with the shortest alt text containing `pattern`.
    If found, returns a random coordinate within that displayable.

    If `pattern` is None, returns a random coordinate that will trigger the
    default focus.

    If `pattern` could not be found, returns None.
    """

    pattern = pattern.casefold()

    # {focus : (len(alt), alt)}
    matching: dict[Focus, tuple[int, str]] = {}

    for f in renpy.display.focus.focus_list:
        alt = match(f, pattern, translate, substitute)

        if alt is not None:
            matching[f] = (len(alt), alt)

    # This gets the matching displayable with the shortest alt text, which
    # is likely what we want.
    return min(matching, key=matching.get, default=None)  # type: ignore


def match(f: Focus, pattern: str, translate: bool = True, substitute: bool = True) -> str | None:
    """
    Checks if a focus matches the given pattern.
    Returns the matched text if found, None otherwise.
    """
    if f.x is None:
        text_to_match = _get_default_focus_text(translate, substitute)
    else:
        text_to_match = _get_focus_text(f.widget, translate, substitute)

    # Apply substitutions to the pattern if needed
    if substitute:
        pattern = renpy.substitutions.substitute(pattern, translate=False)[0]

    # Check if pattern matches
    if pattern in text_to_match.casefold():
        return text_to_match
    else:
        return None


def _get_default_focus_text(translate: bool, substitute: bool) -> str:
    """
    Gets text for the default focus. Searches for the current say node,
    and if found, uses its untranslated text. If not found, falls back to using
    TTS text from the root widget.
    """
    current_node = renpy.game.script.lookup(renpy.game.context().current)

    if not isinstance(current_node, renpy.ast.TranslateSay):
        return _get_focus_text(renpy.display.tts.root, translate, substitute)

    untranslated_node = renpy.game.script.translator.default_translates[current_node.identifier]
    assert isinstance(untranslated_node, renpy.ast.TranslateSay)
    return _process_text_segment(untranslated_node.what, translate, substitute)


def _get_focus_text(widget, translate: bool, substitute: bool) -> str:
    raw_text = widget._tts_all()

    # TTS text is already translated and substituted
    if substitute and (translate or renpy.game.preferences.language is None):
        return raw_text

    # Get the raw text segments from the widget tree, then process them
    text_children = _collect_text_children(widget)
    processed_segments = []

    for text_child in text_children:
        for text_segment in text_child.text_parameter:
            if isinstance(text_segment, str):
                processed_segment = _process_text_segment(text_segment, translate, substitute)
                processed_segments.append(processed_segment)
            # else:
            #     processed_segments.append(text_segment)

    return "¶".join(str(segment) for segment in processed_segments)


def _collect_text_children(widget: Displayable) -> list:
    """
    Collects all Text displayables from the widget tree.
    """
    text_children = []
    stack = [widget]

    while stack:
        current_widget = stack.pop()

        if isinstance(current_widget, renpy.text.text.Text):
            text_children.append(current_widget)
            continue

        if children := getattr(current_widget, "children", None):
            for child in reversed(children):
                stack.append(child)

    return text_children


def _process_text_segment(text: str, translate: bool, substitute: bool) -> str:
    """
    Processes a text segment according to translate and substitute flags.
    """
    if substitute:
        return renpy.substitutions.substitute(text, None, translate=translate)[0]
    elif translate:
        return renpy.translation.translate_string(text)
    else:
        return text


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
