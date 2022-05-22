from __future__ import print_function

from libc.stdlib cimport calloc, free
from cpython.object cimport PyObject
from cpython.dict cimport PyDict_Next, PyDict_Size
from cpython.ref cimport Py_XINCREF, Py_XDECREF


cdef struct Item:
    PyObject *key
    PyObject *value

cdef inline void swap(Item *a, int i, int j):
    cdef Item tmp

    tmp = a[i]
    a[i] = a[j]
    a[j] = tmp

cdef inline void selection_sort(Item *array, int size):

    cdef int i
    cdef int j
    cdef int min
    cdef PyObject *minkey
    cdef Item tmp

    for 0 <= i < size - 1:

        min = i

        for i < j < size:
            if array[j].key < array[min].key:
                min = j

        if i != min:
            swap(array, i, min)


cdef inline int partition(Item *a, int size):

    cdef int i = 0
    cdef int j = size - 1

    # Use the last key as the pivot.
    cdef PyObject *pivot = a[j].key

    while True:

        while a[i].key < pivot:
            i += 1

        while (i < j) and (a[j].key >= pivot):
            j -= 1

        if i >= j:
            break

        swap(a, i, j)

    # Swap the pivot into place.
    swap(a, size - 1, i)

    return i

cdef void quicksort_items(Item *array, int size):

    if size < 6:
        selection_sort(array, size)
        return

    cdef int split = partition(array, size)
    cdef int left_size = split
    cdef int right_size = size - split - 1


    if left_size >= 2:
        quicksort_items(array, split)

    if right_size >= 2:
        quicksort_items(array + split + 1, size - split - 1)


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

        quicksort_items(self.items, self.size)

    def as_dict(self):

        cdef int i

        rv = { }

        for 0 <= i < self.size:
            rv[<object> self.items[i].key] = <object> self.items[i].value

        return rv


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
