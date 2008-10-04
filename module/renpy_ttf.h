/*
    SDL_ttf:  A companion library to SDL for working with TrueType (tm) fonts
    Copyright (C) 1997-2004 Sam Lantinga

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public
    License along with this library; if not, write to the Free
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    Sam Lantinga
    slouken@libsdl.org
*/

/* $Id: SDL_ttf.h 2387 2006-05-11 09:03:37Z slouken $ */

/* This library is a wrapper around the excellent FreeType 2.0 library,
   available at:
	http://www.freetype.org/
*/

#ifndef _RENPY_TTF_H
#define _RENPY_TTF_H

#include "SDL.h"
#include "begin_code.h"

/* Set up for C function definitions, even when using C++ */
#ifdef __cplusplus
extern "C" {
#endif

/* Printable format: "%d.%d.%d", MAJOR, MINOR, PATCHLEVEL
*/
#define RENPY_RENPY_TTF_MAJOR_VERSION	2
#define RENPY_RENPY_TTF_MINOR_VERSION	0
#define RENPY_RENPY_TTF_PATCHLEVEL	8

/* This macro can be used to fill a version structure with the compile-time
 * version of the SDL_ttf library.
 */
#define RENPY_RENPY_TTF_VERSION(X)						\
{									\
	(X)->major = RENPY_RENPY_TTF_MAJOR_VERSION;				\
	(X)->minor = RENPY_RENPY_TTF_MINOR_VERSION;				\
	(X)->patch = RENPY_RENPY_TTF_PATCHLEVEL;				\
}

/* Backwards compatibility */
#define RENPY_TTF_MAJOR_VERSION	RENPY_RENPY_TTF_MAJOR_VERSION
#define RENPY_TTF_MINOR_VERSION	RENPY_RENPY_TTF_MINOR_VERSION
#define RENPY_TTF_PATCHLEVEL		RENPY_RENPY_TTF_PATCHLEVEL
#define RENPY_TTF_VERSION(X)		RENPY_RENPY_TTF_VERSION(X)

/* This function gets the version of the dynamically linked SDL_ttf library.
   it should NOT be used to fill a version structure, instead you should
   use the RENPY_RENPY_TTF_VERSION() macro.
 */
extern DECLSPEC const SDL_version * SDLCALL RENPY_TTF_Linked_Version(void);

/* ZERO WIDTH NO-BREAKSPACE (Unicode byte order mark) */
#define UNICODE_BOM_NATIVE	0xFEFF
#define UNICODE_BOM_SWAPPED	0xFFFE

/* This function tells the library whether UNICODE text is generally
   byteswapped.  A UNICODE BOM character in a string will override
   this setting for the remainder of that string.
*/
extern DECLSPEC void SDLCALL RENPY_TTF_ByteSwappedUNICODE(int swapped);

/* The internal structure containing font information */
typedef struct _RENPY_TTF_Font RENPY_TTF_Font;

/* Initialize the TTF engine - returns 0 if successful, -1 on error */
extern DECLSPEC int SDLCALL RENPY_TTF_Init(void);

/* Open a font file and create a font of the specified point size.
 * Some .fon fonts will have several sizes embedded in the file, so the
 * point size becomes the index of choosing which size.  If the value
 * is too high, the last indexed size will be the default. */
extern DECLSPEC RENPY_TTF_Font * SDLCALL RENPY_TTF_OpenFont(const char *file, int ptsize);
extern DECLSPEC RENPY_TTF_Font * SDLCALL RENPY_TTF_OpenFontIndex(const char *file, int ptsize, long index);
extern DECLSPEC RENPY_TTF_Font * SDLCALL RENPY_TTF_OpenFontRW(SDL_RWops *src, int freesrc, int ptsize);
extern DECLSPEC RENPY_TTF_Font * SDLCALL RENPY_TTF_OpenFontIndexRW(SDL_RWops *src, int freesrc, int ptsize, long index);

/* Set and retrieve the font style
   This font style is implemented by modifying the font glyphs, and
   doesn't reflect any inherent properties of the truetype font file.
*/
#define RENPY_TTF_STYLE_NORMAL	0x00
#define RENPY_TTF_STYLE_BOLD		0x01
#define RENPY_TTF_STYLE_ITALIC	0x02
#define RENPY_TTF_STYLE_UNDERLINE	0x04
extern DECLSPEC int SDLCALL RENPY_TTF_GetFontStyle(RENPY_TTF_Font *font);
extern DECLSPEC void SDLCALL RENPY_TTF_SetFontStyle(RENPY_TTF_Font *font, int style);

/* Get the total height of the font - usually equal to point size */
extern DECLSPEC int SDLCALL RENPY_TTF_FontHeight(RENPY_TTF_Font *font);

/* Get the offset from the baseline to the top of the font
   This is a positive value, relative to the baseline.
 */
extern DECLSPEC int SDLCALL RENPY_TTF_FontAscent(RENPY_TTF_Font *font);

/* Get the offset from the baseline to the bottom of the font
   This is a negative value, relative to the baseline.
 */
extern DECLSPEC int SDLCALL RENPY_TTF_FontDescent(RENPY_TTF_Font *font);

/* Get the recommended spacing between lines of text for this font */
extern DECLSPEC int SDLCALL RENPY_TTF_FontLineSkip(RENPY_TTF_Font *font);

/* Get the number of faces of the font */
extern DECLSPEC long SDLCALL RENPY_TTF_FontFaces(RENPY_TTF_Font *font);

/* Get the font face attributes, if any */
extern DECLSPEC int SDLCALL RENPY_TTF_FontFaceIsFixedWidth(RENPY_TTF_Font *font);
extern DECLSPEC char * SDLCALL RENPY_TTF_FontFaceFamilyName(RENPY_TTF_Font *font);
extern DECLSPEC char * SDLCALL RENPY_TTF_FontFaceStyleName(RENPY_TTF_Font *font);

/* Get the metrics (dimensions) of a glyph
   To understand what these metrics mean, here is a useful link:
    http://freetype.sourceforge.net/freetype2/docs/tutorial/step2.html
 */
extern DECLSPEC int SDLCALL RENPY_TTF_GlyphMetrics(RENPY_TTF_Font *font, Uint16 ch,
				     int *minx, int *maxx,
                                     int *miny, int *maxy, int *advance);

/* Get the dimensions of a rendered string of text */
extern DECLSPEC int SDLCALL RENPY_TTF_SizeText(RENPY_TTF_Font *font, const char *text, int *w, int *h);
extern DECLSPEC int SDLCALL RENPY_TTF_SizeUTF8(RENPY_TTF_Font *font, const char *text, int *w, int *h);
extern DECLSPEC int SDLCALL RENPY_TTF_SizeUNICODE(RENPY_TTF_Font *font, const Uint16 *text, int *w, int *h);

/* Create an 8-bit palettized surface and render the given text at
   fast quality with the given font and color.  The 0 pixel is the
   colorkey, giving a transparent background, and the 1 pixel is set
   to the text color.
   This function returns the new surface, or NULL if there was an error.
*/
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderText_Solid(RENPY_TTF_Font *font,
				const char *text, SDL_Color fg);
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderUTF8_Solid(RENPY_TTF_Font *font,
				const char *text, SDL_Color fg);
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderUNICODE_Solid(RENPY_TTF_Font *font,
				const Uint16 *text, SDL_Color fg);

/* Create an 8-bit palettized surface and render the given glyph at
   fast quality with the given font and color.  The 0 pixel is the
   colorkey, giving a transparent background, and the 1 pixel is set
   to the text color.  The glyph is rendered without any padding or
   centering in the X direction, and aligned normally in the Y direction.
   This function returns the new surface, or NULL if there was an error.
*/
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderGlyph_Solid(RENPY_TTF_Font *font,
					Uint16 ch, SDL_Color fg);

/* Create an 8-bit palettized surface and render the given text at
   high quality with the given font and colors.  The 0 pixel is background,
   while other pixels have varying degrees of the foreground color.
   This function returns the new surface, or NULL if there was an error.
*/
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderText_Shaded(RENPY_TTF_Font *font,
				const char *text, SDL_Color fg, SDL_Color bg);
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderUTF8_Shaded(RENPY_TTF_Font *font,
				const char *text, SDL_Color fg, SDL_Color bg);
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderUNICODE_Shaded(RENPY_TTF_Font *font,
				const Uint16 *text, SDL_Color fg, SDL_Color bg);

/* Create an 8-bit palettized surface and render the given glyph at
   high quality with the given font and colors.  The 0 pixel is background,
   while other pixels have varying degrees of the foreground color.
   The glyph is rendered without any padding or centering in the X
   direction, and aligned normally in the Y direction.
   This function returns the new surface, or NULL if there was an error.
*/
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderGlyph_Shaded(RENPY_TTF_Font *font,
				Uint16 ch, SDL_Color fg, SDL_Color bg);

/* Create a 32-bit ARGB surface and render the given text at high quality,
   using alpha blending to dither the font with the given color.
   This function returns the new surface, or NULL if there was an error.
*/
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderText_Blended(RENPY_TTF_Font *font,
				const char *text, SDL_Color fg);
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderUTF8_Blended(RENPY_TTF_Font *font,
				const char *text, SDL_Color fg);
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderUNICODE_Blended(RENPY_TTF_Font *font,
				const Uint16 *text, SDL_Color fg);

/* Create a 32-bit ARGB surface and render the given glyph at high quality,
   using alpha blending to dither the font with the given color.
   The glyph is rendered without any padding or centering in the X
   direction, and aligned normally in the Y direction.
   This function returns the new surface, or NULL if there was an error.
*/
extern DECLSPEC SDL_Surface * SDLCALL RENPY_TTF_RenderGlyph_Blended(RENPY_TTF_Font *font,
						Uint16 ch, SDL_Color fg);

/* For compatibility with previous versions, here are the old functions */
#define RENPY_TTF_RenderText(font, text, fg, bg)	\
	RENPY_TTF_RenderText_Shaded(font, text, fg, bg)
#define RENPY_TTF_RenderUTF8(font, text, fg, bg)	\
	RENPY_TTF_RenderUTF8_Shaded(font, text, fg, bg)
#define RENPY_TTF_RenderUNICODE(font, text, fg, bg)	\
	RENPY_TTF_RenderUNICODE_Shaded(font, text, fg, bg)

/* Close an opened font file */
extern DECLSPEC void SDLCALL RENPY_TTF_CloseFont(RENPY_TTF_Font *font);

/* De-initialize the TTF engine */
extern DECLSPEC void SDLCALL RENPY_TTF_Quit(void);

/* Check if the TTF engine is initialized */
extern DECLSPEC int SDLCALL RENPY_TTF_WasInit(void);

extern DECLSPEC void SDLCALL RENPY_TTF_SetExpand(RENPY_TTF_Font *, float);

/* We'll use SDL for reporting errors */
#define RENPY_TTF_SetError	SDL_SetError
#define RENPY_TTF_GetError	SDL_GetError

/* Ends C function definitions when using C++ */
#ifdef __cplusplus
}
#endif
#include "close_code.h"

#endif /* _RENPY_TTF_H */
