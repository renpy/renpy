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
