# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

from libc.stdlib cimport malloc, free
from libc.math cimport hypot

from cpython.bytes cimport PyBytes_FromStringAndSize

from renpy.gl2.gl2polygon cimport Polygon, Point2
from renpy.uguu.gl cimport *
from renpy.gl2.gl2statecache cimport SCRATCH_POSITION, SCRATCH_ATTRIBUTE, SCRATCH_INDEX


dead_buffers = []

def drain_dead_buffers(GLStateCache cache):
    cdef GLuint name
    cdef unsigned long long generation

    if not dead_buffers:
        return

    # Deletion may unbind a buffer and its name may immediately be reused.
    cache.bind_array_buffer(0)
    cache.bind_element_buffer(0)

    for name, generation in dead_buffers:
        if generation == cache.buffer_generation:
            glDeleteBuffers(1, &name)

    dead_buffers.clear()


cdef GLuint upload_stream(GLStateCache cache, MeshBuffer* buffer, bint persistent, unsigned int version, int slot, GLenum target, GLsizeiptr size, const void* data) noexcept nogil:
    if buffer.generation != cache.buffer_generation:
        buffer.name = 0
        buffer.generation = cache.buffer_generation

    if not version:
        buffer.version = 0

    if version and (buffer.name or persistent):
        if not buffer.name:
            glGenBuffers(1, &buffer.name)
            buffer.version = 0

        if buffer.name:
            if buffer.version != version or buffer.size != size:
                if target == GL_ELEMENT_ARRAY_BUFFER:
                    cache.bind_element_buffer(buffer.name)
                else:
                    cache.bind_array_buffer(buffer.name)

                glBufferData(target, size, data, GL_DYNAMIC_DRAW)
                buffer.version = version
                buffer.size = size

            return buffer.name

    if cache.core_profile:
        return cache.upload_scratch(slot, target, size, data)

    return 0


cdef class AttributeLayout:

    def __cinit__(self, offset={}, stride=0):
        self.offset = dict(offset)
        self.stride = stride

    def add_attribute(self, name, length):
        self.offset[name] = self.stride
        self.stride += length

    def __reduce__(self):
        return (AttributeLayout, (self.offset, self.stride))


# The layout of a mesh used in a Solid.
SOLID_LAYOUT = AttributeLayout()

# The layout of a mesh used with a texture.
TEXTURE_LAYOUT = AttributeLayout()
TEXTURE_LAYOUT.add_attribute("a_tex_coord", 2) # The texture coordinate.

# The layout of mesh with a normal.
MODEL_N_LAYOUT = AttributeLayout()
MODEL_N_LAYOUT.add_attribute("a_tex_coord", 2) # The texture coordinate.
MODEL_N_LAYOUT.add_attribute("a_normal", 3) # The normal.

# The layout of a mesh used with a texture, normal, tangent, and bitangent.
MODEL_NT_LAYOUT = AttributeLayout()
MODEL_NT_LAYOUT.add_attribute("a_tex_coord", 2) # The texture coordinate.
MODEL_NT_LAYOUT.add_attribute("a_normal", 3) # The normal.
MODEL_NT_LAYOUT.add_attribute("a_tangent", 3) # The tangent.
MODEL_NT_LAYOUT.add_attribute("a_bitangent", 3) # The bitangent.

# The layout of a mesh used with text.
TEXT_LAYOUT = AttributeLayout()
TEXT_LAYOUT.add_attribute("a_tex_coord", 2) # The texture coordinate.
TEXT_LAYOUT.add_attribute("a_text_center", 2) # Position of the vertex center.
TEXT_LAYOUT.add_attribute("a_text_time", 1) # The time this vertex should be shown.
TEXT_LAYOUT.add_attribute("a_text_min_time", 1) # The minimum time any vertex in this glyph should be shown.
TEXT_LAYOUT.add_attribute("a_text_max_time", 1) # The maximum time any vertex in this glyph should be shown.
TEXT_LAYOUT.add_attribute("a_text_index", 1) # The glyph number.
TEXT_LAYOUT.add_attribute("a_text_pos_rect", 4) # The rectangle being drawn.
TEXT_LAYOUT.add_attribute("a_text_ascent", 1) # The ascent of the font.
TEXT_LAYOUT.add_attribute("a_text_descent", 1) # The ascent of the font.
TEXT_LAYOUT.add_attribute("a_text_pseudo_glyph", 1) # 1 if this is a pseudo-glyph, 0 otherwise.

cdef class Mesh:

    def __dealloc__(self):
        cdef int i

        for i in range(3):
            if self.buffers[i].name:
                dead_buffers.append((self.buffers[i].name, self.buffers[i].generation))

    cdef void upload_buffers(Mesh self, GLStateCache cache, GLuint* vbo, GLuint* abo, GLuint* ibo) noexcept nogil:
        cdef bint small_mesh = self.points <= 4 and self.triangles <= 2
        cdef bint persistent = self.draw_seen and (not small_mesh or self.draw_frame != cache.buffer_frame)

        vbo[0] = upload_stream(cache, &self.buffers[SCRATCH_POSITION], persistent,
            self.point_version, SCRATCH_POSITION, GL_ARRAY_BUFFER,
            self.points * self.point_size * sizeof(float), self.point_data)

        abo[0] = 0

        if self.layout.stride:
            abo[0] = upload_stream(cache, &self.buffers[SCRATCH_ATTRIBUTE], persistent,
                self.attribute_version, SCRATCH_ATTRIBUTE, GL_ARRAY_BUFFER,
                self.points * self.layout.stride * sizeof(float), self.attribute)

        ibo[0] = upload_stream(cache, &self.buffers[SCRATCH_INDEX], persistent,
            self.triangle_version, SCRATCH_INDEX, GL_ELEMENT_ARRAY_BUFFER,
            3 * self.triangles * sizeof(unsigned int), self.triangle)

        self.draw_seen = True
        self.draw_frame = cache.buffer_frame

    cdef Mesh get_cropped_mesh(Mesh self, Polygon p):
        if not self.point_version or not self.triangle_version or (self.layout.stride and not self.attribute_version):
            self._crop_key = None
            self._cropped_mesh = None

            return self.crop(p)

        p.ensure_winding()

        cdef tuple key = (
            self.point_version,
            self.attribute_version,
            self.triangle_version,
            self.points,
            self.point_size,
            self.triangles,
            self.layout,
            self.layout.stride,
            PyBytes_FromStringAndSize(<char *> p.point, p.points * sizeof(Point2)),
        )
        cdef Mesh cropped

        if key == self._crop_key:
            return self._cropped_mesh if self._cropped_mesh is not None else self

        self._crop_key = None
        self._cropped_mesh = None

        cropped = self.crop(p)
        
        self._cropped_mesh = cropped if cropped is not self else None
        self._crop_key = key

        return cropped

    def set_geometry_data(self, geometry):
        """
        Sets the geometry data corresponding to this mesh.

        `geometry`
            This should be a sequence of floats, which are interpreted
            as x, y for a Mesh2 or x, y, z for a Mesh3. The length of
            the sequence must be a multiple of the point size of the
            mesh, and must be less than or equal to the number of
            allocated points.

        This sets the `points` attribute of the mesh to the number of
        points in the geometry.
        """

        points = len(geometry) // self.point_size

        if points > self.allocated_points:
            raise Exception("Geometry contains too much data.")

        if points != self.points and self.attribute_version:
            self.attribute_version += 1

        self.points = points
        self.point_version += 1
        cdef int i
        cdef int len_geometry = len(geometry)

        for i in range(len_geometry):
            self.point_data[i] = geometry[i]

    def set_attribute_data(self, attributes):
        """
        Sets the attribute data corresponding to this mesh.

        `attributes`
            This should be a list of floats, with the first
            layout.stride floats corresponding to the first point, the
            next layout.stride floats corresponding to the second point,
            and so on. The length of the sequence must be a multiple of
            the stride of the layout, and must be less than or equal to
            the number of allocated points.
        """

        cdef int i
        cdef int len_attributes = len(attributes)

        if len_attributes > self.allocated_points * self.layout.stride:
            raise Exception("Attributes contains too much data.")

        self.attribute_version += 1

        for i in range(len_attributes):
            self.attribute[i] = attributes[i]

    def set_triangle_data(self, triangles):
        """
        Sets the triangle data corresponding to this mesh.

        `triangles`
            This should be a list of integers, with each triple
            corresponding to a triangle. The length of the sequence
            must be a multiple of 3, and must be less than or equal to
            the number of allocated triangles.

        This sets the `triangles` attribute of the mesh to the number
        of triangles given here.
        """

        cdef int i
        cdef int len_triangles = len(triangles)

        if len_triangles > self.allocated_triangles * 3:
            raise Exception("Triangles contains too much data.")

        self.triangles = len_triangles // 3
        self.triangle_version += 1

        for i in range(len_triangles):
            self.triangle[i] = triangles[i]

    def get_triangles(self):
        """
        Returns the triangles that make up this mesh as triples.
        """

        cdef int i

        rv = [ ]

        for i in range(self.triangles):
            rv.append((
                self.triangle[i * 3 + 0],
                self.triangle[i * 3 + 1],
                self.triangle[i * 3 + 2],
                ))

        return rv
