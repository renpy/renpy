#include "renpy.h"
#include <pygame/pygame.h>
#include "IMG_savepng.h"
#include <stdio.h>
#include <math.h>


#if defined(__GNUC__) && (defined(__i386__) || defined(__x86_64__))
#define GCC_MMX 1
#include "mmx.h"
#endif


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
        
void scale32_core(PyObject *pysrc, PyObject *pydst,
                  float source_xoff, float source_yoff,
                  float source_width, float source_height,
                  float dest_xoff, float dest_yoff,
                  float dest_width, float dest_height) {


    SDL_Surface *src;
    SDL_Surface *dst;
    
    int y;
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    float xdelta, ydelta;
    
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

    xdelta = 255.0 * (source_width - 1) / dest_width;
    ydelta = 255.0 * (source_height - 1) / dest_height;

    for (y = 0; y < dsth; y++) {

        unsigned char *s0;
        unsigned char *s1;
        unsigned char *d;
        unsigned char *dend;

        int sline;
        short s0frac;
        short s1frac;
        float scol;
        
        d = dstpixels + dstpitch * y;
        dend = d + 4 * dstw; // bpp

        sline = source_yoff * 255 + (y + dest_yoff) * ydelta;
        s1frac = (int) sline & 255;
        s0frac = 256 - s1frac;

        s0 = srcpixels + (sline >> 8) * srcpitch;
        s1 = s0 + srcpitch;

        scol = source_xoff * 255 + dest_xoff * xdelta;

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
}


void scale24_core(PyObject *pysrc, PyObject *pydst,
                  float source_xoff, float source_yoff,
                  float source_width, float source_height,
                  float dest_xoff, float dest_yoff,
                  float dest_width, float dest_height) {


    SDL_Surface *src;
    SDL_Surface *dst;
    
    int y;
    Uint32 srcpitch, dstpitch;
    Uint32 srcw, srch;
    Uint32 dstw, dsth;
    float xdelta, ydelta;
    
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

    xdelta = 255.0 * (source_width - 1) / dest_width;
    ydelta = 255.0 * (source_height - 1) / dest_height;

    for (y = 0; y < dsth; y++) {

        unsigned char *s0;
        unsigned char *s1;
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
        s1 = s0 + srcpitch;

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
}

/****************************************************************************/
/* A similar concept to rotozoom, but implemented differently, so we
   can limit the target area. */
void transform32_core(PyObject *pysrc, PyObject *pydst,
                      float corner_x, float corner_y,
                      float xdx, float ydx,
                      float xdy, float ydy) {

    SDL_Surface *src;
    SDL_Surface *dst;
    
    int y;
    int srcpitch, dstpitch;
    int srcw, srch;
    int dstw, dsth;
    
    unsigned char *srcpixels;
    unsigned char *dstpixels;

    float lsx, lsy; // The position of the current line in the source.
    float sx, sy; // The position of the current pixel in the source.
    
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

    lsx = corner_x * 256;
    lsy = corner_y * 256;

    xdx *= 256;
    ydx *= 256;
    xdy *= 256;
    ydy *= 256;


    // Scaled subtracted srcw and srch.
    float fsw = (srcw - 2) * 256;
    float fsh = (srch - 2) * 256;
    
    
    for (y = 0; y < dsth; y++, lsx += xdy, lsy += ydy) {

        sx = lsx;
        sy = lsy;
        
        // unsigned char *d = dstpixels + dstpitch * y;
        // unsigned char *dend = d + 4 * dstw;

        float minx = 0;
        float maxx = dstw - 1;

        if (xdx != 0) {
            float d1 = -lsx / xdx;
            float d2 = (fsw - lsx) / xdx;

            minx = fmaxf(minx, fminf(d1, d2)); 
            maxx = fminf(maxx, fmaxf(d1, d2)); 
            
//            printf("ZZZ1 %f %f\n", d1, d2);
        } else if ( lsx < 0 || lsx >= fsw) {
            continue;
        }

        if (ydx != 0) {
            float d1 = -lsy / ydx;
            float d2 = (fsh - lsy) / ydx;

            minx = fmaxf(minx, fminf(d1, d2)); 
            maxx = fminf(maxx, fmaxf(d1, d2)); 
//            printf("ZZZ2 %f %f\n", d1, d2);
        } else if ( lsy < 0 || lsy >= fsh) {
            continue;
        }

        if (minx > maxx) {
            continue;
        }

//        printf("CCC %f %f\n", minx, maxx); 
        
        minx = ceil(minx);
        maxx = floor(maxx);

//        printf("CCC2 %f %f\n", minx, maxx); 
//        printf("XXX %f %f %f %f\n", lsx / 256, xdx / 256, lsy / 256, ydx/256);

        
        // printf("%f %f\n", minx, maxx);
        
        // printf("Minx at: %f %f\n", (lsx + xdx * minx) / 256, (lsy + ydx * minx) / 256);

        
        unsigned char *d = dstpixels + dstpitch * y;
        unsigned char *dend = d + 4 * (int) maxx;
        d += 4 * (int) minx;

        sx += minx * xdx;
        sy += minx * ydx;
                
        
        while (d <= dend) {

            int px, py, sxi, syi;
            sxi = ((int) sx);
            syi = ((int) sy);                
            px = sxi >> 8;
            py = syi >> 8;


            /* These bounds are checked analytically, hence the if (1)
             * { */
            
            // if (0 <= px && px < srcw - 1 && 0 <= py && py < srch - 1) {
            if (1) {
                
                unsigned char *sp = srcpixels + py * srcpitch + px * 4;

                // unsigned char *s1p = s0p + srcpitch;
                
                int s1frac = syi & 0xff; // ((short) sy) & 0xff;
                int xfrac = sxi & 0xff; // ((short) sx) & 0xff;

#define I(a, b, mul) ((((((b - a) * mul)) >> 8) + a) & 0xff00ff)
                
                unsigned int rl, rh;

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

                // if (y == 10)
                // printf("%x %x %x %x\n", pah, pbh, pch, pdh);
                

                rh = I(I(pah, pch, s1frac), I(pbh, pdh, s1frac), xfrac);
                rl = I(I(pal, pcl, s1frac), I(pbl, pdl, s1frac), xfrac);
                // rl = 0;

                // if (y == 10) 
                // printf("%x\n", rh);
                
                * (unsigned int *) d = (rh << 8) | rl;

                d += 4;
                

            } else {
                // This code can't execute.

                printf("Failed x %f (%d, %d)\n", minx, px, py);
 
                *d++ = 0;
                *d++ = 0;
                *d++ = 0;
                *d++ = 0;                

            }
            
            sx += xdx;
            sy += ydx;
            // minx++;
        }
    }
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
}

#ifdef GCC_MMX

void blend32_core_mmx(PyObject *pysrca, PyObject *pysrcb, PyObject *pydst,
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
        
    srcapixels = (unsigned char *) srca->pixels;
    srcbpixels = (unsigned char *) srcb->pixels;
    dstpixels = (unsigned char *) dst->pixels;
    srcapitch = srca->pitch;
    srcbpitch = srcb->pitch;
    dstpitch = dst->pitch;
    dstw = dst->w;
    dsth = dst->h;

    /* This code is a slightly modified version of that found in
     * SDL_blit_A.c */
    
    pxor_r2r(mm5, mm5); /* 0 -> mm5 */
    /* form the alpha mult */
    movd_m2r(alpha, mm4); /* 0000000A -> mm4 */
    punpcklwd_r2r(mm4, mm4); /* 00000A0A -> mm4 */
    punpckldq_r2r(mm4, mm4); /* 0A0A0A0A -> mm4 */
    
    for (y = 0; y < dsth; y++) {

        unsigned int *dp = (unsigned int *)(dstpixels + dstpitch * y);
        unsigned int *dpe = dp + dstw;

        unsigned int *sap = (unsigned int *)(srcapixels + srcapitch * y);
        unsigned int *sbp = (unsigned int *)(srcbpixels + srcbpitch * y);

        while (dp < dpe) {
            
            movd_m2r((*sbp++), mm1);
            movd_m2r((*sap++), mm2);
            punpcklbw_r2r(mm5, mm1); /* 0A0R0G0B -> mm1(b) */                                      
            punpcklbw_r2r(mm5, mm2); /* 0A0R0G0B -> mm2(a) */
            psubw_r2r(mm2, mm1);/* a - b -> mm1 */
            pmullw_r2r(mm4, mm1); /* mm1 * alpha -> mm1 */
            psrlw_i2r(8, mm1); /* mm1 >> 8 -> mm1 */
            paddb_r2r(mm1, mm2); /* mm1 + mm2(a) -> mm2 */
            packuswb_r2r(mm5, mm2); /* ARGBARGB -> mm2 */
            movd_r2m(mm2, *dp++);
            
            
        }
    }

    emms();
}
    
#endif

void blend32_core(PyObject *pysrca, PyObject *pysrcb, PyObject *pydst,
                  int alpha) {

#ifdef GCC_MMX
    static int checked_mmx = 0;
    static int has_mmx = 0;

    if (! checked_mmx) {
        has_mmx = SDL_HasMMX();
        checked_mmx = 1;
    }

    if (has_mmx) {
        blend32_core_mmx(pysrca, pysrcb, pydst, alpha);
        return;
    }
    
#endif

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
}

#ifdef GCC_MMX

void imageblend32_core_mmx(PyObject *pysrca, PyObject *pysrcb,
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

    pxor_r2r(mm5, mm5); /* 0 -> mm5 */

    for (y = 0; y < dsth; y++) {

        unsigned int *dp = (unsigned int *)(dstpixels + dstpitch * y);
        unsigned int *dpe = dp + dstw;

        unsigned int *sap = (unsigned int *)(srcapixels + srcapitch * y);
        unsigned int *sbp = (unsigned int *)(srcbpixels + srcbpitch * y);

        unsigned char *ip = (unsigned char *)(imgpixels + imgpitch * y);
        ip += alpha_off;
        
        while (dp < dpe) {
            unsigned int alpha = (unsigned char) amap[*ip];
            ip += 4;

            /* form the alpha mult */
            movd_m2r(alpha, mm4); /* 0000000A -> mm4 */
            punpcklwd_r2r(mm4, mm4); /* 00000A0A -> mm4 */
            punpckldq_r2r(mm4, mm4); /* 0A0A0A0A -> mm4 */
            
            movd_m2r((*sbp++), mm1);
            movd_m2r((*sap++), mm2);
            punpcklbw_r2r(mm5, mm1); /* 0A0R0G0B -> mm1(b) */                                      
            punpcklbw_r2r(mm5, mm2); /* 0A0R0G0B -> mm2(a) */
            psubw_r2r(mm2, mm1);/* a - b -> mm1 */
            pmullw_r2r(mm4, mm1); /* mm1 * alpha -> mm1 */
            psrlw_i2r(8, mm1); /* mm1 >> 8 -> mm1 */
            paddb_r2r(mm1, mm2); /* mm1 + mm2(a) -> mm2 */
            packuswb_r2r(mm5, mm2); /* ARGBARGB -> mm2 */
            movd_r2m(mm2, *dp++);
        }
    }

    emms();
}

#endif

void imageblend32_core(PyObject *pysrca, PyObject *pysrcb,
                       PyObject *pydst, PyObject *pyimg,
                       int aoff, char *amap) {

#ifdef GCC_MMX
    static int checked_mmx = 0;
    static int has_mmx = 0;

    if (! checked_mmx) {
        has_mmx = SDL_HasMMX();
        checked_mmx = 1;
    }

    if (has_mmx) {
        imageblend32_core_mmx(pysrca, pysrcb, pydst, pyimg, aoff, amap);
        return;
    }
    
#endif

    imageblend32_core_std(pysrca, pysrcb, pydst, pyimg, aoff, amap);
}
