#cython: profile=False
# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.display.matrix cimport Matrix
from renpy.gl2.gl2texture cimport GLTexture


cdef GLenum TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE


cdef class Setter:
    """
    Subclasses of this class are responsible for setting unforms of a
    given type.
    """

    def __init__(self, uniform_name, uniform_type, GLint location, Getter getter):

        self.uniform_name = uniform_name
        self.uniform_type = uniform_type
        self.location = location
        self.getter = getter

    cdef object set(self, GL2DrawingContext context, value):
        raise NotImplementedError()


cdef class FloatSetter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform1f(self.location, value)


cdef class Vec2Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform2f(self.location, value[0], value[1])


cdef class Vec3Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform3f(self.location, value[0], value[1], value[2])


cdef class Vec4Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform4f(self.location, value[0], value[1], value[2], value[3])


cdef class Mat2Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        cdef Matrix m = value
        cdef GLfloat[4] values = [
            m.xdx, m.ydx,
            m.xdy, m.ydy
            ]

        glUniformMatrix2fv(self.location, 1, GL_FALSE, values)


cdef class Mat3Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        cdef Matrix m = value
        cdef GLfloat[9] values = [
            m.xdx, m.ydx, m.zdx,
            m.xdy, m.ydy, m.zdy,
            m.xdz, m.ydz, m.zdz
            ]

        glUniformMatrix3fv(self.location, 1, GL_FALSE, values)


cdef class Mat4Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniformMatrix4fv(self.location, 1, GL_FALSE, (<Matrix> value).m)


cdef class Sampler2DSetter(Setter):

    cdef int sampler
    "The sampler number to use."

    cdef str texture_wrap_key
    "The key to use to look up the texture wrap mode."

    def __init__(self, uniform_name, uniform_type, GLint location, Getter getter, int sampler):
        Setter.__init__(self, uniform_name, uniform_type, location, getter)
        self.sampler = sampler
        self.texture_wrap_key = "texture_wrap_" + uniform_name

    cdef object set(self, GL2DrawingContext context, value):

        glActiveTexture(GL_TEXTURE0 + self.sampler)
        glUniform1i(self.location, self.sampler)

        # Int case.
        if type(value) is int:
            glBindTexture(GL_TEXTURE_2D, value)
            return

        # GLTexture case.
        cdef GLTexture texture = value

        glBindTexture(GL_TEXTURE_2D, texture.number)

        cdef GLint wrap_s = GL_CLAMP_TO_EDGE
        cdef GLint wrap_t = GL_CLAMP_TO_EDGE
        cdef GLfloat anisotropy = self.loader.max_anisotropy

        if context.properties:
            if self.texture_wrap_key in context.properties:
                wrap_s, wrap_t = context.properties[self.texture_wrap_key]
            elif "texture_wrap" in context.properties:
                wrap_s, wrap_t = context.properties["texture_wrap"]

            if not context.properties.get("anisotropic", True):
                anisotropy = 1.0

        if wrap_s != texture.wrap_s:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
            texture.wrap_s = wrap_s

        if wrap_t != texture.wrap_t:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
            texture.wrap_t = wrap_t

        if anisotropy != texture.anisotropy and texture.loader.max_anisotropy > 1.0:
            glTexParameterf(GL_TEXTURE_2D, TEXTURE_MAX_ANISOTROPY_EXT, anisotropy)
            texture.anisotropy = anisotropy


cdef class Getter:
    """
    Subclasses of this class are responsible for setting unforms of a
    given type.
    """

    def __init__(self, uniform_name):
        self.uniform_name = uniform_name

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        raise NotImplementedError()
