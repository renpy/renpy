cimport renpy.display.render as render

cdef class Environ

cdef class GLDraw:

    cdef bint did_init
    cdef Environ environ
    cdef public object rtt
    cdef object window
    cdef tuple virtual_size
    cdef public tuple physical_size
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
    cdef double upscale_factor
    cdef tuple clip_cache
    cdef bint fast_dissolve
    cdef bint always_opaque
    cdef bint allow_fixed
    cdef tuple default_clip

    cdef public tuple clip_rtt_box

    cpdef set_clip(GLDraw self, tuple clip)

    cpdef int draw_render_textures(
        GLDraw self,
        object what,
        bint non_aligned)

    cpdef int draw_transformed(
        GLDraw self,
        object what,
        tuple clip,
        double xo,
        double yo,
        double alpha,
        double over,
        render.Matrix2D reverse)

cdef class Environ:
    cdef void blit(self)
    cdef void blend(self, double fraction)
    cdef void imageblend(self, double fraction, int ramp)
    cdef void set_vertex(self, float *vertices)
    cdef void set_texture(self, int unit, float *coords)
    cdef void set_color(self, float r, float g, float b, float a)
    cdef void set_clip(self, tuple clip_box, GLDraw draw)
    cdef void unset_clip(self, GLDraw draw)
    cdef void ortho(self, double left, double right, double bottom, double top, double near, double far)
    cdef void viewport(self, int x, int y, int width, int height)

