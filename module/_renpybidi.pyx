# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

cdef extern from "fribidi.h":
    int FRIBIDI_TYPE_LTR
    int FRIBIDI_TYPE_ON
    int FRIBIDI_TYPE_RTL
    int FRIBIDI_TYPE_WR
    int FRIBIDI_TYPE_WL

cdef extern from "renpybidicore.h":
    object renpybidi_log2vis(unicode, int *)

WLTR = FRIBIDI_TYPE_WL
LTR = FRIBIDI_TYPE_LTR
ON = FRIBIDI_TYPE_ON
RTL = FRIBIDI_TYPE_RTL
WRTL = FRIBIDI_TYPE_WR


def log2vis(unicode s, int direction=FRIBIDI_TYPE_ON):

    s = renpybidi_log2vis(s, &direction)
    return s, direction

