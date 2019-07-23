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
    cpdef void offset(Polygon self, float x, float y, float z)
    cpdef void multiply_matrix(Polygon self, int offset, int size, Matrix matrix)
    cpdef void perspective_divide(Polygon self)

cpdef Polygon rectangle(double x, double y, double w, double h)
cpdef Polygon texture_rectangle(double x, double y, double w, double h, double tw, double th)

cpdef intersect(Polygon a, Polygon b, int rvstride)
cpdef barycentric(Polygon a, Polygon b, int offset)

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

