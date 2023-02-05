#include "renpy.h"
#include "IMG_savepng.h"
#include <SDL.h>
#include <pygame_sdl2/pygame_sdl2.h>
#include <stdio.h>
#include <math.h>

// Shows how to do this.
#if SDL_BYTEORDER == SDL_BIG_ENDIAN
#endif

/* Initializes the stuff found in this file.
 */
void core_init() {
    import_pygame_sdl2();
}

void save_png_core(PyObject *pysurf, SDL_RWops *rw, int compress) {
    SDL_Surface *surf;

    surf = PySurface_AsSurface(pysurf);

    /* Can't release GIL, since we're not using threaded RWops. */
    renpy_IMG_SavePNG_RW(rw, surf, compress);
}

/* This pixellates a 32-bit RGBA pygame surface to a destination
 * surface of a given size.
 *
 * pysrc - The source pygame surface, which must be 32-bit RGBA.
 * pydst - The destination pygame surface, which should be 32-bit
 * RGBA, and locked.
 * avgwidth - The width of the pixels that will be averaged together.
 * avgheight - The height of the pixels that will be averaged
 * together.
 * outwidth - The width of pixels that will be written to the output.
 * outheight - The height of pixels that will be written to the
 * output.
 *
 * We assume that pysrc and pydst have been locked before we are called.
 */
void pixellate32_core(PyObject *pysrc,
                      PyObject *pydst,
                      int avgwidth,
                      int avgheight,
                      int outwidth,
                      int outheight
    ) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int x, y, i, j;
    int srcpitch, dstpitch;
    int srcw, srch;
    int dstw, dsth;
    int vw, vh;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

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

    /* Compute the virtual width and height. */
    vw = ( srcw + avgwidth - 1) / avgwidth;
    vh = ( srch + avgheight - 1) / avgheight;

    /* Iterate through each of the virtual pixels. */

    for (y = 0; y < vh; y++) {
        int srcy = avgheight * y;
        int dsty = outheight * y;

        int srcylimit = srcy + avgheight;
        int dstylimit = dsty + outheight;

        if (srcylimit > srch) {
            srcylimit = srch;
        }

        if (dstylimit > dsth) {
            dstylimit = dsth;
        }

        for (x = 0; x < vw; x++) {
            int srcx = avgwidth * x;
            int dstx = outwidth * x;

            int srcxlimit = srcx + avgwidth;
            int dstxlimit = dstx + outheight;

            if (srcxlimit > srcw) {
                srcxlimit = srcw;
            }

            if (dstxlimit > dstw) {
                dstxlimit = dstw;
            }

            // Please note that these names are just
            // suggestions... It's possible that alpha will be
            // in r, for example.
            int r = 0;
            int g = 0;
            int b = 0;
            int a = 0;

            int number = 0;

            // pos always points to the start of the current line.
            unsigned char *pos = &srcpixels[srcy * srcpitch + srcx * 4];

            /* Sum up the pixel values. */

            for (j = srcy; j < srcylimit; j++) {
                // po points to the current pixel.
                unsigned char *po = pos;

                for (i = srcx; i < srcxlimit; i++) {
                    r += *po++;
                    g += *po++;
                    b += *po++;
                    a += *po++;
                    number += 1;
                }

                pos += srcpitch;
            }

            /* Compute the average pixel values. */
            r /= number;
            g /= number;
            b /= number;
            a /= number;

            /* Write out the average pixel values. */
            pos = &dstpixels[dsty * dstpitch + dstx * 4];
            for (j = dsty; j < dstylimit; j++) {
                unsigned char *po = pos;

                for (i = dstx; i < dstxlimit; i++) {
                    *po++ = r;
                    *po++ = g;
                    *po++ = b;
                    *po++ = a;
                }

                pos += dstpitch;
            }
        }
    }

    Py_END_ALLOW_THREADS

}

/* This pixellates a 32-bit RGBA pygame surface to a destination
 * surface of a given size.
 *
 * pysrc - The source pygame surface, which must be 32-bit RGBA.
 * pydst - The destination pygame surface, which should be 32-bit
 * RGBA, and locked.
 * avgwidth - The width of the pixels that will be averaged together.
 * avgheight - The height of the pixels that will be averaged
 * together.
 * outwidth - The width of pixels that will be written to the output.
 * outheight - The height of pixels that will be written to the
 * output.
 *
 * We assume that pysrc and pydst have been locked before we are called.
 */
void pixellate24_core(PyObject *pysrc,
                      PyObject *pydst,
                      int avgwidth,
                      int avgheight,
                      int outwidth,
                      int outheight
    ) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int x, y, i, j;
    int srcpitch, dstpitch;
    int srcw, srch;
    int dstw, dsth;
    int vw, vh;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

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

    /* Compute the virtual width and height. */
    vw = ( srcw + avgwidth - 1) / avgwidth;
    vh = ( srch + avgheight - 1) / avgheight;

    /* Iterate through each of the virtual pixels. */

    for (y = 0; y < vh; y++) {
        int srcy = avgheight * y;
        int dsty = outheight * y;

        int srcylimit = srcy + avgheight;
        int dstylimit = dsty + outheight;

        if (srcylimit > srch) {
            srcylimit = srch;
        }

        if (dstylimit > dsth) {
            dstylimit = dsth;
        }

        for (x = 0; x < vw; x++) {
            int srcx = avgwidth * x;
            int dstx = outwidth * x;

            int srcxlimit = srcx + avgwidth;
            int dstxlimit = dstx + outheight;

            if (srcxlimit > srcw) {
                srcxlimit = srcw;
            }

            if (dstxlimit > dstw) {
                dstxlimit = dstw;
            }

            // Please note that these names are just
            // suggestions... It's possible that blue will be
            // in r, for example.
            int r = 0;
            int g = 0;
            int b = 0;

            int number = 0;

            // pos always points to the start of the current line.
            unsigned char *pos = &srcpixels[srcy * srcpitch + srcx * 3];

            /* Sum up the pixel values. */

            for (j = srcy; j < srcylimit; j++) {
                // po points to the current pixel.
                unsigned char *po = pos;

                for (i = srcx; i < srcxlimit; i++) {
                    r += *po++;
                    g += *po++;
                    b += *po++;
                    number += 1;
                }

                pos += srcpitch;
            }

            /* Compute the average pixel values. */
            r /= number;
            g /= number;
            b /= number;

            /* Write out the average pixel values. */
            pos = &dstpixels[dsty * dstpitch + dstx * 3];
            for (j = dsty; j < dstylimit; j++) {
                unsigned char *po = pos;

                for (i = dstx; i < dstxlimit; i++) {
                    *po++ = r;
                    *po++ = g;
                    *po++ = b;
                }

                pos += dstpitch;
            }
        }
    }

    Py_END_ALLOW_THREADS

}

/*
 * This expects pysrc and pydst to be surfaces of the same size. It
 * the source surface to the destination surface, using the r, g, b,
 * and a maps. These maps are expected to be 256 bytes long, with each
 * byte corresponding to a possible value of a channel in pysrc,
 * giving what that value is mapped to in pydst.
 */
void map32_core(PyObject *pysrc,
                PyObject *pydst,
                char *rmap,
                char *gmap,
                char *bmap,
                char *amap) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int x, y;
    int srcpitch, dstpitch;
    int srcw, srch;

    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    srch = src->h;

    srcrow = srcpixels;
    dstrow = dstpixels;

    for (y = 0; y < srch; y++) {
        srcp = srcrow;
        dstp = dstrow;


        for (x = 0; x < srcw; x++) {
            *dstp++ = rmap[(unsigned char) *srcp++];
            *dstp++ = gmap[(unsigned char) *srcp++];
            *dstp++ = bmap[(unsigned char) *srcp++];
            *dstp++ = amap[(unsigned char) *srcp++];
        }

        srcrow += srcpitch;
        dstrow += dstpitch;
    }

    Py_END_ALLOW_THREADS
}

void map24_core(PyObject *pysrc,
                PyObject *pydst,
                char *rmap,
                char *gmap,
                char *bmap) {


    SDL_Surface *src;
    SDL_Surface *dst;

    int x, y;
    int srcpitch, dstpitch;
    int srcw, srch;

    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    srch = src->h;

    srcrow = srcpixels;
    dstrow = dstpixels;

    for (y = 0; y < srch; y++) {
        srcp = srcrow;
        dstp = dstrow;


        for (x = 0; x < srcw; x++) {
            *dstp++ = rmap[(unsigned char) *srcp++];
            *dstp++ = gmap[(unsigned char) *srcp++];
            *dstp++ = bmap[(unsigned char) *srcp++];
        }

        srcrow += srcpitch;
        dstrow += dstpitch;
    }

    Py_END_ALLOW_THREADS
}

/*
 * This expects pysrc and pydst to be surfaces of the same size. It
 * the source surface to the destination surface, using the r, g, b,
 * and a maps. These maps are expected to be 256 bytes long, with each
 * byte corresponding to a possible value of a channel in pysrc,
 * giving what that value is mapped to in pydst.
 */
void linmap32_core(PyObject *pysrc,
                PyObject *pydst,
                int rmul,
                int gmul,
                int bmul,
                int amul) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int x, y;
    int srcpitch, dstpitch;
    int srcw, srch;

    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    srch = src->h;

    srcrow = srcpixels;
    dstrow = dstpixels;

    for (y = 0; y < srch; y++) {
        srcp = srcrow;
        dstp = dstrow;


        for (x = 0; x < srcw; x++) {
            *dstp++ = ((unsigned char) *srcp++) * rmul >> 8;
            *dstp++ = ((unsigned char) *srcp++) * gmul >> 8;
            *dstp++ = ((unsigned char) *srcp++) * bmul >> 8;
            *dstp++ = ((unsigned char) *srcp++) * amul >> 8;
        }

        srcrow += srcpitch;
        dstrow += dstpitch;
    }

    Py_END_ALLOW_THREADS
}

void linmap24_core(PyObject *pysrc,
                PyObject *pydst,
                int rmul,
                int gmul,
                int bmul) {


    SDL_Surface *src;
    SDL_Surface *dst;

    int x, y;
    int srcpitch, dstpitch;
    int srcw, srch;

    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    srch = src->h;

    srcrow = srcpixels;
    dstrow = dstpixels;

    for (y = 0; y < srch; y++) {
        srcp = srcrow;
        dstp = dstrow;


        for (x = 0; x < srcw; x++) {
            *dstp++ = ((unsigned char) *srcp++) * rmul >> 8;
            *dstp++ = ((unsigned char) *srcp++) * gmul >> 8;
            *dstp++ = ((unsigned char) *srcp++) * bmul >> 8;
        }

        srcrow += srcpitch;
        dstrow += dstpitch;
    }

    Py_END_ALLOW_THREADS
}

/*
 * Helper function to describe averaging filters (AFs) needed to
 * approximate a specific Gaussian. Takes a desired standard deviation
 * and number of passes and produces lower and upper AF widths and the
 * number of passes to perform with the lower AF width.
 * ref: Peter Kovesi, "Fast Almost-Gaussian Filtering", 2010
 *      section II; equations 3 and 5
 *      https://www.peterkovesi.com/papers/FastGaussianSmoothing.pdf
 */
void blur_filters(float sigma, int n, int *wl, int *wu, int *m) {
    *wl = (int) floor(sqrt(12 * sigma * sigma / n + 1));
    if (*wl % 2 == 0) (*wl)--;
    *wu = *wl + 2;
    *m = (int) round(
        (12 * sigma * sigma - n * *wl * *wl - 4 * n * *wl - 3 * n)
        / (-4 * *wl - 4)
    );
}

/*
 * This expects pysrc, pywrk and pydst to be surfaces of the same size.
 * It approximates a Gaussian blur using several box blurs. Box sizes
 * are AF widths as described by blur_filters. Box blurs are performed
 * using two passes of a one-dimensional blur, on the x and y axes
 * respectively. The pywrk surface is used to hold intermediate results
 * only and should not be treated as valid output.
 * ref: Ivan Kutskir, "Fastest Gaussian Blur (in linear time)", 2013
 *      http://blog.ivank.net/fastest-gaussian-blur.html
 */
void blur32_core(PyObject *pysrc,
                 PyObject *pywrk,
                 PyObject *pydst,
                 float xrad,
                 float yrad) {

    int n = 3; // number of passes, no more than six

    int xl, xu, xm;
    int yl, yu, ym;

    blur_filters(xrad, n, &xl, &xu, &xm);

    if (xrad != yrad) {
        blur_filters(yrad, n, &yl, &yu, &ym);
    } else {
        yl = xl; yu = xu; ym = xm;
    }

    for (int i = 0; i < n; i++) {
        int xr = i < xm ? xl : xu;
        linblur32_core(pysrc, pywrk, xr, 0);
        int yr = i < ym ? yl : yu;
        linblur32_core(pywrk, pydst, yr, 1);
        pysrc = pydst;
    }
}

void blur24_core(PyObject *pysrc,
                 PyObject *pywrk,
                 PyObject *pydst,
                 float xrad,
                 float yrad) {

    int n = 3; // number of passes, no more than six

    int xl, xu, xm;
    int yl, yu, ym;

    blur_filters(xrad, n, &xl, &xu, &xm);

    if (xrad != yrad) {
        blur_filters(yrad, n, &yl, &yu, &ym);
    } else {
        yl = xl; yu = xu; ym = xm;
    }

    for (int i = 0; i < n; i++) {
        int xr = i < xm ? xl : xu;
        linblur24_core(pysrc, pywrk, xr, 0);
        int yr = i < ym ? yl : yu;
        linblur24_core(pywrk, pydst, yr, 1);
        pysrc = pydst;
    }
}

/*
 * This expects pysrc and pydst to be surfaces of the same size. It
 * implements a linear time one-dimensional blur using accumulators,
 * with a sample size of twice the radius plus one. It can operate in
 * both the x and y axes.
 */
void linblur32_core(PyObject *pysrc,
                    PyObject *pydst,
                    int radius,
                    int vertical) {

    int c, r;

    SDL_Surface *src;
    SDL_Surface *dst;

    int rows, cols;
    int incr, skip;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

    unsigned char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;

    if (vertical) {
        rows = dst->w;
        skip = 4;
        incr = dst->pitch - 4;
        cols = dst->h;
    } else {
        rows = dst->h;
        skip = dst->pitch;
        incr = 0;
        cols = dst->w;
    }

    int divisor = radius * 2 + 1;

    for (r = 0; r < rows; r++) {
        // The values of the pixels on the left and right ends of the
        // line.
        unsigned char lr, lg, lb, la;
        unsigned char rr, rg, rb, ra;

        unsigned char *leader = srcpixels + r * skip;
        unsigned char *trailer = leader;
        dstp = dstpixels + r * skip;

        lr = *leader;
        lg = *(leader + 1);
        lb = *(leader + 2);
        la = *(leader + 3);

        int sumr = lr * radius;
        int sumg = lg * radius;
        int sumb = lb * radius;
        int suma = la * radius;

        for (c = 0; c < radius; c++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            suma += *leader++;
            leader += incr;
        }

        // left side of the kernel is off of the screen.
        for (c = 0; c < radius; c++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            suma += *leader++;
            leader += incr;

            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            *dstp++ = suma / divisor;
            dstp += incr;

            sumr -= lr;
            sumg -= lg;
            sumb -= lb;
            suma -= la;
        }

        int end = cols - radius - 1;

        // The kernel is fully on the screen.
        for (; c < end; c++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            suma += *leader++;
            leader += incr;

            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            *dstp++ = suma / divisor;
            dstp += incr;

            sumr -= *trailer++;
            sumg -= *trailer++;
            sumb -= *trailer++;
            suma -= *trailer++;
            trailer += incr;
        }

        rr = *leader++;
        rg = *leader++;
        rb = *leader++;
        ra = *leader++;

        // The kernel is off the right side of the screen.
        for (; c < cols; c++) {
            sumr += rr;
            sumg += rg;
            sumb += rb;
            suma += ra;

            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            *dstp++ = suma / divisor;
            dstp += incr;

            sumr -= *trailer++;
            sumg -= *trailer++;
            sumb -= *trailer++;
            suma -= *trailer++;
            trailer += incr;
        }
    }

    Py_END_ALLOW_THREADS
}

void linblur24_core(PyObject *pysrc,
                    PyObject *pydst,
                    int radius,
                    int vertical) {

    int c, r;

    SDL_Surface *src;
    SDL_Surface *dst;

    int rows, cols;
    int incr, skip;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

    unsigned char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;

    if (vertical) {
        rows = dst->w;
        skip = 3;
        incr = dst->pitch - 3;
        cols = dst->h;
    } else {
        rows = dst->h;
        skip = dst->pitch;
        incr = 0;
        cols = dst->w;
    }

    int divisor = radius * 2 + 1;

    for (r = 0; r < rows; r++) {
        // The values of the pixels on the left and right ends of the
        // line.
        unsigned char lr, lg, lb;
        unsigned char rr, rg, rb;

        unsigned char *leader = srcpixels + r * skip;
        unsigned char *trailer = leader;
        dstp = dstpixels + r * skip;

        lr = *leader;
        lg = *(leader + 1);
        lb = *(leader + 2);

        int sumr = lr * radius;
        int sumg = lg * radius;
        int sumb = lb * radius;

        for (c = 0; c < radius; c++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            leader += incr;
        }

        // left side of the kernel is off of the screen.
        for (c = 0; c < radius; c++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            leader += incr;

            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            dstp += incr;

            sumr -= lr;
            sumg -= lg;
            sumb -= lb;
        }

        int end = cols - radius - 1;

        // The kernel is fully on the screen.
        for (; c < end; c++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            leader += incr;

            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            dstp += incr;

            sumr -= *trailer++;
            sumg -= *trailer++;
            sumb -= *trailer++;
            trailer += incr;
        }

        rr = *leader++;
        rg = *leader++;
        rb = *leader++;

        // The kernel is off the right side of the screen.
        for (; c < cols; c++) {
            sumr += rr;
            sumg += rg;
            sumb += rb;

            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            dstp += incr;

            sumr -= *trailer++;
            sumg -= *trailer++;
            sumb -= *trailer++;
            trailer += incr;
        }
    }

    Py_END_ALLOW_THREADS
}

// Alpha Munge takes a channel from the source pixel, maps it, and
// sticks it into the alpha channel of the destination, overwriting
// the destination's alpha channel.
//
// It's used to implement SmartDissolve.

void alphamunge_core(PyObject *pysrc,
                     PyObject *pydst,
                     int src_bypp, // bytes per pixel.
                     int src_aoff, // alpha offset.
                     int dst_aoff, // alpha offset.
                     char *amap) {

    int x, y;

    SDL_Surface *src;
    SDL_Surface *dst;

    int srcpitch, dstpitch;
    int dstw, dsth;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

    unsigned char *srcline;
    unsigned char *dstline;

    unsigned char *srcp;
    unsigned char *dstp;


    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    dstw = dst->w;
    dsth = dst->h;


    // We assume that src is bigger than dst, and so use dst
    // to handle everything.

    srcline = srcpixels;
    dstline = dstpixels;

    for (y = 0; y < dsth; y++) {

        srcp = srcline + src_aoff;
        dstp = dstline + dst_aoff;

        for (x = 0; x < dstw; x++) {

            *dstp = amap[*srcp];
            srcp += src_bypp;
            dstp += 4; // Need an alpha channel.
        }

        srcline += srcpitch;
        dstline += dstpitch;

    }

    Py_END_ALLOW_THREADS
}

void scale32_core(PyObject *pysrc, PyObject *pydst,
                  float source_xoff, float source_yoff,
                  float source_width, float source_height,
                  float dest_xoff, float dest_yoff,
                  float dest_width, float dest_height,
                  int precise
    ) {


    SDL_Surface *src;
    SDL_Surface *dst;

    int y;
    int srcpitch, dstpitch;
    int dstw, dsth;
    float xdelta, ydelta;

    unsigned char *srcpixels;
    unsigned char *dstpixels;


    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    dstw = dst->w;
    dsth = dst->h;

    if (precise) {

        if (dest_width > 1) {
            xdelta = 256.0 * (source_width - 1) / (dest_width - 1);
        } else {
            xdelta = 0;
        }

        if (dest_height > 1) {
            ydelta = 256.0 * (source_height - 1) / (dest_height - 1);
        } else {
            ydelta = 0;
        }

    } else {
        xdelta = 255.0 * (source_width - 1) / dest_width;
        ydelta = 255.0 * (source_height - 1) / dest_height;
    }

    for (y = 0; y < dsth; y++) {

        unsigned char *s0;
        unsigned char *d;
        unsigned char *dend;

        int sline;
        short s0frac;
        short s1frac;
        float scol;

        d = dstpixels + dstpitch * y;
        dend = d + 4 * dstw; // bpp

        sline = source_yoff * 256 + (y + dest_yoff) * ydelta;
        s1frac = (int) sline & 255;
        s0frac = 256 - s1frac;

        s0 = srcpixels + (sline >> 8) * srcpitch;

        scol = source_xoff * 256 + dest_xoff * xdelta;

        while (d < dend) {

            unsigned char *s0p;
            unsigned char *s1p;

            short xfrac = 256 - ((int) scol & 255);
            unsigned short r, g, b, a;

            s0p = s0 + ((int) scol >> 8) * 4; // bpp
            s1p = s0p + srcpitch;

            r = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            g = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            b = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            a = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;

            xfrac = 256 - xfrac;

            r += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            g += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            b += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            a += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;

            *d++ = r >> 8;
            *d++ = g >> 8;
            *d++ = b >> 8;
            *d++ = a >> 8;

            scol += xdelta;
        }
    }

    Py_END_ALLOW_THREADS
}


void scale24_core(PyObject *pysrc, PyObject *pydst,
                  float source_xoff, float source_yoff,
                  float source_width, float source_height,
                  float dest_xoff, float dest_yoff,
                  float dest_width, float dest_height) {


    SDL_Surface *src;
    SDL_Surface *dst;

    int y;
    int srcpitch, dstpitch;
    int dstw, dsth;
    float xdelta, ydelta;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    dstw = dst->w;
    dsth = dst->h;

    xdelta = 255.0 * (source_width - 1) / dest_width;
    ydelta = 255.0 * (source_height - 1) / dest_height;

    for (y = 0; y < dsth; y++) {

        unsigned char *s0;
        unsigned char *d;
        unsigned char *dend;

        int sline;
        short s0frac;
        short s1frac;
        float scol;

        d = dstpixels + dstpitch * y;
        dend = d + 3 * dstw; // bpp

        sline = source_yoff * 255 + (y + dest_yoff) * ydelta;
        s1frac = (int) sline & 255;
        s0frac = 256 - s1frac;

        s0 = srcpixels + (sline >> 8) * srcpitch;

        scol = source_xoff * 255 + dest_xoff * xdelta;

        while (d < dend) {

            unsigned char *s0p;
            unsigned char *s1p;

            short xfrac = 256 - ((int) scol & 255);
            unsigned short r, g, b;

            s0p = s0 + ((int) scol >> 8) * 3; // bpp
            s1p = s0p + srcpitch;

            r = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            g = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            b = (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;

            xfrac = 256 - xfrac;

            r += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            g += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;
            b += (((*s0p++ * s0frac) + (*s1p++ * s1frac)) >> 8) * xfrac;

            *d++ = r >> 8;
            *d++ = g >> 8;
            *d++ = b >> 8;

            scol += xdelta;
        }
    }

    Py_END_ALLOW_THREADS
}

#define I(a, b, mul) ((((((b - a) * mul)) >> 8) + a) & 0xff00ff)

/** This appears to limit the expansion, such that 1/x yields a max
    expansion of lg x */
#define EPSILON (1.0 / 256.0)

/****************************************************************************/
/* A similar concept to rotozoom, but implemented differently, so we
   can limit the target area. */
int transform32_std(PyObject *pysrc, PyObject *pydst,
                    float corner_x, float corner_y,
                    float xdx, float ydx,
                    float xdy, float ydy,
                    int ashift,
                    float a,
                    int precise
    ) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int y;
    int srcpitch, dstpitch;
    int srcw, srch;
    int dstw, dsth;

    // The x and y source pixel coordinates, times 65536. And their
    // delta-per-dest-x-pixel.
    int sxi = 0, syi = 0, dsxi = 0, dsyi = 0;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

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

    // Compute the coloring multiplier.
    unsigned int amul = (unsigned int) (a * 256);

    // Compute the maximum x and y coordinates.
    double maxsx = srcw;
    double maxsy = srch;

    // Deal with pre-6.10.1 versions of Ren'Py, which didn't give us
    // that 1px border that allows us to be precise.
    if (! precise) {
        maxsx -= EPSILON;
        maxsy -= EPSILON;

        // If a delta is too even, subtract epsilon (towards 0) from it.
        if (xdx && fabs(fmodf(1.0 / xdx, 1)) < EPSILON) {
            xdx -= (xdx / fabs(xdx)) * EPSILON;
        }
        if (xdy && fabs(fmodf(1.0 / xdy, 1)) < EPSILON) {
            xdy -= (xdy / fabs(xdy)) * EPSILON;
        }
        if (ydx && fabs(fmodf(1.0 / ydx, 1)) < EPSILON) {
            ydx -= (ydx / fabs(ydx)) * EPSILON;
        }
        if (ydy && fabs(fmodf(1.0 / ydy, 1)) < EPSILON) {
            ydy -= (ydy / fabs(ydy)) * EPSILON;
        }
    }


    // Loop through every line.
    for (y = 0; y < dsth; y++) {

        // The source coordinates of the leftmost pixel in the line.
        double leftsx = corner_x + y * xdy;
        double leftsy = corner_y + y * ydy;

        // Min and max x-extent to draw on the current line.
        double minx = 0;
        double maxx = dstw - 1;

        // Figure out the x-extent based on xdx.
        if (xdx) {
            double x1 = (0.0 - leftsx) / xdx;
            double x2 = (maxsx - leftsx) / xdx;

            if (x1 < x2) {
                minx = fmax(x1, minx);
                maxx = fmin(x2, maxx);
            } else {
                minx = fmax(x2, minx);
                maxx = fmin(x1, maxx);
            }

        } else {
            if (leftsx < 0 || leftsx > maxsx) {
               continue;
            }
        }

        // Figure out the x-extent based on ydx.
        if (ydx) {
            double x1 = (0.0 - leftsy) / ydx;
            double x2 = (maxsy - leftsy) / ydx;

            if (x1 < x2) {
                minx = fmax(x1, minx);
                maxx = fmin(x2, maxx);
            } else {
                minx = fmax(x2, minx);
                maxx = fmin(x1, maxx);
            }

        } else {
            if (leftsy < 0 || leftsy > maxsy) {
                continue;
            }
        }

        minx = ceil(minx);
        maxx = floor(maxx);

        if (minx >= maxx) {
            continue;
        }

        // The start and end of line pointers.
        unsigned char *d = dstpixels + dstpitch * y;
        unsigned char *dend = d + 4 * (int) maxx;

        // Advance start of line by 4.
        d += 4 * (int) minx;

        // Starting coordinates and deltas.
        sxi = (int) ((leftsx + minx * xdx) * 65536);
        syi = (int) ((leftsy + minx * ydx) * 65536);
        dsxi = (int) (xdx * 65536);
        dsyi = (int) (ydx * 65536);

        while (d <= dend) {

            int px = sxi >> 16;
            int py = syi >> 16;

            unsigned char *sp = srcpixels + py * srcpitch + px * 4;

            unsigned int yfrac = (syi >> 8) & 0xff; // ((short) sy) & 0xff;
            unsigned int xfrac = (sxi >> 8) & 0xff; // ((short) sx) & 0xff;

            unsigned int pal = *(unsigned int *) sp;
            unsigned int pbl = *(unsigned int *) (sp + 4);
            sp += srcpitch;
            unsigned int pcl = *(unsigned int *) sp;
            unsigned int pdl = *(unsigned int *) (sp + 4);

            unsigned int pah = (pal >> 8) & 0xff00ff;
            unsigned int pbh = (pbl >> 8) & 0xff00ff;
            unsigned int pch = (pcl >> 8) & 0xff00ff;
            unsigned int pdh = (pdl >> 8) & 0xff00ff;

            pal &= 0xff00ff;
            pbl &= 0xff00ff;
            pcl &= 0xff00ff;
            pdl &= 0xff00ff;

            unsigned int rh = I(I(pah, pch, yfrac), I(pbh, pdh, yfrac), xfrac);
            unsigned int rl = I(I(pal, pcl, yfrac), I(pbl, pdl, yfrac), xfrac);

            unsigned int alpha = (((rh << 8) | rl) >> ashift) & 0xff;
            alpha = (alpha * amul) >> 8;

            unsigned int dl = * (unsigned int *) d;
            unsigned int dh = (dl >> 8) & 0xff00ff;
            dl &= 0xff00ff;

            dl = I(dl, rl, alpha);
            dh = I(dh, rh, alpha);

            * (unsigned int *) d = (dh << 8) | dl;

            d += 4;
            sxi += dsxi;
            syi += dsyi;
        }

    }

    Py_END_ALLOW_THREADS;


    // This is bogus, and only serves to ensure that the FPU
    // computes these variables at the right times.
    return sxi + syi + dsxi + dsyi;
}




void transform32_core(PyObject *pysrc, PyObject *pydst,
                      float corner_x, float corner_y,
                      float xdx, float ydx,
                      float xdy, float ydy,
                      int ashift,
                      float a,
                      int precise
    ) {


    transform32_std(pysrc, pydst, corner_x, corner_y,
                    xdx, ydx, xdy, ydy, ashift, a, precise);

}




void blend32_core_std(PyObject *pysrca, PyObject *pysrcb, PyObject *pydst,
                      int alpha) {

    SDL_Surface *srca;
    SDL_Surface *srcb;
    SDL_Surface *dst;

    int srcapitch, srcbpitch, dstpitch;
    unsigned short dstw, dsth;
    unsigned short y;

    unsigned char *srcapixels;
    unsigned char *srcbpixels;
    unsigned char *dstpixels;

    srca = PySurface_AsSurface(pysrca);
    srcb = PySurface_AsSurface(pysrcb);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcapixels = (unsigned char *) srca->pixels;
    srcbpixels = (unsigned char *) srcb->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcapitch = srca->pitch;
    srcbpitch = srcb->pitch;
    dstpitch = dst->pitch;
    dstw = dst->w;
    dsth = dst->h;

    for (y = 0; y < dsth; y++) {

        unsigned int *dp = (unsigned int *)(dstpixels + dstpitch * y);
        unsigned int *dpe = dp + dstw;

        unsigned int *sap = (unsigned int *)(srcapixels + srcapitch * y);
        unsigned int *sbp = (unsigned int *)(srcbpixels + srcbpitch * y);

        while (dp < dpe) {
            unsigned int sal = *sap++;
            unsigned int sbl = *sbp++;

            unsigned int sah = (sal >> 8) & 0xff00ff;
            unsigned int sbh = (sbl >> 8) & 0xff00ff;

            sal &= 0xff00ff;
            sbl &= 0xff00ff;

            *dp++ = I(sal, sbl, alpha) | (I(sah, sbh, alpha) << 8);
        }
    }

    Py_END_ALLOW_THREADS

}

void blend32_core(PyObject *pysrca, PyObject *pysrcb, PyObject *pydst,
                  int alpha) {

    blend32_core_std(pysrca, pysrcb, pydst, alpha);
}


void imageblend32_core_std(PyObject *pysrca, PyObject *pysrcb,
                           PyObject *pydst, PyObject *pyimg,
                           int alpha_off, char *amap) {

    SDL_Surface *srca;
    SDL_Surface *srcb;
    SDL_Surface *dst;
    SDL_Surface *img;

    int srcapitch, srcbpitch, dstpitch, imgpitch;
    unsigned short dstw, dsth;
    unsigned short y;

    unsigned char *srcapixels;
    unsigned char *srcbpixels;
    unsigned char *dstpixels;
    unsigned char *imgpixels;

    srca = PySurface_AsSurface(pysrca);
    srcb = PySurface_AsSurface(pysrcb);
    dst = PySurface_AsSurface(pydst);
    img = PySurface_AsSurface(pyimg);

    Py_BEGIN_ALLOW_THREADS

    srcapixels = (unsigned char *) srca->pixels;
    srcbpixels = (unsigned char *) srcb->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    imgpixels = (unsigned char *) img->pixels;
    srcapitch = srca->pitch;
    srcbpitch = srcb->pitch;
    dstpitch = dst->pitch;
    imgpitch = img->pitch;

    dstw = dst->w;
    dsth = dst->h;

    for (y = 0; y < dsth; y++) {

        unsigned int *dp = (unsigned int *)(dstpixels + dstpitch * y);
        unsigned int *dpe = dp + dstw;

        unsigned int *sap = (unsigned int *)(srcapixels + srcapitch * y);
        unsigned int *sbp = (unsigned int *)(srcbpixels + srcbpitch * y);

        unsigned char *ip = (unsigned char *)(imgpixels + imgpitch * y);
        ip += alpha_off;

        while (dp < dpe) {
            unsigned char alpha = (unsigned char) amap[*ip];
            ip += 4;

            unsigned int sal = *sap++;
            unsigned int sbl = *sbp++;

            unsigned int sah = (sal >> 8) & 0xff00ff;
            unsigned int sbh = (sbl >> 8) & 0xff00ff;

            sal &= 0xff00ff;
            sbl &= 0xff00ff;

            *dp++ = I(sal, sbl, alpha) | (I(sah, sbh, alpha) << 8);
        }
    }

    Py_END_ALLOW_THREADS
}


void imageblend32_core(PyObject *pysrca, PyObject *pysrcb,
                       PyObject *pydst, PyObject *pyimg,
                       int aoff, char *amap) {

    imageblend32_core_std(pysrca, pysrcb, pydst, pyimg, aoff, amap);
}


void colormatrix32_core(PyObject *pysrc, PyObject *pydst,
                        float c00, float c01, float c02, float c03, float c04,
                        float c10, float c11, float c12, float c13, float c14,
                        float c20, float c21, float c22, float c23, float c24,
                        float c30, float c31, float c32, float c33, float c34) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int srcpitch, dstpitch;
    unsigned short dstw, dsth;
    unsigned short y;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;

    dstw = dst->w;
    dsth = dst->h;

    int o0 = c04 * 255;
    int o1 = c14 * 255;
    int o2 = c24 * 255;
    int o3 = c34 * 255;

    for (y = 0; y < dsth; y++) {

        int r;

        unsigned char *dp =  dstpixels + dstpitch * y;
        unsigned char *dpe = dp + dstw * 4;
        unsigned char *sp = srcpixels + srcpitch * y;

        while (dp < dpe) {
            unsigned char s0 = *sp++;
            unsigned char s1 = *sp++;
            unsigned char s2 = *sp++;
            unsigned char s3 = *sp++;

/*             *dp++ = (unsigned char) */
/*                 fminf(255, fmaxf(0, fmaf(s0, c00, fmaf(s1, c01, fmaf(s2, c02, fmaf(s3, c03, o0)))))); */
/*             *dp++ = (unsigned char) */
/*                 fminf(255, fmaxf(0, fmaf(s0, c10, fmaf(s1, c11, fmaf(s2, c12, fmaf(s3, c13, o1)))))); */
/*             *dp++ = (unsigned char) */
/*                 fminf(255, fmaxf(0, fmaf(s0, c20, fmaf(s1, c21, fmaf(s2, c22, fmaf(s3, c23, o2)))))); */
/*             *dp++ = (unsigned char) */
/*                 fminf(255, fmaxf(0, fmaf(s0, c30, fmaf(s1, c31, fmaf(s2, c32, fmaf(s3, c33, o3)))))); */

            r = o0 + (int) (c00 * s0 + c01 * s1 + c02 * s2 + c03 * s3);
            if (r < 0) r = 0;
            if (r > 255) r = 255;
            *dp++ = r;

            r = o1 + (int) (c10 * s0 + c11 * s1 + c12 * s2 + c13 * s3);
            if (r < 0) r = 0;
            if (r > 255) r = 255;
            *dp++ = r;

            r = o2 + (int) (c20 * s0 + c21 * s1 + c22 * s2 + c23 * s3);
            if (r < 0) r = 0;
            if (r > 255) r = 255;
            *dp++ = r;

            r = o3 + (int) (c30 * s0 + c31 * s1 + c32 * s2 + c33 * s3);
            if (r < 0) r = 0;
            if (r > 255) r = 255;
            *dp++ = r;
        }
    }

    Py_END_ALLOW_THREADS
}

void staticgray_core(PyObject *pysrc, PyObject *pydst,
                     int rmul, int gmul, int bmul, int amul, int shift, char *vmap) {

    SDL_Surface *src;
    SDL_Surface *dst;

    int srcpitch, dstpitch;
    unsigned short dstw, dsth;
    unsigned short x, y;

    unsigned char *srcpixels;
    unsigned char *dstpixels;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);

    Py_BEGIN_ALLOW_THREADS;

    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;

    dstw = dst->w;
    dsth = dst->h;

    for (y = 0; y < dsth; y++) {
        unsigned char *s = &srcpixels[y * srcpitch];
        unsigned char *d = &dstpixels[y * dstpitch];

        for (x = 0; x < dstw; x++) {
            int sum = 0;

            sum += *s++ * rmul;
            sum += *s++ * gmul;
            sum += *s++ * bmul;
            sum += *s++ * amul;
            *d++ = (unsigned char) vmap[sum >> shift];
        }
    }

    Py_END_ALLOW_THREADS;
}
