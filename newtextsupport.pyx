cdef class Glyph:
    
    def __repr__(self):
        return "<Glyph {!r}, width={}, advance={}>".format(self.character, self.width, self.advance)
     