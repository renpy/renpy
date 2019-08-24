

def identity():
    """
    Returns an identity matrix.
    """

    cdef Matrix rv = Matrix(None)

    rv.xdx = 1.00000000000000
    rv.ydy = 1.00000000000000
    rv.zdz = 1.00000000000000
    rv.wdw = 1.00000000000000

    return rv


def offset(float x, float y, float z):
    """
    Returns a matrix that offsets the vertex by a fixed amount.
    """

    cdef Matrix rv = Matrix(None)

    rv.xdx = 1.00000000000000
    rv.xdw = x
    rv.ydy = 1.00000000000000
    rv.ydw = y
    rv.zdz = 1.00000000000000
    rv.zdw = z
    rv.wdw = 1.00000000000000

    return rv


def rotate(float x, float y, float z):
    """
    Returns a matrix that rotates the displayable around the
    origin.

    `x`, `y`, `x`
        The amount to rotate around the origin, in degrees.
    """

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


def perspective(float w, float h, float n, float p, float f):
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


def screen_projection(float w, float h):
    """
    This generates a matrix that projects the Ren'Py space, where (0, 0) is the
    top left and (`w`, `h`) is the bottom right, into the OpenGL viewport, where
    (-1.0, 1.0) is the top left and (1.0, -1.0) is the bottom.

    Generates the matrix that projects the Ren'Py screen to the OpenGL screen.
    """

    cdef Matrix rv = Matrix(None)

    rv.xdx = 2/w
    rv.xdw = -1.00000000000000
    rv.ydy = -2/h
    rv.ydw = 1.00000000000000
    rv.zdz = 1.00000000000000
    rv.wdw = 1.00000000000000

    return rv


def texture_projection(float w, float h):
    """
    This generates a matrix that project the Ren'Py space, where (0, 0) is the
    top left and (`w`, `h`) is the bottom right, into the OpenGL render-to-texture
    space, where (-1.0, -1.0) is the top left and (1.0, 1.0) is the bottom.

    Generates the matrix that projects the Ren'Py screen to the OpenGL screen.
    """

    cdef Matrix rv = Matrix(None)

    rv.xdx = 2/w
    rv.xdw = -1.00000000000000
    rv.ydy = 2/h
    rv.ydw = -1.00000000000000
    rv.zdz = 1.00000000000000
    rv.wdw = 1.00000000000000

    return rv
