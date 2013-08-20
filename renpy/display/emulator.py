# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code to emulate various other devices on the PC.

import renpy.display

import os
import pygame

# The function that's called to perform the emulation.
emulator = None

# An overlay that is placed over the screen to support the emulator.
overlay = [ ]

def null_emulator(ev, x, y):
    """
    This is used when emulation is not desired.
    """
    return ev, x, y

TOUCH_KEYS = [ pygame.K_ESCAPE, pygame.K_PAGEUP ]

def touch_emulator(ev, x, y):
    """
    This emulates a touch-screen device, like a tablet or smartphone.
    """

    if ev.type == pygame.MOUSEBUTTONDOWN:
        if ev.button != 1:
            return None, x, y

    elif ev.type == pygame.MOUSEBUTTONUP:
        if ev.button != 1:
            return None, x, y

        move = pygame.event.Event(pygame.MOUSEMOTION, { "pos" : (0, 0), "rel" : (0, 0), "buttons" : (0, 0, 0) })
        renpy.display.interface.pushed_event = move

    elif ev.type == pygame.MOUSEMOTION:
        if not ev.buttons[0]:
            x = 0
            y = 0

    elif ev.type == pygame.KEYDOWN:
        if not ev.key in TOUCH_KEYS:
            return None, x, y

    elif ev.type == pygame.KEYUP:
        if not ev.key in TOUCH_KEYS:
            return None, x, y

    return ev, x, y


TV_KEYS = [ pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_PAGEUP ]

def tv_emulator(ev, x, y):
    """
    This emulates a tv-based device, like the OUYA.
    """

    if ev.type == pygame.MOUSEBUTTONDOWN:
        return None, x, y
    elif ev.type == pygame.MOUSEBUTTONUP:
        return None, x, y
    elif ev.type == pygame.MOUSEMOTION:
        return None, x, y
    elif ev.type == pygame.KEYDOWN:
        if not ev.key in TV_KEYS:
            return None, x, y
    elif ev.type == pygame.KEYDOWN:
        if not ev.key in TV_KEYS:
            return None, x, y

    return ev, x, y


def init_emulator():
    """
    Sets up the emulator.
    """

    global emulator
    global overlay

    name = os.environ.get("RENPY_EMULATOR", "")

    if name == "touch":
        emulator = touch_emulator
        overlay = [ ]
    elif name == "tv":
        emulator = tv_emulator
        overlay = [ renpy.display.motion.Transform(
            "_tv_unsafe.png",
            xalign=0.5,
            yalign=0.5,
            size=(int(renpy.config.screen_height * 16.0 / 9.0), renpy.config.screen_height),
            ) ]
    else:
        emulator = null_emulator
        overlay = [ ]
