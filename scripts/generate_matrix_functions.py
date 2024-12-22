from __future__ import print_function, unicode_literals
from sympy import symbols, Matrix, pi, cos, sin, simplify
import io

matrix_names = [
    "xdx",
    "xdy",
    "xdz",
    "xdw",

    "ydx",
    "ydy",
    "ydz",
    "ydw",

    "zdx",
    "zdy",
    "zdz",
    "zdw",

    "wdx",
    "wdy",
    "wdz",
    "wdw",
    ]


def prefixed_matrix(prefix):
    """
    Returns a matrix where each entry is of the for prefix___name.
    """

    return Matrix(4, 4, [ symbols(prefix + "___" + i) for i in matrix_names ])

###############################################################################


generators = [ ]


class Generator(object):

    def __init__(self, name, docs):

        self.pyd_f = io.StringIO()
        self.pyx_f = io.StringIO()

        self.f = io.StringIO()

        self.name = name
        self.docs = docs

        generators.append(self)

        self.first_let = True

    def parameters(self, params):

        # PYD.
        print("    @staticmethod", file=self.pyd_f)
        print("    cdef Matrix c{}({})".format(
            self.name,
            ", ".join("float " + i for i in params.split())), file=self.pyd_f)

        # PYX.

        print("    @staticmethod", file=self.pyx_f)
        print("    cdef Matrix c{}({}):".format(
            self.name,
            ", ".join("float " + i for i in params.split())), file=self.pyx_f)
        print("        return {}_matrix({})".format(
            self.name, ", ".join(params.split())), file=self.pyx_f)

        print(file=self.pyx_f)

        print("    @staticmethod", file=self.pyx_f)
        print("    def {}({}):".format(
            self.name,
            ", ".join(params.split())), file=self.pyx_f)

        if self.docs:
            print('        """' + self.docs.replace("\n", "\n    ") + '"""', file=self.pyx_f)

        print("        return {}_matrix({})".format(
            self.name, ", ".join(params.split())), file=self.pyx_f)

        # PXI.

        print(file=self.f)
        print(file=self.f)

        print("cpdef Matrix {}_matrix({}):".format(
            self.name,
            ", ".join("float " + i for i in params.split())), file=self.f)

        if params.split():
            return symbols(params)

    def let(self, name, value):

        if self.first_let:
            print(file=self.f)
            self.first_let = False

        value = simplify(value, rational=True)

        print("    cdef float {} = {}".format(name, str(value)), file=self.f)

        return symbols(name)

    def matrix(self, m):

        print(file=self.f)

        print("    cdef Matrix rv = Matrix(None)", file=self.f)
        print(file=self.f)

        for name, value in zip(matrix_names, m):
            if value == 0.0:
                continue

            print("    rv.{} =".format(name), simplify(value, rational=True), file=self.f)

        print(file=self.f)
        print("    return rv", file=self.f)


def generate(func):
    g = Generator(func.__name__, func.__doc__)
    func(g)
    return func


def write(fn):

    with open(fn, "w") as f:
        for i in generators:
            f.write(i.f.getvalue())

    print("pxd ---------------------------------")

    for i in generators:
        print(i.pyd_f.getvalue())

    print("pyx ---------------------------------")

    for i in generators:
        print(i.pyx_f.getvalue())


@generate
def identity(g):
    """
    Returns an identity matrix.
    """

    g.parameters("")

    g.matrix(Matrix(4, 4, [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
        ]))


@generate
def offset(g):
    """
    Returns a matrix that offsets the vertex by a fixed amount.
    """

    x, y, z = g.parameters("x y z")

    g.matrix(Matrix(4, 4, [
        1.0, 0.0, 0.0, x,
        0.0, 1.0, 0.0, y,
        0.0, 0.0, 1.0, z,
        0.0, 0.0, 0.0, 1.0,
        ]))


@generate
def rotate(g):
    """
    Returns a matrix that rotates the displayable around the
    origin.

    `x`, `y`, `x`
        The amount to rotate around the origin, in degrees.

    The rotations are applied in order:

    * A clockwise rotation by `x` degrees in the Y/Z plane.
    * A clockwise rotation by `y` degrees in the Z/X plane.
    * A clockwise rotation by `z` degrees in the X/Y plane.
    """

    x, y, z = g.parameters("x y z")

    sinx = g.let("sinx", sin(x * pi / 180.0))
    cosx = g.let("cosx", cos(x * pi / 180.0))

    siny = g.let("siny", sin(y * pi / 180.0))
    cosy = g.let("cosy", cos(y * pi / 180.0))

    sinz = g.let("sinz", sin(z * pi / 180.0))
    cosz = g.let("cosz", cos(z * pi / 180.0))

    rx = Matrix(4, 4, [
        1, 0, 0, 0,
        0, cosx, -sinx, 0,
        0, sinx, cosx, 0,
        0, 0, 0, 1 ])

    ry = Matrix(4, 4, [
        cosy, 0, siny, 0,
        0, 1, 0, 0,
        -siny, 0, cosy, 0,
        0, 0, 0, 1])

    rz = Matrix(4, 4, [
        cosz, -sinz, 0, 0,
        sinz, cosz, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1, ])

    g.matrix(rz * ry * rx)


@generate
def scale(g):
    """
    Returns a matrix that scales the displayable.

    `x`, `y`, `z`
        The factor to scale each axis by.
    """

    x, y, z = g.parameters("x y z")

    m = Matrix(4, 4, [
        x, 0, 0, 0,
        0, y, 0, 0,
        0, 0, z, 0,
        0, 0, 0, 1 ])

    g.matrix(m)


@generate
def perspective(g):
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

    w, h, n, p, f = g.parameters('w h n p f')

    offset = Matrix(4, 4, [
        1.0, 0.0, 0.0, -w / 2.0,
        0.0, 1.0, 0.0, -h / 2.0,
        0.0, 0.0, 1.0, -p,
        0.0, 0.0, 0.0, 1.0,
    ])

    projection = Matrix(4, 4, [
        2.0 * p / w, 0.0, 0.0, 0.0,
        0.0, 2.0 * p / h, 0.0, 0.0,
        0.0, 0.0, -(f + n) / (f - n), -2 * f * n / (f - n),
        0.0, 0.0, -1.0, 0.0,
    ])

    reverse_offset = Matrix(4, 4, [
        w / 2.0, 0.0, 0.0, w / 2.0,
        0.0, h / 2.0, 0.0, h / 2.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ])

    g.matrix(reverse_offset * projection * offset)


@generate
def screen_projection(g):
    """
    This generates a matrix that projects the Ren'Py space, where (0, 0) is the
    top left and (`w`, `h`) is the bottom right, into the OpenGL viewport, where
    (-1.0, 1.0) is the top left and (1.0, -1.0) is the bottom.

    Generates the matrix that projects the Ren'Py screen to the OpenGL screen.
    """

    w, h = g.parameters("w h")

    m = Matrix(4, 4, [
        2.0 / w, 0.0, 0.0, -1.0,
        0.0, -2.0 / h, 0.0, 1.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
        ])

    g.matrix(m)


@generate
def texture_projection(g):
    """
    This generates a matrix that project the Ren'Py space, where (0, 0) is the
    top left and (`w`, `h`) is the bottom right, into the OpenGL render-to-texture
    space, where (-1.0, -1.0) is the top left and (1.0, 1.0) is the bottom.

    Generates the matrix that projects the Ren'Py screen to the OpenGL screen.
    """

    w, h = g.parameters("w h")

    m = Matrix(4, 4, [
        2.0 / w, 0.0, 0.0, -1.0,
        0.0, 2.0 / h, 0.0, -1.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
        ])

    g.matrix(m)


if __name__ == "__main__":
    import os

    RENPY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    write(os.path.join(RENPY, "renpy", "display", "matrix_functions.pxi"))
