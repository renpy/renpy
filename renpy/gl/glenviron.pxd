from gldraw cimport *

cdef class Environ:
    cdef void set_vertex(self, float *vertices)        
    cdef void set_texture(self, int unit, float *coords)            
    cdef void set_color(self, float, float, float, float)
    