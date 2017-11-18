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

    def __init__(self, d):

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




def find_changes(DictItems old, DictItems new, object deleted):

    cdef oi = 0
    cdef ni = 0

    cdef Item *op = old.items
    cdef Item *np = new.items

    cdef Item *oend = op + old.size
    cdef Item *nend = np + new.size

    rv = None

    while (op != oend) or (np != nend):

        # print( (op == oend), (np == nend) )

        if (np == nend) or ((op != oend) and (op.key < np.key)):
            # print("Only in old:", <object> op.key)

            if rv is None:
                rv = { }

            rv[<object> op.key] = <object> op.value

            op += 1

        elif (op == oend) or ((np != nend) and (np.key < op.key)):
            # print("Only in new:", <object> np.key)

            if rv is None:
                rv = { }

            rv[<object> np.key] = deleted

            np += 1

        elif (np.value == op.value):
            # print("Same in both:", <object> op.key)
            np += 1
            op += 1

        else:
            # print("Different in both:", <object> op.key)

            if rv is None:
                rv = { }

            rv[<object> op.key] = <object> op.value

            np += 1
            op += 1

    return rv




foo = DictItems({
    "a" : "b",
    "c" : 42,
    "d" : "india",
})


bar = DictItems({
    "c" : 37,
    "d" : "india",
    "e" : True
    })


print(find_changes(foo, bar, "deleted"))

del foo
del bar

