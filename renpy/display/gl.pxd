


cdef extern from "GL/glew.h":
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

    # Support for clip planes.
    GLvoid glClipPlane(GLenum plane, GLdouble *equation)

    enum:
       GL_CLIP_PLANE0
       GL_CLIP_PLANE1
       GL_CLIP_PLANE2
       GL_CLIP_PLANE3
        
    GLenum GLEW_OK
    GLenum glewInit()    
    GLubyte *glewGetErrorString(GLenum)

    int GL_UNPACK_ROW_LENGTH
    int GL_PACK_ROW_LENGTH
     
    void glPixelStorei(
        GLint pname,
        GLint param)

    int GL_TEXTURE_2D
    int GL_RGBA8
    int GL_RGBA
    int GL_BGRA
    int GL_ALPHA
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

    GLenum GL_TEXTURE0_ARB
    GLenum GL_TEXTURE1_ARB
    GLenum GL_TEXTURE2_ARB

    GLenum GL_TRIANGLE_STRIP
    
    void glMultiTexCoord2fARB(GLenum, GLfloat, GLfloat)
    void glVertex2f(GLfloat, GLfloat)
    void glBegin(GLenum)
    void glEnd()
    void glActiveTextureARB(GLenum)
    void glBindTexture(GLenum, GLuint texture)

    GLubyte  *glGetString(GLenum)

    void glReadPixels(
        GLint,
        GLint,
        GLsizei,
        GLsizei,
        GLenum,
        GLenum,
        void *)
