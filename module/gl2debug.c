#include <SDL.h>
#include <SDL_opengl.h>
#include <SDL_opengl_glext.h>
#include <stdio.h>

static void APIENTRY gl2_debug_callback(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam) {
    printf("GL %s: 0x%x, 0x%x: %s\n", (type == GL_DEBUG_TYPE_ERROR ? "ERROR" : "     "), type, severity, message);
}

void gl2_enable_debug(void) {
    void APIENTRY (*debugMessageCallback)(GLDEBUGPROC callback, const void *userParam);

    printf("GL: Debugging enabled.\n");

    debugMessageCallback = SDL_GL_GetProcAddress("glDebugMessageCallback");

    if (!debugMessageCallback) {
        debugMessageCallback = SDL_GL_GetProcAddress("glDebugMessageCallbackKHR");
    }

    if (!debugMessageCallback) {
        debugMessageCallback = SDL_GL_GetProcAddress("glDebugMessageCallbackARB");
    }

    if (debugMessageCallback == NULL) {
         printf("GL: Could not get glDebugMessageCallback\n");
         return;
    }

    glEnable(GL_DEBUG_OUTPUT);
    debugMessageCallback(gl2_debug_callback, 0);
}
