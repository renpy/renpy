#ifndef RENPY_GL_H
#define RENPY_H_H

/* This file exists to import OpenGL or OpenGL ES, as appropriate. */

#include <GL/gl.h>


/* These are temporarily here so we can import GLEW. */

GLenum glewInit();
GLubyte *glewGetErrorString(GLenum);
GLboolean glewIsSupported(char *);

#define GLEW_OK (0)

#endif
