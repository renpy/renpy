/**
 * This takes care of abstracting between OpenGL and OpenGL ES, by
 * choosing the appropriate header file, and renaming various names
 * in the ES case.
 */
#ifndef GL_COMPAT_H
#define GL_COMPAT_H

// Environ is defined on windows, but our GL code uses it as an
// identifier.
#undef environ



#ifdef ANDROID

#include <GLES/gl.h>
#include <GLES/glext.h>

typedef GLfloat GLdouble;
#define glewInit() (1)
#define GLEW_OK (1)
#define glewGetErrorString(x) ("Unknown Error")
#define glewIsSupported(x) (1)
#define glOrtho glOrthof
#define glClipPlane glClipPlanef

#define GL_SOURCE0_ALPHA GL_SRC0_ALPHA
#define GL_SOURCE1_ALPHA GL_SRC1_ALPHA
#define GL_SOURCE2_ALPHA GL_SRC2_ALPHA

#define GL_SOURCE0_RGB GL_SRC0_RGB
#define GL_SOURCE1_RGB GL_SRC1_RGB
#define GL_SOURCE2_RGB GL_SRC2_RGB

// This isn't defined on GL ES, but that's okay, since we'll disable
// screenshots on Android.
#define GL_PACK_ROW_LENGTH 0
#define glReadBuffer(x)

#define GL_FRAMEBUFFER_EXT GL_FRAMEBUFFER_OES
#define GL_COLOR_ATTACHMENT0_EXT GL_COLOR_ATTACHMENT0_OES
#define glBindFramebufferEXT glBindFramebufferOES
#define glFramebufferTexture2DEXT glFramebufferTexture2DOES
#define glGenFramebuffersEXT glGenFramebuffersOES
#define glDeleteFramebuffersEXT glDeleteFramebuffersOES
#define glCheckFramebufferStatusEXT glCheckFramebufferStatusOES

#define RENPY_THIRD_TEXTURE 0


#else
#include <GL/glew.h>

#undef glClientActiveTexture
#define glClientActiveTexture glClientActiveTextureARB

#undef glActiveTexture
#define glActiveTexture glActiveTextureARB

#define GL_RGB565_OES 0
#define RENPY_THIRD_TEXTURE 1

#endif

#endif
