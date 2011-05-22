cdef class Glyph:

    # The character this glyph represents.
    cdef:
    
        # The character we use.
        public unicode character
        
        # The ascent and descent of the font.
        public int ascent
        public int descent
        
        # The width and advance of the font.
        public float width
        public float advance
        