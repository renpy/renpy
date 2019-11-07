from renpy.display.render import IDENTITY

cdef class Model:

    def __init__(Model self, size, mesh, shaders, uniforms):
        self.size = size
        self.mesh = mesh
        self.shaders = shaders
        self.uniforms = uniforms
        self.cached_texture = None

        self.forward = IDENTITY
        self.reverse = IDENTITY


    cpdef Model copy(Model self):
        cdef Model rv = Model(self.size, self.mesh, self.shaders, self.uniforms)
        rv.forward = self.forward
        rv.reverse = self.reverse

        return rv

