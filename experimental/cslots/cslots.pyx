
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
from copyreg import __newobj__


# Used in CObject.index_slots to indicate that the object is compressed.
cdef unsigned char COMPRESSED_FLAG = 0x80

# Used in CObject.index_slots to mask the index count.
cdef unsigned char INDEX_COUNT_MASK = 0x7f

# Used in Value.integer to indicate that the value is an integer, shifted right by 1.
cdef unsigned char INTEGER_FLAG = 0x01

# Used in an index slot to indicate there is no value.
cdef unsigned char DEFAULT_VALUE = 0xff

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

    def __cinit__(self):

        cdef unsigned char i
        cdef unsigned char cslot_count = type(self)._cslot_count

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

        cdef unsigned char cslot_count = type(self)._cslot_count

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

    def __reduce_ex__(self, protocol):

        cdef dict slots = { "linenumber" : self.linenumber, "column" : self.column }
        cdef list cslot_fields = type(self)._cslot_fields
        cdef unsigned char *indexes = <unsigned char *> (self.values + self.value_count)
        cdef unsigned char i
        cdef Value v
        cdef unsigned char index

        for i in range(self.index_count & INDEX_COUNT_MASK):
            if indexes[i] == DEFAULT_VALUE:
                continue

            index = indexes[i]

            if index > self.value_count:
                continue

            v = self.values[index]

            if v.integer & INTEGER_FLAG:
                slots[cslot_fields[i]] = v.integer >> 1
            elif v.object is not NULL:
                slots[cslot_fields[i]] = <object> v.object

        return ( __newobj__, (type(self),), (None, slots) )

    def __setstate__(self, state):

        cdef dict cslot_setters = type(self)._cslot_setters
        cdef dict d

        if type(state) is tuple:
            for d in (<tuple> state):
                if d is None:
                    continue

                for k, v in d.items():
                    f = cslot_setters.get(k, None)
                    if f is not None:
                        f(self, v)

        elif type(state) is dict:
            d = state

            for k, v in d.items():
                f = cslot_setters.get(k, None)
                if f is not None:
                    f(self, v)

        else:
            raise TypeError("Invalid state type.")



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


cdef class IntegerSlot(Slot):

    cdef long long default_int_value

    def __init__(self, default_value=0):
        super(IntegerSlot, self).__init__(default_value)
        self.default_int_value = default_value

    def __set__(self, CObject instance, unsigned int value):

        cdef Value v

        if value == self.default_int_value:
            v.object = NULL
        else:
            v.integer = (value << 1) | INTEGER_FLAG

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

        instance.values[index] = v



class Metaclass(type):
    """
    This handles setting up the slots, and adds three names to the classes:

    * `_cslot_count` - The number of slots in the class.
    * `_cslot_setters` - A dictionary mapping slot names to their setters.
    * `_cslot_fields` - A list of slot names.
    """

    def __new__(cls, name, bases, namespace, **kwds):

        if len(bases) != 1:
            raise TypeError("cslots.Object only supports single inheritance.")

        namespace["__slots__"] = [ ]

        base = bases[0]

        if base is CObject:
            cslot_count = 0
            cslot_setters = { "linenumber" : CObject.linenumber.__set__, "column" : CObject.column.__set__ }
            cslot_fields = [ ]
        else:
            cslot_count = base._cslot_count
            cslot_setters = dict(base._cslot_setters)
            cslot_fields = list(base._cslot_fields)


        for k, v in namespace.items():
            if isinstance(v, Slot):
                v.number = cslot_count
                v.name = k
                cslot_fields.append(k)
                cslot_setters[k] = v.__set__
                cslot_count += 1

        namespace["_cslot_count"] = cslot_count
        namespace["_cslot_setters"] = cslot_setters
        namespace["_cslot_fields"] = cslot_fields

        rv = type.__new__(cls, name, bases, namespace)

        cdef PyTypeObject *pto = <PyTypeObject *> rv
        pto.tp_flags =  pto.tp_flags & ~(Py_TPFLAGS_HAVE_GC)
        pto.tp_traverse = NULL
        pto.tp_clear = NULL
        pto.tp_dealloc = <void (*)(PyObject *) noexcept> PyObject_Free

        return rv


class Object(CObject, metaclass=Metaclass):

    pass
