from renpy.display.matrix cimport Matrix
from renpy.gl2.gl2mesh cimport Mesh

cdef class GL2Model:

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

    # Either a dictionary giving properties associated with this model,
    # or None.
    cdef public dict properties

    # The cached_texture that comes from this model. (This is
    # a Texture.)
    cdef public object cached_texture

    cpdef GL2Model copy(GL2Model self)
    cpdef subsurface(GL2Model self, t)
    cpdef scale(GL2Model self, float factor)
