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

from renpy.uguu.gl cimport *
from libc.stdlib cimport malloc, free

from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2texture cimport GLTexture
from renpy.gl2.gl2draw cimport GL2DrawingContext
from renpy.gl2.gl2model cimport GL2Model
from renpy.gl2.gl2uniform cimport Setter, Sampler2DSetter
from renpy.gl2.gl2statecache cimport GLStateCache, SCRATCH_POSITION, SCRATCH_ATTRIBUTE, SCRATCH_INDEX

from renpy.display.matrix cimport Matrix

from renpy.gl2.gl2uniform import generate_uniform_setter
from renpy.gl2.gl2shadercache import FLAT_TYPES, FRAGMENT_OUTPUT

import renpy
import copy
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

# Precision qualifiers ordered from weakest to strongest.
GLSL_PRECISION_RANK = [ None, "lowp", "mediump", "highp" ]

GLSL_INTERPOLATIONS = {
    "flat",
    "smooth",
    "noperspective",
    }

# As above. A conflict resolves to flat, as that's the only qualifier that
# changes what the shader is allowed to do.
GLSL_INTERPOLATION_RANK = [ None, "smooth", "noperspective", "flat" ]

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

    Accepts two dialects for the storage class. The legacy dialect (GLSL ES 1.00)
    spells these uniform, attribute, and varying, while the modern dialect
    (GLSL ES 3.00) spells them uniform, in, and out. Both are normalized to the
    legacy names, so that the two dialects can be freely mixed within a single shader.
    """

    storage: str|None = None
    "The storage class, one of uniform, attribute, or varying, or None if not a variable."

    type: str|None = None
    "The type of the variable, one of float, int, bool, vec<2-4>, ivec<2-4>, bvec<2-4>, mat<2-4>, or sampler2D."

    name: str|None = None
    "The name of the variable."

    shader_name: str
    "The shader part that declared this variable."

    array: int|None = None
    "The size of the array, or None if not an array."

    line: str
    "The line of source code that the variable was parsed from, including qualifiers and the trailing semicolon."

    precision: str|None = None
    "The precision qualifier (highp, mediump, or lowp). None if not given."

    invariant: bool = False
    "True if the variable was declared invariant."

    interpolation: str|None = None
    "The interpolation qualifier (flat, smooth, or noperspective). None if not given."

    interpolation_warnings: set
    "Unsupported interpolation modes already reported for this variable."

    def __init__(self, shader_name, line, fragment=False):

        l = line.strip().rstrip("; ")
        self.line = l
        self.shader_name = shader_name
        self.interpolation_warnings = set()

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

        if token == "layout":
            if m := re.match(r'\s*\([^)]*\)', l):
                l = l[m.end():]

            if match_word() == "out":
                raise ShaderError(
                    f"In {shader_name}, '{line.strip()}' declares an additional fragment output. This "
                    "syntax is reserved for multiple render targets. Location 0 is Ren'Py's "
                    f"{renpy.gl2.gl2shadercache.FRAGMENT_OUTPUT}; outputs declared by a shader part will "
                    "start at 1."
                )

            raise ShaderError(
                f"In {shader_name}, layout qualifiers are not supported, in '{line.strip()}'. "
                f"Declare the variable without one."
            )

        while True:
            if token == "invariant":
                self.invariant = True
            elif token in GLSL_INTERPOLATIONS:
                self.interpolation = token
            else:
                break

            token = match_word()

        if token == "uniform":
            self.storage = "uniform"
            types = UNIFORM_TYPES
        elif token == "attribute":
            self.storage = "attribute"
            types = ATTRIBUTE_TYPES
        elif token == "varying" or token == "out":
            self.storage = "varying"
            types = VARYING_TYPES
        elif token == "in":
            if fragment:
                self.storage = "varying"
                types = VARYING_TYPES
            else:
                self.storage = "attribute"
                types = ATTRIBUTE_TYPES
        else:
            self.storage = None
            return

        if self.invariant and self.storage != "varying":
            raise ShaderError(
                f"In {shader_name}, invariant can only qualify a varying, not '{self.storage}', in '{line}'."
            )

        if self.interpolation and self.storage != "varying":
            raise ShaderError(
                f"In {shader_name}, {self.interpolation} can only qualify a varying, not '{self.storage}', in '{line}'."
            )

        token = match_word()

        if token in GLSL_PRECISIONS:
            self.precision = token
            token = match_word()

        if token not in types:
            raise ShaderError(f"In {shader_name}, Unsupported type {token} in '{line}'. Only float, int, bool, vec<2-4>, ivec<2-4>, bvec<2-4>, mat<2-4>, and sampler2D are supported.")

        self.type = token

        self.array = match_array()

        self.name = match_word()
        if self.name is None:
            raise ShaderError(f"In {shader_name}, couldn't find name in '{line}'.")

        if self.array is None:
            self.array = match_array()

        if l.rstrip():
            raise ShaderError("Spurious tokens after the name in '{}'.".format(line))

    def declaration(self, fragment, gles, version):
        """
        Returns the GLSL declaration of this variable, in the dialect the
        shader is being emitted in.

        `fragment`
            True if this is being emitted into a fragment shader.

        `gles`
            True if this is being emitted into an OpenGL ES context.

        `version`
            The GLSL version being targeted (100, 120, 300, or 330).
        """

        modern = version >= 300

        if self.storage == "uniform":
            storage = "uniform"
        elif not modern:
            storage = self.storage
        elif self.storage == "attribute":
            storage = "in"
        else: # A varying is written by vertex and read by fragment.
            storage = "in" if fragment else "out"

        rv = []

        # GLSL ES 3.00 permits invariant on the vertex output, but not on the
        # matching fragment input. Desktop GLSL requires the matching input to
        # be invariant as well.
        if self.invariant and not (gles and version == 300 and fragment):
            rv.append("invariant")

        interpolation = self.interpolation

        if interpolation is None and self.storage == "varying" and self.type in FLAT_TYPES:
            interpolation = "flat"

        unsupported = (
            (interpolation == "flat" and not modern)
            or (interpolation == "noperspective" and (not modern or gles))
        )

        if unsupported:
            dialect = "GLSL ES {}".format(version) if gles else "desktop GLSL {}".format(version)
            message = (
                f"In shader {self.shader_name}, {interpolation} interpolation on {self.name} is not supported by "
                f"{dialect}; it will be omitted."
            )

            if renpy.config.developer:
                raise ShaderError(message)

            warning = (interpolation, gles, version)

            if warning not in self.interpolation_warnings:
                self.interpolation_warnings.add(warning)
                renpy.display.log.write("%s", message)

            interpolation = None

        if modern and self.storage == "varying" and interpolation is not None:
            rv.append(interpolation)

        rv.append(storage)

        # Precision qualifiers were added to desktop GLSL in 1.30.
        if self.precision and version != 120:
            rv.append(self.precision)

        rv.append(self.type)

        name = self.name

        if self.array is not None:
            name = "{}[{}]".format(name, self.array)

        rv.append(name)

        return " ".join(rv)

    def merge(self, other):
        """
        Returns a variable combining the qualifiers of this variable and
        `other`, which must declare the same thing.
        """

        qualifiers = (self.precision, self.invariant, self.interpolation)

        if qualifiers == (other.precision, other.invariant, other.interpolation):
            return self

        rv = copy.copy(self)

        rv.invariant = self.invariant or other.invariant

        rv.precision = max(
            self.precision, other.precision, key=GLSL_PRECISION_RANK.index)

        rv.interpolation = max(
            self.interpolation, other.interpolation, key=GLSL_INTERPOLATION_RANK.index)

        return rv

    def __hash__(self):
        return hash((self.storage, self.type, self.name, self.array))

    def __eq__(self, other):
        return (self.storage, self.type, self.name, self.array) == (other.storage, other.type, other.name, other.array)


cdef inline void upload_mesh_scratch(GLStateCache cache, Mesh mesh, GLuint* vbo, GLuint* abo, GLuint* ibo) noexcept nogil:
    vbo[0] = 0
    abo[0] = 0
    ibo[0] = 0

    if not cache.core_profile:
        return

    vbo[0] = cache.upload_scratch(
        SCRATCH_POSITION, GL_ARRAY_BUFFER,
        mesh.points * mesh.point_size * sizeof(float), mesh.point_data)

    if mesh.layout.stride:
        abo[0] = cache.upload_scratch(
            SCRATCH_ATTRIBUTE, GL_ARRAY_BUFFER,
            mesh.points * mesh.layout.stride * sizeof(float), mesh.attribute)

    ibo[0] = cache.upload_scratch(
        SCRATCH_INDEX, GL_ELEMENT_ARRAY_BUFFER,
        3 * mesh.triangles * sizeof(unsigned int), mesh.triangle)


cdef inline void set_attribute_pointer(GLStateCache cache, GLuint buffer, GLint location, GLint size, int stride, const float* data, int offset) noexcept nogil:
    cache.bind_array_buffer(buffer)

    if buffer:
        glVertexAttribPointer(location, size, GL_FLOAT, GL_FALSE, stride * sizeof(float), <const void*> (<size_t> offset * sizeof(float)))
    else:
        glVertexAttribPointer(location, size, GL_FLOAT, GL_FALSE, stride * sizeof(float), data + offset)


cdef inline void draw_mesh_elements(GLStateCache cache, GLuint ibo, Mesh mesh) noexcept nogil:
    cache.bind_element_buffer(ibo)

    if ibo:
        glDrawElements(GL_TRIANGLES, 3 * mesh.triangles, GL_UNSIGNED_INT, NULL)
    else:
        glDrawElements(GL_TRIANGLES, 3 * mesh.triangles, GL_UNSIGNED_INT, mesh.triangle)


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

    def __dealloc__(self):
        glDeleteProgram(self.program)

    def find_variables(self, source, seen_uniforms: set, samplers: int, fragment=False):

        shader_name = "+".join(self.name)

        for line in source.split("\n"):

            l = line.strip()

            # Only top-level declarations are of interest here.
            if not l.endswith(";"):
                continue

            if ("(" in l) or ("=" in l) or ("{" in l):
                continue

            l = l.rstrip("; ")

            if not l:
                continue

            # This declaration is generated by shadercache.source. User-provided
            # layout declarations have already been rejected by Variable.
            if fragment and l == "layout(location = 0) out vec4 {}".format(FRAGMENT_OUTPUT):
                continue

            v = Variable(shader_name, l, fragment)

            if v.storage == "uniform":
                if v.name in seen_uniforms:
                    continue

                location = glGetUniformLocation(self.program, v.name.encode("utf-8"))

                if location >= 0:
                    seen_uniforms.add(v.name)
                    setter, samplers = generate_uniform_setter(shader_name, location, v.name, v.type, v.array, samplers)
                    self.uniform_setters.append(setter)

            elif v.storage == "attribute" and not fragment:
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
        cdef GLint max_samplers = 0

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

        samplers = self.find_variables(self.vertex, seen_uniforms, samplers, False)
        samplers = self.find_variables(self.fragment, seen_uniforms, samplers, True)

        glGetIntegerv(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS, &max_samplers)

        if max_samplers > 0 and samplers > max_samplers:
            raise ShaderError(
                "Shader %s needs %d texture units, but this system provides %d." % (
                    "+".join(self.name), samplers, max_samplers))

    cpdef void draw(self, GL2DrawingContext context, GL2Model model, Mesh mesh):

        cdef Attribute a
        cdef int i
        cdef dict properties
        cdef dict attribute_offsets
        cdef GLStateCache cache = context.state_cache
        cdef unsigned int required_mask = 0
        cdef GLuint vbo, abo, ibo

        cache.use_program(self.program)

        properties = context.properties
        attribute_offsets = mesh.layout.offset

        upload_mesh_scratch(cache, mesh, &vbo, &abo, &ibo)

        # Set up the attributes and build the mask of required attribute arrays.
        for a in self.attributes:
            if a.name == "a_position":
                set_attribute_pointer(cache, vbo, a.location, mesh.point_size, mesh.point_size, mesh.point_data, 0)
                required_mask |= (<unsigned int> 1 << a.location)
            else:
                try:
                    offset = attribute_offsets[a.name]
                    set_attribute_pointer(cache, abo, a.location, a.size, mesh.layout.stride, mesh.attribute, <int> offset)
                    required_mask |= (<unsigned int> 1 << a.location)
                except KeyError:
                    shader_name = "+".join(self.name)
                    raise ShaderError(f"Shader {shader_name} requires attribute {a.name}, but it is not in the mesh.")

        # Enable and disable only the vertex attrib arrays that changed.
        cache.sync_attrib_arrays(required_mask)

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
                cache.set_color_mask(mask_r, mask_g, mask_b, mask_a)

            if "blend_func" in properties:
                rgb_eq, src_rgb, dst_rgb, alpha_eq, src_alpha, dst_alpha = properties["blend_func"]
                cache.set_blend(rgb_eq, alpha_eq, src_rgb, dst_rgb, src_alpha, dst_alpha)

        draw_mesh_elements(cache, ibo, mesh)

        if properties:

            if "blend_func" in properties:
                cache.set_blend(GL_FUNC_ADD, GL_FUNC_ADD, GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

            if "color_mask" in properties:
                cache.set_color_mask(True, True, True, True)

    def draw_ftl(self, GLStateCache cache, GLuint texture, Mesh mesh):
        """
        Draws the given texture using mesh, for the ftl alpha premultiply shader.

        `cache`
            The GL2Draw's GLStateCache, used to skip redundant GL calls.
        """

        cdef Attribute a
        cdef unsigned int required_mask = 0
        cdef GLuint vbo, abo, ibo

        cache.use_program(self.program)

        upload_mesh_scratch(cache, mesh, &vbo, &abo, &ibo)

        # Set up the attributes.
        for a in self.attributes:
            if a.name == "a_position":
                set_attribute_pointer(cache, vbo, a.location, mesh.point_size, mesh.point_size, mesh.point_data, 0)
                required_mask |= (<unsigned int> 1 << a.location)
            else:
                offset = mesh.layout.offset.get(a.name, None)
                if offset is None:
                    self.missing("mesh attribute", a.name)

                set_attribute_pointer(cache, abo, a.location, a.size, mesh.layout.stride, mesh.attribute, <int> offset)
                required_mask |= (<unsigned int> 1 << a.location)

        cache.sync_attrib_arrays(required_mask)

        # There's only one setter, and it's for tex0.
        cdef Sampler2DSetter setter

        for setter in self.uniform_setters:
            setter.set_texture(cache, texture)

        draw_mesh_elements(cache, ibo, mesh)
