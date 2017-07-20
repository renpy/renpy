#include <stdio.h>
#include <SDL.h>
#include <SDL_syswm.h>
#include "pygame_sdl2/pygame_sdl2.h"
#include "EGL/egl.h"
#include "GLES2/gl2.h"

#include "eglsupport.h"

HWND window;

EGLDisplay display;
EGLSurface surface;
EGLConfig config;
EGLContext context;

int imported_pygame = 0;
int initialized = 0;

char error_message[100];

int egl_available() {
	return 1;
}

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

/* Sets up an OpenGL ES 2 context. Returns NULL if it succeeds, or
 * an error message on failure.
 */
char *egl_init(SDL_Window *sdl_window, int interval) {
    SDL_SysWMinfo wminfo;
    EGLint major, minor;
    EGLint num_config;
    HWND new_window;

    const EGLint attrs[] = {
         EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
         EGL_ALPHA_SIZE, 8,
         EGL_NONE
     };

    const EGLint context_attrs[] = {
        EGL_CONTEXT_CLIENT_VERSION, 2,
        EGL_NONE
    };

    if (!imported_pygame) {
    	import_pygame_sdl2();
    	imported_pygame = 1;
    }

    SDL_VERSION(&wminfo.version);
    SDL_GetWindowWMInfo(sdl_window, &wminfo);

    new_window = wminfo.info.win.window;

    if (! initialized) {

    	display = eglGetDisplay(GetDC(new_window));
		egl_check("getting display");

		eglInitialize(display, &major, &minor);
		egl_check("initializing EGL");

		eglBindAPI(EGL_OPENGL_ES_API);
		egl_check("binding OpenGL ES");

		eglChooseConfig(display, attrs, &config, 1, &num_config);
		egl_check("choosing EGL config");

		context = eglCreateContext(display, config, EGL_NO_CONTEXT, context_attrs);
		egl_check("creating EGL context");

    	surface = eglCreateWindowSurface(display, config, new_window, NULL);
    	egl_check("creating EGL surface");


    } else if (window != wminfo.info.win.window) {

    	eglDestroySurface(display, surface);
    	egl_check("destroying existing EGL surface")

    	surface = eglCreateWindowSurface(display, config, new_window, NULL);
    	egl_check("creating EGL surface");

    }

	eglMakeCurrent(display, surface, surface, context);
	egl_check("making EGL context current");

    eglSwapInterval(display, interval);
    egl_check("setting swap interval")

	initialized = 1;
	window = new_window;

    return NULL;
}

void egl_swap() {
	eglSwapBuffers(display, surface);
}

void egl_quit() {
	// Does nothing at the moment.
}
