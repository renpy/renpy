# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

from libc.string cimport memset
from libc.math cimport sin, cos, M_PI as pi

cdef float *aligned_1 = [ 1, 0, 0, 0, 0, 1, 0, 0,  0, 0, 1, 0, 0, 0, 0, 1 ]
cdef float *aligned_2 = [ 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ]

fields = [
    "xdx", "ydx", "zdx", "wdx",
    "xdy", "ydy", "zdy", "wdy",
    "xdz", "ydz", "zdz", "wdz",
    "xdw", "ydw", "zdw", "wdw",
    ]

cdef inline bint absne(float a, float b):
    return abs(a - b) > .0001

cdef inline bint abseq(float a, float b):
    return abs(a - b) < .0001


cdef class Matrix:
    """
    :doc: matrix
    :args: (l)

    This represents a 4x4 matrix, that is used in various places in Ren'Py.

    When used to transform coordinates, the 16 elements of this matrix are::

        xdx, xdy, xdz, xdw,
        ydx, ydy, ydz, ydw,
        zdx, zdy, zdz, zdw,
        wdx, wdy, wdz, wdw

    where x' = xdx * x + xdy * y + xdz * z + xdw * w, where x is the original
    value of x and x' is the transformed value, and similarly for x, y, x, and
    w.  This is usually applied to a position where w is 1, allowing any combination
    of translation, rotation, and scaling to be expressed in a single matrix.

    When used to transform colors, the 16 elements of this matrix are::

        rdr, rdg, rdb, rda,
        gdr, gdg, gdg, gda,
        bdr, bdg, bdb, bda,
        adr, adg, adb, ada,

    For the red, green, blue, and alpha channels.

    Matrix objects can be multiplied using the Python multiplication operator,
    to generate a matrix that performs both operations. The order in which
    the matrixes appear can matter. Assuming `v` is a position or color being
    transformed::

        (step2 * step1) * v

    is equivalent to::

        step2 * (step1 * v)

    `l`
        This can be a list of 4, 9, or 16 numbers that is used to introduce
        this matrix. If not the full 16, the top-left corner of the matrix
        is initialized, with zdz and wdw set to 1.0 if not given. For example::

            Matrix([ 1, 2, 3, 4 ])

        would result in the Matrix::

            1.0, 2.0, 0.0, 0.0,
            3.0, 4.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
    """

    def __init__(Matrix self, l):

        memset(self.m, 0, sizeof(float) * 16)

        if l is None:
            return

        cdef int lenl = len(l)

        if lenl == 4:
            (self.xdx, self.xdy,
             self.ydx, self.ydy) = l
            self.ydy = 1.0
            self.wdw = 1.0

        elif lenl == 9:
            (self.xdx, self.xdy, self.xdz,
             self.ydx, self.ydy, self.ydz,
             self.zdx, self.zdy, self.zdz) = l
            self.wdw = 1.0

        elif lenl == 16:
            (self.xdx, self.xdy, self.xdz, self.xdw,
             self.ydx, self.ydy, self.ydz, self.ydw,
             self.zdx, self.zdy, self.zdz, self.zdw,
             self.wdx, self.wdy, self.wdz, self.wdw) = l

        else:
            raise Exception("Unsupported matrix length {} (must be 4, 9, or 16).".format(len(l)))


    def __getstate__(self):
        rv = { }

        for i in range(16):
            rv[fields[i]] = self.m[i]

        return rv

    def __setstate__(self, state):

        memset(self.m, 0, sizeof(float) * 16)

        self.zdz = 1.0
        self.wdw = 1.0

        for i in range(16):
            if fields[i] in state:
                self.m[i] = state[fields[i]]

    def __mul__(Matrix self, Matrix other):

        cdef Matrix rv = Matrix(None)

        rv.xdx = other.wdx*self.xdw + other.xdx*self.xdx + other.ydx*self.xdy + other.zdx*self.xdz
        rv.xdy = other.wdy*self.xdw + other.xdy*self.xdx + other.ydy*self.xdy + other.zdy*self.xdz
        rv.xdz = other.wdz*self.xdw + other.xdz*self.xdx + other.ydz*self.xdy + other.zdz*self.xdz
        rv.xdw = other.wdw*self.xdw + other.xdw*self.xdx + other.ydw*self.xdy + other.zdw*self.xdz

        rv.ydx = other.wdx*self.ydw + other.xdx*self.ydx + other.ydx*self.ydy + other.zdx*self.ydz
        rv.ydy = other.wdy*self.ydw + other.xdy*self.ydx + other.ydy*self.ydy + other.zdy*self.ydz
        rv.ydz = other.wdz*self.ydw + other.xdz*self.ydx + other.ydz*self.ydy + other.zdz*self.ydz
        rv.ydw = other.wdw*self.ydw + other.xdw*self.ydx + other.ydw*self.ydy + other.zdw*self.ydz

        rv.zdx = other.wdx*self.zdw + other.xdx*self.zdx + other.ydx*self.zdy + other.zdx*self.zdz
        rv.zdy = other.wdy*self.zdw + other.xdy*self.zdx + other.ydy*self.zdy + other.zdy*self.zdz
        rv.zdz = other.wdz*self.zdw + other.xdz*self.zdx + other.ydz*self.zdy + other.zdz*self.zdz
        rv.zdw = other.wdw*self.zdw + other.xdw*self.zdx + other.ydw*self.zdy + other.zdw*self.zdz

        rv.wdx = other.wdx*self.wdw + other.xdx*self.wdx + other.ydx*self.wdy + other.zdx*self.wdz
        rv.wdy = other.wdy*self.wdw + other.xdy*self.wdx + other.ydy*self.wdy + other.zdy*self.wdz
        rv.wdz = other.wdz*self.wdw + other.xdz*self.wdx + other.ydz*self.wdy + other.zdz*self.wdz
        rv.wdw = other.wdw*self.wdw + other.xdw*self.wdx + other.ydw*self.wdy + other.zdw*self.wdz

        return rv

    def __getitem__(Matrix self, int index):
        if 0 <= index < 16:
            return self.m[index]

        raise IndexError("Matrix index out of range.")

    def __setitem__(Matrix self, int index, float value):
        if 0 <= index < 16:
            self.m[index] = value
            return

        raise IndexError("Matrix index out of range.")

    def __repr__(Matrix self):
        cdef int x, y

        rv = "Matrix(["

        for 0 <= y < 4:
            if y:
                rv += "\n        "
            for 0 <= x < 4:
                rv += "{:10.7f}, ".format(self.m[x + y * 4])

        return rv + "])"

    def transform(Matrix self, float x, float y, float z=0.0, float w=1.0, int components=2):
        cdef float ox, oy, oz, ow

        self.transform4(&ox, &oy, &oz, &ow, x, y, z, w)

        if components == 2:
            return (ox, oy)
        elif components == 3:
            return (ox, oy, oz)
        elif components == 4:
            return (ox, oy, oz, ow)

    def __richcmp__(Matrix self, Matrix other, op):

        if op != 2:
            return NotImplemented

        if self is other:
            return True

        cdef int i
        cdef double total

        total = 0

        for 0 < i < 16:
            total += abs(self.m[i] - other.m[i])

        return total < .0001

    cpdef bint is_unit_aligned(Matrix self):
        """
        Returns true if exactly one of abs(xdx) or abs(xdy) is 1.0, and
        the same for xdy and ydy. This is intended to report if a matrix
        is aligned to the axes.
        """

        cdef int i
        cdef float v
        cdef float total_1
        cdef float total_2

        total_1 = 0
        total_2 = 0

        for 0 < i < 16:
            v = abs(self.m[i])
            total_1 += abs(v - aligned_1[i])
            total_2 += abs(v - aligned_2[i])

        return (total_1 < .0001) or (total_2 < .0001)

    @staticmethod
    cdef bint is_drawable_aligned(Matrix a, Matrix b):
        """
        This returns true if `a` and `b` are drawable aligned with each
        other.

        This is true if for every pair of values v1 and v2, such that
        a*v1 and a*v2 differ by 1 or -1 in either the x or the y dimension,
        b*v1 and b*b2 differ by 1 or -1 in either the x or the y dimension.

        Equivalently, this is true if a polygon projected by `a` can be
        transformed into a polygon projected by `b` using only 90 degree
        rotations, flips, and translation.
        """

        if absne(a.xdz, b.xdz):
            return False

        if absne(a.ydz, b.ydz):
            return False

        if absne(a.zdx, b.zdx):
            return False

        if absne(a.zdy, b.zdy):
            return False

        if absne(a.zdz, b.zdz):
            return False

        if abseq(a.xdx, b.xdx) and abseq(a.xdy, b.xdy) and abseq(a.ydx, b.ydx) and abseq(a.ydy, b.ydy):
            return True

        if abseq(a.xdx, b.xdy) and abseq(a.xdy, b.xdx) and abseq(a.ydx, b.ydy) and abseq(a.ydy, b.ydx):
            return True

        return False

    @staticmethod
    cdef Matrix cidentity():
        return identity_matrix()

    @staticmethod
    def identity():
        """
        Returns an identity matrix.
        """
        return identity_matrix()

    @staticmethod
    cdef Matrix coffset(float x, float y, float z):
        return offset_matrix(x, y, z)

    @staticmethod
    def offset(x, y, z):
        """
        Returns a matrix that offsets the vertex by a fixed amount.
        """
        return offset_matrix(x, y, z)

    @staticmethod
    cdef Matrix crotate(float x, float y, float z):
        return rotate_matrix(x, y, z)

    @staticmethod
    def rotate(x, y, z):
        """
        Returns a matrix that rotates the displayable around the
        origin.

        `x`, `y`, `x`
            The amount to rotate around the origin, in degrees.
        """
        return rotate_matrix(x, y, z)

    @staticmethod
    cdef Matrix cscale(float x, float y, float z):
        return scale_matrix(x, y, z)

    @staticmethod
    def scale(x, y, z):
        """
        Returns a matrix that scales the displayable.

        `x`, `y`, `z`
            The factor to scale each axis by.
        """
        return scale_matrix(x, y, z)

    @staticmethod
    cdef Matrix cperspective(float w, float h, float n, float p, float f):
        return perspective_matrix(w, h, n, p, f)

    @staticmethod
    def perspective(w, h, n, p, f):
        """
        Returns the Ren'Py projection matrix. This is a view into a 3d space
        where (0, 0) is the top left corner (`w`/2, `h`/2) is the center, and
        (`w`,`h`) is the bottom right, when the z coordinate is 0.

        `w`, `h`
            The width and height of the input plane, in pixels.

        `n`
            The distance of the near plane from the camera.

        `p`
            The distance of the 1:1 plane from the camera. This is where 1 pixel
            is one coordinate unit.

        `f`
            The distance of the far plane from the camera.
        """
        return perspective_matrix(w, h, n, p, f)

    @staticmethod
    cdef Matrix cscreen_projection(float w, float h):
        return screen_projection_matrix(w, h)

    @staticmethod
    def screen_projection(w, h):
        """
        This generates a matrix that projects the Ren'Py space, where (0, 0) is the
        top left and (`w`, `h`) is the bottom right, into the OpenGL viewport, where
        (-1.0, 1.0) is the top left and (1.0, -1.0) is the bottom.

        Generates the matrix that projects the Ren'Py screen to the OpenGL screen.
        """
        return screen_projection_matrix(w, h)

    @staticmethod
    cdef Matrix ctexture_projection(float w, float h):
        return texture_projection_matrix(w, h)

    @staticmethod
    def texture_projection(w, h):
        """
        This generates a matrix that project the Ren'Py space, where (0, 0) is the
        top left and (`w`, `h`) is the bottom right, into the OpenGL render-to-texture
        space, where (-1.0, -1.0) is the top left and (1.0, 1.0) is the bottom.

        Generates the matrix that projects the Ren'Py screen to the OpenGL screen.
        """
        return texture_projection_matrix(w, h)


cdef class Matrix2D(Matrix):

    def __init__(Matrix2D self, double xdx, double xdy, double ydx, double ydy):
        memset(self.m, 0, sizeof(float) * 16)

        self.xdx = xdx
        self.xdy = xdy
        self.ydx = ydx
        self.ydy = ydy

        self.zdz = 1.0
        self.wdw = 1.0

include "matrix_functions.pxi"
