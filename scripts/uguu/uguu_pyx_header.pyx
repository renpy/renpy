from libc.stddef cimport ptrdiff_t
from libc.stdint cimport int64_t, uint64_t
from libc.stdio cimport printf
from libc.stdlib cimport calloc, free

from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_CONTIG, PyBUF_CONTIG_RO

cimport renpy.uguu.gl
import renpy.uguu.gl


cdef object proxy_return_string(const GLubyte *s):
    """
    This is used for string return values. It returns the return value as
    a python string if it's not NULL, or None if it's null.
    """

    if s == NULL:
        return None

    cdef const char *ss = <const char *> s
    return ss


cdef class ptr:
    """
    This is a class that wraps a generic contiguous Python buffer, and
    allows the retrieval of a pointer to that buffer.
    """

    cdef void *ptr
    cdef Py_buffer view

    def __init__(self, o, ro=True):
        if o is None:
            self.ptr = NULL
            return

        PyObject_GetBuffer(o, &self.view, PyBUF_CONTIG_RO if ro else PyBUF_CONTIG)
        self.ptr = self.view.buf

    def __dealloc__(self):
        if self.ptr:
            PyBuffer_Release(&self.view)
            self.ptr = NULL

cdef ptr get_ptr(o):
    """
    If o is a ptr, return it. Otherwise, convert the buffer into a ptr, and
    return that.
    """

    if isinstance(o, ptr):
        return o
    else:
        return ptr(o)

cdef class Buffer:
    """
    The base class for all buffers.
    """

    cdef Py_ssize_t length
    cdef Py_ssize_t itemsize
    cdef const char *format
    cdef void *data
    cdef int readonly

    cdef setup_buffer(self, Py_ssize_t length, Py_ssize_t itemsize, const char *format, int readonly):
        """
        This is called by a specific buffer's init method to set up various fields, and especially
        allocate the data field.

        `length`
            The number of items in this buffer.
        `itemsize`
            The size of a single item.
        `format`
            The struct-style format code.
        `readonly`
            1 if readonly, 0 if read-write.
        """

        self.length = length
        self.itemsize = itemsize
        self.format = format
        self.readonly = readonly
        self.data = calloc(self.length, self.itemsize)

    def __getbuffer__(self, Py_buffer *buffer, int flags):

        buffer.buf = self.data
        buffer.format = <char *> self.format
        buffer.internal = NULL
        buffer.itemsize = self.itemsize
        buffer.len = self.length * self.itemsize
        buffer.ndim = 1
        buffer.obj = self
        buffer.readonly = self.readonly
        buffer.shape = &self.length
        buffer.strides = &self.itemsize
        buffer.suboffsets = NULL

    def __releasebuffer__(self, Py_buffer *buffer):
        pass

    def __dealloc__(self):
        if self.data:
            free(self.data)
            self.data = NULL

cdef class BytesBuffer(Buffer):

    def __init__(self, length):

        self.setup_buffer(length, 1, "B", 0)

    def get(self):
        return bytes(<char *> self.data)

cdef class BytesListBuffer(Buffer):
    cdef object value

    def __init__(self, value):
        self.value = [ ptr(v) for v in value ]
        self.setup_buffer(len(value), sizeof(const char *), "P", 1)

        cdef int i

        for 0 <= i < self.length:
            (<const char **> self.data)[i] = <const char *> (<ptr> self.value[i]).ptr

cdef class IntBuffer(Buffer):

    def __init__(self, value):

        self.setup_buffer(len(value), sizeof(int), "i", 0)

        cdef int i

        for 0 <= i < self.length:
            (<int*> self.data)[i] = <int> value[i]

    def __getitem__(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("index out of range")

        return (<int*> self.data)[index]

cdef class FloatBuffer(Buffer):

    def __init__(self, value):

        self.setup_buffer(len(value), sizeof(float), "f", 0)

        cdef int i

        for 0 <= i < self.length:
            (<float *> self.data)[i] = <float> value[i]

    def __getitem__(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("index out of range")

        return (<float *> self.data)[index]
