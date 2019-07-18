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


from sdl2 cimport *
from pygame_sdl2 cimport *
import_pygame_sdl2()

from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

import sys
import time
import collections
import weakref

import renpy
from renpy.gl2.uguugl cimport *
from renpy.gl2.gl2draw cimport GL2Draw
from renpy.gl2.gl2geometry cimport rectangle, texture_rectangle, Mesh


################################################################################



cdef class TextureLoader:

    def __init__(self, GL2Draw draw):
        self.generation = 1
        self.texture_generation = { }
        self.free_list = [ ]
        self.texture_count = 0
        self.total_texture_size = 0
        self.texture_load_queue = weakref.WeakSet()

        glGenFramebuffers(1, &self.ftl_fbo)

        self.ftl_program = draw.shader_cache.get(("renpy.ftl",))

    def load_surface(self, surf):
        """
        Converts a surface into a texture.
        """

        size = surf.get_size()
        w, h = size

        tex = GLTexture(surf, self)

        mesh = Mesh()

        mesh.add_attribute("aTexCoord", 2)
        mesh.add_texture_rectangle(0.0, 0.0, w, h)

        rv = TexturedMesh(surf.get_size(),
                          mesh,
                          { "uTex0" : tex },
                          ( "renpy.geometry", "renpy.texture" ),
                          { })

        return rv


    def cleanup(self):
        """
        This is called once per frame, to free textures that are no longer used.
        """

        cdef GLuint texnums[1]

        for (texture_number, texture_generation) in self.free_list:
            if self.generation == texture_generation:
                texnums[0] = texture_number
                glDeleteTextures(1, texnums)

        self.free_list = [ ]


    def end_generation(self):
        """
        This deallocates the current generation of textures, and starts a new one.
        """

        self.cleanup()

        # Do not reset texture numbers - we don't want to reuse a number that's
        # in use, only to have it deallocated later.

        self.generation += 1


cdef class GLTextureCore:
    """
    This class represents an OpenGL texture that needs to be loaded by
    Ren'Py. It's responsible for handling deferred loading of textures,
    and using the Python reference counting system to free textures that
    are no longer required.
    """

    def __init__(self, surface, loader):

        # The width and height of this texture.
        self.width, self.height = surface.get_size()

        # The number of the OpenGL texture this texture object
        # represents.
        self.generation = 0
        self.number = 0

        # True if the texture has been loaded into OpenGL, False otherwise.
        self.loaded = False

        # Make a copy of the texture data.
        cdef SDL_Surface *s
        s = PySurface_AsSurface(surface)

        cdef unsigned char *pixels = <unsigned char *> s.pixels
        cdef unsigned char *data = <unsigned char *> malloc(s.h * s.w * 4)

        cdef unsigned char *p = data

        if s.pitch == s.w * 4:
            memcpy(p, pixels, s.h * s.w * 4)
        else:
            for 0 <= i < s.h:
                memcpy(p, pixels, s.w * 4)

                pixels += s.pitch
                p += (s.w * 4)

        self.data = data

        self.loader = loader
        self.loader.texture_load_queue.add(self)
        self.loader.total_texture_size += self.width * self.height * 4
        self.loader.texture_count += 1


    def load(self):
        """
        Loads this texture. When it's loaded, generation and number are set,
        and the texture is ready to use.
        """

        cdef GLuint old_fbo
        cdef GLuint tex
        cdef GLuint premultiplied

        if self.loaded:
            return

        # Generate the old textures.
        glGenTextures(1, &tex)
        glGenTextures(1, &premultiplied)

        # Bind the framebuffer.
        glGetIntegerv(GL_FRAMEBUFFER_BINDING, <GLint *> &old_fbo);
        glBindFramebuffer(GL_FRAMEBUFFER, self.loader.ftl_fbo)

        # Create premultiplied as an empty texture.
        glBindTexture(GL_TEXTURE_2D, premultiplied)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, NULL)

        # Bind premultiplied to the framebuffer.
        glFramebufferTexture2D(
            GL_FRAMEBUFFER,
            GL_COLOR_ATTACHMENT0,
            GL_TEXTURE_2D,
            premultiplied,
            0)

        # Set up the viewport and clear the  texure.
        glViewport(0, 0, self.width, self.height)

        # glClearColor(0, 0, 0, 0)
        # glClear(GL_COLOR_BUFFER_BIT)

        # Set up a mesh.
        m = Mesh()
        m.add_attribute("aTexCoord", 2)
        m.add_polygon([
            -1.0, -1.0, 0.0, 1.0, 0.0, 0.0,
            -1.0,  1.0, 0.0, 1.0, 0.0, 1.0,
             1.0,  1.0, 0.0, 1.0, 1.0, 1.0,
             1.0, -1.0, 0.0, 1.0, 1.0, 0.0,
            ])

        # Load the pixel data into tex, and set it up for drawing.
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # Set up the blend mode for premultiplication.
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ZERO, GL_ONE, GL_ZERO)

        # Draw.
        self.loader.ftl_program.draw(m, { "uTex0" : 0 })

        # Delete tex.
        glDeleteTextures(1, &tex)

        # Configure premultiplied.
        glBindTexture(GL_TEXTURE_2D, premultiplied)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Set the old framebuffer.
        glBindFramebuffer(GL_FRAMEBUFFER, old_fbo)

        # Store the loaded texture.
        self.number = premultiplied
        self.generation = self.loader.generation
        self.loader.texture_generation[self.number] = self.loader.generation

        self.loaded = True

        # Free the data memory.
        free(self.data)
        self.data = NULL

    def __dealloc__(self):

        if self.data:
            free(self.data)
            self.data = NULL

    def __del__(self):
        try:
            if self.loaded:
                self.loader.free_list.append((self.number, self.generation))

            self.loader.total_texture_size -= self.width * self.height * 4
            self.loader.texture_count -= 1
        except TypeError:
            pass # Let's not error on shutdown.

# Wraps GLTextureCore in a Python class, so garbage collection can occur.
class GLTexture(GLTextureCore):
    pass



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


