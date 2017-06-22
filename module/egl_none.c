#include <stdio.h>
#include "eglsupport.h"


int egl_available() {
	return 0;
}

// Checks for an EGL error. Returns an error string if there is one,
// or NULL otherwise.
char *egl_error(char *where) {
	return NULL;
}

/* Sets up an OpenGL ES 2 context. Returnes NULL if it succeeds, or
 * an error message on failure.
 */
char *egl_init(SDL_Window *sdl_window, int interval) {
	return NULL;
}

void egl_swap(void) {
}

void egl_quit(void) {
}
