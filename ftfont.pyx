from freetype cimport *
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
    
        object f
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

    def setup(self, size, bold, italic, outline):
        
        return
    


# Ideas for how text rendering will work:
#
# 1) Break things up into style/text pairs. Break into paragraphs
# at this point, process each paragraph separately.
# 2) Style objects lay out text into lists of glyph objects.
# 3) The glyph objects are combined into one list (per paragraph).
# 4) The paragraph lists are broken into lines, justified, and offset.
# 5) The style objects then draw the glyph objects.


