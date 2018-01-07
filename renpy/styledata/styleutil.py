# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

# Utility functions used by the various property functions:

import renpy


def none_is_null(o):
    if o is None:
        return renpy.display.layout.Null()  # @UndefinedVariable
    else:
        return renpy.easy.displayable(o)


def expand_focus_mask(v):
    if v is None:
        return v
    elif v is False:
        return v
    elif v is True:
        return v
    elif callable(v):
        return v
    else:
        return renpy.easy.displayable(v)


def expand_outlines(l):
    rv = [ ]

    for i in l:
        if len(i) == 2:
            rv.append((i[0], renpy.easy.color(i[1]), 0, 0))
        else:
            rv.append((i[0], renpy.easy.color(i[1]), i[2], i[3]))

    return rv

# Names for anchors.
ANCHORS = dict(
    left=0.0,
    right=1.0,
    center=0.5,
    top=0.0,
    bottom=1.0,
    )


def expand_anchor(v):
    """
    Turns an anchor into a number.
    """

    try:
        return ANCHORS.get(v, v)
    except:
        # This fixes some bugs in very old Ren'Pys.

        for n in ANCHORS:
            o = getattr(renpy.store, n, None)
            if o is None:
                continue

            if v is o:
                return ANCHORS[n]

        raise
