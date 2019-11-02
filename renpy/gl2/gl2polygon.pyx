from libc.stdlib cimport calloc, free

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

    def __init__(Polygon self, int allocate_points):
        """
        `allocate_points`
            The number of points to allocate room for.
        """

        self.points = 0
        self.point = <Point2 *> calloc(allocate_points, sizeof(Point2))

    def __dealloc__(Polygon self):
        free(self.point)

    def __repr__(Polygon self):
        cdef int i

        rv = "<Polygon"

        for 0 <= i < self.points:
            rv += " ({:.3f}, {:.3f})".format(self.point[i].x, self.point[i].y)

        rv += ">"

        return rv

    @staticmethod
    def from_list(list l):
        cdef int i

        cdef int points = len(l) / 2

        cdef Polygon rv = Polygon(points)
        rv.points = points

        for 0 <= i < points:
            rv.point[i].x = l[i * 2 + 0]
            rv.point[i].y = l[i * 2 + 1]

        return rv
