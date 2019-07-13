cdef class Matrix:

    cdef float m[0]

    cdef public float xdx
    cdef public float xdy
    cdef public float xdz
    cdef public float xdw

    cdef public float ydx
    cdef public float ydy
    cdef public float ydz
    cdef public float ydw

    cdef public float zdx
    cdef public float zdy
    cdef public float zdz
    cdef public float zdw

    cdef public float wdx
    cdef public float wdy
    cdef public float wdz
    cdef public float wdw


    cdef inline void transform4(Matrix self, float *ox, float *oy, float *oz, float *ow, float x, float y, float z, float w):
        ox[0] = x * self.xdx + y * self.xdy + z * self.xdz + w * self.xdw
        oy[0] = x * self.ydx + y * self.ydy + z * self.ydz + w * self.ydw
        oz[0] = x * self.zdx + y * self.zdy + z * self.zdz + w * self.zdw
        ow[0] = x * self.wdx + y * self.wdy + z * self.wdz + w * self.wdw

    cdef inline void transform3(Matrix self, float *ox, float *oy, float *oz, float x, float y, float z, float w):
        ox[0] = x * self.xdx + y * self.xdy + z * self.xdz + w * self.xdw
        oy[0] = x * self.ydx + y * self.ydy + z * self.ydz + w * self.ydw
        oz[0] = x * self.zdx + y * self.zdy + z * self.zdz + w * self.zdw

    cdef inline void transform2(Matrix self, float *ox, float *oy, float x, float y, float z, float w):
        ox[0] = x * self.xdx + y * self.xdy + z * self.xdz + w * self.xdw
        oy[0] = x * self.ydx + y * self.ydy + z * self.ydz + w * self.ydw

    cpdef bint is_unit_aligned(Matrix self)

cdef class Matrix2D(Matrix):
    pass
