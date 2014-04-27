#include <stdio.h>
#include <SDL/SDL.h>
#include <SDL/SDL_syswm.h>
#include "EGL/egl.h"
#include "GLES2/gl2.h"
#include <bcm_host.h>

#include "eglsupport.h"

EGLDisplay display;
EGLSurface surface;
EGLConfig config;
EGLContext context;

int initialized = 0;

char error_message[100];

int egl_available() {
	printf("RPI egl.\n");
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

/* Sets up an OpenGL ES 2 context. Returnes NULL if it succeeds, or
 * an error message on failure.
 */
char *egl_init(int interval) {
    EGLint major, minor;
    EGLint num_config;

    static EGL_DISPMANX_WINDOW_T nativewindow;

    DISPMANX_ELEMENT_HANDLE_T dispman_element;
    DISPMANX_DISPLAY_HANDLE_T dispman_display;
    DISPMANX_UPDATE_HANDLE_T dispman_update;
    VC_RECT_T dst_rect;
    VC_RECT_T src_rect;

    printf("In egl init.\n");

    bcm_host_init();

    const EGLint attrs[] = {
         EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
         EGL_ALPHA_SIZE, 8,
         EGL_NONE
     };

    const EGLint context_attrs[] = {
        EGL_CONTEXT_CLIENT_VERSION, 2,
        EGL_NONE
    };

	display = eglGetDisplay(EGL_DEFAULT_DISPLAY);
	egl_check("getting display");

	eglInitialize(display, &major, &minor);
	egl_check("initializing EGL");

	eglBindAPI(EGL_OPENGL_ES_API);
	egl_check("binding OpenGL ES");

	eglChooseConfig(display, attrs, &config, 1, &num_config);
	egl_check("choosing EGL config");

	context = eglCreateContext(display, config, EGL_NO_CONTEXT, context_attrs);
	egl_check("creating EGL context");

	int display_width;
	int display_height;

	// You can hardcode the resolution here:
	display_width = 800;
	display_height = 600;

	printf("%d x %d\n", display_width, display_height);

	dst_rect.x = 0;
	dst_rect.y = 0;
	dst_rect.width = display_width;
	dst_rect.height = display_height;

	src_rect.x = 0;
	src_rect.y = 0;
	src_rect.width = display_width << 16;
	src_rect.height = display_height << 16;

	dispman_display = vc_dispmanx_display_open( 0 /* LCD */);
	dispman_update = vc_dispmanx_update_start( 0 );

	dispman_element = vc_dispmanx_element_add ( dispman_update, dispman_display,
	   0/*layer*/, &dst_rect, 0/*src*/,
	   &src_rect, DISPMANX_PROTECTION_NONE, 0 /*alpha*/, 0/*clamp*/, 0/*transform*/);

	nativewindow.element = dispman_element;
	nativewindow.width = display_width;
	nativewindow.height = display_height;
	vc_dispmanx_update_submit_sync( dispman_update );

//    if (! initialized) {


	surface = eglCreateWindowSurface(display, config, &nativewindow, NULL);
	egl_check("creating EGL surface");


//    } else if (window != wminfo.window) {
//
//    	eglDestroySurface(display, surface);
//    	egl_check("destroying existing EGL surface")
//
//    	surface = eglCreateWindowSurface(display, config, &nativeWindow, NULL);
//    	egl_check("creating EGL surface");
//    }

	eglMakeCurrent(display, surface, surface, context);
	egl_check("making EGL context current");

    eglSwapInterval(display, interval);
    egl_check("setting swap interval")

	initialized = 1;

	// window = wminfo.window;

    printf("Finished egl init.\n");

    glClearColor(0.15f, 0.25f, 0.35f, 1.0f);
    glClear( GL_COLOR_BUFFER_BIT );
    glClear( GL_DEPTH_BUFFER_BIT );

    egl_swap();

    glClearColor(0.15f, 0.25f, 0.35f, 1.0f);
    glClear( GL_COLOR_BUFFER_BIT );
    glClear( GL_DEPTH_BUFFER_BIT );

    egl_swap();

    return NULL;
}

void egl_swap() {
	eglSwapBuffers(display, surface);
}

void egl_quit() {
	// Does nothing at the moment.
}
