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

cpdef Polygon rectangle(float w, float h, float tw, float th)

cpdef intersect(Polygon a, Polygon b, int rvstride)
cpdef barycentric(Polygon a, Polygon b, int offset)
