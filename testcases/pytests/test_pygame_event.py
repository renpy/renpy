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
Tests for converting SDL events into Ren'Py event objects in renpy.pygame.event.

The keyboard tests run without a window, so text input is never active. That is the case of a game with no focused input,
where KEYDOWN events get their unicode character from the keyboard layout. With no video subsystem, SDL uses its
default US keymap, so the expected characters are those of a US layout.
"""

import pytest

import renpy.display.behavior
from renpy import pygame

# SDL scancodes (USB HID usage IDs), which renpy.pygame does not expose.
SCANCODE_I: int = 12
SCANCODE_1: int = 30
SCANCODE_F1: int = 58
SCANCODE_KP_1: int = 89


def make_keydown(scancode: int, key: int, mod: int = 0):
    """
    Returns the event object the event queue would produce for an SDL KEYDOWN with these fields.
    """

    return pygame.event._make_keyboard_event(pygame.KEYDOWN, scancode, key, mod)


@pytest.mark.parametrize(
    "scancode, key, mod, expected",
    [
        (SCANCODE_I, pygame.K_i, 0, "i"),
        (SCANCODE_I, pygame.K_i, pygame.KMOD_LSHIFT, "I"),
        (SCANCODE_I, pygame.K_i, pygame.KMOD_CAPS, "I"),
        (SCANCODE_I, pygame.K_i, pygame.KMOD_LCTRL, "i"),
        (SCANCODE_1, pygame.K_1, 0, "1"),
        (SCANCODE_1, pygame.K_1, pygame.KMOD_RSHIFT, "!"),
        (SCANCODE_F1, pygame.K_F1, 0, ""),
        (SCANCODE_KP_1, pygame.K_KP_1, pygame.KMOD_NUM, ""),
    ],
)
def test_keydown_unicode_without_text_input(scancode, key, mod, expected):
    """
    Without text input, a KEYDOWN gets the character the key types in the layout, with shift and caps lock
    applied, and keys that do not type a character get an empty string.

    Ctrl does not change the character; keymap matching checks it separately. Keypad keycodes are outside
    the Unicode range, even with num lock on, so keypad digits get no character.
    """

    assert make_keydown(scancode, key, mod).unicode == expected


def test_keyup_has_no_unicode():
    """
    A KEYUP never carries a character, so single-character keysyms only match key presses.
    """

    ev = pygame.event._make_keyboard_event(pygame.KEYUP, SCANCODE_I, pygame.K_i, 0)
    assert ev.unicode == ""


def test_single_character_keysym_matches_without_text_input():
    """
    A screen's `key "i"` matches pressing I when no input is focused, and `key "I"` matches shift+I but not I.

    This is the regression in issue #7530: under SDL3, KEYDOWN events had no unicode unless text input was
    active, so single-character keysyms only matched while the player typed in an input.
    """

    plain = make_keydown(SCANCODE_I, pygame.K_i)
    shifted = make_keydown(SCANCODE_I, pygame.K_i, pygame.KMOD_LSHIFT)

    assert renpy.display.behavior.map_event(plain, "i")
    assert not renpy.display.behavior.map_event(plain, "I")
    assert renpy.display.behavior.map_event(shifted, "I")
    assert not renpy.display.behavior.map_event(shifted, "i")


@pytest.mark.parametrize("kind", ["FINGERDOWN", "FINGERUP", "FINGERMOTION", "FINGERCANCELED"])
def test_finger_event_fields(kind):
    """
    Touch finger events carry their touch and finger IDs, position, motion, and pressure, under both the
    pygame 2 names (touch_id, finger_id) and the older camelCase names (touchId, fingerId).

    This is the regression in issue #7541: the conversion read misspelled SDL3 field names, so these events
    raised AttributeError when taken from the queue, and FINGERCANCELED events carried no fields at all.
    The touch ID is above 2**32 to check that 64-bit IDs are not truncated.
    """

    event_type = getattr(pygame, kind)
    touch_id = 2**40 + 12

    ev = pygame.event._make_finger_event(event_type, touch_id, 34, 0.25, 0.75, 0.125, -0.5, 0.5)

    assert ev.type == event_type
    assert ev.touch_id == touch_id
    assert ev.touchId == touch_id
    assert ev.finger_id == 34
    assert ev.fingerId == 34
    assert (ev.x, ev.y) == (0.25, 0.75)
    assert (ev.dx, ev.dy) == (0.125, -0.5)
    assert ev.pressure == 0.5
