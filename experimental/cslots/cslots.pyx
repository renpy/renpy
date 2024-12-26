
"""
Cslots - Compressed Slots

The goal of this object is to reduce the amount of space an object with slots takes up,
by only storing slots that exist and have a non-default value.

This is done through indirection. Each Object has a storage allocation consisting of a series of
Value unions, followed by a series of byes that give the value union corresponding to a given slot.
"""

from libc.stdlib cimport calloc, free
from cpython.object cimport PyObject
from cpython.ref cimport Py_XINCREF, Py_XDECREF


cdef class CObject:

    # The number of value unions in the storage allocation.
    cdef unsigned char value_count

    # The number of indexes the object has.
    cdef unsigned char index_count

    # The column number of this object
    cdef unsigned short column

    # The line number of this object.
    cdef unsigned int linenumber

    # This points to value_count PyObject *s, followed by index_count bytes
    cdef PyObject **values


cdef class Slot:

    cdef public int index


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

        for v in namespace.values():
            if isinstance(v, Slot):
                v.index = slot_count
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
