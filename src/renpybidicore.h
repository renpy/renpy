#ifndef RENPYBIDICORE_H
#define RENPYBIDICORE_H
#include <Python.h>

PyObject *renpybidi_log2vis(PyObject *s, int *direction);
PyObject *renpybidi_get_embedding_levels(PyObject *s, int *direction, PyObject *levels);
#endif
