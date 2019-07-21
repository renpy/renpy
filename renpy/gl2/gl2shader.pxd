from uguugl cimport *

cdef class Program:

    # The name of this program.
    cdef public object name

    # The number of the OpenGL program created.
    cdef GLuint program

    # The text of the vertex and fragment shaders.
    cdef object vertex
    cdef object fragment

    cdef public dict uniforms

    cdef public list attributes

    cdef public int sampler

    cdef GLuint load_shader(self, GLenum shader_type, source) except? 0
