#include "renpy.h"
#include <pygame/pygame.h>
#include "IMG_savepng.h"
#include <stdio.h>

// Shows how to do this.
#if SDL_BYTEORDER == SDL_BIG_ENDIAN
#endif 

/* Initializes the stuff found in this file.
 */
void core_init() {
    import_pygame_base();
    import_pygame_surface();
}

void save_png_core(PyObject *pysurf, SDL_RWops *rw, int compress) {
    SDL_Surface *surf;
    
    surf = PySurface_AsSurface(pysurf);

    IMG_SavePNG_RW(rw, surf, compress);
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
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    int vw, vh;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
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
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    int vw, vh;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
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
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    
    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

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

}

void map24_core(PyObject *pysrc,
                PyObject *pydst,
                char *rmap,
                char *gmap,
                char *bmap) {


    SDL_Surface *src;
    SDL_Surface *dst;
    
    int x, y;
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    
    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

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
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    
    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

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

}

void linmap24_core(PyObject *pysrc,
                PyObject *pydst,
                int rmul,
                int gmul,
                int bmul) {


    SDL_Surface *src;
    SDL_Surface *dst;
    
    int x, y;
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    
    char *srcpixels;
    char *dstpixels;

    char *srcrow;
    char *dstrow;
    char *srcp;
    char *dstp;

    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (char *) src->pixels;
    dstpixels = (char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

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

}


#if 0

void xblur32_core(PyObject *pysrc,
                  PyObject *pydst,
                  int radius) {
    
    int i, x, y;

    SDL_Surface *src;
    SDL_Surface *dst;
    
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    int count;

    unsigned char *srcp;
    unsigned char *dstp;

    
    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

    int divisor = radius * 2 + 1;
    
    for (y = 0; y < dsth; y++) {

        // The values of the pixels on the left and right ends of the
        // line. 
        unsigned char lr, lg, lb, la;
        unsigned char rr, rg, rb, ra;
        
        unsigned char *leader = srcpixels + y * srcpitch;
        unsigned char *trailer = leader;
        dstp = dstpixels + y * dstpitch;

        lr = *leader;
        lg = *(leader + 1);
        lb = *(leader + 2);
        la = *(leader + 3);
        
        int sumr = lr * radius;
        int sumg = lg * radius;
        int sumb = lb * radius;
        int suma = la * radius;


        for (x = 0; x < radius + 0; x++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            suma += *leader++;
        }
        
        // left side of the kernel is off of the screen.
        for (x = 0; x < radius; x++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            suma += *leader++;
            
            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            *dstp++ = suma / divisor;

            sumr -= lr;
            sumg -= lg;
            sumb -= lb;
            suma -= la;
        }

        int end = srcw - radius - 1;
        
        // The kernel is fully on the screen.
        for (; x < end; x++) {
            sumr += *leader++;
            sumg += *leader++;
            sumb += *leader++;
            suma += *leader++;
            
            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            *dstp++ = suma / divisor;

            sumr -= *trailer++;
            sumg -= *trailer++;
            sumb -= *trailer++;
            suma -= *trailer++;
        }

        rr = *leader++;
        rg = *leader++;
        rb = *leader++;
        ra = *leader++;
               
        // The kernel is off the right side of the screen.
        for (; x < srcw; x++) {
            sumr += rr;
            sumg += rg;
            sumb += rb;
            suma += ra;
            
            *dstp++ = sumr / divisor;
            *dstp++ = sumg / divisor;
            *dstp++ = sumb / divisor;
            *dstp++ = suma / divisor;

            sumr -= *trailer++;
            sumg -= *trailer++;
            sumb -= *trailer++;
            suma -= *trailer++;
        }    
    }
}

#endif


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
    
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    unsigned char *srcline;
    unsigned char *dstline;
    
    unsigned char *srcp;
    unsigned char *dstp;

    
    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
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
}
        
/* int stretch_core(PyObject *pysrc, PyObject *pydst, int x, int y, int w, int h) { */
/*     SDL_Surface *src; */
/*     SDL_Surface *dst; */
/*     SDL_Rect rect; */
    
/*     src = PySurface_AsSurface(pysrc); */
/*     dst = PySurface_AsSurface(pydst); */

/*     rect.x = x; */
/*     rect.y = y; */
/*     rect.w = w; */
/*     rect.h = h; */
    
/*     SDL_StretchSurfaceBlit(src, &rect, dst, NULL); */
/* } */



void scale32_core(PyObject *pysrc, PyObject *pydst) {

    SDL_Surface *src;
    SDL_Surface *dst;
    
    int x, y, i, j;
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    short xdelta, ydelta;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    
    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

    xdelta = 255 * srcw / dstw;
    ydelta = 255 * srch / dsth;

    for (y = 0; y < dsth; y++) {

        unsigned char *s0;
        unsigned char *s1;
        unsigned char *d;
        unsigned char *dend;

        int sline;
        short s0frac;
        short s1frac;
        int scol;
        
        d = dstpixels + dstpitch * y;
        dend = d + 4 * dstw; // bpp

        sline = y * ydelta;
        s1frac = sline & 255;
        s0frac = 256 - s1frac;

        s0 = srcpixels + (sline >> 8) * srcpitch;
        s1 = s0 + srcpitch;

        scol = 0;

        while (d < dend) {

            unsigned char *s0p;
            unsigned char *s1p;

            short xfrac = 256 - (scol & 255);
            unsigned short r, g, b, a;
            
            s0p = s0 + (scol >> 8) * 4; // bpp
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
}

void scale24_core(PyObject *pysrc, PyObject *pydst) {

    SDL_Surface *src;
    SDL_Surface *dst;
    
    int x, y, i, j;
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    short xdelta, ydelta;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    
    src = PySurface_AsSurface(pysrc);
    dst = PySurface_AsSurface(pydst);
        
    srcpixels = (unsigned char *) src->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcpitch = src->pitch;
    dstpitch = dst->pitch;
    srcw = src->w;
    dstw = dst->w;
    srch = src->h;
    dsth = dst->h;

    xdelta = 255 * srcw / dstw;
    ydelta = 255 * srch / dsth;

    for (y = 0; y < dsth; y++) {

        unsigned char *s0;
        unsigned char *s1;
        unsigned char *d;
        unsigned char *dend;

        int sline;
        short s0frac;
        short s1frac;
        int scol;
        
        d = dstpixels + dstpitch * y;
        dend = d + 3 * dstw; // bpp

        sline = y * ydelta;
        s1frac = sline & 255;
        s0frac = 256 - s1frac;

        s0 = srcpixels + (sline >> 8) * srcpitch;
        s1 = s0 + srcpitch;

        scol = 0;

        while (d < dend) {

            unsigned char *s0p;
            unsigned char *s1p;

            short xfrac = 256 - (scol & 255);
            unsigned short r, g, b;
            
            s0p = s0 + (scol >> 8) * 3; // bpp
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
}

