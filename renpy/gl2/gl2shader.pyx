from uguugl cimport *
from libc.stdlib cimport malloc, free

from renpy.gl2.gl2geometry cimport Polygon, Mesh
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
        glUniformMatrix4fv(self.location, 1, GL_TRUE, (<Matrix> data).m)

cdef class UniformSampler2D(Uniform):
    cdef int sampler

    def __init__(self, program, location):
        Uniform.__init__(self, program, location)
        self.sampler = program.sampler
        program.sampler += 1

    cdef void assign(self, data):
        glActiveTexture(GL_TEXTURE0 + self.sampler)
        glUniform1i(self.location, self.sampler)

        if isinstance(data, GLTexture):
            glBindTexture(GL_TEXTURE_2D, data.number)
        else:
            glBindTexture(GL_TEXTURE_2D, data)

    cdef void finish(self):
        glActiveTexture(GL_TEXTURE0 + self.sampler)
        return


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

        # The index of the next sampler to be added.
        self.sampler = 0

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

    def draw(self, Mesh mesh):

        cdef Attribute a

        # Set up the attributes.
        for a in self.attributes:
            offset = mesh.attributes.get(a.name, None)
            if offset is None:
                self.missing("mesh attribute", a.ame)

            glVertexAttribPointer(a.location, a.size, GL_FLOAT, GL_FALSE, mesh.stride * sizeof(float), mesh.get_data(offset))
            glEnableVertexAttribArray(a.location)

        if mesh.polygon_points == 3:
            glDrawArrays(GL_TRIANGLES, 0, 3 * mesh.polygon_count)
            return

        cdef int i = 0
        cdef Polygon p

        for p in mesh.polygons:

            glDrawArrays(GL_TRIANGLE_FAN, i, p.points)
            i += p.points

    def finish(self):
        cdef Attribute a
        cdef Uniform u

        for a in self.attributes:
            glDisableVertexAttribArray(a.location)

        for u in self.uniforms.itervalues():
            u.finish()


