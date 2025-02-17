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


import cython
from cpython.object cimport PyObject, PyTypeObject, newfunc
from typing import Any

import renpy

# These hash functions use the FNV-1a algorithm to provide a stable hash from strings
# to integers. The stability allows them to be used to hash tlids and pyexprs that may
# be stored in .rpyc and persistent files, unlike Pythons' built-in hash function which
# changes values each time Python is started.

cpdef unsigned int hash32(s):

    cdef unsigned int rv = 0x811c9dc5
    cdef Py_UCS4 u

    if type(s) is not unicode:
        s = unicode(s)

    cdef unicode us = <unicode> s

    for u in us:
        rv ^= <unsigned int> u
        rv *= <unsigned int> 0x01000193

    return rv


cpdef unsigned long long hash64(s):

    cdef unsigned long long rv = 0xcbf29ce484222325
    cdef Py_UCS4 u

    if type(s) is not unicode:
        s = unicode(s)

    cdef unicode us = <unicode> s

    for u in us:
        rv ^= <unsigned int> u
        rv *= <unsigned long long> 0x100000001b3

    return rv


@cython.no_gc
cdef class PyExpr(str):
    """
    Represents a string containing python expression.
    """

    cdef public str filename
    cdef public unsigned int hashcode
    cdef public unsigned int linenumber
    cdef public unsigned short column
    cdef public unsigned char py

    def __reduce__(self):
        return (PyExpr, (str(self), self.filename, self.linenumber, self.py, self.hashcode, self.column))

    @staticmethod
    def checkpoint() -> Any:
        """
        Checkpoints the pyexpr list. Returns an opaque object that can be used
        to revert the list.
        """

        if renpy.game.script.all_pyexpr is None:
            return None

        return len(renpy.game.script.all_pyexpr)

    @staticmethod
    def revert(opaque: Any):

        if renpy.game.script.all_pyexpr is None:
            return

        if opaque is None:
            return

        renpy.game.script.all_pyexpr[opaque:] = []


# cdef classes can't have a new method, so we have to modify the type to add our own.

cdef PyTypeObject *PyExprType = <PyTypeObject *> PyExpr
cdef newfunc old_pyexpr_newfunc = PyExprType.tp_new


cdef object PyExpr_new(type cls, PyObject *args, PyObject *kwargs):

    if not args:
        raise Exception("PyExpr.__new__ called incorrectly.")

    cdef tuple cargs = <tuple> args

    if len(cargs) == 6:
        s, filename, linenumber, py, hashcode, column = cargs
    elif len(cargs) == 5:
        s, filename, linenumber, py, hashcode = cargs
        column = 0
    elif len(cargs) == 4:
        s, filename, linenumber, py = cargs
        hashcode = None
        column = 0
    elif len(cargs) == 3:
        s, filename, linenumber = cargs
        py = 2
        hashcode = None
        column = 0
    else:
        raise Exception("PyExpr.__new__ called with invalid arguments.", str(<object> args))

    new_args = (s, )

    cdef PyExpr rv = old_pyexpr_newfunc(cls, <PyObject *> new_args, kwargs)

    if py != 3 and py != 2:
        raise ValueError("PyExpr was given an invalid value for its py argument. Did you put the column in the py argument?")

    if <PyObject *> rv:

        rv.filename = filename
        rv.linenumber = linenumber
        rv.column = column
        rv.py = py

        if hashcode is not None:
            rv.hashcode = hashcode
        else:
            rv.hashcode = hash32(s)

        all_pyexpr = renpy.game.script.all_pyexpr

        # Queue the string for precompilation.
        if all_pyexpr is not None:
            all_pyexpr.append(rv)

    return rv

PyExprType.tp_new = <newfunc> PyExpr_new


def make_pyexpr(s, str filename, int linenumber, int column, str text, int pos):
    """
    Used by lexer to make a pyexpr, rapidly adjusting line number and column.

    `s`
        The string that is the expression.

    `filename`
        The name of the file the expression is in.

    `linenumber`
        The line number the logical line starts at.

    `column`
        The column the logical line starts at.

    `text`
        The text of the line.

    `pos`
        The position in the text where the expression starts.
    """

    cdef Py_UCS4 c
    cdef int i = 0

    for c in text:
        if i >= pos:
            break

        i += 1

        if c == 10: # NL
            linenumber += 1
            column = 0
        else:
            column += 1

    return PyExpr(s, filename, linenumber, 3, hash32(s), column)
