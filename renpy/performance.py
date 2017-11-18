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


def log(depth, event, *args):

    if (not renpy.config.profile) or (not running):
        return

    try:
        fpl.append((time.time(), depth, event.format(*args)))
    except:
        raise


def PPP(event, *args):
    log(3, event, *args)


__builtins__['PPP'] = PPP


def analyze():
    """
    Analyze the FPL and prints a report.
    """

    if not fpl:
        return

    if renpy.config.frames < 30:
        return

    start = fpl[0][0]

    for t, _, event in fpl:
        if event == renpy.config.profile_to_event:
            end = t
            break
    else:
        return

    if (end - start) < renpy.config.profile_time:
        return

    print("\n")

    times = [ fpl[0][0] ] * DEPTH_LEVELS

    for t, depth, event in fpl:
        dt = [ (1000000 * (t - it)) if i <= depth else 0 for i, it in enumerate(times) ]

        print("{: 7.0f} {: 7.0f} {: 7.0f} {: 7.0f} {}".format(
            dt[0],
            dt[1],
            dt[2],
            dt[3],
            event,
            ))

        for i in range(depth, DEPTH_LEVELS):
            times[i] = t
