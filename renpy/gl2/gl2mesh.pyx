from __future__ import print_function

from libc.stdlib cimport malloc, free
from libc.math cimport hypot

# Information used when cropping.
cdef class AttributeLayout:

    def __cinit__(self):
        self.offset = { }
        self.stride = 0

    def add_attribute(self, name, length):
        self.offset[name] = self.stride
        self.stride += length

SOLID_LAYOUT = AttributeLayout()
TEXTURE_LAYOUT = AttributeLayout()
TEXTURE_LAYOUT.add_attribute("aTexCoord", 2)

cdef class Data:

    def __init__(Data self, AttributeLayout layout, int points, int triangles):
        """
        `layout`
            An object that contains information about how non-geometry attributes
            are laid out.

        `points`
            The number of points for which space should be allocated.

        `triangles`
            The number of triangles for which space should be allocated.
        """

        self.allocated_points = points
        self.points = 0
        self.point = <Point3 *> malloc(points * sizeof(Point3))

        self.layout = layout
        self.attribute = <float *> malloc(points * layout.stride * sizeof(float))

        self.allocated_triangles = triangles
        self.triangles = 0
        self.triangle = <int *> malloc(triangles * 3 * sizeof(int))

    def __dealloc__(Data self):
        free(self.point)
        free(self.attribute)
        free(self.triangle)




cdef class Mesh:

    def __repr__(Mesh self):

        cdef Data data = self.data
        cdef int i
        cdef int j

        rv = "<Mesh {!r}".format(data.layout.offset)

        for 0 <= i < data.points:
            rv += "\n    {}: {: >8.3f} {:> 8.3f} {:> 8.3f} | ".format(chr(i + 65), data.point[i].x, data.point[i].y, data.point[i].z)
            for 0 <= j < data.layout.stride:
                rv += "{:> 8.3f} ".format(data.attribute[i * data.layout.stride + j])

        rv += "\n    "

        for 0 <= i < data.triangles:
            rv += "{}-{}-{} ".format(
                chr(data.triangle[i * 3 + 0] + 65),
                chr(data.triangle[i * 3 + 1] + 65),
                chr(data.triangle[i * 3 + 2] + 65),
                )

        rv += ">"

        return rv


    @staticmethod
    def rectangle(
            double pl, double pb, double pr, double pt
            ):

        cdef Data data = Data(SOLID_LAYOUT, 4, 2)

        data.points = 4

        data.point[0].x = pl
        data.point[0].y = pb
        data.point[0].z = 0

        data.point[1].x = pr
        data.point[1].y = pb
        data.point[1].z = 0

        data.point[2].x = pr
        data.point[2].y = pt
        data.point[2].z = 0

        data.point[3].x = pl
        data.point[3].y = pt
        data.point[3].z = 0

        data.triangles = 2

        data.triangle[0] = 0
        data.triangle[1] = 1
        data.triangle[2] = 2

        data.triangle[3] = 0
        data.triangle[4] = 2
        data.triangle[5] = 3

        cdef Mesh rv = Mesh()
        rv.data = data

        return rv

    def texture_rectangle_mesh(
        double pl, double pb, double pr, double pt,
        double tl, double tb, double tr, double tt
        ):

        cdef Data data = Data(TEXTURE_LAYOUT, 4, 2)

        data.points = 4

        data.point[0].x = pl
        data.point[0].y = pb
        data.point[0].z = 0

        data.point[1].x = pr
        data.point[1].y = pb
        data.point[1].z = 0

        data.point[2].x = pr
        data.point[2].y = pt
        data.point[2].z = 0

        data.point[3].x = pl
        data.point[3].y = pt
        data.point[3].z = 0

        data.attribute[0] = tl
        data.attribute[1] = tb

        data.attribute[2] = tr
        data.attribute[3] = tb

        data.attribute[4] = tr
        data.attribute[5] = tt

        data.attribute[6] = tl
        data.attribute[7] = tt

        data.triangles = 2

        data.triangle[0] = 0
        data.triangle[1] = 1
        data.triangle[2] = 2

        data.triangle[3] = 0
        data.triangle[4] = 2
        data.triangle[5] = 3

        cdef Mesh rv = Mesh()
        rv.data = data

        return rv


