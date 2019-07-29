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
import math

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

        glGenRenderbuffers(1, &self.ftl_renderbuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.ftl_renderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, 2048, 2048)
        glBindFramebuffer(GL_FRAMEBUFFER, self.ftl_fbo)

        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER,
            GL_COLOR_ATTACHMENT0,
            GL_RENDERBUFFER,
            self.ftl_renderbuffer)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.ftl_program = draw.shader_cache.get(("renpy.ftl",))

        # Set up a mesh.
        m = Mesh()
        m.add_attribute("aTexCoord", 2)
        m.add_polygon([
            -1.0, -1.0, 0.0, 1.0, 0.0, 0.0,
            -1.0,  1.0, 0.0, 1.0, 0.0, 1.0,
             1.0,  1.0, 0.0, 1.0, 1.0, 1.0,
             1.0, -1.0, 0.0, 1.0, 1.0, 0.0,
            ])

        self.ftl_mesh = m



    def load_one_surface(self, surf, bl, bt, br, bb):
        """
        Converts a surface into a texture.
        """

        size = surf.get_size()
        w, h = size

        tex = GLTexture(surf, self)

        mesh = Mesh()
        mesh.add_attribute("aTexCoord", 2)
        if (w and h):
            mesh.add_texture_rectangle(
                0.0, 0.0, w - bl - br, h - bt - bb,
                1.0 * bl / w, 1.0 * bt / h, 1.0 - 1.0 * br / w, 1.0 - 1.0 * bb / h)

        rv = TexturedMesh(surf.get_size(),
                          mesh,
                          ( "renpy.geometry", "renpy.texture" ),
                          { "uTex0" : tex },
                          [ tex ])

        return rv

    def texture_axis(self, length, limit, border):
        """
        Splits `length` up into multiple textures.

        This returns a series of (offset, width, left/top border, right/bottom border) tuples.
        """

        if length <= limit:
            return [ (0, length, 0, 0) ]

        elif length <= 2 * (limit - border):

            right = length // 2
            left = length - right

            return [ (0, left, 0, border), (left, right, border, 0) ]

        else:
            tiles = math.ceil(1.0 * length / (limit - 2 * border))
            tile_length = length / tiles
            tiles = int(tiles)

            rv = [ ]

            for i in xrange(tiles):
                start = int(i * tile_length)
                end = int((i + 1) * tile_length)

                if i > 0:
                    left = border
                else:
                    left = 0

                if i < tiles - 1:
                    right = border
                else:
                    right = 0

                rv.append((start, end - start, left, right))

        return rv


    def load_surface(self, surf):
        limit = 100
        border = 1

        size = surf.get_size()
        w, h = size

        if (w <= limit) and (h <= limit):
            return self.load_one_surface(surf, 0, 0, 0, 0)

        htiles = self.texture_axis(w, limit, border)
        vtiles = self.texture_axis(h, limit, border)

        rv = renpy.display.render.Render(w, h)

        for ty, th, bt, bb in vtiles:
            for tx, tw, bl, br in htiles:
                ss = surf.subsurface((tx - bl, ty - bt, tw + bl + br, th + bt + bb))
                t = self.load_one_surface(ss, bl, bt, br, bb)
                rv.blit(t, (tx, ty))

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

    def __repr__(self):
        return "<GLTexture {}x{} {}>".format(self.width, self.height, self.number)

    def load(self):
        """
        Loads this texture. When it's loaded, generation and number are set,
        and the texture is ready to use.
        """

        cdef GLuint old_fbo
        cdef GLuint tex
        cdef GLuint premultiplied
        cdef Program program

        if self.loaded:
            return

        # Generate the old textures.
        glGenTextures(1, &tex)
        glGenTextures(1, &premultiplied)

        # Bind the framebuffer.
        glGetIntegerv(GL_FRAMEBUFFER_BINDING, <GLint *> &old_fbo);
        glBindFramebuffer(GL_FRAMEBUFFER, self.loader.ftl_fbo)

        # Load the pixel data into tex, and set it up for drawing.
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # Set up the viewport.
        glViewport(0, 0, self.width, self.height)

        # Set up the blend mode for premultiplication.
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ZERO, GL_ONE, GL_ZERO)

        # Draw.
        program = self.loader.ftl_program
        program.start()
        program.set_uniform("uTex0", tex)
        program.draw(self.loader.ftl_mesh)
        program.finish()

        # Create premultiplied.
        glBindTexture(GL_TEXTURE_2D, premultiplied)
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, self.width, self.height, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # Set the old framebuffer.
        glBindFramebuffer(GL_FRAMEBUFFER, old_fbo)

        # Delete tex.
        glDeleteTextures(1, &tex)

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
    """

    def __init__(self, size, mesh, shaders, uniforms, textures):
        self.size = size
        self.mesh = mesh
        self.shaders = shaders
        self.uniforms = uniforms
        self.textures = textures

    def copy(self):
        return TexturedMesh(self.size, self.mesh, self.shaders, self.uniforms, self.textures)

    def load(self):
        for i in self.textures:
            i.load()

    def get_size(self):
        return self.size

    def subsurface(self, rect):
        rv = self.copy()

        x, y, w, h = rect
        rv.mesh = self.mesh.crop(rectangle(x, y, x+w, y+h))
        rv.mesh.offset_inplace(-x, -y, 0)

        return rv


