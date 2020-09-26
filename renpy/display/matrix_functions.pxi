

cpdef Matrix identity_matrix():

    cdef Matrix rv = Matrix(None)

    rv.xdx = 1.00000000000000
    rv.ydy = 1.00000000000000
    rv.zdz = 1.00000000000000
    rv.wdw = 1.00000000000000

    return rv


cpdef Matrix offset_matrix(float x, float y, float z):

    cdef Matrix rv = Matrix(None)

    rv.xdx = 1.00000000000000
    rv.xdw = x
    rv.ydy = 1.00000000000000
    rv.ydw = y
    rv.zdz = 1.00000000000000
    rv.zdw = z
    rv.wdw = 1.00000000000000

    return rv


cpdef Matrix rotate_matrix(float x, float y, float z):

    cdef float sinx = sin(pi*x/180)
    cdef float cosx = cos(pi*x/180)
    cdef float siny = sin(pi*y/180)
    cdef float cosy = cos(pi*y/180)
    cdef float sinz = sin(pi*z/180)
    cdef float cosz = cos(pi*z/180)

    cdef Matrix rv = Matrix(None)

    rv.xdx = cosy*cosz
    rv.xdy = -cosx*sinz + cosz*sinx*siny
    rv.xdz = cosx*cosz*siny + sinx*sinz
    rv.ydx = cosy*sinz
    rv.ydy = cosx*cosz + sinx*siny*sinz
    rv.ydz = cosx*siny*sinz - cosz*sinx
    rv.zdx = -siny
    rv.zdy = cosy*sinx
    rv.zdz = cosx*cosy
    rv.wdw = 1

    return rv


cpdef Matrix scale_matrix(float x, float y, float z):

    cdef Matrix rv = Matrix(None)

    rv.xdx = x
    rv.ydy = y
    rv.zdz = z
    rv.wdw = 1

    return rv


cpdef Matrix perspective_matrix(float w, float h, float n, float p, float f):

    cdef Matrix rv = Matrix(None)

    rv.xdx = p
    rv.xdz = -w/2
    rv.ydy = p
    rv.ydz = -h/2
    rv.zdz = -(f + n)/(f - n)
    rv.zdw = (-2*f*n + p*(f + n))/(f - n)
    rv.wdz = -1.00000000000000
    rv.wdw = p

    return rv


cpdef Matrix screen_projection_matrix(float w, float h):

    cdef Matrix rv = Matrix(None)

    rv.xdx = 2/w
    rv.xdw = -1.00000000000000
    rv.ydy = -2/h
    rv.ydw = 1.00000000000000
    rv.zdz = 1.00000000000000
    rv.wdw = 1.00000000000000

    return rv


cpdef Matrix texture_projection_matrix(float w, float h):

    cdef Matrix rv = Matrix(None)

    rv.xdx = 2/w
    rv.xdw = -1.00000000000000
    rv.ydy = 2/h
    rv.ydw = -1.00000000000000
    rv.zdz = 1.00000000000000
    rv.wdw = 1.00000000000000

    return rv
