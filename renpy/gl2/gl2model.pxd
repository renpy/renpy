from renpy.display.matrix cimport Matrix
from renpy.gl2.gl2mesh cimport Mesh

cdef class Model:

    # The width and height.
    cdef public int width
    cdef public int height

    # The mesh giving the geometry of this model.
    cdef public Mesh mesh

    # A matrix transforming screen coordinates toward mesh coordinates.
    cdef public Matrix forward

    # A matrix transforming mesh coordinates towards screen coordinates.
    cdef public Matrix reverse

    # A tuple giving the shaders used with this model.
    cdef public tuple shaders

    # Either a dictionary giving uniforms associated with this model,
    # or None.
    cdef public dict uniforms

    # The cached_texture that comes from this model. (This is
    # a Texture.)
    cdef object cached_texture

    cpdef Model copy(Model self)
    cpdef subsurface(Model self, t)
    cpdef scale(Model self, float factor)
