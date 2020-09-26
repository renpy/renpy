#ifndef RENPY_H
#define RENPY_H

#include <Python.h>
#include <SDL.h>

void core_init(void);
void subpixel_init(void);

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

void blur32_core(PyObject *pysrc,
                 PyObject *pywrk,
                 PyObject *pydst,
                 float xrad,
                 float yrad);

void blur24_core(PyObject *pysrc,
                 PyObject *pywrk,
                 PyObject *pydst,
                 float xrad,
                 float yrad);

void linblur32_core(PyObject *pysrc,
                    PyObject *pydst,
                    int radius,
                    int vertical);

void linblur24_core(PyObject *pysrc,
                    PyObject *pydst,
                    int radius,
                    int vertical);

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
                  float, float, float, float,
                  int);

void scale24_core(PyObject *pysrc,
                  PyObject *pydst,
                  float, float, float, float,
                  float, float, float, float);

void transform32_core(PyObject *pysrc,
                      PyObject *pydst,
                      float, float,
                      float, float,
                      float, float,
                      int, float, int);

void blend32_core(PyObject *pysrca,
                  PyObject *pysrcb,
                  PyObject *pydst,
                  int alpha);

void imageblend32_core(PyObject *pysrca, PyObject *pysrcb,
                       PyObject *pydst, PyObject *pyimg,
                       int alpha, char *amap);


void colormatrix32_core(PyObject *pysrc, PyObject *pydst,
                        float c00, float c01, float c02, float c03, float c04,
                        float c10, float c11, float c12, float c13, float c14,
                        float c20, float c21, float c22, float c23, float c24,
                        float c30, float c31, float c32, float c33, float c34);

void staticgray_core(
    PyObject *pysrc, PyObject *pydst,
    int rmul, int gmul, int bmul, int amul, int shift,
    char *vmap);

int subpixel32(
    PyObject *pysrc, PyObject *pydst,
    float xoffset, float yoffset, int ashift);


#endif
