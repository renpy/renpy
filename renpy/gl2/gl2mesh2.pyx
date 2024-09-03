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
from renpy.gl2.gl2mesh import SOLID_LAYOUT, TEXTURE_LAYOUT, TEXT_LAYOUT

cdef class Mesh2(Mesh):

    def __init__(Mesh2 self, AttributeLayout layout, int points, int triangles):
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

        self.layout = layout

        self.allocated_points = points
        self.point_size = 2

        if points:

            self.points = 0
            self.point = <Point2 *> malloc(points * sizeof(Point2))
            self.point_data = <float *> self.point

            self.attribute = <float *> malloc(points * layout.stride * sizeof(float))

        self.allocated_triangles = triangles

        if triangles:

            self.triangles = 0
            self.triangle = <unsigned int *> malloc(triangles * 3 * sizeof(unsigned int))

    def __dealloc__(Mesh2 self):

        if self.allocated_points:
            free(self.point)
            free(self.attribute)

        if self.allocated_triangles:
            free(self.triangle)

    def __repr__(Mesh2 self):

        cdef int i
        cdef int j

        rv = "<Mesh2 {!r}".format(self.layout.offset)

        for 0 <= i < self.points:
            rv += "\n    {}: {: >8.3f} {:> 8.3f}| ".format(chr(i + 65), self.point[i].x, self.point[i].y)
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

        cdef Mesh2 rv = Mesh2(SOLID_LAYOUT, 4, 2)

        rv.points = 4

        rv.point[0].x = pl
        rv.point[0].y = pb

        rv.point[1].x = pr
        rv.point[1].y = pb

        rv.point[2].x = pr
        rv.point[2].y = pt

        rv.point[3].x = pl
        rv.point[3].y = pt

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

        cdef Mesh2 rv = Mesh2(TEXTURE_LAYOUT, 4, 2)

        rv.points = 4

        rv.point[0].x = pl
        rv.point[0].y = pb

        rv.point[1].x = pr
        rv.point[1].y = pb

        rv.point[2].x = pr
        rv.point[2].y = pt

        rv.point[3].x = pl
        rv.point[3].y = pt

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


    @staticmethod
    def texture_grid_mesh(
        int width, int height,
        double pl, double pb, double pr, double pt,
        double tl, double tb, double tr, double tt
        ):

        cdef Mesh2 rv = Mesh2(TEXTURE_LAYOUT, width * height, 2 * (width - 1) * (height - 1))

        cdef int x
        cdef int y
        cdef int i

        cdef int p0
        cdef int p1
        cdef int p2
        cdef int p3

        rv.points = width * height

        for 0 <= y < height:
            for 0 <= x < width:
                i = x + y * width

                rv.point[i].x = pl + (pr - pl) * (1.0 * x / (width - 1))
                rv.point[i].y = pb + (pt - pb) * (1.0 * y / (height - 1))

                rv.attribute[i * 2] = tl + (tr - tl) * (1.0 * x / (width - 1))
                rv.attribute[i * 2 + 1] = tb + (tt - tb) * (1.0 * y / (height - 1))

        rv.triangles = 2 * (width - 1) * (height - 1)

        for 0 <= y < height - 1:
            for 0 <= x < width - 1:

                i = 6 * (x + y * (width - 1))

                p0 = x + y * width
                p1 = p0 + 1
                p2 = p0 + width + 1
                p3 = p0 + width

                rv.triangle[i + 0] = p0
                rv.triangle[i + 1] = p1
                rv.triangle[i + 2] = p2

                rv.triangle[i + 3] = p0
                rv.triangle[i + 4] = p2
                rv.triangle[i + 5] = p3

        return rv

    @staticmethod
    def text_mesh(int glyphs):
        """
        Creates a mesh that can hold `glyphs` glyphs.
        """

        cdef Mesh2 rv = Mesh2(TEXT_LAYOUT, glyphs * 4, glyphs * 2)

        rv.points = 0
        rv.triangles = 0

        return rv

    def add_glyph(Mesh2 self,
        double tw, double th,
        double cx, double cy,
        double index,
        double left, double top, double right, double bottom,
        double left_time, double right_time,
        double ascent, double descent,
        ):
        """
        Adds a glyph to a mesh created by `text_mesh`.

        `tx`, `ty`
            The size of the texture the glyph is in.
        """

        if self.layout is not TEXT_LAYOUT:
            raise ValueError("This mesh is not a text mesh.")

        if tw == 0 or th == 0:
            return

        cdef double tex_left = left / tw
        cdef double tex_right = right / tw
        cdef double tex_top = top / th
        cdef double tex_bottom = bottom / th

        cdef double width = right - left
        cdef double height = bottom - top

        cdef double mint = min(left_time, right_time)
        cdef double maxt = max(left_time, right_time)

        cdef int point = self.points
        cdef int stride = self.layout.stride
        cdef int attribute = self.points * stride

        self.point[point + 0].x = left
        self.point[point + 0].y = bottom
        self.attribute[attribute + 0] = tex_left
        self.attribute[attribute + 1] = tex_bottom
        self.attribute[attribute + 2] = cx
        self.attribute[attribute + 3] = cy
        self.attribute[attribute + 4] = left_time

        self.attribute[attribute + 5] = mint
        self.attribute[attribute + 6] = maxt
        self.attribute[attribute + 7] = index
        self.attribute[attribute + 8] = left
        self.attribute[attribute + 9] = top
        self.attribute[attribute + 10] = width
        self.attribute[attribute + 11] = height
        self.attribute[attribute + 12] = ascent
        self.attribute[attribute + 13] = descent

        attribute += stride

        self.point[point + 1].x = right
        self.point[point + 1].y = bottom
        self.attribute[attribute + 0] = tex_right
        self.attribute[attribute + 1] = tex_bottom
        self.attribute[attribute + 2] = cx
        self.attribute[attribute + 3] = cy
        self.attribute[attribute + 4] = right_time

        self.attribute[attribute + 5] = mint
        self.attribute[attribute + 6] = maxt
        self.attribute[attribute + 7] = index
        self.attribute[attribute + 8] = left
        self.attribute[attribute + 9] = top
        self.attribute[attribute + 10] = width
        self.attribute[attribute + 11] = height
        self.attribute[attribute + 12] = ascent
        self.attribute[attribute + 13] = descent

        attribute += stride

        self.point[point + 2].x = right
        self.point[point + 2].y = top
        self.attribute[attribute + 0] = tex_right
        self.attribute[attribute + 1] = tex_top
        self.attribute[attribute + 2] = cx
        self.attribute[attribute + 3] = cy
        self.attribute[attribute + 4] = right_time

        self.attribute[attribute + 5] = mint
        self.attribute[attribute + 6] = maxt
        self.attribute[attribute + 7] = index
        self.attribute[attribute + 8] = left
        self.attribute[attribute + 9] = top
        self.attribute[attribute + 10] = width
        self.attribute[attribute + 11] = height
        self.attribute[attribute + 12] = ascent
        self.attribute[attribute + 13] = descent

        attribute += stride

        self.point[point + 3].x = left
        self.point[point + 3].y = top
        self.attribute[attribute + 0] = tex_left
        self.attribute[attribute + 1] = tex_top
        self.attribute[attribute + 2] = cx
        self.attribute[attribute + 3] = cy
        self.attribute[attribute + 4] = left_time

        self.attribute[attribute + 5] = mint
        self.attribute[attribute + 6] = maxt
        self.attribute[attribute + 7] = index
        self.attribute[attribute + 8] = left
        self.attribute[attribute + 9] = top
        self.attribute[attribute + 10] = width
        self.attribute[attribute + 11] = height
        self.attribute[attribute + 12] = ascent
        self.attribute[attribute + 13] = descent

        cdef int triangle = self.triangles * 3

        self.triangle[triangle + 0] = point + 0
        self.triangle[triangle + 1] = point + 1
        self.triangle[triangle + 2] = point + 2

        self.triangle[triangle + 3] = point + 0
        self.triangle[triangle + 4] = point + 2
        self.triangle[triangle + 5] = point + 3

        self.points += 4
        self.triangles += 2

    cpdef Mesh2 crop(Mesh2 self, Polygon p):
        """
        Crops this mesh against Polygon `p`, and returns a new Mesh2.
        """

        return crop_mesh(self, p)

    def remap_texture(
        self,
        float old_x, float old_y, float old_w, float old_h,
        float new_x, float new_y, float new_w, float new_h):

        """
        Offsets the texture coordinates of this mesh by the given amount.
        """

        cdef int i
        cdef float x
        cdef float y

        if new_w == 0 or new_h == 0:
            return

        for 0 <= i < self.points:
            x = self.attribute[i * self.layout.stride + 0] * old_w + old_x
            y = self.attribute[i * self.layout.stride + 1] * old_h + old_y

            self.attribute[i * self.layout.stride + 0] = (x - new_x) / new_w
            self.attribute[i * self.layout.stride + 1] = (y - new_y) / new_h

    def get_points(Mesh2 self):
        """
        Returns the points that make up this mesh as tuples.
        """

        cdef int i

        rv = [ ]

        for 0 <= i < self.points:
            rv.append((self.point[i].x, self.point[i].y, 0.0, 1.0))

        return rv

    def get_point0(Mesh2 self):
        """
        Returns the coordinates of the first point.
        """

        if self.points == 0:
            return (0.0, 0.0, 0.0, 1.0)
        else:
            return (self.point[0].x, self.point[0].y, 0.0, 1.0)


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


cdef void copy_point(Mesh2 old, int op, Mesh2 new, int np):
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


cdef int split_line(Mesh2 old, Mesh2 new, CropInfo *ci, int p0idx, int p1idx):

    cdef int i

    for 0 <= i < SPLIT_CACHE_LEN:
        if (ci.split[i].p0idx == p0idx) and (ci.split[i].p1idx == p1idx):
            return ci.split[i].npidx
        elif (ci.split[i].p0idx == p1idx) and (ci.split[i].p1idx == p0idx):
            return ci.split[i].npidx

    cdef Point2 p0 # old point 0
    cdef Point2 p1 # old point 1
    cdef Point2 np # new point.

    p0 = old.point[p0idx]
    p1 = old.point[p1idx]

    # Find the location of the new point.
    intersectLines(p0.x, p0.y, p1.x, p1.y, ci.x0, ci.y0, ci.x1, ci.y1, &np.x, &np.y)

    # The distance between p0 and p1.
    cdef float p1dist2d = hypot(p1.x - p0.x, p1.y - p0.y)
    cdef float npdist2d = hypot(np.x - p0.x, np.y - p0.y)
    cdef float d = npdist2d / p1dist2d

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


cdef void triangle1(Mesh2 old, Mesh2 new, CropInfo *ci, int p0, int p1, int p2):
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


cdef void triangle2(Mesh2 old, Mesh2 new, CropInfo *ci, int p0, int p1, int p2):
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


cdef void triangle3(Mesh2 old, Mesh2 new, CropInfo *ci, int p0, int p1, int p2):
    """
    Processes a triangle that's entirely inside the line.
    """

    cdef int t = new.triangles

    new.triangle[t * 3 + 0] = ci.point[p0].replacement
    new.triangle[t * 3 + 1] = ci.point[p1].replacement
    new.triangle[t * 3 + 2] = ci.point[p2].replacement

    new.triangles += 1


cdef Mesh2 split_mesh(Mesh2 old, float x0, float y0, float x1, float y1):

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
        return Mesh2(old.layout, 0, 0)

    if all_inside:
        free(ci)
        return old

    cdef Mesh2 new = Mesh2(old.layout, old.points + old.triangles * 2, old.triangles * 2)

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

cdef Mesh2 crop_mesh(Mesh2 m, Polygon p):
    """
    Returns a new Mesh that only the portion of `d` that is entirely
    contained in `p`.
    """

    cdef int i
    cdef int j

    p.ensure_winding()

    if p.points < 3:
        return Mesh2(m.layout, 0, 0)

    rv = m

    j = p.points - 1

    for 0 <= i < p.points:
        rv = split_mesh(rv, p.point[j].x, p.point[j].y, p.point[i].x, p.point[i].y)
        j = i

    return rv
