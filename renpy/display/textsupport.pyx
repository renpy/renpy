# Constants that control glyph splitting.
SPLIT_NONE=0 # Can't split at this glyph.
SPLIT_BEFORE=1 # Can split before this glyph. 
SPLIT_INSTEAD=2 # Can split at this glyph - and it gets removed if we do.

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
    
    
def annotate_western(list glyphs):
    """
    Annotate the characters with line splitting information.
    """
    
    cdef Glyph g
    
    for g in glyphs:
        if g.character == 0x20 or g.character == 0x200b:
            g.split = SPLIT_INSTEAD
        else:
            g.split = SPLIT_NONE


def linebreak_greedy(list glyphs, int first_width, int rest_width):
    """
    Starting with a list of glyphs, decides where to split it. The result of
    this is the same list of glyphs, but with some of the .split fields set
    back to SPLIT_NONE, where we decided not to go ahead with the split after
    all.
    
    This is the greedy algorithm, which splits when the line is longer 
    than a specified width.
    """

    cdef Glyph g, split_g
    cdef float width, linewidth, splitwidth
    
    width = first_width
    split_g = None
    
    # The width of the line.
    linewidth = 0
    
    # The width of the line after being split at the last split point.
    splitwidth = 0
    
    for g in glyphs:
                
        linewidth += g.advance
        splitwidth += g.advance
        
        if linewidth > width and split_g is not None:
            linewidth = splitwidth
            split_g = None
            
        if g.split == SPLIT_INSTEAD:
            if split_g is not None:
                split_g.split = SPLIT_NONE
                
            split_g = g
            splitwidth = 0

        elif g.split == SPLIT_BEFORE:
            
            if split_g is not None:
                split_g.split = SPLIT_NONE
            
            split_g = g
            splitwidth = g.advance

            
def linebreak_debug(list glyphs):
    """
    Return a string giving the results of linebreaking a list of gylphs.
    """
    
    cdef Glyph g
     
    rv = ""
     
    for g in glyphs:
        
        if g.split == SPLIT_INSTEAD:
            rv += "|"
        elif g.split == SPLIT_BEFORE:
            rv += "[" + unichr(g.character)
        else:
            rv += unichr(g.character)
            
    return rv
            
                
    
           
    