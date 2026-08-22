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

    def __init__(GLStateCache self):
        cdef int i

        self.sampler_bindings = {}

        # Set the cache to a safe initial state, without making GL calls.
        self.current_program = 0
        self.current_active_texture = 0

        for i in range(8):
            self.current_texture[i] = 0

        self.blend_eq_rgb = 0
        self.blend_eq_alpha = 0
        self.blend_src_rgb = 0
        self.blend_dst_rgb = 0
        self.blend_src_alpha = 0
        self.blend_dst_alpha = 0

        self.color_mask_r = True
        self.color_mask_g = True
        self.color_mask_b = True
        self.color_mask_a = True

        self.enabled_attrib_mask = 0

    cpdef void reset(GLStateCache self):
        """
        Resets the cache and forces GL state to known defaults.

        This should only be called when the GL context is valid.
        """

        cdef int i
        cdef unsigned int bit

        self.current_program = 0

        # 0 is not GL_TEXTURE0, so this forces the first activate call.
        self.current_active_texture = 0

        for i in range(8):
            self.current_texture[i] = 0

        # Force the GL blend state to Ren'Py's premultiplied alpha defaults.
        glBlendEquationSeparate(GL_FUNC_ADD, GL_FUNC_ADD)
        glBlendFuncSeparate(GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        self.blend_eq_rgb = GL_FUNC_ADD
        self.blend_eq_alpha = GL_FUNC_ADD
        self.blend_src_rgb = GL_ONE
        self.blend_dst_rgb = GL_ONE_MINUS_SRC_ALPHA
        self.blend_src_alpha = GL_ONE
        self.blend_dst_alpha = GL_ONE_MINUS_SRC_ALPHA

        # Force the color mask to all-enabled.
        glColorMask(True, True, True, True)

        self.color_mask_r = True
        self.color_mask_g = True
        self.color_mask_b = True
        self.color_mask_a = True

        # Disable all previously enabled vertex attribute arrays.
        if self.enabled_attrib_mask:
            for i in range(32):
                bit = <unsigned int> 1 << i

                if self.enabled_attrib_mask & bit:
                    glDisableVertexAttribArray(i)

        self.enabled_attrib_mask = 0

        # Clear the sampler binding cache, as it's program-specific.
        self.sampler_bindings.clear()

    cdef void use_program(GLStateCache self, GLuint program):
        if program != self.current_program:
            glUseProgram(program)

            self.current_program = program

    cdef void activate_texture(GLStateCache self, GLenum unit):
        if unit != self.current_active_texture:
            glActiveTexture(unit)

            self.current_active_texture = unit

    cdef void bind_texture(GLStateCache self, GLenum unit, GLuint texture):
        cdef int index = unit - GL_TEXTURE0

        self.activate_texture(unit)

        if index < 8 and self.current_texture[index] != texture:
            glBindTexture(GL_TEXTURE_2D, texture)

            self.current_texture[index] = texture

        # For units beyond the cached range, always bind.
        elif index >= 8:
            glBindTexture(GL_TEXTURE_2D, texture)

    cdef void set_blend(
        GLStateCache self,
        GLenum eq_rgb,
        GLenum eq_alpha,
        GLenum src_rgb,
        GLenum dst_rgb,
        GLenum src_alpha,
        GLenum dst_alpha,
    ):
        if eq_rgb != self.blend_eq_rgb or eq_alpha != self.blend_eq_alpha:
            glBlendEquationSeparate(eq_rgb, eq_alpha)

            self.blend_eq_rgb = eq_rgb
            self.blend_eq_alpha = eq_alpha

        if (
            src_rgb != self.blend_src_rgb
            or dst_rgb != self.blend_dst_rgb
            or src_alpha != self.blend_src_alpha
            or dst_alpha != self.blend_dst_alpha
        ):
            glBlendFuncSeparate(src_rgb, dst_rgb, src_alpha, dst_alpha)

            self.blend_src_rgb = src_rgb
            self.blend_dst_rgb = dst_rgb
            self.blend_src_alpha = src_alpha
            self.blend_dst_alpha = dst_alpha

    cdef void set_color_mask(GLStateCache self, bint r, bint g, bint b, bint a):
        if r != self.color_mask_r or g != self.color_mask_g or b != self.color_mask_b or a != self.color_mask_a:
            glColorMask(r, g, b, a)

            self.color_mask_r = r
            self.color_mask_g = g
            self.color_mask_b = b
            self.color_mask_a = a

    cdef void sync_attrib_arrays(GLStateCache self, unsigned int required_mask):
        """
        Enables exactly the vertex attribute arrays in `required_mask`, and
        disables any that were previously enabled but are no longer needed.

        Only issues GL calls for the difference.
        """

        cdef int i
        cdef unsigned int bit

        cdef unsigned int to_enable = required_mask & ~self.enabled_attrib_mask
        cdef unsigned int to_disable = self.enabled_attrib_mask & ~required_mask

        if to_enable:
            for i in range(32):
                bit = <unsigned int> 1 << i

                if to_enable & bit:
                    glEnableVertexAttribArray(i)

        if to_disable:
            for i in range(32):
                bit = <unsigned int> 1 << i

                if to_disable & bit:
                    glDisableVertexAttribArray(i)

        self.enabled_attrib_mask = required_mask

    cdef bint check_sampler_binding(GLStateCache self, GLuint program, GLint location, int sampler):
        """
        Returns True if the sampler-to-unit binding needs to be set, updating
        the cache if so.
        """

        cdef tuple key = (program, location)
        cdef object cached = self.sampler_bindings.get(key)

        if cached is not None and cached == sampler:
            return False

        self.sampler_bindings[key] = sampler

        return True
