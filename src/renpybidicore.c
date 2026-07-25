#include <Python.h>

#include <fribidi/fribidi.h>

#include <stdlib.h>

#ifndef alloca
#include <alloca.h>
#endif

PyObject *renpybidi_log2vis(PyObject *s, int *direction) {
    Py_ssize_t size;
    FriBidiChar *srcuni;
    FriBidiChar *dstuni;

    PyUnicode_READY(s);
    size = PyUnicode_GET_LENGTH(s);

    srcuni = (FriBidiChar *) alloca(size * 4);
    dstuni = (FriBidiChar *) alloca(size * 4);

    PyUnicode_AsUCS4(s, (Py_UCS4 *) srcuni, size, 0);

    fribidi_log2vis(
        srcuni,
        size,
        (FriBidiParType *) direction,
        dstuni,
        NULL,
        NULL,
        NULL);

    return PyUnicode_FromKindAndData(PyUnicode_4BYTE_KIND, dstuni, size);
}

PyObject *renpybidi_get_embedding_levels(PyObject *s, int *direction) {
    Py_ssize_t size;
    FriBidiChar *srcuni;
    FriBidiCharType *types;
    FriBidiLevel *levels;
    PyObject *rv;
    FriBidiLevel ret;

    PyUnicode_READY(s);
    size = PyUnicode_GET_LENGTH(s);

    srcuni = (FriBidiChar *) alloca(size * 4);
    types = (FriBidiCharType *) alloca(size * 4);
    levels = (FriBidiLevel *) alloca(size * 4);

    PyUnicode_AsUCS4(s, (Py_UCS4 *) srcuni, size, 0);

    fribidi_get_bidi_types(
        srcuni,
        size,
        types);

    ret = fribidi_get_par_embedding_levels_ex(
        types,
        NULL,
        size,
        (FriBidiParType *) direction,
        levels);

    if (ret == 0) {
        Py_RETURN_NONE;
    }

    rv = PyTuple_New(size);

    for (int i=0; i<size; i++)
        PyTuple_SetItem(rv, i, Py_BuildValue("i", (int) levels[i]));

    return rv;
}
