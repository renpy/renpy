#ifndef PYGAME_SDL2_H
#define PYGAME_SDL2_H

#include "pygame_sdl2/pygame_sdl2.rwobject_api.h"
#include "pygame_sdl2/pygame_sdl2.surface_api.h"
#include "pygame_sdl2/pygame_sdl2.display_api.h"

/**
 * This imports the pygame_sdl2 C api. It returns 0 if the import succeeds, or
 * 1 if it fails.
 */
static int import_pygame_sdl2(void) {
	int rv = 0;

	rv |= import_pygame_sdl2__rwobject();
	rv |= import_pygame_sdl2__surface();
	rv |= import_pygame_sdl2__display();

	return rv;
}

#endif
