# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

cdef union UCS4:
    Py_UCS4 u
    unsigned char c[4]


def hash_fnv1a(s):
    """
    FNV-1a hash function.

    This computes a stable 32-bit hash of the unicode string (s).
    """

    cdef unsigned int rv = 0x811c9dc5
    cdef UCS4 codepoint

    if type(s) is not unicode:
        s = unicode(s)

    cdef unicode us = <unicode> s

    for codepoint.u in us:
        rv ^= codepoint.c[0]
        rv *= 0x01000193

        rv ^= codepoint.c[1]
        rv *= 0x01000193

        rv ^= codepoint.c[2]
        rv *= 0x01000193

        rv ^= codepoint.c[3]
        rv *= 0x01000193

    return rv

@cython.no_gc
cdef class PyExpr(str):
    """
    Represents a string containing python expression.
    """

    cdef public str filename
    cdef public unsigned int hashcode
    cdef public int linenumber
    cdef public unsigned char py

    filename: str
    linenumber: int
    py: int
    hashcode: int

    def __reduce__(self):
        return (PyExpr, (str(self), self.filename, self.linenumber, self.py, self.hashcode))

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

    if len(cargs) == 5:
        s, filename, linenumber, py, hashcode = cargs
    elif len(cargs) == 4:
        s, filename, linenumber, py = cargs
        hashcode = None
    elif len(cargs) == 3:
        s, filename, linenumber = cargs
        py = 2
        hashcode = None
    else:
        raise Exception("PyExpr.__new__ called with invalid arguments.", str(<object> args))

    new_args = (s, )

    cdef PyExpr rv = old_pyexpr_newfunc(cls, <PyObject *> new_args, kwargs)

    if <PyObject *> rv:

        rv.filename = filename
        rv.linenumber = linenumber
        rv.py = py

        if hashcode is not None:
            rv.hashcode = hashcode
        else:
            rv.hashcode = hash_fnv1a(s)

        all_pyexpr = renpy.game.script.all_pyexpr

        # Queue the string for precompilation.
        if all_pyexpr is not None:
            all_pyexpr.append(rv)

    return rv

PyExprType.tp_new = <newfunc> PyExpr_new
