from sdl2 cimport SDL_GL_GetProcAddress

cdef void *find_gl_command(names):

    cdef void *rv = NULL

    for i in names:
        rv = SDL_GL_GetProcAddress(i)

        if rv != NULL:
            return rv

    raise Exception("{} not found.".format(names[0]))


cdef const char *error_function
cdef GLenum error_code

def reset_error():
    """
    Resets the
    """

    global error_function
    error_function = NULL

    global error_code
    error_code = GL_NO_ERROR

reset_error()

def get_error():

    if error_function != NULL:
        return error_function.decode("utf-8"), error_code
    else:
        return None, GL_NO_ERROR


cdef void check_error(const char *function) nogil:

    global error_function
    global error_code

    cdef GLenum error

    error = real_glGetError()

    if (error_function == NULL) and (error != GL_NO_ERROR):
        error_function = function
        error_code = error



cdef glActiveTexture_type real_glActiveTexture
cdef glActiveTexture_type glActiveTexture

cdef void check_glActiveTexture(GLenum  texture) nogil:
    real_glActiveTexture(texture)
    check_error("glActiveTexture")

cdef glAttachShader_type real_glAttachShader
cdef glAttachShader_type glAttachShader

cdef void check_glAttachShader(GLuint  program, GLuint  shader) nogil:
    real_glAttachShader(program, shader)
    check_error("glAttachShader")

cdef glBindAttribLocation_type real_glBindAttribLocation
cdef glBindAttribLocation_type glBindAttribLocation

cdef void check_glBindAttribLocation(GLuint  program, GLuint  index, const GLchar * name) nogil:
    real_glBindAttribLocation(program, index, name)
    check_error("glBindAttribLocation")

cdef glBindBuffer_type real_glBindBuffer
cdef glBindBuffer_type glBindBuffer

cdef void check_glBindBuffer(GLenum  target, GLuint  buffer) nogil:
    real_glBindBuffer(target, buffer)
    check_error("glBindBuffer")

cdef glBindFramebuffer_type real_glBindFramebuffer
cdef glBindFramebuffer_type glBindFramebuffer

cdef void check_glBindFramebuffer(GLenum  target, GLuint  framebuffer) nogil:
    real_glBindFramebuffer(target, framebuffer)
    check_error("glBindFramebuffer")

cdef glBindRenderbuffer_type real_glBindRenderbuffer
cdef glBindRenderbuffer_type glBindRenderbuffer

cdef void check_glBindRenderbuffer(GLenum  target, GLuint  renderbuffer) nogil:
    real_glBindRenderbuffer(target, renderbuffer)
    check_error("glBindRenderbuffer")

cdef glBindTexture_type real_glBindTexture
cdef glBindTexture_type glBindTexture

cdef void check_glBindTexture(GLenum  target, GLuint  texture) nogil:
    real_glBindTexture(target, texture)
    check_error("glBindTexture")

cdef glBlendColor_type real_glBlendColor
cdef glBlendColor_type glBlendColor

cdef void check_glBlendColor(GLfloat  red, GLfloat  green, GLfloat  blue, GLfloat  alpha) nogil:
    real_glBlendColor(red, green, blue, alpha)
    check_error("glBlendColor")

cdef glBlendEquation_type real_glBlendEquation
cdef glBlendEquation_type glBlendEquation

cdef void check_glBlendEquation(GLenum  mode) nogil:
    real_glBlendEquation(mode)
    check_error("glBlendEquation")

cdef glBlendEquationSeparate_type real_glBlendEquationSeparate
cdef glBlendEquationSeparate_type glBlendEquationSeparate

cdef void check_glBlendEquationSeparate(GLenum  modeRGB, GLenum  modeAlpha) nogil:
    real_glBlendEquationSeparate(modeRGB, modeAlpha)
    check_error("glBlendEquationSeparate")

cdef glBlendFunc_type real_glBlendFunc
cdef glBlendFunc_type glBlendFunc

cdef void check_glBlendFunc(GLenum  sfactor, GLenum  dfactor) nogil:
    real_glBlendFunc(sfactor, dfactor)
    check_error("glBlendFunc")

cdef glBlendFuncSeparate_type real_glBlendFuncSeparate
cdef glBlendFuncSeparate_type glBlendFuncSeparate

cdef void check_glBlendFuncSeparate(GLenum  sfactorRGB, GLenum  dfactorRGB, GLenum  sfactorAlpha, GLenum  dfactorAlpha) nogil:
    real_glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha)
    check_error("glBlendFuncSeparate")

cdef glBufferData_type real_glBufferData
cdef glBufferData_type glBufferData

cdef void check_glBufferData(GLenum  target, GLsizeiptr  size, const void * data, GLenum  usage) nogil:
    real_glBufferData(target, size, data, usage)
    check_error("glBufferData")

cdef glBufferSubData_type real_glBufferSubData
cdef glBufferSubData_type glBufferSubData

cdef void check_glBufferSubData(GLenum  target, GLintptr  offset, GLsizeiptr  size, const void * data) nogil:
    real_glBufferSubData(target, offset, size, data)
    check_error("glBufferSubData")

cdef glCheckFramebufferStatus_type real_glCheckFramebufferStatus
cdef glCheckFramebufferStatus_type glCheckFramebufferStatus

cdef GLenum check_glCheckFramebufferStatus(GLenum  target) nogil:
    cdef GLenum rv
    rv = real_glCheckFramebufferStatus(target)
    check_error("glCheckFramebufferStatus")
    return rv

cdef glClear_type real_glClear
cdef glClear_type glClear

cdef void check_glClear(GLbitfield  mask) nogil:
    real_glClear(mask)
    check_error("glClear")

cdef glClearColor_type real_glClearColor
cdef glClearColor_type glClearColor

cdef void check_glClearColor(GLfloat  red, GLfloat  green, GLfloat  blue, GLfloat  alpha) nogil:
    real_glClearColor(red, green, blue, alpha)
    check_error("glClearColor")

cdef glClearStencil_type real_glClearStencil
cdef glClearStencil_type glClearStencil

cdef void check_glClearStencil(GLint  s) nogil:
    real_glClearStencil(s)
    check_error("glClearStencil")

cdef glColorMask_type real_glColorMask
cdef glColorMask_type glColorMask

cdef void check_glColorMask(GLboolean  red, GLboolean  green, GLboolean  blue, GLboolean  alpha) nogil:
    real_glColorMask(red, green, blue, alpha)
    check_error("glColorMask")

cdef glCompileShader_type real_glCompileShader
cdef glCompileShader_type glCompileShader

cdef void check_glCompileShader(GLuint  shader) nogil:
    real_glCompileShader(shader)
    check_error("glCompileShader")

cdef glCompressedTexImage2D_type real_glCompressedTexImage2D
cdef glCompressedTexImage2D_type glCompressedTexImage2D

cdef void check_glCompressedTexImage2D(GLenum  target, GLint  level, GLenum  internalformat, GLsizei  width, GLsizei  height, GLint  border, GLsizei  imageSize, const void * data) nogil:
    real_glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, data)
    check_error("glCompressedTexImage2D")

cdef glCompressedTexSubImage2D_type real_glCompressedTexSubImage2D
cdef glCompressedTexSubImage2D_type glCompressedTexSubImage2D

cdef void check_glCompressedTexSubImage2D(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLsizei  width, GLsizei  height, GLenum  format, GLsizei  imageSize, const void * data) nogil:
    real_glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, data)
    check_error("glCompressedTexSubImage2D")

cdef glCopyTexImage2D_type real_glCopyTexImage2D
cdef glCopyTexImage2D_type glCopyTexImage2D

cdef void check_glCopyTexImage2D(GLenum  target, GLint  level, GLenum  internalformat, GLint  x, GLint  y, GLsizei  width, GLsizei  height, GLint  border) nogil:
    real_glCopyTexImage2D(target, level, internalformat, x, y, width, height, border)
    check_error("glCopyTexImage2D")

cdef glCopyTexSubImage2D_type real_glCopyTexSubImage2D
cdef glCopyTexSubImage2D_type glCopyTexSubImage2D

cdef void check_glCopyTexSubImage2D(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil:
    real_glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height)
    check_error("glCopyTexSubImage2D")

cdef glCreateProgram_type real_glCreateProgram
cdef glCreateProgram_type glCreateProgram

cdef GLuint check_glCreateProgram() nogil:
    cdef GLuint rv
    rv = real_glCreateProgram()
    check_error("glCreateProgram")
    return rv

cdef glCreateShader_type real_glCreateShader
cdef glCreateShader_type glCreateShader

cdef GLuint check_glCreateShader(GLenum  type) nogil:
    cdef GLuint rv
    rv = real_glCreateShader(type)
    check_error("glCreateShader")
    return rv

cdef glCullFace_type real_glCullFace
cdef glCullFace_type glCullFace

cdef void check_glCullFace(GLenum  mode) nogil:
    real_glCullFace(mode)
    check_error("glCullFace")

cdef glDeleteBuffers_type real_glDeleteBuffers
cdef glDeleteBuffers_type glDeleteBuffers

cdef void check_glDeleteBuffers(GLsizei  n, const GLuint * buffers) nogil:
    real_glDeleteBuffers(n, buffers)
    check_error("glDeleteBuffers")

cdef glDeleteFramebuffers_type real_glDeleteFramebuffers
cdef glDeleteFramebuffers_type glDeleteFramebuffers

cdef void check_glDeleteFramebuffers(GLsizei  n, const GLuint * framebuffers) nogil:
    real_glDeleteFramebuffers(n, framebuffers)
    check_error("glDeleteFramebuffers")

cdef glDeleteProgram_type real_glDeleteProgram
cdef glDeleteProgram_type glDeleteProgram

cdef void check_glDeleteProgram(GLuint  program) nogil:
    real_glDeleteProgram(program)
    check_error("glDeleteProgram")

cdef glDeleteRenderbuffers_type real_glDeleteRenderbuffers
cdef glDeleteRenderbuffers_type glDeleteRenderbuffers

cdef void check_glDeleteRenderbuffers(GLsizei  n, const GLuint * renderbuffers) nogil:
    real_glDeleteRenderbuffers(n, renderbuffers)
    check_error("glDeleteRenderbuffers")

cdef glDeleteShader_type real_glDeleteShader
cdef glDeleteShader_type glDeleteShader

cdef void check_glDeleteShader(GLuint  shader) nogil:
    real_glDeleteShader(shader)
    check_error("glDeleteShader")

cdef glDeleteTextures_type real_glDeleteTextures
cdef glDeleteTextures_type glDeleteTextures

cdef void check_glDeleteTextures(GLsizei  n, const GLuint * textures) nogil:
    real_glDeleteTextures(n, textures)
    check_error("glDeleteTextures")

cdef glDepthFunc_type real_glDepthFunc
cdef glDepthFunc_type glDepthFunc

cdef void check_glDepthFunc(GLenum  func) nogil:
    real_glDepthFunc(func)
    check_error("glDepthFunc")

cdef glDepthMask_type real_glDepthMask
cdef glDepthMask_type glDepthMask

cdef void check_glDepthMask(GLboolean  flag) nogil:
    real_glDepthMask(flag)
    check_error("glDepthMask")

cdef glDetachShader_type real_glDetachShader
cdef glDetachShader_type glDetachShader

cdef void check_glDetachShader(GLuint  program, GLuint  shader) nogil:
    real_glDetachShader(program, shader)
    check_error("glDetachShader")

cdef glDisable_type real_glDisable
cdef glDisable_type glDisable

cdef void check_glDisable(GLenum  cap) nogil:
    real_glDisable(cap)
    check_error("glDisable")

cdef glDisableVertexAttribArray_type real_glDisableVertexAttribArray
cdef glDisableVertexAttribArray_type glDisableVertexAttribArray

cdef void check_glDisableVertexAttribArray(GLuint  index) nogil:
    real_glDisableVertexAttribArray(index)
    check_error("glDisableVertexAttribArray")

cdef glDrawArrays_type real_glDrawArrays
cdef glDrawArrays_type glDrawArrays

cdef void check_glDrawArrays(GLenum  mode, GLint  first, GLsizei  count) nogil:
    real_glDrawArrays(mode, first, count)
    check_error("glDrawArrays")

cdef glDrawElements_type real_glDrawElements
cdef glDrawElements_type glDrawElements

cdef void check_glDrawElements(GLenum  mode, GLsizei  count, GLenum  type, const void * indices) nogil:
    real_glDrawElements(mode, count, type, indices)
    check_error("glDrawElements")

cdef glEnable_type real_glEnable
cdef glEnable_type glEnable

cdef void check_glEnable(GLenum  cap) nogil:
    real_glEnable(cap)
    check_error("glEnable")

cdef glEnableVertexAttribArray_type real_glEnableVertexAttribArray
cdef glEnableVertexAttribArray_type glEnableVertexAttribArray

cdef void check_glEnableVertexAttribArray(GLuint  index) nogil:
    real_glEnableVertexAttribArray(index)
    check_error("glEnableVertexAttribArray")

cdef glFinish_type real_glFinish
cdef glFinish_type glFinish

cdef void check_glFinish() nogil:
    real_glFinish()
    check_error("glFinish")

cdef glFlush_type real_glFlush
cdef glFlush_type glFlush

cdef void check_glFlush() nogil:
    real_glFlush()
    check_error("glFlush")

cdef glFramebufferRenderbuffer_type real_glFramebufferRenderbuffer
cdef glFramebufferRenderbuffer_type glFramebufferRenderbuffer

cdef void check_glFramebufferRenderbuffer(GLenum  target, GLenum  attachment, GLenum  renderbuffertarget, GLuint  renderbuffer) nogil:
    real_glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer)
    check_error("glFramebufferRenderbuffer")

cdef glFramebufferTexture2D_type real_glFramebufferTexture2D
cdef glFramebufferTexture2D_type glFramebufferTexture2D

cdef void check_glFramebufferTexture2D(GLenum  target, GLenum  attachment, GLenum  textarget, GLuint  texture, GLint  level) nogil:
    real_glFramebufferTexture2D(target, attachment, textarget, texture, level)
    check_error("glFramebufferTexture2D")

cdef glFrontFace_type real_glFrontFace
cdef glFrontFace_type glFrontFace

cdef void check_glFrontFace(GLenum  mode) nogil:
    real_glFrontFace(mode)
    check_error("glFrontFace")

cdef glGenBuffers_type real_glGenBuffers
cdef glGenBuffers_type glGenBuffers

cdef void check_glGenBuffers(GLsizei  n, GLuint * buffers) nogil:
    real_glGenBuffers(n, buffers)
    check_error("glGenBuffers")

cdef glGenFramebuffers_type real_glGenFramebuffers
cdef glGenFramebuffers_type glGenFramebuffers

cdef void check_glGenFramebuffers(GLsizei  n, GLuint * framebuffers) nogil:
    real_glGenFramebuffers(n, framebuffers)
    check_error("glGenFramebuffers")

cdef glGenRenderbuffers_type real_glGenRenderbuffers
cdef glGenRenderbuffers_type glGenRenderbuffers

cdef void check_glGenRenderbuffers(GLsizei  n, GLuint * renderbuffers) nogil:
    real_glGenRenderbuffers(n, renderbuffers)
    check_error("glGenRenderbuffers")

cdef glGenTextures_type real_glGenTextures
cdef glGenTextures_type glGenTextures

cdef void check_glGenTextures(GLsizei  n, GLuint * textures) nogil:
    real_glGenTextures(n, textures)
    check_error("glGenTextures")

cdef glGenerateMipmap_type real_glGenerateMipmap
cdef glGenerateMipmap_type glGenerateMipmap

cdef void check_glGenerateMipmap(GLenum  target) nogil:
    real_glGenerateMipmap(target)
    check_error("glGenerateMipmap")

cdef glGetActiveAttrib_type real_glGetActiveAttrib
cdef glGetActiveAttrib_type glGetActiveAttrib

cdef void check_glGetActiveAttrib(GLuint  program, GLuint  index, GLsizei  bufSize, GLsizei * length, GLint * size, GLenum * type, GLchar * name) nogil:
    real_glGetActiveAttrib(program, index, bufSize, length, size, type, name)
    check_error("glGetActiveAttrib")

cdef glGetActiveUniform_type real_glGetActiveUniform
cdef glGetActiveUniform_type glGetActiveUniform

cdef void check_glGetActiveUniform(GLuint  program, GLuint  index, GLsizei  bufSize, GLsizei * length, GLint * size, GLenum * type, GLchar * name) nogil:
    real_glGetActiveUniform(program, index, bufSize, length, size, type, name)
    check_error("glGetActiveUniform")

cdef glGetAttachedShaders_type real_glGetAttachedShaders
cdef glGetAttachedShaders_type glGetAttachedShaders

cdef void check_glGetAttachedShaders(GLuint  program, GLsizei  maxCount, GLsizei * count, GLuint * shaders) nogil:
    real_glGetAttachedShaders(program, maxCount, count, shaders)
    check_error("glGetAttachedShaders")

cdef glGetAttribLocation_type real_glGetAttribLocation
cdef glGetAttribLocation_type glGetAttribLocation

cdef GLint check_glGetAttribLocation(GLuint  program, const GLchar * name) nogil:
    cdef GLint rv
    rv = real_glGetAttribLocation(program, name)
    check_error("glGetAttribLocation")
    return rv

cdef glGetBooleanv_type real_glGetBooleanv
cdef glGetBooleanv_type glGetBooleanv

cdef void check_glGetBooleanv(GLenum  pname, GLboolean * data) nogil:
    real_glGetBooleanv(pname, data)
    check_error("glGetBooleanv")

cdef glGetBufferParameteriv_type real_glGetBufferParameteriv
cdef glGetBufferParameteriv_type glGetBufferParameteriv

cdef void check_glGetBufferParameteriv(GLenum  target, GLenum  pname, GLint * params) nogil:
    real_glGetBufferParameteriv(target, pname, params)
    check_error("glGetBufferParameteriv")

cdef glGetError_type real_glGetError
cdef glGetError_type glGetError

cdef GLenum check_glGetError() nogil:
    cdef GLenum rv
    rv = real_glGetError()
    check_error("glGetError")
    return rv

cdef glGetFloatv_type real_glGetFloatv
cdef glGetFloatv_type glGetFloatv

cdef void check_glGetFloatv(GLenum  pname, GLfloat * data) nogil:
    real_glGetFloatv(pname, data)
    check_error("glGetFloatv")

cdef glGetFramebufferAttachmentParameteriv_type real_glGetFramebufferAttachmentParameteriv
cdef glGetFramebufferAttachmentParameteriv_type glGetFramebufferAttachmentParameteriv

cdef void check_glGetFramebufferAttachmentParameteriv(GLenum  target, GLenum  attachment, GLenum  pname, GLint * params) nogil:
    real_glGetFramebufferAttachmentParameteriv(target, attachment, pname, params)
    check_error("glGetFramebufferAttachmentParameteriv")

cdef glGetIntegerv_type real_glGetIntegerv
cdef glGetIntegerv_type glGetIntegerv

cdef void check_glGetIntegerv(GLenum  pname, GLint * data) nogil:
    real_glGetIntegerv(pname, data)
    check_error("glGetIntegerv")

cdef glGetProgramInfoLog_type real_glGetProgramInfoLog
cdef glGetProgramInfoLog_type glGetProgramInfoLog

cdef void check_glGetProgramInfoLog(GLuint  program, GLsizei  bufSize, GLsizei * length, GLchar * infoLog) nogil:
    real_glGetProgramInfoLog(program, bufSize, length, infoLog)
    check_error("glGetProgramInfoLog")

cdef glGetProgramiv_type real_glGetProgramiv
cdef glGetProgramiv_type glGetProgramiv

cdef void check_glGetProgramiv(GLuint  program, GLenum  pname, GLint * params) nogil:
    real_glGetProgramiv(program, pname, params)
    check_error("glGetProgramiv")

cdef glGetRenderbufferParameteriv_type real_glGetRenderbufferParameteriv
cdef glGetRenderbufferParameteriv_type glGetRenderbufferParameteriv

cdef void check_glGetRenderbufferParameteriv(GLenum  target, GLenum  pname, GLint * params) nogil:
    real_glGetRenderbufferParameteriv(target, pname, params)
    check_error("glGetRenderbufferParameteriv")

cdef glGetShaderInfoLog_type real_glGetShaderInfoLog
cdef glGetShaderInfoLog_type glGetShaderInfoLog

cdef void check_glGetShaderInfoLog(GLuint  shader, GLsizei  bufSize, GLsizei * length, GLchar * infoLog) nogil:
    real_glGetShaderInfoLog(shader, bufSize, length, infoLog)
    check_error("glGetShaderInfoLog")

cdef glGetShaderSource_type real_glGetShaderSource
cdef glGetShaderSource_type glGetShaderSource

cdef void check_glGetShaderSource(GLuint  shader, GLsizei  bufSize, GLsizei * length, GLchar * source) nogil:
    real_glGetShaderSource(shader, bufSize, length, source)
    check_error("glGetShaderSource")

cdef glGetShaderiv_type real_glGetShaderiv
cdef glGetShaderiv_type glGetShaderiv

cdef void check_glGetShaderiv(GLuint  shader, GLenum  pname, GLint * params) nogil:
    real_glGetShaderiv(shader, pname, params)
    check_error("glGetShaderiv")

cdef glGetString_type real_glGetString
cdef glGetString_type glGetString

cdef const GLubyte * check_glGetString(GLenum  name) nogil:
    cdef const GLubyte * rv
    rv = real_glGetString(name)
    check_error("glGetString")
    return rv

cdef glGetTexParameterfv_type real_glGetTexParameterfv
cdef glGetTexParameterfv_type glGetTexParameterfv

cdef void check_glGetTexParameterfv(GLenum  target, GLenum  pname, GLfloat * params) nogil:
    real_glGetTexParameterfv(target, pname, params)
    check_error("glGetTexParameterfv")

cdef glGetTexParameteriv_type real_glGetTexParameteriv
cdef glGetTexParameteriv_type glGetTexParameteriv

cdef void check_glGetTexParameteriv(GLenum  target, GLenum  pname, GLint * params) nogil:
    real_glGetTexParameteriv(target, pname, params)
    check_error("glGetTexParameteriv")

cdef glGetUniformLocation_type real_glGetUniformLocation
cdef glGetUniformLocation_type glGetUniformLocation

cdef GLint check_glGetUniformLocation(GLuint  program, const GLchar * name) nogil:
    cdef GLint rv
    rv = real_glGetUniformLocation(program, name)
    check_error("glGetUniformLocation")
    return rv

cdef glGetUniformfv_type real_glGetUniformfv
cdef glGetUniformfv_type glGetUniformfv

cdef void check_glGetUniformfv(GLuint  program, GLint  location, GLfloat * params) nogil:
    real_glGetUniformfv(program, location, params)
    check_error("glGetUniformfv")

cdef glGetUniformiv_type real_glGetUniformiv
cdef glGetUniformiv_type glGetUniformiv

cdef void check_glGetUniformiv(GLuint  program, GLint  location, GLint * params) nogil:
    real_glGetUniformiv(program, location, params)
    check_error("glGetUniformiv")

cdef glGetVertexAttribPointerv_type real_glGetVertexAttribPointerv
cdef glGetVertexAttribPointerv_type glGetVertexAttribPointerv

cdef void check_glGetVertexAttribPointerv(GLuint  index, GLenum  pname, void ** pointer) nogil:
    real_glGetVertexAttribPointerv(index, pname, pointer)
    check_error("glGetVertexAttribPointerv")

cdef glGetVertexAttribfv_type real_glGetVertexAttribfv
cdef glGetVertexAttribfv_type glGetVertexAttribfv

cdef void check_glGetVertexAttribfv(GLuint  index, GLenum  pname, GLfloat * params) nogil:
    real_glGetVertexAttribfv(index, pname, params)
    check_error("glGetVertexAttribfv")

cdef glGetVertexAttribiv_type real_glGetVertexAttribiv
cdef glGetVertexAttribiv_type glGetVertexAttribiv

cdef void check_glGetVertexAttribiv(GLuint  index, GLenum  pname, GLint * params) nogil:
    real_glGetVertexAttribiv(index, pname, params)
    check_error("glGetVertexAttribiv")

cdef glHint_type real_glHint
cdef glHint_type glHint

cdef void check_glHint(GLenum  target, GLenum  mode) nogil:
    real_glHint(target, mode)
    check_error("glHint")

cdef glIsBuffer_type real_glIsBuffer
cdef glIsBuffer_type glIsBuffer

cdef GLboolean check_glIsBuffer(GLuint  buffer) nogil:
    cdef GLboolean rv
    rv = real_glIsBuffer(buffer)
    check_error("glIsBuffer")
    return rv

cdef glIsEnabled_type real_glIsEnabled
cdef glIsEnabled_type glIsEnabled

cdef GLboolean check_glIsEnabled(GLenum  cap) nogil:
    cdef GLboolean rv
    rv = real_glIsEnabled(cap)
    check_error("glIsEnabled")
    return rv

cdef glIsFramebuffer_type real_glIsFramebuffer
cdef glIsFramebuffer_type glIsFramebuffer

cdef GLboolean check_glIsFramebuffer(GLuint  framebuffer) nogil:
    cdef GLboolean rv
    rv = real_glIsFramebuffer(framebuffer)
    check_error("glIsFramebuffer")
    return rv

cdef glIsProgram_type real_glIsProgram
cdef glIsProgram_type glIsProgram

cdef GLboolean check_glIsProgram(GLuint  program) nogil:
    cdef GLboolean rv
    rv = real_glIsProgram(program)
    check_error("glIsProgram")
    return rv

cdef glIsRenderbuffer_type real_glIsRenderbuffer
cdef glIsRenderbuffer_type glIsRenderbuffer

cdef GLboolean check_glIsRenderbuffer(GLuint  renderbuffer) nogil:
    cdef GLboolean rv
    rv = real_glIsRenderbuffer(renderbuffer)
    check_error("glIsRenderbuffer")
    return rv

cdef glIsShader_type real_glIsShader
cdef glIsShader_type glIsShader

cdef GLboolean check_glIsShader(GLuint  shader) nogil:
    cdef GLboolean rv
    rv = real_glIsShader(shader)
    check_error("glIsShader")
    return rv

cdef glIsTexture_type real_glIsTexture
cdef glIsTexture_type glIsTexture

cdef GLboolean check_glIsTexture(GLuint  texture) nogil:
    cdef GLboolean rv
    rv = real_glIsTexture(texture)
    check_error("glIsTexture")
    return rv

cdef glLineWidth_type real_glLineWidth
cdef glLineWidth_type glLineWidth

cdef void check_glLineWidth(GLfloat  width) nogil:
    real_glLineWidth(width)
    check_error("glLineWidth")

cdef glLinkProgram_type real_glLinkProgram
cdef glLinkProgram_type glLinkProgram

cdef void check_glLinkProgram(GLuint  program) nogil:
    real_glLinkProgram(program)
    check_error("glLinkProgram")

cdef glPixelStorei_type real_glPixelStorei
cdef glPixelStorei_type glPixelStorei

cdef void check_glPixelStorei(GLenum  pname, GLint  param) nogil:
    real_glPixelStorei(pname, param)
    check_error("glPixelStorei")

cdef glPolygonOffset_type real_glPolygonOffset
cdef glPolygonOffset_type glPolygonOffset

cdef void check_glPolygonOffset(GLfloat  factor, GLfloat  units) nogil:
    real_glPolygonOffset(factor, units)
    check_error("glPolygonOffset")

cdef glReadPixels_type real_glReadPixels
cdef glReadPixels_type glReadPixels

cdef void check_glReadPixels(GLint  x, GLint  y, GLsizei  width, GLsizei  height, GLenum  format, GLenum  type, void * pixels) nogil:
    real_glReadPixels(x, y, width, height, format, type, pixels)
    check_error("glReadPixels")

cdef glRenderbufferStorage_type real_glRenderbufferStorage
cdef glRenderbufferStorage_type glRenderbufferStorage

cdef void check_glRenderbufferStorage(GLenum  target, GLenum  internalformat, GLsizei  width, GLsizei  height) nogil:
    real_glRenderbufferStorage(target, internalformat, width, height)
    check_error("glRenderbufferStorage")

cdef glSampleCoverage_type real_glSampleCoverage
cdef glSampleCoverage_type glSampleCoverage

cdef void check_glSampleCoverage(GLfloat  value, GLboolean  invert) nogil:
    real_glSampleCoverage(value, invert)
    check_error("glSampleCoverage")

cdef glScissor_type real_glScissor
cdef glScissor_type glScissor

cdef void check_glScissor(GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil:
    real_glScissor(x, y, width, height)
    check_error("glScissor")

cdef glShaderSource_type real_glShaderSource
cdef glShaderSource_type glShaderSource

cdef void check_glShaderSource(GLuint  shader, GLsizei  count, const GLchar *const* string, const GLint * length) nogil:
    real_glShaderSource(shader, count, string, length)
    check_error("glShaderSource")

cdef glStencilFunc_type real_glStencilFunc
cdef glStencilFunc_type glStencilFunc

cdef void check_glStencilFunc(GLenum  func, GLint  ref, GLuint  mask) nogil:
    real_glStencilFunc(func, ref, mask)
    check_error("glStencilFunc")

cdef glStencilFuncSeparate_type real_glStencilFuncSeparate
cdef glStencilFuncSeparate_type glStencilFuncSeparate

cdef void check_glStencilFuncSeparate(GLenum  face, GLenum  func, GLint  ref, GLuint  mask) nogil:
    real_glStencilFuncSeparate(face, func, ref, mask)
    check_error("glStencilFuncSeparate")

cdef glStencilMask_type real_glStencilMask
cdef glStencilMask_type glStencilMask

cdef void check_glStencilMask(GLuint  mask) nogil:
    real_glStencilMask(mask)
    check_error("glStencilMask")

cdef glStencilMaskSeparate_type real_glStencilMaskSeparate
cdef glStencilMaskSeparate_type glStencilMaskSeparate

cdef void check_glStencilMaskSeparate(GLenum  face, GLuint  mask) nogil:
    real_glStencilMaskSeparate(face, mask)
    check_error("glStencilMaskSeparate")

cdef glStencilOp_type real_glStencilOp
cdef glStencilOp_type glStencilOp

cdef void check_glStencilOp(GLenum  fail, GLenum  zfail, GLenum  zpass) nogil:
    real_glStencilOp(fail, zfail, zpass)
    check_error("glStencilOp")

cdef glStencilOpSeparate_type real_glStencilOpSeparate
cdef glStencilOpSeparate_type glStencilOpSeparate

cdef void check_glStencilOpSeparate(GLenum  face, GLenum  sfail, GLenum  dpfail, GLenum  dppass) nogil:
    real_glStencilOpSeparate(face, sfail, dpfail, dppass)
    check_error("glStencilOpSeparate")

cdef glTexImage2D_type real_glTexImage2D
cdef glTexImage2D_type glTexImage2D

cdef void check_glTexImage2D(GLenum  target, GLint  level, GLint  internalformat, GLsizei  width, GLsizei  height, GLint  border, GLenum  format, GLenum  type, const void * pixels) nogil:
    real_glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels)
    check_error("glTexImage2D")

cdef glTexParameterf_type real_glTexParameterf
cdef glTexParameterf_type glTexParameterf

cdef void check_glTexParameterf(GLenum  target, GLenum  pname, GLfloat  param) nogil:
    real_glTexParameterf(target, pname, param)
    check_error("glTexParameterf")

cdef glTexParameterfv_type real_glTexParameterfv
cdef glTexParameterfv_type glTexParameterfv

cdef void check_glTexParameterfv(GLenum  target, GLenum  pname, const GLfloat * params) nogil:
    real_glTexParameterfv(target, pname, params)
    check_error("glTexParameterfv")

cdef glTexParameteri_type real_glTexParameteri
cdef glTexParameteri_type glTexParameteri

cdef void check_glTexParameteri(GLenum  target, GLenum  pname, GLint  param) nogil:
    real_glTexParameteri(target, pname, param)
    check_error("glTexParameteri")

cdef glTexParameteriv_type real_glTexParameteriv
cdef glTexParameteriv_type glTexParameteriv

cdef void check_glTexParameteriv(GLenum  target, GLenum  pname, const GLint * params) nogil:
    real_glTexParameteriv(target, pname, params)
    check_error("glTexParameteriv")

cdef glTexSubImage2D_type real_glTexSubImage2D
cdef glTexSubImage2D_type glTexSubImage2D

cdef void check_glTexSubImage2D(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLsizei  width, GLsizei  height, GLenum  format, GLenum  type, const void * pixels) nogil:
    real_glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels)
    check_error("glTexSubImage2D")

cdef glUniform1f_type real_glUniform1f
cdef glUniform1f_type glUniform1f

cdef void check_glUniform1f(GLint  location, GLfloat  v0) nogil:
    real_glUniform1f(location, v0)
    check_error("glUniform1f")

cdef glUniform1fv_type real_glUniform1fv
cdef glUniform1fv_type glUniform1fv

cdef void check_glUniform1fv(GLint  location, GLsizei  count, const GLfloat * value) nogil:
    real_glUniform1fv(location, count, value)
    check_error("glUniform1fv")

cdef glUniform1i_type real_glUniform1i
cdef glUniform1i_type glUniform1i

cdef void check_glUniform1i(GLint  location, GLint  v0) nogil:
    real_glUniform1i(location, v0)
    check_error("glUniform1i")

cdef glUniform1iv_type real_glUniform1iv
cdef glUniform1iv_type glUniform1iv

cdef void check_glUniform1iv(GLint  location, GLsizei  count, const GLint * value) nogil:
    real_glUniform1iv(location, count, value)
    check_error("glUniform1iv")

cdef glUniform2f_type real_glUniform2f
cdef glUniform2f_type glUniform2f

cdef void check_glUniform2f(GLint  location, GLfloat  v0, GLfloat  v1) nogil:
    real_glUniform2f(location, v0, v1)
    check_error("glUniform2f")

cdef glUniform2fv_type real_glUniform2fv
cdef glUniform2fv_type glUniform2fv

cdef void check_glUniform2fv(GLint  location, GLsizei  count, const GLfloat * value) nogil:
    real_glUniform2fv(location, count, value)
    check_error("glUniform2fv")

cdef glUniform2i_type real_glUniform2i
cdef glUniform2i_type glUniform2i

cdef void check_glUniform2i(GLint  location, GLint  v0, GLint  v1) nogil:
    real_glUniform2i(location, v0, v1)
    check_error("glUniform2i")

cdef glUniform2iv_type real_glUniform2iv
cdef glUniform2iv_type glUniform2iv

cdef void check_glUniform2iv(GLint  location, GLsizei  count, const GLint * value) nogil:
    real_glUniform2iv(location, count, value)
    check_error("glUniform2iv")

cdef glUniform3f_type real_glUniform3f
cdef glUniform3f_type glUniform3f

cdef void check_glUniform3f(GLint  location, GLfloat  v0, GLfloat  v1, GLfloat  v2) nogil:
    real_glUniform3f(location, v0, v1, v2)
    check_error("glUniform3f")

cdef glUniform3fv_type real_glUniform3fv
cdef glUniform3fv_type glUniform3fv

cdef void check_glUniform3fv(GLint  location, GLsizei  count, const GLfloat * value) nogil:
    real_glUniform3fv(location, count, value)
    check_error("glUniform3fv")

cdef glUniform3i_type real_glUniform3i
cdef glUniform3i_type glUniform3i

cdef void check_glUniform3i(GLint  location, GLint  v0, GLint  v1, GLint  v2) nogil:
    real_glUniform3i(location, v0, v1, v2)
    check_error("glUniform3i")

cdef glUniform3iv_type real_glUniform3iv
cdef glUniform3iv_type glUniform3iv

cdef void check_glUniform3iv(GLint  location, GLsizei  count, const GLint * value) nogil:
    real_glUniform3iv(location, count, value)
    check_error("glUniform3iv")

cdef glUniform4f_type real_glUniform4f
cdef glUniform4f_type glUniform4f

cdef void check_glUniform4f(GLint  location, GLfloat  v0, GLfloat  v1, GLfloat  v2, GLfloat  v3) nogil:
    real_glUniform4f(location, v0, v1, v2, v3)
    check_error("glUniform4f")

cdef glUniform4fv_type real_glUniform4fv
cdef glUniform4fv_type glUniform4fv

cdef void check_glUniform4fv(GLint  location, GLsizei  count, const GLfloat * value) nogil:
    real_glUniform4fv(location, count, value)
    check_error("glUniform4fv")

cdef glUniform4i_type real_glUniform4i
cdef glUniform4i_type glUniform4i

cdef void check_glUniform4i(GLint  location, GLint  v0, GLint  v1, GLint  v2, GLint  v3) nogil:
    real_glUniform4i(location, v0, v1, v2, v3)
    check_error("glUniform4i")

cdef glUniform4iv_type real_glUniform4iv
cdef glUniform4iv_type glUniform4iv

cdef void check_glUniform4iv(GLint  location, GLsizei  count, const GLint * value) nogil:
    real_glUniform4iv(location, count, value)
    check_error("glUniform4iv")

cdef glUniformMatrix2fv_type real_glUniformMatrix2fv
cdef glUniformMatrix2fv_type glUniformMatrix2fv

cdef void check_glUniformMatrix2fv(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil:
    real_glUniformMatrix2fv(location, count, transpose, value)
    check_error("glUniformMatrix2fv")

cdef glUniformMatrix3fv_type real_glUniformMatrix3fv
cdef glUniformMatrix3fv_type glUniformMatrix3fv

cdef void check_glUniformMatrix3fv(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil:
    real_glUniformMatrix3fv(location, count, transpose, value)
    check_error("glUniformMatrix3fv")

cdef glUniformMatrix4fv_type real_glUniformMatrix4fv
cdef glUniformMatrix4fv_type glUniformMatrix4fv

cdef void check_glUniformMatrix4fv(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil:
    real_glUniformMatrix4fv(location, count, transpose, value)
    check_error("glUniformMatrix4fv")

cdef glUseProgram_type real_glUseProgram
cdef glUseProgram_type glUseProgram

cdef void check_glUseProgram(GLuint  program) nogil:
    real_glUseProgram(program)
    check_error("glUseProgram")

cdef glValidateProgram_type real_glValidateProgram
cdef glValidateProgram_type glValidateProgram

cdef void check_glValidateProgram(GLuint  program) nogil:
    real_glValidateProgram(program)
    check_error("glValidateProgram")

cdef glVertexAttrib1f_type real_glVertexAttrib1f
cdef glVertexAttrib1f_type glVertexAttrib1f

cdef void check_glVertexAttrib1f(GLuint  index, GLfloat  x) nogil:
    real_glVertexAttrib1f(index, x)
    check_error("glVertexAttrib1f")

cdef glVertexAttrib1fv_type real_glVertexAttrib1fv
cdef glVertexAttrib1fv_type glVertexAttrib1fv

cdef void check_glVertexAttrib1fv(GLuint  index, const GLfloat * v) nogil:
    real_glVertexAttrib1fv(index, v)
    check_error("glVertexAttrib1fv")

cdef glVertexAttrib2f_type real_glVertexAttrib2f
cdef glVertexAttrib2f_type glVertexAttrib2f

cdef void check_glVertexAttrib2f(GLuint  index, GLfloat  x, GLfloat  y) nogil:
    real_glVertexAttrib2f(index, x, y)
    check_error("glVertexAttrib2f")

cdef glVertexAttrib2fv_type real_glVertexAttrib2fv
cdef glVertexAttrib2fv_type glVertexAttrib2fv

cdef void check_glVertexAttrib2fv(GLuint  index, const GLfloat * v) nogil:
    real_glVertexAttrib2fv(index, v)
    check_error("glVertexAttrib2fv")

cdef glVertexAttrib3f_type real_glVertexAttrib3f
cdef glVertexAttrib3f_type glVertexAttrib3f

cdef void check_glVertexAttrib3f(GLuint  index, GLfloat  x, GLfloat  y, GLfloat  z) nogil:
    real_glVertexAttrib3f(index, x, y, z)
    check_error("glVertexAttrib3f")

cdef glVertexAttrib3fv_type real_glVertexAttrib3fv
cdef glVertexAttrib3fv_type glVertexAttrib3fv

cdef void check_glVertexAttrib3fv(GLuint  index, const GLfloat * v) nogil:
    real_glVertexAttrib3fv(index, v)
    check_error("glVertexAttrib3fv")

cdef glVertexAttrib4f_type real_glVertexAttrib4f
cdef glVertexAttrib4f_type glVertexAttrib4f

cdef void check_glVertexAttrib4f(GLuint  index, GLfloat  x, GLfloat  y, GLfloat  z, GLfloat  w) nogil:
    real_glVertexAttrib4f(index, x, y, z, w)
    check_error("glVertexAttrib4f")

cdef glVertexAttrib4fv_type real_glVertexAttrib4fv
cdef glVertexAttrib4fv_type glVertexAttrib4fv

cdef void check_glVertexAttrib4fv(GLuint  index, const GLfloat * v) nogil:
    real_glVertexAttrib4fv(index, v)
    check_error("glVertexAttrib4fv")

cdef glVertexAttribPointer_type real_glVertexAttribPointer
cdef glVertexAttribPointer_type glVertexAttribPointer

cdef void check_glVertexAttribPointer(GLuint  index, GLint  size, GLenum  type, GLboolean  normalized, GLsizei  stride, const void * pointer) nogil:
    real_glVertexAttribPointer(index, size, type, normalized, stride, pointer)
    check_error("glVertexAttribPointer")

cdef glViewport_type real_glViewport
cdef glViewport_type glViewport

cdef void check_glViewport(GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil:
    real_glViewport(x, y, width, height)
    check_error("glViewport")

def load():

    global real_glActiveTexture, glActiveTexture
    real_glActiveTexture = <glActiveTexture_type> find_gl_command([b'glActiveTexture', b'glActiveTextureARB'])
    glActiveTexture = real_glActiveTexture

    global real_glAttachShader, glAttachShader
    real_glAttachShader = <glAttachShader_type> find_gl_command([b'glAttachShader'])
    glAttachShader = real_glAttachShader

    global real_glBindAttribLocation, glBindAttribLocation
    real_glBindAttribLocation = <glBindAttribLocation_type> find_gl_command([b'glBindAttribLocation', b'glBindAttribLocationARB'])
    glBindAttribLocation = real_glBindAttribLocation

    global real_glBindBuffer, glBindBuffer
    real_glBindBuffer = <glBindBuffer_type> find_gl_command([b'glBindBuffer', b'glBindBufferARB'])
    glBindBuffer = real_glBindBuffer

    global real_glBindFramebuffer, glBindFramebuffer
    real_glBindFramebuffer = <glBindFramebuffer_type> find_gl_command([b'glBindFramebuffer'])
    glBindFramebuffer = real_glBindFramebuffer

    global real_glBindRenderbuffer, glBindRenderbuffer
    real_glBindRenderbuffer = <glBindRenderbuffer_type> find_gl_command([b'glBindRenderbuffer'])
    glBindRenderbuffer = real_glBindRenderbuffer

    global real_glBindTexture, glBindTexture
    real_glBindTexture = <glBindTexture_type> find_gl_command([b'glBindTexture', b'glBindTextureEXT'])
    glBindTexture = real_glBindTexture

    global real_glBlendColor, glBlendColor
    real_glBlendColor = <glBlendColor_type> find_gl_command([b'glBlendColor', b'glBlendColorEXT'])
    glBlendColor = real_glBlendColor

    global real_glBlendEquation, glBlendEquation
    real_glBlendEquation = <glBlendEquation_type> find_gl_command([b'glBlendEquation', b'glBlendEquationEXT'])
    glBlendEquation = real_glBlendEquation

    global real_glBlendEquationSeparate, glBlendEquationSeparate
    real_glBlendEquationSeparate = <glBlendEquationSeparate_type> find_gl_command([b'glBlendEquationSeparate', b'glBlendEquationSeparateEXT'])
    glBlendEquationSeparate = real_glBlendEquationSeparate

    global real_glBlendFunc, glBlendFunc
    real_glBlendFunc = <glBlendFunc_type> find_gl_command([b'glBlendFunc'])
    glBlendFunc = real_glBlendFunc

    global real_glBlendFuncSeparate, glBlendFuncSeparate
    real_glBlendFuncSeparate = <glBlendFuncSeparate_type> find_gl_command([b'glBlendFuncSeparate', b'glBlendFuncSeparateEXT', b'glBlendFuncSeparateINGR'])
    glBlendFuncSeparate = real_glBlendFuncSeparate

    global real_glBufferData, glBufferData
    real_glBufferData = <glBufferData_type> find_gl_command([b'glBufferData', b'glBufferDataARB'])
    glBufferData = real_glBufferData

    global real_glBufferSubData, glBufferSubData
    real_glBufferSubData = <glBufferSubData_type> find_gl_command([b'glBufferSubData', b'glBufferSubDataARB'])
    glBufferSubData = real_glBufferSubData

    global real_glCheckFramebufferStatus, glCheckFramebufferStatus
    real_glCheckFramebufferStatus = <glCheckFramebufferStatus_type> find_gl_command([b'glCheckFramebufferStatus', b'glCheckFramebufferStatusEXT'])
    glCheckFramebufferStatus = real_glCheckFramebufferStatus

    global real_glClear, glClear
    real_glClear = <glClear_type> find_gl_command([b'glClear'])
    glClear = real_glClear

    global real_glClearColor, glClearColor
    real_glClearColor = <glClearColor_type> find_gl_command([b'glClearColor'])
    glClearColor = real_glClearColor

    global real_glClearStencil, glClearStencil
    real_glClearStencil = <glClearStencil_type> find_gl_command([b'glClearStencil'])
    glClearStencil = real_glClearStencil

    global real_glColorMask, glColorMask
    real_glColorMask = <glColorMask_type> find_gl_command([b'glColorMask'])
    glColorMask = real_glColorMask

    global real_glCompileShader, glCompileShader
    real_glCompileShader = <glCompileShader_type> find_gl_command([b'glCompileShader', b'glCompileShaderARB'])
    glCompileShader = real_glCompileShader

    global real_glCompressedTexImage2D, glCompressedTexImage2D
    real_glCompressedTexImage2D = <glCompressedTexImage2D_type> find_gl_command([b'glCompressedTexImage2D', b'glCompressedTexImage2DARB'])
    glCompressedTexImage2D = real_glCompressedTexImage2D

    global real_glCompressedTexSubImage2D, glCompressedTexSubImage2D
    real_glCompressedTexSubImage2D = <glCompressedTexSubImage2D_type> find_gl_command([b'glCompressedTexSubImage2D', b'glCompressedTexSubImage2DARB'])
    glCompressedTexSubImage2D = real_glCompressedTexSubImage2D

    global real_glCopyTexImage2D, glCopyTexImage2D
    real_glCopyTexImage2D = <glCopyTexImage2D_type> find_gl_command([b'glCopyTexImage2D', b'glCopyTexImage2DEXT'])
    glCopyTexImage2D = real_glCopyTexImage2D

    global real_glCopyTexSubImage2D, glCopyTexSubImage2D
    real_glCopyTexSubImage2D = <glCopyTexSubImage2D_type> find_gl_command([b'glCopyTexSubImage2D', b'glCopyTexSubImage2DEXT'])
    glCopyTexSubImage2D = real_glCopyTexSubImage2D

    global real_glCreateProgram, glCreateProgram
    real_glCreateProgram = <glCreateProgram_type> find_gl_command([b'glCreateProgram', b'glCreateProgramObjectARB'])
    glCreateProgram = real_glCreateProgram

    global real_glCreateShader, glCreateShader
    real_glCreateShader = <glCreateShader_type> find_gl_command([b'glCreateShader', b'glCreateShaderObjectARB'])
    glCreateShader = real_glCreateShader

    global real_glCullFace, glCullFace
    real_glCullFace = <glCullFace_type> find_gl_command([b'glCullFace'])
    glCullFace = real_glCullFace

    global real_glDeleteBuffers, glDeleteBuffers
    real_glDeleteBuffers = <glDeleteBuffers_type> find_gl_command([b'glDeleteBuffers', b'glDeleteBuffersARB'])
    glDeleteBuffers = real_glDeleteBuffers

    global real_glDeleteFramebuffers, glDeleteFramebuffers
    real_glDeleteFramebuffers = <glDeleteFramebuffers_type> find_gl_command([b'glDeleteFramebuffers', b'glDeleteFramebuffersEXT'])
    glDeleteFramebuffers = real_glDeleteFramebuffers

    global real_glDeleteProgram, glDeleteProgram
    real_glDeleteProgram = <glDeleteProgram_type> find_gl_command([b'glDeleteProgram'])
    glDeleteProgram = real_glDeleteProgram

    global real_glDeleteRenderbuffers, glDeleteRenderbuffers
    real_glDeleteRenderbuffers = <glDeleteRenderbuffers_type> find_gl_command([b'glDeleteRenderbuffers', b'glDeleteRenderbuffersEXT'])
    glDeleteRenderbuffers = real_glDeleteRenderbuffers

    global real_glDeleteShader, glDeleteShader
    real_glDeleteShader = <glDeleteShader_type> find_gl_command([b'glDeleteShader'])
    glDeleteShader = real_glDeleteShader

    global real_glDeleteTextures, glDeleteTextures
    real_glDeleteTextures = <glDeleteTextures_type> find_gl_command([b'glDeleteTextures'])
    glDeleteTextures = real_glDeleteTextures

    global real_glDepthFunc, glDepthFunc
    real_glDepthFunc = <glDepthFunc_type> find_gl_command([b'glDepthFunc'])
    glDepthFunc = real_glDepthFunc

    global real_glDepthMask, glDepthMask
    real_glDepthMask = <glDepthMask_type> find_gl_command([b'glDepthMask'])
    glDepthMask = real_glDepthMask

    global real_glDetachShader, glDetachShader
    real_glDetachShader = <glDetachShader_type> find_gl_command([b'glDetachShader'])
    glDetachShader = real_glDetachShader

    global real_glDisable, glDisable
    real_glDisable = <glDisable_type> find_gl_command([b'glDisable'])
    glDisable = real_glDisable

    global real_glDisableVertexAttribArray, glDisableVertexAttribArray
    real_glDisableVertexAttribArray = <glDisableVertexAttribArray_type> find_gl_command([b'glDisableVertexAttribArray', b'glDisableVertexAttribArrayARB'])
    glDisableVertexAttribArray = real_glDisableVertexAttribArray

    global real_glDrawArrays, glDrawArrays
    real_glDrawArrays = <glDrawArrays_type> find_gl_command([b'glDrawArrays', b'glDrawArraysEXT'])
    glDrawArrays = real_glDrawArrays

    global real_glDrawElements, glDrawElements
    real_glDrawElements = <glDrawElements_type> find_gl_command([b'glDrawElements'])
    glDrawElements = real_glDrawElements

    global real_glEnable, glEnable
    real_glEnable = <glEnable_type> find_gl_command([b'glEnable'])
    glEnable = real_glEnable

    global real_glEnableVertexAttribArray, glEnableVertexAttribArray
    real_glEnableVertexAttribArray = <glEnableVertexAttribArray_type> find_gl_command([b'glEnableVertexAttribArray', b'glEnableVertexAttribArrayARB'])
    glEnableVertexAttribArray = real_glEnableVertexAttribArray

    global real_glFinish, glFinish
    real_glFinish = <glFinish_type> find_gl_command([b'glFinish'])
    glFinish = real_glFinish

    global real_glFlush, glFlush
    real_glFlush = <glFlush_type> find_gl_command([b'glFlush'])
    glFlush = real_glFlush

    global real_glFramebufferRenderbuffer, glFramebufferRenderbuffer
    real_glFramebufferRenderbuffer = <glFramebufferRenderbuffer_type> find_gl_command([b'glFramebufferRenderbuffer', b'glFramebufferRenderbufferEXT'])
    glFramebufferRenderbuffer = real_glFramebufferRenderbuffer

    global real_glFramebufferTexture2D, glFramebufferTexture2D
    real_glFramebufferTexture2D = <glFramebufferTexture2D_type> find_gl_command([b'glFramebufferTexture2D', b'glFramebufferTexture2DEXT'])
    glFramebufferTexture2D = real_glFramebufferTexture2D

    global real_glFrontFace, glFrontFace
    real_glFrontFace = <glFrontFace_type> find_gl_command([b'glFrontFace'])
    glFrontFace = real_glFrontFace

    global real_glGenBuffers, glGenBuffers
    real_glGenBuffers = <glGenBuffers_type> find_gl_command([b'glGenBuffers', b'glGenBuffersARB'])
    glGenBuffers = real_glGenBuffers

    global real_glGenFramebuffers, glGenFramebuffers
    real_glGenFramebuffers = <glGenFramebuffers_type> find_gl_command([b'glGenFramebuffers', b'glGenFramebuffersEXT'])
    glGenFramebuffers = real_glGenFramebuffers

    global real_glGenRenderbuffers, glGenRenderbuffers
    real_glGenRenderbuffers = <glGenRenderbuffers_type> find_gl_command([b'glGenRenderbuffers', b'glGenRenderbuffersEXT'])
    glGenRenderbuffers = real_glGenRenderbuffers

    global real_glGenTextures, glGenTextures
    real_glGenTextures = <glGenTextures_type> find_gl_command([b'glGenTextures'])
    glGenTextures = real_glGenTextures

    global real_glGenerateMipmap, glGenerateMipmap
    real_glGenerateMipmap = <glGenerateMipmap_type> find_gl_command([b'glGenerateMipmap', b'glGenerateMipmapEXT'])
    glGenerateMipmap = real_glGenerateMipmap

    global real_glGetActiveAttrib, glGetActiveAttrib
    real_glGetActiveAttrib = <glGetActiveAttrib_type> find_gl_command([b'glGetActiveAttrib', b'glGetActiveAttribARB'])
    glGetActiveAttrib = real_glGetActiveAttrib

    global real_glGetActiveUniform, glGetActiveUniform
    real_glGetActiveUniform = <glGetActiveUniform_type> find_gl_command([b'glGetActiveUniform', b'glGetActiveUniformARB'])
    glGetActiveUniform = real_glGetActiveUniform

    global real_glGetAttachedShaders, glGetAttachedShaders
    real_glGetAttachedShaders = <glGetAttachedShaders_type> find_gl_command([b'glGetAttachedShaders'])
    glGetAttachedShaders = real_glGetAttachedShaders

    global real_glGetAttribLocation, glGetAttribLocation
    real_glGetAttribLocation = <glGetAttribLocation_type> find_gl_command([b'glGetAttribLocation', b'glGetAttribLocationARB'])
    glGetAttribLocation = real_glGetAttribLocation

    global real_glGetBooleanv, glGetBooleanv
    real_glGetBooleanv = <glGetBooleanv_type> find_gl_command([b'glGetBooleanv'])
    glGetBooleanv = real_glGetBooleanv

    global real_glGetBufferParameteriv, glGetBufferParameteriv
    real_glGetBufferParameteriv = <glGetBufferParameteriv_type> find_gl_command([b'glGetBufferParameteriv', b'glGetBufferParameterivARB'])
    glGetBufferParameteriv = real_glGetBufferParameteriv

    global real_glGetError, glGetError
    real_glGetError = <glGetError_type> find_gl_command([b'glGetError'])
    glGetError = real_glGetError

    global real_glGetFloatv, glGetFloatv
    real_glGetFloatv = <glGetFloatv_type> find_gl_command([b'glGetFloatv'])
    glGetFloatv = real_glGetFloatv

    global real_glGetFramebufferAttachmentParameteriv, glGetFramebufferAttachmentParameteriv
    real_glGetFramebufferAttachmentParameteriv = <glGetFramebufferAttachmentParameteriv_type> find_gl_command([b'glGetFramebufferAttachmentParameteriv', b'glGetFramebufferAttachmentParameterivEXT'])
    glGetFramebufferAttachmentParameteriv = real_glGetFramebufferAttachmentParameteriv

    global real_glGetIntegerv, glGetIntegerv
    real_glGetIntegerv = <glGetIntegerv_type> find_gl_command([b'glGetIntegerv'])
    glGetIntegerv = real_glGetIntegerv

    global real_glGetProgramInfoLog, glGetProgramInfoLog
    real_glGetProgramInfoLog = <glGetProgramInfoLog_type> find_gl_command([b'glGetProgramInfoLog'])
    glGetProgramInfoLog = real_glGetProgramInfoLog

    global real_glGetProgramiv, glGetProgramiv
    real_glGetProgramiv = <glGetProgramiv_type> find_gl_command([b'glGetProgramiv'])
    glGetProgramiv = real_glGetProgramiv

    global real_glGetRenderbufferParameteriv, glGetRenderbufferParameteriv
    real_glGetRenderbufferParameteriv = <glGetRenderbufferParameteriv_type> find_gl_command([b'glGetRenderbufferParameteriv', b'glGetRenderbufferParameterivEXT'])
    glGetRenderbufferParameteriv = real_glGetRenderbufferParameteriv

    global real_glGetShaderInfoLog, glGetShaderInfoLog
    real_glGetShaderInfoLog = <glGetShaderInfoLog_type> find_gl_command([b'glGetShaderInfoLog'])
    glGetShaderInfoLog = real_glGetShaderInfoLog

    global real_glGetShaderSource, glGetShaderSource
    real_glGetShaderSource = <glGetShaderSource_type> find_gl_command([b'glGetShaderSource', b'glGetShaderSourceARB'])
    glGetShaderSource = real_glGetShaderSource

    global real_glGetShaderiv, glGetShaderiv
    real_glGetShaderiv = <glGetShaderiv_type> find_gl_command([b'glGetShaderiv'])
    glGetShaderiv = real_glGetShaderiv

    global real_glGetString, glGetString
    real_glGetString = <glGetString_type> find_gl_command([b'glGetString'])
    glGetString = real_glGetString

    global real_glGetTexParameterfv, glGetTexParameterfv
    real_glGetTexParameterfv = <glGetTexParameterfv_type> find_gl_command([b'glGetTexParameterfv'])
    glGetTexParameterfv = real_glGetTexParameterfv

    global real_glGetTexParameteriv, glGetTexParameteriv
    real_glGetTexParameteriv = <glGetTexParameteriv_type> find_gl_command([b'glGetTexParameteriv'])
    glGetTexParameteriv = real_glGetTexParameteriv

    global real_glGetUniformLocation, glGetUniformLocation
    real_glGetUniformLocation = <glGetUniformLocation_type> find_gl_command([b'glGetUniformLocation', b'glGetUniformLocationARB'])
    glGetUniformLocation = real_glGetUniformLocation

    global real_glGetUniformfv, glGetUniformfv
    real_glGetUniformfv = <glGetUniformfv_type> find_gl_command([b'glGetUniformfv', b'glGetUniformfvARB'])
    glGetUniformfv = real_glGetUniformfv

    global real_glGetUniformiv, glGetUniformiv
    real_glGetUniformiv = <glGetUniformiv_type> find_gl_command([b'glGetUniformiv', b'glGetUniformivARB'])
    glGetUniformiv = real_glGetUniformiv

    global real_glGetVertexAttribPointerv, glGetVertexAttribPointerv
    real_glGetVertexAttribPointerv = <glGetVertexAttribPointerv_type> find_gl_command([b'glGetVertexAttribPointerv', b'glGetVertexAttribPointervARB', b'glGetVertexAttribPointervNV'])
    glGetVertexAttribPointerv = real_glGetVertexAttribPointerv

    global real_glGetVertexAttribfv, glGetVertexAttribfv
    real_glGetVertexAttribfv = <glGetVertexAttribfv_type> find_gl_command([b'glGetVertexAttribfv', b'glGetVertexAttribfvARB', b'glGetVertexAttribfvNV'])
    glGetVertexAttribfv = real_glGetVertexAttribfv

    global real_glGetVertexAttribiv, glGetVertexAttribiv
    real_glGetVertexAttribiv = <glGetVertexAttribiv_type> find_gl_command([b'glGetVertexAttribiv', b'glGetVertexAttribivARB', b'glGetVertexAttribivNV'])
    glGetVertexAttribiv = real_glGetVertexAttribiv

    global real_glHint, glHint
    real_glHint = <glHint_type> find_gl_command([b'glHint'])
    glHint = real_glHint

    global real_glIsBuffer, glIsBuffer
    real_glIsBuffer = <glIsBuffer_type> find_gl_command([b'glIsBuffer', b'glIsBufferARB'])
    glIsBuffer = real_glIsBuffer

    global real_glIsEnabled, glIsEnabled
    real_glIsEnabled = <glIsEnabled_type> find_gl_command([b'glIsEnabled'])
    glIsEnabled = real_glIsEnabled

    global real_glIsFramebuffer, glIsFramebuffer
    real_glIsFramebuffer = <glIsFramebuffer_type> find_gl_command([b'glIsFramebuffer', b'glIsFramebufferEXT'])
    glIsFramebuffer = real_glIsFramebuffer

    global real_glIsProgram, glIsProgram
    real_glIsProgram = <glIsProgram_type> find_gl_command([b'glIsProgram'])
    glIsProgram = real_glIsProgram

    global real_glIsRenderbuffer, glIsRenderbuffer
    real_glIsRenderbuffer = <glIsRenderbuffer_type> find_gl_command([b'glIsRenderbuffer', b'glIsRenderbufferEXT'])
    glIsRenderbuffer = real_glIsRenderbuffer

    global real_glIsShader, glIsShader
    real_glIsShader = <glIsShader_type> find_gl_command([b'glIsShader'])
    glIsShader = real_glIsShader

    global real_glIsTexture, glIsTexture
    real_glIsTexture = <glIsTexture_type> find_gl_command([b'glIsTexture'])
    glIsTexture = real_glIsTexture

    global real_glLineWidth, glLineWidth
    real_glLineWidth = <glLineWidth_type> find_gl_command([b'glLineWidth'])
    glLineWidth = real_glLineWidth

    global real_glLinkProgram, glLinkProgram
    real_glLinkProgram = <glLinkProgram_type> find_gl_command([b'glLinkProgram', b'glLinkProgramARB'])
    glLinkProgram = real_glLinkProgram

    global real_glPixelStorei, glPixelStorei
    real_glPixelStorei = <glPixelStorei_type> find_gl_command([b'glPixelStorei'])
    glPixelStorei = real_glPixelStorei

    global real_glPolygonOffset, glPolygonOffset
    real_glPolygonOffset = <glPolygonOffset_type> find_gl_command([b'glPolygonOffset'])
    glPolygonOffset = real_glPolygonOffset

    global real_glReadPixels, glReadPixels
    real_glReadPixels = <glReadPixels_type> find_gl_command([b'glReadPixels'])
    glReadPixels = real_glReadPixels

    global real_glRenderbufferStorage, glRenderbufferStorage
    real_glRenderbufferStorage = <glRenderbufferStorage_type> find_gl_command([b'glRenderbufferStorage', b'glRenderbufferStorageEXT'])
    glRenderbufferStorage = real_glRenderbufferStorage

    global real_glSampleCoverage, glSampleCoverage
    real_glSampleCoverage = <glSampleCoverage_type> find_gl_command([b'glSampleCoverage', b'glSampleCoverageARB'])
    glSampleCoverage = real_glSampleCoverage

    global real_glScissor, glScissor
    real_glScissor = <glScissor_type> find_gl_command([b'glScissor'])
    glScissor = real_glScissor

    global real_glShaderSource, glShaderSource
    real_glShaderSource = <glShaderSource_type> find_gl_command([b'glShaderSource', b'glShaderSourceARB'])
    glShaderSource = real_glShaderSource

    global real_glStencilFunc, glStencilFunc
    real_glStencilFunc = <glStencilFunc_type> find_gl_command([b'glStencilFunc'])
    glStencilFunc = real_glStencilFunc

    global real_glStencilFuncSeparate, glStencilFuncSeparate
    real_glStencilFuncSeparate = <glStencilFuncSeparate_type> find_gl_command([b'glStencilFuncSeparate'])
    glStencilFuncSeparate = real_glStencilFuncSeparate

    global real_glStencilMask, glStencilMask
    real_glStencilMask = <glStencilMask_type> find_gl_command([b'glStencilMask'])
    glStencilMask = real_glStencilMask

    global real_glStencilMaskSeparate, glStencilMaskSeparate
    real_glStencilMaskSeparate = <glStencilMaskSeparate_type> find_gl_command([b'glStencilMaskSeparate'])
    glStencilMaskSeparate = real_glStencilMaskSeparate

    global real_glStencilOp, glStencilOp
    real_glStencilOp = <glStencilOp_type> find_gl_command([b'glStencilOp'])
    glStencilOp = real_glStencilOp

    global real_glStencilOpSeparate, glStencilOpSeparate
    real_glStencilOpSeparate = <glStencilOpSeparate_type> find_gl_command([b'glStencilOpSeparate', b'glStencilOpSeparateATI'])
    glStencilOpSeparate = real_glStencilOpSeparate

    global real_glTexImage2D, glTexImage2D
    real_glTexImage2D = <glTexImage2D_type> find_gl_command([b'glTexImage2D'])
    glTexImage2D = real_glTexImage2D

    global real_glTexParameterf, glTexParameterf
    real_glTexParameterf = <glTexParameterf_type> find_gl_command([b'glTexParameterf'])
    glTexParameterf = real_glTexParameterf

    global real_glTexParameterfv, glTexParameterfv
    real_glTexParameterfv = <glTexParameterfv_type> find_gl_command([b'glTexParameterfv'])
    glTexParameterfv = real_glTexParameterfv

    global real_glTexParameteri, glTexParameteri
    real_glTexParameteri = <glTexParameteri_type> find_gl_command([b'glTexParameteri'])
    glTexParameteri = real_glTexParameteri

    global real_glTexParameteriv, glTexParameteriv
    real_glTexParameteriv = <glTexParameteriv_type> find_gl_command([b'glTexParameteriv'])
    glTexParameteriv = real_glTexParameteriv

    global real_glTexSubImage2D, glTexSubImage2D
    real_glTexSubImage2D = <glTexSubImage2D_type> find_gl_command([b'glTexSubImage2D', b'glTexSubImage2DEXT'])
    glTexSubImage2D = real_glTexSubImage2D

    global real_glUniform1f, glUniform1f
    real_glUniform1f = <glUniform1f_type> find_gl_command([b'glUniform1f', b'glUniform1fARB'])
    glUniform1f = real_glUniform1f

    global real_glUniform1fv, glUniform1fv
    real_glUniform1fv = <glUniform1fv_type> find_gl_command([b'glUniform1fv', b'glUniform1fvARB'])
    glUniform1fv = real_glUniform1fv

    global real_glUniform1i, glUniform1i
    real_glUniform1i = <glUniform1i_type> find_gl_command([b'glUniform1i', b'glUniform1iARB'])
    glUniform1i = real_glUniform1i

    global real_glUniform1iv, glUniform1iv
    real_glUniform1iv = <glUniform1iv_type> find_gl_command([b'glUniform1iv', b'glUniform1ivARB'])
    glUniform1iv = real_glUniform1iv

    global real_glUniform2f, glUniform2f
    real_glUniform2f = <glUniform2f_type> find_gl_command([b'glUniform2f', b'glUniform2fARB'])
    glUniform2f = real_glUniform2f

    global real_glUniform2fv, glUniform2fv
    real_glUniform2fv = <glUniform2fv_type> find_gl_command([b'glUniform2fv', b'glUniform2fvARB'])
    glUniform2fv = real_glUniform2fv

    global real_glUniform2i, glUniform2i
    real_glUniform2i = <glUniform2i_type> find_gl_command([b'glUniform2i', b'glUniform2iARB'])
    glUniform2i = real_glUniform2i

    global real_glUniform2iv, glUniform2iv
    real_glUniform2iv = <glUniform2iv_type> find_gl_command([b'glUniform2iv', b'glUniform2ivARB'])
    glUniform2iv = real_glUniform2iv

    global real_glUniform3f, glUniform3f
    real_glUniform3f = <glUniform3f_type> find_gl_command([b'glUniform3f', b'glUniform3fARB'])
    glUniform3f = real_glUniform3f

    global real_glUniform3fv, glUniform3fv
    real_glUniform3fv = <glUniform3fv_type> find_gl_command([b'glUniform3fv', b'glUniform3fvARB'])
    glUniform3fv = real_glUniform3fv

    global real_glUniform3i, glUniform3i
    real_glUniform3i = <glUniform3i_type> find_gl_command([b'glUniform3i', b'glUniform3iARB'])
    glUniform3i = real_glUniform3i

    global real_glUniform3iv, glUniform3iv
    real_glUniform3iv = <glUniform3iv_type> find_gl_command([b'glUniform3iv', b'glUniform3ivARB'])
    glUniform3iv = real_glUniform3iv

    global real_glUniform4f, glUniform4f
    real_glUniform4f = <glUniform4f_type> find_gl_command([b'glUniform4f', b'glUniform4fARB'])
    glUniform4f = real_glUniform4f

    global real_glUniform4fv, glUniform4fv
    real_glUniform4fv = <glUniform4fv_type> find_gl_command([b'glUniform4fv', b'glUniform4fvARB'])
    glUniform4fv = real_glUniform4fv

    global real_glUniform4i, glUniform4i
    real_glUniform4i = <glUniform4i_type> find_gl_command([b'glUniform4i', b'glUniform4iARB'])
    glUniform4i = real_glUniform4i

    global real_glUniform4iv, glUniform4iv
    real_glUniform4iv = <glUniform4iv_type> find_gl_command([b'glUniform4iv', b'glUniform4ivARB'])
    glUniform4iv = real_glUniform4iv

    global real_glUniformMatrix2fv, glUniformMatrix2fv
    real_glUniformMatrix2fv = <glUniformMatrix2fv_type> find_gl_command([b'glUniformMatrix2fv', b'glUniformMatrix2fvARB'])
    glUniformMatrix2fv = real_glUniformMatrix2fv

    global real_glUniformMatrix3fv, glUniformMatrix3fv
    real_glUniformMatrix3fv = <glUniformMatrix3fv_type> find_gl_command([b'glUniformMatrix3fv', b'glUniformMatrix3fvARB'])
    glUniformMatrix3fv = real_glUniformMatrix3fv

    global real_glUniformMatrix4fv, glUniformMatrix4fv
    real_glUniformMatrix4fv = <glUniformMatrix4fv_type> find_gl_command([b'glUniformMatrix4fv', b'glUniformMatrix4fvARB'])
    glUniformMatrix4fv = real_glUniformMatrix4fv

    global real_glUseProgram, glUseProgram
    real_glUseProgram = <glUseProgram_type> find_gl_command([b'glUseProgram', b'glUseProgramObjectARB'])
    glUseProgram = real_glUseProgram

    global real_glValidateProgram, glValidateProgram
    real_glValidateProgram = <glValidateProgram_type> find_gl_command([b'glValidateProgram', b'glValidateProgramARB'])
    glValidateProgram = real_glValidateProgram

    global real_glVertexAttrib1f, glVertexAttrib1f
    real_glVertexAttrib1f = <glVertexAttrib1f_type> find_gl_command([b'glVertexAttrib1f', b'glVertexAttrib1fARB', b'glVertexAttrib1fNV'])
    glVertexAttrib1f = real_glVertexAttrib1f

    global real_glVertexAttrib1fv, glVertexAttrib1fv
    real_glVertexAttrib1fv = <glVertexAttrib1fv_type> find_gl_command([b'glVertexAttrib1fv', b'glVertexAttrib1fvARB', b'glVertexAttrib1fvNV'])
    glVertexAttrib1fv = real_glVertexAttrib1fv

    global real_glVertexAttrib2f, glVertexAttrib2f
    real_glVertexAttrib2f = <glVertexAttrib2f_type> find_gl_command([b'glVertexAttrib2f', b'glVertexAttrib2fARB', b'glVertexAttrib2fNV'])
    glVertexAttrib2f = real_glVertexAttrib2f

    global real_glVertexAttrib2fv, glVertexAttrib2fv
    real_glVertexAttrib2fv = <glVertexAttrib2fv_type> find_gl_command([b'glVertexAttrib2fv', b'glVertexAttrib2fvARB', b'glVertexAttrib2fvNV'])
    glVertexAttrib2fv = real_glVertexAttrib2fv

    global real_glVertexAttrib3f, glVertexAttrib3f
    real_glVertexAttrib3f = <glVertexAttrib3f_type> find_gl_command([b'glVertexAttrib3f', b'glVertexAttrib3fARB', b'glVertexAttrib3fNV'])
    glVertexAttrib3f = real_glVertexAttrib3f

    global real_glVertexAttrib3fv, glVertexAttrib3fv
    real_glVertexAttrib3fv = <glVertexAttrib3fv_type> find_gl_command([b'glVertexAttrib3fv', b'glVertexAttrib3fvARB', b'glVertexAttrib3fvNV'])
    glVertexAttrib3fv = real_glVertexAttrib3fv

    global real_glVertexAttrib4f, glVertexAttrib4f
    real_glVertexAttrib4f = <glVertexAttrib4f_type> find_gl_command([b'glVertexAttrib4f', b'glVertexAttrib4fARB', b'glVertexAttrib4fNV'])
    glVertexAttrib4f = real_glVertexAttrib4f

    global real_glVertexAttrib4fv, glVertexAttrib4fv
    real_glVertexAttrib4fv = <glVertexAttrib4fv_type> find_gl_command([b'glVertexAttrib4fv', b'glVertexAttrib4fvARB', b'glVertexAttrib4fvNV'])
    glVertexAttrib4fv = real_glVertexAttrib4fv

    global real_glVertexAttribPointer, glVertexAttribPointer
    real_glVertexAttribPointer = <glVertexAttribPointer_type> find_gl_command([b'glVertexAttribPointer', b'glVertexAttribPointerARB'])
    glVertexAttribPointer = real_glVertexAttribPointer

    global real_glViewport, glViewport
    real_glViewport = <glViewport_type> find_gl_command([b'glViewport'])
    glViewport = real_glViewport

def enable_check_error():
    global glActiveTexture
    glActiveTexture = check_glActiveTexture
    global glAttachShader
    glAttachShader = check_glAttachShader
    global glBindAttribLocation
    glBindAttribLocation = check_glBindAttribLocation
    global glBindBuffer
    glBindBuffer = check_glBindBuffer
    global glBindFramebuffer
    glBindFramebuffer = check_glBindFramebuffer
    global glBindRenderbuffer
    glBindRenderbuffer = check_glBindRenderbuffer
    global glBindTexture
    glBindTexture = check_glBindTexture
    global glBlendColor
    glBlendColor = check_glBlendColor
    global glBlendEquation
    glBlendEquation = check_glBlendEquation
    global glBlendEquationSeparate
    glBlendEquationSeparate = check_glBlendEquationSeparate
    global glBlendFunc
    glBlendFunc = check_glBlendFunc
    global glBlendFuncSeparate
    glBlendFuncSeparate = check_glBlendFuncSeparate
    global glBufferData
    glBufferData = check_glBufferData
    global glBufferSubData
    glBufferSubData = check_glBufferSubData
    global glCheckFramebufferStatus
    glCheckFramebufferStatus = check_glCheckFramebufferStatus
    global glClear
    glClear = check_glClear
    global glClearColor
    glClearColor = check_glClearColor
    global glClearStencil
    glClearStencil = check_glClearStencil
    global glColorMask
    glColorMask = check_glColorMask
    global glCompileShader
    glCompileShader = check_glCompileShader
    global glCompressedTexImage2D
    glCompressedTexImage2D = check_glCompressedTexImage2D
    global glCompressedTexSubImage2D
    glCompressedTexSubImage2D = check_glCompressedTexSubImage2D
    global glCopyTexImage2D
    glCopyTexImage2D = check_glCopyTexImage2D
    global glCopyTexSubImage2D
    glCopyTexSubImage2D = check_glCopyTexSubImage2D
    global glCreateProgram
    glCreateProgram = check_glCreateProgram
    global glCreateShader
    glCreateShader = check_glCreateShader
    global glCullFace
    glCullFace = check_glCullFace
    global glDeleteBuffers
    glDeleteBuffers = check_glDeleteBuffers
    global glDeleteFramebuffers
    glDeleteFramebuffers = check_glDeleteFramebuffers
    global glDeleteProgram
    glDeleteProgram = check_glDeleteProgram
    global glDeleteRenderbuffers
    glDeleteRenderbuffers = check_glDeleteRenderbuffers
    global glDeleteShader
    glDeleteShader = check_glDeleteShader
    global glDeleteTextures
    glDeleteTextures = check_glDeleteTextures
    global glDepthFunc
    glDepthFunc = check_glDepthFunc
    global glDepthMask
    glDepthMask = check_glDepthMask
    global glDetachShader
    glDetachShader = check_glDetachShader
    global glDisable
    glDisable = check_glDisable
    global glDisableVertexAttribArray
    glDisableVertexAttribArray = check_glDisableVertexAttribArray
    global glDrawArrays
    glDrawArrays = check_glDrawArrays
    global glDrawElements
    glDrawElements = check_glDrawElements
    global glEnable
    glEnable = check_glEnable
    global glEnableVertexAttribArray
    glEnableVertexAttribArray = check_glEnableVertexAttribArray
    global glFinish
    glFinish = check_glFinish
    global glFlush
    glFlush = check_glFlush
    global glFramebufferRenderbuffer
    glFramebufferRenderbuffer = check_glFramebufferRenderbuffer
    global glFramebufferTexture2D
    glFramebufferTexture2D = check_glFramebufferTexture2D
    global glFrontFace
    glFrontFace = check_glFrontFace
    global glGenBuffers
    glGenBuffers = check_glGenBuffers
    global glGenFramebuffers
    glGenFramebuffers = check_glGenFramebuffers
    global glGenRenderbuffers
    glGenRenderbuffers = check_glGenRenderbuffers
    global glGenTextures
    glGenTextures = check_glGenTextures
    global glGenerateMipmap
    glGenerateMipmap = check_glGenerateMipmap
    global glGetActiveAttrib
    glGetActiveAttrib = check_glGetActiveAttrib
    global glGetActiveUniform
    glGetActiveUniform = check_glGetActiveUniform
    global glGetAttachedShaders
    glGetAttachedShaders = check_glGetAttachedShaders
    global glGetAttribLocation
    glGetAttribLocation = check_glGetAttribLocation
    global glGetBooleanv
    glGetBooleanv = check_glGetBooleanv
    global glGetBufferParameteriv
    glGetBufferParameteriv = check_glGetBufferParameteriv
    global glGetError
    glGetError = check_glGetError
    global glGetFloatv
    glGetFloatv = check_glGetFloatv
    global glGetFramebufferAttachmentParameteriv
    glGetFramebufferAttachmentParameteriv = check_glGetFramebufferAttachmentParameteriv
    global glGetIntegerv
    glGetIntegerv = check_glGetIntegerv
    global glGetProgramInfoLog
    glGetProgramInfoLog = check_glGetProgramInfoLog
    global glGetProgramiv
    glGetProgramiv = check_glGetProgramiv
    global glGetRenderbufferParameteriv
    glGetRenderbufferParameteriv = check_glGetRenderbufferParameteriv
    global glGetShaderInfoLog
    glGetShaderInfoLog = check_glGetShaderInfoLog
    global glGetShaderSource
    glGetShaderSource = check_glGetShaderSource
    global glGetShaderiv
    glGetShaderiv = check_glGetShaderiv
    global glGetString
    glGetString = check_glGetString
    global glGetTexParameterfv
    glGetTexParameterfv = check_glGetTexParameterfv
    global glGetTexParameteriv
    glGetTexParameteriv = check_glGetTexParameteriv
    global glGetUniformLocation
    glGetUniformLocation = check_glGetUniformLocation
    global glGetUniformfv
    glGetUniformfv = check_glGetUniformfv
    global glGetUniformiv
    glGetUniformiv = check_glGetUniformiv
    global glGetVertexAttribPointerv
    glGetVertexAttribPointerv = check_glGetVertexAttribPointerv
    global glGetVertexAttribfv
    glGetVertexAttribfv = check_glGetVertexAttribfv
    global glGetVertexAttribiv
    glGetVertexAttribiv = check_glGetVertexAttribiv
    global glHint
    glHint = check_glHint
    global glIsBuffer
    glIsBuffer = check_glIsBuffer
    global glIsEnabled
    glIsEnabled = check_glIsEnabled
    global glIsFramebuffer
    glIsFramebuffer = check_glIsFramebuffer
    global glIsProgram
    glIsProgram = check_glIsProgram
    global glIsRenderbuffer
    glIsRenderbuffer = check_glIsRenderbuffer
    global glIsShader
    glIsShader = check_glIsShader
    global glIsTexture
    glIsTexture = check_glIsTexture
    global glLineWidth
    glLineWidth = check_glLineWidth
    global glLinkProgram
    glLinkProgram = check_glLinkProgram
    global glPixelStorei
    glPixelStorei = check_glPixelStorei
    global glPolygonOffset
    glPolygonOffset = check_glPolygonOffset
    global glReadPixels
    glReadPixels = check_glReadPixels
    global glRenderbufferStorage
    glRenderbufferStorage = check_glRenderbufferStorage
    global glSampleCoverage
    glSampleCoverage = check_glSampleCoverage
    global glScissor
    glScissor = check_glScissor
    global glShaderSource
    glShaderSource = check_glShaderSource
    global glStencilFunc
    glStencilFunc = check_glStencilFunc
    global glStencilFuncSeparate
    glStencilFuncSeparate = check_glStencilFuncSeparate
    global glStencilMask
    glStencilMask = check_glStencilMask
    global glStencilMaskSeparate
    glStencilMaskSeparate = check_glStencilMaskSeparate
    global glStencilOp
    glStencilOp = check_glStencilOp
    global glStencilOpSeparate
    glStencilOpSeparate = check_glStencilOpSeparate
    global glTexImage2D
    glTexImage2D = check_glTexImage2D
    global glTexParameterf
    glTexParameterf = check_glTexParameterf
    global glTexParameterfv
    glTexParameterfv = check_glTexParameterfv
    global glTexParameteri
    glTexParameteri = check_glTexParameteri
    global glTexParameteriv
    glTexParameteriv = check_glTexParameteriv
    global glTexSubImage2D
    glTexSubImage2D = check_glTexSubImage2D
    global glUniform1f
    glUniform1f = check_glUniform1f
    global glUniform1fv
    glUniform1fv = check_glUniform1fv
    global glUniform1i
    glUniform1i = check_glUniform1i
    global glUniform1iv
    glUniform1iv = check_glUniform1iv
    global glUniform2f
    glUniform2f = check_glUniform2f
    global glUniform2fv
    glUniform2fv = check_glUniform2fv
    global glUniform2i
    glUniform2i = check_glUniform2i
    global glUniform2iv
    glUniform2iv = check_glUniform2iv
    global glUniform3f
    glUniform3f = check_glUniform3f
    global glUniform3fv
    glUniform3fv = check_glUniform3fv
    global glUniform3i
    glUniform3i = check_glUniform3i
    global glUniform3iv
    glUniform3iv = check_glUniform3iv
    global glUniform4f
    glUniform4f = check_glUniform4f
    global glUniform4fv
    glUniform4fv = check_glUniform4fv
    global glUniform4i
    glUniform4i = check_glUniform4i
    global glUniform4iv
    glUniform4iv = check_glUniform4iv
    global glUniformMatrix2fv
    glUniformMatrix2fv = check_glUniformMatrix2fv
    global glUniformMatrix3fv
    glUniformMatrix3fv = check_glUniformMatrix3fv
    global glUniformMatrix4fv
    glUniformMatrix4fv = check_glUniformMatrix4fv
    global glUseProgram
    glUseProgram = check_glUseProgram
    global glValidateProgram
    glValidateProgram = check_glValidateProgram
    global glVertexAttrib1f
    glVertexAttrib1f = check_glVertexAttrib1f
    global glVertexAttrib1fv
    glVertexAttrib1fv = check_glVertexAttrib1fv
    global glVertexAttrib2f
    glVertexAttrib2f = check_glVertexAttrib2f
    global glVertexAttrib2fv
    glVertexAttrib2fv = check_glVertexAttrib2fv
    global glVertexAttrib3f
    glVertexAttrib3f = check_glVertexAttrib3f
    global glVertexAttrib3fv
    glVertexAttrib3fv = check_glVertexAttrib3fv
    global glVertexAttrib4f
    glVertexAttrib4f = check_glVertexAttrib4f
    global glVertexAttrib4fv
    glVertexAttrib4fv = check_glVertexAttrib4fv
    global glVertexAttribPointer
    glVertexAttribPointer = check_glVertexAttribPointer
    global glViewport
    glViewport = check_glViewport
