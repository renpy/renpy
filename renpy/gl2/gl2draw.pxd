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
from renpy.gl2.gl2polygon cimport Polygon
from renpy.display.render cimport Render

from renpy.uguu.gl cimport *

cdef class GL2Draw:


    cdef public bint gles
    cdef public bint angle

    cdef public bint did_init
    cdef public object window
    cdef public tuple virtual_size
    cdef public tuple physical_size
    cdef public tuple drawable_size
    cdef public tuple virtual_box
    cdef public tuple physical_box
    cdef public double last_redraw_time
    cdef public double redraw_period
    cdef public dict info
    cdef public object old_fullscreen
    cdef public object fullscreen_surface
    cdef public object display_info
    cdef public tuple clip_cache
    cdef public tuple default_clip
    cdef public float dpi_scale
    cdef public object shader_cache
    cdef public bint ever_set_position

    cdef public tuple clip_rtt_box

    cdef public float draw_per_phys
    cdef public tuple drawable_viewport

    cdef public object draw_per_virt
    cdef public Matrix virt_to_draw
    cdef public Matrix draw_to_virt

    cdef public bint auto_mipmap

    # The matrix that goes from drawable space to the window. This isn't used
    # directly, it's used to determine if something is being drawn in a wa
    # that it should be lined up with pixels.
    cdef public Matrix draw_transform

    cdef public int fast_redraw_frames

    # The color texture object used for offscreen rendering.
    cdef public GLuint color_renderbuffer

    # The depth renderbuffer object used for offscreen rendering.
    cdef public GLuint depth_renderbuffer

    # The framebuffer object used for offscreen rendering.
    cdef public GLuint fbo

    # The color texture object used for pixel tests (1x1).
    cdef public GLuint color_renderbuffer_1px

    # The depth renderbuffer object used for pixel tests. (1x1)
    cdef public GLuint depth_renderbuffer_1px

    # The framebuffer object used for pixel tests (1x1)
    cdef public GLuint fbo_1px

    # The texture_loader singleton.
    cdef public TextureLoader texture_loader

    # The default FBO.
    cdef public GLuint default_fbo

    # The current FBO.
    cdef public GLuint current_fbo

    # Was the window maximized?
    cdef public bint maximized

    cdef void change_fbo(self, GLuint fbo)


cdef class GL2DrawingContext:

    # The width and height of the drawable surface that will be affected
    # by the draw operations.
    cdef float width
    cdef float height

    # Is debugging enabled?
    cdef bint debug

    # Caches a second GL2DrawingContext returned when child_context() is called.
    cdef GL2DrawingContext _child_context

    # A matrix that maps camera-space coordinates to viewport coordinates.
    cdef Matrix projection_matrix

    # A matrix that maps world-space coordinates to camera-space coordinates.
    cdef Matrix view_matrix

    # The projection and view matrices, multiplied together.
    cdef Matrix projectionview_matrix

    # A matrix that maps model-space coordinates to
    cdef Matrix model_matrix

    # The clipping Polygon
    cdef Polygon clip_polygon

    # A tuple giving the names of shaders that will be applied to the model.
    cdef tuple shaders

    # A dictionary mapping uniforms names to values.
    cdef dict uniforms

    # A dictionary mapping property names to values.
    cdef dict properties

    # Is the pixel perfect transform eligible to be performed?
    cdef bint pixel_perfect

    # Has depth been enabled?
    cdef bint has_depth

    cdef GL2DrawingContext child_context(self)

    cdef dict merge_properties(self, dict old, dict child)

    cdef void correct_pixel_perfect(self)

    cdef object draw_model(self, model)

    cdef void set_text_rect(self, Render r)

    cdef object draw_one(self, what)
