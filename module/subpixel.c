/* subpixel.c - Ren'Py subpixel blitter code.
 * Copyright 2009 Tom Rothamel <pytom@bishoujo.us>
 *
 * This allows one to blit an image at a fractional pixel position. It
 * requires MMX to operate. On non-mmx platforms, a traditional blit
 * is used instead.
 */

#include "renpy.h"
#include <pygame/pygame.h>
#include <stdio.h>
#include <math.h>

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
 * mm7 - (256 - yfrac)
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


#define MMX_INTERP(dest)   \
    movd_m2r((dest), mm2); \
    punpcklbw_r2r(mm0, mm0); \
    punpcklbw_r2r(mm1, mm1); \
    punpcklbw_r2r(mm2, mm2); \
    \
    psubw_r2r(mm0, mm4); \
    psubw_r2r(mm1, mm4); \
    pmullw_r2r(mm6, mm4); \
    pmullw_r2r(mm6, mm5); \
    psrlw_i2r(8, mm4);  \
    psrlw_i2r(8, mm5); \
    paddw_r2r(mm0, mm4); \
    paddw_r2r(mm1, mm5); \
    \
    psubw_r2r(mm5, mm4); \
    pmullw_r2r(mm7, mm4); \
    psrlw_i2r(8, mm4); \
    paddw_r2r(mm5, mm4); \
    \
    movq_r2r(mm4, mm5); \
    psrlq_r2r(mm3, mm5); \
    punpcklwd_r2r(mm5, mm5); \
    psubw_r2r(mm2, mm4); \
    punpcklwd_r2r(mm5, mm5); \
    pmullw_r2r(mm5, mm4); \
    psrlw_i2r(8, mm4); \
    paddw_r2r(mm2, mm4);   \
    packuswb_r2r(mm4, mm4); \
    movd_r2m(mm4, (dest)); \
    movq_r2r(mm0, mm4); \
    movq_r2r(mm1, mm5);

#define min(x, y) ( ((x) < (y)) ? (x) : (y) )


/* This blits pysrc intp pydst such that the upper-right corner of
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

    unsigned char *s0;
    unsigned char *s1;
    unsigned char *d;
    unsigned char *dend;

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

    // Due to mmx.
    ashift *= 2;

    xo = (int) floor(xoffset);
    yo = (int) floor(yoffset);
    xfrac = (int) ((xoffset - xo) * 256);
    yfrac = (int) ((yoffset - yo) * 256);

   // Due to the way the interpolator works.
    xfrac = 256 - xfrac;
    yfrac = 256 - yfrac;

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

    // Figure out how many pixels we need to draw on each line.
    normal_pixels = min(srcw - sy - 1, dstw - xo);
    if (normal_pixels < dstw - xo) {
        draw_finalx = 1;
    } else {
        draw_finalx = 0;
    }

    if (xo >= dstw) {
        goto done;
    }
    
    // Draw the first line.

    if (yo >= dsth) {
        goto done;
    }

    s1 = srcpixels + sx * 4;
    
    if (yo == -1) {

        pxor_r2r(mm4, mm4);
        
        if (xo < 0) {
            pxor_r2r(mm5, mm5);
        } else {
            movd_m2r(* (unsigned int *) s1, mm5);
        }

        s1 += 4;
    }
        
    d = dstpixels + xo * 4 + yo * srcpitch;
    dend = d + normal_pixels * 4;

    while (d != dend) {
        pxor_r2r(mm4, mm4);
        movd_m2r(* (unsigned int *) s1, mm5);        
        MMX_INTERP(* (unsigned int *) d);
        d += 4;
        s1 += 4;
    }

    if (draw_finalx) {
        pxor_r2r(mm4, mm4);
        pxor_r2r(mm5, mm5);
        MMX_INTERP(* (unsigned int *) d);
    }

    sy += 1;
    yo += 1;

    // Draw the second and later lines..

    while (sy < srch) {

        if (yo >= dsth) {
            goto done;
        }

        s0 = srcpixels + sx * 4 + (srcpitch * sy);
        s1 = srcpixels + sx * 4 + (srcpitch * (sy + 1));
        
        if (yo == -1) {

        
            if (xo < 0) {
                pxor_r2r(mm4, mm4);
                pxor_r2r(mm5, mm5);
            } else {
                movd_m2r(* (unsigned int *) s0, mm4);
                movd_m2r(* (unsigned int *) s1, mm5);
            }

            s0 += 4;
            s1 += 4;
        }
        
        d = dstpixels + xo * 4 + yo * srcpitch;
        dend = d + normal_pixels * 4;

        while (d != dend) {
            movd_m2r(* (unsigned int *) s0, mm4);        
            movd_m2r(* (unsigned int *) s1, mm5);        
            MMX_INTERP(* (unsigned int *) d);
            d += 4;
            s0 += 4;
            s1 += 4;
        }

        if (draw_finalx) {
            pxor_r2r(mm4, mm4);
            pxor_r2r(mm5, mm5);
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
        
    if (yo == -1) {
        
        if (xo < 0) {
            pxor_r2r(mm4, mm4);
            pxor_r2r(mm5, mm5);
        } else {
            movd_m2r(* (unsigned int *) s0, mm4);
            pxor_r2r(mm5, mm5);
        }

        s0 += 4;
    }
        
    d = dstpixels + xo * 4 + yo * srcpitch;
    dend = d + normal_pixels * 4;

    while (d != dend) {
        movd_m2r(* (unsigned int *) s0, mm4);        
        pxor_r2r(mm5, mm5);
        MMX_INTERP(* (unsigned int *) d);
        d += 4;
        s0 += 4;
    }

    if (draw_finalx) {
        pxor_r2r(mm4, mm4);
        pxor_r2r(mm5, mm5);
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

void subpixel32(PyObject *pysrc, PyObject *pydst,
                float xoffset, float yoffset, int ashift) {
    return 0;
}

#endif
