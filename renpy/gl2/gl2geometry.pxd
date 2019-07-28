from renpy.display.matrix cimport Matrix

cdef class Polygon:

    # The number of points in the polygon.
    cdef int points

    # The stride of the polygon - the number of floats comprising a data
    # point.
    cdef int stride

    # The data in a polygon.
    cdef float *data

    cpdef Polygon copy(Polygon self)

    cpdef void offset_inplace(Polygon self, double x, double y, double z)
    cpdef Polygon offset(Polygon self, double x, double y, double z)

    cpdef void multiply_matrix_inplace(Polygon self, Matrix matrix)
    cpdef Polygon multiply_matrix(Polygon self, Matrix matrix)

    cpdef void perspective_divide_inplace(Polygon self)
    cpdef Polygon perspective_divide(Polygon self)

    cpdef Polygon intersect(Polygon self, Polygon other)

# Constructors for particularly useful polygons.
cpdef Polygon rectangle(double x, double y, double w, double h)
cpdef Polygon texture_rectangle(double x, double y, double w, double h, double tw, double th)


cdef class Mesh:

    # The total number of points.
    cdef public int points

    # The stride - the amount of data per point, in floats.
    cdef public int stride

    # A map from an attribute to the offset of that attribute.
    cdef public dict attributes

    # A list of polygons that comprise the mesh.
    cdef public list polygons

    # An array that contains all the data from the points. This is NULL
    # until it's created.
    cdef float *data

    cdef float *get_data(self, int offset)

    cpdef Mesh copy(Mesh self)

    cpdef void offset_inplace(Mesh self, double x, double y, double z)
    cpdef Mesh offset(Mesh self, double x, double y, double z)

    cpdef void multiply_matrix_inplace(Mesh self, Matrix matrix)
    cpdef Mesh multiply_matrix(Mesh self, Matrix matrix)

    cpdef void perspective_divide_inplace(Mesh self)
    cpdef Mesh perspective_divide(Mesh self)

    cpdef Mesh intersect(Mesh self, Mesh other)
    cpdef Mesh crop(Mesh self, Polygon other)

