from renpy.display.render import IDENTITY
from renpy.display.matrix import Matrix
from renpy.gl2.gl2polygon cimport Polygon
from renpy.gl2.gl2texture cimport GLTexture

from libc.math cimport ceil

cdef class Model:
    """
    A model can be placed as a leaf of the tree of Renders, and contains
    everything needed to be draw to the screen.
    """

    def __init__(Model self, size, mesh, shaders, uniforms):
        self.width = size[0]
        self.height = size[1]
        self.mesh = mesh
        self.shaders = shaders
        self.uniforms = uniforms
        self.cached_texture = None

        self.forward = IDENTITY
        self.reverse = IDENTITY

    def __repr__(self):
        rv = "<Model {}x{} {} {}".format(self.width, self.height, self.shaders, self.uniforms)

        if self.forward is not IDENTITY:
            rv += "\n    forward (to mesh):\n    " + repr(self.forward).replace("\n", "\n    ")
            rv += "\n    reverse (to screen):\n    " + repr(self.reverse).replace("\n", "\n    ")

        rv += "\n    " + repr(self.mesh).replace("\n", "\n    ")
        rv += ">"

        return rv

    def load(self):
        """
        Loads the textures associated with this model.
        """

        for i in self.uniforms.itervalues():
            if isinstance(i, GLTexture):
                i.load_gltexture()

    def program_uniforms(self, shader):
        """
        Called by the rest of the drawing code to set up the textures associated
        with this model.
        """

        shader.set_uniforms(self.uniforms)

    def get_size(self):
        """
        Returns the size of this Model.
        """

        return (self.width, self.height)

    cpdef Model copy(Model self):
        """
        Creates an identical copy of the current model.
        """

        cdef Model rv = Model((self.width, self.height), self.mesh, self.shaders, self.uniforms)
        rv.forward = self.forward
        rv.reverse = self.reverse

        return rv

    cpdef subsurface(Model self, rect):
        """
        Given a rectangle `rect`, returns a Model that only contains the
        portion of the model inside the rectangle.
        """

        cdef float x, y, w, h

        x, y, w, h = rect

        cdef Model rv = self.copy()

        rv.width = <int> ceil(w)
        rv.height = <int> ceil(h)

        rv.reverse = rv.reverse * Matrix.coffset(-x, -y, 0)
        rv.forward = Matrix.coffset(x, y, 0) * rv.forward

        cdef Polygon p = Polygon.rectangle(0, 0, w, h)
        p.multiply_matrix_inplace(rv.forward)

        rv.mesh = rv.mesh.crop(p)

        return rv

    cpdef scale(Model self, float factor):
        """
        Creates a new model that is this model scaled by a constant factor.
        """

        cdef float reciprocal_factor

        cdef Model rv = self.copy()

        rv.width = <int> ceil(rv.width * factor)
        rv.height = <int> ceil(rv.height * factor)

        rv.reverse = rv.reverse * Matrix.scale(factor, factor, factor)

        if factor <= 0.0:
            # Map everything onto the (0, 0, 0) point for the zero-
            # scale case.
            rv.forward =  Matrix.cscale(0, 0, 0) * rv.forward
        else:
            reciprocal_factor = 1.0 / factor
            rv.forward = Matrix.cscale(reciprocal_factor, reciprocal_factor, reciprocal_factor) * rv.forward

        return rv

