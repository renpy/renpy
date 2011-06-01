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

        # Don't split ruby.
        if g.ruby != RUBY_NONE:
            continue
        
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
    cdef float width, x, splitx, gwidth
    
    width = first_width
    split_g = None
    
    # The x position of the current character. Invariant: x can never be more
    # that one character-width greater than width.
    x = 0
    
    # The x position after splitting the line.
    splitx = 0
    
    for g in glyphs:
                       
        # If the x coordinate is greater than the width of the screen, 
        # split at the last split point, if any.
        if x > width and split_g is not None:
            x = splitx
            split_g = None
            width = rest_width
            
        x += g.advance
        splitx += g.advance
 
        if g.split == SPLIT_INSTEAD:
            if split_g is not None:
                split_g.split = SPLIT_NONE
                
            split_g = g
            splitx = 0

        elif g.split == SPLIT_BEFORE:
            
            if split_g is not None:
                split_g.split = SPLIT_NONE
            
            split_g = g
            splitx = g.advance

    # Split at the last character, if necessary.
    if x > width:
        split_g = None

    if split_g is not None:
        split_g.split = SPLIT_NONE

            
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
            

def place_horizontal(list glyphs, float start_x, float first_indent, float rest_indent):
    """
    Place the glyphs horizontally, without taking into account the indentation
    at the start of the line. Returns the width of the laid-out line.
    """
    
    if not glyphs:
        return 0
    
    cdef Glyph g
    cdef float x, maxx
    
    x = start_x + first_indent
    maxx = 0
        
    for g in glyphs:

        if g.ruby == RUBY_TOP:
            continue
        
        if g.split == SPLIT_INSTEAD:
            x = start_x + rest_indent
            continue

        elif g.split == SPLIT_BEFORE:
            x = start_x + rest_indent

        g.x = <short> (x + .5)

        if maxx < x + g.width:
            maxx = x + g.width
        if maxx < x + g.advance:
            maxx = x + g.advance
            
        x += g.advance
            
    return maxx
    
def place_vertical(list glyphs, int y, int spacing, int leading):
    """
    Vertically places the non-ruby glyphs. Returns a list of line end heights,
    and the y-value for the top of the next line.
    """

    cdef Glyph g, gg
    
    cdef int pos, sol, len_glyphs, i
    cdef int ascent, line_spacing
    cdef bint end_line
    
    len_glyphs = len(glyphs)

    pos = 0
    sol = 0
    
    ascent = 0
    line_spacing = 0
        
    rv = [ ]
        
    y += leading
        
    while True:
        
        if pos == len_glyphs:
            end_line = True
        else:
            g = glyphs[pos]
            end_line = (g.split != SPLIT_NONE)
                
        if end_line:
            
            for i from sol <= i < pos:
                gg = glyphs[i]
                
                if gg.ruby == RUBY_TOP:
                    continue
                
                if gg.ascent:
                    gg.y = y + ascent
                
                else:
                    # Glyphs without ascents are displayables, which get 
                    # aligned to the top of the line. (Or they're image-font
                    # glyphs, which are the same.)                   
                    gg.y = y
            
            y += line_spacing
            y += spacing
            rv.append(y)
            y += leading

            sol = pos
            ascent = 0
            line_spacing = 0
            
        if pos == len_glyphs:
            break
                    
        if g.ascent > ascent:
            ascent = g.ascent
            
        if g.line_spacing > line_spacing:
            line_spacing = g.line_spacing        
    
        pos += 1
    
    return rv
    
def kerning(list glyphs, float amount):
    cdef Glyph g
    
    for g in glyphs:
        g.advance += amount
        

    