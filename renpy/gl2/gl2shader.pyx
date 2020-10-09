from renpy.uguu.gl cimport *
from libc.stdlib cimport malloc, free

from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2texture cimport GLTexture
from renpy.display.matrix cimport Matrix


class ShaderError(Exception):
    pass


GLSL_PRECISIONS = {
    "highp",
    "mediump",
    "lowp",
    }


cdef class Uniform:
    cdef Program program
    cdef GLint location
    cdef bint ready

    def __init__(self, program, location):
        self.program = program
        self.location = location
        self.ready = False

    cdef void assign(self, data):
        return

    cdef void finish(self):
        self.ready = False
        return

cdef class UniformFloat(Uniform):
    cdef void assign(self, data):
        glUniform1f(self.location, data)

cdef class UniformVec2(Uniform):
    cdef void assign(self, data):
        glUniform2f(self.location, data[0], data[1])

cdef class UniformVec3(Uniform):
    cdef void assign(self, data):
        glUniform3f(self.location, data[0], data[1], data[2])

cdef class UniformVec4(Uniform):
    cdef void assign(self, data):
        glUniform4f(self.location, data[0], data[1], data[2], data[3])

cdef class UniformMat4(Uniform):
    cdef void assign(self, data):
        glUniformMatrix4fv(self.location, 1, GL_FALSE, (<Matrix> data).m)

cdef class UniformSampler2D(Uniform):
    cdef int sampler

    def __init__(self, program, location):
        Uniform.__init__(self, program, location)
        self.sampler = program.samplers
        program.samplers += 1

    cdef void assign(self, data):
        glActiveTexture(GL_TEXTURE0 + self.sampler)
        glUniform1i(self.location, self.sampler)

        if isinstance(data, GLTexture):
            glBindTexture(GL_TEXTURE_2D, data.number)
            self.program.set_uniform("res{}".format(self.sampler), (data.texture_width, data.texture_height))
        else:
            glBindTexture(GL_TEXTURE_2D, data)



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
                location = glGetUniformLocation(self.program, name)

                if location >= 0:
                    self.uniforms[name] = types[type](self, location)

            else:
                location = glGetAttribLocation(self.program, name)

                if location >= 0:
                    self.attributes.append(Attribute(name, location, types[type]))

    cdef GLuint load_shader(self, GLenum shader_type, source) except? 0:
        """
        This loads a shader into the GPU, and returns the number.
        """

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
            raise ShaderError((<object> error).decode("utf-8"))

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
            raise ShaderError((<object> error).decode("utf-8"))

        glDeleteShader(vertex)
        glDeleteShader(fragment)

        self.program = program

        self.find_variables(self.vertex)
        self.find_variables(self.fragment)

    def missing(self, kind, name):
        raise Exception("Shader {} has not been given {} {}.".format(self.name, kind, name))

    def start(self):
        glUseProgram(self.program)

    def set_uniform(self, name, value):
        cdef Uniform u
        u = self.uniforms.get(name, None)
        if u is None:
            return

        u.assign(value)
        u.ready = True

    def set_uniforms(self, dict uniforms):
        cdef Uniform u

        for name, value in uniforms.iteritems():
            u = self.uniforms.get(name, None)
            if u is None:
                continue

            u.assign(value)
            u.ready = True

    def draw(self, Mesh mesh, dict properties):

        cdef Attribute a
        cdef Uniform u
        cdef int i

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

        if len(properties) > 1:

            if "color_mask" in properties:
                mask_r, mask_g, mask_b, mask_a = properties["color_mask"]
                glColorMask(mask_r, mask_g, mask_b, mask_a)

            if "texture_scaling" in properties:
                magnify, minify = TEXTURE_SCALING[properties["texture_scaling"]]

                for 0 <= i < self.samplers:
                    glActiveTexture(GL_TEXTURE0 + i)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magnify)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minify)

        glDrawElements(GL_TRIANGLES, 3 * mesh.triangles, GL_UNSIGNED_SHORT, mesh.triangle)

        if len(properties) > 1:

            if "texture_scaling" in properties:
                for 0 <= i < self.samplers:
                    glActiveTexture(GL_TEXTURE0 + i)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)

            if "color_mask" in properties:
                glColorMask(True, True, True, True)


    def finish(Program self):
        cdef Attribute a
        cdef Uniform u

        for a in self.attributes:
            glDisableVertexAttribArray(a.location)

        for u in self.uniforms.itervalues():
            u.finish()
