# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

from copyreg import __newobj__

import typing

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

cdef class CMetaclass(type):

    cdef public unsigned char _cslot_count
    "The number of slots in the class."

    cdef public dict _cslot_setters
    "A dictionary mapping slot names to their setters."

    cdef public list _cslot_fields
    "A list of slot names."

    cdef public bint _cslot_linenumbers
    "If true, linenumber information should be included when objects of this class are pickled."

    cdef public bint _cslot_has_getstate
    "If true, the class defines its own __getstate__ method."


cdef class CObject:

    # The number of indexes the object has. This also stores COMPRESSED_FLAG.
    cdef unsigned char index_count

    # The number of value unions in the storage allocation.
    cdef unsigned char value_count

    # The column number of this object
    cdef public unsigned short col_offset

    # The line number of this object.
    cdef public unsigned int linenumber

    # This points to value_count PyObject *s, followed by index_count bytes
    cdef Value *values

    def __cinit__(self):

        cdef CMetaclass cbase = <CMetaclass> type(self)

        cdef unsigned char i
        cdef unsigned char cslot_count = cbase._cslot_count

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

        cdef CMetaclass cbase = <CMetaclass> type(self)

        cdef unsigned char cslot_count = cbase._cslot_count

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

        cdef CMetaclass ctype
        cdef dict slots
        cdef list cslot_fields
        cdef unsigned char *indexes
        cdef unsigned char i
        cdef Value v
        cdef unsigned char index

        ctype = <CMetaclass> type(self)

        if ctype._cslot_has_getstate:
            state = self.__getstate__()
        else:

            if ctype._cslot_linenumbers:
                slots = { "linenumber" : self.linenumber, "col_offset" : self.col_offset }
            else:
                slots = { }

            cslot_fields = ctype._cslot_fields
            indexes = <unsigned char *> (self.values + self.value_count)

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

            state = (None, slots)

        return ( __newobj__, (type(self),), state )

    def __setstate__(self, state):

        cdef CMetaclass ctype = <CMetaclass> type(self)
        cdef dict cslot_setters = ctype._cslot_setters
        cdef dict d

        name = None

        if type(state) is tuple:
            for d in (<tuple> state):
                if d is None:
                    continue

                for k, v in d.items():
                    f = cslot_setters.get(k, None)
                    if f is not None:
                        f(self, v)
                    elif k == "name":
                        name = v

        elif type(state) is dict:
            d = state

            for k, v in d.items():
                f = cslot_setters.get(k, None)
                if f is not None:
                    f(self, v)
                elif k == "name":
                    name = v

        else:
            raise TypeError("Invalid state type.")

        if name:
            try:
                setattr(self, "name", name)
            except AttributeError:
                pass


cdef class Slot:

    # The number of this slot inside the indexes contained by CObject.
    cdef public int number

    # The default value of this slot.
    cdef public object default_value

    # The name of this slot.
    cdef public str name

    def __class_getitem__(self, arg):
        return None

    def __init__(self, default_value=None):

        self.default_value = default_value

    def __get__(self, CObject instance, owner):

        if instance is None:
            return self

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

        cdef PyObject *v

        if instance is None:
            raise AttributeError("Slot is not bound to an instance.")

        if (type(value) is type(self.default_value)) and (value == self.default_value):
            v = NULL
        else:
            v = <PyObject *> value

        if instance.index_count & COMPRESSED_FLAG:
            instance._decompress()

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
            instance._decompress()

        if self.number >= instance.index_count & INDEX_COUNT_MASK:
            raise AttributeError("Slot number is too large for object.")

        cdef unsigned char *indexes = <unsigned char *> (instance.values + instance.value_count)
        cdef int index = indexes[self.number]

        if index >= instance.value_count:
            raise AttributeError("Index is too large for object.")

        if not instance.values[index].integer & INTEGER_FLAG:
            Py_XDECREF(instance.values[index].object)

        instance.values[index] = v


class Metaclass(CMetaclass):
    """
    A metaclass that sets up the slots, and makes sure classes that inherit from it do not participate
    in cyclic GC.
    """

    def __new__(cls, name, bases, namespace, **kwds):


        if len(bases) != 1:
            raise TypeError("cslots.Object only supports single inheritance.")

        # Add empty Python slots, so the object doesn't get a dict.
        namespace["__slots__"] = [ ]

        # Number slots, and create the _cslot_setters and _cslot_fields attributes.
        base = bases[0]

        cdef CMetaclass cbase

        if base is CObject:
            cslot_count = 0
            cslot_setters = { "linenumber" : CObject.linenumber.__set__, "col_offset" : CObject.col_offset.__set__ }
            cslot_fields = [ ]
            cslot_linenumbers = False
            cslot_has_getstate = False
        else:
            cbase = <CMetaclass> base

            cslot_count = cbase._cslot_count
            cslot_setters = dict(cbase._cslot_setters)
            cslot_fields = list(cbase._cslot_fields)
            cslot_linenumbers = cbase._cslot_linenumbers
            cslot_has_getstate = cbase._cslot_has_getstate

        rv = CMetaclass.__new__(cls, name, bases, namespace, **kwds)

        annotations = rv.__annotations__

        for k, v in annotations.items():
            if typing.get_origin(v) is typing.ClassVar:
                continue

            if v is int:
                default_value = namespace.get(k, 0)
                namespace[k] = IntegerSlot(default_value)
            else:
                default_value = namespace.get(k, None)
                namespace[k] = Slot(default_value)

            setattr(rv, k, namespace[k])

        for k, v in namespace.items():
            if isinstance(v, Slot):
                v.number = cslot_count
                v.name = k
                cslot_fields.append(k)
                cslot_setters[k] = v.__set__
                cslot_count += 1


        cdef CMetaclass crv = <CMetaclass> rv

        crv._cslot_count = cslot_count
        crv._cslot_setters = cslot_setters
        crv._cslot_fields = cslot_fields
        crv._cslot_linenumbers = namespace.get("_cslot_linenumbers", cslot_linenumbers)
        crv._cslot_has_getstate = cslot_has_getstate or ("__getstate__" in namespace)

        # Modify the type object to remove support for the cyclic GC. This saves 16 bytes per object, but
        # means reference cycles.
        cdef PyTypeObject *pto = <PyTypeObject *> rv
        pto.tp_flags =  pto.tp_flags & ~(Py_TPFLAGS_HAVE_GC)
        pto.tp_traverse = NULL
        pto.tp_clear = NULL
        pto.tp_dealloc = <void (*)(PyObject *) noexcept> PyObject_Free

        return rv


class Object(CObject, metaclass=Metaclass):

    pass
