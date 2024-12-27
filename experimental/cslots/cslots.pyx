
"""
Cslots - Compressed Slots

The goal of this object is to reduce the amount of space an object with slots takes up,
by only storing slots that exist and have a non-default value.

This is done through indirection. Each Object has a storage allocation consisting of a series of
Value unions, followed by a series of byes that give the value union corresponding to a given slot.
"""

from libc.stdlib cimport calloc, free
from cpython.object cimport PyObject, PyTypeObject, traverseproc, visitproc, Py_TPFLAGS_HAVE_GC
from cpython.ref cimport Py_XINCREF, Py_XDECREF, Py_CLEAR


from sys import intern

cdef COMPRESSED_FLAG = 0x80
cdef INDEX_COUNT_MASK = 0x7f

cdef class CObject:

    # The number of indexes the object has. This also stores COMPRESSED_FLAG.
    cdef unsigned char index_count

    # The number of value unions in the storage allocation.
    cdef unsigned char value_count

    # The column number of this object
    cdef public unsigned short column

    # The line number of this object.
    cdef public unsigned int linenumber

    # This points to value_count PyObject *s, followed by index_count bytes
    cdef PyObject **values

    # Note: Adding any non-slot objects to this object will require tp_traverse and tp_clear to be
    # changed.

    def __init__(self):

        cdef int i
        cdef int slot_count = self.__class__._slot_count

        self.value_count = slot_count
        self.index_count = slot_count

        self.values = <PyObject **>calloc(slot_count, sizeof(PyObject *) + 1)

        cdef unsigned char *indexes = <unsigned char *>(self.values + slot_count)

        for i in range(slot_count):
            indexes[i] = i

    def __dealloc__(self):

        cdef int i
        cdef int slot_count = self.__class__._slot_count

        for i in range(slot_count):
            Py_XDECREF(self.values[i])

        free(self.values)


cdef int cobject_tp_traverse(PyObject *raw, visitproc visit, void *arg) except -1:
    """
    Supports cyclic garbage collection by visiting objects in slots.
    """


    cdef CObject self = <CObject> raw

    for i in range(self.value_count):
        if self.values[i] is not NULL:
            visit(<PyObject *>self.values[i], arg)

    return 0


cdef int cobject_tp_clear(object raw) except -1:
    """
    Supports cyclic garbage collection by clearing slots to break a cycle.
    """

    cdef CObject self = raw

    for i in range(self.value_count):
        if self.values[i] is not NULL:
            Py_CLEAR(self.values[i])

    return 0


# Assign the functions to the tp_traverse and tp_clear slots of CObject.
cdef PyTypeObject *cobject = <PyTypeObject *> CObject
cobject.tp_traverse = cobject_tp_traverse
cobject.tp_clear = cobject_tp_clear
cobject.tp_flags = cobject.tp_flags | Py_TPFLAGS_HAVE_GC


cdef class Slot:

    # The number of this slot inside the indexes contained by CObject.
    cdef public int number

    # The default value of this slot.
    cdef public object default_value

    # Whether this slot should be interned.
    cdef public bint intern

    # The name of this slot.
    cdef public str name

    def __init__(self, default_value, intern=False):

        self.default_value = default_value
        self.intern = intern

    def __get__(self, CObject instance, owner):

        if self.number >= instance.index_count & INDEX_COUNT_MASK:
            return self.default_value

        cdef unsigned char *indexes = <unsigned char *> (instance.values + instance.value_count)
        cdef int index = indexes[self.number]

        if index >= instance.value_count:
            return self.default_value

        cdef PyObject *rv = instance.values[index]

        if rv is NULL:
            return self.default_value

        return <object> rv

    def __set__(self, CObject instance, value):

        if self.intern:
            value = intern(value)

        cdef PyObject *v

        if value == self.default_value:
            v = NULL
        else:
            v = <PyObject *> value

        if instance.index_count & COMPRESSED_FLAG:
            raise AttributeError("Cannot set a value on a compressed object.")

        if self.number >= instance.index_count & INDEX_COUNT_MASK:
            raise AttributeError("Slot number is too large for object.")

        cdef unsigned char *indexes = <unsigned char *> (instance.values + instance.value_count)
        cdef int index = indexes[self.number]

        if index >= instance.value_count:
            raise AttributeError("Index is too large for object.")

        Py_XDECREF(instance.values[index])
        Py_XINCREF(v)
        instance.values[index] = v


class Metaclass(type):

    slot_count: int
    "The number of slots in this class and all of its parents."

    def __new__(cls, name, bases, namespace, **kwds):

        if len(bases) != 1:
            raise TypeError("cslots.Object only supports single inheritance.")

        namespace["__slots__"] = [ ]

        base = bases[0]

        if base is CObject:
            slot_count = 0
        else:
            slot_count = base._slot_count

        for k, v in namespace.items():
            if isinstance(v, Slot):
                v.number = slot_count
                v.name = k
                slot_count += 1

        namespace["_slot_count"] = slot_count

        return type.__new__(cls, name, bases, namespace)


class Object(CObject, metaclass=Metaclass):
    pass


def cobject_size():
    """
    Returns the size of the CObject struct, in bytes.
    """

    return sizeof(CObject)
