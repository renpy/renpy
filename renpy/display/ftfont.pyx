from pygame cimport *
from freetype cimport *
from textsupport cimport Glyph, SPLIT_INSTEAD
import traceback

cdef extern char *freetype_error_to_string(int error)

# The freetype library object we use.
cdef FT_Library library

class FreetypeError(Exception):
    def __init__(self, code):
        Exception.__init__(self, "%d: %s" % (code, freetype_error_to_string(code)))

def init():
    
    cdef int error
    
    error = FT_Init_FreeType(&library)
    if error:
        raise FreetypeError(error)
    
cdef unsigned long io_func(FT_Stream stream, unsigned long offset, unsigned char *buffer, unsigned long count):
    """
    Seeks to offset, and then reads count bytes from the stream into buffer.
    """
    
    cdef FTFont font
    cdef char *cbuf
    
    font = <FTFont> stream.descriptor.pointer
    f = font.f 
    
    if font.offset != offset:

        try:
            f.seek(offset)
            font.offset = offset
        except:
            traceback.print_exc()
            return -1
        
    if count != 0:
        try:            
            buf = f.read(count)
            cbuf = buf
            count = len(buf)
            
            for i from 0 <= i < count:
                buffer[i] = cbuf[i]        
        except:            
            traceback.print_exc()
            return -1

    font.offset += count
            
    return count

cdef void close_func(FT_Stream stream):
    """
    Close the stream. 

    Currently does nothing, closing is taken care of at the Font 
    object level.
    """
    
    return            
    
cdef class FTFont(object):
    
    cdef:
        FT_StreamRec stream
        FT_Open_Args open_args
        FT_Face face

        # The file the font is read from.    
        object f
        
        # The offset in that file.
        unsigned long offset

        # A cache of various properties.
        float size
        bint bold
        bint italic
        float outline
        bint underline

        # Information used to modify the font.

        # Overhang - used for bold.
        int glyph_overhang
        
        # The amount to skew an italic face by.
        float glyph_italics
        
        # The offset and height of the underline.        
        int underline_offset
        int underline_height

        # How much we expand the font by, to leave space
        # for strokes.
        int expand
        
        # The stroker object.
        FT_Stroker stroker

        # Basic Y-direction metrics for this font.
        public int ascent
        public int descent
        public int height
        public int lineskip

        
    def __init__(self, f, index):
        
        cdef int error
        cdef unsigned long size
        
        # The file that the font is opened from.
        self.f = f
    
        f.seek(0, 2)
        size = f.tell()
        f.seek(0, 0)
    
        # The offset within the stream we're currently at.
        self.offset = 0

        self.open_args.flags = FT_OPEN_STREAM
        self.open_args.stream = &self.stream
        
        self.stream.size = size
        self.stream.pos = 0
        self.stream.descriptor.pointer = <void *> self
        self.stream.read = io_func
        self.stream.close = close_func

        error = FT_Open_Face(library, &self.open_args, index, &self.face)
        if error:
            raise FreetypeError(error)

        error = FT_Select_Charmap(self.face, FT_ENCODING_UNICODE)
        if error:
            raise FreetypeError(error)

        self.stroker = NULL;

    def setup(self, float size, bint bold, bint italic, float outline):
        """
        Changes the parameters of this font.
        """
        
        cdef int error
        cdef FT_Face face
        cdef FT_Fixed scale
        

        if self.size != size:
            self.size = size
        
            error = FT_Set_Char_Size(self.face, 0, <int> size * 64, 0, 0)
            if error:
                raise FreetypeError(error)

            face = self.face

            scale = face.size.metrics.y_scale

            self.ascent = FT_CEIL(face.size.metrics.ascender)
            self.descent = FT_FLOOR(face.size.metrics.descender)
            self.height = self.ascent - self.descent
            
            self.lineskip = FT_CEIL(face.size.metrics.height)
            if self.height > self.lineskip:
                self.lineskip = self.height                

            self.glyph_overhang = face.size.metrics.y_ppem / 10
            self.glyph_italics = 0.207 * self.height

            self.underline_offset = FT_FLOOR(FT_MulFix(face.underline_position, scale))
            self.underline_height = FT_FLOOR(FT_MulFix(face.underline_thickness, scale))

            if self.underline_height < 1:
                self.underline_height = 1

        self.bold = bold
        self.italic = italic
        
        # TODO: Set up expand and stroker.
                
        return

    def glyphs(self, unicode s):
        """
        Sizes s, returning a list of Glyph objects.
        """
        
        cdef FT_Face face
        cdef FT_GlyphSlot g
        cdef list rv
        cdef int len_s 
        cdef Py_UNICODE c, next_c
        cdef FT_UInt index, next_index
        cdef int error
        cdef Glyph gl
        cdef FT_Vector kerning
        cdef int kern
        cdef int advance

        cdef float min_advance, next_min_advance
                
        len_s = len(s)
        
        face = self.face
        g = face.glyph

        rv = [ ]
    
        if len_s:
    
            min_advance_next = 0        
            next_c = s[0]
            next_index = FT_Get_Char_Index(face, next_c)
    
        for i from 0 <= i < len_s:
            
            c = next_c 
            index = next_index
            min_advance = next_min_advance
            
            error = FT_Load_Glyph(face, index, 0)
            if error:
                raise FreetypeError(error)
            
            gl = Glyph()
            gl.character = c
            gl.ascent = self.ascent
            gl.line_spacing = self.lineskip            
            gl.width = FT_CEIL(g.metrics.width)
            advance = FT_ROUND(g.metrics.horiAdvance)
                        
            if i < len_s - 1:
                next_c = s[i + 1]
                next_index = FT_Get_Char_Index(face, next_c)
                
                error = FT_Get_Kerning(face, index, next_index, FT_KERNING_DEFAULT, &kerning)
                if error:
                    raise FreetypeError(error)
                
                kern = FT_ROUND(kerning.x)                
                
                if advance + kern > min_advance:
                    gl.advance = advance + kern
                else:
                    gl.advance = min_advance
                    
                next_min_advance = advance - gl.advance
                        
            rv.append(gl)
        
        return rv
    
    def draw(self, pysurf, float xo, int yo, color, list glyphs):
        """
        Draws a list of glyphs to surf, with the baseline starting at x, y.
        """
                
        cdef SDL_Surface *surf
        cdef unsigned int red, green, blue, a
        cdef unsigned int rshift, gshift, bshift, ashift
        cdef unsigned int fixed
        cdef unsigned int alpha
        cdef Glyph glyph
        
        cdef FT_Face face
        cdef FT_GlyphSlot g
        cdef FT_UInt index
        cdef int error
        cdef int bmx, bmy, px, py
                
        cdef unsigned int *pixels
        cdef unsigned int *line
        cdef unsigned char *gline 
        cdef int pitch
                
        print "XXX", color

        red, green, blue, a = color

        if a == 0:
            return

        # TODO: Grab these from SDL directly.
        rshift, gshift, bshift, ashift = pysurf.get_shifts()
        
        fixed = (red << rshift) | (green << gshift) | (blue << bshift)
        
        surf = PySurface_AsSurface(pysurf)
        pixels = <unsigned int *> surf.pixels
        pitch = surf.pitch / 4

        face = self.face
        g = face.glyph
                
        for glyph in glyphs:

            if glyph.split == SPLIT_INSTEAD:
                continue
                        
            x = glyph.x 
            y = glyph.y
            
            print x, y
            
            index = FT_Get_Char_Index(face, <Py_UNICODE> glyph.character)
            error = FT_Load_Glyph(face, index, 0)
            if error:
                raise FreetypeError(error)
            
            if g.format != FT_GLYPH_FORMAT_BITMAP:
                
                error = FT_Render_Glyph(g, FT_RENDER_MODE_NORMAL)
                if error:
                    raise FreetypeError(error)
                
                bmx = <int> (x + .5) + g.bitmap_left
                bmy = y - g.bitmap_top
                
                for py from 0 <= py < g.bitmap.rows:                    

                    line = pixels + bmy * pitch + bmx
                    gline = g.bitmap.buffer + py * g.bitmap.pitch
                    
                    for px from 0 <= px < g.bitmap.width:
                        
                        alpha = gline[0]
                        
                        print "%02x" % alpha,
                        
                        alpha = ((alpha * a + alpha)) >> 8 << ashift
                        line[0] = (alpha | fixed)
                        gline += 1
                        line += 1
                        
                    print
                        
                    bmy += 1

        print "SHIFTS", rshift, gshift, bshift, ashift
            
 
# Ideas for how text rendering will work:
#
# 1) Break things up into style/text pairs. Break into paragraphs
# at this point, process each paragraph separately.
# 2) Style objects lay out text into lists of glyph objects.
# 3) The glyph objects are combined into one list (per paragraph).
# 4) The paragraph lists are broken into lines, justified, and offset.
# 5) The style objects then draw the glyph objects.
