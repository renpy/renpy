from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

from renpy.gl2.gl2polygon cimport Polygon, intersect, barycentric, rectangle


cdef class Mesh:

    def __init__(Mesh self):
        """
        Represents a mesh consisting of one or more polygons.

        This needs to be created in the correct order.

        First, use add_attribute to add attributes. Then call add_polygon
        to add polygons with attributes. After that, it is possible to call
        methods like offset to manipulate the mesh.

        Once get_data is called (by Shader.draw), the mesh becomes immutable.
        """

        self.points = 0
        self.stride = 4
        self.polygons = [ ]
        self.attributes = { "aPosition" : 0 }
        self.data = NULL

    def __dealloc__(Mesh self):
        if self.data:
            free(self.data)

    def add_attribute(Mesh self, name, size):
        """
        Adds an attribute to this mesh.

        `name`
            The name of the attribute.

        `size`
            The number of floats per vertex that make up the attribute.
        """

        self.attributes[name] = self.stride
        self.stride += size

    def add_polygon(Mesh self, data):
        """
        Adds a polygon.

        `data`
            This is an iterable. It should have self.stride data for each
            vertex, and the number of vertices is derived from the length
            of the data.
        """

        cdef Polygon p = Polygon(self.stride, len(data) // self.stride, data)
        self.points += p.points

        self.polygons.append(p)

    def add_texture_rectangle(Mesh self, float w, float h):
        """
        Returns a polygon corresponding to a texture rectangle.
        """

        self.points += 4
        self.polygons.append(rectangle(w, h, 1.0, 1.0))


    cdef float *get_data(Mesh self, name):
        cdef Polygon p
        cdef int i

        if len(self.polygons) == 1:

            p = self.polygons[0]
            return p.data + <int> self.attributes[name]

        if not self.data:
            self.data = <float *> malloc(self.points * self.stride * sizeof(float))

            i = 0

            for p in self.polygons:
                memcpy(&self.data[i], p.data, p.points * self.stride * sizeof(float))
                i += p.points * self.stride

        return self.data + <int> self.attributes[name]

    def copy(Mesh self):
        """
        Returns a copy of this mesh.
        """

        rv = Mesh()
        rv.stride = self.stride
        rv.points = self.points
        rv.polygons = [ i.copy() for i in self.polygons ]
        rv.attributes = self.attributes

        return rv

    def offset(Mesh self, float x, float y, float z):
        """
        Applies an offset to the position of every vertex.
        """

        cdef Polygon p

        for p in self.polygons:
            p.offset(x, y, z)

    def perspective_divide(Mesh self):

        for p in self.polygons:
            p.perspective_divide()

    def multiply_matrix(Mesh self, attribute, int attribute_size, Matrix matrix):
        """
        Multiplies vertex data by a matrix.

        `attribute`
            The offset of the attribute in question.

        `attribute_size`
            The number of elements in the attribute. If the matrix is larger
            than this, other fields are padded with 1s.

        `matrix`
            The matrix to use.
        """

        cdef Polygon p

        cdef int offset = self.attributes[attribute]

        for p in self.polygons:
            p.multiply_matrix(offset, attribute_size, matrix)


    def intersect(Mesh self, Mesh other):
        """
        Intersects this mesh with this one. The resulting mesh has z-coordinates
        from this one. Attributes that are present in this mesh are taken from
        this mesh, otherwise the attributes from the other mesh are used.
        """

        rv = Mesh()
        rv.stride = self.stride + other.stride - 4
        rv.attributes = { k : v + self.stride - 4 for k, v in other.attributes.iteritems() }
        rv.attributes.update(self.attributes)

        cdef Polygon op
        cdef Polygon sp
        cdef Polygon p

        for op in other.polygons:
            for sp in self.polygons:
                p = intersect(op, sp, rv.stride)

                if p is None:
                    continue

                barycentric(op, p, self.stride - 4)
                barycentric(sp, p, 0)

                rv.polygons.append(p)
                rv.points += p.points

        return rv

    def crop(Mesh self, Mesh other):
        """
        Crops this mesh with the other one. No attributes are taken from the other
        mesh.
        """

        rv = Mesh()
        rv.stride = self.stride
        rv.attributes = self.attributes

        cdef Polygon op
        cdef Polygon sp
        cdef Polygon p

        for op in other.polygons:
            for sp in self.polygons:
                p = intersect(op, sp, rv.stride)

                if p is None:
                    continue

                barycentric(sp, p, 0)

                rv.polygons.append(p)
                rv.points += p.points

        return rv

    def print_points(Mesh self, prefix):
        for i, p in enumerate(self.polygons):
            p.print_points(prefix + " " + str(i))

