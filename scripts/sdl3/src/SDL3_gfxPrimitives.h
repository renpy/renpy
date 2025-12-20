/* 

SDL3_gfxPrimitives.h: graphics primitives for SDL

Copyright (C) 2012-2014  Andreas Schiffler

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
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

3. This notice may not be removed or altered from any source
distribution.

Andreas Schiffler -- aschiffler at ferzkopp dot net

*/

#ifndef _SDL3_gfxPrimitives_h
#define _SDL3_gfxPrimitives_h

#include <math.h>
#ifndef M_PI
#define M_PI	3.1415926535897932384626433832795
#endif

#include <SDL3/SDL.h>

/* Set up for C function definitions, even when using C++ */
#ifdef __cplusplus
extern "C" {
#endif

	/* ----- Versioning */

#define SDL3_GFXPRIMITIVES_MAJOR	1
#define SDL3_GFXPRIMITIVES_MINOR	0
#define SDL3_GFXPRIMITIVES_MICRO	0


	/* ---- Function Prototypes */

#ifdef _MSC_VER
#  if defined(DLL_EXPORT) && !defined(LIBSDL3_GFX_DLL_IMPORT)
#    define SDL3_GFXPRIMITIVES_SCOPE __declspec(dllexport)
#  else
#    ifdef LIBSDL3_GFX_DLL_IMPORT
#      define SDL3_GFXPRIMITIVES_SCOPE __declspec(dllimport)
#    endif
#  endif
#endif
#ifndef SDL3_GFXPRIMITIVES_SCOPE
#  define SDL3_GFXPRIMITIVES_SCOPE extern
#endif

	/* Note: all ___Color routines expect the color to be in format 0xRRGGBBAA */

	/* Pixel */

	SDL3_GFXPRIMITIVES_SCOPE bool pixelColor(SDL_Renderer * renderer, float x, float y, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool pixelRGBA(SDL_Renderer * renderer, float x, float y, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Horizontal line */

	SDL3_GFXPRIMITIVES_SCOPE bool hlineColor(SDL_Renderer * renderer, float x1, float x2, float y, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool hlineRGBA(SDL_Renderer * renderer, float x1, float x2, float y, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Vertical line */

	SDL3_GFXPRIMITIVES_SCOPE bool vlineColor(SDL_Renderer * renderer, float x, float y1, float y2, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool vlineRGBA(SDL_Renderer * renderer, float x, float y1, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Rectangle */

	SDL3_GFXPRIMITIVES_SCOPE bool rectangleColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool rectangleRGBA(SDL_Renderer * renderer, float x1, float y1,
		float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Rounded-Corner Rectangle */

	SDL3_GFXPRIMITIVES_SCOPE bool roundedRectangleColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float rad, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool roundedRectangleRGBA(SDL_Renderer * renderer, float x1, float y1,
		float x2, float y2, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Filled rectangle (Box) */

	SDL3_GFXPRIMITIVES_SCOPE bool boxColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool boxRGBA(SDL_Renderer * renderer, float x1, float y1, float x2,
		float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Rounded-Corner Filled rectangle (Box) */

	SDL3_GFXPRIMITIVES_SCOPE bool roundedBoxColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float rad, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool roundedBoxRGBA(SDL_Renderer * renderer, float x1, float y1, float x2,
		float y2, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Line */

	SDL3_GFXPRIMITIVES_SCOPE bool lineColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool lineRGBA(SDL_Renderer * renderer, float x1, float y1,
		float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* AA Line */

	SDL3_GFXPRIMITIVES_SCOPE bool aalineColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool aalineRGBA(SDL_Renderer * renderer, float x1, float y1,
		float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Thick Line */
	SDL3_GFXPRIMITIVES_SCOPE bool thickLineColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2,
		float width, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool thickLineRGBA(SDL_Renderer * renderer, float x1, float y1, float x2, float y2,
		float width, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Circle */

	SDL3_GFXPRIMITIVES_SCOPE bool circleColor(SDL_Renderer * renderer, float x, float y, float rad, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool circleRGBA(SDL_Renderer * renderer, float x, float y, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Arc */

	SDL3_GFXPRIMITIVES_SCOPE bool arcColor(SDL_Renderer * renderer, float x, float y, float rad, Sint32 start, Sint32 end, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool arcRGBA(SDL_Renderer * renderer, float x, float y, float rad, Sint32 start, Sint32 end,
		Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* AA Circle */

	SDL3_GFXPRIMITIVES_SCOPE bool aacircleColor(SDL_Renderer * renderer, float x, float y, float rad, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool aacircleRGBA(SDL_Renderer * renderer, float x, float y,
		float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Filled Circle */

	SDL3_GFXPRIMITIVES_SCOPE bool filledCircleColor(SDL_Renderer * renderer, float x, float y, float r, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool filledCircleRGBA(SDL_Renderer * renderer, float x, float y,
		float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Ellipse */

	SDL3_GFXPRIMITIVES_SCOPE bool ellipseColor(SDL_Renderer * renderer, float x, float y, float rx, float ry, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool ellipseRGBA(SDL_Renderer * renderer, float x, float y,
		float rx, float ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* AA Ellipse */

	SDL3_GFXPRIMITIVES_SCOPE bool aaellipseColor(SDL_Renderer * renderer, float x, float y, float rx, float ry, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool aaellipseRGBA(SDL_Renderer * renderer, float x, float y,
		float rx, float ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Filled Ellipse */

	SDL3_GFXPRIMITIVES_SCOPE bool filledEllipseColor(SDL_Renderer * renderer, float x, float y, float rx, float ry, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool filledEllipseRGBA(SDL_Renderer * renderer, float x, float y,
		float rx, float ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Pie */

	SDL3_GFXPRIMITIVES_SCOPE bool pieColor(SDL_Renderer * renderer, float x, float y, float rad,
		Sint32 start, Sint32 end, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool pieRGBA(SDL_Renderer * renderer, float x, float y, float rad,
		Sint32 start, Sint32 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Filled Pie */

	SDL3_GFXPRIMITIVES_SCOPE bool filledPieColor(SDL_Renderer * renderer, float x, float y, float rad,
		Sint32 start, Sint32 end, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool filledPieRGBA(SDL_Renderer * renderer, float x, float y, float rad,
		Sint32 start, Sint32 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Trigon */

	SDL3_GFXPRIMITIVES_SCOPE bool trigonColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float x3, float y3, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool trigonRGBA(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float x3, float y3,
		Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* AA-Trigon */

	SDL3_GFXPRIMITIVES_SCOPE bool aatrigonColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float x3, float y3, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool aatrigonRGBA(SDL_Renderer * renderer,  float x1, float y1, float x2, float y2, float x3, float y3,
		Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Filled Trigon */

	SDL3_GFXPRIMITIVES_SCOPE bool filledTrigonColor(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float x3, float y3, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool filledTrigonRGBA(SDL_Renderer * renderer, float x1, float y1, float x2, float y2, float x3, float y3,
		Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Polygon */

	SDL3_GFXPRIMITIVES_SCOPE bool polygonColor(SDL_Renderer * renderer, const float * vx, const float * vy, Sint32 n, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool polygonRGBA(SDL_Renderer * renderer, const float * vx, const float * vy,
		Sint32 n, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* AA-Polygon */

	SDL3_GFXPRIMITIVES_SCOPE bool aapolygonColor(SDL_Renderer * renderer, const float * vx, const float * vy, Sint32 n, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool aapolygonRGBA(SDL_Renderer * renderer, const float * vx, const float * vy,
		Sint32 n, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Filled Polygon */

	SDL3_GFXPRIMITIVES_SCOPE bool filledPolygonColor(SDL_Renderer * renderer, const float * vx, const float * vy, Sint32 n, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool filledPolygonRGBA(SDL_Renderer * renderer, const float * vx,
		const float * vy, Sint32 n, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Textured Polygon */

	SDL3_GFXPRIMITIVES_SCOPE bool texturedPolygon(SDL_Renderer * renderer, const float * vx, const float * vy, Sint32 n, SDL_Surface * texture,Sint32 texture_dx,Sint32 texture_dy);

	/* Bezier */

	SDL3_GFXPRIMITIVES_SCOPE bool bezierColor(SDL_Renderer * renderer, const float * vx, const float * vy, Sint32 n, Sint32 s, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool bezierRGBA(SDL_Renderer * renderer, const float * vx, const float * vy,
		Sint32 n, Sint32 s, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Characters/Strings */

	SDL3_GFXPRIMITIVES_SCOPE void gfxPrimitivesSetFont(const void *fontdata, Uint32 cw, Uint32 ch);
	SDL3_GFXPRIMITIVES_SCOPE void gfxPrimitivesSetFontRotation(Uint32 rotation);
	SDL3_GFXPRIMITIVES_SCOPE bool characterColor(SDL_Renderer * renderer, float x, float y, char c, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool characterRGBA(SDL_Renderer * renderer, float x, float y, char c, Uint8 r, Uint8 g, Uint8 b, Uint8 a);
	SDL3_GFXPRIMITIVES_SCOPE bool stringColor(SDL_Renderer * renderer, float x, float y, const char *s, Uint32 color);
	SDL3_GFXPRIMITIVES_SCOPE bool stringRGBA(SDL_Renderer * renderer, float x, float y, const char *s, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

	/* Ends C function definitions when using C++ */
#ifdef __cplusplus
}
#endif

#endif				/* _SDL3_gfxPrimitives_h */