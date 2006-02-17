#ifndef RENPY_H
#define RENPY_H

#include <Python.h>

void core_init(void);

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
    
int stretch_core(PyObject *pysrc,
                 PyObject *pydst,
                 int x,
                 int y,
                 int w,
                 int h);



#endif 
