# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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
cimport renpy.display.render as render
from renpy.gl.gldraw cimport Environ

cdef class TextureCore:
    cdef public int width
    cdef public int height
    cdef public int generation
    cdef public unsigned int number
    cdef unsigned int format
    cdef double xmul
    cdef double xadd
    cdef double ymul
    cdef double yadd
    cdef object premult
    cdef tuple premult_size
    cdef int premult_left
    cdef int premult_right
    cdef int premult_top
    cdef int premult_bottom
    cdef bint nearest
    cdef public list free_list

    cdef void make_ready(TextureCore)
    cdef void make_nearest(TextureCore)
    cdef void make_linear(TextureCore)
    cpdef int allocate(TextureCore)

    cdef public object debug

cdef class TextureGrid:


    cdef object __weakref__

    cdef public int width
    cdef public int height
    cdef list rows
    cdef list columns
    cdef list tiles # list of lists.
    cdef public TextureGrid half_cache

    cpdef void make_ready(self, bint nearest)

    cdef public object debug
    cdef public bint ready


cpdef blit(
    TextureGrid tg,
    double sx,
    double sy,
    Matrix transform,
    double alpha,
    double over,
    Environ environ,
    bint nearest)

cpdef blend(
    TextureGrid tg0,
    TextureGrid tg1,
    double sx,
    double sy,
    Matrix transform,
    double alpha,
    double over,
    double fraction,
    Environ environ,
    bint nearest)

cpdef imageblend(
    TextureGrid tg0,
    TextureGrid tg1,
    TextureGrid tg2,
    double sx,
    double sy,
    Matrix transform,
    double alpha,
    double over,
    double fraction,
    int ramp,
    Environ environ,
    bint nearest)
