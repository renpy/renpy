from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2polygon cimport Polygon, Point2

cdef class Mesh2(Mesh):

    # The geometry of the points.
    cdef Point2 *point

    cpdef Mesh2 crop(Mesh2 self, Polygon p)
