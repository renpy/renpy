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
from renpy.gl2.gl2mesh cimport Mesh

cdef class GL2Model:

    # The width and height.
    cdef public int width
    cdef public int height

    # The mesh giving the geometry of this model.
    cdef public Mesh mesh

    # A matrix transforming screen coordinates toward mesh coordinates.
    cdef public Matrix forward

    # A matrix transforming mesh coordinates towards screen coordinates.
    cdef public Matrix reverse

    # A tuple giving the shaders used with this model.
    cdef public tuple shaders

    # Either a dictionary giving uniforms associated with this model,
    # or None.
    cdef public dict uniforms

    # Either a dictionary giving properties associated with this model,
    # or None.
    cdef public dict properties

    # The cached_texture that comes from this model. (This is
    # a Texture.)
    cdef public object cached_texture

    cpdef GL2Model copy(GL2Model self)
    cpdef subsurface(GL2Model self, t)
    cpdef scale(GL2Model self, float factor)
