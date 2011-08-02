/**
 * This takes care of abstracting between OpenGL and OpenGL ES, by
 * choosing the appropriate header file, and renaming various names
 * in the ES case.
 */
#ifndef GL_COMPAT_H
#define GL_COMPAT_H

// Environ is defined on windows, but our GL code uses it as an
// identifier. So get rid of it here.
#undef environ

#if defined ANDROID

#define RENPY_GLES_1

#elif defined ANGLE

#define RENPY_GLES_2

#else

#define RENPY_OPENGL

#endif


#if defined RENPY_GLES_1

#include <GLES/gl.h>
#include <GLES/glext.h>

#define glOrtho glOrthof

#define GL_SOURCE0_ALPHA GL_SRC0_ALPHA
#define GL_SOURCE1_ALPHA GL_SRC1_ALPHA
#define GL_SOURCE2_ALPHA GL_SRC2_ALPHA
#define GL_SOURCE0_RGB GL_SRC0_RGB
#define GL_SOURCE1_RGB GL_SRC1_RGB
#define GL_SOURCE2_RGB GL_SRC2_RGB

#define GL_FRAMEBUFFER_EXT GL_FRAMEBUFFER_OES
#define GL_COLOR_ATTACHMENT0_EXT GL_COLOR_ATTACHMENT0_OES
#define glBindFramebufferEXT glBindFramebufferOES
#define glFramebufferTexture2DEXT glFramebufferTexture2DOES
#define glGenFramebuffersEXT glGenFramebuffersOES
#define glDeleteFramebuffersEXT glDeleteFramebuffersOES
#define glCheckFramebufferStatusEXT glCheckFramebufferStatusOES

#define RENPY_THIRD_TEXTURE 0

#endif


#if defined RENPY_GLES_2

#include <EGL/egl.h>
#include <GLES2/gl2.h">

#define GL_FRAMEBUFFER_EXT GL_FRAMEBUFFER
#define GL_COLOR_ATTACHMENT0_EXT GL_COLOR_ATTACHMENT0
#define glBindFramebufferEXT glBindFramebuffer
#define glFramebufferTexture2DEXT glFramebufferTexture2D
#define glGenFramebuffersEXT glGenFramebuffers
#define glDeleteFramebuffersEXT glDeleteFramebuffers
#define glCheckFramebufferStatusEXT glCheckFramebufferStatus

#define GL_OBJECT_INFO_LOG_LENGTH_ARB GL_OBJECT_INFO_LOG_LENGTH
#define GL_OBJECT_COMPILE_STATUS_ARB GL_OBJECT_COMPILE_STATUS
#define GL_VERTEX_SHADER_ARB GL_VERTEX_SHADER
#define GL_FRAGMENT_SHADER_ARB GL_FRAGMENT_SHADER
#define GL_OBJECT_LINK_STATUS_ARB GL_OBJECT_LINK_STATUS

#define glGetObjectParameterivARB glGetObjectParameteriv
#define glGetInfoLogARB glGetInfoLog
#define glCreateShaderObjectARB glCreateShaderObject
#define glShaderSourceARB glShaderSource
#define glCompileShaderARB glCompileShader
#define glCreateProgramObjectARB glCreateProgramObject
#define glAttachObjectARB glAttachObject
#define glLinkProgramARB glLinkProgram
#define glUseProgramObjectARB glUseProgramObject
#define glDeleteObjectARB glDeleteObject
#define glGetAttribLocationARB glGetAttribLocation
#define glGetUniformLocationARB glGetUniformLocation
#define glUniformMatrix4fvARB glUnifomMatrix4fv
#define glUniform1iARB glUniform1i
#define glUniform1fARB glUniform1f
#define glUniform4fARB glUniform4f
#define glVertexAttribPointerARB glVertexAttribPointer
#define glEnableVertexAttribArrayARB glEnableVertexAttribArray
#define glDisableVertexAttribArrayARB glDisableVertexAttribArray

#define RENPY_THIRD_TEXTURE 1

#endif


#if defined RENPY_GLES_1 || defined RENPY_GLES_2

typedef GLfloat GLdouble;

#define glewInit() (1)
#define GLEW_OK (1)
#define glewGetErrorString(x) ("Unknown Error")
#define glewIsSupported(x) (1)
#define glClipPlane glClipPlanef

// This isn't defined on GL ES, but that's okay, since we'll disable
// screenshots on Android.
#define GL_PACK_ROW_LENGTH 0
#define glReadBuffer(x)

#define glClientActiveTextureARB glClientActiveTexture
#define glActiveTextureARB glActiveTexture

#endif


#if defined RENPY_OPENGL

#include <GL/glew.h>

// #define GL_RGB565_OES 0
#define RENPY_THIRD_TEXTURE 1

#endif

#endif // GL_COMPAT_H
