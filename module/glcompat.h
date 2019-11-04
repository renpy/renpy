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

#if defined __APPLE__
#include "TargetConditionals.h"
#if TARGET_OS_IPHONE
#define IOS
#endif
#endif

#if defined ANDROID

	#define RENPY_GLES_2

#elif defined ANGLE

	#define RENPY_GLES_2

#elif defined IOS

	#define RENPY_GLES_2

#elif defined EMSCRIPTEN

	#define RENPY_GLES_2

#elif defined RASPBERRY_PI

    #define RENPY_GLES_2

#else

	#define RENPY_OPENGL

#endif


#if defined RENPY_GLES_2

#ifdef ANGLE
#include <EGL/egl.h>
#endif

#ifdef IOS
#include <OpenGLES/ES2/gl.h>
#else
#include <GLES2/gl2.h>
#endif

typedef GLuint GLhandleARB;
typedef GLchar GLcharARB;

#define GL_MAX_TEXTURE_UNITS GL_MAX_TEXTURE_IMAGE_UNITS

#define GL_RENDERBUFFER_EXT GL_RENDERBUFFER
#define glGenRenderbuffersEXT glGenRenderbuffers
#define glBindRenderbufferEXT glBindRenderbuffer
#define glRenderbufferStorageEXT glRenderbufferStorage
#define glDeleteRenderbuffersEXT glDeleteRenderbuffers

#define GL_FRAMEBUFFER_EXT GL_FRAMEBUFFER
#define GL_FRAMEBUFFER_BINDING_EXT GL_FRAMEBUFFER_BINDING
#define GL_COLOR_ATTACHMENT0_EXT GL_COLOR_ATTACHMENT0
#define glBindFramebufferEXT glBindFramebuffer
#define glFramebufferTexture2DEXT glFramebufferTexture2D
#define glGenFramebuffersEXT glGenFramebuffers
#define glDeleteFramebuffersEXT glDeleteFramebuffers
#define glCheckFramebufferStatusEXT glCheckFramebufferStatus
#define glFramebufferRenderbufferEXT glFramebufferRenderbuffer

#define GL_OBJECT_INFO_LOG_LENGTH_ARB GL_INFO_LOG_LENGTH
#define GL_OBJECT_COMPILE_STATUS_ARB GL_COMPILE_STATUS
#define GL_VERTEX_SHADER_ARB GL_VERTEX_SHADER
#define GL_FRAGMENT_SHADER_ARB GL_FRAGMENT_SHADER
#define GL_OBJECT_LINK_STATUS_ARB GL_LINK_STATUS

#define glCreateShaderObjectARB glCreateShader
#define glShaderSourceARB glShaderSource
#define glCompileShaderARB glCompileShader
#define glCreateProgramObjectARB glCreateProgram
#define glAttachObjectARB glAttachShader
#define glLinkProgramARB glLinkProgram
#define glUseProgramObjectARB glUseProgram
#define glGetAttribLocationARB glGetAttribLocation
#define glGetUniformLocationARB glGetUniformLocation
#define glUniformMatrix4fvARB glUniformMatrix4fv
#define glUniform1iARB glUniform1i
#define glUniform1fARB glUniform1f
#define glUniform2fARB glUniform2f
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
// screenshots on Android/iOS.
#define GL_PACK_ROW_LENGTH 0

#define glClientActiveTextureARB glClientActiveTexture
#define glActiveTextureARB glActiveTexture

#define GL_BGRA GL_RGBA
#define GL_UNSIGNED_INT_8_8_8_8_REV GL_UNSIGNED_BYTE
#define GL_MAX_TEXTURE_UNITS GL_MAX_TEXTURE_IMAGE_UNITS

#endif


#if defined RENPY_OPENGL

#include <GL/glew.h>

#define RENPY_THIRD_TEXTURE 1

// These have to be written 2.0-style, since the ARB-style doesn't
// include the object type.
#undef GL_INFO_LOG_LENGTH
#define GL_INFO_LOG_LENGTH GL_OBJECT_INFO_LOG_LENGTH_ARB
#undef glDeleteShader
#define glDeleteShader glDeleteObjectARB
#undef glDeleteProgram
#define glDeleteProgram glDeleteObjectARB
#undef glGetShaderiv
#define glGetShaderiv glGetObjectParameterivARB
#undef glGetProgramiv
#define glGetProgramiv glGetObjectParameterivARB
#undef glGetShaderInfoLog
#define glGetShaderInfoLog glGetInfoLogARB
#undef glGetProgramInfoLog
#define glGetProgramInfoLog glGetInfoLogARB

#endif

#endif // GL_COMPAT_H
