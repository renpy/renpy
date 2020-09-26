from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2polygon cimport Polygon

# Represents a point in three dimensional space.
cdef struct Point3:
    float x
    float y
    float z

cdef class Mesh3(Mesh):

    # The geometry of the points.
    cdef Point3 *point

    cpdef Mesh3 crop(Mesh3 self, Polygon p)
