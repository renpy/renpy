from renpy.gl2.gl2polygon cimport Polygon
from renpy.display.matrix cimport Matrix

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

    cdef float *get_data(self, name)

