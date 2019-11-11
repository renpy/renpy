from renpy.display.render import IDENTITY
from renpy.display.matrix import Matrix
from renpy.gl2.gl2polygon cimport Polygon

cdef class Model:

    def __init__(Model self, size, mesh, shaders, uniforms):
        self.size = size
        self.mesh = mesh
        self.shaders = shaders
        self.uniforms = uniforms
        self.cached_texture = None

        self.forward = IDENTITY
        self.reverse = IDENTITY

    def __repr__(self):
        rv = "<Model {} {} {}".format(self.size, self.shaders, self.uniforms)

        if self.forward is not IDENTITY:
            rv += "\n    forward (to screen): " + repr(self.forward).replace("\n", "\n    ")
            rv += "\n    reverse (to mesh)  : " + repr(self.reverse).replace("\n", "\n    ")

        rv += "\n    " + repr(self.mesh).replace("\n", "\n    ")
        rv += ">"

        return rv

    cpdef Model copy(Model self):
        """
        This creates a copy of the current model.
        """

        cdef Model rv = Model(self.size, self.mesh, self.shaders, self.uniforms)
        rv.forward = self.forward
        rv.reverse = self.reverse

        return rv

    cpdef subsurface(Model self, t):
        cdef float x, y, w, h

        x, y, w, h = t

        cdef Model rv = self.copy()

        rv.size = (int(w), int(h))

        rv.reverse = rv.reverse * Matrix.coffset(-x, -y, 0)
        rv.forward = Matrix.coffset(x, y, 0) * rv.forward

        cdef Polygon p = Polygon.rectangle(0, 0, w, h)
        p.multiply_matrix_inplace(rv.forward)

        rv.mesh = rv.mesh.crop(p)

        return rv


