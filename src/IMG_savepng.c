/*
  Based on zlib license - see http://www.gzip.org/zlib/zlib_license.html

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.

  "Philip D. Bober" <wildfire1138@mchsi.com>
*/

/**
 * 4/17/04 - IMG_SavePNG & IMG_SavePNG_RW - Philip D. Bober
 * 11/08/2004 - Compr fix, levels -1,1-7 now work - Tyler Montbriand
 */
#include <stdlib.h>
#include <SDL3/SDL.h>
#include <png.h>
#include <zlib.h>
#include "IMG_savepng.h"

#ifndef png_voidp
#define png_voidp voidp
#endif

int renpy_IMG_SavePNG(const char *file, SDL_Surface *surf,int compression){
	SDL_IOStream *fp;
	int ret;

	fp=SDL_IOFromFile(file,"wb");

	if( fp == NULL ) {
		return (-1);
	}

	ret=renpy_IMG_SavePNG_RW(fp,surf,compression);
	return ret;
}

static void png_write_data(png_structp png_ptr,png_bytep data, png_size_t length){
	SDL_IOStream *rp = (SDL_IOStream*) png_get_io_ptr(png_ptr);
	SDL_WriteIO(rp,data,length);
}

int renpy_IMG_SavePNG_RW(SDL_IOStream *src, SDL_Surface *surf,int compression){
	png_structp png_ptr;
	png_infop info_ptr;
	const SDL_PixelFormatDetails *fmt=NULL;
	SDL_Surface *tempsurf=NULL;
	int ret;
	png_byte **row_pointers=NULL;
	Uint32 target_format;

	if( !src || !surf) {
		goto savedone2; /* Nothing to do. */
	}

	row_pointers=(png_byte **)malloc(surf->h * sizeof(png_byte*));
	if (!row_pointers) {
		SDL_SetError("Couldn't allocate memory for rowpointers");
		goto savedone2;
	}

	png_ptr=png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL,NULL,NULL);
	if (!png_ptr){
		SDL_SetError("Couldn't allocate memory for PNG file version: " PNG_LIBPNG_VER_STRING);
		goto savedone2;
	}
	info_ptr= png_create_info_struct(png_ptr);
	if (!info_ptr){
		SDL_SetError("Couldn't allocate image information for PNG file");
		goto savedone;
	}
	/* setup custom writer functions */
	png_set_write_fn(png_ptr,(png_voidp)src,png_write_data,NULL);

	if (setjmp(png_jmpbuf(png_ptr))){
		SDL_SetError("Unknown error writing PNG");
		goto savedone;
	}

	if(compression>Z_BEST_COMPRESSION)
		compression=Z_BEST_COMPRESSION;

	if(compression == Z_NO_COMPRESSION) // No compression
	{
		png_set_filter(png_ptr,0,PNG_FILTER_NONE);
		png_set_compression_level(png_ptr,Z_NO_COMPRESSION);
	}
	else if(compression<0) // Default compression
		png_set_compression_level(png_ptr,Z_DEFAULT_COMPRESSION);
	else
		png_set_compression_level(png_ptr,compression);

	fmt= SDL_GetPixelFormatDetails(surf->format);

	if (fmt->Amask) {
		png_set_IHDR(png_ptr,info_ptr,
			surf->w,surf->h,8,PNG_COLOR_TYPE_RGB_ALPHA,
			PNG_INTERLACE_NONE,PNG_COMPRESSION_TYPE_DEFAULT,
			PNG_FILTER_TYPE_DEFAULT);
	} else {
		png_set_IHDR(png_ptr,info_ptr,
			surf->w,surf->h,8,PNG_COLOR_TYPE_RGB,
			PNG_INTERLACE_NONE,PNG_COMPRESSION_TYPE_DEFAULT,
			PNG_FILTER_TYPE_DEFAULT);
	}

	png_write_info(png_ptr, info_ptr);

#if SDL_BYTEORDER == SDL_LIL_ENDIAN
	if (fmt->Amask) {
		target_format = SDL_PIXELFORMAT_ABGR8888;
	} else {
		target_format = SDL_PIXELFORMAT_XBGR8888;
	}
#else
	if (fmt->Amask) {
		target_format = SDL_PIXELFORMAT_RGBA8888;
	} else {
		target_format = SDL_PIXELFORMAT_RGB888;
	}
#endif

	if (surf->format != target_format) {
		tempsurf = SDL_ConvertSurface(surf, target_format);
		surf = tempsurf;

		if (!tempsurf){
			SDL_SetError("Couldn't allocate temp surface");
			goto savedone;
		}
	}

	for(int i=0;i < surf->h;i++){
		row_pointers[i]= ((png_byte*) surf->pixels) + i * surf->pitch;
	}

	png_write_image(png_ptr, row_pointers);

	if (tempsurf) {
		SDL_DestroySurface(tempsurf);
	}

	png_write_end(png_ptr, NULL);

	ret=0; /* got here, so nothing went wrong. YAY! */

savedone: /* clean up and return */
	png_destroy_write_struct(&png_ptr,&info_ptr);

savedone2:
	if (row_pointers) {
		free(row_pointers);
	}

	SDL_CloseIO(src);

	return ret;
}
