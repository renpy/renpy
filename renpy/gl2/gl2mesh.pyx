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
TEXTURE_LAYOUT.add_attribute("a_tex_coord", 2)



cdef class Mesh:

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
