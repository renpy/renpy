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
