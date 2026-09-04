# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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


import cython
from cpython.object cimport PyObject, PyTypeObject, newfunc

# These hash functions use the FNV-1a algorithm to provide a stable hash from strings
# to integers. The stability allows them to be used to hash tlids and pyexprs that may
# be stored in .rpyc and persistent files, unlike Pythons' built-in hash function which
# changes values each time Python is started.

cpdef unsigned int hash32(s):

    cdef unsigned int rv = 0x811c9dc5
    cdef Py_UCS4 u

    if not isinstance(s, str):
        s = str(s)

    cdef str us = <str> s

    for u in us:
        rv ^= <unsigned int> u
        rv *= <unsigned int> 0x01000193

    return rv


cpdef unsigned long long hash64(s):

    cdef unsigned long long rv = 0xcbf29ce484222325
    cdef Py_UCS4 u

    if not isinstance(s, str):
        s = str(s)

    cdef str us = <str> s

    for u in us:
        rv ^= <unsigned int> u
        rv *= <unsigned long long> 0x100000001b3

    return rv


@cython.no_gc
@cython.final
cdef class PyExpr(str):
    cdef readonly str filename
    cdef readonly unsigned int linenumber
    cdef readonly unsigned short column
    cdef readonly unsigned int hashcode

    def __init__(
        self: PyExpr,
        s: str, /,
        *args: object,
        filename: str | None = None,
        linenumber: int | None = None,
        column: cython.ushort = 0,
    ):
        # Public signature, documented in the .pyi:
        #     PyExpr(s, /, *, filename, linenumber, column)
        #
        # Legacy positional signatures, kept only so that pickles written
        # by older Ren'Py versions keep loading. `py` is validated and
        # then discarded.
        #     (s, filename, linenumber)
        #     (s, filename, linenumber, py)
        #     (s, filename, linenumber, py, hashcode)
        #     (s, filename, linenumber, py, hashcode, column)

        if not (args or filename is None or linenumber is None):
            self.filename = filename
            self.linenumber = linenumber
            self.column = column
            self.hashcode = hash32(s)
            return

        if args:
            py = 2
            hashcode = None
            column = 0

            if len(args) == 2:
                filename, linenumber = args
            elif len(args) == 3:
                filename, linenumber, py = args
            elif len(args) == 4:
                filename, linenumber, py, hashcode = args
            elif len(args) == 5:
                filename, linenumber, py, hashcode, column = args
            else:
                raise TypeError(
                    "PyExpr() called with invalid arguments.",
                    (s, ) + args,
                )

            if py not in (2, 3):
                raise ValueError(
                    "PyExpr was given an invalid value for its py argument. "
                    "Did you put the column in the py argument?")

            if hashcode is None:
                hashcode = hash32(s)

            self.filename = filename
            self.linenumber = linenumber
            self.column = column
            self.hashcode = hashcode

        elif filename is None and linenumber is None:
            raise TypeError("PyExpr() missing 2 required keyword-only arguments: 'filename' and 'linenumber'")
        elif filename is None:
            raise TypeError("PyExpr() missing 1 required keyword-only argument: 'filename'")
        else:
            raise TypeError("PyExpr() missing 1 required keyword-only argument: 'linenumber'")


    @staticmethod
    def _from_pickle(
        version: int,
        s: str,
        filename: str,
        linenumber: cython.uint,
        column: cython.ushort,
        hashcode: cython.uint,
        /,
    ) -> PyExpr:
        if version != 1:
            raise ValueError("Invalid PyExpr unpickle version.")

        cdef PyExpr rv = _PyExpr_new(s)
        rv.filename = filename
        rv.linenumber = linenumber
        rv.column = column
        rv.hashcode = hashcode
        return rv

    def __reduce__(self: PyExpr, /) -> tuple:
        return (
            PyExpr._from_pickle,
            (
                1,  # version
                str(self),
                self.filename,
                self.linenumber,
                self.column,
                self.hashcode,
            ),
        )

    @staticmethod
    def from_logical_line(
        text: str,
        start: cython.Py_ssize_t,
        end: cython.Py_ssize_t,
        filename: str,
        linenumber: cython.uint,
        column: cython.ushort,
        /,
    ) -> PyExpr:
        cdef Py_ssize_t i = 0

        for c in text:
            if i >= start:
                break

            i += 1

            if c == "\n":
                linenumber += 1
                column = 0
            else:
                column += 1

        cdef str slice = text[start:end]
        cdef PyExpr rv = _PyExpr_new(slice)
        rv.filename = filename
        rv.linenumber = linenumber
        rv.column = column
        rv.hashcode = hash32(slice)
        return rv


# cdef classes can't have a new method, so we have to modify the type to add our own.
cdef newfunc _str_new = (<PyTypeObject *> str).tp_new

cdef inline PyExpr _PyExpr_new(str s):
    cdef tuple cargs = (s, )
    return _str_new(PyExpr, <PyObject *> cargs, NULL)

cdef object PyExpr_new(type cls, PyObject *args, PyObject *kwargs):
    # str.__new__ only understands (object, encoding, errors), so swallow
    # everything else here and let __init__ deal with it.
    cdef tuple cargs = <tuple> args

    if not cargs:
        raise TypeError("PyExpr() missing required argument 's'.")

    return _PyExpr_new(cargs[0])

(<PyTypeObject *> PyExpr).tp_new = <newfunc> PyExpr_new
