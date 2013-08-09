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

# This file is responsible for joystick support in Ren'Py.

import os
import pygame

import renpy.display

# Do we have a joystick enabled?
enabled = False

# The old states for each axis.
old_axis_states = { }

def init():
    """
    Initialize the joystick system.
    """

    global enabled

    if not renpy.config.joystick:
        return

    if 'RENPY_DISABLE_JOYSTICK' in os.environ:
        return

    try:
        pygame.joystick.init()

        for i in range(0, pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
            enabled = True
    except:
        if renpy.config.debug:
            raise

def event(ev):

    if not enabled:
        return ev

    if ev.type == pygame.JOYAXISMOTION:

        if not renpy.display.interface.focused:
            return None

        if ev.value >= 0.5:
            state = "Positive"
        elif ev.value <= -0.5:
            state = "Negative"
        else:
            state = None

        oldstate = old_axis_states.get((ev.joy, ev.axis), None)

        if state == oldstate:
            return None

        if oldstate:
            release = "Axis %d.%d %s" % (ev.joy, ev.axis, oldstate)
        else:
            release = None

        old_axis_states[ev.joy, ev.axis] = state

        if state:
            press = "Axis %d.%d %s" % (ev.joy, ev.axis, state)
        else:
            press = None

        if not press and not release:
            return None

        return pygame.event.Event(renpy.display.core.JOYEVENT,
                                  press=press, release=release)

    if ev.type == pygame.JOYBUTTONDOWN:

        if not renpy.display.interface.focused:
            return None

        return pygame.event.Event(renpy.display.core.JOYEVENT,
                                  press="Button %d.%d" % (ev.joy, ev.button),
                                  release=None)
    if ev.type == pygame.JOYBUTTONUP:

        if not renpy.display.interface.focused:
            return None

        return pygame.event.Event(renpy.display.core.JOYEVENT,
                                  press=None,
                                  release="Button %d.%d" % (ev.joy, ev.button))

    return ev

class JoyBehavior(renpy.display.layout.Null):
    """
    This is a behavior intended for joystick calibration. If a joystick
    event occurs, this returns it as a string.
    """

    def event(self, ev, x, y, st):
        if ev.type == renpy.display.core.JOYEVENT:
            return ev.press

