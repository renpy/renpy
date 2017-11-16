# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

# This file manages the frame performance log.

from __future__ import print_function, unicode_literals
import time

import renpy

# A list of (time, depth, message) tuples.
fpl = [ ]

# The number of levels of depth we use.
DEPTH_LEVELS = 4

# Are we running? Only log stuff if the FPL has been cleared at least
# once.
running = False


def clear():
    global fpl
    fpl = [ ]

    global running
    running = True


def log(depth, message):

    if not running:
        return

    fpl.append((time.time(), depth, message))


def analyze():
    """
    Analyze the FPL and prints a report.
    """

    if not fpl:
        return

    if renpy.config.frames < 30:
        return

    start = fpl[0][0]
    end = fpl[-1][0]

    if (end - start) < .025:
        return

    renpy.log.real_stderr.write("\n")

    times = [ fpl[0][0] ] * DEPTH_LEVELS

    for t, depth, message in fpl:
        dt = [ (1000000 * (t - it)) if i <= depth else 0 for i, it in enumerate(times) ]

        renpy.log.real_stderr.write("{: 7.0f} {: 7.0f} {: 7.0f} {: 7.0f} {}\n".format(
            dt[0],
            dt[1],
            dt[2],
            dt[3],
            message,
            ))

        for i in range(depth, DEPTH_LEVELS):
            times[i] = t
