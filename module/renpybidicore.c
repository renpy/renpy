#include <Python.h>

#ifdef RENPY_BUILD
#include <fribidi.h>
#else
#include <fribidi-src/lib/fribidi.h>
#endif

#include <stdlib.h>

#ifndef alloca
#include <alloca.h>
#endif


PyObject *renpybidi_log2vis(PyObject *s, int *direction) {
    Py_ssize_t size;
    FriBidiChar *srcuni;
    FriBidiChar *dstuni;
    PyObject *rv;


    Py_UNICODE *p = PyUnicode_AS_UNICODE((PyUnicodeObject *) s);
    size = PyUnicode_GET_SIZE((PyUnicodeObject *) s);

    srcuni = (FriBidiChar *) alloca(size * 4);
    dstuni = (FriBidiChar *) alloca(size * 4);

    for (Py_ssize_t i = 0; i < size; i++) {
        srcuni[i] = p[i];
    }

    fribidi_log2vis(
        srcuni,
        size,
        (FriBidiParType *) direction,
        dstuni,
        NULL,
        NULL,
        NULL);


    p = (Py_UNICODE *) alloca(size * sizeof(Py_UNICODE));

    for (Py_ssize_t i = 0; i < size; i++) {
        p[i] = (Py_UNICODE) dstuni[i];
    }

    rv = PyUnicode_FromUnicode(p, size);

    return rv;
}
