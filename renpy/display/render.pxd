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

cdef class Render:

    cdef public bint mark, cache_killed, killed

    cdef public float width, height
    cdef public object layer_name

    cdef public list children
    cdef public set parents
    cdef public list depends_on_list

    # gl, sw: The drawing operation and its parameters.
    cdef public int operation
    cdef public double operation_complete
    cdef public bint operation_alpha
    cdef public object operation_parameter

    # The transform toward texture space
    cdef public Matrix forward

    # The transform toward screen space.
    cdef public Matrix reverse

    # Alpha multiplication - this is multipled with r, g, b, and a, to reduce
    # the alpha of this Render and its children.
    cdef public double alpha

    # Over multiplication - this is multiplied with a. This is really (1-additive),
    # such that if this is 0.0, additive blending occurs.
    cdef public double over

    # True if child textures should be rendered in nearest-neighbor mode.
    cdef public object nearest

    cdef public list focuses
    cdef public list pass_focuses
    cdef public object focus_screen

    cdef public object render_of

    cdef public bint xclipping
    cdef public bint yclipping

    # gl, sw: Caching of render-to-texture.
    cdef public object surface, alpha_surface, half_cache

    cdef public object modal

    cdef public bint text_input

    # gl2 ######################################################################

    # The mesh. If this is not None, the children are all rendered to Textures,
    # and used to form a model. If this is True, the Mesh is taken from the first
    # child's Texture, otherwise this must be a Mesh.
    cdef public object mesh

    # A tuple of shaders that will be used when rendering, or None.
    cdef public tuple shaders

    # A dictionary containing uniforms that will be used when rendering, or
    # None.
    cdef public dict uniforms

    # Properties that control rendering.
    cdef public dict properties

    # Used to cache the result of rendering this Render to a texture.
    cdef public object cached_texture

    # Used to cache the model.
    cdef public object cached_model

    # True if the texture has been loaded.
    cdef public bint loaded

    # A flag that's used to enable debugging on a per-render basis.
    cdef public bint debug

    # operations ###############################################################

    cpdef int blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)
    cpdef int subpixel_blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)
    cpdef int absolute_blit(Render self, source, tuple pos, object focus=*, object main=*, object index=*)


cpdef render(object d, object widtho, object heighto, double st, double at)
