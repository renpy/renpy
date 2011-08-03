#include <stdio.h>
#include <SDL/SDL.h>
#include <SDL/SDL_syswm.h>
#include "EGL/egl.h"
#include "GLES2/gl2.h"


EGLDisplay display;
EGLSurface surface;

char error_message[100];

// Checks for an EGL error. Returns an error string if there is one,
// or NULL otherwise.
char *egl_error(char *where) {
	EGLint error;

	error = eglGetError();

	if (error == EGL_SUCCESS) {
		return NULL;
	}

	snprintf(error_message, 100, "Error %s (egl error 0x%x)", where, error);
	return error_message;
}

#define egl_check(where) { char *rv = egl_error(where); if (rv) return rv; }

/* Sets up an OpenGL ES 2 context. Returnes NULL if it succeeds, or
 * an error message on failure.
 */
char *egl_init() {
    SDL_SysWMinfo wminfo;
    EGLint major, minor;
    EGLint num_config;
    EGLConfig config;
    EGLContext context;
    
    const EGLint attrs[] = {
         EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
         EGL_ALPHA_SIZE, 8,
         EGL_NONE
     };

    const EGLint context_attrs[] = {
        EGL_CONTEXT_CLIENT_VERSION, 2,
        EGL_NONE
    };
    
    SDL_VERSION(&wminfo.version);
    SDL_GetWMInfo(&wminfo);

    display = eglGetDisplay(GetDC(wminfo.window));

    eglInitialize(display, &major, &minor);
    egl_check("initializing EGL");

    eglBindAPI(EGL_OPENGL_ES_API);
	egl_check("binding OpenGL ES");
    
    eglChooseConfig(display, attrs, &config, 1, &num_config);
    egl_check("choosing EGL config");

    surface = eglCreateWindowSurface(display, config, wminfo.window, NULL);
    egl_check("creating EGL surface");

    context = eglCreateContext(display, config, EGL_NO_CONTEXT, context_attrs);
    egl_check("creating EGL context");

    eglMakeCurrent(display, surface, surface, context);
    egl_check("making EGL context current");

    return NULL;
}

void egl_swap() {
	eglSwapBuffers(display, surface);
}

void egl_quit() {
	eglTerminate(display);
}
