cdef class Glyph:
    
    def __repr__(self):
        return "<Glyph {!r}, width={}, advance={}>".format(self.character, self.width, self.advance)

TEXT=1
TAG=2
PARAGRAPH=3
DISPLAYABLE=4

def tokenize(unicode s):
    """
    This tokenizes a unicode string into text tags and tokens. It returns a list of 
    pairs, where each pair begins with either TEXT or TAG, and then has the contents 
    of the text run or tag.
    """      
    
    cdef int start
    cdef int pos
    cdef int len_s
    cdef list rv
    
    pos = 0
    len_s = len(s)
    
    rv = [ ]
    
    while pos < len_s:

        if s[pos] == u"\n":
            pos += 1
            rv.append((PARAGRAPH, ""))
            continue
                    
        # Do we have a text tag?
        if s[pos] == u"{" and (pos == len_s - 1 or s[pos+1] != u"{"):
            
            start = pos + 1
            
            while pos < len_s:
                if s[pos] == u"}":
                    break

                pos += 1
                
            if pos >= len_s:
                raise Exception("Text tag open at end of string: %r" % s)
                
            rv.append((TAG, s[start:pos]))
            pos += 1
            
            continue
        
        start = pos 
        pos += 1
        
        while pos < len_s:
            if s[pos] == u"{" or s[pos] == u"\n":
                break
            pos += 1
            
        rv.append((TEXT, s[start:pos]))
        
    return rv
    
    
    