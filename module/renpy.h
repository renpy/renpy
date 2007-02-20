#ifndef RENPY_H
#define RENPY_H

#include <Python.h>
#include <SDL/SDL.h>

SDL_RWops* RWopsFromPython(PyObject* obj);

void core_init(void);

void save_png_core(PyObject *pysurf, SDL_RWops *file, int compress);

void pixellate32_core(PyObject *pysrc,
                      PyObject *pydst,
                      int avgwidth,
                      int avgheight,
                      int outwidth,
                      int outheight);

void pixellate24_core(PyObject *pysrc,
                      PyObject *pydst,
                      int avgwidth,
                      int avgheight,
                      int outwidth,
                      int outheight);

void map32_core(PyObject *pysrc,
                PyObject *pydst,
                char *rmap,
                char *gmap,
                char *bmap,
                char *amap);

void map24_core(PyObject *pysrc,
                PyObject *pydst,
                char *rmap,
                char *gmap,
                char *bmap);

void linmap32_core(PyObject *pysrc,
                PyObject *pydst,
                int rmap,
                int gmap,
                int bmap,
                int amap);

void linmap24_core(PyObject *pysrc,
                PyObject *pydst,
                int rmap,
                int gmap,
                int bmap);

#if 0

void xblur32_core(PyObject *pysrc,
                  PyObject *pydst,
                  int radius);

#endif

void alphamunge_core(PyObject *pysrc,
                     PyObject *pydst,
                     int src_bypp, // bytes per pixel.
                     int src_aoff, // alpha offset.
                     int dst_aoff, // alpha offset.
                     char *amap);
    
/* int stretch_core(PyObject *pysrc, */
/*                  PyObject *pydst, */
/*                  int x, */
/*                  int y, */
/*                  int w, */
/*                  int h); */

void scale32_core(PyObject *pysrc,
                  PyObject *pydst,
                  float, float, float, float,
                  float, float, float, float);

void scale24_core(PyObject *pysrc,
                  PyObject *pydst,
                  float, float, float, float,
                  float, float, float, float);

void transform32_core(PyObject *pysrc,
                      PyObject *pydst,
                      float, float,
                      float, float,
                      float, float);

void blend32_core(PyObject *pysrca,
                  PyObject *pysrcb,
                  PyObject *pydst,
                  int alpha);

void imageblend32_core(PyObject *pysrca, PyObject *pysrcb,
                       PyObject *pydst, PyObject *pyimg,
                       int alpha, char *amap);

#endif 
