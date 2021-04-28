# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import *

import pygame_sdl2 as pygame
import math
import renpy.display

DIRECTIONS = [ "n", "ne", "e", "se", "s", "sw", "w", "nw" ]


def dispatch_gesture(gesture):
    """
    This is called with a gesture to dispatch it as an event.
    """

    event = renpy.config.gestures.get(gesture, None)
    if event is not None:
        renpy.exports.queue_event(event)
        raise renpy.display.core.IgnoreEvent()


class GestureRecognizer(object):

    def __init__(self):
        super(GestureRecognizer, self).__init__()

        self.x = None
        self.y = None

    def start(self, x, y):

        # The last coordinates we saw motion at.
        self.x = x
        self.y = y

        # Minimum sizes for gestures.
        self.min_component = renpy.config.screen_width * renpy.config.gesture_component_size
        self.min_stroke = renpy.config.screen_width * renpy.config.gesture_stroke_size

        # The direction of the current strokes.
        self.current_stroke = None

        # The length of the current stroke.
        self.stroke_length = 0

        # A list of strokes we've recognized.
        self.strokes = [ ]

    def take_point(self, x, y):
        if self.x is None:
            return

        dx = x - self.x
        dy = y - self.y

        length = math.hypot(dx, dy)

        if length < self.min_component:
            return

        self.x = x
        self.y = y

        angle = math.atan2(dx, -dy) * 180 / math.pi + 22.5

        if angle < 0:
            angle += 360

        stroke = DIRECTIONS[int(angle / 45)]

        if stroke == self.current_stroke:
            self.stroke_length += length
        else:
            self.current_stroke = stroke
            self.stroke_length = length

        if self.stroke_length > self.min_stroke:
            if (not self.strokes) or (self.strokes[-1] != stroke):
                self.strokes.append(stroke)

    def finish(self):
        rv = None

        if self.x is None:
            return

        if self.strokes:
            func = renpy.config.dispatch_gesture

            if func is None:
                func = dispatch_gesture

            rv = func("_".join(self.strokes))

        self.x = None
        self.y = None

        return rv

    def cancel(self):
        self.x = None
        self.y = None

    def event(self, ev, x, y):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            self.start(x, y)

        elif ev.type == pygame.MOUSEMOTION:
            if ev.buttons[0]:
                self.take_point(x, y)

        elif ev.type == pygame.MOUSEBUTTONUP:
            self.take_point(x, y)

            if ev.button == 1:
                return self.finish()


recognizer = GestureRecognizer()
