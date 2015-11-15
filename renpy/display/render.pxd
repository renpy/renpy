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

cdef class Matrix2D:
    cdef public double xdx
    cdef public double xdy
    cdef public double ydx
    cdef public double ydy

    cpdef tuple transform(Matrix2D self, double x, double y)

cdef class Render:

    cdef public bint mark, cache_killed

    cdef public float width, height
    cdef public object layer_name

    cdef public list children
    cdef public set parents
    cdef public list depends_on_list

    cdef public int operation
    cdef public double operation_complete
    cdef public bint operation_alpha
    cdef public object operation_parameter

    cdef public Matrix2D forward, reverse
    cdef public double alpha
    cdef public double over
    cdef public object nearest

    cdef public list focuses
    cdef public list pass_focuses
    cdef public object focus_screen

    cdef public object draw_func
    cdef public object render_of

    cdef public bint opaque
    cdef public list visible_children

    cdef public bint clipping

    cdef public object surface, alpha_surface, half_cache

    cdef public bint modal

    cdef public bint text_input

    cpdef int blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)
    cpdef int subpixel_blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)
    cpdef int absolute_blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)


cpdef render(object d, object widtho, object heighto, double st, double at)

