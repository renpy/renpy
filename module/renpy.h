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

void xblur32_core(PyObject *pysrc,
                  PyObject *pydst,
                  int radius);

#endif 
