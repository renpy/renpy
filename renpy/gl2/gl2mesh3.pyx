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
from renpy.gl2.gl2mesh cimport Mesh, AttributeLayout
from renpy.gl2.gl2mesh import SOLID_LAYOUT, TEXTURE_LAYOUT

cdef class Mesh3(Mesh):

    def __init__(Mesh3 self, AttributeLayout layout, int points, int triangles):
        """
        `layout`
            An object that contains information about how non-geometry attributes
            are laid out.

        `points`
            The number of points for which space should be allocated.

        `triangles`
            The number of triangles for which space should be allocated.

        If `points` or `triangles` are 0, no allocation takes place. The creator
        of the Mesh is responsible for setting point, point_data, attribute, and
        triangle, and for freeing the data when done.
        """

        self.points = 0
        self.point_size = 3

        self.layout = layout

        self.allocated_points = points

        if points:
            self.point = <Point3 *> malloc(points * sizeof(Point3))
            self.point_data = <float *> self.point

            self.attribute = <float *> malloc(points * layout.stride * sizeof(float))

        self.allocated_triangles = triangles

        if triangles:
            self.triangles = 0
            self.triangle = <unsigned int *> malloc(triangles * 3 * sizeof(unsigned int))


    def __dealloc__(Mesh3 self):
        if self.allocated_points:
            free(self.point)
            free(self.attribute)

        if self.allocated_triangles:
            free(self.triangle)

    def __repr__(Mesh3 self):

        cdef int i
        cdef int j

        rv = "<Mesh3 {!r}".format(self.layout.offset)

        for 0 <= i < self.points:
            rv += "\n    {}: {: >8.3f} {:> 8.3f} {:> 8.3f} | ".format(chr(i + 65), self.point[i].x, self.point[i].y, self.point[i].z)
            for 0 <= j < self.layout.stride:
                rv += "{:> 8.3f} ".format(self.attribute[i * self.layout.stride + j])

        rv += "\n    "

        for 0 <= i < self.triangles:
            rv += "{}-{}-{} ".format(
                chr(self.triangle[i * 3 + 0] + 65),
                chr(self.triangle[i * 3 + 1] + 65),
                chr(self.triangle[i * 3 + 2] + 65),
                )

        rv += ">"

        return rv

    @staticmethod
    def rectangle(
            double pl, double pb, double pr, double pt
            ):

        cdef Mesh3 rv = Mesh3(SOLID_LAYOUT, 4, 2)

        rv.points = 4

        rv.point[0].x = pl
        rv.point[0].y = pb
        rv.point[0].z = 0

        rv.point[1].x = pr
        rv.point[1].y = pb
        rv.point[1].z = 0

        rv.point[2].x = pr
        rv.point[2].y = pt
        rv.point[2].z = 0

        rv.point[3].x = pl
        rv.point[3].y = pt
        rv.point[3].z = 0

        rv.triangles = 2

        rv.triangle[0] = 0
        rv.triangle[1] = 1
        rv.triangle[2] = 2

        rv.triangle[3] = 0
        rv.triangle[4] = 2
        rv.triangle[5] = 3

        return rv

    @staticmethod
    def texture_rectangle(
        double pl, double pb, double pr, double pt,
        double tl, double tb, double tr, double tt
        ):

        cdef Mesh3 rv = Mesh3(TEXTURE_LAYOUT, 4, 2)

        rv.points = 4

        rv.point[0].x = pl
        rv.point[0].y = pb
        rv.point[0].z = 0

        rv.point[1].x = pr
        rv.point[1].y = pb
        rv.point[1].z = 0

        rv.point[2].x = pr
        rv.point[2].y = pt
        rv.point[2].z = 0

        rv.point[3].x = pl
        rv.point[3].y = pt
        rv.point[3].z = 0

        rv.attribute[0] = tl
        rv.attribute[1] = tb

        rv.attribute[2] = tr
        rv.attribute[3] = tb

        rv.attribute[4] = tr
        rv.attribute[5] = tt

        rv.attribute[6] = tl
        rv.attribute[7] = tt

        rv.triangles = 2

        rv.triangle[0] = 0
        rv.triangle[1] = 1
        rv.triangle[2] = 2

        rv.triangle[3] = 0
        rv.triangle[4] = 2
        rv.triangle[5] = 3

        return rv

    cpdef Mesh3 crop(Mesh3 self, Polygon p):
        """
        Crops this mesh against Polygon `p`, and returns a new Mesh3.
        """

        return crop_mesh(self, p)

    def get_points(Mesh3 self):
        """
        Returns the points that make up this mesh as tuples.
        """

        cdef int i

        rv = [ ]

        for 0 <= i < self.points:
            rv.append((self.point[i].x, self.point[i].y, self.point[i].z, 1.0))

        return rv

    def get_point0(Mesh3 self):
        """
        Returns the coordinates of one point.
        """

        if self.points == 0:
            return (0.0, 0.0, 0.0, 1.0)
        else:
            return (self.point[0].x, self.point[0].y, self.point[0].z, 1.0)

###############################################################################
# Mesh cropping.

DEF SPLIT_CACHE_LEN = 4

# Stores the information learned about a point when cropping it.
cdef struct CropPoint:
    bint inside
    int replacement

# This is used to indicate that splitting the line between p0 and
# p1 has created point np.
cdef struct CropSplit:
    int p0idx
    int p1idx
    int npidx

# This stores information about the crop operation.
cdef struct CropInfo:

    float x0
    float y0

    float x1
    float y1

    # The number of splits.
    int splits

    # The last four line segment splits.
    CropSplit split[SPLIT_CACHE_LEN]

    # The information learned about the points when cropping them. This
    # is actually created to be
    CropPoint point[0]


cdef void copy_point(Mesh3 old, int op, Mesh3 new, int np):
    """
    Copies the point at index `op` in ci.old to index `np` in ci.new.
    """

    cdef int i
    cdef int stride = old.layout.stride

    new.point[np] = old.point[op]

    for 0 <= i < stride:
        new.attribute[np * stride + i] = old.attribute[op * stride + i]


cdef void intersectLines(
    double x1, double y1,
    double x2, double y2,
    double x3, double y3,
    double x4, double y4,
    float *px, float *py,
    ):
    """
    Given a line that goes through (x1, y1) to (x2, y2), and a second line
    that goes through (x3, y3) and (x4, y4), find the point where the two
    lines intersect.
    """

    cdef double denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    px[0] = <float> ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py[0] = <float> ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom


cdef int split_line(Mesh3 old, Mesh3 new, CropInfo *ci, int p0idx, int p1idx):

    cdef int i

    for 0 <= i < SPLIT_CACHE_LEN:
        if (ci.split[i].p0idx == p0idx) and (ci.split[i].p1idx == p1idx):
            return ci.split[i].npidx
        elif (ci.split[i].p0idx == p1idx) and (ci.split[i].p1idx == p0idx):
            return ci.split[i].npidx

    cdef Point3 p0 # old point 0
    cdef Point3 p1 # old point 1
    cdef Point3 np # new point.

    p0 = old.point[p0idx]
    p1 = old.point[p1idx]

    # Find the location of the new point.
    intersectLines(p0.x, p0.y, p1.x, p1.y, ci.x0, ci.y0, ci.x1, ci.y1, &np.x, &np.y)

    # The distance between p0 and p1.
    cdef float p1dist2d = hypot(p1.x - p0.x, p1.y - p0.y)
    cdef float npdist2d = hypot(np.x - p0.x, np.y - p0.y)

    # The z coordinate is interpolated.
    np.z = p0.z + (npdist2d / p1dist2d) * (p1.z - p0.z)

    # Use the distance with z to interpolate attributes.
    cdef float p1dist3d = hypot(p1dist2d, p1.z - p0.z)
    cdef float npdist3d = hypot(npdist2d, np.z - p0.z)
    cdef float d = npdist3d / p1dist3d

    # Allocate a new point.
    cdef int npidx = new.points
    new.point[npidx] = np
    new.points += 1

    # Interpolate the attributes.
    cdef int stride = old.layout.stride
    cdef float a
    cdef float b

    for 0 <= i < stride:
        a = old.attribute[p0idx * stride + i]
        b = old.attribute[p1idx * stride + i]
        new.attribute[npidx * stride + i] = a + d * (b - a)

    ci.split[ci.splits % SPLIT_CACHE_LEN].p0idx = p0idx
    ci.split[ci.splits % SPLIT_CACHE_LEN].p1idx = p1idx
    ci.split[ci.splits % SPLIT_CACHE_LEN].npidx = npidx
    ci.splits += 1

    return npidx


cdef void triangle1(Mesh3 old, Mesh3 new, CropInfo *ci, int p0, int p1, int p2):
    """
    Processes a triangle where only one point is inside the line.
    """

    cdef int a = split_line(old, new, ci, p0, p1)
    cdef int b = split_line(old, new, ci, p0, p2)

    cdef int t = new.triangles

    new.triangle[t * 3 + 0] = ci.point[p0].replacement
    new.triangle[t * 3 + 1] = a
    new.triangle[t * 3 + 2] = b

    new.triangles += 1


cdef void triangle2(Mesh3 old, Mesh3 new, CropInfo *ci, int p0, int p1, int p2):
    """
    Processes a triangle where two points are inside the line.
    """

    cdef int a = split_line(old, new, ci, p1, p2)
    cdef int b = split_line(old, new, ci, p0, p2)

    cdef int t = new.triangles

    new.triangle[t * 3 + 0] = ci.point[p0].replacement
    new.triangle[t * 3 + 1] = ci.point[p1].replacement
    new.triangle[t * 3 + 2] = a

    t += 1

    new.triangle[t * 3 + 0] = ci.point[p0].replacement
    new.triangle[t * 3 + 1] = a
    new.triangle[t * 3 + 2] = b

    new.triangles += 2


cdef void triangle3(Mesh3 old, Mesh3 new, CropInfo *ci, int p0, int p1, int p2):
    """
    Processes a triangle that's entirely inside the line.
    """

    cdef int t = new.triangles

    new.triangle[t * 3 + 0] = ci.point[p0].replacement
    new.triangle[t * 3 + 1] = ci.point[p1].replacement
    new.triangle[t * 3 + 2] = ci.point[p2].replacement

    new.triangles += 1


cdef Mesh3 split_mesh(Mesh3 old, float x0, float y0, float x1, float y1):

    cdef int i
    cdef int op, np

    cdef CropInfo *ci = <CropInfo *> malloc(sizeof(CropInfo) + old.points * sizeof(CropPoint))

    ci.x0 = x0
    ci.y0 = y0
    ci.x1 = x1
    ci.y1 = y1

    # Step 1: Determine what points are inside and outside the line.

    cdef bint all_inside
    cdef bint all_outside

    # The vector corresponding to the line.
    cdef float lx = x1 - x0
    cdef float ly = y1 - y0

    # The vector corresponding to the point.
    cdef float px
    cdef float py

    all_outside = True
    all_inside = True

    for 0 <= i < old.points:
        px = old.point[i].x - x0
        py = old.point[i].y - y0

        if (lx * py - ly * px) > -0.000001:
            all_outside = False
            ci.point[i].inside = True
        else:
            all_inside = False
            ci.point[i].inside = False

    # Step 1a: Short circuit if all points are inside or out, otherwise
    # allocate a new object.

    if all_outside:
        free(ci)
        return Mesh3(old.layout, 0, 0)

    if all_inside:
        free(ci)
        return old

    cdef Mesh3 new = Mesh3(old.layout, old.points + old.triangles * 2, old.triangles * 2)

    # Step 2: Copy points that are inside.

    for 0 <= i < old.points:
        if ci.point[i].inside:
            copy_point(old, i, new, new.points)
            ci.point[i].replacement = new.points
            new.points += 1
        else:
            ci.point[i].replacement = -1

    ci.splits = 0

    for 0 <= i < SPLIT_CACHE_LEN:
        ci.split[i].p0idx = -1
        ci.split[i].p1idx = -1

    # Step 3: Triangles.

    # Indexes of the three points that make up a triangle.
    cdef int p0
    cdef int p1
    cdef int p2

    # Are the points inside the triangle?
    cdef bint p0in
    cdef bint p1in
    cdef bint p2in

    for 0 <= i < old.triangles:
        p0 = old.triangle[3 * i + 0]
        p1 = old.triangle[3 * i + 1]
        p2 = old.triangle[3 * i + 2]

        p0in = ci.point[p0].inside
        p1in = ci.point[p1].inside
        p2in = ci.point[p2].inside

        if p0in and p1in and p2in:
            triangle3(old, new, ci, p0, p1, p2)

        elif (not p0in) and (not p1in) and (not p2in):
            continue

        elif p0in and (not p1in) and (not p2in):
            triangle1(old, new, ci, p0, p1, p2)
        elif (not p0in) and p1in and (not p2in):
            triangle1(old, new, ci, p1, p2, p0)
        elif (not p0in) and (not p1in) and p2in:
            triangle1(old, new, ci, p2, p0, p1)

        elif p0in and p1in and (not p2in):
            triangle2(old, new, ci, p0, p1, p2 )
        elif (not p0in) and p1in and p2in:
            triangle2(old, new, ci, p1, p2, p0)
        elif p0in and (not p1in) and p2in:
            triangle2(old, new, ci, p2, p0, p1)

    free(ci)
    return new

cdef Mesh3 crop_mesh(Mesh3 m, Polygon p):
    """
    Returns a new Mesh that only the portion of `d` that is entirely
    contained in `p`.
    """

    cdef int i
    cdef int j

    rv = m

    p.ensure_winding()

    if p.points < 3:
        return Mesh3(m.layout, 0, 0)

    j = p.points - 1

    for 0 <= i < p.points:
        rv = split_mesh(rv, p.point[j].x, p.point[j].y, p.point[i].x, p.point[i].y)
        j = i

    return rv
