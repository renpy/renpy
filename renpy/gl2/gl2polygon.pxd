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
