# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.display.matrix cimport Matrix

import renpy
import random

cdef GLenum TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE


class ShaderError(Exception):
    pass


GLSL_PRECISIONS = {
    "highp",
    "mediump",
    "lowp",
    }


cdef class Uniform:
    cdef GLint location
    cdef bint ready

    def __init__(self, program, location, name):
        self.location = location
        self.ready = False

    cdef void assign(self, Program program, data):
        return

    cdef void finish(self, Program program):
        self.ready = False
        return

cdef class UniformFloat(Uniform):
    cdef void assign(self, Program program, data):
        glUniform1f(self.location, data)

cdef class UniformVec2(Uniform):
    cdef void assign(self, Program program, data):
        glUniform2f(self.location, data[0], data[1])

cdef class UniformVec3(Uniform):
    cdef void assign(self, Program program, data):
        glUniform3f(self.location, data[0], data[1], data[2])

cdef class UniformVec4(Uniform):
    cdef void assign(self, Program program, data):
        glUniform4f(self.location, data[0], data[1], data[2], data[3])

cdef class UniformMat4(Uniform):
    cdef void assign(self, Program program, data):
        glUniformMatrix4fv(self.location, 1, GL_FALSE, (<Matrix> data).m)

cdef class UniformSampler2D(Uniform):
    cdef int sampler
    cdef object last_data
    cdef bint cleanup
    cdef object texture_wrap_key

    def __init__(self, program, location, name):
        Uniform.__init__(self, program, location, name)
        self.sampler = program.samplers
        self.cleanup = False
        self.texture_wrap_key = "texture_wrap_" + name
        program.samplers += 1

    cdef void assign(self, Program program, data):
        cdef dict properties = program.properties
        self.last_data = data
        self.cleanup = False

        glActiveTexture(GL_TEXTURE0 + self.sampler)
        glUniform1i(self.location, self.sampler)

        if isinstance(data, GLTexture):
            glBindTexture(GL_TEXTURE_2D, data.number)
        else:
            glBindTexture(GL_TEXTURE_2D, data)


        if self.texture_wrap_key in properties:
            wrap_s, wrap_t = properties[self.texture_wrap_key]
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
            self.cleanup = True

        elif "texture_wrap" in properties:
            wrap_s, wrap_t = properties["texture_wrap"]
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
            self.cleanup = True

        if "anisotropic" in properties:
            if not properties.get("anisotropic", True) and renpy.display.draw.loader.max_anisotropy > 1.0:
                glTexParameterf(GL_TEXTURE_2D, TEXTURE_MAX_ANISOTROPY_EXT, 1.0)
                self.cleanup = True


    cdef void finish(self, Program program):
        cdef dict properties = program.properties
        self.ready = False

        if self.cleanup:

            self.cleanup = False

            if isinstance(self.last_data, GLTexture):
                glBindTexture(GL_TEXTURE_2D, self.last_data.number)
            else:
                glBindTexture(GL_TEXTURE_2D, self.last_data)

            if "texture_wrap" in properties or self.texture_wrap_key in properties:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            if "anisotropic" in properties:
                if not properties.get("anisotropic", True) and renpy.display.draw.loader.max_anisotropy > 1.0:
                    glTexParameterf(GL_TEXTURE_2D, TEXTURE_MAX_ANISOTROPY_EXT, renpy.display.draw.loader.max_anisotropy)

        self.last_data = None



UNIFORM_TYPES = {
    "float" : UniformFloat,
    "vec2" : UniformVec2,
    "vec3" : UniformVec3,
    "vec4" : UniformVec4,
    "mat4" : UniformMat4,
    "sampler2D" : UniformSampler2D,
    }

cdef class Attribute:
    cdef object name
    cdef GLint location
    cdef GLint size

    def __init__(self, name, GLint location, GLint size):
        self.name = name
        self.location = location
        self.size = size

ATTRIBUTE_TYPES = {
    "float" : 1,
    "vec2" : 2,
    "vec3" : 3,
    "vec4" : 4,
}

TEXTURE_SCALING = {
    "nearest" : (GL_NEAREST, GL_NEAREST),
    "linear" : (GL_LINEAR, GL_LINEAR),
    "nearest_mipmap_nearest" : (GL_NEAREST, GL_NEAREST_MIPMAP_NEAREST),
    "linear_mipmap_nearest" : (GL_LINEAR, GL_LINEAR_MIPMAP_NEAREST),
    "nearest_mipmap_linear" : (GL_NEAREST, GL_NEAREST_MIPMAP_LINEAR),
    "linear_mipmap_linear" : (GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR),
}

cdef class Program:
    """
    Represents an OpenGL program.
    """

    def __init__(self, name, vertex, fragment):
        self.name = name
        self.vertex = vertex
        self.fragment = fragment

        # A map from uniform name to a Uniform object.
        self.uniforms = { }

        # A map from unform name to a value.
        self.uniform_values = { }

        # A list of Attribute objects
        self.attributes = [ ]

        # The number of samplers that have been added.
        self.samplers = 0

    def find_variables(self, source):

        for l in source.split("\n"):

            l = l.strip()
            l = l.rstrip("; ")
            tokens = l.split()

            def advance():
                if not tokens:
                    return None
                else:
                    return tokens.pop(0)

            token = advance()

            if token == "invariant":
                token = advance()

            if token == "uniform":
                storage = "uniform"
                types = UNIFORM_TYPES
            elif token == "attribute":
                storage = "attribute"
                types = ATTRIBUTE_TYPES
            else:
                continue

            token = advance()

            if token in ( "highp", "mediump", "lowp"):
                token = advance()
                continue

            if token not in types:
                raise ShaderError("Unsupported type {} in '{}'. Only float, vec<2-4>, mat<2-4>, and sampler2D are supported.".format(token, l))

            type = token

            name = advance()
            if name is None:
                raise ShaderError("Couldn't finds name in {}".format(l))

            if tokens:
                raise ShaderError("Spurious tokens after the name in '{}'. Arrays are not supported in Ren'Py.".format(l))

            if storage == "uniform":
                location = glGetUniformLocation(self.program, name.encode("utf-8"))

                if location >= 0:
                    self.uniforms[name] = types[type](self, location, name)

            else:
                location = glGetAttribLocation(self.program, name.encode("utf-8"))

                if location >= 0:
                    self.attributes.append(Attribute(name, location, types[type]))

    cdef GLuint load_shader(self, GLenum shader_type, source) except? 0:
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

            renpy.display.log.write("Error compiling shader %s:", self.name)

            for i, l in enumerate(original_source.splitlines()):
                renpy.display.log.write("% 3d %s" % (i+1 , l))

            glGetShaderInfoLog(shader, 1024, NULL, error)
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

        cdef char error[1024]

        vertex = self.load_shader(GL_VERTEX_SHADER, self.vertex)
        fragment = self.load_shader(GL_FRAGMENT_SHADER, self.fragment)

        program = glCreateProgram()
        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)

        glGetProgramiv(program, GL_LINK_STATUS, &status)

        if status == GL_FALSE:
            glGetProgramInfoLog(program, 1024, NULL, error)
            raise ShaderError(repr((<object> error)))

        glDeleteShader(vertex)
        glDeleteShader(fragment)

        self.program = program

        self.find_variables(self.vertex)
        self.find_variables(self.fragment)

    def missing(self, kind, name):
        cdef GLfloat viewport[4]

        if name == "u_lod_bias":
            self.set_uniform("u_lod_bias", float(renpy.config.gl_lod_bias))
        elif name == "u_time":
            self.set_uniform("u_time", (renpy.display.interface.frame_time - renpy.display.interface.init_time) % 86400)
        elif name == "u_random":
            self.set_uniform("u_random", (random.random(), random.random(), random.random(), random.random()))
        elif name == "u_viewport":
            glGetFloatv(GL_VIEWPORT, viewport)
            self.set_uniform("u_viewport", (viewport[0], viewport[1], viewport[2], viewport[3]))
        elif name == "u_drawable_size":
            self.set_uniform("u_drawable_size", renpy.display.draw.drawable_viewport[2:])
        elif name == "u_virtual_size":
            self.set_uniform("u_virtual_size", renpy.display.draw.virtual_size)
        else:
            raise Exception("Shader {} has not been given {} {}.".format(self.name, kind, name))

    def start(self, properties):
        self.properties = properties

        glUseProgram(self.program)


    def set_uniform(self, name, value):
        cdef Uniform u
        u = self.uniforms.get(name, None)
        if u is None:
            return

        if name in self.uniform_values and name in renpy.config.merge_uniforms:
            value = renpy.config.merge_uniforms[name](self.uniform_values[name], value)

        self.uniform_values[name] = value

        u.assign(self, value)
        u.ready = True

    def set_uniforms(self, dict uniforms):
        cdef Uniform u

        for name, value in uniforms.iteritems():

            self.set_uniform(name, value)

    def draw(self, Mesh mesh):

        cdef Attribute a
        cdef Uniform u
        cdef int i
        cdef dict properties

        if not mesh.triangles:
            return

        properties = self.properties

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

        for name, u in self.uniforms.iteritems():
            if not u.ready:
                self.missing("uniform", name)

        if properties:

            if "color_mask" in properties:
                mask_r, mask_g, mask_b, mask_a = properties["color_mask"]
                glColorMask(mask_r, mask_g, mask_b, mask_a)

            if "texture_scaling" in properties:
                magnify, minify = TEXTURE_SCALING[properties["texture_scaling"]]

                for 0 <= i < self.samplers:
                    glActiveTexture(GL_TEXTURE0 + i)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magnify)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minify)

            if "blend_func" in properties:
                rgb_eq, src_rgb, dst_rgb, alpha_eq, src_alpha, dst_alpha = properties["blend_func"]
                glBlendEquationSeparate(rgb_eq, alpha_eq)
                glBlendFuncSeparate(src_rgb, dst_rgb, src_alpha, dst_alpha)

        glDrawElements(GL_TRIANGLES, 3 * mesh.triangles, GL_UNSIGNED_INT, mesh.triangle)

        if properties:

            if "texture_scaling" in properties:
                for 0 <= i < self.samplers:
                    glActiveTexture(GL_TEXTURE0 + i)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)

            if "color_mask" in properties:
                glColorMask(True, True, True, True)

            if "blend_func" in properties:
                glBlendEquation(GL_FUNC_ADD)
                glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

    def finish(Program self):
        cdef Attribute a
        cdef Uniform u

        for a in self.attributes:
            glDisableVertexAttribArray(a.location)

        for u in self.uniforms.itervalues():
            u.finish(self)

        self.properties = None
        self.uniform_values = { }
