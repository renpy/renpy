import os
import renpy

cdef int check_errors
check_errors = int(os.environ.get("RENPY_GL_CHECK_ERRORS", 0))


cdef int glActiveTextureARB(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glActiveTextureARB')
    cdef GLenum error
    realGlActiveTextureARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glActiveTextureARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glAttachObjectARB(GLhandleARB a0, GLhandleARB a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glAttachObjectARB')
    cdef GLenum error
    realGlAttachObjectARB(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glAttachObjectARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glBindFramebufferEXT(GLenum a0, GLuint a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glBindFramebufferEXT')
    cdef GLenum error
    realGlBindFramebufferEXT(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glBindFramebufferEXT' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glBindTexture(GLenum a0, GLuint a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glBindTexture')
    cdef GLenum error
    realGlBindTexture(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glBindTexture' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glBlendFunc(GLenum a0, GLenum a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glBlendFunc')
    cdef GLenum error
    realGlBlendFunc(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glBlendFunc' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glClear(GLbitfield a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glClear')
    cdef GLenum error
    realGlClear(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glClear' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glClearColor(GLclampf a0, GLclampf a1, GLclampf a2, GLclampf a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glClearColor')
    cdef GLenum error
    realGlClearColor(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glClearColor' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glCompileShaderARB(GLhandleARB a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glCompileShaderARB')
    cdef GLenum error
    realGlCompileShaderARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glCompileShaderARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glCopyTexSubImage2D(GLenum a0, GLint a1, GLint a2, GLint a3, GLint a4, GLint a5, GLsizei a6, GLsizei a7) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glCopyTexSubImage2D')
    cdef GLenum error
    realGlCopyTexSubImage2D(a0, a1, a2, a3, a4, a5, a6, a7)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glCopyTexSubImage2D' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef GLhandleARB glCreateProgramObjectARB() except? 0:
    if check_errors & 4:
        renpy.display.log.write('glCreateProgramObjectARB')
    cdef GLenum error
    cdef GLhandleARB rv = realGlCreateProgramObjectARB()
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glCreateProgramObjectARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return rv

cdef GLhandleARB glCreateShaderObjectARB(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glCreateShaderObjectARB')
    cdef GLenum error
    cdef GLhandleARB rv = realGlCreateShaderObjectARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glCreateShaderObjectARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return rv

cdef int glDeleteFramebuffersEXT(GLsizei a0, GLuint * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDeleteFramebuffersEXT')
    cdef GLenum error
    realGlDeleteFramebuffersEXT(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDeleteFramebuffersEXT' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glDeleteProgram(GLuint a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDeleteProgram')
    cdef GLenum error
    realGlDeleteProgram(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDeleteProgram' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glDeleteShader(GLuint a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDeleteShader')
    cdef GLenum error
    realGlDeleteShader(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDeleteShader' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glDeleteTextures(GLsizei a0, GLuint * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDeleteTextures')
    cdef GLenum error
    realGlDeleteTextures(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDeleteTextures' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glDisable(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDisable')
    cdef GLenum error
    realGlDisable(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDisable' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glDisableVertexAttribArrayARB(GLuint a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDisableVertexAttribArrayARB')
    cdef GLenum error
    realGlDisableVertexAttribArrayARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDisableVertexAttribArrayARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glDrawArrays(GLenum a0, GLint a1, GLsizei a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDrawArrays')
    cdef GLenum error
    realGlDrawArrays(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDrawArrays' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glEnable(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glEnable')
    cdef GLenum error
    realGlEnable(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glEnable' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glEnableVertexAttribArrayARB(GLuint a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glEnableVertexAttribArrayARB')
    cdef GLenum error
    realGlEnableVertexAttribArrayARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glEnableVertexAttribArrayARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glFinish() except? 0:
    if check_errors & 4:
        renpy.display.log.write('glFinish')
    cdef GLenum error
    realGlFinish()
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glFinish' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glFramebufferTexture2DEXT(GLenum a0, GLenum a1, GLenum a2, GLuint a3, GLint a4) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glFramebufferTexture2DEXT')
    cdef GLenum error
    realGlFramebufferTexture2DEXT(a0, a1, a2, a3, a4)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glFramebufferTexture2DEXT' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glGenFramebuffersEXT(GLsizei a0, GLuint * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGenFramebuffersEXT')
    cdef GLenum error
    realGlGenFramebuffersEXT(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGenFramebuffersEXT' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glGenTextures(GLsizei a0, GLuint * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGenTextures')
    cdef GLenum error
    realGlGenTextures(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGenTextures' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef GLint glGetAttribLocationARB(GLhandleARB a0, GLchar * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetAttribLocationARB')
    cdef GLenum error
    cdef GLint rv = realGlGetAttribLocationARB(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetAttribLocationARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return rv

cdef int glGetIntegerv(GLenum a0, GLint * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetIntegerv')
    cdef GLenum error
    realGlGetIntegerv(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetIntegerv' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glGetProgramInfoLog(GLhandleARB a0, GLsizei a1, GLsizei * a2, GLchar * a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetProgramInfoLog')
    cdef GLenum error
    realGlGetProgramInfoLog(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetProgramInfoLog' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glGetProgramiv(GLuint a0, GLenum a1, GLint * a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetProgramiv')
    cdef GLenum error
    realGlGetProgramiv(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetProgramiv' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glGetShaderInfoLog(GLhandleARB a0, GLsizei a1, GLsizei * a2, GLchar * a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetShaderInfoLog')
    cdef GLenum error
    realGlGetShaderInfoLog(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetShaderInfoLog' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glGetShaderiv(GLuint a0, GLenum a1, GLint * a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetShaderiv')
    cdef GLenum error
    realGlGetShaderiv(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetShaderiv' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef GLchar * glGetString(GLenum a0) except? NULL:
    if check_errors & 4:
        renpy.display.log.write('glGetString')
    cdef GLenum error
    cdef GLchar * rv = realGlGetString(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetString' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return rv

cdef GLint glGetUniformLocationARB(GLhandleARB a0, GLchar * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glGetUniformLocationARB')
    cdef GLenum error
    cdef GLint rv = realGlGetUniformLocationARB(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glGetUniformLocationARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return rv

cdef int glLinkProgramARB(GLhandleARB a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glLinkProgramARB')
    cdef GLenum error
    realGlLinkProgramARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glLinkProgramARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glReadPixels(GLint a0, GLint a1, GLsizei a2, GLsizei a3, GLenum a4, GLenum a5, GLubyte * a6) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glReadPixels')
    cdef GLenum error
    realGlReadPixels(a0, a1, a2, a3, a4, a5, a6)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glReadPixels' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glScissor(GLint a0, GLint a1, GLsizei a2, GLsizei a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glScissor')
    cdef GLenum error
    realGlScissor(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glScissor' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glShaderSourceARB(GLhandleARB a0, GLsizei a1, GLchar * * a2, GLint * a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glShaderSourceARB')
    cdef GLenum error
    realGlShaderSourceARB(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glShaderSourceARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glTexImage2D(GLenum a0, GLint a1, GLint a2, GLsizei a3, GLsizei a4, GLint a5, GLenum a6, GLenum a7, GLubyte * a8) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexImage2D')
    cdef GLenum error
    realGlTexImage2D(a0, a1, a2, a3, a4, a5, a6, a7, a8)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexImage2D' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glTexParameteri(GLenum a0, GLenum a1, GLint a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexParameteri')
    cdef GLenum error
    realGlTexParameteri(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexParameteri' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glTexSubImage2D(GLenum a0, GLint a1, GLint a2, GLint a3, GLsizei a4, GLsizei a5, GLenum a6, GLenum a7, GLubyte * a8) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexSubImage2D')
    cdef GLenum error
    realGlTexSubImage2D(a0, a1, a2, a3, a4, a5, a6, a7, a8)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexSubImage2D' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glUniform1fARB(GLint a0, GLfloat a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glUniform1fARB')
    cdef GLenum error
    realGlUniform1fARB(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glUniform1fARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glUniform1iARB(GLint a0, GLint a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glUniform1iARB')
    cdef GLenum error
    realGlUniform1iARB(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glUniform1iARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glUniform2fARB(GLint a0, GLfloat a1, GLfloat a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glUniform2fARB')
    cdef GLenum error
    realGlUniform2fARB(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glUniform2fARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glUniform4fARB(GLint a0, GLfloat a1, GLfloat a2, GLfloat a3, GLfloat a4) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glUniform4fARB')
    cdef GLenum error
    realGlUniform4fARB(a0, a1, a2, a3, a4)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glUniform4fARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glUniformMatrix4fvARB(GLint a0, GLsizei a1, GLboolean a2, GLfloat * a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glUniformMatrix4fvARB')
    cdef GLenum error
    realGlUniformMatrix4fvARB(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glUniformMatrix4fvARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glUseProgramObjectARB(GLhandleARB a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glUseProgramObjectARB')
    cdef GLenum error
    realGlUseProgramObjectARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glUseProgramObjectARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glVertexAttribPointerARB(GLuint a0, GLint a1, GLenum a2, GLboolean a3, GLsizei a4, GLubyte * a5) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glVertexAttribPointerARB')
    cdef GLenum error
    realGlVertexAttribPointerARB(a0, a1, a2, a3, a4, a5)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glVertexAttribPointerARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glViewport(GLint a0, GLint a1, GLsizei a2, GLsizei a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glViewport')
    cdef GLenum error
    realGlViewport(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glViewport' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1
