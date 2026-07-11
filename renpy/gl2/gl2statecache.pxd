from renpy.uguu.gl cimport *

cdef class GLStateCache:

    # the currently bound shader program
    cdef GLuint current_program

    # the currently bound texture, per texture unit (up to 8 units)
    cdef GLuint current_texture[8]

    # the currently active texture unit
    cdef GLenum current_active_texture

    # blend state
    cdef GLenum blend_eq_rgb
    cdef GLenum blend_eq_alpha
    cdef GLenum blend_src_rgb
    cdef GLenum blend_dst_rgb
    cdef GLenum blend_src_alpha
    cdef GLenum blend_dst_alpha

    # color mask state
    cdef bint color_mask_r
    cdef bint color_mask_g
    cdef bint color_mask_b
    cdef bint color_mask_a

    # a bitmask of the currently enabled vertex attribute arrays
    cdef unsigned int enabled_attrib_mask

    # a per-program sampler binding cache, {(program, location): sampler_unit}
    # this avoids redundant glUniform1i calls for sampler bindings
    cdef dict sampler_bindings

    cpdef void reset(GLStateCache self)

    cdef void use_program(GLStateCache self, GLuint program)

    cdef void activate_texture(GLStateCache self, GLenum unit)

    cdef void bind_texture(GLStateCache self, GLenum unit, GLuint texture)

    cdef void set_blend(GLStateCache self, GLenum eq_rgb, GLenum eq_alpha, GLenum src_rgb, GLenum dst_rgb, GLenum src_alpha, GLenum dst_alpha)

    cdef void set_color_mask(GLStateCache self, bint r, bint g, bint b, bint a)

    cdef void sync_attrib_arrays(GLStateCache self, unsigned int required_mask)

    cdef bint check_sampler_binding(GLStateCache self, GLuint program, GLint location, int sampler)