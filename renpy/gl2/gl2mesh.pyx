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

from __future__ import print_function

from libc.stdlib cimport malloc, free
from libc.math cimport hypot

from renpy.gl2.gl2polygon cimport Polygon, Point2


cdef class AttributeLayout:

    def __cinit__(self, offset={}, stride=0):
        self.offset = dict(offset)
        self.stride = stride

    def add_attribute(self, name, length):
        self.offset[name] = self.stride
        self.stride += length

    def __reduce__(self):
        return (AttributeLayout, (self.offset, self.stride))


# The layout of a mesh used in a Solid.
SOLID_LAYOUT = AttributeLayout()

# The layout of a mesh used with a texture.
TEXTURE_LAYOUT = AttributeLayout()
TEXTURE_LAYOUT.add_attribute("a_tex_coord", 2) # The texture coordinate.

# The layout of a mesh used with text.
TEXT_LAYOUT = AttributeLayout()
TEXT_LAYOUT.add_attribute("a_tex_coord", 2) # The texture coordinate.
TEXT_LAYOUT.add_attribute("a_text_center", 2) # Position of the vertex center.
TEXT_LAYOUT.add_attribute("a_text_time", 1) # The time this vertex should be shown.
TEXT_LAYOUT.add_attribute("a_text_min_time", 1) # The minimum time any vertex in this glyph should be shown.
TEXT_LAYOUT.add_attribute("a_text_max_time", 1) # The maximum time any vertex in this glyph should be shown.
TEXT_LAYOUT.add_attribute("a_text_index", 1) # The glyph number.
TEXT_LAYOUT.add_attribute("a_text_pos_rect", 4) # The rectangle being drawn.
TEXT_LAYOUT.add_attribute("a_text_ascent", 1) # The ascent of the font.
TEXT_LAYOUT.add_attribute("a_text_descent", 1) # The ascent of the font.

cdef class Mesh:

    def set_geometry_data(self, geometry):
        """
        Sets the geometry data corresponding to this mesh.

        `geometry`
            This should be a sequence of floats, which are interpreted
            as x, y for a Mesh2 or x, y, z for a Mesh3. The length of
            the sequence must be a multiple of the point size of the
            mesh, and must be less than or equal to the number of
            allocated points.

        This sets the `points` attribute of the mesh to the number of
        points in the geometry.
        """

        points = len(geometry) // self.point_size

        if points > self.allocated_points:
            raise Exception("Geometry contains too much data.")

        self.points = points
        cdef int i
        cdef int len_geometry = len(geometry)

        for 0 <= i < len_geometry:
            self.point_data[i] = geometry[i]

    def set_attribute_data(self, attributes):
        """
        Sets the attribute data corresponding to this mesh.

        `attributes`
            This should be a list of floats, with the first
            layout.stride floats corresponding to the first point, the
            next layout.stride floats corresponding to the second point,
            and so on. The length of the sequence must be a multiple of
            the stride of the layout, and must be less than or equal to
            the number of allocated points.
        """

        cdef int i
        cdef int len_attributes = len(attributes)

        if len_attributes > self.allocated_points * self.layout.stride:
            raise Exception("Attributes contains too much data.")

        for 0 <= i < len_attributes:
            self.attribute[i] = attributes[i]

    def set_triangle_data(self, triangles):
        """
        Sets the triangle data corresponding to this mesh.

        `triangles`
            This should be a list of integers, with each triple
            corresponding to a triangle. The length of the sequence
            must be a multiple of 3, and must be less than or equal to
            the number of allocated triangles.

        This sets the `triangles` attribute of the mesh to the number
        of triangles given here.
        """

        cdef int i
        cdef int len_triangles = len(triangles)

        if len_triangles > self.allocated_triangles * 3:
            raise Exception("Triangles contains too much data.")

        self.triangles = len_triangles // 3

        for 0 <= i < len_triangles:
            self.triangle[i] = triangles[i]

    def get_triangles(self):
        """
        Returns the triangles that make up this mesh as triples.
        """

        cdef int i

        rv = [ ]

        for 0 <= i < self.triangles:
            rv.append((
                self.triangle[i * 3 + 0],
                self.triangle[i * 3 + 1],
                self.triangle[i * 3 + 2],
                ))

        return rv
