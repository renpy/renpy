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

from uguugl cimport *
from renpy.gl2.gl2shader cimport Program
from renpy.gl2.gl2geometry cimport Mesh

cdef class TextureLoader:

    # The texture generation.
    cdef int generation

    # A map from texture number to the generation that number belongs to.
    cdef dict texture_generation

    # A list of (number, generation) pairs for textures that need to be freed.
    cdef list free_list

    # The number of textures that have been allocated but not deallocated.
    cdef int texture_count

    # The total size (in bytes) of all the textures that have been allocated
    # but not deallocated.
    cdef int total_texture_size

    # The framebuffer object used for fast texture loading.
    cdef GLuint ftl_fbo

    # The program used for fast texture loading
    cdef Program ftl_program

    # The mesh used for fast texture loading.
    cdef Mesh ftl_mesh

    # The queue of textures that need to be loaded.
    cdef object texture_load_queue



cdef class GLTextureCore:

    # The size of the texture.
    cdef public int width
    cdef public int height

    # A generation number, to prevent stale texture objects from being
    # retained.
    cdef public int generation

    # The number of the texture in OpenGL.
    cdef public unsigned int number

    # Has this texture been loaded yet?
    cdef public bint loaded

    # This is the data required to load a texture, if it has not been
    # loaded yet.
    cdef unsigned char *data

    # The texture loader associated with this texture.
    cdef TextureLoader loader

