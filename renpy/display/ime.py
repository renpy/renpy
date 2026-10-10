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

# Support for drawing the IME candidate list inside the game, rather than
# relying on the platform's IME window, which may be hidden when the game
# is fullscreen.

from __future__ import annotations

from typing import Any, NamedTuple

import renpy


class IMECandidates(NamedTuple):
    """
    The candidate list supplied by the platform IME.
    """

    candidates: tuple[str, ...]
    "The candidate strings."

    selected: int
    "The index of the selected candidate, or -1 if no candidate is selected."

    horizontal: bool
    "True if the candidates should be laid out horizontally."

    @classmethod
    def from_event(cls, ev: Any) -> IMECandidates | None:
        """
        Creates an IMECandidates from a TEXTEDITINGCANDIDATES event, or
        returns None if the event does not contain any candidates.
        """

        candidates = tuple(getattr(ev, "candidates", None) or ())

        if not candidates:
            return None

        selected = getattr(ev, "selected", -1)

        # SDL may report an index that is not on the current page of
        # candidates, so ignore it if it's out of range.
        if not (0 <= selected < len(candidates)):
            selected = -1

        return cls(candidates, selected, bool(getattr(ev, "horizontal", False)))


def place_candidates(
    text_rect: tuple[float, float, float, float],
    size: tuple[float, float],
    screen_size: tuple[float, float],
) -> tuple[float, float]:
    """
    Returns the position of the top-left corner of a candidate window of
    `size`, placed below `text_rect` (or above it, if there isn't room
    below), and kept within a screen of `screen_size`.
    """

    tx, ty, _tw, th = text_rect
    w, h = size
    sw, sh = screen_size

    x = tx
    y = ty + th

    if y + h > sh and ty - h >= 0:
        y = ty - h

    x = max(0, min(x, sw - w))
    y = max(0, min(y, sh - h))

    return x, y


def get_candidates() -> IMECandidates | None:
    """
    Returns the candidate list to display, or None if none should be shown.
    """

    interface = renpy.display.interface

    if interface is None:
        return None

    return interface.text_editing_candidates


class IMECandidatesPlacer(renpy.display.layout.Container):
    """
    Places its child near the active text input, so it can be used to
    display the IME candidate list.
    """

    def render(self, width, height, st, at):
        rv = renpy.display.render.Render(width, height)
        self.offsets = [ ]

        if not self.children:
            return rv

        # The text rectangle is only known after a frame is drawn, so use
        # the one from the previous frame, and redraw to follow it.
        renpy.display.render.redraw(self, 0)

        interface = renpy.display.interface
        text_rect = interface.ime_text_rect if interface is not None else None

        if text_rect is None:
            return rv

        cr = renpy.display.render.render(self.children[0], width, height, st, at)
        x, y = place_candidates(text_rect, cr.get_size(), (width, height))
        rv.blit(cr, (int(x), int(y)))
        self.offsets = [(int(x), int(y))]

        return rv
