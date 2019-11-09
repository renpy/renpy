from renpy.gl2.gl2polygon cimport Polygon

# Represents a point in three dimensional space.
cdef struct Point3:
    float x
    float y
    float z

cdef class AttributeLayout:
    """
    This represents the layout of attributes inside a mesh.
    """

    # A map from a string giving the name of the attribute to the
    # offset of the attribute.
    cdef dict offset

    # The number of floats that make up the attributes for a single
    # point.
    cdef int stride

cdef class Mesh:
    """
    This represents the polygon and vertex data that is stored within
    a Model.
    """

    # The number of points that space has been allocated for.
    cdef int allocated_points

    # The number of points that are in use.
    cdef int points

    # The geometry of the points.
    cdef Point3 *point

    # An AttributeLayout object controlling how attributes are stored.
    cdef AttributeLayout layout

    # The non-geometry attribute data. This is allocated_points * attribute_per_point in size.
    cdef float *attribute

    # The number of triangles that spaces has been allocated for.,
    cdef int allocated_triangles

    # The number of triangles that are in use.
    cdef int triangles

    # The triangle data, where each triangle consists of the index of three
    # points. This is 3 * allocated_triangles in size.
    cdef int *triangle

    cpdef Mesh copy(Mesh self)
    cpdef Mesh crop(Mesh self, Polygon p)
    cpdef Mesh crop_to_rectangle(Mesh m, float l, float b, float r, float t)
