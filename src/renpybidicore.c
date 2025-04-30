#include <Python.h>

#include <fribidi/fribidi.h>

#include <stdlib.h>

#ifndef alloca
#include <alloca.h>
#endif

#if PY_VERSION_HEX > 0x030300f0

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

PyObject *renpybidi_get_embedding_levels(PyObject *s, int *direction, PyObject *seg_levels) {
    Py_ssize_t size;
    FriBidiChar *srcuni;
    FriBidiCharType *types;
    FriBidiLevel *levels;
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
        return s;
    }
    
    for (int i=0; i<size; i++)
        PyList_Append(seg_levels, Py_BuildValue("i", (int) levels[i]));
    
    return PyUnicode_FromKindAndData(PyUnicode_4BYTE_KIND, srcuni, size);
}

#else

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

PyObject *renpybidi_get_embedding_levels(PyObject *s, int *direction, PyObject *seg_levels) {
    Py_ssize_t size;
    FriBidiChar *srcuni;
    FriBidiCharType *types;
    FriBidiLevel *levels;
    PyObject *rv;
    FriBidiLevel ret;


    Py_UNICODE *p = PyUnicode_AS_UNICODE((PyUnicodeObject *) s);
    size = PyUnicode_GET_SIZE((PyUnicodeObject *) s);

    srcuni = (FriBidiChar *) alloca(size * 4);
    types = (FriBidiCharType *) alloca(size * 4);
    levels = (FriBidiLevel *) alloca(size * 4);

    for (Py_ssize_t i = 0; i < size; i++) {
        srcuni[i] = p[i];
    }
    
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
        goto done;
    }
    
    for (int i=0; i<size; i++)
        PyList_Append(seg_levels, Py_BuildValue("i", (int) levels[i]));

    p = (Py_UNICODE *) alloca(size * sizeof(Py_UNICODE));

    for (Py_ssize_t i = 0; i < size; i++) {
        p[i] = (Py_UNICODE) srcuni[i];
    }

    rv = PyUnicode_FromUnicode(p, size);

done:
    return rv;
}

#endif
