#ifndef SDL_IMAGE_COMPAT_H
#define SDL_IMAGE_COMPAT_H

#include "SDL_image.h"

#if ! SDL_IMAGE_VERSION_ATLEAST(2, 6, 0)

#define IMG_INIT_JXL  (0x00000010)
#define IMG_INIT_AVIF (0x00000020)

static SDL_Surface *mock_IMG_LoadSizedSVG_RW(void) {
    SDL_SetError("SDL_image is too old for SVG support.");
    return NULL;
}

#define IMG_LoadSizedSVG_RW(src, width, height) (mock_IMG_LoadSizedSVG_RW())

#endif

#endif
