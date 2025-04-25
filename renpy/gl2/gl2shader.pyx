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

from renpy.uguu.gl cimport *
from libc.stdlib cimport malloc, free

from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2texture cimport GLTexture
from renpy.gl2.gl2draw cimport GL2DrawingContext
from renpy.gl2.gl2model cimport GL2Model
from renpy.gl2.gl2uniform cimport Setter

from renpy.display.matrix cimport Matrix

from renpy.gl2.gl2uniform import generate_uniform_setter

import renpy
import random
import re

cdef GLenum TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE


class ShaderError(Exception):
    pass


GLSL_PRECISIONS = {
    "highp",
    "mediump",
    "lowp",
    }

ATTRIBUTE_TYPES = {
    "float" : 1,
    "vec2" : 2,
    "vec3" : 3,
    "vec4" : 4,
}

UNIFORM_TYPES = {
    "float",
    "vec2",
    "vec3",
    "vec4",
    "int",
    "ivec2",
    "ivec3",
    "ivec4",
    "bool",
    "bvec2",
    "bvec3",
    "bvec4",
    "mat2",
    "mat3",
    "mat4",
    "sampler2D",
}

VARYING_TYPES = set(ATTRIBUTE_TYPES)| set(UNIFORM_TYPES)


cdef class Attribute:
    cdef object name
    cdef GLint location
    cdef GLint size

    def __init__(self, name, GLint location, GLint size):
        self.name = name
        self.location = location
        self.size = size



class Variable:
    """
    Represents a variable parsed from a shader, as part of the parsing process.
    Returns an empty object if the line is not a variable.
    """

    storage: str|None = None
    "The storage class, one of uniform, attribute, or varying, or None if not a variable."

    type: str|None = None
    "The type of the variable, one of float, int, bool, vec<2-4>, ivec<2-4>, bvec<2-4>, mat<2-4>, or sampler2D."

    name: str|None = None
    "The name of the variable."

    array: int|None = None
    "The size of the array, or None if not an array."

    line: str
    "The line of source code that the variable was parsed from, including qualifiers and the trailing semicolon."

    def __init__(self, shader_name, line):

        l = line.strip().rstrip("; ")
        self.line = l

        def match_word():
            nonlocal l
            if m := re.match(r'\s*(\w+)', l):
                l = l[m.end():]
                return m.group(1)
            else:
                return None

        def match_array():
            nonlocal l
            if m := re.match(r'\s*\[\s*(\d+)\s*\]', l):
                l = l[m.end():]
                return int(m.group(1))
            else:
                return None

        token = match_word()

        if token == "invariant":
            token = match_word()

        if token == "uniform":
            self.storage = "uniform"
            types = UNIFORM_TYPES
        elif token == "attribute":
            self.storage = "attribute"
            types = ATTRIBUTE_TYPES
        elif token == "varying":
            self.storage = "varying"
            types = VARYING_TYPES
        else:
            self.storage = None
            return

        token = match_word()

        if token in ( "highp", "mediump", "lowp"):
            token = match_word()

        if token not in types:
            raise ShaderError(f"In {shader_name}, Unsupported type {token} in '{line}'. Only float, int, bool, vec<2-4>, ivec<2-4>, bvec<2-4>, mat<2-4>, and sampler2D are supported.")

        self.type = token

        self.name = match_word()
        if self.name is None:
            raise ShaderError(f"In {shader_name}, couldn't find name in '{line}'.")

        self.array = match_array()

        if l.rstrip():
            raise ShaderError("Spurious tokens after the name in '{}'.".format(line))

    def __hash__(self):
        return hash((self.storage, self.type, self.name, self.array))

    def __eq__(self, other):
        return (self.storage, self.type, self.name, self.array) == (other.storage, other.type, other.name, other.array)


cdef class Program:
    """
    Represents an OpenGL program.
    """

    def __init__(self, name, vertex, fragment):
        self.name = name
        self.vertex = vertex
        self.fragment = fragment

        # A list of Attribute objects
        self.attributes = [ ]

        # A list of gl2uniform.Setter objects that can be called to set
        # the uniforms.
        self.uniform_setters = [ ]

    def find_variables(self, source, seen_uniforms: set, samplers: int):

        shader_name = "+".join(self.name)

        for line in source.split("\n"):

            l = line.strip()
            l = l.rstrip("; ")

            if not l:
                continue

            v = Variable(shader_name, l)

            if v.storage == "uniform":
                location = glGetUniformLocation(self.program, v.name.encode("utf-8"))

                if location >= 0:
                    setter, samplers = generate_uniform_setter(shader_name, location, v.name, v.type, v.array, samplers)
                    self.uniform_setters.append(setter)

            elif v.storage == "attribute":

                location = glGetAttribLocation(self.program, v.name.encode("utf-8"))

                if v.array is None:
                    array = 1
                else:
                    array = v.array

                if location >= 0:
                    self.attributes.append(Attribute(v.name, location, ATTRIBUTE_TYPES[v.type] * array))

        return samplers

    cdef GLuint load_shader(self, GLenum shader_type, source) except 0:
        """
        This loads a shader into the GPU, and returns the number.
        """

        original_source = source

        source = source.encode("utf-8")

        cdef GLuint shader
        cdef GLchar *source_ptr = <char *> source
        cdef GLint length
        cdef GLint status

        cdef char error[1024]

        shader = glCreateShader(shader_type)
        length = len(source)

        glShaderSource(shader, 1, <const GLchar * const *> &source_ptr, &length)
        glCompileShader(shader)

        glGetShaderiv(shader, GL_COMPILE_STATUS, &status)

        if status == GL_FALSE:

            glGetShaderInfoLog(shader, 1024, NULL, error)

            renpy.display.log.write("Error compiling shader %s: %r", self.name, <object> error)

            for i, l in enumerate(original_source.splitlines()):
                renpy.display.log.write("% 3d %s" % (i+1 , l))

            raise ShaderError((<object> error).decode("latin-1"))

        return shader

    def load(self):
        """
        This loads the program into the GPU.
        """

        cdef GLuint fragment
        cdef GLuint vertex
        cdef GLuint program
        cdef GLint status

        cdef char[1024] error

        vertex = self.load_shader(GL_VERTEX_SHADER, self.vertex)
        fragment = self.load_shader(GL_FRAGMENT_SHADER, self.fragment)

        program = glCreateProgram()
        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)

        glGetProgramiv(program, GL_LINK_STATUS, &status)

        if status == GL_FALSE:

            glGetProgramInfoLog(program, 1024, NULL, error)

            renpy.display.log.write("Error linking shader %s: %r", self.name, <object> error)

            renpy.display.log.write("Vertex shader:")
            for i, l in enumerate(self.vertex.splitlines()):
                renpy.display.log.write("% 3d %s" % (i+1 , l))

            renpy.display.log.write("Fragment shader:")

            for i, l in enumerate(self.fragment.splitlines()):
                renpy.display.log.write("% 3d %s" % (i+1 , l))

            raise ShaderError(repr((<object> error)))

        glDeleteShader(vertex)
        glDeleteShader(fragment)

        self.program = program

        # Create self.uniform_setters
        seen_uniforms = set()
        samplers = 0

        self.uniform_setters = [ ]

        samplers = self.find_variables(self.vertex, seen_uniforms, samplers)
        self.find_variables(self.fragment, seen_uniforms, samplers)

    def draw(self, GL2DrawingContext context, GL2Model model, Mesh mesh):

        cdef Attribute a
        cdef int i
        cdef dict properties
        cdef dict attribute_offsets

        glUseProgram(self.program)

        properties = context.properties
        attribute_offsets = mesh.layout.offset

        # Set up the attributes.
        for a in self.attributes:
            if a.name == "a_position":
                glVertexAttribPointer(a.location, mesh.point_size, GL_FLOAT, GL_FALSE, mesh.point_size * sizeof(float), mesh.point_data)
            else:
                try:
                    offset = attribute_offsets[a.name]
                    glVertexAttribPointer(a.location, a.size, GL_FLOAT, GL_FALSE, mesh.layout.stride * sizeof(float), mesh.attribute + <int> offset)
                except KeyError:
                    shader_name = "+".join(self.name)
                    raise ShaderError(f"Shader {shader_name} requires attribute {a.name}, but it is not in the mesh.")

            glEnableVertexAttribArray(a.location)

        cdef Setter setter

        for setter in self.uniform_setters:
            try:
                value = setter.getter.get(context, model)
            except:
                shader_name = "+".join(self.name)
                raise ShaderError(f"Could not get value for uniform {setter.uniform_name} in shader {shader_name}, using {setter.getter!r}")

            try:
                setter.set(context, value)
            except:
                shader_name = "+".join(self.name)
                raise ShaderError(f"Could not set value for uniform {setter.uniform_type} {setter.uniform_name} in shader {shader_name}, value {value!r}")

        if properties:

            if "color_mask" in properties:
                mask_r, mask_g, mask_b, mask_a = properties["color_mask"]
                glColorMask(mask_r, mask_g, mask_b, mask_a)

            if "blend_func" in properties:
                rgb_eq, src_rgb, dst_rgb, alpha_eq, src_alpha, dst_alpha = properties["blend_func"]
                glBlendEquationSeparate(rgb_eq, alpha_eq)
                glBlendFuncSeparate(src_rgb, dst_rgb, src_alpha, dst_alpha)

        glDrawElements(GL_TRIANGLES, 3 * mesh.triangles, GL_UNSIGNED_INT, mesh.triangle)

        if properties:

            if "color_mask" in properties:
                glColorMask(True, True, True, True)

            if "blend_func" in properties:
                glBlendEquation(GL_FUNC_ADD)
                glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        for a in self.attributes:
            glDisableVertexAttribArray(a.location)

    def draw_ftl(self, GLuint texture, Mesh mesh):
        """
        Draws the given texture using mesh, for the ftl alpha premultiply shader.
        """

        cdef Attribute a

        glUseProgram(self.program)

        # Set up the attributes.
        for a in self.attributes:
            if a.name == "a_position":
                glVertexAttribPointer(a.location, mesh.point_size, GL_FLOAT, GL_FALSE, mesh.point_size * sizeof(float), mesh.point_data)
            else:
                offset = mesh.layout.offset.get(a.name, None)
                if offset is None:
                    self.missing("mesh attribute", a.name)

                glVertexAttribPointer(a.location, a.size, GL_FLOAT, GL_FALSE, mesh.layout.stride * sizeof(float), mesh.attribute + <int> offset)

            glEnableVertexAttribArray(a.location)

        # There's only one setter, and it's for tex0.
        cdef Setter setter = self.uniform_setters[0]

        for setter in self.uniform_setters:
            setter.set(None, texture)

        glDrawElements(GL_TRIANGLES, 3 * mesh.triangles, GL_UNSIGNED_INT, mesh.triangle)

        for a in self.attributes:
            glDisableVertexAttribArray(a.location)
