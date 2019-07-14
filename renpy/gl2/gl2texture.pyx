#@PydevCodeAnalysisIgnore
#cython: profile=False
# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

DEF ANGLE = False

from uguugl cimport *
from gl2draw cimport *

from sdl2 cimport *
from pygame_sdl2 cimport *
import_pygame_sdl2()

from libc.stdlib cimport calloc, free

import sys
import time
import collections
import renpy

from renpy.gl2.gl2geometry import rectangle, Mesh


################################################################################

# The texture generation.
generation = 1

# A map from texture number to the generation that number belongs to.
texture_generation = { }

# A list of (number, generation) pairs for textures that need to be freed.
free_list = [ ]

# The number of textues that have been allocated but not deallocated.
texture_count = 0

# The total size (in bytes) of all the textures that have been allocated
# but not deallocated.
total_texture_size = 0

cdef class GLTextureCore:
    """
    This class represents an OpenGL texture that needs to be loaded by
    Ren'Py. It's responsible for handling deferred loading of textures,
    and using the Python reference counting system to free textures that
    are no longer required.
    """

    def __init__(self, int width, int height):

        # The width and height of this texture.
        self.width = width
        self.height = height

        # The number of the OpenGL texture this texture object
        # represents.
        self.generation = 0
        self.number = 0

        # True if the texture has been loaded into OpenGL, False otherwise.
        self.loaded = False

        global texture_count
        global total_texture_size
        total_texture_size += self.width * self.height * 4
        texture_count += 1

    def __dealloc__(self):

        if self.data:
            free(self.data)
            self.data = NULL

    def __del__(self):
        try:
            if self.loaded:
                free_list.append((self.number, self.generation))

            global texture_count
            global total_texture_size
            total_texture_size -= self.width * self.height * 4
            texture_count -= 1
        except TypeError:
            pass # Let's not error on shutdown.

# Wraps GLTextureCore in a Python class, so garbace collection can occur.
class GLTexture(GLTextureCore):
    pass



def cleanup():
    """
    This is called once per frame, to free textures that are no longer used.
    """

    global free_list
    cdef GLuint texnums[1]

    for (texture_number, texture_generation) in free_list:
        if generation == texture_generation:
            texnums[0] = texture_number

            glDeleteTextures(1, texnums)

    free_list = [ ]


def end_generation():
    """
    This deallocates the current generation of textures, and starts a new one.
    """

    cleanup()

    # Do not reset texture numbers - we don't want to reuse a number that's
    # in use, only to have it deallocated later.

    global generation
    generation += 1


################################################################################

class TexturedMesh:
    """
    This represents a combination of the geometry, textures, shaders, and
    uniform values required to display something on the screen.

    :ivar Mesh mesh: Contains the geometry and per-vertex attributes.
    :ivar textures: Maps the names of textures used by the shaders to GLTexture
        objects.
    :vartype textures: dict(str, GLTexture)
    :ivar shaders: A tuple of strings giving the shaders that are used.
    :vartype shaders: list(str)
    :ivar uniforms: A dictionary mapping uniform names to their values.
    :vartype uniforms: dict(str, object)
    """

    def __init__(self, size, mesh, textures, shaders, uniforms):
        self.size = size
        self.mesh = mesh
        self.textures = textures
        self.shaders = shaders
        self.uniforms = uniforms

    def copy(self):
        return TexturedMesh(self.size, self.mesh, self.textures, self.shaders, self.uniforms)

    def get_size(self):
        return self.size

    def subsurface(self, rect):
        rv = self.copy()

        x, y, w, h = rect
        rv.mesh = self.mesh.crop_polygon(rectangle(x, y, w, h))
        rv.mesh.offset(-x, -y, 0)

        return self




