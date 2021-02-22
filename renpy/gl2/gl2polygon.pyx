from libc.stdlib cimport calloc, free
from libc.string cimport memcpy


cdef object point2str(Point2 p):
    return "({:.3f}, {:.3f})".format(p.x, p.y)

cdef class Polygon:

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
            rv += " "
            rv += point2str(self.point[i])

        ax = self.point[1].x - self.point[0].x
        ay = self.point[1].y - self.point[0].y
        bx = self.point[2].x - self.point[0].x
        by = self.point[2].y - self.point[0].y

        if (ax * by - bx * ay) > -0.000001:
            rv += " ccw"
        else:
            rv += " cw"

        rv += ">"

        return rv

    cpdef void ensure_winding(Polygon self):
        """
        Checks to ensure that the winding of this polygon is what
        Ren'Py expects (CCW). If not, rearranges the points top
        ensure the winding is correct.
        """

        cdef float ax, ay, bx, by
        cdef int i, j
        cdef Point2 t

        # Check each point after the second to see if it's on the right
        # side of the line between points 0 and 1.

        ax = self.point[1].x - self.point[0].x
        ay = self.point[1].y - self.point[0].y

        for 2 <= i < self.points:

            bx = self.point[i].x - self.point[0].x
            by = self.point[i].y - self.point[0].y

            if (ax * by - bx * ay) > -0.000001:
                return

        # If we're here, the winding is bad, and needs to be fixed by swapping
        # points around.

        i = 0
        j = self.points - 1

        while i < j:
            tmp = self.point[i]
            self.point[i] = self.point[j]
            self.point[j] = tmp

            i += 1
            j -= 1


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

    @staticmethod
    def rectangle(float l, float b, float r, float t):
        cdef Polygon rv = Polygon(4)
        rv.points = 4

        rv.point[0].x = l
        rv.point[0].y = b

        rv.point[1].x = r
        rv.point[1].y = b

        rv.point[2].x = r
        rv.point[2].y = t

        rv.point[3].x = l
        rv.point[3].y = t

        return rv

    cpdef Polygon intersect(Polygon self, Polygon p):
        """
        Intersects this polygon with `p`.

        This returns a polygon or None. The polygon may be this Polygon in
        the case where the intersection is the same as this Polygon.
        """

        cdef int i
        cdef int j

        self.ensure_winding()
        p.ensure_winding()

        rv = self

        j = p.points - 1

        for 0 <= i < p.points:
            rv = intersectOnce(p.point[j], p.point[i], rv)

            if rv is None:
                return None

            j = i

        return rv


    cpdef Polygon copy(Polygon self):
        """
        Returns a copy of this polygon.
        """

        cdef Polygon rv = Polygon(self.points)
        rv.points = self.points
        memcpy(rv.point, self.point, self.points * sizeof(Point2))
        return rv


    cpdef void multiply_matrix_inplace(Polygon self, Matrix m):
        """
        Multiplies each point's position with the matrix `m`, in place.
        """

        cdef int i

        for 0 <= i < self.points:
            m.transform2(&self.point[i].x, &self.point[i].y, self.point[i].x, self.point[i].y, 0, 1)

    cpdef Polygon multiply_matrix(Polygon self, Matrix m):
        """
        Multiplies each point's position with the matrix `m`, in place,
        and returns a copy.
        """

        cdef Polygon rv = self.copy()
        rv.multiply_matrix_inplace(m)
        return rv


cdef void intersectLines(Point2 a0, Point2 a1, Point2 b0, Point2 b1, Point2 *p):
    """
    Given a line that goes through a0 and a1, and a second line that goes through
    b0 and b1, find the point where the two lines intersect and put it in p.
    """

    cdef float denom = (a0.x - a1.x) * (b0.y - b1.y) - (a0.y - a1.y) * (b0.x - b1.x)
    p.x = ((a0.x * a1.y - a0.y * a1.x) * (b0.x - b1.x) - (a0.x - a1.x) * (b0.x * b1.y - b0.y * b1.x)) / denom
    p.y = ((a0.x * a1.y - a0.y * a1.x) * (b0.y - b1.y) - (a0.y - a1.y) * (b0.x * b1.y - b0.y * b1.x)) / denom



cdef Polygon intersectOnce(Point2 a0, Point2 a1, Polygon p):

    cdef int i
    cdef int j

    # The vector from a0 to a1.
    cdef float lx = a1.x - a0.x
    cdef float ly = a1.y - a0.y

    # The vector from a0 to each point.
    cdef float px
    cdef float py

    cdef bint allin = True
    cdef bint allout = True

    # For each point, are we inside or outside the polygon?
    # We assume we never have more than 1024 sides to the polygon.
    cdef bint inside[1024]

    # Figure out which points are 'inside' the wound line.
    for 0 <= i < p.points:
        px = p.point[i].x - a0.x
        py = p.point[i].y - a0.y

        inside[i] = (lx * py - ly * px) > -0.000001

        allin = allin and inside[i]
        allout = allout and not inside[i]


    # If the points are all out, return None.
    if allout:
        return None

    # If all the points are inside, just return the polygon intact.
    if allin:
        return p

    rv = Polygon(p.points * 2)

    j = p.points - 1

    for 0 <= i < p.points:
        if inside[i]:
            if not inside[j]:
                intersectLines(a0, a1, p.point[j], p.point[i], &rv.point[rv.points])
                rv.points += 1

            rv.point[rv.points].x = p.point[i].x
            rv.point[rv.points].y = p.point[i].y
            rv.points += 1

        else:
            if inside[j]:
                intersectLines(a0, a1, p.point[j], p.point[i], &rv.point[rv.points])
                rv.points += 1

        j = i

    return rv

