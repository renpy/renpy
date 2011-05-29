cdef class Glyph:

    # The character this glyph represents.
    cdef:
    
        # The x and y coordinates of the placed character.
        public short x, y
    
        # The character we use.
        public int character
        
        # Controls splitting of this glyph, based on where we are in the
        # the line.
        char split
                
        # The ascent and descent of the font.
        public short ascent
        public short descent
        
        # The width and advance of the font.
        public float width
        public float advance
        