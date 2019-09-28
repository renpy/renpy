from __future__ import print_function

from libc.string cimport memset
from libc.math cimport sin, cos, M_PI as pi

cdef float *aligned_1 = [ 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ]
cdef float *aligned_2 = [ 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ]

fields = [
    "xdx", "xdy", "xdz", "xdw",
    "ydx", "ydy", "ydz", "ydw",
    "zdx", "zdy", "zdz", "zdw",
    "wdx", "wdy", "wdz", "wdw",
    ]


cdef class Matrix:
    """
    Represents a 4x4 matrix.
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
                rv += "{:8.5f}, ".format(self.m[x + y * 4])

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
