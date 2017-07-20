#ifndef EGLSUPPORT_H
#define EGLSUPPORT_H
#include <SDL.h>

/*
 * Returns 1 if this is an EGL platform, or 0 if we are not an EGL platform.
 */
int egl_available(void);

/*
 * If an EGL error has occured, returns a string giving ther error. `where`
 * is text that's included in that string.
 */
char *egl_error(char *where);

/*
 * Initializes the egl system. `interval` is the vsync refresh interval,
 * usually either 1 or 0. Returns NULL on success, or a string if
 * initialization has failed.
 */
char *egl_init(SDL_Window *, int interval);


/*
 * Tells EGL to swap buffers.
 */
void egl_swap(void);

/*
 * Deinitializes EGL support.
 */
void egl_quit(void);

#endif
