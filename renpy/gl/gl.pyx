
cdef int glActiveTextureARB(GLenum a0) except? 0:
    cdef GLenum error
    realGlActiveTextureARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glAttachObjectARB(GLhandleARB a0, GLhandleARB a1) except? 0:
    cdef GLenum error
    realGlAttachObjectARB(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glBindFramebufferEXT(GLenum a0, GLuint a1) except? 0:
    cdef GLenum error
    realGlBindFramebufferEXT(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glBindTexture(GLenum a0, GLuint a1) except? 0:
    cdef GLenum error
    realGlBindTexture(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glBlendFunc(GLenum a0, GLenum a1) except? 0:
    cdef GLenum error
    realGlBlendFunc(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glClear(GLbitfield a0) except? 0:
    cdef GLenum error
    realGlClear(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glClearColor(GLclampf a0, GLclampf a1, GLclampf a2, GLclampf a3) except? 0:
    cdef GLenum error
    realGlClearColor(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glClientActiveTextureARB(GLenum a0) except? 0:
    cdef GLenum error
    realGlClientActiveTextureARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glClipPlane(GLenum a0, GLdouble * a1) except? 0:
    cdef GLenum error
    realGlClipPlane(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glColor4f(GLfloat a0, GLfloat a1, GLfloat a2, GLfloat a3) except? 0:
    cdef GLenum error
    realGlColor4f(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glCompileShaderARB(GLhandleARB a0) except? 0:
    cdef GLenum error
    realGlCompileShaderARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glCopyTexSubImage2D(GLenum a0, GLint a1, GLint a2, GLint a3, GLint a4, GLint a5, GLsizei a6, GLsizei a7) except? 0:
    cdef GLenum error
    realGlCopyTexSubImage2D(a0, a1, a2, a3, a4, a5, a6, a7)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef GLhandleARB glCreateProgramObjectARB() except? 0:
    cdef GLenum error
    cdef GLhandleARB rv = realGlCreateProgramObjectARB()
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return rv

cdef GLhandleARB glCreateShaderObjectARB(GLenum a0) except? 0:
    cdef GLenum error
    cdef GLhandleARB rv = realGlCreateShaderObjectARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return rv

cdef int glDeleteFramebuffersEXT(GLsizei a0, GLuint * a1) except? 0:
    cdef GLenum error
    realGlDeleteFramebuffersEXT(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDeleteProgram(GLuint a0) except? 0:
    cdef GLenum error
    realGlDeleteProgram(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDeleteShader(GLuint a0) except? 0:
    cdef GLenum error
    realGlDeleteShader(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDeleteTextures(GLsizei a0, GLuint * a1) except? 0:
    cdef GLenum error
    realGlDeleteTextures(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDisable(GLenum a0) except? 0:
    cdef GLenum error
    realGlDisable(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDisableClientState(GLenum a0) except? 0:
    cdef GLenum error
    realGlDisableClientState(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDisableVertexAttribArrayARB(GLuint a0) except? 0:
    cdef GLenum error
    realGlDisableVertexAttribArrayARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glDrawArrays(GLenum a0, GLint a1, GLsizei a2) except? 0:
    cdef GLenum error
    realGlDrawArrays(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glEnable(GLenum a0) except? 0:
    cdef GLenum error
    realGlEnable(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glEnableClientState(GLenum a0) except? 0:
    cdef GLenum error
    realGlEnableClientState(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glEnableVertexAttribArrayARB(GLuint a0) except? 0:
    cdef GLenum error
    realGlEnableVertexAttribArrayARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glFinish() except? 0:
    cdef GLenum error
    realGlFinish()
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glFramebufferTexture2DEXT(GLenum a0, GLenum a1, GLenum a2, GLuint a3, GLint a4) except? 0:
    cdef GLenum error
    realGlFramebufferTexture2DEXT(a0, a1, a2, a3, a4)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glGenFramebuffersEXT(GLsizei a0, GLuint * a1) except? 0:
    cdef GLenum error
    realGlGenFramebuffersEXT(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glGenTextures(GLsizei a0, GLuint * a1) except? 0:
    cdef GLenum error
    realGlGenTextures(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef GLint glGetAttribLocationARB(GLhandleARB a0, GLchar * a1) except? 0:
    cdef GLenum error
    cdef GLint rv = realGlGetAttribLocationARB(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return rv

cdef int glGetIntegerv(GLenum a0, GLint * a1) except? 0:
    cdef GLenum error
    realGlGetIntegerv(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glGetProgramInfoLog(GLhandleARB a0, GLsizei a1, GLsizei * a2, GLchar * a3) except? 0:
    cdef GLenum error
    realGlGetProgramInfoLog(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glGetProgramiv(GLuint a0, GLenum a1, GLint * a2) except? 0:
    cdef GLenum error
    realGlGetProgramiv(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glGetShaderInfoLog(GLhandleARB a0, GLsizei a1, GLsizei * a2, GLchar * a3) except? 0:
    cdef GLenum error
    realGlGetShaderInfoLog(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glGetShaderiv(GLuint a0, GLenum a1, GLint * a2) except? 0:
    cdef GLenum error
    realGlGetShaderiv(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef GLchar * glGetString(GLenum a0) except? NULL:
    cdef GLenum error
    cdef GLchar * rv = realGlGetString(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return rv

cdef GLint glGetUniformLocationARB(GLhandleARB a0, GLchar * a1) except? 0:
    cdef GLenum error
    cdef GLint rv = realGlGetUniformLocationARB(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return rv

cdef int glLinkProgramARB(GLhandleARB a0) except? 0:
    cdef GLenum error
    realGlLinkProgramARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glLoadIdentity() except? 0:
    cdef GLenum error
    realGlLoadIdentity()
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glMatrixMode(GLenum a0) except? 0:
    cdef GLenum error
    realGlMatrixMode(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glOrtho(GLdouble a0, GLdouble a1, GLdouble a2, GLdouble a3, GLdouble a4, GLdouble a5) except? 0:
    cdef GLenum error
    realGlOrtho(a0, a1, a2, a3, a4, a5)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glReadPixels(GLint a0, GLint a1, GLsizei a2, GLsizei a3, GLenum a4, GLenum a5, GLubyte * a6) except? 0:
    cdef GLenum error
    realGlReadPixels(a0, a1, a2, a3, a4, a5, a6)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glScissor(GLint a0, GLint a1, GLsizei a2, GLsizei a3) except? 0:
    cdef GLenum error
    realGlScissor(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glShaderSourceARB(GLhandleARB a0, GLsizei a1, GLchar * * a2, GLint * a3) except? 0:
    cdef GLenum error
    realGlShaderSourceARB(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexCoordPointer(GLint a0, GLenum a1, GLsizei a2, GLubyte * a3) except? 0:
    cdef GLenum error
    realGlTexCoordPointer(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexEnvf(GLenum a0, GLenum a1, GLfloat a2) except? 0:
    cdef GLenum error
    realGlTexEnvf(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexEnvfv(GLenum a0, GLenum a1, GLfloat * a2) except? 0:
    cdef GLenum error
    realGlTexEnvfv(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexEnvi(GLenum a0, GLenum a1, GLint a2) except? 0:
    cdef GLenum error
    realGlTexEnvi(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexImage2D(GLenum a0, GLint a1, GLint a2, GLsizei a3, GLsizei a4, GLint a5, GLenum a6, GLenum a7, GLubyte * a8) except? 0:
    cdef GLenum error
    realGlTexImage2D(a0, a1, a2, a3, a4, a5, a6, a7, a8)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexParameteri(GLenum a0, GLenum a1, GLint a2) except? 0:
    cdef GLenum error
    realGlTexParameteri(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glTexSubImage2D(GLenum a0, GLint a1, GLint a2, GLint a3, GLsizei a4, GLsizei a5, GLenum a6, GLenum a7, GLubyte * a8) except? 0:
    cdef GLenum error
    realGlTexSubImage2D(a0, a1, a2, a3, a4, a5, a6, a7, a8)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glUniform1fARB(GLint a0, GLfloat a1) except? 0:
    cdef GLenum error
    realGlUniform1fARB(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glUniform1iARB(GLint a0, GLint a1) except? 0:
    cdef GLenum error
    realGlUniform1iARB(a0, a1)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glUniform2fARB(GLint a0, GLfloat a1, GLfloat a2) except? 0:
    cdef GLenum error
    realGlUniform2fARB(a0, a1, a2)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glUniform4fARB(GLint a0, GLfloat a1, GLfloat a2, GLfloat a3, GLfloat a4) except? 0:
    cdef GLenum error
    realGlUniform4fARB(a0, a1, a2, a3, a4)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glUniformMatrix4fvARB(GLint a0, GLsizei a1, GLboolean a2, GLfloat * a3) except? 0:
    cdef GLenum error
    realGlUniformMatrix4fvARB(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glUseProgramObjectARB(GLhandleARB a0) except? 0:
    cdef GLenum error
    realGlUseProgramObjectARB(a0)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glVertexAttribPointerARB(GLuint a0, GLint a1, GLenum a2, GLboolean a3, GLsizei a4, GLubyte * a5) except? 0:
    cdef GLenum error
    realGlVertexAttribPointerARB(a0, a1, a2, a3, a4, a5)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glVertexPointer(GLint a0, GLenum a1, GLsizei a2, GLubyte * a3) except? 0:
    cdef GLenum error
    realGlVertexPointer(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1

cdef int glViewport(GLint a0, GLint a1, GLsizei a2, GLsizei a3) except? 0:
    cdef GLenum error
    realGlViewport(a0, a1, a2, a3)
    if 1:
        error = realGlGetError()
        if error:
            raise Exception('GL error %x' % error)
    return 1
