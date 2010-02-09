# This file contains bindings to integrate pygame (SDL) and OpenGL.

cdef extern from "pygame/pygame.h":
    struct SDL_Surface:
        int w
        int h
        int pitch
        void *pixels
 
    SDL_Surface *PySurface_AsSurface(object)

    
cdef extern from "GL/gl.h":
    ctypedef unsigned int    GLenum
    ctypedef unsigned char   GLboolean
    ctypedef unsigned int    GLbitfield
    ctypedef void            GLvoid
    ctypedef signed char     GLbyte
    ctypedef short           GLshort
    ctypedef int             GLint
    ctypedef unsigned char   GLubyte
    ctypedef unsigned short  GLushort
    ctypedef unsigned int    GLuint
    ctypedef int             GLsizei
    ctypedef float           GLfloat
    ctypedef float           GLclampf
    ctypedef double          GLdouble
    ctypedef double          GLclampd


    int GL_UNPACK_ROW_LENGTH
     
    void glPixelStorei(
        GLint pname,
        GLint param)

    int GL_TEXTURE_2D
    int GL_RGBA
    int GL_UNSIGNED_BYTE
          
    void glTexImage2D(
        GLenum target,
        GLint level,
        GLint internalformat, 
        GLsizei width,
        GLsizei height,
        GLint border,
        GLenum format,
        GLenum type,
        void *pixels)


    void glTexSubImage2D(
        int target,
        int level,
        int xoffset,
        int yoffset,
        int width,
        int height,
        int format,
        int type,
        void *pixels)
     
    
def load_texture(
    object pysurf,
    int width,
    int height,
    int xoffset,
    int yoffset,
    int replace):
    
    """
    This loads the supplied pygame surface into the numbered
    texture. The created texture will be of size (width, height),
    and at position (xoffset, yoffset) relative to the containing
    image. 
    """
    
    cdef SDL_Surface *surf = PySurface_AsSurface(pysurf)
    cdef unsigned char *pixels = <unsigned char *> surf.pixels

    pixels += yoffset * surf.pitch
    pixels += xoffset * 4

    glPixelStorei(GL_UNPACK_ROW_LENGTH, surf.pitch / 4)

    if replace:

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            pixels)

    else:
        glTexSubImage2D(
            GL_TEXTURE_2D,
            0,
            0,
            0,
            width,
            height,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            pixels)

        
    
