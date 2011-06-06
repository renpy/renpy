from pygame cimport *
from freetype cimport *
from textsupport cimport Glyph, SPLIT_INSTEAD
import traceback

cdef extern char *freetype_error_to_string(int error)

# The freetype library object we use.
cdef FT_Library library

# Represents a cached glyph.
cdef struct glyph_cache:
    
    # The character we're caching. -1 if we're not representing a valid
    # character.
    int index
    
    int width
    float advance
        
    FT_Bitmap bitmap
    int bitmap_left
    int bitmap_top


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
    
    cdef FTFace face
    cdef char *cbuf
    
    face = <FTFace> stream.descriptor.pointer
    f = face.f 
    
    if face.offset != offset:

        try:
            f.seek(offset)
            face.offset = offset
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

    face.offset += count
            
    return count

cdef void close_func(FT_Stream stream):
    """
    Close the stream. 

    Currently does nothing, closing is taken care of at the Font 
    object level.
    """
    
    return            
    
    
cdef class FTFace:
    """
    Represents a freetype face.
    """
    
    cdef:
        FT_StreamRec stream
        FT_Open_Args open_args
        FT_Face face

        float size

        # The file the font is read from.    
        object f
        
        # The offset in that file.
        unsigned long offset
    
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
    
        # The size the face is at.
        self.size = -1
    
cdef class FTFont:
    
    cdef:

        FTFace face_object
        FT_Face face

        # A cache of various properties.
        float size
        float bold
        bint italic
        int outline
        bint antialias

        # Information used to modify the font.

        # Overhang - used for bold.
        int glyph_overhang
        
        # The amount to skew an italic face by.
        float glyph_italics
        
        # The offset and height of the underline.        
        public int underline_offset
        public int underline_height
        
        # The stroker object.
        FT_Stroker stroker

        # The number of pixels the outlines are expanded by.
        public int expand

        # Basic Y-direction metrics for this font.
        public int ascent
        public int descent
        public int height
        public int lineskip

        glyph_cache cache[256]
        

    def __cinit__(self):
        for i from 0 <= i < 256:
            self.cache[i].index = -1
            FT_Bitmap_New(&(self.cache[i].bitmap))

    def __dealloc__(self):
        for i from 0 <= i < 256:
            FT_Bitmap_Done(library, &(self.cache[i].bitmap))
        
        if self.stroker != NULL:
            FT_Stroker_Done(self.stroker)
        
        
    def __init__(self, face, float size, float bold, bint italic, int outline, bint antialias):
        
        self.face_object = face
        self.face = self.face_object.face
        
        self.size = size
        self.bold = bold
        self.italic = italic
        self.outline = outline
        self.antialias = antialias
        
        print "XXX", self.outline
        
        if outline == 0:        
            self.stroker = NULL;
            self.expand = 0            
            
        else:
            FT_Stroker_New(library, &self.stroker)
            FT_Stroker_Set(self.stroker, outline * 64, FT_STROKER_LINECAP_ROUND, FT_STROKER_LINEJOIN_ROUND, 0)
            self.expand = outline * 2
            print "Creating stroker with", self.outline

    cdef setup(self):
        """
        Changes the parameters of the face to match this font.
        """
        
        cdef int error
        cdef FT_Face face
        cdef FT_Fixed scale
                
        if self.face_object.size != self.size:
            self.face_object.size = self.size
        
            face = self.face

            error = FT_Set_Char_Size(face, 0, <int> (self.size * 64), 0, 0)
            if error:
                raise FreetypeError(error)

            scale = face.size.metrics.y_scale

            self.ascent = FT_CEIL(face.size.metrics.ascender) + self.expand
            self.descent = FT_FLOOR(face.size.metrics.descender) - self.expand
            self.height = self.ascent - self.descent
            
            self.lineskip = FT_CEIL(face.size.metrics.height) + self.expand
            if self.height > self.lineskip:
                self.lineskip = self.height                

            # self.glyph_overhang = face.size.metrics.y_ppem / 10
            # self.glyph_italics = 0.207 * self.height

            self.underline_offset = FT_FLOOR(FT_MulFix(face.underline_position, scale))
            self.underline_height = FT_FLOOR(FT_MulFix(face.underline_thickness, scale))

            if self.underline_height < 1:
                self.underline_height = 1

        # TODO: Set up expand and stroker.
                
        return

    cdef glyph_cache *get_glyph(self, int index):
        """
        Returns the glyph_cache object for a given glyph.
        """

        cdef FT_Face face
        cdef FT_Glyph g
        cdef FT_BitmapGlyph bg

        cdef int error
        cdef glyph_cache *rv

        rv = &(self.cache[index & 255])        
        if rv.index == index:            
            return rv
    
        rv.index = index
    
        face = self.face
        
        error = FT_Load_Glyph(face, index, 0)
        if error:
            raise FreetypeError(error)
        
        error = FT_Get_Glyph(face.glyph, &g)

        if error:
            raise FreetypeError(error)
    
        if g.format != FT_GLYPH_FORMAT_BITMAP:
    
            if self.stroker != NULL:
                FT_Glyph_StrokeBorder(&g, self.stroker, 0, 1)

            if self.antialias:
                FT_Glyph_To_Bitmap(&g, FT_RENDER_MODE_NORMAL, NULL, 1)
            else:
                FT_Glyph_To_Bitmap(&g, FT_RENDER_MODE_MONO, NULL, 1)

        bg = <FT_BitmapGlyph> g 
         
        if face.glyph.bitmap.pixel_mode != FT_PIXEL_MODE_GRAY:
            FT_Bitmap_Convert(library, &(bg.bitmap), &(rv.bitmap), 4)
        else:
            FT_Bitmap_Copy(library, &(bg.bitmap), &(rv.bitmap))
            
        rv.width = FT_CEIL(face.glyph.metrics.width) + self.expand
        rv.advance = face.glyph.metrics.horiAdvance / 64.0 + self.expand
    
        rv.bitmap_left = bg.left + self.expand / 2
        rv.bitmap_top = bg.top - self.expand / 2
    
        FT_Done_Glyph(g)
    
        return rv

    def glyphs(self, unicode s):
        """
        Sizes s, returning a list of Glyph objects.
        """
        
        cdef FT_Face face
        cdef list rv
        cdef int len_s 
        cdef Py_UNICODE c, next_c
        cdef FT_UInt index, next_index
        cdef int error
        cdef Glyph gl
        cdef FT_Vector kerning
        cdef int kern
        cdef float advance
        cdef int i
        cdef glyph_cache *cache

        cdef float min_advance, next_min_advance

        self.setup()
                        
        len_s = len(s)
        
        face = self.face
        g = face.glyph

        rv = [ ]
    
        if len_s:
    
            next_min_advance = 0        
            next_c = s[0]
            next_index = FT_Get_Char_Index(face, next_c)
    
        for i from 0 <= i < len_s:
            
            c = next_c 
            index = next_index
            min_advance = next_min_advance

            cache = self.get_glyph(index)
                        
            gl = Glyph()

            gl.character = c
            gl.ascent = self.ascent
            gl.line_spacing = self.lineskip            
            gl.width = cache.width
                        
            if i < len_s - 1:
                next_c = s[i + 1]
                next_index = FT_Get_Char_Index(face, next_c)
                
                error = FT_Get_Kerning(face, index, next_index, FT_KERNING_DEFAULT, &kerning)
                if error:
                    raise FreetypeError(error)
                
                kern = FT_ROUND(kerning.x)                
                
                if cache.advance + kern > min_advance:
                    gl.advance = cache.advance + kern
                else:
                    gl.advance = min_advance
                    
                next_min_advance = cache.advance - gl.advance
                        
            else:
                gl.advance = cache.advance
        
            rv.append(gl)
        
        return rv
    
    def draw(self, pysurf, float xo, int yo, color, list glyphs):
        """
        Draws a list of glyphs to surf, with the baseline starting at x, y.
        """
                
        cdef SDL_Surface *surf
        cdef unsigned int Sr, Sb, Sg, Sa
        cdef unsigned int Dr, Db, Dg, Da
        cdef unsigned int rshift, gshift, bshift, ashift
        cdef unsigned int fixed
        cdef unsigned int alpha
        cdef Glyph glyph
        
        cdef FT_Face face
        cdef FT_GlyphSlot g
        cdef FT_UInt index
        cdef int error
        cdef int bmx, bmy, px, py
                
        cdef unsigned char *pixels
        cdef unsigned char *line
        cdef unsigned char *gline 
        cdef int pitch
        cdef glyph_cache *cache
                
                
        Sr, Sg, Sb, Sa = color

        if Sa == 0:
            return
        
        self.setup()
        
        surf = PySurface_AsSurface(pysurf)
        pixels = <unsigned char *> surf.pixels
        pitch = surf.pitch

        face = self.face
        g = face.glyph
                
        for glyph in glyphs:

            if glyph.split == SPLIT_INSTEAD:
                continue
                        
            x = glyph.x + xo
            y = glyph.y + yo
            
            index = FT_Get_Char_Index(face, <Py_UNICODE> glyph.character)

            cache = self.get_glyph(index)
            
                
            bmx = <int> (x + .5) + cache.bitmap_left
            bmy = y - cache.bitmap_top

            for py from 0 <= py < cache.bitmap.rows:                    

                line = pixels + bmy * pitch + bmx * 4
                gline = cache.bitmap.buffer + py * cache.bitmap.pitch
                
                for px from 0 <= px < cache.bitmap.width:
                    
                    alpha = gline[0]
                    
                    # Modulate Sa by the glyph's alpha.
                    alpha = (alpha * Sa + Sa) >> 8

                    # This code is the ALPHA_BLEND macro, from the surface.h
                    # file in pygame-1.8          
                    Da = line[3]
                                           
                    if Da:
                        Dr = line[0]
                        Dg = line[1]
                        Db = line[2]
                        
                        line[0] = (((Sr - Dr) * alpha) >> 8) + Dr
                        line[1] = (((Sg - Dg) * alpha) >> 8) + Dg
                        line[2] = (((Sb - Db) * alpha) >> 8) + Db
                        line[3] = alpha + Da - ((alpha * Da) / 255)
                        
                    else:
                        line[0] = Sr
                        line[1] = Sg
                        line[2] = Sb
                        line[3] = alpha
                    
                    gline += 1
                    line += 4
                    
                bmy += 1
