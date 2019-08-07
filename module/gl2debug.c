#include <SDL.h>
#include <SDL_opengl.h>
#include <SDL_opengl_glext.h>
#include <stdio.h>

#include "gl2debug.h"

static void APIENTRY gl2_debug_callback(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam) {
    printf("GL %s: 0x%x, 0x%x: %s\n", (type == GL_DEBUG_TYPE_ERROR ? "ERROR" : "     "), type, severity, message);
}

void gl2_enable_debug(void) {
    void APIENTRY (*debugMessageCallback)(GLDEBUGPROC callback, const void *userParam);
    void APIENTRY (*debugMessageControl)(GLenum source, GLenum type, GLenum severity, GLsizei count, const GLuint* ids, GLboolean enabled);
    void APIENTRY (*glEnable)(GLenum);

    debugMessageCallback = SDL_GL_GetProcAddress("glDebugMessageCallback");

    if (!debugMessageCallback) {
        debugMessageCallback = SDL_GL_GetProcAddress("glDebugMessageCallbackKHR");
    }

    if (debugMessageCallback == NULL) {
         printf("GL: Could not get glDebugMessageCallback\n");
         return;
    }

    debugMessageControl = SDL_GL_GetProcAddress("glDebugMessageControl");

    if (!debugMessageControl) {
        debugMessageControl = SDL_GL_GetProcAddress("glDebugMessageControlKHR");
    }

    if (debugMessageControl == NULL) {
         printf("GL: Could not get glDebugMessageControl\n");
         return;
    }

    glEnable = SDL_GL_GetProcAddress("glEnable");

    glEnable(GL_DEBUG_OUTPUT);
    debugMessageCallback(gl2_debug_callback, 0);
    debugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, NULL, 1);
}
+
