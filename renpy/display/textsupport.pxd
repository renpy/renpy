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
        public int character
        
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
        