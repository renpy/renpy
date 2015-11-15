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

cdef int glClientActiveTextureARB(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glClientActiveTextureARB')
    cdef GLenum error
    realGlClientActiveTextureARB(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glClientActiveTextureARB' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glClipPlane(GLenum a0, GLdouble * a1) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glClipPlane')
    cdef GLenum error
    realGlClipPlane(a0, a1)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glClipPlane' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glColor4f(GLfloat a0, GLfloat a1, GLfloat a2, GLfloat a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glColor4f')
    cdef GLenum error
    realGlColor4f(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glColor4f' % error
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

cdef int glDisableClientState(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glDisableClientState')
    cdef GLenum error
    realGlDisableClientState(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glDisableClientState' % error
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

cdef int glEnableClientState(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glEnableClientState')
    cdef GLenum error
    realGlEnableClientState(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glEnableClientState' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glLoadIdentity() except? 0:
    if check_errors & 4:
        renpy.display.log.write('glLoadIdentity')
    cdef GLenum error
    realGlLoadIdentity()
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glLoadIdentity' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glMatrixMode(GLenum a0) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glMatrixMode')
    cdef GLenum error
    realGlMatrixMode(a0)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glMatrixMode' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glOrtho(GLdouble a0, GLdouble a1, GLdouble a2, GLdouble a3, GLdouble a4, GLdouble a5) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glOrtho')
    cdef GLenum error
    realGlOrtho(a0, a1, a2, a3, a4, a5)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glOrtho' % error
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

cdef int glTexCoordPointer(GLint a0, GLenum a1, GLsizei a2, GLubyte * a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexCoordPointer')
    cdef GLenum error
    realGlTexCoordPointer(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexCoordPointer' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glTexEnvf(GLenum a0, GLenum a1, GLfloat a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexEnvf')
    cdef GLenum error
    realGlTexEnvf(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexEnvf' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glTexEnvfv(GLenum a0, GLenum a1, GLfloat * a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexEnvfv')
    cdef GLenum error
    realGlTexEnvfv(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexEnvfv' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glTexEnvi(GLenum a0, GLenum a1, GLint a2) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glTexEnvi')
    cdef GLenum error
    realGlTexEnvi(a0, a1, a2)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glTexEnvi' % error
            if check_errors & 1:
                renpy.display.log.write('%s', message)
            if check_errors & 2:
                raise Exception(message)
    return 1

cdef int glVertexPointer(GLint a0, GLenum a1, GLsizei a2, GLubyte * a3) except? 0:
    if check_errors & 4:
        renpy.display.log.write('glVertexPointer')
    cdef GLenum error
    realGlVertexPointer(a0, a1, a2, a3)
    if check_errors:
        error = realGlGetError()
        if error:
            message = 'GL error %x in glVertexPointer' % error
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
