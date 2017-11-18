from __future__ import print_function

from libc.stdlib cimport calloc, free, qsort
from cpython.object cimport PyObject
from cpython.dict cimport PyDict_Next, PyDict_Size
from cpython.ref cimport Py_XINCREF, Py_XDECREF


cdef struct Item:
    PyObject *key
    PyObject *value

cdef inline int compare(const void *ap, const void *bp) nogil:
    cdef Item *a = <Item *> ap
    cdef Item *b = <Item *> bp

    if a.key < b.key:
        return -1
    elif a.key > b.key:
        return 1
    else:
        return 0


cdef class DictItems(object):

    cdef int size
    cdef Item *items

    def __dealloc__(self):
        cdef int i

        for 0 <= i < self.size:
            Py_XDECREF(self.items[i].key)
            Py_XDECREF(self.items[i].value)

        free(self.items)

    def __init__(self, dict d):

        cdef Py_ssize_t ppos = 0
        cdef Item *p

        self.size = PyDict_Size(d)
        self.items = <Item *> calloc(self.size, sizeof(Item))

        p = self.items

        while PyDict_Next(d, &ppos, &p.key, &p.value):
            Py_XINCREF(p.key)
            Py_XINCREF(p.value)
            p += 1

        qsort(self.items, self.size, sizeof(Item), compare)

        print(<object> self.items[0].key)


DictItems({
    "a" : "b",
    "c" : 42,
    "d" : "india",
})




