from __future__ import print_function

from renpy.display.matrix cimport Matrix
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from libc.math cimport copysign

DEF MAX_POINTS = 128

DEF X = 0
DEF Y = 1
DEF Z = 2
DEF W = 3

DEF TX = 4
DEF TY = 5


cdef class Polygon:

    def __init__(Polygon self, int stride, int points, data):
        """
        Allocates a new Polygon.

        `stride`
            The number of floats per vertex. This should be at least 3, for the
            default aPosition vec3.

        `points`
            The number of vertices in the polygon that space is allocated for.
            If `data` is given, this is also the number of points in the polygon.

        `data`
            If not None, an iterable of length stride * points, that gives the
            vertex data for each of the points.
        """

        cdef int i

        self.stride = stride

        self.data = <float *> malloc(sizeof(float) * points * stride)

        if data is None:
            self.points = 0
        else:
            self.points = points

            for 0 <= i < stride * points:
                self.data[i] = data[i]

    def __dealloc__(Polygon self):
        free(self.data)

    cpdef Polygon copy(Polygon self):
        """
        Returns a copy of this polygon.
        """

        cdef Polygon rv = Polygon(self.stride, self.points, None)
        rv.points = self.points
        memcpy(rv.data, self.data, sizeof(float) * self.stride * self.points)
        return rv

    cpdef void offset_inplace(Polygon self, double x, double y, double z):
        cdef float *p = self.data
        cdef int i

        for 0 <= i < self.points:
            p[X] += x
            p[Y] += y
            p[Z] += z

            p += self.stride

    cpdef Polygon offset(Polygon self, double x, double y, double z):
        cdef Polygon rv = self.copy()
        rv.offset_inplace(x, y, z)
        return rv

    cpdef void perspective_divide_inplace(Polygon self):
        """
        Performs a perspective divide on each point in this polygon, in place.
        """

        cdef float *p = self.data
        cdef int i

        for 0 <= i < self.points:
            if p[W]:
                p[X] /= p[W]
                p[Y] /= p[W]
                p[Z] /= p[W]

            p += self.stride

    cpdef Polygon perspective_divide(Polygon self):
        """
        Returns a perspective divided copy of this polygon.
        """

        cdef Polygon rv = self.copy()
        rv.perspective_divide_inplace()
        return rv

    cpdef void multiply_matrix_inplace(Polygon self, Matrix m):
        """
        Multiplies each point's position with the matrix `m`, in place.
        """

        cdef int i
        cdef float *p = self.data

        for 0 <= i < self.points:
            m.transform4(p, p+1, p+2, p+3, p[0], p[1], p[2], p[3])
            p += self.stride

    cpdef Polygon multiply_matrix(Polygon self, Matrix m):
        """
        Multiplies each point's position with the matrix `m`, in place,
        and returns a copy.
        """

        cdef Polygon rv = self.copy()
        rv.multiply_matrix_inplace(m)
        return rv

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.multiply_matrix(other)

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            return self.multiply_matrix(other)

        return NotImplemented

    cpdef Polygon intersect(Polygon self, Polygon other):
        """
        Returns a new polygon that is the intersection of the current polygon
        and the other polygon.
        """

        rv = intersect(other, self, self.stride + other.stride - 4, True)

        if rv is None:
            return None

        # We only need to interpolate OP if it has something other than
        # position data.
        if other.stride > 4:
            barycentric(other, rv, self.stride - 4)

        barycentric(self, rv, 0)

        return rv

    def __repr__(self):
        rv = "<Polygon"

        for 0 <= p < self.points:
            rv += "\n  ["
            for 0 <= i < self.stride:
                rv += "{:g}, ".format(self.data[p * self.stride + i])
            rv += "]"

        rv += ">"
        return rv


cpdef Polygon rectangle(double l, double t, double r, double b):
    """
    Generates a rectangle with one corner at (l, t, 0, 1) and the other at (r, b, 0, 1).
    """

    cdef Polygon rv = Polygon(4, 4, None)

    rv.points = 4

    cdef float *p = rv.data

    p[X] = l
    p[Y] = t
    p[Z] = 0
    p[W] = 1

    p += 4

    p[X] = r
    p[Y] = t
    p[Z] = 0
    p[W] = 1

    p += 4

    p[X] = r
    p[Y] = b
    p[Z] = 0
    p[W] = 1

    p += 4

    p[X] = l
    p[Y] = b
    p[Z] = 0
    p[W] = 1

    return rv


cpdef Polygon texture_rectangle(double pl, double pt, double pr, double pb, double tl, double tt, double tr, double tb):
    """
    This generates a rectangle with teture coordinates. One corner is at (pl, pt, 0, 1) with
    texture coordinates (tl, tt), while the other is at (pr, pb, 0, 1) / (tr, tb).
    """

    cdef Polygon rv = Polygon(6, 4, None)

    rv.points = 4

    cdef float *p = rv.data

    p[X] = pl
    p[Y] = pt
    p[Z] = 0
    p[W] = 1
    p[TX] = tl
    p[TY] = tt

    p += 6

    p[X] = pr
    p[Y] = pt
    p[Z] = 0
    p[W] = 1
    p[TX] = tr
    p[TY] = tt

    p += 6

    p[X] = pr
    p[Y] = pb
    p[Z] = 0
    p[W] = 1
    p[TX] = tr
    p[TY] = tb

    p += 6

    p[X] = pl
    p[Y] = pb
    p[Z] = 0
    p[W] = 1
    p[TX] = tl
    p[TY] = tb

    return rv


# Accssor functions for the contents of polygons.
cdef inline float get(Polygon p, int index, int offset):
    return p.data[index * p.stride + offset]

cdef inline float *ref(Polygon p, int index, int offset):
    return &p.data[index * p.stride + offset]

cdef inline float set(Polygon p, int index, int offset, float value):
    p.data[index * p.stride + offset] = value
    return value


cdef void intersectLines(
    float x1, float y1,
    float x2, float y2,
    float x3, float y3,
    float x4, float y4,
    float *px, float *py,
    ):

    """
    Given a line that goes through (x1, y1) to (x2, y2), and a second line
    that goes through (x3, y3) and (x4, y4), find the point where the two
    lines intersect.


    """

    cdef float denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px[0] = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py[0] = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

cdef Polygon intersectOnce(float winding, float a0x, float a0y, float a1x, float a1y, Polygon p, int rvstride):

    # The vector from a0 to a1.
    cdef float vecax = a1x - a0x
    cdef float vecay = a1y - a0y

    # The vector from a0 to each point.
    cdef float vecpx
    cdef float vexpx

    # For each point, are we inside or outside?
    cdef bint inside[MAX_POINTS]

    cdef int i
    cdef int j
    cdef bint allin = True

    # Figure out which points are 'inside' the wound line.
    for 0 <= i < p.points:
        vecpx = get(p, i, X) - a0x
        vecpy = get(p, i, Y) - a0y

        inside[i] = winding * (vecax * vecpy - vecay * vecpx) <= 0.00001
        allin = allin and inside[i]

    # If all the points are inside, just return the polygon intact.
    if allin:
        return p

    rv = Polygon(rvstride, p.points * 2, None)

    j = p.points - 1

    for 0 <= i < p.points:
        if inside[i]:
            if not inside[j]:
                intersectLines(
                    a0x, a0y, a1x, a1y,
                    get(p, j, X), get(p, j, Y), get(p, i, X), get(p, i, Y),
                    ref(rv, rv.points, X), ref(rv, rv.points, Y))

                rv.points += 1

            set(rv, rv.points, X, get(p, i, X))
            set(rv, rv.points, Y, get(p, i, Y))
            rv.points += 1

        else:
            if inside[j]:
                intersectLines(
                    a0x, a0y, a1x, a1y,
                    get(p, j, X), get(p, j, Y), get(p, i, X), get(p, i, Y),
                    ref(rv, rv.points, X), ref(rv, rv.points, Y))

                rv.points += 1

        j = i

    return rv


cdef Polygon restride_polygon(Polygon src, int new_stride):
    """
    Returns a copy of the polygon with the stride changed to
    be `new_stride`.
    """

    cdef Polygon rv = Polygon(new_stride, src.points, None)

    cdef float *ap = src.data
    cdef float *bp = rv.data

    cdef int i

    for 0 <= i < src.points:
        bp[X] = ap[X]
        bp[Y] = ap[Y]
        bp[Z] = ap[Z]

        ap += src.stride
        bp += rv.stride

    rv.points = src.points

    return rv


cpdef intersect(Polygon a, Polygon b, int new_stride, bint copy):
    """
    Given two Polygons, returns a new Polygon that is the intersecti of
    the two. This assumes that both polygons are convex, and wound in the
    same direction (clockwise or counterclockwise).

    `new_stride` is the stride of the new Polygon.
    """

    cdef int i
    cdef float a0x, a0y, a1x, a1y
    cdef float winding

    a0x = get(a, a.points-2, X)
    a0y = get(a, a.points-2, Y)

    a1x = get(a, a.points-1, X)
    a1y = get(a, a.points-1, Y)

    cdef Polygon rv = b

    for 0 <= i < a.points:
        a2x = get(a, i, X)
        a2y = get(a, i, Y)

        winding = (a2x - a0x) * (a1y - a0y) - (a2y - a0y) * (a1x - a0x)
        winding = copysign(1.0, winding)

        if winding:
            rv = intersectOnce(winding, a1x, a1y, a2x, a2y, rv, new_stride)

            if rv.points < 3:
                return None

        a0x = a1x
        a0y = a1y

        a1x = a2x
        a1y = a2y

    if rv is b:
        if (not copy) and (new_stride == rv.stride):
            return rv

        rv = restride_polygon(rv, new_stride)

    return rv


cpdef barycentric(Polygon a, Polygon b, int offset):
    """
    This uses barycentric interpolation to transfer the attributes from
    Polygon `a` to Polygon `b`, starting at `offset`.
    """

    cdef int i
    cdef int j
    cdef int k

    cdef float ax0 = get(a, 0, X)
    cdef float ay0 = get(a, 0, Y)
    cdef float az0 = get(a, 0, Z)

    cdef float v0x = get(a, 1, X) - ax0
    cdef float v0y = get(a, 1, Y) - ay0
    cdef float v0z = get(a, 1, Z) - az0

    cdef float v1x, v1y, v1z, v2x, v2y, v2z
    cdef float d00, d01, d11, d20, d21
    cdef float d003, d013, d113, d203, d213
    cdef float denom
    cdef float u, v, w

    for 2 <= i < a.points:

        v1x = get(a, i, X) - ax0
        v1y = get(a, i, Y) - ay0
        v1z = get(a, i, Z) - az0

        d00 = v0x * v0x + v0y * v0y
        d01 = v0x * v1x + v0y * v1y
        d11 = v1x * v1x + v1y * v1y

        d003 = d00 + v0z * v0z
        d013 = d01 + v0z * v1z
        d113 = d11 + v1z * v1z

        denom = d00 * d11 - d01 * d01
        denom3 = d003 * d113 - d013 * d013

        if denom and denom3:

            for 0 <= j < b.points:

                v2x = get(b, j, X) - ax0
                v2y = get(b, j, Y) - ay0

                d20 = v2x * v0x + v2y * v0y
                d21 = v2x * v1x + v2y * v1y

                v = (d11 * d20 - d01 * d21) / denom
                w = (d00 * d21 - d01 * d20) / denom

                if not ((-0.00001 <= v <= 1.00001) and (-0.00001 <= w <= 1.00001)):
                    continue

                u = 1.0 - v - w

                z = u * az0 + v * get(a, i-1, Z) + w * get(a, i, Z)
                set(b, j, Z, z)
                set(b, j, W, 1.0)

                v2z = z - az0

                d203 = d20 + v2z * v0z
                d213 = d21 + v2z * v1z

                v = (d113 * d203 - d013 * d213) / denom3
                w = (d003 * d213 - d013 * d203) / denom3
                u = 1.0 - v - w

                for 3 <= k < a.stride:
                    set(b, j, k + offset,
                        u * get(a, 0, k) +
                        v * get(a, i-1, k) +
                        w * get(a, i, k))

        v0x = v1x
        v0y = v1y


def barycentric_point(Polygon a, float x, float y):
    """
    This expects Polygon a to be a polygon with a stride of 6, with a
    position (x, y, z, 1) and a pair of attributes (tx, ty) at each
    point.

    Given `x` and `y`, this barycentricly interpolates the `x` and `y`
    at the point, if it's inside the Polygon. It returns None, None
    if the point is inside the polygon.

    This is mostly intended to be used to interpolate screen-space
    coordinates onto a Render's internal coordinate space.
    """

    cdef Polygon b = Polygon(6, 1, None)
    b.points = 1

    cdef float *p = b.data
    p[X] = x
    p[Y] = y
    p[Z] = 0.0
    p[W] = 0.0

    barycentric(a, b, 0)

    if p[W] == 0:
        return None, None

    return (p[TX], p[TY])


cdef class Mesh:

    def __init__(Mesh self):
        """
        Represents a mesh consisting of one or more polygons. A mesh needs
        to be created either by:

        * First, create the mesh object.
        * Next, add any additional attributes to it.
        * Finally, add polygons to the mesh.

        Or by copying the mesh or calling a method that returns a new mesh.

        After that, the inplace methods can be called to further change
        the mesh.

        Lastly, get_data can be called to access the mesh data. Once get_data
        is called, the mesh becomes immutable. (This is usally called by
        Shader.draw.)
        """

        self.points = 0
        self.stride = 4
        self.polygons = [ ]
        self.attributes = { "aPosition" : 0 }
        self.data = NULL

    def __dealloc__(Mesh self):
        if self.data:
            free(self.data)

    def add_attribute(Mesh self, name, size):
        """
        Adds an attribute to this mesh.

        `name`
            The name of the attribute.

        `size`
            The number of floats per vertex that make up the attribute.
        """

        self.attributes[name] = self.stride
        self.stride += size

    def add_polygon(Mesh self, data):
        """
        Adds a polygon.

        `data`
            This is an iterable. It should have self.stride data for each
            vertex, and the number of vertices is derived from the length
            of the data.
        """

        cdef Polygon p = Polygon(self.stride, len(data) // self.stride, data)
        self.points += p.points

        self.polygons.append(p)


    def add_rectangle(Mesh self, double x, double y, double w, double h):
        """
        Adds a polygon.
        """

        self.points += 4
        self.polygons.append(rectangle(x, y, w, h))


    def add_texture_rectangle(Mesh self, double pl, double pt, double pr, double pb, double tl, double tt, double tr, double tb):
        """
        Returns a polygon corresponding to a texture rectangle.
        """

        self.points += 4
        self.polygons.append(texture_rectangle(pl, pt, pr, pb, tl, tt, tr, tb))


    cdef float *get_data(Mesh self, int offset):
        """
        When called, this freezes the data of this mesh. It then returns
        a pointer to the data for the attribute at ``offset``. This is a
        pointer to the first piece of data, with others following at
        self.stride intervals.
        """

        cdef Polygon p
        cdef int i
        cdef int count
        cdef int points

        self.polygon_count = count = len(self.polygons)

        if not count:
            self.polygon_points = 0
            return NULL

        p = self.polygons[0]
        points = p.points

        if count == 1:
            self.polygon_points = points
            return p.data + offset

        if not self.data:
            self.data = <float *> malloc(self.points * self.stride * sizeof(float))

            i = 0

            for p in self.polygons:
                memcpy(&self.data[i], p.data, p.points * self.stride * sizeof(float))
                i += p.points * self.stride

                if p.points != points:
                    points = 0

            self.polygon_points = points

        return self.data + offset

    cpdef Mesh copy(Mesh self):
        """
        Returns a copy of this Mesh.
        """

        rv = Mesh()
        rv.stride = self.stride
        rv.points = self.points
        rv.polygons = [ i.copy() for i in self.polygons ]
        rv.attributes = self.attributes

        return rv

    cpdef void offset_inplace(Mesh self, double x, double y, double z):
        """
        Offsets each polygon in the mesh, in place.
        """

        cdef Polygon p

        for p in self.polygons:
            p.offset_inplace(x, y, z)

    cpdef Mesh offset(self, double x, double y, double z):
        """
        Returns a copy of the mesh with each polygon offset.
        """

        cdef Mesh rv = self.copy()
        rv.offset_inplace(x, y, z)
        return rv


    cpdef void perspective_divide_inplace(Mesh self):
        """
        Performs a perspective divide on this mesh, inplace.
        """

        cdef Polygon p

        for p in self.polygons:
            p.perspective_divide_inplace()

    cpdef Mesh perspective_divide(Mesh self):
        """
        Returns a copy of this mesh that has been perspective divided.
        """

        cdef Mesh rv = self.copy()
        rv.perspective_divide_inplace()
        return rv

    cpdef void multiply_matrix_inplace(Mesh self, Matrix matrix):
        """
        Multiplies the position data in this Mesh by the matrix, in place.
        """

        cdef Polygon p

        for p in self.polygons:
            p.multiply_matrix_inplace(matrix)

    cpdef Mesh multiply_matrix(Mesh self, Matrix matrix):
        """
        Returns a copy of this Mesh with the position data multipled by Matrix.
        """

        cdef Mesh rv = self.copy()
        rv.multiply_matrix_inplace(matrix)
        return rv

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.multiply_matrix(other)

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            return self.multiply_matrix(other)

        return NotImplemented

    cpdef Mesh intersect(Mesh self, Mesh other):
        """
        Intersects this mesh with another mesh, and returns a new mesh that
        is the result. The resulting mesh has z- and w-coordinates from this
        mesh. Attributes that are present in this mesh are taken from
        this mesh, otherwise the attributes from the other mesh are used.
        """

        rv = Mesh()
        rv.stride = self.stride + other.stride - 4
        rv.attributes = { k : v + self.stride - 4 for k, v in other.attributes.iteritems() }
        rv.attributes.update(self.attributes)

        cdef Polygon op
        cdef Polygon sp
        cdef Polygon p

        for op in other.polygons:
            for sp in self.polygons:
                p = intersect(op, sp, rv.stride, True)

                if p is None:
                    continue

                # We only need to interpolate OP if it has something other than
                # position data.
                if op.stride > 4:
                    barycentric(op, p, self.stride - 4)

                barycentric(sp, p, 0)

                rv.polygons.append(p)
                rv.points += p.points

        return rv

    cpdef Mesh crop(Mesh self, Polygon op):
        """
        This uses the polygon `op` to crop this mesh.

        This may or may not return a new Mesh. (If op contains all of self, it
        will return self.)
        """

        same = True

        cdef Polygon sp
        cdef Polygon p

        cdef list polygons = [ ]
        cdef int points = 0

        for sp in self.polygons:
            p = intersect(op, sp, self.stride, False)

            if p is None:
                same = False
                continue

            if p is not sp:
                same = False
                barycentric(sp, p, 0)

            polygons.append(p)
            points += p.points

        if same:
            return self

        rv = Mesh()
        rv.stride = self.stride
        rv.attributes = self.attributes
        rv.polygons = polygons
        rv.points = points

        return rv

    def __repr__(self):
        rv = "<Mesh "

        for p in self.polygons:
            rv += repr(p)
            rv += ", "

        rv += ">"
        return rv



