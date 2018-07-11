#include <Python.h>
#include <fribidi-src/lib/fribidi.h>
#include <stdlib.h>

#ifndef alloca
#include <alloca.h>
#endif


PyObject *renpybidi_log2vis(PyUnicodeObject *s, int *direction) {
    Py_ssize_t size;
    FriBidiChar *srcuni;
    FriBidiChar *dstuni;
    PyUnicodeObject *rv;


    Py_UNICODE *p = PyUnicode_AS_UNICODE(s);
    size = PyUnicode_GET_SIZE(s);

    srcuni = (FriBidiChar *) alloca(size * 4);
    dstuni = (FriBidiChar *) alloca(size * 4);

    for (Py_ssize_t i = 0; i < size; i++) {
        srcuni[i] = p[i];
    }

    fribidi_log2vis(
        srcuni,
        size,
        direction,
        dstuni,
        NULL,
        NULL,
        NULL);

    rv = PyUnicode_FromUnicode(NULL, size);
    p = PyUnicode_AS_UNICODE(rv);

    for (Py_ssize_t i = 0; i < size; i++) {
        p[i] = dstuni[i];
    }

    return rv;
}
