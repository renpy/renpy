# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

cdef enum split_t:
    SPLIT_NONE
    SPLIT_BEFORE
    SPLIT_INSTEAD

cdef enum ruby_t:
    RUBY_NONE
    RUBY_BOTTOM
    RUBY_TOP

cdef class Glyph:

    # The character this glyph represents.
    cdef:

        # The x and y coordinates of the placed character.
        public short x, y

        # The change in the amount this character was shifted to the right
        # when adjusting placement.
        public short delta_x_offset

        # The character we use.
        public unsigned int character

        # Controls splitting of this glyph, based on where we are in the
        # the line.
        split_t split

        # Is this ruby or not?
        ruby_t ruby

        # The ascent and spacing of the font.
        public short ascent
        public short line_spacing

        # The width and advance of the font.
        public float width
        public float advance

        # The time when this glyph should be shown.
        public float time

        # The hyperlink this is part of.
        public short hyperlink


cdef class Line:

    cdef:

        # The y coordinate of this line.
        public short y

        # The height of this line.
        public short height

        # The list of glyphs on this line.
        public list glyphs

        # The maximum time of any glyph in this line.
        public float max_time

        # Are we the last line in a paragraph?
        public bint eop
