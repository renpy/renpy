from renpy.display.matrix cimport Matrix
from renpy.gl2.gl2mesh cimport Mesh

cdef class Model:

    # The size of this model's bounding box, in virtual pixels.
    cdef tuple size

    # The mesh giving the geometry of this model.
    cdef Mesh mesh

    # A matrix transforming screen coordinates toward mesh coordinates.
    cdef Matrix forward

    # A matrix transforming mesh coordinates towards screen coordinates.
    cdef Matrix reverse

    # A tuple giving the shaders used with this model.
    cdef tuple shaders

    # Either a dictionary giving uniforms associated with this model,
    # or None.
    cdef dict uniforms

    # The cached_texture that comes from this model. (This is
    # a Texture.)
    cdef object cached_texture


    cpdef Model copy(Model self)
    cpdef subsurface(Model self, t)
