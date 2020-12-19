# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.display.matrix cimport Matrix, Matrix2D
cimport renpy.display.render as render
from renpy.gl2.gl2texture cimport TextureLoader
from renpy.uguu.gl cimport *

cdef class GL2Draw:


    cdef public bint gles
    cdef public bint angle

    cdef bint did_init
    cdef object window
    cdef tuple virtual_size
    cdef public tuple physical_size
    cdef public tuple drawable_size
    cdef public tuple virtual_box
    cdef public tuple physical_box
    cdef object texture_cache
    cdef double last_redraw_time
    cdef double redraw_period
    cdef public dict info
    cdef object old_fullscreen
    cdef public object fullscreen_surface
    cdef object display_info
    cdef tuple clip_cache
    cdef tuple default_clip
    cdef float dpi_scale
    cdef object shader_cache

    cdef public tuple clip_rtt_box

    cdef public float draw_per_phys
    cdef public tuple drawable_viewport

    cdef public object draw_per_virt
    cdef public Matrix virt_to_draw
    cdef public Matrix draw_to_virt

    # The matrix that goes from drawable space to the window. This isn't used
    # directly, it's used to determine if something is being drawn in a wa
    # that it shoudl be lined up with pixels.
    cdef public Matrix draw_transform

    cdef public int fast_redraw_frames

    # The color texture object used for offscreen rendering.
    cdef GLuint color_texture

    # The depth renderbuffer object used for offscreen rendering.
    cdef GLuint depth_renderbuffer

    # The framebuffer object used for offscreen rendering.
    cdef GLuint fbo

    # The texture_loader singleton.
    cdef public TextureLoader texture_loader

    # The default FBO.
    cdef public GLuint default_fbo

    # The current FBO.
    cdef public GLuint current_fbo

    cdef void change_fbo(self, GLuint fbo)
