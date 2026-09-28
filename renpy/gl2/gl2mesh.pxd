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

from renpy.gl2.gl2polygon cimport Polygon
from renpy.gl2.gl2statecache cimport GLStateCache
from renpy.uguu.gl cimport GLuint, GLsizeiptr

cdef struct MeshBuffer:
    GLuint name
    unsigned long long generation
    unsigned int version
    GLsizeiptr size

cdef class AttributeLayout:
    """
    This represents the layout of attributes inside a mesh.
    """

    # A map from a string giving the name of the attribute to the
    # offset of the attribute.
    cdef public dict offset

    # The number of floats that make up the attributes for a single
    # point.
    cdef public int stride

cdef class Mesh:
    """
    This represents the polygon and vertex data that is stored within
    a GL2Model.
    """

    # The number of points that space has been allocated for.
    cdef public int allocated_points

    # The number of points that are in use.
    cdef public int points

    # The data corresponding to each point.
    cdef float *point_data

    # The number of floats corresponding to each point.
    cdef public int point_size

    # An AttributeLayout object controlling how attributes are stored.
    cdef public AttributeLayout layout

    # The non-geometry attribute data. This is allocated_points * attribute_per_point in size.
    cdef float *attribute

    # The number of triangles that spaces has been allocated for.,
    cdef public int allocated_triangles

    # The number of triangles that are in use.
    cdef public int triangles

    # The triangle data, where each triangle consists of the index of three
    # points. This is 3 * allocated_triangles in size.
    cdef unsigned int *triangle

    # Versions to be tracked and incremented before enabling crop and buffer reuse.
    # Zero indicates the field is not tracked.
    cdef public unsigned int point_version
    cdef public unsigned int attribute_version
    cdef public unsigned int triangle_version

    # The key used to cache crops.
    cdef tuple _crop_key
    cdef Mesh _cropped_mesh

    cdef Mesh get_cropped_mesh(self, Polygon p)

    cdef MeshBuffer buffers[3]
    cdef bint draw_seen
    cdef unsigned long long draw_frame

    cdef void upload_buffers(self, GLStateCache cache, GLuint* vbo, GLuint* abo, GLuint* ibo) noexcept nogil
