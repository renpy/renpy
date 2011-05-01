cimport render

cdef class GLDraw:

    cdef bint did_init
    cdef object environ
    cdef object rtt
    cdef object window
    cdef tuple virtual_size
    cdef public tuple physical_size
    cdef tuple virtual_box
    cdef tuple physical_box
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
    cdef bint use_clipping_planes
    cdef bint always_opaque
        
    cdef tuple clip_rtt_box
    
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
        render.Matrix2D reverse)

    
