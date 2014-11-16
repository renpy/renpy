/* subpixel.c - Ren'Py subpixel blitter code.
 * Copyright 2009 Tom Rothamel <pytom@bishoujo.us>
 *
 * This allows one to blit an image at a fractional pixel position. It
 * requires MMX to operate. On non-mmx platforms, a traditional blit
 * is used instead.
 */

#include "renpy.h"
#include <SDL.h>
#include <pygame_sdl2/pygame_sdl2.h>
#include <stdio.h>
#include <math.h>

void subpixel_init() {
    import_pygame_sdl2();
}

#if defined(__GNUC__) && (defined(__i386__) || defined(__x86_64__))
#define GCC_MMX 1
#include "mmx.h"
#endif


/* MMX Register assignments (between applications of the blitter core).
 *
 * mm0 - new row 0
 * mm1 - new row 1
 * mm2 - destination
 * mm3 - alpha shift.
 * mm4 - old row 0
 * mm5 - old row 1
 * mm6 - (256 - xfrac)
 * mm7 - (256 - yfrac) (or alpha-multiply)
 */


/*************************************************************************
 * This is the basic algorithm that does the subpixel blit
 * interpolation.
 *************************************************************************/

/* mm2 = destination; */

/* unpack mm0; */
/* unpack mm1; */
/* unpack mm2; */

/* // Horizontal */
/* mm4 -= mm0; */
/* mm5 -= mm1; */
/* mm4 *= xfrac; */
/* mm5 *= xfrac; */
/* mm4 >>= 8; */
/* mm5 >>= 8; */
/* mm4 += mm0; */
/* mm5 += mm1; */

/* // Vertical */
/* mm4 -= mm5; */
/* mm4 *= yfrac; */
/* mm4 >>= 8; */
/* mm4 += mm5; */

/* // Alpha blend, */
/* mm5 = mm4; */
/* mm5 >>= mm3; */
/* unpack mm5; */
/* mm4 -= mm2; */
/* unpack mm5; */
/* mm4 *= mm5; */
/* mm4 >>= 8; */
/* mm4 += mm2; */

/* // Store and repeat */
/* pack mm4 */
/* destination = mm4; */
/* mm4 = mm0; */
/* mm5 = mm1; */

#ifdef GCC_MMX


#define dp(s, r)            \
    movq_r2m(r, scratch); \
    printf(s, scratch);

// This expands registers 4 and 5, which are initialized below.
#define MMX_EXPAND()                            \
    pxor_r2r(mm2, mm2);                         \
    punpcklbw_r2r(mm2, mm4);                    \
    punpcklbw_r2r(mm2, mm5);


// This expects the two old pixels to be arranged like:
// mm4 mm0
// mm5 mm1
// alpha shift in mm3
// (256 - xfrac) in mm6
// (256 - yfrac) in mm7
// It does the bilinear interpolation, and leaves the result
// in mm4.
#define MMX_INTERP(dest)                        \
    pxor_r2r(mm2, mm2);                         \
    punpcklbw_r2r(mm2, mm0);                    \
    punpcklbw_r2r(mm2, mm1);                    \
                                                \
    psubw_r2r(mm0, mm4);                        \
    psubw_r2r(mm1, mm5);                        \
    pmullw_r2r(mm6, mm4);                       \
    pmullw_r2r(mm6, mm5);                       \
    psrlw_i2r(8, mm4);                          \
    psrlw_i2r(8, mm5);                          \
    paddb_r2r(mm0, mm4);                        \
    paddb_r2r(mm1, mm5);                        \
    /* p0 in mm4, p1 in mm5 */                  \
                                                \
    psubw_r2r(mm5, mm4);                        \
    pmullw_r2r(mm7, mm4);                       \
    psrlw_i2r(8, mm4);                          \
    paddb_r2r(mm5, mm4);                        \
    /* p in mm4 */                              \
                                                \
    pxor_r2r(mm5, mm5);                         \
    movd_m2r((dest), mm2);                      \
    punpcklbw_r2r(mm5, mm2);                    \
                                                \
    movq_r2r(mm4, mm5);                         \
    psrlq_r2r(mm3, mm5);                        \
    punpcklwd_r2r(mm5, mm5);                    \
    punpcklwd_r2r(mm5, mm5);                    \
    psubw_r2r(mm2, mm4);                        \
    pmullw_r2r(mm5, mm4);                       \
    psrlw_i2r(8, mm4);                          \
    paddb_r2r(mm2, mm4);                        \
    packuswb_r2r(mm4, mm4);                     \
    movd_r2m(mm4, (dest));                      \
    movq_r2r(mm0, mm4);                         \
    movq_r2r(mm1, mm5);

#define min(x, y) ( ((x) < (y)) ? (x) : (y) )

/* This blits pysrc into pydst such that the upper-right corner of
   pysrc is at xo, yo relative to pydst. */
int subpixel32(PyObject *pysrc, PyObject *pydst,
               float xoffset, float yoffset, int ashift) {
    SDL_Surface *src;
    SDL_Surface *dst;

    int srcpitch, dstpitch;
    int srcw, srch;
    int dstw, dsth;
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    int xfrac, yfrac;
    int xo, yo;
    int sx, sy;

    int draw_finalx;
    int normal_pixels;

    int inverted_alpha_mask;

    unsigned int pixel;
    unsigned int blankpixel;

    unsigned char *s0;
    unsigned char *s1;
    unsigned char *d;
    unsigned char *dend;


    long long scratch;

    if (!SDL_HasMMX()) {
        return 0;
    }

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

    inverted_alpha_mask = ~(0xff << ashift);

    // Due to mmx.
    ashift *= 2;

    xo = (int) floor(xoffset);
    yo = (int) floor(yoffset);
    xfrac = (int) ((xoffset - xo) * 255);
    yfrac = (int) ((yoffset - yo) * 255);

    // Due to the way the interpolator works.
    // xfrac = 256 - xfrac;
    // yfrac = 256 - yfrac;

    if (xo < 0) {
        sx = -xo - 1;
        xo = 0;
    } else {
        sx = -1;
    }

    if (yo < 0) {
        sy = -yo - 1;
        yo = 0;
    } else {
        sy = -1;
    }

    if (sx >= srcw - 1 || sy >= srch - 1) {
        goto done;
    }

    // Figure out how many pixels we need to draw on each line.
    normal_pixels = min(srcw - sx - 1, dstw - xo);

    if (normal_pixels < dstw - xo) {
        draw_finalx = 1;
    } else {
        draw_finalx = 0;
    }

    // Load up the mmx registers.
    movd_m2r(xfrac, mm6);
    punpcklwd_r2r(mm6, mm6);
    punpckldq_r2r(mm6, mm6);

    movd_m2r(yfrac, mm7);
    punpcklwd_r2r(mm7, mm7);
    punpckldq_r2r(mm7, mm7);

    movd_m2r(ashift, mm3);

    if (xo >= dstw) {
        goto done;
    }

    // Draw the first line, when sy == -1.

    if (sy == -1) {

        if (yo >= dsth) {
            goto done;
        }

        s1 = srcpixels + sx * 4;

        if (sx < 0) {
            pixel = (* (unsigned int *) (s1 + 4)) & inverted_alpha_mask;
        } else {
            pixel = * (unsigned int *) s1;
        }

        blankpixel = pixel & inverted_alpha_mask;

        movd_m2r(blankpixel, mm4);
        movd_m2r(pixel, mm5);

        MMX_EXPAND();
        s1 += 4;

        d = dstpixels + xo * 4 + yo * dstpitch;
        dend = d + normal_pixels * 4;

        while (d != dend) {
            pixel = * (unsigned int *) s1;
            blankpixel = pixel & inverted_alpha_mask;
            movd_m2r(blankpixel, mm0);
            movd_m2r(pixel, mm1);
            MMX_INTERP(* (unsigned int *) d);
            d += 4;
            s1 += 4;

        }

        if (draw_finalx) {
            s1 -= 4;
            movd_m2r(blankpixel, mm0);
            movd_m2r(blankpixel, mm1);
            MMX_INTERP(* (unsigned int *) d);
        }

        sy += 1;
        yo += 1;
    }

    // Draw the second and later lines..

    while (sy < srch - 1) {

        if (yo >= dsth) {
            goto done;
        }

        s0 = srcpixels + sx * 4 + (srcpitch * sy);
        s1 = srcpixels + sx * 4 + (srcpitch * (sy + 1));

        if (sx < 0) {
            blankpixel = (* (unsigned int *) (s0 + 4)) & inverted_alpha_mask;
            movd_m2r(blankpixel, mm4);

            blankpixel = (* (unsigned int *) (s1 + 4)) & inverted_alpha_mask;
            movd_m2r(blankpixel, mm5);

        } else {
            movd_m2r(* (unsigned int *) s0, mm4);
            movd_m2r(* (unsigned int *) s1, mm5);
        }

        MMX_EXPAND();

        s0 += 4;
        s1 += 4;

        d = dstpixels + xo * 4 + yo * dstpitch;
        dend = d + normal_pixels * 4;

        unsigned char *dp = d;

        while (d != dend) {
            movd_m2r(* (unsigned int *) s0, mm0);
            movd_m2r(* (unsigned int *) s1, mm1);
            MMX_INTERP(* (unsigned int *) d);

            d += 4;
            s0 += 4;
            s1 += 4;
        }

        if (draw_finalx) {
            s0 -= 4;
            s1 -= 4;

            blankpixel = (* (unsigned int *) s0) & inverted_alpha_mask;
            movd_m2r(blankpixel, mm0);
            blankpixel = (* (unsigned int *) s1) & inverted_alpha_mask;
            movd_m2r(blankpixel, mm1);
            MMX_INTERP(* (unsigned int *) d);
        }

        yo += 1;
        sy += 1;

    }

    // The final part, where we handle the bottom line of the source surface.

    if (yo >= dsth) {
        goto done;
    }

    s0 = srcpixels + sx * 4 + (srcpitch * sy);

    if (sx < 0) {
        pixel = * (unsigned int *) (s0 + 4);
        blankpixel = pixel & inverted_alpha_mask;

        movd_m2r(blankpixel, mm4);
        movd_m2r(blankpixel, mm5);
    } else {
        pixel = * (unsigned int *) s0;
        blankpixel = pixel & inverted_alpha_mask;

        movd_m2r(pixel, mm4);
        movd_m2r(blankpixel, mm5);
    }

    MMX_EXPAND();

    s0 += 4;

    d = dstpixels + xo * 4 + yo * dstpitch;
    dend = d + normal_pixels * 4;

    while (d != dend) {
        pixel = * (unsigned int *) s0;
        blankpixel = pixel & inverted_alpha_mask;

        movd_m2r(pixel, mm0);
        movd_m2r(blankpixel, mm1);
        MMX_INTERP(* (unsigned int *) d);
        d += 4;
        s0 += 4;
    }

    if (draw_finalx) {
        movd_m2r(blankpixel, mm0);
        movd_m2r(blankpixel, mm1);
        MMX_INTERP(* (unsigned int *) d);
    }


done:

    // Reset the MMX unit and call it a night.
    emms();

    Py_END_ALLOW_THREADS


    return 1;
}

#else


/* On a non-mmx platform, return 0 to let the pyrex code handle it. */

int subpixel32(PyObject *pysrc, PyObject *pydst,
                float xoffset, float yoffset, int ashift) {
    return 0;
}

#endif
