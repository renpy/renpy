/* Copyright 2006 Rene Dudfield
 * Copyright 2014 Tom Rothamel
 *
 * This software is provided 'as-is', without any express or implied
 * warranty.  In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 */

#include <stdio.h>
#include <SDL.h>
#include <jpeglib.h>

static int write_jpeg (
		const char *file_name,
		JSAMPROW *rows,
		int width,
		int height,
		int quality) {

    struct jpeg_compress_struct cinfo;
    struct jpeg_error_mgr jerr;
    FILE * outfile;

    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_compress(&cinfo);

    if ((outfile = fopen(file_name, "wb")) == NULL) {
        SDL_SetError ("SaveJPEG: could not open %s", file_name);
        return -1;
    }

    jpeg_stdio_dest (&cinfo, outfile);

    cinfo.image_width = width;
    cinfo.image_height = height;
    cinfo.input_components = 3;
    cinfo.in_color_space = JCS_RGB;

    jpeg_set_defaults (&cinfo);
    jpeg_set_quality (&cinfo, quality, TRUE);

    jpeg_start_compress (&cinfo, TRUE);
    jpeg_write_scanlines(&cinfo, rows, height);
    jpeg_finish_compress (&cinfo);

    fclose (outfile);

    jpeg_destroy_compress (&cinfo);

    return 0;
}

int Pygame_SDL2_SaveJPEG(SDL_Surface *surface, const char *file, int quality) {

	SDL_Surface *rgb_surf;
	JSAMPROW *samples;
	int i, rv;

	if (quality < 0) {
		quality = 90;
	}

	rgb_surf = SDL_ConvertSurfaceFormat(surface, SDL_PIXELFORMAT_RGB24, 0);

    if (! rgb_surf) {
    	return -1;
    }

    samples = (JSAMPROW *) malloc (sizeof(JSAMPROW) * rgb_surf->h);

    if (!samples) {
    	SDL_FreeSurface(rgb_surf);
    	return -1;
    }

    /* copy pointers to the scanlines... since they might not be packed.
     */
    for (i = 0; i < rgb_surf->h; i++) {
        samples[i] = ((unsigned char*)rgb_surf->pixels) + i * rgb_surf->pitch;
    }

    rv = write_jpeg(file, samples, surface->w, surface->h, quality);

    free(samples);
    SDL_FreeSurface(rgb_surf);

    return rv;
}
