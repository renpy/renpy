from renpy.uguu.gl cimport GLenum
from renpy.uguu.gl cimport GLboolean
from renpy.uguu.gl cimport GLbitfield
from renpy.uguu.gl cimport GLvoid
from renpy.uguu.gl cimport GLbyte
from renpy.uguu.gl cimport GLshort
from renpy.uguu.gl cimport GLint
from renpy.uguu.gl cimport GLclampx
from renpy.uguu.gl cimport GLubyte
from renpy.uguu.gl cimport GLushort
from renpy.uguu.gl cimport GLuint
from renpy.uguu.gl cimport GLsizei
from renpy.uguu.gl cimport GLfloat
from renpy.uguu.gl cimport GLclampf
from renpy.uguu.gl cimport GLdouble
from renpy.uguu.gl cimport GLclampd
from renpy.uguu.gl cimport GLeglClientBufferEXT
from renpy.uguu.gl cimport GLeglImageOES
from renpy.uguu.gl cimport GLchar
from renpy.uguu.gl cimport GLcharARB
from renpy.uguu.gl cimport GLhalfARB
from renpy.uguu.gl cimport GLhalf
from renpy.uguu.gl cimport GLfixed
from renpy.uguu.gl cimport GLintptr
from renpy.uguu.gl cimport GLsizeiptr
from renpy.uguu.gl cimport GLint64
from renpy.uguu.gl cimport GLuint64
from renpy.uguu.gl cimport GLintptrARB
from renpy.uguu.gl cimport GLsizeiptrARB
from renpy.uguu.gl cimport GLint64EXT
from renpy.uguu.gl cimport GLuint64EXT

from libc.stddef cimport ptrdiff_t
from libc.stdint cimport int64_t, uint64_t
from libc.stdio cimport printf
from libc.stdlib cimport calloc, free

from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_CONTIG, PyBUF_CONTIG_RO

cimport renpy.uguu.gl
import renpy.uguu.gl


cdef object proxy_return_string(const GLubyte *s):
    """
    This is used for string return values. It returns the return value as
    a python string if it's not NULL, or None if it's null.
    """

    if s == NULL:
        return None

    cdef const char *ss = <const char *> s
    return ss


cdef class ptr:
    """
    This is a class that wraps a generic contiguous Python buffer, and
    allows the retrieval of a pointer to that buffer.
    """

    cdef void *ptr
    cdef Py_buffer view

    def __init__(self, o, ro=True):
        if o is None:
            self.ptr = NULL
            return

        PyObject_GetBuffer(o, &self.view, PyBUF_CONTIG_RO if ro else PyBUF_CONTIG)
        self.ptr = self.view.buf

    def __dealloc__(self):
        if self.ptr:
            PyBuffer_Release(&self.view)
            self.ptr = NULL

cdef ptr get_ptr(o):
    """
    If o is a ptr, return it. Otherwise, convert the buffer into a ptr, and
    return that.
    """

    if isinstance(o, ptr):
        return o
    else:
        return ptr(o)

cdef class Buffer:
    """
    The base class for all buffers.
    """

    cdef Py_ssize_t length
    cdef Py_ssize_t itemsize
    cdef const char *format
    cdef void *data
    cdef int readonly

    cdef setup_buffer(self, Py_ssize_t length, Py_ssize_t itemsize, const char *format, int readonly):
        """
        This is called by a specific buffer's init method to set up various fields, and especially
        allocate the data field.

        `length`
            The number of items in this buffer.
        `itemsize`
            The size of a single item.
        `format`
            The struct-style format code.
        `readonly`
            1 if readonly, 0 if read-write.
        """

        self.length = length
        self.itemsize = itemsize
        self.format = format
        self.readonly = readonly
        self.data = calloc(self.length, self.itemsize)

    def __getbuffer__(self, Py_buffer *buffer, int flags):

        buffer.buf = self.data
        buffer.format = self.format
        buffer.internal = NULL
        buffer.itemsize = self.itemsize
        buffer.len = self.length * self.itemsize
        buffer.ndim = 1
        buffer.obj = self
        buffer.readonly = self.readonly
        buffer.shape = &self.length
        buffer.strides = &self.itemsize
        buffer.suboffsets = NULL

    def __releasebuffer__(self, Py_buffer *buffer):
        pass

    def __dealloc__(self):
        if self.data:
            free(self.data)
            self.data = NULL

cdef class BytesBuffer(Buffer):

    def __init__(self, length):

        self.setup_buffer(length, 1, "B", 0)

    def get(self):
        return bytes(<char *> self.data)

cdef class BytesListBuffer(Buffer):
    cdef object value

    def __init__(self, value):
        self.value = [ ptr(v) for v in value ]
        self.setup_buffer(len(value), sizeof(const char *), "P", 1)

        cdef int i

        for 0 <= i < self.length:
            (<const char **> self.data)[i] = <const char *> (<ptr> self.value[i]).ptr

cdef class IntBuffer(Buffer):

    def __init__(self, value):

        self.setup_buffer(len(value), sizeof(int), "i", 0)

        cdef int i

        for 0 <= i < self.length:
            (<int*> self.data)[i] = <int> value[i]

    def __getitem__(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("index out of range")

        return (<int*> self.data)[index]

cdef class FloatBuffer(Buffer):

    def __init__(self, value):

        self.setup_buffer(len(value), sizeof(float), "f", 0)

        cdef int i

        for 0 <= i < self.length:
            (<float *> self.data)[i] = <float> value[i]

    def __getitem__(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("index out of range")

        return (<float *> self.data)[index]


from renpy.uguu.gl cimport GLenum
from renpy.uguu.gl cimport GLboolean
from renpy.uguu.gl cimport GLbitfield
from renpy.uguu.gl cimport GLvoid
from renpy.uguu.gl cimport GLbyte
from renpy.uguu.gl cimport GLshort
from renpy.uguu.gl cimport GLint
from renpy.uguu.gl cimport GLclampx
from renpy.uguu.gl cimport GLubyte
from renpy.uguu.gl cimport GLushort
from renpy.uguu.gl cimport GLuint
from renpy.uguu.gl cimport GLsizei
from renpy.uguu.gl cimport GLfloat
from renpy.uguu.gl cimport GLclampf
from renpy.uguu.gl cimport GLdouble
from renpy.uguu.gl cimport GLclampd
from renpy.uguu.gl cimport GLeglClientBufferEXT
from renpy.uguu.gl cimport GLeglImageOES
from renpy.uguu.gl cimport GLchar
from renpy.uguu.gl cimport GLcharARB
from renpy.uguu.gl cimport GLhalfARB
from renpy.uguu.gl cimport GLhalf
from renpy.uguu.gl cimport GLfixed
from renpy.uguu.gl cimport GLintptr
from renpy.uguu.gl cimport GLsizeiptr
from renpy.uguu.gl cimport GLint64
from renpy.uguu.gl cimport GLuint64
from renpy.uguu.gl cimport GLintptrARB
from renpy.uguu.gl cimport GLsizeiptrARB
from renpy.uguu.gl cimport GLint64EXT
from renpy.uguu.gl cimport GLuint64EXT

def glActiveTexture(texture):
    renpy.uguu.gl.glActiveTexture(texture)

def glAttachShader(program, shader):
    renpy.uguu.gl.glAttachShader(program, shader)

def glBindAttribLocation(program, index, name):
    cdef ptr name_ptr = get_ptr(name)
    renpy.uguu.gl.glBindAttribLocation(program, index, <const GLchar *> name_ptr.ptr)

def glBindBuffer(target, buffer):
    renpy.uguu.gl.glBindBuffer(target, buffer)

def glBindFramebuffer(target, framebuffer):
    renpy.uguu.gl.glBindFramebuffer(target, framebuffer)

def glBindRenderbuffer(target, renderbuffer):
    renpy.uguu.gl.glBindRenderbuffer(target, renderbuffer)

def glBindTexture(target, texture):
    renpy.uguu.gl.glBindTexture(target, texture)

def glBlendColor(red, green, blue, alpha):
    renpy.uguu.gl.glBlendColor(red, green, blue, alpha)

def glBlendEquation(mode):
    renpy.uguu.gl.glBlendEquation(mode)

def glBlendEquationSeparate(modeRGB, modeAlpha):
    renpy.uguu.gl.glBlendEquationSeparate(modeRGB, modeAlpha)

def glBlendFunc(sfactor, dfactor):
    renpy.uguu.gl.glBlendFunc(sfactor, dfactor)

def glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha):
    renpy.uguu.gl.glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha)

def glBufferData(target, size, data, usage):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glBufferData(target, size, <const void *> data_ptr.ptr, usage)

def glBufferSubData(target, offset, size, data):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glBufferSubData(target, offset, size, <const void *> data_ptr.ptr)

def glCheckFramebufferStatus(target):
    return renpy.uguu.gl.glCheckFramebufferStatus(target)

def glClear(mask):
    renpy.uguu.gl.glClear(mask)

def glClearColor(red, green, blue, alpha):
    renpy.uguu.gl.glClearColor(red, green, blue, alpha)

def glClearStencil(s):
    renpy.uguu.gl.glClearStencil(s)

def glColorMask(red, green, blue, alpha):
    renpy.uguu.gl.glColorMask(red, green, blue, alpha)

def glCompileShader(shader):
    renpy.uguu.gl.glCompileShader(shader)

def glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, data):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, <const void *> data_ptr.ptr)

def glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, data):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, <const void *> data_ptr.ptr)

def glCopyTexImage2D(target, level, internalformat, x, y, width, height, border):
    renpy.uguu.gl.glCopyTexImage2D(target, level, internalformat, x, y, width, height, border)

def glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height):
    renpy.uguu.gl.glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height)

def glCreateProgram():
    return renpy.uguu.gl.glCreateProgram()

def glCreateShader(type):
    return renpy.uguu.gl.glCreateShader(type)

def glCullFace(mode):
    renpy.uguu.gl.glCullFace(mode)

def glDeleteBuffers(n, buffers):
    cdef ptr buffers_ptr = get_ptr(buffers)
    renpy.uguu.gl.glDeleteBuffers(n, <const GLuint *> buffers_ptr.ptr)

def glDeleteFramebuffers(n, framebuffers):
    cdef ptr framebuffers_ptr = get_ptr(framebuffers)
    renpy.uguu.gl.glDeleteFramebuffers(n, <const GLuint *> framebuffers_ptr.ptr)

def glDeleteProgram(program):
    renpy.uguu.gl.glDeleteProgram(program)

def glDeleteRenderbuffers(n, renderbuffers):
    cdef ptr renderbuffers_ptr = get_ptr(renderbuffers)
    renpy.uguu.gl.glDeleteRenderbuffers(n, <const GLuint *> renderbuffers_ptr.ptr)

def glDeleteShader(shader):
    renpy.uguu.gl.glDeleteShader(shader)

def glDeleteTextures(n, textures):
    cdef ptr textures_ptr = get_ptr(textures)
    renpy.uguu.gl.glDeleteTextures(n, <const GLuint *> textures_ptr.ptr)

def glDepthFunc(func):
    renpy.uguu.gl.glDepthFunc(func)

def glDepthMask(flag):
    renpy.uguu.gl.glDepthMask(flag)

def glDetachShader(program, shader):
    renpy.uguu.gl.glDetachShader(program, shader)

def glDisable(cap):
    renpy.uguu.gl.glDisable(cap)

def glDisableVertexAttribArray(index):
    renpy.uguu.gl.glDisableVertexAttribArray(index)

def glDrawArrays(mode, first, count):
    renpy.uguu.gl.glDrawArrays(mode, first, count)

def glDrawElements(mode, count, type, indices):
    cdef ptr indices_ptr = get_ptr(indices)
    renpy.uguu.gl.glDrawElements(mode, count, type, <const void *> indices_ptr.ptr)

def glEnable(cap):
    renpy.uguu.gl.glEnable(cap)

def glEnableVertexAttribArray(index):
    renpy.uguu.gl.glEnableVertexAttribArray(index)

def glFinish():
    renpy.uguu.gl.glFinish()

def glFlush():
    renpy.uguu.gl.glFlush()

def glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer):
    renpy.uguu.gl.glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer)

def glFramebufferTexture2D(target, attachment, textarget, texture, level):
    renpy.uguu.gl.glFramebufferTexture2D(target, attachment, textarget, texture, level)

def glFrontFace(mode):
    renpy.uguu.gl.glFrontFace(mode)

def glGenBuffers(n, buffers):
    cdef ptr buffers_ptr = get_ptr(buffers)
    renpy.uguu.gl.glGenBuffers(n, <GLuint *> buffers_ptr.ptr)

def glGenFramebuffers(n, framebuffers):
    cdef ptr framebuffers_ptr = get_ptr(framebuffers)
    renpy.uguu.gl.glGenFramebuffers(n, <GLuint *> framebuffers_ptr.ptr)

def glGenRenderbuffers(n, renderbuffers):
    cdef ptr renderbuffers_ptr = get_ptr(renderbuffers)
    renpy.uguu.gl.glGenRenderbuffers(n, <GLuint *> renderbuffers_ptr.ptr)

def glGenTextures(n, textures):
    cdef ptr textures_ptr = get_ptr(textures)
    renpy.uguu.gl.glGenTextures(n, <GLuint *> textures_ptr.ptr)

def glGenerateMipmap(target):
    renpy.uguu.gl.glGenerateMipmap(target)

def glGetActiveAttrib(program, index, bufSize, length, size, type, name):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr size_ptr = get_ptr(size)
    cdef ptr type_ptr = get_ptr(type)
    cdef ptr name_ptr = get_ptr(name)
    renpy.uguu.gl.glGetActiveAttrib(program, index, bufSize, <GLsizei *> length_ptr.ptr, <GLint *> size_ptr.ptr, <GLenum *> type_ptr.ptr, <GLchar *> name_ptr.ptr)

def glGetActiveUniform(program, index, bufSize, length, size, type, name):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr size_ptr = get_ptr(size)
    cdef ptr type_ptr = get_ptr(type)
    cdef ptr name_ptr = get_ptr(name)
    renpy.uguu.gl.glGetActiveUniform(program, index, bufSize, <GLsizei *> length_ptr.ptr, <GLint *> size_ptr.ptr, <GLenum *> type_ptr.ptr, <GLchar *> name_ptr.ptr)

def glGetAttachedShaders(program, maxCount, count, shaders):
    cdef ptr count_ptr = get_ptr(count)
    cdef ptr shaders_ptr = get_ptr(shaders)
    renpy.uguu.gl.glGetAttachedShaders(program, maxCount, <GLsizei *> count_ptr.ptr, <GLuint *> shaders_ptr.ptr)

def glGetAttribLocation(program, name):
    cdef ptr name_ptr = get_ptr(name)
    return renpy.uguu.gl.glGetAttribLocation(program, <const GLchar *> name_ptr.ptr)

def glGetBooleanv(pname, data):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glGetBooleanv(pname, <GLboolean *> data_ptr.ptr)

def glGetBufferParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetBufferParameteriv(target, pname, <GLint *> params_ptr.ptr)

def glGetError():
    return renpy.uguu.gl.glGetError()

def glGetFloatv(pname, data):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glGetFloatv(pname, <GLfloat *> data_ptr.ptr)

def glGetFramebufferAttachmentParameteriv(target, attachment, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetFramebufferAttachmentParameteriv(target, attachment, pname, <GLint *> params_ptr.ptr)

def glGetIntegerv(pname, data):
    cdef ptr data_ptr = get_ptr(data)
    renpy.uguu.gl.glGetIntegerv(pname, <GLint *> data_ptr.ptr)

def glGetProgramInfoLog(program, bufSize, length, infoLog):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr infoLog_ptr = get_ptr(infoLog)
    renpy.uguu.gl.glGetProgramInfoLog(program, bufSize, <GLsizei *> length_ptr.ptr, <GLchar *> infoLog_ptr.ptr)

def glGetProgramiv(program, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetProgramiv(program, pname, <GLint *> params_ptr.ptr)

def glGetRenderbufferParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetRenderbufferParameteriv(target, pname, <GLint *> params_ptr.ptr)

def glGetShaderInfoLog(shader, bufSize, length, infoLog):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr infoLog_ptr = get_ptr(infoLog)
    renpy.uguu.gl.glGetShaderInfoLog(shader, bufSize, <GLsizei *> length_ptr.ptr, <GLchar *> infoLog_ptr.ptr)

def glGetShaderSource(shader, bufSize, length, source):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr source_ptr = get_ptr(source)
    renpy.uguu.gl.glGetShaderSource(shader, bufSize, <GLsizei *> length_ptr.ptr, <GLchar *> source_ptr.ptr)

def glGetShaderiv(shader, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetShaderiv(shader, pname, <GLint *> params_ptr.ptr)

def glGetString(name):
    return proxy_return_string(renpy.uguu.gl.glGetString(name))

def glGetTexParameterfv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetTexParameterfv(target, pname, <GLfloat *> params_ptr.ptr)

def glGetTexParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetTexParameteriv(target, pname, <GLint *> params_ptr.ptr)

def glGetUniformLocation(program, name):
    cdef ptr name_ptr = get_ptr(name)
    return renpy.uguu.gl.glGetUniformLocation(program, <const GLchar *> name_ptr.ptr)

def glGetUniformfv(program, location, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetUniformfv(program, location, <GLfloat *> params_ptr.ptr)

def glGetUniformiv(program, location, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetUniformiv(program, location, <GLint *> params_ptr.ptr)

def glGetVertexAttribPointerv(index, pname, pointer):
    cdef ptr pointer_ptr = get_ptr(pointer)
    renpy.uguu.gl.glGetVertexAttribPointerv(index, pname, <void **> pointer_ptr.ptr)

def glGetVertexAttribfv(index, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetVertexAttribfv(index, pname, <GLfloat *> params_ptr.ptr)

def glGetVertexAttribiv(index, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glGetVertexAttribiv(index, pname, <GLint *> params_ptr.ptr)

def glHint(target, mode):
    renpy.uguu.gl.glHint(target, mode)

def glIsBuffer(buffer):
    return renpy.uguu.gl.glIsBuffer(buffer)

def glIsEnabled(cap):
    return renpy.uguu.gl.glIsEnabled(cap)

def glIsFramebuffer(framebuffer):
    return renpy.uguu.gl.glIsFramebuffer(framebuffer)

def glIsProgram(program):
    return renpy.uguu.gl.glIsProgram(program)

def glIsRenderbuffer(renderbuffer):
    return renpy.uguu.gl.glIsRenderbuffer(renderbuffer)

def glIsShader(shader):
    return renpy.uguu.gl.glIsShader(shader)

def glIsTexture(texture):
    return renpy.uguu.gl.glIsTexture(texture)

def glLineWidth(width):
    renpy.uguu.gl.glLineWidth(width)

def glLinkProgram(program):
    renpy.uguu.gl.glLinkProgram(program)

def glPixelStorei(pname, param):
    renpy.uguu.gl.glPixelStorei(pname, param)

def glPolygonOffset(factor, units):
    renpy.uguu.gl.glPolygonOffset(factor, units)

def glReadPixels(x, y, width, height, format, type, pixels):
    cdef ptr pixels_ptr = get_ptr(pixels)
    renpy.uguu.gl.glReadPixels(x, y, width, height, format, type, <void *> pixels_ptr.ptr)

def glRenderbufferStorage(target, internalformat, width, height):
    renpy.uguu.gl.glRenderbufferStorage(target, internalformat, width, height)

def glSampleCoverage(value, invert):
    renpy.uguu.gl.glSampleCoverage(value, invert)

def glScissor(x, y, width, height):
    renpy.uguu.gl.glScissor(x, y, width, height)

def glShaderSource(shader, count, string, length):
    cdef ptr string_ptr = get_ptr(string)
    cdef ptr length_ptr = get_ptr(length)
    renpy.uguu.gl.glShaderSource(shader, count, <const GLchar *const*> string_ptr.ptr, <const GLint *> length_ptr.ptr)

def glStencilFunc(func, ref, mask):
    renpy.uguu.gl.glStencilFunc(func, ref, mask)

def glStencilFuncSeparate(face, func, ref, mask):
    renpy.uguu.gl.glStencilFuncSeparate(face, func, ref, mask)

def glStencilMask(mask):
    renpy.uguu.gl.glStencilMask(mask)

def glStencilMaskSeparate(face, mask):
    renpy.uguu.gl.glStencilMaskSeparate(face, mask)

def glStencilOp(fail, zfail, zpass):
    renpy.uguu.gl.glStencilOp(fail, zfail, zpass)

def glStencilOpSeparate(face, sfail, dpfail, dppass):
    renpy.uguu.gl.glStencilOpSeparate(face, sfail, dpfail, dppass)

def glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels):
    cdef ptr pixels_ptr = get_ptr(pixels)
    renpy.uguu.gl.glTexImage2D(target, level, internalformat, width, height, border, format, type, <const void *> pixels_ptr.ptr)

def glTexParameterf(target, pname, param):
    renpy.uguu.gl.glTexParameterf(target, pname, param)

def glTexParameterfv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glTexParameterfv(target, pname, <const GLfloat *> params_ptr.ptr)

def glTexParameteri(target, pname, param):
    renpy.uguu.gl.glTexParameteri(target, pname, param)

def glTexParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    renpy.uguu.gl.glTexParameteriv(target, pname, <const GLint *> params_ptr.ptr)

def glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels):
    cdef ptr pixels_ptr = get_ptr(pixels)
    renpy.uguu.gl.glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, <const void *> pixels_ptr.ptr)

def glUniform1f(location, v0):
    renpy.uguu.gl.glUniform1f(location, v0)

def glUniform1fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform1fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform1i(location, v0):
    renpy.uguu.gl.glUniform1i(location, v0)

def glUniform1iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform1iv(location, count, <const GLint *> value_ptr.ptr)

def glUniform2f(location, v0, v1):
    renpy.uguu.gl.glUniform2f(location, v0, v1)

def glUniform2fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform2fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform2i(location, v0, v1):
    renpy.uguu.gl.glUniform2i(location, v0, v1)

def glUniform2iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform2iv(location, count, <const GLint *> value_ptr.ptr)

def glUniform3f(location, v0, v1, v2):
    renpy.uguu.gl.glUniform3f(location, v0, v1, v2)

def glUniform3fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform3fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform3i(location, v0, v1, v2):
    renpy.uguu.gl.glUniform3i(location, v0, v1, v2)

def glUniform3iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform3iv(location, count, <const GLint *> value_ptr.ptr)

def glUniform4f(location, v0, v1, v2, v3):
    renpy.uguu.gl.glUniform4f(location, v0, v1, v2, v3)

def glUniform4fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform4fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform4i(location, v0, v1, v2, v3):
    renpy.uguu.gl.glUniform4i(location, v0, v1, v2, v3)

def glUniform4iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniform4iv(location, count, <const GLint *> value_ptr.ptr)

def glUniformMatrix2fv(location, count, transpose, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniformMatrix2fv(location, count, transpose, <const GLfloat *> value_ptr.ptr)

def glUniformMatrix3fv(location, count, transpose, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniformMatrix3fv(location, count, transpose, <const GLfloat *> value_ptr.ptr)

def glUniformMatrix4fv(location, count, transpose, value):
    cdef ptr value_ptr = get_ptr(value)
    renpy.uguu.gl.glUniformMatrix4fv(location, count, transpose, <const GLfloat *> value_ptr.ptr)

def glUseProgram(program):
    renpy.uguu.gl.glUseProgram(program)

def glValidateProgram(program):
    renpy.uguu.gl.glValidateProgram(program)

def glVertexAttrib1f(index, x):
    renpy.uguu.gl.glVertexAttrib1f(index, x)

def glVertexAttrib1fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    renpy.uguu.gl.glVertexAttrib1fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttrib2f(index, x, y):
    renpy.uguu.gl.glVertexAttrib2f(index, x, y)

def glVertexAttrib2fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    renpy.uguu.gl.glVertexAttrib2fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttrib3f(index, x, y, z):
    renpy.uguu.gl.glVertexAttrib3f(index, x, y, z)

def glVertexAttrib3fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    renpy.uguu.gl.glVertexAttrib3fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttrib4f(index, x, y, z, w):
    renpy.uguu.gl.glVertexAttrib4f(index, x, y, z, w)

def glVertexAttrib4fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    renpy.uguu.gl.glVertexAttrib4fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttribPointer(index, size, type, normalized, stride, pointer):
    cdef ptr pointer_ptr = get_ptr(pointer)
    renpy.uguu.gl.glVertexAttribPointer(index, size, type, normalized, stride, <const void *> pointer_ptr.ptr)

def glViewport(x, y, width, height):
    renpy.uguu.gl.glViewport(x, y, width, height)

GL_FALSE = renpy.uguu.gl.GL_FALSE
GL_NONE = renpy.uguu.gl.GL_NONE
GL_NO_ERROR = renpy.uguu.gl.GL_NO_ERROR
GL_POINTS = renpy.uguu.gl.GL_POINTS
GL_ZERO = renpy.uguu.gl.GL_ZERO
GL_LINES = renpy.uguu.gl.GL_LINES
GL_ONE = renpy.uguu.gl.GL_ONE
GL_TRUE = renpy.uguu.gl.GL_TRUE
GL_LINE_LOOP = renpy.uguu.gl.GL_LINE_LOOP
GL_LINE_STRIP = renpy.uguu.gl.GL_LINE_STRIP
GL_TRIANGLES = renpy.uguu.gl.GL_TRIANGLES
GL_TRIANGLE_STRIP = renpy.uguu.gl.GL_TRIANGLE_STRIP
GL_TRIANGLE_FAN = renpy.uguu.gl.GL_TRIANGLE_FAN
GL_DEPTH_BUFFER_BIT = renpy.uguu.gl.GL_DEPTH_BUFFER_BIT
GL_NEVER = renpy.uguu.gl.GL_NEVER
GL_LESS = renpy.uguu.gl.GL_LESS
GL_EQUAL = renpy.uguu.gl.GL_EQUAL
GL_LEQUAL = renpy.uguu.gl.GL_LEQUAL
GL_GREATER = renpy.uguu.gl.GL_GREATER
GL_NOTEQUAL = renpy.uguu.gl.GL_NOTEQUAL
GL_GEQUAL = renpy.uguu.gl.GL_GEQUAL
GL_ALWAYS = renpy.uguu.gl.GL_ALWAYS
GL_SRC_COLOR = renpy.uguu.gl.GL_SRC_COLOR
GL_ONE_MINUS_SRC_COLOR = renpy.uguu.gl.GL_ONE_MINUS_SRC_COLOR
GL_SRC_ALPHA = renpy.uguu.gl.GL_SRC_ALPHA
GL_ONE_MINUS_SRC_ALPHA = renpy.uguu.gl.GL_ONE_MINUS_SRC_ALPHA
GL_DST_ALPHA = renpy.uguu.gl.GL_DST_ALPHA
GL_ONE_MINUS_DST_ALPHA = renpy.uguu.gl.GL_ONE_MINUS_DST_ALPHA
GL_DST_COLOR = renpy.uguu.gl.GL_DST_COLOR
GL_ONE_MINUS_DST_COLOR = renpy.uguu.gl.GL_ONE_MINUS_DST_COLOR
GL_SRC_ALPHA_SATURATE = renpy.uguu.gl.GL_SRC_ALPHA_SATURATE
GL_STENCIL_BUFFER_BIT = renpy.uguu.gl.GL_STENCIL_BUFFER_BIT
GL_FRONT = renpy.uguu.gl.GL_FRONT
GL_BACK = renpy.uguu.gl.GL_BACK
GL_FRONT_AND_BACK = renpy.uguu.gl.GL_FRONT_AND_BACK
GL_INVALID_ENUM = renpy.uguu.gl.GL_INVALID_ENUM
GL_INVALID_VALUE = renpy.uguu.gl.GL_INVALID_VALUE
GL_INVALID_OPERATION = renpy.uguu.gl.GL_INVALID_OPERATION
GL_OUT_OF_MEMORY = renpy.uguu.gl.GL_OUT_OF_MEMORY
GL_INVALID_FRAMEBUFFER_OPERATION = renpy.uguu.gl.GL_INVALID_FRAMEBUFFER_OPERATION
GL_CW = renpy.uguu.gl.GL_CW
GL_CCW = renpy.uguu.gl.GL_CCW
GL_LINE_WIDTH = renpy.uguu.gl.GL_LINE_WIDTH
GL_CULL_FACE = renpy.uguu.gl.GL_CULL_FACE
GL_CULL_FACE_MODE = renpy.uguu.gl.GL_CULL_FACE_MODE
GL_FRONT_FACE = renpy.uguu.gl.GL_FRONT_FACE
GL_DEPTH_RANGE = renpy.uguu.gl.GL_DEPTH_RANGE
GL_DEPTH_TEST = renpy.uguu.gl.GL_DEPTH_TEST
GL_DEPTH_WRITEMASK = renpy.uguu.gl.GL_DEPTH_WRITEMASK
GL_DEPTH_CLEAR_VALUE = renpy.uguu.gl.GL_DEPTH_CLEAR_VALUE
GL_DEPTH_FUNC = renpy.uguu.gl.GL_DEPTH_FUNC
GL_STENCIL_TEST = renpy.uguu.gl.GL_STENCIL_TEST
GL_STENCIL_CLEAR_VALUE = renpy.uguu.gl.GL_STENCIL_CLEAR_VALUE
GL_STENCIL_FUNC = renpy.uguu.gl.GL_STENCIL_FUNC
GL_STENCIL_VALUE_MASK = renpy.uguu.gl.GL_STENCIL_VALUE_MASK
GL_STENCIL_FAIL = renpy.uguu.gl.GL_STENCIL_FAIL
GL_STENCIL_PASS_DEPTH_FAIL = renpy.uguu.gl.GL_STENCIL_PASS_DEPTH_FAIL
GL_STENCIL_PASS_DEPTH_PASS = renpy.uguu.gl.GL_STENCIL_PASS_DEPTH_PASS
GL_STENCIL_REF = renpy.uguu.gl.GL_STENCIL_REF
GL_STENCIL_WRITEMASK = renpy.uguu.gl.GL_STENCIL_WRITEMASK
GL_VIEWPORT = renpy.uguu.gl.GL_VIEWPORT
GL_DITHER = renpy.uguu.gl.GL_DITHER
GL_BLEND = renpy.uguu.gl.GL_BLEND
GL_SCISSOR_BOX = renpy.uguu.gl.GL_SCISSOR_BOX
GL_SCISSOR_TEST = renpy.uguu.gl.GL_SCISSOR_TEST
GL_COLOR_CLEAR_VALUE = renpy.uguu.gl.GL_COLOR_CLEAR_VALUE
GL_COLOR_WRITEMASK = renpy.uguu.gl.GL_COLOR_WRITEMASK
GL_UNPACK_ALIGNMENT = renpy.uguu.gl.GL_UNPACK_ALIGNMENT
GL_PACK_ALIGNMENT = renpy.uguu.gl.GL_PACK_ALIGNMENT
GL_MAX_TEXTURE_SIZE = renpy.uguu.gl.GL_MAX_TEXTURE_SIZE
GL_MAX_VIEWPORT_DIMS = renpy.uguu.gl.GL_MAX_VIEWPORT_DIMS
GL_SUBPIXEL_BITS = renpy.uguu.gl.GL_SUBPIXEL_BITS
GL_RED_BITS = renpy.uguu.gl.GL_RED_BITS
GL_GREEN_BITS = renpy.uguu.gl.GL_GREEN_BITS
GL_BLUE_BITS = renpy.uguu.gl.GL_BLUE_BITS
GL_ALPHA_BITS = renpy.uguu.gl.GL_ALPHA_BITS
GL_DEPTH_BITS = renpy.uguu.gl.GL_DEPTH_BITS
GL_STENCIL_BITS = renpy.uguu.gl.GL_STENCIL_BITS
GL_TEXTURE_2D = renpy.uguu.gl.GL_TEXTURE_2D
GL_DONT_CARE = renpy.uguu.gl.GL_DONT_CARE
GL_FASTEST = renpy.uguu.gl.GL_FASTEST
GL_NICEST = renpy.uguu.gl.GL_NICEST
GL_BYTE = renpy.uguu.gl.GL_BYTE
GL_UNSIGNED_BYTE = renpy.uguu.gl.GL_UNSIGNED_BYTE
GL_SHORT = renpy.uguu.gl.GL_SHORT
GL_UNSIGNED_SHORT = renpy.uguu.gl.GL_UNSIGNED_SHORT
GL_INT = renpy.uguu.gl.GL_INT
GL_UNSIGNED_INT = renpy.uguu.gl.GL_UNSIGNED_INT
GL_FLOAT = renpy.uguu.gl.GL_FLOAT
GL_INVERT = renpy.uguu.gl.GL_INVERT
GL_TEXTURE = renpy.uguu.gl.GL_TEXTURE
GL_DEPTH_COMPONENT = renpy.uguu.gl.GL_DEPTH_COMPONENT
GL_ALPHA = renpy.uguu.gl.GL_ALPHA
GL_RGB = renpy.uguu.gl.GL_RGB
GL_RGBA = renpy.uguu.gl.GL_RGBA
GL_LUMINANCE = renpy.uguu.gl.GL_LUMINANCE
GL_LUMINANCE_ALPHA = renpy.uguu.gl.GL_LUMINANCE_ALPHA
GL_KEEP = renpy.uguu.gl.GL_KEEP
GL_REPLACE = renpy.uguu.gl.GL_REPLACE
GL_INCR = renpy.uguu.gl.GL_INCR
GL_DECR = renpy.uguu.gl.GL_DECR
GL_VENDOR = renpy.uguu.gl.GL_VENDOR
GL_RENDERER = renpy.uguu.gl.GL_RENDERER
GL_VERSION = renpy.uguu.gl.GL_VERSION
GL_EXTENSIONS = renpy.uguu.gl.GL_EXTENSIONS
GL_NEAREST = renpy.uguu.gl.GL_NEAREST
GL_LINEAR = renpy.uguu.gl.GL_LINEAR
GL_NEAREST_MIPMAP_NEAREST = renpy.uguu.gl.GL_NEAREST_MIPMAP_NEAREST
GL_LINEAR_MIPMAP_NEAREST = renpy.uguu.gl.GL_LINEAR_MIPMAP_NEAREST
GL_NEAREST_MIPMAP_LINEAR = renpy.uguu.gl.GL_NEAREST_MIPMAP_LINEAR
GL_LINEAR_MIPMAP_LINEAR = renpy.uguu.gl.GL_LINEAR_MIPMAP_LINEAR
GL_TEXTURE_MAG_FILTER = renpy.uguu.gl.GL_TEXTURE_MAG_FILTER
GL_TEXTURE_MIN_FILTER = renpy.uguu.gl.GL_TEXTURE_MIN_FILTER
GL_TEXTURE_WRAP_S = renpy.uguu.gl.GL_TEXTURE_WRAP_S
GL_TEXTURE_WRAP_T = renpy.uguu.gl.GL_TEXTURE_WRAP_T
GL_REPEAT = renpy.uguu.gl.GL_REPEAT
GL_POLYGON_OFFSET_UNITS = renpy.uguu.gl.GL_POLYGON_OFFSET_UNITS
GL_COLOR_BUFFER_BIT = renpy.uguu.gl.GL_COLOR_BUFFER_BIT
GL_CONSTANT_COLOR = renpy.uguu.gl.GL_CONSTANT_COLOR
GL_ONE_MINUS_CONSTANT_COLOR = renpy.uguu.gl.GL_ONE_MINUS_CONSTANT_COLOR
GL_CONSTANT_ALPHA = renpy.uguu.gl.GL_CONSTANT_ALPHA
GL_ONE_MINUS_CONSTANT_ALPHA = renpy.uguu.gl.GL_ONE_MINUS_CONSTANT_ALPHA
GL_BLEND_COLOR = renpy.uguu.gl.GL_BLEND_COLOR
GL_FUNC_ADD = renpy.uguu.gl.GL_FUNC_ADD
GL_BLEND_EQUATION = renpy.uguu.gl.GL_BLEND_EQUATION
GL_BLEND_EQUATION_RGB = renpy.uguu.gl.GL_BLEND_EQUATION_RGB
GL_FUNC_SUBTRACT = renpy.uguu.gl.GL_FUNC_SUBTRACT
GL_FUNC_REVERSE_SUBTRACT = renpy.uguu.gl.GL_FUNC_REVERSE_SUBTRACT
GL_UNSIGNED_SHORT_4_4_4_4 = renpy.uguu.gl.GL_UNSIGNED_SHORT_4_4_4_4
GL_UNSIGNED_SHORT_5_5_5_1 = renpy.uguu.gl.GL_UNSIGNED_SHORT_5_5_5_1
GL_POLYGON_OFFSET_FILL = renpy.uguu.gl.GL_POLYGON_OFFSET_FILL
GL_POLYGON_OFFSET_FACTOR = renpy.uguu.gl.GL_POLYGON_OFFSET_FACTOR
GL_RGBA4 = renpy.uguu.gl.GL_RGBA4
GL_RGB5_A1 = renpy.uguu.gl.GL_RGB5_A1
GL_TEXTURE_BINDING_2D = renpy.uguu.gl.GL_TEXTURE_BINDING_2D
GL_SAMPLE_ALPHA_TO_COVERAGE = renpy.uguu.gl.GL_SAMPLE_ALPHA_TO_COVERAGE
GL_SAMPLE_COVERAGE = renpy.uguu.gl.GL_SAMPLE_COVERAGE
GL_SAMPLE_BUFFERS = renpy.uguu.gl.GL_SAMPLE_BUFFERS
GL_SAMPLES = renpy.uguu.gl.GL_SAMPLES
GL_SAMPLE_COVERAGE_VALUE = renpy.uguu.gl.GL_SAMPLE_COVERAGE_VALUE
GL_SAMPLE_COVERAGE_INVERT = renpy.uguu.gl.GL_SAMPLE_COVERAGE_INVERT
GL_BLEND_DST_RGB = renpy.uguu.gl.GL_BLEND_DST_RGB
GL_BLEND_SRC_RGB = renpy.uguu.gl.GL_BLEND_SRC_RGB
GL_BLEND_DST_ALPHA = renpy.uguu.gl.GL_BLEND_DST_ALPHA
GL_BLEND_SRC_ALPHA = renpy.uguu.gl.GL_BLEND_SRC_ALPHA
GL_CLAMP_TO_EDGE = renpy.uguu.gl.GL_CLAMP_TO_EDGE
GL_GENERATE_MIPMAP_HINT = renpy.uguu.gl.GL_GENERATE_MIPMAP_HINT
GL_DEPTH_COMPONENT16 = renpy.uguu.gl.GL_DEPTH_COMPONENT16
GL_UNSIGNED_SHORT_5_6_5 = renpy.uguu.gl.GL_UNSIGNED_SHORT_5_6_5
GL_MIRRORED_REPEAT = renpy.uguu.gl.GL_MIRRORED_REPEAT
GL_ALIASED_POINT_SIZE_RANGE = renpy.uguu.gl.GL_ALIASED_POINT_SIZE_RANGE
GL_ALIASED_LINE_WIDTH_RANGE = renpy.uguu.gl.GL_ALIASED_LINE_WIDTH_RANGE
GL_TEXTURE0 = renpy.uguu.gl.GL_TEXTURE0
GL_TEXTURE1 = renpy.uguu.gl.GL_TEXTURE1
GL_TEXTURE2 = renpy.uguu.gl.GL_TEXTURE2
GL_TEXTURE3 = renpy.uguu.gl.GL_TEXTURE3
GL_TEXTURE4 = renpy.uguu.gl.GL_TEXTURE4
GL_TEXTURE5 = renpy.uguu.gl.GL_TEXTURE5
GL_TEXTURE6 = renpy.uguu.gl.GL_TEXTURE6
GL_TEXTURE7 = renpy.uguu.gl.GL_TEXTURE7
GL_TEXTURE8 = renpy.uguu.gl.GL_TEXTURE8
GL_TEXTURE9 = renpy.uguu.gl.GL_TEXTURE9
GL_TEXTURE10 = renpy.uguu.gl.GL_TEXTURE10
GL_TEXTURE11 = renpy.uguu.gl.GL_TEXTURE11
GL_TEXTURE12 = renpy.uguu.gl.GL_TEXTURE12
GL_TEXTURE13 = renpy.uguu.gl.GL_TEXTURE13
GL_TEXTURE14 = renpy.uguu.gl.GL_TEXTURE14
GL_TEXTURE15 = renpy.uguu.gl.GL_TEXTURE15
GL_TEXTURE16 = renpy.uguu.gl.GL_TEXTURE16
GL_TEXTURE17 = renpy.uguu.gl.GL_TEXTURE17
GL_TEXTURE18 = renpy.uguu.gl.GL_TEXTURE18
GL_TEXTURE19 = renpy.uguu.gl.GL_TEXTURE19
GL_TEXTURE20 = renpy.uguu.gl.GL_TEXTURE20
GL_TEXTURE21 = renpy.uguu.gl.GL_TEXTURE21
GL_TEXTURE22 = renpy.uguu.gl.GL_TEXTURE22
GL_TEXTURE23 = renpy.uguu.gl.GL_TEXTURE23
GL_TEXTURE24 = renpy.uguu.gl.GL_TEXTURE24
GL_TEXTURE25 = renpy.uguu.gl.GL_TEXTURE25
GL_TEXTURE26 = renpy.uguu.gl.GL_TEXTURE26
GL_TEXTURE27 = renpy.uguu.gl.GL_TEXTURE27
GL_TEXTURE28 = renpy.uguu.gl.GL_TEXTURE28
GL_TEXTURE29 = renpy.uguu.gl.GL_TEXTURE29
GL_TEXTURE30 = renpy.uguu.gl.GL_TEXTURE30
GL_TEXTURE31 = renpy.uguu.gl.GL_TEXTURE31
GL_ACTIVE_TEXTURE = renpy.uguu.gl.GL_ACTIVE_TEXTURE
GL_MAX_RENDERBUFFER_SIZE = renpy.uguu.gl.GL_MAX_RENDERBUFFER_SIZE
GL_INCR_WRAP = renpy.uguu.gl.GL_INCR_WRAP
GL_DECR_WRAP = renpy.uguu.gl.GL_DECR_WRAP
GL_TEXTURE_CUBE_MAP = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP
GL_TEXTURE_BINDING_CUBE_MAP = renpy.uguu.gl.GL_TEXTURE_BINDING_CUBE_MAP
GL_TEXTURE_CUBE_MAP_POSITIVE_X = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X
GL_TEXTURE_CUBE_MAP_NEGATIVE_X = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_X
GL_TEXTURE_CUBE_MAP_POSITIVE_Y = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Y
GL_TEXTURE_CUBE_MAP_NEGATIVE_Y = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
GL_TEXTURE_CUBE_MAP_POSITIVE_Z = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Z
GL_TEXTURE_CUBE_MAP_NEGATIVE_Z = renpy.uguu.gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
GL_MAX_CUBE_MAP_TEXTURE_SIZE = renpy.uguu.gl.GL_MAX_CUBE_MAP_TEXTURE_SIZE
GL_VERTEX_ATTRIB_ARRAY_ENABLED = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_ENABLED
GL_VERTEX_ATTRIB_ARRAY_SIZE = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_SIZE
GL_VERTEX_ATTRIB_ARRAY_STRIDE = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_STRIDE
GL_VERTEX_ATTRIB_ARRAY_TYPE = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_TYPE
GL_CURRENT_VERTEX_ATTRIB = renpy.uguu.gl.GL_CURRENT_VERTEX_ATTRIB
GL_VERTEX_ATTRIB_ARRAY_POINTER = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_POINTER
GL_NUM_COMPRESSED_TEXTURE_FORMATS = renpy.uguu.gl.GL_NUM_COMPRESSED_TEXTURE_FORMATS
GL_COMPRESSED_TEXTURE_FORMATS = renpy.uguu.gl.GL_COMPRESSED_TEXTURE_FORMATS
GL_BUFFER_SIZE = renpy.uguu.gl.GL_BUFFER_SIZE
GL_BUFFER_USAGE = renpy.uguu.gl.GL_BUFFER_USAGE
GL_STENCIL_BACK_FUNC = renpy.uguu.gl.GL_STENCIL_BACK_FUNC
GL_STENCIL_BACK_FAIL = renpy.uguu.gl.GL_STENCIL_BACK_FAIL
GL_STENCIL_BACK_PASS_DEPTH_FAIL = renpy.uguu.gl.GL_STENCIL_BACK_PASS_DEPTH_FAIL
GL_STENCIL_BACK_PASS_DEPTH_PASS = renpy.uguu.gl.GL_STENCIL_BACK_PASS_DEPTH_PASS
GL_BLEND_EQUATION_ALPHA = renpy.uguu.gl.GL_BLEND_EQUATION_ALPHA
GL_MAX_VERTEX_ATTRIBS = renpy.uguu.gl.GL_MAX_VERTEX_ATTRIBS
GL_VERTEX_ATTRIB_ARRAY_NORMALIZED = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_NORMALIZED
GL_MAX_TEXTURE_IMAGE_UNITS = renpy.uguu.gl.GL_MAX_TEXTURE_IMAGE_UNITS
GL_ARRAY_BUFFER = renpy.uguu.gl.GL_ARRAY_BUFFER
GL_ELEMENT_ARRAY_BUFFER = renpy.uguu.gl.GL_ELEMENT_ARRAY_BUFFER
GL_ARRAY_BUFFER_BINDING = renpy.uguu.gl.GL_ARRAY_BUFFER_BINDING
GL_ELEMENT_ARRAY_BUFFER_BINDING = renpy.uguu.gl.GL_ELEMENT_ARRAY_BUFFER_BINDING
GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING = renpy.uguu.gl.GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING
GL_STREAM_DRAW = renpy.uguu.gl.GL_STREAM_DRAW
GL_STATIC_DRAW = renpy.uguu.gl.GL_STATIC_DRAW
GL_DYNAMIC_DRAW = renpy.uguu.gl.GL_DYNAMIC_DRAW
GL_FRAGMENT_SHADER = renpy.uguu.gl.GL_FRAGMENT_SHADER
GL_VERTEX_SHADER = renpy.uguu.gl.GL_VERTEX_SHADER
GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS = renpy.uguu.gl.GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS
GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS = renpy.uguu.gl.GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS
GL_SHADER_TYPE = renpy.uguu.gl.GL_SHADER_TYPE
GL_FLOAT_VEC2 = renpy.uguu.gl.GL_FLOAT_VEC2
GL_FLOAT_VEC3 = renpy.uguu.gl.GL_FLOAT_VEC3
GL_FLOAT_VEC4 = renpy.uguu.gl.GL_FLOAT_VEC4
GL_INT_VEC2 = renpy.uguu.gl.GL_INT_VEC2
GL_INT_VEC3 = renpy.uguu.gl.GL_INT_VEC3
GL_INT_VEC4 = renpy.uguu.gl.GL_INT_VEC4
GL_BOOL = renpy.uguu.gl.GL_BOOL
GL_BOOL_VEC2 = renpy.uguu.gl.GL_BOOL_VEC2
GL_BOOL_VEC3 = renpy.uguu.gl.GL_BOOL_VEC3
GL_BOOL_VEC4 = renpy.uguu.gl.GL_BOOL_VEC4
GL_FLOAT_MAT2 = renpy.uguu.gl.GL_FLOAT_MAT2
GL_FLOAT_MAT3 = renpy.uguu.gl.GL_FLOAT_MAT3
GL_FLOAT_MAT4 = renpy.uguu.gl.GL_FLOAT_MAT4
GL_SAMPLER_2D = renpy.uguu.gl.GL_SAMPLER_2D
GL_SAMPLER_CUBE = renpy.uguu.gl.GL_SAMPLER_CUBE
GL_DELETE_STATUS = renpy.uguu.gl.GL_DELETE_STATUS
GL_COMPILE_STATUS = renpy.uguu.gl.GL_COMPILE_STATUS
GL_LINK_STATUS = renpy.uguu.gl.GL_LINK_STATUS
GL_VALIDATE_STATUS = renpy.uguu.gl.GL_VALIDATE_STATUS
GL_INFO_LOG_LENGTH = renpy.uguu.gl.GL_INFO_LOG_LENGTH
GL_ATTACHED_SHADERS = renpy.uguu.gl.GL_ATTACHED_SHADERS
GL_ACTIVE_UNIFORMS = renpy.uguu.gl.GL_ACTIVE_UNIFORMS
GL_ACTIVE_UNIFORM_MAX_LENGTH = renpy.uguu.gl.GL_ACTIVE_UNIFORM_MAX_LENGTH
GL_SHADER_SOURCE_LENGTH = renpy.uguu.gl.GL_SHADER_SOURCE_LENGTH
GL_ACTIVE_ATTRIBUTES = renpy.uguu.gl.GL_ACTIVE_ATTRIBUTES
GL_ACTIVE_ATTRIBUTE_MAX_LENGTH = renpy.uguu.gl.GL_ACTIVE_ATTRIBUTE_MAX_LENGTH
GL_SHADING_LANGUAGE_VERSION = renpy.uguu.gl.GL_SHADING_LANGUAGE_VERSION
GL_CURRENT_PROGRAM = renpy.uguu.gl.GL_CURRENT_PROGRAM
GL_STENCIL_BACK_REF = renpy.uguu.gl.GL_STENCIL_BACK_REF
GL_STENCIL_BACK_VALUE_MASK = renpy.uguu.gl.GL_STENCIL_BACK_VALUE_MASK
GL_STENCIL_BACK_WRITEMASK = renpy.uguu.gl.GL_STENCIL_BACK_WRITEMASK
GL_FRAMEBUFFER_BINDING = renpy.uguu.gl.GL_FRAMEBUFFER_BINDING
GL_RENDERBUFFER_BINDING = renpy.uguu.gl.GL_RENDERBUFFER_BINDING
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE = renpy.uguu.gl.GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME = renpy.uguu.gl.GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL = renpy.uguu.gl.GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE = renpy.uguu.gl.GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE
GL_FRAMEBUFFER_COMPLETE = renpy.uguu.gl.GL_FRAMEBUFFER_COMPLETE
GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT = renpy.uguu.gl.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT
GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT = renpy.uguu.gl.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT
GL_FRAMEBUFFER_UNSUPPORTED = renpy.uguu.gl.GL_FRAMEBUFFER_UNSUPPORTED
GL_COLOR_ATTACHMENT0 = renpy.uguu.gl.GL_COLOR_ATTACHMENT0
GL_DEPTH_ATTACHMENT = renpy.uguu.gl.GL_DEPTH_ATTACHMENT
GL_STENCIL_ATTACHMENT = renpy.uguu.gl.GL_STENCIL_ATTACHMENT
GL_FRAMEBUFFER = renpy.uguu.gl.GL_FRAMEBUFFER
GL_RENDERBUFFER = renpy.uguu.gl.GL_RENDERBUFFER
GL_RENDERBUFFER_WIDTH = renpy.uguu.gl.GL_RENDERBUFFER_WIDTH
GL_RENDERBUFFER_HEIGHT = renpy.uguu.gl.GL_RENDERBUFFER_HEIGHT
GL_RENDERBUFFER_INTERNAL_FORMAT = renpy.uguu.gl.GL_RENDERBUFFER_INTERNAL_FORMAT
GL_STENCIL_INDEX8 = renpy.uguu.gl.GL_STENCIL_INDEX8
GL_RENDERBUFFER_RED_SIZE = renpy.uguu.gl.GL_RENDERBUFFER_RED_SIZE
GL_RENDERBUFFER_GREEN_SIZE = renpy.uguu.gl.GL_RENDERBUFFER_GREEN_SIZE
GL_RENDERBUFFER_BLUE_SIZE = renpy.uguu.gl.GL_RENDERBUFFER_BLUE_SIZE
GL_RENDERBUFFER_ALPHA_SIZE = renpy.uguu.gl.GL_RENDERBUFFER_ALPHA_SIZE
GL_RENDERBUFFER_DEPTH_SIZE = renpy.uguu.gl.GL_RENDERBUFFER_DEPTH_SIZE
GL_RENDERBUFFER_STENCIL_SIZE = renpy.uguu.gl.GL_RENDERBUFFER_STENCIL_SIZE
