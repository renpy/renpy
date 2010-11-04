/**
 * This takes care of abstracting between OpenGL and OpenGL ES, by
 * choosing the appropriate header file, and renaming various names
 * in the ES case.
 */
#ifndef GL_COMPAT_H
#define GL_COMPAT_H

#ifdef ANDROID
#include <GLES/gl.h>
typedef GLfloat GLdouble;
#define glewInit() (1)
#define GLEW_OK (1)
#define glOrtho glOrthof

// This isn't defined on GL ES, but that's okay, since we'll disable
// screenshots on Android.
#define GL_PACK_ROW_LENGTH 0

// TODO: Rid ourselves of this.
#define GL_BGRA GL_RGBA

#else
#include <GL/glew.h>
#endif

#endif
