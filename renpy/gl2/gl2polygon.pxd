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

from renpy.display.matrix cimport Matrix

# Represents a 2D point inside a polygon.
cdef struct Point2:
    float x
    float y

cdef class Polygon:
    """
    Represents a 2-dimensional polygon.
    """

    # The number of points in the polygon.
    cdef int points

    # The points.
    cdef Point2 *point

    cpdef Polygon intersect(Polygon self, Polygon p)
    cpdef Polygon copy(Polygon self)
    cpdef void multiply_matrix_inplace(Polygon self, Matrix m)
    cpdef Polygon multiply_matrix(Polygon self, Matrix m)
    cpdef void ensure_winding(Polygon self)
