from sdl2 cimport SDL_GL_GetProcAddress

found_functions = set()

cdef void *find_gl_command(names):

    cdef void *rv = NULL

    for i in names:
        rv = SDL_GL_GetProcAddress(i)

        if rv != NULL:
            found_functions.add(names[0].decode("utf-8"))
            return rv


    return NULL

def clear_missing_functions():
    global found_functions
    found_functions = set()

def check_missing_functions(required):
    import renpy

    required = set(required)

    missing_required = list(required - found_functions)
    missing_required.sort()

    if missing_required:

        renpy.display.log.write("The following gl functions are missing:")
        for i in missing_required:
            renpy.display.log.write("- %s", i)

        return True
    else:
        return False



cdef glActiveTexture_type glActiveTexture


cdef glAttachShader_type glAttachShader


cdef glBeginQuery_type glBeginQuery


cdef glBeginTransformFeedback_type glBeginTransformFeedback


cdef glBindAttribLocation_type glBindAttribLocation


cdef glBindBuffer_type glBindBuffer


cdef glBindBufferBase_type glBindBufferBase


cdef glBindBufferRange_type glBindBufferRange


cdef glBindFramebuffer_type glBindFramebuffer


cdef glBindRenderbuffer_type glBindRenderbuffer


cdef glBindTexture_type glBindTexture


cdef glBindVertexArray_type glBindVertexArray


cdef glBlendColor_type glBlendColor


cdef glBlendEquation_type glBlendEquation


cdef glBlendEquationSeparate_type glBlendEquationSeparate


cdef glBlendFunc_type glBlendFunc


cdef glBlendFuncSeparate_type glBlendFuncSeparate


cdef glBlitFramebuffer_type glBlitFramebuffer


cdef glBufferData_type glBufferData


cdef glBufferSubData_type glBufferSubData


cdef glCheckFramebufferStatus_type glCheckFramebufferStatus


cdef glClear_type glClear


cdef glClearBufferfi_type glClearBufferfi


cdef glClearBufferfv_type glClearBufferfv


cdef glClearBufferiv_type glClearBufferiv


cdef glClearBufferuiv_type glClearBufferuiv


cdef glClearColor_type glClearColor


cdef glClearStencil_type glClearStencil


cdef glColorMask_type glColorMask


cdef glCompileShader_type glCompileShader


cdef glCompressedTexImage2D_type glCompressedTexImage2D


cdef glCompressedTexImage3D_type glCompressedTexImage3D


cdef glCompressedTexSubImage2D_type glCompressedTexSubImage2D


cdef glCompressedTexSubImage3D_type glCompressedTexSubImage3D


cdef glCopyTexImage2D_type glCopyTexImage2D


cdef glCopyTexSubImage2D_type glCopyTexSubImage2D


cdef glCopyTexSubImage3D_type glCopyTexSubImage3D


cdef glCreateProgram_type glCreateProgram


cdef glCreateShader_type glCreateShader


cdef glCullFace_type glCullFace


cdef glDeleteBuffers_type glDeleteBuffers


cdef glDeleteFramebuffers_type glDeleteFramebuffers


cdef glDeleteProgram_type glDeleteProgram


cdef glDeleteQueries_type glDeleteQueries


cdef glDeleteRenderbuffers_type glDeleteRenderbuffers


cdef glDeleteShader_type glDeleteShader


cdef glDeleteTextures_type glDeleteTextures


cdef glDeleteVertexArrays_type glDeleteVertexArrays


cdef glDepthFunc_type glDepthFunc


cdef glDepthMask_type glDepthMask


cdef glDetachShader_type glDetachShader


cdef glDisable_type glDisable


cdef glDisableVertexAttribArray_type glDisableVertexAttribArray


cdef glDrawArrays_type glDrawArrays


cdef glDrawBuffers_type glDrawBuffers


cdef glDrawElements_type glDrawElements


cdef glDrawRangeElements_type glDrawRangeElements


cdef glEnable_type glEnable


cdef glEnableVertexAttribArray_type glEnableVertexAttribArray


cdef glEndQuery_type glEndQuery


cdef glEndTransformFeedback_type glEndTransformFeedback


cdef glFinish_type glFinish


cdef glFlush_type glFlush


cdef glFlushMappedBufferRange_type glFlushMappedBufferRange


cdef glFramebufferRenderbuffer_type glFramebufferRenderbuffer


cdef glFramebufferTexture2D_type glFramebufferTexture2D


cdef glFramebufferTextureLayer_type glFramebufferTextureLayer


cdef glFrontFace_type glFrontFace


cdef glGenBuffers_type glGenBuffers


cdef glGenFramebuffers_type glGenFramebuffers


cdef glGenQueries_type glGenQueries


cdef glGenRenderbuffers_type glGenRenderbuffers


cdef glGenTextures_type glGenTextures


cdef glGenVertexArrays_type glGenVertexArrays


cdef glGenerateMipmap_type glGenerateMipmap


cdef glGetActiveAttrib_type glGetActiveAttrib


cdef glGetActiveUniform_type glGetActiveUniform


cdef glGetAttachedShaders_type glGetAttachedShaders


cdef glGetAttribLocation_type glGetAttribLocation


cdef glGetBooleanv_type glGetBooleanv


cdef glGetBufferParameteriv_type glGetBufferParameteriv


cdef glGetBufferPointerv_type glGetBufferPointerv


cdef glGetError_type glGetError


cdef glGetFloatv_type glGetFloatv


cdef glGetFragDataLocation_type glGetFragDataLocation


cdef glGetFramebufferAttachmentParameteriv_type glGetFramebufferAttachmentParameteriv


cdef glGetIntegeri_v_type glGetIntegeri_v


cdef glGetIntegerv_type glGetIntegerv


cdef glGetProgramInfoLog_type glGetProgramInfoLog


cdef glGetProgramiv_type glGetProgramiv


cdef glGetQueryObjectuiv_type glGetQueryObjectuiv


cdef glGetQueryiv_type glGetQueryiv


cdef glGetRenderbufferParameteriv_type glGetRenderbufferParameteriv


cdef glGetShaderInfoLog_type glGetShaderInfoLog


cdef glGetShaderSource_type glGetShaderSource


cdef glGetShaderiv_type glGetShaderiv


cdef glGetString_type glGetString


cdef glGetStringi_type glGetStringi


cdef glGetTexParameterfv_type glGetTexParameterfv


cdef glGetTexParameteriv_type glGetTexParameteriv


cdef glGetTransformFeedbackVarying_type glGetTransformFeedbackVarying


cdef glGetUniformLocation_type glGetUniformLocation


cdef glGetUniformfv_type glGetUniformfv


cdef glGetUniformiv_type glGetUniformiv


cdef glGetUniformuiv_type glGetUniformuiv


cdef glGetVertexAttribIiv_type glGetVertexAttribIiv


cdef glGetVertexAttribIuiv_type glGetVertexAttribIuiv


cdef glGetVertexAttribPointerv_type glGetVertexAttribPointerv


cdef glGetVertexAttribfv_type glGetVertexAttribfv


cdef glGetVertexAttribiv_type glGetVertexAttribiv


cdef glHint_type glHint


cdef glIsBuffer_type glIsBuffer


cdef glIsEnabled_type glIsEnabled


cdef glIsFramebuffer_type glIsFramebuffer


cdef glIsProgram_type glIsProgram


cdef glIsQuery_type glIsQuery


cdef glIsRenderbuffer_type glIsRenderbuffer


cdef glIsShader_type glIsShader


cdef glIsTexture_type glIsTexture


cdef glIsVertexArray_type glIsVertexArray


cdef glLineWidth_type glLineWidth


cdef glLinkProgram_type glLinkProgram


cdef glMapBufferRange_type glMapBufferRange


cdef glPixelStorei_type glPixelStorei


cdef glPolygonOffset_type glPolygonOffset


cdef glReadBuffer_type glReadBuffer


cdef glReadPixels_type glReadPixels


cdef glRenderbufferStorage_type glRenderbufferStorage


cdef glRenderbufferStorageMultisample_type glRenderbufferStorageMultisample


cdef glSampleCoverage_type glSampleCoverage


cdef glScissor_type glScissor


cdef glShaderSource_type glShaderSource


cdef glStencilFunc_type glStencilFunc


cdef glStencilFuncSeparate_type glStencilFuncSeparate


cdef glStencilMask_type glStencilMask


cdef glStencilMaskSeparate_type glStencilMaskSeparate


cdef glStencilOp_type glStencilOp


cdef glStencilOpSeparate_type glStencilOpSeparate


cdef glTexImage2D_type glTexImage2D


cdef glTexImage3D_type glTexImage3D


cdef glTexParameterf_type glTexParameterf


cdef glTexParameterfv_type glTexParameterfv


cdef glTexParameteri_type glTexParameteri


cdef glTexParameteriv_type glTexParameteriv


cdef glTexSubImage2D_type glTexSubImage2D


cdef glTexSubImage3D_type glTexSubImage3D


cdef glTransformFeedbackVaryings_type glTransformFeedbackVaryings


cdef glUniform1f_type glUniform1f


cdef glUniform1fv_type glUniform1fv


cdef glUniform1i_type glUniform1i


cdef glUniform1iv_type glUniform1iv


cdef glUniform1ui_type glUniform1ui


cdef glUniform1uiv_type glUniform1uiv


cdef glUniform2f_type glUniform2f


cdef glUniform2fv_type glUniform2fv


cdef glUniform2i_type glUniform2i


cdef glUniform2iv_type glUniform2iv


cdef glUniform2ui_type glUniform2ui


cdef glUniform2uiv_type glUniform2uiv


cdef glUniform3f_type glUniform3f


cdef glUniform3fv_type glUniform3fv


cdef glUniform3i_type glUniform3i


cdef glUniform3iv_type glUniform3iv


cdef glUniform3ui_type glUniform3ui


cdef glUniform3uiv_type glUniform3uiv


cdef glUniform4f_type glUniform4f


cdef glUniform4fv_type glUniform4fv


cdef glUniform4i_type glUniform4i


cdef glUniform4iv_type glUniform4iv


cdef glUniform4ui_type glUniform4ui


cdef glUniform4uiv_type glUniform4uiv


cdef glUniformMatrix2fv_type glUniformMatrix2fv


cdef glUniformMatrix2x3fv_type glUniformMatrix2x3fv


cdef glUniformMatrix2x4fv_type glUniformMatrix2x4fv


cdef glUniformMatrix3fv_type glUniformMatrix3fv


cdef glUniformMatrix3x2fv_type glUniformMatrix3x2fv


cdef glUniformMatrix3x4fv_type glUniformMatrix3x4fv


cdef glUniformMatrix4fv_type glUniformMatrix4fv


cdef glUniformMatrix4x2fv_type glUniformMatrix4x2fv


cdef glUniformMatrix4x3fv_type glUniformMatrix4x3fv


cdef glUnmapBuffer_type glUnmapBuffer


cdef glUseProgram_type glUseProgram


cdef glValidateProgram_type glValidateProgram


cdef glVertexAttrib1f_type glVertexAttrib1f


cdef glVertexAttrib1fv_type glVertexAttrib1fv


cdef glVertexAttrib2f_type glVertexAttrib2f


cdef glVertexAttrib2fv_type glVertexAttrib2fv


cdef glVertexAttrib3f_type glVertexAttrib3f


cdef glVertexAttrib3fv_type glVertexAttrib3fv


cdef glVertexAttrib4f_type glVertexAttrib4f


cdef glVertexAttrib4fv_type glVertexAttrib4fv


cdef glVertexAttribI4i_type glVertexAttribI4i


cdef glVertexAttribI4iv_type glVertexAttribI4iv


cdef glVertexAttribI4ui_type glVertexAttribI4ui


cdef glVertexAttribI4uiv_type glVertexAttribI4uiv


cdef glVertexAttribIPointer_type glVertexAttribIPointer


cdef glVertexAttribPointer_type glVertexAttribPointer


cdef glViewport_type glViewport


def load():

    global glActiveTexture
    glActiveTexture = <glActiveTexture_type> find_gl_command([b'glActiveTexture', b'glActiveTextureARB'])

    global glAttachShader
    glAttachShader = <glAttachShader_type> find_gl_command([b'glAttachShader'])

    global glBeginQuery
    glBeginQuery = <glBeginQuery_type> find_gl_command([b'glBeginQuery', b'glBeginQueryARB'])

    global glBeginTransformFeedback
    glBeginTransformFeedback = <glBeginTransformFeedback_type> find_gl_command([b'glBeginTransformFeedback', b'glBeginTransformFeedbackEXT', b'glBeginTransformFeedbackNV'])

    global glBindAttribLocation
    glBindAttribLocation = <glBindAttribLocation_type> find_gl_command([b'glBindAttribLocation', b'glBindAttribLocationARB'])

    global glBindBuffer
    glBindBuffer = <glBindBuffer_type> find_gl_command([b'glBindBuffer', b'glBindBufferARB'])

    global glBindBufferBase
    glBindBufferBase = <glBindBufferBase_type> find_gl_command([b'glBindBufferBase', b'glBindBufferBaseEXT', b'glBindBufferBaseNV'])

    global glBindBufferRange
    glBindBufferRange = <glBindBufferRange_type> find_gl_command([b'glBindBufferRange', b'glBindBufferRangeEXT', b'glBindBufferRangeNV'])

    global glBindFramebuffer
    glBindFramebuffer = <glBindFramebuffer_type> find_gl_command([b'glBindFramebuffer'])

    global glBindRenderbuffer
    glBindRenderbuffer = <glBindRenderbuffer_type> find_gl_command([b'glBindRenderbuffer'])

    global glBindTexture
    glBindTexture = <glBindTexture_type> find_gl_command([b'glBindTexture', b'glBindTextureEXT'])

    global glBindVertexArray
    glBindVertexArray = <glBindVertexArray_type> find_gl_command([b'glBindVertexArray', b'glBindVertexArrayOES'])

    global glBlendColor
    glBlendColor = <glBlendColor_type> find_gl_command([b'glBlendColor', b'glBlendColorEXT'])

    global glBlendEquation
    glBlendEquation = <glBlendEquation_type> find_gl_command([b'glBlendEquation', b'glBlendEquationEXT'])

    global glBlendEquationSeparate
    glBlendEquationSeparate = <glBlendEquationSeparate_type> find_gl_command([b'glBlendEquationSeparate', b'glBlendEquationSeparateEXT'])

    global glBlendFunc
    glBlendFunc = <glBlendFunc_type> find_gl_command([b'glBlendFunc'])

    global glBlendFuncSeparate
    glBlendFuncSeparate = <glBlendFuncSeparate_type> find_gl_command([b'glBlendFuncSeparate', b'glBlendFuncSeparateEXT', b'glBlendFuncSeparateINGR'])

    global glBlitFramebuffer
    glBlitFramebuffer = <glBlitFramebuffer_type> find_gl_command([b'glBlitFramebuffer', b'glBlitFramebufferEXT', b'glBlitFramebufferNV'])

    global glBufferData
    glBufferData = <glBufferData_type> find_gl_command([b'glBufferData', b'glBufferDataARB'])

    global glBufferSubData
    glBufferSubData = <glBufferSubData_type> find_gl_command([b'glBufferSubData', b'glBufferSubDataARB'])

    global glCheckFramebufferStatus
    glCheckFramebufferStatus = <glCheckFramebufferStatus_type> find_gl_command([b'glCheckFramebufferStatus', b'glCheckFramebufferStatusEXT'])

    global glClear
    glClear = <glClear_type> find_gl_command([b'glClear'])

    global glClearBufferfi
    glClearBufferfi = <glClearBufferfi_type> find_gl_command([b'glClearBufferfi'])

    global glClearBufferfv
    glClearBufferfv = <glClearBufferfv_type> find_gl_command([b'glClearBufferfv'])

    global glClearBufferiv
    glClearBufferiv = <glClearBufferiv_type> find_gl_command([b'glClearBufferiv'])

    global glClearBufferuiv
    glClearBufferuiv = <glClearBufferuiv_type> find_gl_command([b'glClearBufferuiv'])

    global glClearColor
    glClearColor = <glClearColor_type> find_gl_command([b'glClearColor'])

    global glClearStencil
    glClearStencil = <glClearStencil_type> find_gl_command([b'glClearStencil'])

    global glColorMask
    glColorMask = <glColorMask_type> find_gl_command([b'glColorMask'])

    global glCompileShader
    glCompileShader = <glCompileShader_type> find_gl_command([b'glCompileShader', b'glCompileShaderARB'])

    global glCompressedTexImage2D
    glCompressedTexImage2D = <glCompressedTexImage2D_type> find_gl_command([b'glCompressedTexImage2D', b'glCompressedTexImage2DARB'])

    global glCompressedTexImage3D
    glCompressedTexImage3D = <glCompressedTexImage3D_type> find_gl_command([b'glCompressedTexImage3D', b'glCompressedTexImage3DARB'])

    global glCompressedTexSubImage2D
    glCompressedTexSubImage2D = <glCompressedTexSubImage2D_type> find_gl_command([b'glCompressedTexSubImage2D', b'glCompressedTexSubImage2DARB'])

    global glCompressedTexSubImage3D
    glCompressedTexSubImage3D = <glCompressedTexSubImage3D_type> find_gl_command([b'glCompressedTexSubImage3D', b'glCompressedTexSubImage3DARB'])

    global glCopyTexImage2D
    glCopyTexImage2D = <glCopyTexImage2D_type> find_gl_command([b'glCopyTexImage2D', b'glCopyTexImage2DEXT'])

    global glCopyTexSubImage2D
    glCopyTexSubImage2D = <glCopyTexSubImage2D_type> find_gl_command([b'glCopyTexSubImage2D', b'glCopyTexSubImage2DEXT'])

    global glCopyTexSubImage3D
    glCopyTexSubImage3D = <glCopyTexSubImage3D_type> find_gl_command([b'glCopyTexSubImage3D', b'glCopyTexSubImage3DEXT'])

    global glCreateProgram
    glCreateProgram = <glCreateProgram_type> find_gl_command([b'glCreateProgram', b'glCreateProgramObjectARB'])

    global glCreateShader
    glCreateShader = <glCreateShader_type> find_gl_command([b'glCreateShader', b'glCreateShaderObjectARB'])

    global glCullFace
    glCullFace = <glCullFace_type> find_gl_command([b'glCullFace'])

    global glDeleteBuffers
    glDeleteBuffers = <glDeleteBuffers_type> find_gl_command([b'glDeleteBuffers', b'glDeleteBuffersARB'])

    global glDeleteFramebuffers
    glDeleteFramebuffers = <glDeleteFramebuffers_type> find_gl_command([b'glDeleteFramebuffers', b'glDeleteFramebuffersEXT'])

    global glDeleteProgram
    glDeleteProgram = <glDeleteProgram_type> find_gl_command([b'glDeleteProgram'])

    global glDeleteQueries
    glDeleteQueries = <glDeleteQueries_type> find_gl_command([b'glDeleteQueries', b'glDeleteQueriesARB'])

    global glDeleteRenderbuffers
    glDeleteRenderbuffers = <glDeleteRenderbuffers_type> find_gl_command([b'glDeleteRenderbuffers', b'glDeleteRenderbuffersEXT'])

    global glDeleteShader
    glDeleteShader = <glDeleteShader_type> find_gl_command([b'glDeleteShader'])

    global glDeleteTextures
    glDeleteTextures = <glDeleteTextures_type> find_gl_command([b'glDeleteTextures'])

    global glDeleteVertexArrays
    glDeleteVertexArrays = <glDeleteVertexArrays_type> find_gl_command([b'glDeleteVertexArrays', b'glDeleteVertexArraysAPPLE', b'glDeleteVertexArraysOES'])

    global glDepthFunc
    glDepthFunc = <glDepthFunc_type> find_gl_command([b'glDepthFunc'])

    global glDepthMask
    glDepthMask = <glDepthMask_type> find_gl_command([b'glDepthMask'])

    global glDetachShader
    glDetachShader = <glDetachShader_type> find_gl_command([b'glDetachShader'])

    global glDisable
    glDisable = <glDisable_type> find_gl_command([b'glDisable'])

    global glDisableVertexAttribArray
    glDisableVertexAttribArray = <glDisableVertexAttribArray_type> find_gl_command([b'glDisableVertexAttribArray', b'glDisableVertexAttribArrayARB'])

    global glDrawArrays
    glDrawArrays = <glDrawArrays_type> find_gl_command([b'glDrawArrays', b'glDrawArraysEXT'])

    global glDrawBuffers
    glDrawBuffers = <glDrawBuffers_type> find_gl_command([b'glDrawBuffers', b'glDrawBuffersARB', b'glDrawBuffersATI', b'glDrawBuffersEXT'])

    global glDrawElements
    glDrawElements = <glDrawElements_type> find_gl_command([b'glDrawElements'])

    global glDrawRangeElements
    glDrawRangeElements = <glDrawRangeElements_type> find_gl_command([b'glDrawRangeElements', b'glDrawRangeElementsEXT'])

    global glEnable
    glEnable = <glEnable_type> find_gl_command([b'glEnable'])

    global glEnableVertexAttribArray
    glEnableVertexAttribArray = <glEnableVertexAttribArray_type> find_gl_command([b'glEnableVertexAttribArray', b'glEnableVertexAttribArrayARB'])

    global glEndQuery
    glEndQuery = <glEndQuery_type> find_gl_command([b'glEndQuery', b'glEndQueryARB'])

    global glEndTransformFeedback
    glEndTransformFeedback = <glEndTransformFeedback_type> find_gl_command([b'glEndTransformFeedback', b'glEndTransformFeedbackEXT', b'glEndTransformFeedbackNV'])

    global glFinish
    glFinish = <glFinish_type> find_gl_command([b'glFinish'])

    global glFlush
    glFlush = <glFlush_type> find_gl_command([b'glFlush'])

    global glFlushMappedBufferRange
    glFlushMappedBufferRange = <glFlushMappedBufferRange_type> find_gl_command([b'glFlushMappedBufferRange', b'glFlushMappedBufferRangeAPPLE', b'glFlushMappedBufferRangeEXT'])

    global glFramebufferRenderbuffer
    glFramebufferRenderbuffer = <glFramebufferRenderbuffer_type> find_gl_command([b'glFramebufferRenderbuffer', b'glFramebufferRenderbufferEXT'])

    global glFramebufferTexture2D
    glFramebufferTexture2D = <glFramebufferTexture2D_type> find_gl_command([b'glFramebufferTexture2D', b'glFramebufferTexture2DEXT'])

    global glFramebufferTextureLayer
    glFramebufferTextureLayer = <glFramebufferTextureLayer_type> find_gl_command([b'glFramebufferTextureLayer', b'glFramebufferTextureLayerARB', b'glFramebufferTextureLayerEXT'])

    global glFrontFace
    glFrontFace = <glFrontFace_type> find_gl_command([b'glFrontFace'])

    global glGenBuffers
    glGenBuffers = <glGenBuffers_type> find_gl_command([b'glGenBuffers', b'glGenBuffersARB'])

    global glGenFramebuffers
    glGenFramebuffers = <glGenFramebuffers_type> find_gl_command([b'glGenFramebuffers', b'glGenFramebuffersEXT'])

    global glGenQueries
    glGenQueries = <glGenQueries_type> find_gl_command([b'glGenQueries', b'glGenQueriesARB'])

    global glGenRenderbuffers
    glGenRenderbuffers = <glGenRenderbuffers_type> find_gl_command([b'glGenRenderbuffers', b'glGenRenderbuffersEXT'])

    global glGenTextures
    glGenTextures = <glGenTextures_type> find_gl_command([b'glGenTextures'])

    global glGenVertexArrays
    glGenVertexArrays = <glGenVertexArrays_type> find_gl_command([b'glGenVertexArrays', b'glGenVertexArraysAPPLE', b'glGenVertexArraysOES'])

    global glGenerateMipmap
    glGenerateMipmap = <glGenerateMipmap_type> find_gl_command([b'glGenerateMipmap', b'glGenerateMipmapEXT'])

    global glGetActiveAttrib
    glGetActiveAttrib = <glGetActiveAttrib_type> find_gl_command([b'glGetActiveAttrib', b'glGetActiveAttribARB'])

    global glGetActiveUniform
    glGetActiveUniform = <glGetActiveUniform_type> find_gl_command([b'glGetActiveUniform', b'glGetActiveUniformARB'])

    global glGetAttachedShaders
    glGetAttachedShaders = <glGetAttachedShaders_type> find_gl_command([b'glGetAttachedShaders'])

    global glGetAttribLocation
    glGetAttribLocation = <glGetAttribLocation_type> find_gl_command([b'glGetAttribLocation', b'glGetAttribLocationARB'])

    global glGetBooleanv
    glGetBooleanv = <glGetBooleanv_type> find_gl_command([b'glGetBooleanv'])

    global glGetBufferParameteriv
    glGetBufferParameteriv = <glGetBufferParameteriv_type> find_gl_command([b'glGetBufferParameteriv', b'glGetBufferParameterivARB'])

    global glGetBufferPointerv
    glGetBufferPointerv = <glGetBufferPointerv_type> find_gl_command([b'glGetBufferPointerv', b'glGetBufferPointervARB', b'glGetBufferPointervOES'])

    global glGetError
    glGetError = <glGetError_type> find_gl_command([b'glGetError'])

    global glGetFloatv
    glGetFloatv = <glGetFloatv_type> find_gl_command([b'glGetFloatv'])

    global glGetFragDataLocation
    glGetFragDataLocation = <glGetFragDataLocation_type> find_gl_command([b'glGetFragDataLocation', b'glGetFragDataLocationEXT'])

    global glGetFramebufferAttachmentParameteriv
    glGetFramebufferAttachmentParameteriv = <glGetFramebufferAttachmentParameteriv_type> find_gl_command([b'glGetFramebufferAttachmentParameteriv', b'glGetFramebufferAttachmentParameterivEXT'])

    global glGetIntegeri_v
    glGetIntegeri_v = <glGetIntegeri_v_type> find_gl_command([b'glGetIntegeri_v', b'glGetIntegerIndexedvEXT'])

    global glGetIntegerv
    glGetIntegerv = <glGetIntegerv_type> find_gl_command([b'glGetIntegerv'])

    global glGetProgramInfoLog
    glGetProgramInfoLog = <glGetProgramInfoLog_type> find_gl_command([b'glGetProgramInfoLog'])

    global glGetProgramiv
    glGetProgramiv = <glGetProgramiv_type> find_gl_command([b'glGetProgramiv'])

    global glGetQueryObjectuiv
    glGetQueryObjectuiv = <glGetQueryObjectuiv_type> find_gl_command([b'glGetQueryObjectuiv', b'glGetQueryObjectuivARB'])

    global glGetQueryiv
    glGetQueryiv = <glGetQueryiv_type> find_gl_command([b'glGetQueryiv', b'glGetQueryivARB'])

    global glGetRenderbufferParameteriv
    glGetRenderbufferParameteriv = <glGetRenderbufferParameteriv_type> find_gl_command([b'glGetRenderbufferParameteriv', b'glGetRenderbufferParameterivEXT'])

    global glGetShaderInfoLog
    glGetShaderInfoLog = <glGetShaderInfoLog_type> find_gl_command([b'glGetShaderInfoLog'])

    global glGetShaderSource
    glGetShaderSource = <glGetShaderSource_type> find_gl_command([b'glGetShaderSource', b'glGetShaderSourceARB'])

    global glGetShaderiv
    glGetShaderiv = <glGetShaderiv_type> find_gl_command([b'glGetShaderiv'])

    global glGetString
    glGetString = <glGetString_type> find_gl_command([b'glGetString'])

    global glGetStringi
    glGetStringi = <glGetStringi_type> find_gl_command([b'glGetStringi'])

    global glGetTexParameterfv
    glGetTexParameterfv = <glGetTexParameterfv_type> find_gl_command([b'glGetTexParameterfv'])

    global glGetTexParameteriv
    glGetTexParameteriv = <glGetTexParameteriv_type> find_gl_command([b'glGetTexParameteriv'])

    global glGetTransformFeedbackVarying
    glGetTransformFeedbackVarying = <glGetTransformFeedbackVarying_type> find_gl_command([b'glGetTransformFeedbackVarying', b'glGetTransformFeedbackVaryingEXT'])

    global glGetUniformLocation
    glGetUniformLocation = <glGetUniformLocation_type> find_gl_command([b'glGetUniformLocation', b'glGetUniformLocationARB'])

    global glGetUniformfv
    glGetUniformfv = <glGetUniformfv_type> find_gl_command([b'glGetUniformfv', b'glGetUniformfvARB'])

    global glGetUniformiv
    glGetUniformiv = <glGetUniformiv_type> find_gl_command([b'glGetUniformiv', b'glGetUniformivARB'])

    global glGetUniformuiv
    glGetUniformuiv = <glGetUniformuiv_type> find_gl_command([b'glGetUniformuiv', b'glGetUniformuivEXT'])

    global glGetVertexAttribIiv
    glGetVertexAttribIiv = <glGetVertexAttribIiv_type> find_gl_command([b'glGetVertexAttribIiv', b'glGetVertexAttribIivEXT'])

    global glGetVertexAttribIuiv
    glGetVertexAttribIuiv = <glGetVertexAttribIuiv_type> find_gl_command([b'glGetVertexAttribIuiv', b'glGetVertexAttribIuivEXT'])

    global glGetVertexAttribPointerv
    glGetVertexAttribPointerv = <glGetVertexAttribPointerv_type> find_gl_command([b'glGetVertexAttribPointerv', b'glGetVertexAttribPointervARB', b'glGetVertexAttribPointervNV'])

    global glGetVertexAttribfv
    glGetVertexAttribfv = <glGetVertexAttribfv_type> find_gl_command([b'glGetVertexAttribfv', b'glGetVertexAttribfvARB', b'glGetVertexAttribfvNV'])

    global glGetVertexAttribiv
    glGetVertexAttribiv = <glGetVertexAttribiv_type> find_gl_command([b'glGetVertexAttribiv', b'glGetVertexAttribivARB', b'glGetVertexAttribivNV'])

    global glHint
    glHint = <glHint_type> find_gl_command([b'glHint'])

    global glIsBuffer
    glIsBuffer = <glIsBuffer_type> find_gl_command([b'glIsBuffer', b'glIsBufferARB'])

    global glIsEnabled
    glIsEnabled = <glIsEnabled_type> find_gl_command([b'glIsEnabled'])

    global glIsFramebuffer
    glIsFramebuffer = <glIsFramebuffer_type> find_gl_command([b'glIsFramebuffer', b'glIsFramebufferEXT'])

    global glIsProgram
    glIsProgram = <glIsProgram_type> find_gl_command([b'glIsProgram'])

    global glIsQuery
    glIsQuery = <glIsQuery_type> find_gl_command([b'glIsQuery', b'glIsQueryARB'])

    global glIsRenderbuffer
    glIsRenderbuffer = <glIsRenderbuffer_type> find_gl_command([b'glIsRenderbuffer', b'glIsRenderbufferEXT'])

    global glIsShader
    glIsShader = <glIsShader_type> find_gl_command([b'glIsShader'])

    global glIsTexture
    glIsTexture = <glIsTexture_type> find_gl_command([b'glIsTexture'])

    global glIsVertexArray
    glIsVertexArray = <glIsVertexArray_type> find_gl_command([b'glIsVertexArray', b'glIsVertexArrayAPPLE', b'glIsVertexArrayOES'])

    global glLineWidth
    glLineWidth = <glLineWidth_type> find_gl_command([b'glLineWidth'])

    global glLinkProgram
    glLinkProgram = <glLinkProgram_type> find_gl_command([b'glLinkProgram', b'glLinkProgramARB'])

    global glMapBufferRange
    glMapBufferRange = <glMapBufferRange_type> find_gl_command([b'glMapBufferRange', b'glMapBufferRangeEXT'])

    global glPixelStorei
    glPixelStorei = <glPixelStorei_type> find_gl_command([b'glPixelStorei'])

    global glPolygonOffset
    glPolygonOffset = <glPolygonOffset_type> find_gl_command([b'glPolygonOffset'])

    global glReadBuffer
    glReadBuffer = <glReadBuffer_type> find_gl_command([b'glReadBuffer'])

    global glReadPixels
    glReadPixels = <glReadPixels_type> find_gl_command([b'glReadPixels'])

    global glRenderbufferStorage
    glRenderbufferStorage = <glRenderbufferStorage_type> find_gl_command([b'glRenderbufferStorage', b'glRenderbufferStorageEXT'])

    global glRenderbufferStorageMultisample
    glRenderbufferStorageMultisample = <glRenderbufferStorageMultisample_type> find_gl_command([b'glRenderbufferStorageMultisample', b'glRenderbufferStorageMultisampleEXT', b'glRenderbufferStorageMultisampleNV'])

    global glSampleCoverage
    glSampleCoverage = <glSampleCoverage_type> find_gl_command([b'glSampleCoverage', b'glSampleCoverageARB'])

    global glScissor
    glScissor = <glScissor_type> find_gl_command([b'glScissor'])

    global glShaderSource
    glShaderSource = <glShaderSource_type> find_gl_command([b'glShaderSource', b'glShaderSourceARB'])

    global glStencilFunc
    glStencilFunc = <glStencilFunc_type> find_gl_command([b'glStencilFunc'])

    global glStencilFuncSeparate
    glStencilFuncSeparate = <glStencilFuncSeparate_type> find_gl_command([b'glStencilFuncSeparate'])

    global glStencilMask
    glStencilMask = <glStencilMask_type> find_gl_command([b'glStencilMask'])

    global glStencilMaskSeparate
    glStencilMaskSeparate = <glStencilMaskSeparate_type> find_gl_command([b'glStencilMaskSeparate'])

    global glStencilOp
    glStencilOp = <glStencilOp_type> find_gl_command([b'glStencilOp'])

    global glStencilOpSeparate
    glStencilOpSeparate = <glStencilOpSeparate_type> find_gl_command([b'glStencilOpSeparate', b'glStencilOpSeparateATI'])

    global glTexImage2D
    glTexImage2D = <glTexImage2D_type> find_gl_command([b'glTexImage2D'])

    global glTexImage3D
    glTexImage3D = <glTexImage3D_type> find_gl_command([b'glTexImage3D', b'glTexImage3DEXT'])

    global glTexParameterf
    glTexParameterf = <glTexParameterf_type> find_gl_command([b'glTexParameterf'])

    global glTexParameterfv
    glTexParameterfv = <glTexParameterfv_type> find_gl_command([b'glTexParameterfv'])

    global glTexParameteri
    glTexParameteri = <glTexParameteri_type> find_gl_command([b'glTexParameteri'])

    global glTexParameteriv
    glTexParameteriv = <glTexParameteriv_type> find_gl_command([b'glTexParameteriv'])

    global glTexSubImage2D
    glTexSubImage2D = <glTexSubImage2D_type> find_gl_command([b'glTexSubImage2D', b'glTexSubImage2DEXT'])

    global glTexSubImage3D
    glTexSubImage3D = <glTexSubImage3D_type> find_gl_command([b'glTexSubImage3D', b'glTexSubImage3DEXT'])

    global glTransformFeedbackVaryings
    glTransformFeedbackVaryings = <glTransformFeedbackVaryings_type> find_gl_command([b'glTransformFeedbackVaryings', b'glTransformFeedbackVaryingsEXT'])

    global glUniform1f
    glUniform1f = <glUniform1f_type> find_gl_command([b'glUniform1f', b'glUniform1fARB'])

    global glUniform1fv
    glUniform1fv = <glUniform1fv_type> find_gl_command([b'glUniform1fv', b'glUniform1fvARB'])

    global glUniform1i
    glUniform1i = <glUniform1i_type> find_gl_command([b'glUniform1i', b'glUniform1iARB'])

    global glUniform1iv
    glUniform1iv = <glUniform1iv_type> find_gl_command([b'glUniform1iv', b'glUniform1ivARB'])

    global glUniform1ui
    glUniform1ui = <glUniform1ui_type> find_gl_command([b'glUniform1ui', b'glUniform1uiEXT'])

    global glUniform1uiv
    glUniform1uiv = <glUniform1uiv_type> find_gl_command([b'glUniform1uiv', b'glUniform1uivEXT'])

    global glUniform2f
    glUniform2f = <glUniform2f_type> find_gl_command([b'glUniform2f', b'glUniform2fARB'])

    global glUniform2fv
    glUniform2fv = <glUniform2fv_type> find_gl_command([b'glUniform2fv', b'glUniform2fvARB'])

    global glUniform2i
    glUniform2i = <glUniform2i_type> find_gl_command([b'glUniform2i', b'glUniform2iARB'])

    global glUniform2iv
    glUniform2iv = <glUniform2iv_type> find_gl_command([b'glUniform2iv', b'glUniform2ivARB'])

    global glUniform2ui
    glUniform2ui = <glUniform2ui_type> find_gl_command([b'glUniform2ui', b'glUniform2uiEXT'])

    global glUniform2uiv
    glUniform2uiv = <glUniform2uiv_type> find_gl_command([b'glUniform2uiv', b'glUniform2uivEXT'])

    global glUniform3f
    glUniform3f = <glUniform3f_type> find_gl_command([b'glUniform3f', b'glUniform3fARB'])

    global glUniform3fv
    glUniform3fv = <glUniform3fv_type> find_gl_command([b'glUniform3fv', b'glUniform3fvARB'])

    global glUniform3i
    glUniform3i = <glUniform3i_type> find_gl_command([b'glUniform3i', b'glUniform3iARB'])

    global glUniform3iv
    glUniform3iv = <glUniform3iv_type> find_gl_command([b'glUniform3iv', b'glUniform3ivARB'])

    global glUniform3ui
    glUniform3ui = <glUniform3ui_type> find_gl_command([b'glUniform3ui', b'glUniform3uiEXT'])

    global glUniform3uiv
    glUniform3uiv = <glUniform3uiv_type> find_gl_command([b'glUniform3uiv', b'glUniform3uivEXT'])

    global glUniform4f
    glUniform4f = <glUniform4f_type> find_gl_command([b'glUniform4f', b'glUniform4fARB'])

    global glUniform4fv
    glUniform4fv = <glUniform4fv_type> find_gl_command([b'glUniform4fv', b'glUniform4fvARB'])

    global glUniform4i
    glUniform4i = <glUniform4i_type> find_gl_command([b'glUniform4i', b'glUniform4iARB'])

    global glUniform4iv
    glUniform4iv = <glUniform4iv_type> find_gl_command([b'glUniform4iv', b'glUniform4ivARB'])

    global glUniform4ui
    glUniform4ui = <glUniform4ui_type> find_gl_command([b'glUniform4ui', b'glUniform4uiEXT'])

    global glUniform4uiv
    glUniform4uiv = <glUniform4uiv_type> find_gl_command([b'glUniform4uiv', b'glUniform4uivEXT'])

    global glUniformMatrix2fv
    glUniformMatrix2fv = <glUniformMatrix2fv_type> find_gl_command([b'glUniformMatrix2fv', b'glUniformMatrix2fvARB'])

    global glUniformMatrix2x3fv
    glUniformMatrix2x3fv = <glUniformMatrix2x3fv_type> find_gl_command([b'glUniformMatrix2x3fv', b'glUniformMatrix2x3fvNV'])

    global glUniformMatrix2x4fv
    glUniformMatrix2x4fv = <glUniformMatrix2x4fv_type> find_gl_command([b'glUniformMatrix2x4fv', b'glUniformMatrix2x4fvNV'])

    global glUniformMatrix3fv
    glUniformMatrix3fv = <glUniformMatrix3fv_type> find_gl_command([b'glUniformMatrix3fv', b'glUniformMatrix3fvARB'])

    global glUniformMatrix3x2fv
    glUniformMatrix3x2fv = <glUniformMatrix3x2fv_type> find_gl_command([b'glUniformMatrix3x2fv', b'glUniformMatrix3x2fvNV'])

    global glUniformMatrix3x4fv
    glUniformMatrix3x4fv = <glUniformMatrix3x4fv_type> find_gl_command([b'glUniformMatrix3x4fv', b'glUniformMatrix3x4fvNV'])

    global glUniformMatrix4fv
    glUniformMatrix4fv = <glUniformMatrix4fv_type> find_gl_command([b'glUniformMatrix4fv', b'glUniformMatrix4fvARB'])

    global glUniformMatrix4x2fv
    glUniformMatrix4x2fv = <glUniformMatrix4x2fv_type> find_gl_command([b'glUniformMatrix4x2fv', b'glUniformMatrix4x2fvNV'])

    global glUniformMatrix4x3fv
    glUniformMatrix4x3fv = <glUniformMatrix4x3fv_type> find_gl_command([b'glUniformMatrix4x3fv', b'glUniformMatrix4x3fvNV'])

    global glUnmapBuffer
    glUnmapBuffer = <glUnmapBuffer_type> find_gl_command([b'glUnmapBuffer', b'glUnmapBufferARB', b'glUnmapBufferOES'])

    global glUseProgram
    glUseProgram = <glUseProgram_type> find_gl_command([b'glUseProgram', b'glUseProgramObjectARB'])

    global glValidateProgram
    glValidateProgram = <glValidateProgram_type> find_gl_command([b'glValidateProgram', b'glValidateProgramARB'])

    global glVertexAttrib1f
    glVertexAttrib1f = <glVertexAttrib1f_type> find_gl_command([b'glVertexAttrib1f', b'glVertexAttrib1fARB', b'glVertexAttrib1fNV'])

    global glVertexAttrib1fv
    glVertexAttrib1fv = <glVertexAttrib1fv_type> find_gl_command([b'glVertexAttrib1fv', b'glVertexAttrib1fvARB', b'glVertexAttrib1fvNV'])

    global glVertexAttrib2f
    glVertexAttrib2f = <glVertexAttrib2f_type> find_gl_command([b'glVertexAttrib2f', b'glVertexAttrib2fARB', b'glVertexAttrib2fNV'])

    global glVertexAttrib2fv
    glVertexAttrib2fv = <glVertexAttrib2fv_type> find_gl_command([b'glVertexAttrib2fv', b'glVertexAttrib2fvARB', b'glVertexAttrib2fvNV'])

    global glVertexAttrib3f
    glVertexAttrib3f = <glVertexAttrib3f_type> find_gl_command([b'glVertexAttrib3f', b'glVertexAttrib3fARB', b'glVertexAttrib3fNV'])

    global glVertexAttrib3fv
    glVertexAttrib3fv = <glVertexAttrib3fv_type> find_gl_command([b'glVertexAttrib3fv', b'glVertexAttrib3fvARB', b'glVertexAttrib3fvNV'])

    global glVertexAttrib4f
    glVertexAttrib4f = <glVertexAttrib4f_type> find_gl_command([b'glVertexAttrib4f', b'glVertexAttrib4fARB', b'glVertexAttrib4fNV'])

    global glVertexAttrib4fv
    glVertexAttrib4fv = <glVertexAttrib4fv_type> find_gl_command([b'glVertexAttrib4fv', b'glVertexAttrib4fvARB', b'glVertexAttrib4fvNV'])

    global glVertexAttribI4i
    glVertexAttribI4i = <glVertexAttribI4i_type> find_gl_command([b'glVertexAttribI4i', b'glVertexAttribI4iEXT'])

    global glVertexAttribI4iv
    glVertexAttribI4iv = <glVertexAttribI4iv_type> find_gl_command([b'glVertexAttribI4iv', b'glVertexAttribI4ivEXT'])

    global glVertexAttribI4ui
    glVertexAttribI4ui = <glVertexAttribI4ui_type> find_gl_command([b'glVertexAttribI4ui', b'glVertexAttribI4uiEXT'])

    global glVertexAttribI4uiv
    glVertexAttribI4uiv = <glVertexAttribI4uiv_type> find_gl_command([b'glVertexAttribI4uiv', b'glVertexAttribI4uivEXT'])

    global glVertexAttribIPointer
    glVertexAttribIPointer = <glVertexAttribIPointer_type> find_gl_command([b'glVertexAttribIPointer', b'glVertexAttribIPointerEXT'])

    global glVertexAttribPointer
    glVertexAttribPointer = <glVertexAttribPointer_type> find_gl_command([b'glVertexAttribPointer', b'glVertexAttribPointerARB'])

    global glViewport
    glViewport = <glViewport_type> find_gl_command([b'glViewport'])
