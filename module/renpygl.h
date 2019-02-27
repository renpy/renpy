#ifndef RENPY_GL_H
#define RENPY_GL_H

#include <SDL.h>

#if defined(__IPHONEOS__) || defined(__ANDROID__)

#include <SDL_opengles2.h>

#else

#include <SDL_opengl.h>

#endif

#undef environ

#endif
