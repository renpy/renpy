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

cdef class GLStateCache:
    """
    This tracks the OpenGL state that Ren'Py sets, so that redundant
    state changes can be skipped.
    """

    # The currently bound shader program.
    cdef GLuint current_program

    # The currently bound texture, for each of the first 8 texture units.
    cdef GLuint current_texture[8]

    # The currently active texture unit.
    cdef GLenum current_active_texture

    # The blend state.
    cdef GLenum blend_eq_rgb
    cdef GLenum blend_eq_alpha
    cdef GLenum blend_src_rgb
    cdef GLenum blend_dst_rgb
    cdef GLenum blend_src_alpha
    cdef GLenum blend_dst_alpha

    # The color mask state.
    cdef bint color_mask_r
    cdef bint color_mask_g
    cdef bint color_mask_b
    cdef bint color_mask_a

    # A bitmask of the currently enabled vertex attribute arrays.
    cdef unsigned int enabled_attrib_mask

    # A per-program sampler binding cache, mapping (program, location) to the
    # sampler unit. This avoids redundant glUniform1i calls.
    cdef dict sampler_bindings

    cpdef void reset(GLStateCache self)

    cdef void use_program(GLStateCache self, GLuint program)

    cdef void activate_texture(GLStateCache self, GLenum unit)

    cdef void bind_texture(GLStateCache self, GLenum unit, GLuint texture)

    cdef void set_blend(
        GLStateCache self,
        GLenum eq_rgb,
        GLenum eq_alpha,
        GLenum src_rgb,
        GLenum dst_rgb,
        GLenum src_alpha,
        GLenum dst_alpha,
    )

    cdef void set_color_mask(GLStateCache self, bint r, bint g, bint b, bint a)

    cdef void sync_attrib_arrays(GLStateCache self, unsigned int required_mask)

    cdef bint check_sampler_binding(GLStateCache self, GLuint program, GLint location, int sampler)
