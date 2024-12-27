
"""
Cslots - Compressed Slots

The goal of this object is to reduce the amount of space an object with slots takes up,
by only storing slots that exist and have a non-default value.

This is done through indirection. Each Object has a storage allocation consisting of a series of
Value unions, followed by a series of byes that give the value union corresponding to a given slot.
"""

from cpython.mem cimport PyMem_Calloc, PyMem_Free
from cpython.object cimport PyObject, PyTypeObject, Py_TPFLAGS_HAVE_GC, PyObject_Free
from cpython.ref cimport Py_XINCREF, Py_XDECREF, Py_CLEAR

from sys import intern


# Used in CObject.index_slots to indicate that the object is compressed.
cdef COMPRESSED_FLAG = 0x80

# Used in CObject.index_slots to mask the index count.
cdef INDEX_COUNT_MASK = 0x7f

# Used in Value.integer to indicate that the value is an integer, shifted right by 1.
cdef INTEGER_FLAG = 0x01

# Used in an index slot to indicate there is no value.
cdef DEFAULT_VALUE = 0xff

cdef union Value:
    PyObject *object
    unsigned long long integer


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
    cdef Value *values

    # Note: Adding any non-slot objects to this object will require tp_traverse and tp_clear to be
    # changed.

    def __cinit__(self):

        cdef int i
        cdef int cslot_count = self.__class__._cslot_count

        self.value_count = cslot_count
        self.index_count = cslot_count

        self.values = <Value *> PyMem_Calloc(1, cslot_count * sizeof(Value) + cslot_count)

        cdef unsigned char *indexes = <unsigned char *>(self.values + cslot_count)

        for i in range(cslot_count):
            indexes[i] = i

    def __dealloc__(self):

        for i in range(self.value_count):
            if not self.values[i].integer & INTEGER_FLAG:
                Py_XDECREF(self.values[i].object)

        PyMem_Free(self.values)

    def _kill(self):

        for i in range(self.value_count):
            if not self.values[i].integer & INTEGER_FLAG:
                Py_XDECREF(self.values[i].object)

            self.values[i].object = NULL


    def _compress(self):

        if self.index_count & COMPRESSED_FLAG:
            return

        cdef unsigned char *old_indexes = <unsigned char *> (self.values + self.value_count)

        # The number of distinct values in the new object.
        cdef unsigned char new_value_count = 0

        # The maximum slot index in the new object.
        cdef unsigned char new_index_count = 0

        cdef unsigned char i
        cdef unsigned char index

        for i in range(self.index_count):
            index = old_indexes[i]

            if self.values[index].object is NULL:
                continue

            new_value_count += 1
            new_index_count = i + 1

        cdef Value *new_values = <Value *> PyMem_Calloc(1, new_value_count * sizeof(Value) + new_index_count)
        cdef unsigned char *new_indexes = <unsigned char *> (new_values + new_value_count)

        self.value_count = 0

        for i in range(new_index_count):
            index = old_indexes[i]

            if self.values[index].object is NULL:
                new_indexes[i] = 0xff
                continue

            new_values[self.value_count] = self.values[index]
            new_indexes[i] = self.value_count
            self.value_count += 1

        self.index_count = new_index_count | COMPRESSED_FLAG

        PyMem_Free(self.values)

        self.values = new_values


    def _decompress(self):

        cdef unsigned char i
        cdef unsigned char index

        if not self.index_count & COMPRESSED_FLAG:
            return

        cdef unsigned char cslot_count = self.__class__._cslot_count

        cdef unsigned char *old_indexes = <unsigned char *> (self.values + self.value_count)

        cdef Value *new_values = <Value *> PyMem_Calloc(1, cslot_count * sizeof(Value) + cslot_count)
        cdef unsigned char *new_indexes = <unsigned char *>(new_values + cslot_count)

        for i in range(cslot_count):
            new_indexes[i] = i

        for i in range(self.index_count & INDEX_COUNT_MASK):
            index = old_indexes[i]

            if index > self.value_count:
                continue

            new_values[i] = self.values[index]

        PyMem_Free(self.values)
        self.values = new_values
        self.index_count = cslot_count
        self.value_count = cslot_count


    def __sizeof__(self):
        return sizeof(CObject) + self.value_count * sizeof(Value) + self.index_count & INDEX_COUNT_MASK


cdef class Slot:

    # The number of this slot inside the indexes contained by CObject.
    cdef public int number

    # The default value of this slot.
    cdef public object default_value

    # Whether this slot should be interned.
    cdef public bint intern

    # The name of this slot.
    cdef public str name

    def __class_getitem__(self, arg):
        return None

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

        if instance.values[index].integer & INTEGER_FLAG:
            return instance.values[index].integer >> 1

        cdef PyObject *rv = instance.values[index].object

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

        if not instance.values[index].integer & INTEGER_FLAG:
            Py_XDECREF(instance.values[index].object)

        Py_XINCREF(v)
        instance.values[index].object = v


class Metaclass(type):

    def __new__(cls, name, bases, namespace, **kwds):

        if len(bases) != 1:
            raise TypeError("cslots.Object only supports single inheritance.")

        namespace["__slots__"] = [ ]

        base = bases[0]

        if base is CObject:
            cslot_count = 0
            cslot_map = { }
            cslot_list = [ ]
        else:
            cslot_count = base._cslot_count
            cslot_map = dict(base._cslot_map)
            cslot_list = list(base._cslot_list)


        for k, v in namespace.items():
            if isinstance(v, Slot):
                v.number = cslot_count
                v.name = k
                cslot_count += 1

        namespace["_cslot_count"] = cslot_count
        namespace["_cslot_map"] = cslot_map
        namespace["_cslot_list"] = cslot_list

        rv = type.__new__(cls, name, bases, namespace)

        cdef PyTypeObject *pto = <PyTypeObject *> rv
        pto.tp_flags =  pto.tp_flags & ~(Py_TPFLAGS_HAVE_GC)
        pto.tp_traverse = NULL
        pto.tp_clear = NULL
        pto.tp_dealloc = <void (*)(PyObject *) noexcept> PyObject_Free

        return rv


class Object(CObject, metaclass=Metaclass):

    pass


def cobject_size():
    """
    Returns the size of the CObject struct, in bytes.
    """

    return sizeof(CObject)
