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

cdef class Environ

cdef class GLDraw:

    cdef bint did_init
    cdef bint did_texture_test
    cdef Environ environ
    cdef public object rtt
    cdef object window
    cdef tuple virtual_size
    cdef public tuple physical_size
    cdef public tuple drawable_size
    cdef public tuple virtual_box
    cdef public tuple physical_box
    cdef object mouse_old_visible
    cdef object mouse_info
    cdef object texture_cache
    cdef double last_redraw_time
    cdef double redraw_period
    cdef public dict info
    cdef object old_fullscreen
    cdef public object fullscreen_surface
    cdef object display_info
    cdef tuple clip_cache
    cdef bint fast_dissolve
    cdef bint allow_fixed
    cdef tuple default_clip
    cdef bint did_render_to_texture
    cdef float dpi_scale
    cdef object ready_texture_queue

    cdef public tuple clip_rtt_box

    # The number of drawable pixels per virtual pixel.
    cdef public object draw_per_virt

    # Matrices that transform drawable to virtual, and vice versa.
    cdef public Matrix virt_to_draw
    cdef public Matrix draw_to_virt

    cdef public int fast_redraw_frames

    cpdef set_clip(GLDraw self, tuple clip)

    cpdef int draw_render_textures(
        GLDraw self,
        object what,
        bint non_aligned) except 1

    cpdef int draw_transformed(
        GLDraw self,
        object what,
        tuple clip,
        double xo,
        double yo,
        double alpha,
        double over,
        Matrix reverse,
        bint nearest,
        bint subpixel) except 1

cdef class Environ:
    cdef void blit(self)
    cdef void blend(self, double fraction)
    cdef void imageblend(self, double fraction, int ramp)
    cdef void set_vertex(self, float *vertices)
    cdef void set_texture(self, int unit, float *coords)
    cdef void set_color(self, double r, double g, double b, double a)
    cdef void set_clip(self, tuple clip_box, GLDraw draw)
    cdef void unset_clip(self, GLDraw draw)
    cdef void ortho(self, double left, double right, double bottom, double top, double near, double far)
    cdef void viewport(self, int x, int y, int width, int height)

