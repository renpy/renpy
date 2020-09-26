from uguugl cimport GLenum
from uguugl cimport GLboolean
from uguugl cimport GLbitfield
from uguugl cimport GLvoid
from uguugl cimport GLbyte
from uguugl cimport GLshort
from uguugl cimport GLint
from uguugl cimport GLclampx
from uguugl cimport GLubyte
from uguugl cimport GLushort
from uguugl cimport GLuint
from uguugl cimport GLsizei
from uguugl cimport GLfloat
from uguugl cimport GLclampf
from uguugl cimport GLdouble
from uguugl cimport GLclampd
from uguugl cimport GLeglClientBufferEXT
from uguugl cimport GLeglImageOES
from uguugl cimport GLchar
from uguugl cimport GLcharARB
from uguugl cimport GLhalfARB
from uguugl cimport GLhalf
from uguugl cimport GLfixed
from uguugl cimport GLintptr
from uguugl cimport GLsizeiptr
from uguugl cimport GLint64
from uguugl cimport GLuint64
from uguugl cimport GLintptrARB
from uguugl cimport GLsizeiptrARB
from uguugl cimport GLint64EXT
from uguugl cimport GLuint64EXT

from libc.stddef cimport ptrdiff_t
from libc.stdint cimport int64_t, uint64_t
from libc.stdio cimport printf
from libc.stdlib cimport calloc, free

from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_CONTIG, PyBUF_CONTIG_RO

cimport uguugl
from uguugl import load

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


from uguugl cimport GLenum
from uguugl cimport GLboolean
from uguugl cimport GLbitfield
from uguugl cimport GLvoid
from uguugl cimport GLbyte
from uguugl cimport GLshort
from uguugl cimport GLint
from uguugl cimport GLclampx
from uguugl cimport GLubyte
from uguugl cimport GLushort
from uguugl cimport GLuint
from uguugl cimport GLsizei
from uguugl cimport GLfloat
from uguugl cimport GLclampf
from uguugl cimport GLdouble
from uguugl cimport GLclampd
from uguugl cimport GLeglClientBufferEXT
from uguugl cimport GLeglImageOES
from uguugl cimport GLchar
from uguugl cimport GLcharARB
from uguugl cimport GLhalfARB
from uguugl cimport GLhalf
from uguugl cimport GLfixed
from uguugl cimport GLintptr
from uguugl cimport GLsizeiptr
from uguugl cimport GLint64
from uguugl cimport GLuint64
from uguugl cimport GLintptrARB
from uguugl cimport GLsizeiptrARB
from uguugl cimport GLint64EXT
from uguugl cimport GLuint64EXT

def glActiveTexture(texture):
    uguugl.glActiveTexture(texture)

def glAttachShader(program, shader):
    uguugl.glAttachShader(program, shader)

def glBindAttribLocation(program, index, name):
    cdef ptr name_ptr = get_ptr(name)
    uguugl.glBindAttribLocation(program, index, <const GLchar *> name_ptr.ptr)

def glBindBuffer(target, buffer):
    uguugl.glBindBuffer(target, buffer)

def glBindFramebuffer(target, framebuffer):
    uguugl.glBindFramebuffer(target, framebuffer)

def glBindRenderbuffer(target, renderbuffer):
    uguugl.glBindRenderbuffer(target, renderbuffer)

def glBindTexture(target, texture):
    uguugl.glBindTexture(target, texture)

def glBlendColor(red, green, blue, alpha):
    uguugl.glBlendColor(red, green, blue, alpha)

def glBlendEquation(mode):
    uguugl.glBlendEquation(mode)

def glBlendEquationSeparate(modeRGB, modeAlpha):
    uguugl.glBlendEquationSeparate(modeRGB, modeAlpha)

def glBlendFunc(sfactor, dfactor):
    uguugl.glBlendFunc(sfactor, dfactor)

def glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha):
    uguugl.glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha)

def glBufferData(target, size, data, usage):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glBufferData(target, size, <const void *> data_ptr.ptr, usage)

def glBufferSubData(target, offset, size, data):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glBufferSubData(target, offset, size, <const void *> data_ptr.ptr)

def glCheckFramebufferStatus(target):
    return uguugl.glCheckFramebufferStatus(target)

def glClear(mask):
    uguugl.glClear(mask)

def glClearColor(red, green, blue, alpha):
    uguugl.glClearColor(red, green, blue, alpha)

def glClearStencil(s):
    uguugl.glClearStencil(s)

def glColorMask(red, green, blue, alpha):
    uguugl.glColorMask(red, green, blue, alpha)

def glCompileShader(shader):
    uguugl.glCompileShader(shader)

def glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, data):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, <const void *> data_ptr.ptr)

def glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, data):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, <const void *> data_ptr.ptr)

def glCopyTexImage2D(target, level, internalformat, x, y, width, height, border):
    uguugl.glCopyTexImage2D(target, level, internalformat, x, y, width, height, border)

def glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height):
    uguugl.glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height)

def glCreateProgram():
    return uguugl.glCreateProgram()

def glCreateShader(type):
    return uguugl.glCreateShader(type)

def glCullFace(mode):
    uguugl.glCullFace(mode)

def glDeleteBuffers(n, buffers):
    cdef ptr buffers_ptr = get_ptr(buffers)
    uguugl.glDeleteBuffers(n, <const GLuint *> buffers_ptr.ptr)

def glDeleteFramebuffers(n, framebuffers):
    cdef ptr framebuffers_ptr = get_ptr(framebuffers)
    uguugl.glDeleteFramebuffers(n, <const GLuint *> framebuffers_ptr.ptr)

def glDeleteProgram(program):
    uguugl.glDeleteProgram(program)

def glDeleteRenderbuffers(n, renderbuffers):
    cdef ptr renderbuffers_ptr = get_ptr(renderbuffers)
    uguugl.glDeleteRenderbuffers(n, <const GLuint *> renderbuffers_ptr.ptr)

def glDeleteShader(shader):
    uguugl.glDeleteShader(shader)

def glDeleteTextures(n, textures):
    cdef ptr textures_ptr = get_ptr(textures)
    uguugl.glDeleteTextures(n, <const GLuint *> textures_ptr.ptr)

def glDepthFunc(func):
    uguugl.glDepthFunc(func)

def glDepthMask(flag):
    uguugl.glDepthMask(flag)

def glDetachShader(program, shader):
    uguugl.glDetachShader(program, shader)

def glDisable(cap):
    uguugl.glDisable(cap)

def glDisableVertexAttribArray(index):
    uguugl.glDisableVertexAttribArray(index)

def glDrawArrays(mode, first, count):
    uguugl.glDrawArrays(mode, first, count)

def glDrawElements(mode, count, type, indices):
    cdef ptr indices_ptr = get_ptr(indices)
    uguugl.glDrawElements(mode, count, type, <const void *> indices_ptr.ptr)

def glEnable(cap):
    uguugl.glEnable(cap)

def glEnableVertexAttribArray(index):
    uguugl.glEnableVertexAttribArray(index)

def glFinish():
    uguugl.glFinish()

def glFlush():
    uguugl.glFlush()

def glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer):
    uguugl.glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer)

def glFramebufferTexture2D(target, attachment, textarget, texture, level):
    uguugl.glFramebufferTexture2D(target, attachment, textarget, texture, level)

def glFrontFace(mode):
    uguugl.glFrontFace(mode)

def glGenBuffers(n, buffers):
    cdef ptr buffers_ptr = get_ptr(buffers)
    uguugl.glGenBuffers(n, <GLuint *> buffers_ptr.ptr)

def glGenFramebuffers(n, framebuffers):
    cdef ptr framebuffers_ptr = get_ptr(framebuffers)
    uguugl.glGenFramebuffers(n, <GLuint *> framebuffers_ptr.ptr)

def glGenRenderbuffers(n, renderbuffers):
    cdef ptr renderbuffers_ptr = get_ptr(renderbuffers)
    uguugl.glGenRenderbuffers(n, <GLuint *> renderbuffers_ptr.ptr)

def glGenTextures(n, textures):
    cdef ptr textures_ptr = get_ptr(textures)
    uguugl.glGenTextures(n, <GLuint *> textures_ptr.ptr)

def glGenerateMipmap(target):
    uguugl.glGenerateMipmap(target)

def glGetActiveAttrib(program, index, bufSize, length, size, type, name):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr size_ptr = get_ptr(size)
    cdef ptr type_ptr = get_ptr(type)
    cdef ptr name_ptr = get_ptr(name)
    uguugl.glGetActiveAttrib(program, index, bufSize, <GLsizei *> length_ptr.ptr, <GLint *> size_ptr.ptr, <GLenum *> type_ptr.ptr, <GLchar *> name_ptr.ptr)

def glGetActiveUniform(program, index, bufSize, length, size, type, name):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr size_ptr = get_ptr(size)
    cdef ptr type_ptr = get_ptr(type)
    cdef ptr name_ptr = get_ptr(name)
    uguugl.glGetActiveUniform(program, index, bufSize, <GLsizei *> length_ptr.ptr, <GLint *> size_ptr.ptr, <GLenum *> type_ptr.ptr, <GLchar *> name_ptr.ptr)

def glGetAttachedShaders(program, maxCount, count, shaders):
    cdef ptr count_ptr = get_ptr(count)
    cdef ptr shaders_ptr = get_ptr(shaders)
    uguugl.glGetAttachedShaders(program, maxCount, <GLsizei *> count_ptr.ptr, <GLuint *> shaders_ptr.ptr)

def glGetAttribLocation(program, name):
    cdef ptr name_ptr = get_ptr(name)
    return uguugl.glGetAttribLocation(program, <const GLchar *> name_ptr.ptr)

def glGetBooleanv(pname, data):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glGetBooleanv(pname, <GLboolean *> data_ptr.ptr)

def glGetBufferParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetBufferParameteriv(target, pname, <GLint *> params_ptr.ptr)

def glGetError():
    return uguugl.glGetError()

def glGetFloatv(pname, data):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glGetFloatv(pname, <GLfloat *> data_ptr.ptr)

def glGetFramebufferAttachmentParameteriv(target, attachment, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetFramebufferAttachmentParameteriv(target, attachment, pname, <GLint *> params_ptr.ptr)

def glGetIntegerv(pname, data):
    cdef ptr data_ptr = get_ptr(data)
    uguugl.glGetIntegerv(pname, <GLint *> data_ptr.ptr)

def glGetProgramInfoLog(program, bufSize, length, infoLog):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr infoLog_ptr = get_ptr(infoLog)
    uguugl.glGetProgramInfoLog(program, bufSize, <GLsizei *> length_ptr.ptr, <GLchar *> infoLog_ptr.ptr)

def glGetProgramiv(program, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetProgramiv(program, pname, <GLint *> params_ptr.ptr)

def glGetRenderbufferParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetRenderbufferParameteriv(target, pname, <GLint *> params_ptr.ptr)

def glGetShaderInfoLog(shader, bufSize, length, infoLog):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr infoLog_ptr = get_ptr(infoLog)
    uguugl.glGetShaderInfoLog(shader, bufSize, <GLsizei *> length_ptr.ptr, <GLchar *> infoLog_ptr.ptr)

def glGetShaderSource(shader, bufSize, length, source):
    cdef ptr length_ptr = get_ptr(length)
    cdef ptr source_ptr = get_ptr(source)
    uguugl.glGetShaderSource(shader, bufSize, <GLsizei *> length_ptr.ptr, <GLchar *> source_ptr.ptr)

def glGetShaderiv(shader, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetShaderiv(shader, pname, <GLint *> params_ptr.ptr)

def glGetString(name):
    return proxy_return_string(uguugl.glGetString(name))

def glGetTexParameterfv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetTexParameterfv(target, pname, <GLfloat *> params_ptr.ptr)

def glGetTexParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetTexParameteriv(target, pname, <GLint *> params_ptr.ptr)

def glGetUniformLocation(program, name):
    cdef ptr name_ptr = get_ptr(name)
    return uguugl.glGetUniformLocation(program, <const GLchar *> name_ptr.ptr)

def glGetUniformfv(program, location, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetUniformfv(program, location, <GLfloat *> params_ptr.ptr)

def glGetUniformiv(program, location, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetUniformiv(program, location, <GLint *> params_ptr.ptr)

def glGetVertexAttribPointerv(index, pname, pointer):
    cdef ptr pointer_ptr = get_ptr(pointer)
    uguugl.glGetVertexAttribPointerv(index, pname, <void **> pointer_ptr.ptr)

def glGetVertexAttribfv(index, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetVertexAttribfv(index, pname, <GLfloat *> params_ptr.ptr)

def glGetVertexAttribiv(index, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glGetVertexAttribiv(index, pname, <GLint *> params_ptr.ptr)

def glHint(target, mode):
    uguugl.glHint(target, mode)

def glIsBuffer(buffer):
    return uguugl.glIsBuffer(buffer)

def glIsEnabled(cap):
    return uguugl.glIsEnabled(cap)

def glIsFramebuffer(framebuffer):
    return uguugl.glIsFramebuffer(framebuffer)

def glIsProgram(program):
    return uguugl.glIsProgram(program)

def glIsRenderbuffer(renderbuffer):
    return uguugl.glIsRenderbuffer(renderbuffer)

def glIsShader(shader):
    return uguugl.glIsShader(shader)

def glIsTexture(texture):
    return uguugl.glIsTexture(texture)

def glLineWidth(width):
    uguugl.glLineWidth(width)

def glLinkProgram(program):
    uguugl.glLinkProgram(program)

def glPixelStorei(pname, param):
    uguugl.glPixelStorei(pname, param)

def glPolygonOffset(factor, units):
    uguugl.glPolygonOffset(factor, units)

def glReadPixels(x, y, width, height, format, type, pixels):
    cdef ptr pixels_ptr = get_ptr(pixels)
    uguugl.glReadPixels(x, y, width, height, format, type, <void *> pixels_ptr.ptr)

def glRenderbufferStorage(target, internalformat, width, height):
    uguugl.glRenderbufferStorage(target, internalformat, width, height)

def glSampleCoverage(value, invert):
    uguugl.glSampleCoverage(value, invert)

def glScissor(x, y, width, height):
    uguugl.glScissor(x, y, width, height)

def glShaderSource(shader, count, string, length):
    cdef ptr string_ptr = get_ptr(string)
    cdef ptr length_ptr = get_ptr(length)
    uguugl.glShaderSource(shader, count, <const GLchar *const*> string_ptr.ptr, <const GLint *> length_ptr.ptr)

def glStencilFunc(func, ref, mask):
    uguugl.glStencilFunc(func, ref, mask)

def glStencilFuncSeparate(face, func, ref, mask):
    uguugl.glStencilFuncSeparate(face, func, ref, mask)

def glStencilMask(mask):
    uguugl.glStencilMask(mask)

def glStencilMaskSeparate(face, mask):
    uguugl.glStencilMaskSeparate(face, mask)

def glStencilOp(fail, zfail, zpass):
    uguugl.glStencilOp(fail, zfail, zpass)

def glStencilOpSeparate(face, sfail, dpfail, dppass):
    uguugl.glStencilOpSeparate(face, sfail, dpfail, dppass)

def glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels):
    cdef ptr pixels_ptr = get_ptr(pixels)
    uguugl.glTexImage2D(target, level, internalformat, width, height, border, format, type, <const void *> pixels_ptr.ptr)

def glTexParameterf(target, pname, param):
    uguugl.glTexParameterf(target, pname, param)

def glTexParameterfv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glTexParameterfv(target, pname, <const GLfloat *> params_ptr.ptr)

def glTexParameteri(target, pname, param):
    uguugl.glTexParameteri(target, pname, param)

def glTexParameteriv(target, pname, params):
    cdef ptr params_ptr = get_ptr(params)
    uguugl.glTexParameteriv(target, pname, <const GLint *> params_ptr.ptr)

def glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels):
    cdef ptr pixels_ptr = get_ptr(pixels)
    uguugl.glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, <const void *> pixels_ptr.ptr)

def glUniform1f(location, v0):
    uguugl.glUniform1f(location, v0)

def glUniform1fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform1fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform1i(location, v0):
    uguugl.glUniform1i(location, v0)

def glUniform1iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform1iv(location, count, <const GLint *> value_ptr.ptr)

def glUniform2f(location, v0, v1):
    uguugl.glUniform2f(location, v0, v1)

def glUniform2fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform2fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform2i(location, v0, v1):
    uguugl.glUniform2i(location, v0, v1)

def glUniform2iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform2iv(location, count, <const GLint *> value_ptr.ptr)

def glUniform3f(location, v0, v1, v2):
    uguugl.glUniform3f(location, v0, v1, v2)

def glUniform3fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform3fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform3i(location, v0, v1, v2):
    uguugl.glUniform3i(location, v0, v1, v2)

def glUniform3iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform3iv(location, count, <const GLint *> value_ptr.ptr)

def glUniform4f(location, v0, v1, v2, v3):
    uguugl.glUniform4f(location, v0, v1, v2, v3)

def glUniform4fv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform4fv(location, count, <const GLfloat *> value_ptr.ptr)

def glUniform4i(location, v0, v1, v2, v3):
    uguugl.glUniform4i(location, v0, v1, v2, v3)

def glUniform4iv(location, count, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniform4iv(location, count, <const GLint *> value_ptr.ptr)

def glUniformMatrix2fv(location, count, transpose, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniformMatrix2fv(location, count, transpose, <const GLfloat *> value_ptr.ptr)

def glUniformMatrix3fv(location, count, transpose, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniformMatrix3fv(location, count, transpose, <const GLfloat *> value_ptr.ptr)

def glUniformMatrix4fv(location, count, transpose, value):
    cdef ptr value_ptr = get_ptr(value)
    uguugl.glUniformMatrix4fv(location, count, transpose, <const GLfloat *> value_ptr.ptr)

def glUseProgram(program):
    uguugl.glUseProgram(program)

def glValidateProgram(program):
    uguugl.glValidateProgram(program)

def glVertexAttrib1f(index, x):
    uguugl.glVertexAttrib1f(index, x)

def glVertexAttrib1fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    uguugl.glVertexAttrib1fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttrib2f(index, x, y):
    uguugl.glVertexAttrib2f(index, x, y)

def glVertexAttrib2fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    uguugl.glVertexAttrib2fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttrib3f(index, x, y, z):
    uguugl.glVertexAttrib3f(index, x, y, z)

def glVertexAttrib3fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    uguugl.glVertexAttrib3fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttrib4f(index, x, y, z, w):
    uguugl.glVertexAttrib4f(index, x, y, z, w)

def glVertexAttrib4fv(index, v):
    cdef ptr v_ptr = get_ptr(v)
    uguugl.glVertexAttrib4fv(index, <const GLfloat *> v_ptr.ptr)

def glVertexAttribPointer(index, size, type, normalized, stride, pointer):
    cdef ptr pointer_ptr = get_ptr(pointer)
    uguugl.glVertexAttribPointer(index, size, type, normalized, stride, <const void *> pointer_ptr.ptr)

def glViewport(x, y, width, height):
    uguugl.glViewport(x, y, width, height)

GL_FALSE = uguugl.GL_FALSE
GL_NONE = uguugl.GL_NONE
GL_NO_ERROR = uguugl.GL_NO_ERROR
GL_POINTS = uguugl.GL_POINTS
GL_ZERO = uguugl.GL_ZERO
GL_LINES = uguugl.GL_LINES
GL_ONE = uguugl.GL_ONE
GL_TRUE = uguugl.GL_TRUE
GL_LINE_LOOP = uguugl.GL_LINE_LOOP
GL_LINE_STRIP = uguugl.GL_LINE_STRIP
GL_TRIANGLES = uguugl.GL_TRIANGLES
GL_TRIANGLE_STRIP = uguugl.GL_TRIANGLE_STRIP
GL_TRIANGLE_FAN = uguugl.GL_TRIANGLE_FAN
GL_DEPTH_BUFFER_BIT = uguugl.GL_DEPTH_BUFFER_BIT
GL_NEVER = uguugl.GL_NEVER
GL_LESS = uguugl.GL_LESS
GL_EQUAL = uguugl.GL_EQUAL
GL_LEQUAL = uguugl.GL_LEQUAL
GL_GREATER = uguugl.GL_GREATER
GL_NOTEQUAL = uguugl.GL_NOTEQUAL
GL_GEQUAL = uguugl.GL_GEQUAL
GL_ALWAYS = uguugl.GL_ALWAYS
GL_SRC_COLOR = uguugl.GL_SRC_COLOR
GL_ONE_MINUS_SRC_COLOR = uguugl.GL_ONE_MINUS_SRC_COLOR
GL_SRC_ALPHA = uguugl.GL_SRC_ALPHA
GL_ONE_MINUS_SRC_ALPHA = uguugl.GL_ONE_MINUS_SRC_ALPHA
GL_DST_ALPHA = uguugl.GL_DST_ALPHA
GL_ONE_MINUS_DST_ALPHA = uguugl.GL_ONE_MINUS_DST_ALPHA
GL_DST_COLOR = uguugl.GL_DST_COLOR
GL_ONE_MINUS_DST_COLOR = uguugl.GL_ONE_MINUS_DST_COLOR
GL_SRC_ALPHA_SATURATE = uguugl.GL_SRC_ALPHA_SATURATE
GL_STENCIL_BUFFER_BIT = uguugl.GL_STENCIL_BUFFER_BIT
GL_FRONT = uguugl.GL_FRONT
GL_BACK = uguugl.GL_BACK
GL_FRONT_AND_BACK = uguugl.GL_FRONT_AND_BACK
GL_INVALID_ENUM = uguugl.GL_INVALID_ENUM
GL_INVALID_VALUE = uguugl.GL_INVALID_VALUE
GL_INVALID_OPERATION = uguugl.GL_INVALID_OPERATION
GL_OUT_OF_MEMORY = uguugl.GL_OUT_OF_MEMORY
GL_INVALID_FRAMEBUFFER_OPERATION = uguugl.GL_INVALID_FRAMEBUFFER_OPERATION
GL_CW = uguugl.GL_CW
GL_CCW = uguugl.GL_CCW
GL_LINE_WIDTH = uguugl.GL_LINE_WIDTH
GL_CULL_FACE = uguugl.GL_CULL_FACE
GL_CULL_FACE_MODE = uguugl.GL_CULL_FACE_MODE
GL_FRONT_FACE = uguugl.GL_FRONT_FACE
GL_DEPTH_RANGE = uguugl.GL_DEPTH_RANGE
GL_DEPTH_TEST = uguugl.GL_DEPTH_TEST
GL_DEPTH_WRITEMASK = uguugl.GL_DEPTH_WRITEMASK
GL_DEPTH_CLEAR_VALUE = uguugl.GL_DEPTH_CLEAR_VALUE
GL_DEPTH_FUNC = uguugl.GL_DEPTH_FUNC
GL_STENCIL_TEST = uguugl.GL_STENCIL_TEST
GL_STENCIL_CLEAR_VALUE = uguugl.GL_STENCIL_CLEAR_VALUE
GL_STENCIL_FUNC = uguugl.GL_STENCIL_FUNC
GL_STENCIL_VALUE_MASK = uguugl.GL_STENCIL_VALUE_MASK
GL_STENCIL_FAIL = uguugl.GL_STENCIL_FAIL
GL_STENCIL_PASS_DEPTH_FAIL = uguugl.GL_STENCIL_PASS_DEPTH_FAIL
GL_STENCIL_PASS_DEPTH_PASS = uguugl.GL_STENCIL_PASS_DEPTH_PASS
GL_STENCIL_REF = uguugl.GL_STENCIL_REF
GL_STENCIL_WRITEMASK = uguugl.GL_STENCIL_WRITEMASK
GL_VIEWPORT = uguugl.GL_VIEWPORT
GL_DITHER = uguugl.GL_DITHER
GL_BLEND = uguugl.GL_BLEND
GL_SCISSOR_BOX = uguugl.GL_SCISSOR_BOX
GL_SCISSOR_TEST = uguugl.GL_SCISSOR_TEST
GL_COLOR_CLEAR_VALUE = uguugl.GL_COLOR_CLEAR_VALUE
GL_COLOR_WRITEMASK = uguugl.GL_COLOR_WRITEMASK
GL_UNPACK_ALIGNMENT = uguugl.GL_UNPACK_ALIGNMENT
GL_PACK_ALIGNMENT = uguugl.GL_PACK_ALIGNMENT
GL_MAX_TEXTURE_SIZE = uguugl.GL_MAX_TEXTURE_SIZE
GL_MAX_VIEWPORT_DIMS = uguugl.GL_MAX_VIEWPORT_DIMS
GL_SUBPIXEL_BITS = uguugl.GL_SUBPIXEL_BITS
GL_RED_BITS = uguugl.GL_RED_BITS
GL_GREEN_BITS = uguugl.GL_GREEN_BITS
GL_BLUE_BITS = uguugl.GL_BLUE_BITS
GL_ALPHA_BITS = uguugl.GL_ALPHA_BITS
GL_DEPTH_BITS = uguugl.GL_DEPTH_BITS
GL_STENCIL_BITS = uguugl.GL_STENCIL_BITS
GL_TEXTURE_2D = uguugl.GL_TEXTURE_2D
GL_DONT_CARE = uguugl.GL_DONT_CARE
GL_FASTEST = uguugl.GL_FASTEST
GL_NICEST = uguugl.GL_NICEST
GL_BYTE = uguugl.GL_BYTE
GL_UNSIGNED_BYTE = uguugl.GL_UNSIGNED_BYTE
GL_SHORT = uguugl.GL_SHORT
GL_UNSIGNED_SHORT = uguugl.GL_UNSIGNED_SHORT
GL_INT = uguugl.GL_INT
GL_UNSIGNED_INT = uguugl.GL_UNSIGNED_INT
GL_FLOAT = uguugl.GL_FLOAT
GL_INVERT = uguugl.GL_INVERT
GL_TEXTURE = uguugl.GL_TEXTURE
GL_DEPTH_COMPONENT = uguugl.GL_DEPTH_COMPONENT
GL_ALPHA = uguugl.GL_ALPHA
GL_RGB = uguugl.GL_RGB
GL_RGBA = uguugl.GL_RGBA
GL_LUMINANCE = uguugl.GL_LUMINANCE
GL_LUMINANCE_ALPHA = uguugl.GL_LUMINANCE_ALPHA
GL_KEEP = uguugl.GL_KEEP
GL_REPLACE = uguugl.GL_REPLACE
GL_INCR = uguugl.GL_INCR
GL_DECR = uguugl.GL_DECR
GL_VENDOR = uguugl.GL_VENDOR
GL_RENDERER = uguugl.GL_RENDERER
GL_VERSION = uguugl.GL_VERSION
GL_EXTENSIONS = uguugl.GL_EXTENSIONS
GL_NEAREST = uguugl.GL_NEAREST
GL_LINEAR = uguugl.GL_LINEAR
GL_NEAREST_MIPMAP_NEAREST = uguugl.GL_NEAREST_MIPMAP_NEAREST
GL_LINEAR_MIPMAP_NEAREST = uguugl.GL_LINEAR_MIPMAP_NEAREST
GL_NEAREST_MIPMAP_LINEAR = uguugl.GL_NEAREST_MIPMAP_LINEAR
GL_LINEAR_MIPMAP_LINEAR = uguugl.GL_LINEAR_MIPMAP_LINEAR
GL_TEXTURE_MAG_FILTER = uguugl.GL_TEXTURE_MAG_FILTER
GL_TEXTURE_MIN_FILTER = uguugl.GL_TEXTURE_MIN_FILTER
GL_TEXTURE_WRAP_S = uguugl.GL_TEXTURE_WRAP_S
GL_TEXTURE_WRAP_T = uguugl.GL_TEXTURE_WRAP_T
GL_REPEAT = uguugl.GL_REPEAT
GL_POLYGON_OFFSET_UNITS = uguugl.GL_POLYGON_OFFSET_UNITS
GL_COLOR_BUFFER_BIT = uguugl.GL_COLOR_BUFFER_BIT
GL_CONSTANT_COLOR = uguugl.GL_CONSTANT_COLOR
GL_ONE_MINUS_CONSTANT_COLOR = uguugl.GL_ONE_MINUS_CONSTANT_COLOR
GL_CONSTANT_ALPHA = uguugl.GL_CONSTANT_ALPHA
GL_ONE_MINUS_CONSTANT_ALPHA = uguugl.GL_ONE_MINUS_CONSTANT_ALPHA
GL_BLEND_COLOR = uguugl.GL_BLEND_COLOR
GL_FUNC_ADD = uguugl.GL_FUNC_ADD
GL_BLEND_EQUATION = uguugl.GL_BLEND_EQUATION
GL_BLEND_EQUATION_RGB = uguugl.GL_BLEND_EQUATION_RGB
GL_FUNC_SUBTRACT = uguugl.GL_FUNC_SUBTRACT
GL_FUNC_REVERSE_SUBTRACT = uguugl.GL_FUNC_REVERSE_SUBTRACT
GL_UNSIGNED_SHORT_4_4_4_4 = uguugl.GL_UNSIGNED_SHORT_4_4_4_4
GL_UNSIGNED_SHORT_5_5_5_1 = uguugl.GL_UNSIGNED_SHORT_5_5_5_1
GL_POLYGON_OFFSET_FILL = uguugl.GL_POLYGON_OFFSET_FILL
GL_POLYGON_OFFSET_FACTOR = uguugl.GL_POLYGON_OFFSET_FACTOR
GL_RGBA4 = uguugl.GL_RGBA4
GL_RGB5_A1 = uguugl.GL_RGB5_A1
GL_TEXTURE_BINDING_2D = uguugl.GL_TEXTURE_BINDING_2D
GL_SAMPLE_ALPHA_TO_COVERAGE = uguugl.GL_SAMPLE_ALPHA_TO_COVERAGE
GL_SAMPLE_COVERAGE = uguugl.GL_SAMPLE_COVERAGE
GL_SAMPLE_BUFFERS = uguugl.GL_SAMPLE_BUFFERS
GL_SAMPLES = uguugl.GL_SAMPLES
GL_SAMPLE_COVERAGE_VALUE = uguugl.GL_SAMPLE_COVERAGE_VALUE
GL_SAMPLE_COVERAGE_INVERT = uguugl.GL_SAMPLE_COVERAGE_INVERT
GL_BLEND_DST_RGB = uguugl.GL_BLEND_DST_RGB
GL_BLEND_SRC_RGB = uguugl.GL_BLEND_SRC_RGB
GL_BLEND_DST_ALPHA = uguugl.GL_BLEND_DST_ALPHA
GL_BLEND_SRC_ALPHA = uguugl.GL_BLEND_SRC_ALPHA
GL_CLAMP_TO_EDGE = uguugl.GL_CLAMP_TO_EDGE
GL_GENERATE_MIPMAP_HINT = uguugl.GL_GENERATE_MIPMAP_HINT
GL_DEPTH_COMPONENT16 = uguugl.GL_DEPTH_COMPONENT16
GL_UNSIGNED_SHORT_5_6_5 = uguugl.GL_UNSIGNED_SHORT_5_6_5
GL_MIRRORED_REPEAT = uguugl.GL_MIRRORED_REPEAT
GL_ALIASED_POINT_SIZE_RANGE = uguugl.GL_ALIASED_POINT_SIZE_RANGE
GL_ALIASED_LINE_WIDTH_RANGE = uguugl.GL_ALIASED_LINE_WIDTH_RANGE
GL_TEXTURE0 = uguugl.GL_TEXTURE0
GL_TEXTURE1 = uguugl.GL_TEXTURE1
GL_TEXTURE2 = uguugl.GL_TEXTURE2
GL_TEXTURE3 = uguugl.GL_TEXTURE3
GL_TEXTURE4 = uguugl.GL_TEXTURE4
GL_TEXTURE5 = uguugl.GL_TEXTURE5
GL_TEXTURE6 = uguugl.GL_TEXTURE6
GL_TEXTURE7 = uguugl.GL_TEXTURE7
GL_TEXTURE8 = uguugl.GL_TEXTURE8
GL_TEXTURE9 = uguugl.GL_TEXTURE9
GL_TEXTURE10 = uguugl.GL_TEXTURE10
GL_TEXTURE11 = uguugl.GL_TEXTURE11
GL_TEXTURE12 = uguugl.GL_TEXTURE12
GL_TEXTURE13 = uguugl.GL_TEXTURE13
GL_TEXTURE14 = uguugl.GL_TEXTURE14
GL_TEXTURE15 = uguugl.GL_TEXTURE15
GL_TEXTURE16 = uguugl.GL_TEXTURE16
GL_TEXTURE17 = uguugl.GL_TEXTURE17
GL_TEXTURE18 = uguugl.GL_TEXTURE18
GL_TEXTURE19 = uguugl.GL_TEXTURE19
GL_TEXTURE20 = uguugl.GL_TEXTURE20
GL_TEXTURE21 = uguugl.GL_TEXTURE21
GL_TEXTURE22 = uguugl.GL_TEXTURE22
GL_TEXTURE23 = uguugl.GL_TEXTURE23
GL_TEXTURE24 = uguugl.GL_TEXTURE24
GL_TEXTURE25 = uguugl.GL_TEXTURE25
GL_TEXTURE26 = uguugl.GL_TEXTURE26
GL_TEXTURE27 = uguugl.GL_TEXTURE27
GL_TEXTURE28 = uguugl.GL_TEXTURE28
GL_TEXTURE29 = uguugl.GL_TEXTURE29
GL_TEXTURE30 = uguugl.GL_TEXTURE30
GL_TEXTURE31 = uguugl.GL_TEXTURE31
GL_ACTIVE_TEXTURE = uguugl.GL_ACTIVE_TEXTURE
GL_MAX_RENDERBUFFER_SIZE = uguugl.GL_MAX_RENDERBUFFER_SIZE
GL_INCR_WRAP = uguugl.GL_INCR_WRAP
GL_DECR_WRAP = uguugl.GL_DECR_WRAP
GL_TEXTURE_CUBE_MAP = uguugl.GL_TEXTURE_CUBE_MAP
GL_TEXTURE_BINDING_CUBE_MAP = uguugl.GL_TEXTURE_BINDING_CUBE_MAP
GL_TEXTURE_CUBE_MAP_POSITIVE_X = uguugl.GL_TEXTURE_CUBE_MAP_POSITIVE_X
GL_TEXTURE_CUBE_MAP_NEGATIVE_X = uguugl.GL_TEXTURE_CUBE_MAP_NEGATIVE_X
GL_TEXTURE_CUBE_MAP_POSITIVE_Y = uguugl.GL_TEXTURE_CUBE_MAP_POSITIVE_Y
GL_TEXTURE_CUBE_MAP_NEGATIVE_Y = uguugl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
GL_TEXTURE_CUBE_MAP_POSITIVE_Z = uguugl.GL_TEXTURE_CUBE_MAP_POSITIVE_Z
GL_TEXTURE_CUBE_MAP_NEGATIVE_Z = uguugl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
GL_MAX_CUBE_MAP_TEXTURE_SIZE = uguugl.GL_MAX_CUBE_MAP_TEXTURE_SIZE
GL_VERTEX_ATTRIB_ARRAY_ENABLED = uguugl.GL_VERTEX_ATTRIB_ARRAY_ENABLED
GL_VERTEX_ATTRIB_ARRAY_SIZE = uguugl.GL_VERTEX_ATTRIB_ARRAY_SIZE
GL_VERTEX_ATTRIB_ARRAY_STRIDE = uguugl.GL_VERTEX_ATTRIB_ARRAY_STRIDE
GL_VERTEX_ATTRIB_ARRAY_TYPE = uguugl.GL_VERTEX_ATTRIB_ARRAY_TYPE
GL_CURRENT_VERTEX_ATTRIB = uguugl.GL_CURRENT_VERTEX_ATTRIB
GL_VERTEX_ATTRIB_ARRAY_POINTER = uguugl.GL_VERTEX_ATTRIB_ARRAY_POINTER
GL_NUM_COMPRESSED_TEXTURE_FORMATS = uguugl.GL_NUM_COMPRESSED_TEXTURE_FORMATS
GL_COMPRESSED_TEXTURE_FORMATS = uguugl.GL_COMPRESSED_TEXTURE_FORMATS
GL_BUFFER_SIZE = uguugl.GL_BUFFER_SIZE
GL_BUFFER_USAGE = uguugl.GL_BUFFER_USAGE
GL_STENCIL_BACK_FUNC = uguugl.GL_STENCIL_BACK_FUNC
GL_STENCIL_BACK_FAIL = uguugl.GL_STENCIL_BACK_FAIL
GL_STENCIL_BACK_PASS_DEPTH_FAIL = uguugl.GL_STENCIL_BACK_PASS_DEPTH_FAIL
GL_STENCIL_BACK_PASS_DEPTH_PASS = uguugl.GL_STENCIL_BACK_PASS_DEPTH_PASS
GL_BLEND_EQUATION_ALPHA = uguugl.GL_BLEND_EQUATION_ALPHA
GL_MAX_VERTEX_ATTRIBS = uguugl.GL_MAX_VERTEX_ATTRIBS
GL_VERTEX_ATTRIB_ARRAY_NORMALIZED = uguugl.GL_VERTEX_ATTRIB_ARRAY_NORMALIZED
GL_MAX_TEXTURE_IMAGE_UNITS = uguugl.GL_MAX_TEXTURE_IMAGE_UNITS
GL_ARRAY_BUFFER = uguugl.GL_ARRAY_BUFFER
GL_ELEMENT_ARRAY_BUFFER = uguugl.GL_ELEMENT_ARRAY_BUFFER
GL_ARRAY_BUFFER_BINDING = uguugl.GL_ARRAY_BUFFER_BINDING
GL_ELEMENT_ARRAY_BUFFER_BINDING = uguugl.GL_ELEMENT_ARRAY_BUFFER_BINDING
GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING = uguugl.GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING
GL_STREAM_DRAW = uguugl.GL_STREAM_DRAW
GL_STATIC_DRAW = uguugl.GL_STATIC_DRAW
GL_DYNAMIC_DRAW = uguugl.GL_DYNAMIC_DRAW
GL_FRAGMENT_SHADER = uguugl.GL_FRAGMENT_SHADER
GL_VERTEX_SHADER = uguugl.GL_VERTEX_SHADER
GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS = uguugl.GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS
GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS = uguugl.GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS
GL_SHADER_TYPE = uguugl.GL_SHADER_TYPE
GL_FLOAT_VEC2 = uguugl.GL_FLOAT_VEC2
GL_FLOAT_VEC3 = uguugl.GL_FLOAT_VEC3
GL_FLOAT_VEC4 = uguugl.GL_FLOAT_VEC4
GL_INT_VEC2 = uguugl.GL_INT_VEC2
GL_INT_VEC3 = uguugl.GL_INT_VEC3
GL_INT_VEC4 = uguugl.GL_INT_VEC4
GL_BOOL = uguugl.GL_BOOL
GL_BOOL_VEC2 = uguugl.GL_BOOL_VEC2
GL_BOOL_VEC3 = uguugl.GL_BOOL_VEC3
GL_BOOL_VEC4 = uguugl.GL_BOOL_VEC4
GL_FLOAT_MAT2 = uguugl.GL_FLOAT_MAT2
GL_FLOAT_MAT3 = uguugl.GL_FLOAT_MAT3
GL_FLOAT_MAT4 = uguugl.GL_FLOAT_MAT4
GL_SAMPLER_2D = uguugl.GL_SAMPLER_2D
GL_SAMPLER_CUBE = uguugl.GL_SAMPLER_CUBE
GL_DELETE_STATUS = uguugl.GL_DELETE_STATUS
GL_COMPILE_STATUS = uguugl.GL_COMPILE_STATUS
GL_LINK_STATUS = uguugl.GL_LINK_STATUS
GL_VALIDATE_STATUS = uguugl.GL_VALIDATE_STATUS
GL_INFO_LOG_LENGTH = uguugl.GL_INFO_LOG_LENGTH
GL_ATTACHED_SHADERS = uguugl.GL_ATTACHED_SHADERS
GL_ACTIVE_UNIFORMS = uguugl.GL_ACTIVE_UNIFORMS
GL_ACTIVE_UNIFORM_MAX_LENGTH = uguugl.GL_ACTIVE_UNIFORM_MAX_LENGTH
GL_SHADER_SOURCE_LENGTH = uguugl.GL_SHADER_SOURCE_LENGTH
GL_ACTIVE_ATTRIBUTES = uguugl.GL_ACTIVE_ATTRIBUTES
GL_ACTIVE_ATTRIBUTE_MAX_LENGTH = uguugl.GL_ACTIVE_ATTRIBUTE_MAX_LENGTH
GL_SHADING_LANGUAGE_VERSION = uguugl.GL_SHADING_LANGUAGE_VERSION
GL_CURRENT_PROGRAM = uguugl.GL_CURRENT_PROGRAM
GL_STENCIL_BACK_REF = uguugl.GL_STENCIL_BACK_REF
GL_STENCIL_BACK_VALUE_MASK = uguugl.GL_STENCIL_BACK_VALUE_MASK
GL_STENCIL_BACK_WRITEMASK = uguugl.GL_STENCIL_BACK_WRITEMASK
GL_FRAMEBUFFER_BINDING = uguugl.GL_FRAMEBUFFER_BINDING
GL_RENDERBUFFER_BINDING = uguugl.GL_RENDERBUFFER_BINDING
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE = uguugl.GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME = uguugl.GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL = uguugl.GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE = uguugl.GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE
GL_FRAMEBUFFER_COMPLETE = uguugl.GL_FRAMEBUFFER_COMPLETE
GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT = uguugl.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT
GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT = uguugl.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT
GL_FRAMEBUFFER_UNSUPPORTED = uguugl.GL_FRAMEBUFFER_UNSUPPORTED
GL_COLOR_ATTACHMENT0 = uguugl.GL_COLOR_ATTACHMENT0
GL_DEPTH_ATTACHMENT = uguugl.GL_DEPTH_ATTACHMENT
GL_STENCIL_ATTACHMENT = uguugl.GL_STENCIL_ATTACHMENT
GL_FRAMEBUFFER = uguugl.GL_FRAMEBUFFER
GL_RENDERBUFFER = uguugl.GL_RENDERBUFFER
GL_RENDERBUFFER_WIDTH = uguugl.GL_RENDERBUFFER_WIDTH
GL_RENDERBUFFER_HEIGHT = uguugl.GL_RENDERBUFFER_HEIGHT
GL_RENDERBUFFER_INTERNAL_FORMAT = uguugl.GL_RENDERBUFFER_INTERNAL_FORMAT
GL_STENCIL_INDEX8 = uguugl.GL_STENCIL_INDEX8
GL_RENDERBUFFER_RED_SIZE = uguugl.GL_RENDERBUFFER_RED_SIZE
GL_RENDERBUFFER_GREEN_SIZE = uguugl.GL_RENDERBUFFER_GREEN_SIZE
GL_RENDERBUFFER_BLUE_SIZE = uguugl.GL_RENDERBUFFER_BLUE_SIZE
GL_RENDERBUFFER_ALPHA_SIZE = uguugl.GL_RENDERBUFFER_ALPHA_SIZE
GL_RENDERBUFFER_DEPTH_SIZE = uguugl.GL_RENDERBUFFER_DEPTH_SIZE
GL_RENDERBUFFER_STENCIL_SIZE = uguugl.GL_RENDERBUFFER_STENCIL_SIZE
