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
cpdef Polygon rectangle(double l, double t, double r, double b)
cpdef Polygon texture_rectangle(double pl, double pt, double pr, double pb, double tl, double tt, double tr, double tb)

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

    # The count of polygons that comprise the mesh. This is  only valid after
    # get_data is called.
    cdef public int polygon_count

    # If all the polygons in the mesh have the same number of points, this is
    # that number of points. Else, it's 0.
    cdef public int polygon_points

    cpdef Mesh copy(Mesh self)

    cpdef void offset_inplace(Mesh self, double x, double y, double z)
    cpdef Mesh offset(Mesh self, double x, double y, double z)

    cpdef void multiply_matrix_inplace(Mesh self, Matrix matrix)
    cpdef Mesh multiply_matrix(Mesh self, Matrix matrix)

    cpdef void perspective_divide_inplace(Mesh self)
    cpdef Mesh perspective_divide(Mesh self)

    cpdef Mesh intersect(Mesh self, Mesh other)
    cpdef Mesh crop(Mesh self, Polygon other)

