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
from renpy.display.render cimport Render

from cpython.mem cimport PyMem_Malloc, PyMem_Free

import random

import renpy

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


cdef class IntSetter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform1i(self.location, value)


cdef class IVec2Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):

        glUniform2i(self.location, value[0], value[1])

cdef class IVec3Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform3i(self.location, value[0], value[1], value[2])


cdef class IVec4Setter(Setter):
    cdef object set(self, GL2DrawingContext context, value):
        glUniform4i(self.location, value[0], value[1], value[2], value[3])


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

NON_ARRAY_SETTERS = {
    "float" : FloatSetter,
    "vec2" : Vec2Setter,
    "vec3" : Vec3Setter,
    "vec4" : Vec4Setter,

    "int" : IntSetter,
    "ivec2" : IVec2Setter,
    "ivec3" : IVec3Setter,
    "ivec4" : IVec4Setter,

    "bool": IntSetter,
    "bvec2": IVec2Setter,
    "bvec3": IVec3Setter,
    "bvec4": IVec4Setter,

    "mat2" : Mat2Setter,
    "mat3" : Mat3Setter,
    "mat4" : Mat4Setter,
}

cdef GLfloat *to_float_array(l, int length) except NULL:
    """
    Converts a list of floats or tuples containing floats to an array of GLFloats.

    `length`
        The number of floats required.
    """

    cdef int index = 0

    cdef GLfloat *rv = <GLfloat *> PyMem_Malloc(length * sizeof(GLfloat))

    for i in l:
        if type(i) is tuple:
            for j in i:
                if index < length:
                    rv[index] = <GLfloat> <float> j
                index += 1
        else:
            if index < length:
                rv[index] = <GLfloat> <float> i
            index += 1

    if index != length:
        PyMem_Free(rv)
        raise Exception(f"Expected {length} floats, got {index}.")

    return rv


cdef GLint *to_int_array(l, int length) except NULL:
    """
    Converts a list of ints or tuples containing ints to an array of GLints.

    `length`
        The number of ints required.
    """

    cdef int index = 0

    cdef GLint *rv = <GLint *> PyMem_Malloc(length * sizeof(GLint))

    for i in l:
        if type(i) is tuple:
            for j in i:
                if index < length:
                    rv[index] = <GLint> <int> j
                index += 1
        else:
            if index < length:
                rv[index] = <GLint> <int> i
            index += 1

    if index != length:
        PyMem_Free(rv)
        raise Exception(f"Expected {length} ints, got {index}.")

    return rv


cdef class ArraySetter(Setter):

    cdef int length
    "The number of elements in the array."

    def __init__(self, uniform_name, uniform_type, GLint location, Getter getter, int length):

        Setter.__init__(self, uniform_name, uniform_type, location, getter)
        self.length = length


cdef class FloatArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLfloat *values = to_float_array(value, self.length)
        glUniform1fv(self.location, self.length, values)
        PyMem_Free(values)


cdef class Vec2ArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLfloat *values = to_float_array(value, self.length * 2)
        glUniform2fv(self.location, self.length, values)
        PyMem_Free(values)


cdef class Vec3ArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLfloat *values = to_float_array(value, self.length * 3)
        glUniform3fv(self.location, self.length, values)
        PyMem_Free(values)


cdef class Vec4ArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLfloat *values = to_float_array(value, self.length * 4)
        glUniform4fv(self.location, self.length, values)
        PyMem_Free(values)


cdef class IntArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLint *values = to_int_array(value, self.length)
        glUniform1iv(self.location, self.length, values)
        PyMem_Free(values)


cdef class IVec2ArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLint *values = to_int_array(value, self.length * 2)
        glUniform2iv(self.location, self.length, values)
        PyMem_Free(values)


cdef class IVec3ArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLint *values = to_int_array(value, self.length * 3)
        glUniform3iv(self.location, self.length, values)
        PyMem_Free(values)


cdef class IVec4ArraySetter(ArraySetter):

    cdef object set(self, GL2DrawingContext context, value):
        cdef GLint *values = to_int_array(value, self.length * 4)
        glUniform4iv(self.location, self.length, values)
        PyMem_Free(values)

ARRAY_SETTERS = {
    "float" : FloatArraySetter,
    "vec2" : Vec2ArraySetter,
    "vec3" : Vec3ArraySetter,
    "vec4" : Vec4ArraySetter,

    "int" : IntArraySetter,
    "ivec2" : IVec2ArraySetter,
    "ivec3" : IVec3ArraySetter,
    "ivec4" : IVec4ArraySetter,

    "bool": IntArraySetter,
    "bvec2": IVec2ArraySetter,
    "bvec3": IVec3ArraySetter,
    "bvec4": IVec4ArraySetter,
}




TEXTURE_SCALING = {
    "nearest" : (GL_NEAREST, GL_NEAREST),
    "linear" : (GL_LINEAR, GL_LINEAR),
    "nearest_mipmap_nearest" : (GL_NEAREST, GL_NEAREST_MIPMAP_NEAREST),
    "linear_mipmap_nearest" : (GL_LINEAR, GL_LINEAR_MIPMAP_NEAREST),
    "nearest_mipmap_linear" : (GL_NEAREST, GL_NEAREST_MIPMAP_LINEAR),
    "linear_mipmap_linear" : (GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR),
}


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

        # None case.
        if value is None:
            raise Exception(f"Uniform {self.uniform_name} in shader {context.shader_name} given None.")

        # Int case.
        if type(value) is int:
            glBindTexture(GL_TEXTURE_2D, value)
            return

        if type(value) is Render:
            value = value.cached_texture

        # GLTexture case.
        cdef GLTexture texture = value

        glBindTexture(GL_TEXTURE_2D, texture.number)

        cdef GLint wrap_s = GL_CLAMP_TO_EDGE
        cdef GLint wrap_t = GL_CLAMP_TO_EDGE
        cdef GLfloat anisotropy = texture.loader.max_anisotropy
        cdef GLint mag_filter = texture.default_mag_filter
        cdef GLint min_filter = texture.default_min_filter

        if context.properties:
            if self.texture_wrap_key in context.properties:
                wrap_s, wrap_t = context.properties[self.texture_wrap_key]
            elif "texture_wrap" in context.properties:
                wrap_s, wrap_t = context.properties["texture_wrap"]

            if not context.properties.get("anisotropic", True):
                anisotropy = 1.0

            if "texture_scaling" in context.properties:
                mag_filter, min_filter = TEXTURE_SCALING[context.properties["texture_scaling"]]

        if wrap_s != texture.wrap_s:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
            texture.wrap_s = wrap_s

        if wrap_t != texture.wrap_t:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
            texture.wrap_t = wrap_t

        if anisotropy != texture.anisotropy and texture.loader.max_anisotropy > 1.0:
            glTexParameterf(GL_TEXTURE_2D, TEXTURE_MAX_ANISOTROPY_EXT, anisotropy)
            texture.anisotropy = anisotropy

        if mag_filter != texture.mag_filter:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, mag_filter)
            texture.mag_filter = mag_filter

        if min_filter != texture.min_filter:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_filter)
            texture.min_filter = min_filter


cdef class Getter:
    """
    Subclasses of this class are responsible for setting unforms of a
    given type.
    """

    def __init__(self, uniform_name):
        self.uniform_name = uniform_name

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        raise NotImplementedError()


cdef class ContextGetter(Getter):

    def __repr__(self):
        return f"ContextGetter({self.uniform_name})"

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return context.uniforms[self.uniform_name]


cdef class ProjectionGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return context.projection_matrix


cdef class ViewGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return context.view_matrix


cdef class ModelGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return context.model_matrix


cdef class ProjectionViewGetter(Getter):
    cdef Matrix matrix

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return context.projectionview_matrix


cdef class TransformMatrixGetter(Getter):
    cdef Matrix matrix

    def __init__(self, uniform_name):
        Getter.__init__(self, uniform_name)
        self.matrix = Matrix(None)

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        self.matrix.ctake(context.projectionview_matrix)
        self.matrix.inplace_multiply(context.model_matrix)
        return self.matrix


cdef class ModelSizeGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return (model.width, model.height)


cdef class LODBiasGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return float(renpy.config.gl_lod_bias)


cdef class TimeGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return (renpy.display.interface.frame_time - renpy.display.interface.init_time) % 86400


cdef class RandomGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return (random.random(), random.random(), random.random(), random.random())


cdef class ViewportGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        cdef GLfloat[4] viewport
        glGetFloatv(GL_VIEWPORT, viewport)
        return viewport


cdef class DrawableSizeGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return renpy.display.draw.drawable_viewport[2:]


cdef class VirtualSizeGetter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return renpy.display.draw.virtual_size



cdef class InverseGetter(Getter):

    cdef Getter getter
    cdef Matrix matrix

    def __init__(self, uniform_name, getter):
        Getter.__init__(self, uniform_name)
        self.getter = getter
        self.matrix = Matrix(None)

    def __repr__(self):
        return f"InverseGetter({self.getter!r})"

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        value = self.getter.get(context, model)

        if type(value) is Matrix:
            self.matrix.ctake(value)
            self.matrix.inplace_inverse()
            return self.matrix
        else:
            raise TypeError("InverseGetter only works with Matrix values.")


cdef class TransposeGetter(Getter):

    cdef Getter getter
    cdef Matrix matrix

    def __init__(self, uniform_name, getter):
        Getter.__init__(self, uniform_name)
        self.getter = getter
        self.matrix = Matrix(None)

    def __repr__(self):
        return f"TransposeGetter({self.getter!r})"

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        value = self.getter.get(context, model)

        if type(value) is Matrix:
            self.matrix.ctake(value)
            self.matrix.inplace_transpose()
            return self.matrix
        else:
            raise TypeError("TransposeGetter only works with Matrix values.")


cdef class InverseTransposeGetter(Getter):

    cdef Getter getter
    cdef Matrix matrix

    def __init__(self, uniform_name, getter):
        Getter.__init__(self, uniform_name)
        self.getter = getter
        self.matrix = Matrix(None)

    def __repr__(self):
        return f"InverseTransposeGetter({self.getter!r})"

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        value = self.getter.get(context, model)

        if type(value) is Matrix:
            self.matrix.ctake(value)
            self.matrix.inplace_inverse()
            self.matrix.inplace_transpose()
            return self.matrix
        else:
            raise TypeError("InverseTransposeGetter only works with Matrix values.")

cdef class Tex0Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return model.get_texture(0)

cdef class Tex1Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return model.get_texture(1)

cdef class Tex2Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return model.get_texture(2)

cdef class Tex3Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        return model.get_texture(3)

cdef class Res0Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        tex = model.get_texture(0)
        return (tex.texture_width, tex.texture_height)

cdef class Res1Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        tex = model.get_texture(1)
        return (tex.texture_width, tex.texture_height)

cdef class Res2Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        tex = model.get_texture(2)
        return (tex.texture_width, tex.texture_height)

cdef class Res3Getter(Getter):
    cdef object get(self, GL2DrawingContext context, GL2Model model):
        tex = model.get_texture(3)
        return (tex.texture_width, tex.texture_height)

cdef class ResGetter(Getter):
    def __init__(self, uniform_name, getter):
        Getter.__init__(self, uniform_name)
        self.getter = getter

    cdef object get(self, GL2DrawingContext context, GL2Model model):
        value = self.getter.get(context, model)

        if type(value) is Render:
            value = value.cached_texture

        if type(value) is GLTexture:
            return (value.texture_width, value.texture_height)
        else:
            raise TypeError("ResGetter only works with GLTexture values.")

# The classes that are used to get the values of uniforms.
UNIFORM_GETTER_CLASSES = {
    "u_projection": (ProjectionGetter, "mat4"),
    "u_view": (ViewGetter, "mat4"),
    "u_model": (ModelGetter, "mat4"),
    "u_projectionview": (ProjectionViewGetter, "mat4"),
    "u_transform": (TransformMatrixGetter, "mat4"),
    "u_model_size": (ModelSizeGetter, "vec2"),
    "u_lod_bias": (LODBiasGetter, "float"),
    "u_time": (TimeGetter, "float"),
    "u_random": (RandomGetter, "vec4"),
    "u_viewport": (ViewportGetter, "vec2"),
    "u_drawable_size": (DrawableSizeGetter, "vec2"),
    "u_virtual_size": (VirtualSizeGetter, "vec2"),
    "tex0" : (Tex0Getter, "sampler2D"),
    "tex1" : (Tex1Getter, "sampler2D"),
    "tex2" : (Tex2Getter, "sampler2D"),
    "tex3" : (Tex3Getter, "sampler2D"),
    "res0" : (Res0Getter, "vec2"),
    "res1" : (Res1Getter, "vec2"),
    "res2" : (Res2Getter, "vec2"),
    "res3" : (Res3Getter, "vec2"),
}


def generate_uniform_setter(shader_name: str, location: int, uniform_name: str, uniform_type: str, array: int|None, sampler: int):
    """
    Given the information about a uniform, generates an object that will get the
    information for the uniform, and set it.

    `shader_name`
        The name of the shader that this uniform is associated with. Used to
        report errors.

    `location`
        The location of the uniform. This should not be -1, as that indicates
        that the uniform is not used in the shader.

    `uniform_name`
        The name of the uniform.

    `uniform_type`
        The type of the uniform.

    `sampler`
        The sampler number to allocate next.

    Returns a (setter, sampler) tuple, where setter is a Setter object with its getter
    field set, and sampler is the sampler number to use for the next sampler.
    """

    if "__" in uniform_name:
        base_name, _, operation = uniform_name.rpartition("__")
    else:
        base_name = uniform_name
        operation = None

    if base_name in UNIFORM_GETTER_CLASSES:
        getter_class, require_type = UNIFORM_GETTER_CLASSES[base_name]
        getter = getter_class(uniform_name)
    else:
        getter = ContextGetter(uniform_name)
        require_type = None

    if require_type is not None and uniform_type != require_type:
        raise TypeError(
            f"Uniform {uniform_name} in shader {shader_name} has type {uniform_type}, "
            f"but requires type {require_type}."
        )

    if operation is None:
        pass
    elif operation == "inverse":
        getter = InverseGetter(uniform_name, getter)
        uniform_type = "mat4"
    elif operation == "transpose":
        getter = TransposeGetter(uniform_name, getter)
        uniform_type = "mat4"
    elif operation == "inverse_transpose":
        getter = InverseTransposeGetter(uniform_name, getter)
        uniform_type = "mat4"
    elif operation == "res":
        getter = ResGetter(uniform_name, getter)
        uniform_type = "vec2"
    else:
        raise TypeError(
            f"Uniform {uniform_name} in shader {shader_name} has unknown operation "
            f"{operation}."
        )

    if uniform_type == "sampler2D":
        setter = Sampler2DSetter(uniform_name, uniform_type, location, getter, sampler)
        sampler += 1
    elif (array is None) and (setter_class := NON_ARRAY_SETTERS.get(uniform_type, None)):
        setter = setter_class(uniform_name, uniform_type, location, getter)
    elif setter_class := ARRAY_SETTERS.get(uniform_type, None):
        setter = setter_class(uniform_name, uniform_type, location, getter, array)

    else:
        raise TypeError(
            f"Uniform {uniform_name} in shader {shader_name} has unknown type "
            f"{uniform_type}."
        )

    return setter, sampler
