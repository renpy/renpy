cdef class Matrix2D:
    cdef public double xdx
    cdef public double xdy
    cdef public double ydx
    cdef public double ydy

    cpdef tuple transform(Matrix2D self, double x, double y)

cdef class Render:

    cdef public bint mark, cache_killed

    cdef public float width, height
    cdef public object layer_name

    cdef public list children
    cdef public set parents
    cdef public list depends_on_list

    cdef public int operation
    cdef public double operation_complete
    cdef public bint operation_alpha
    cdef public object operation_parameter

    cdef public Matrix2D forward, reverse
    cdef public double alpha
    cdef public double over

    cdef public list focuses
    cdef public list pass_focuses
    cdef public object draw_func
    cdef public object render_of

    cdef public bint opaque
    cdef public list visible_children

    cdef public bint clipping

    cdef public object surface, alpha_surface, half_cache

    cdef public bint modal

    cpdef int blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)
    cpdef int subpixel_blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)


cpdef render(object d, object widtho, object heighto, double st, double at)

