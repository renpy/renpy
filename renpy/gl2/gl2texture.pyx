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

from renpy.display.matrix cimport Matrix

# This has different names in GL and GLES, but the same value.
cdef GLenum RGBA8 = 0x8058

################################################################################

cdef class TextureLoader:

    def __init__(TextureLoader self, GL2Draw draw):
        self.allocated = set()
        self.free_list = [ ]
        self.total_texture_size = 0
        self.texture_load_queue = weakref.WeakSet()
        self.draw = draw

        self.ftl_program = draw.shader_cache.get(("renpy.ftl",))

    def quit(self):
        """
        Gets rid of this TextureLoader.
        """

        cdef GLuint texnums[1]

        for texture_number in self.allocated:
            texnums[0] = texture_number
            glDeleteTextures(1, texnums)

    def get_texture_size(self):
        """
        Returns the amount of memory locked up in textures.
        """

        return self.total_texture_size, len(self.allocated)

    def load_one_surface(self, surf, bl, bt, br, bb):
        """
        Converts a surface into a texture.
        """

        size = surf.get_size()

        rv = Texture(size, self)
        rv.from_surface(surf)

        if bl or bt or br or bb:
            w, h = size

            mesh = Mesh()
            mesh.add_attribute("aTexCoord", 2)

            pw = w - bl - br
            ph = h - bt - bb

            if (w and h):

                mesh.add_texture_rectangle(
                    0.0, 0.0, pw, ph,
                    1.0 * bl / w, 1.0 * bt / h, 1.0 - 1.0 * br / w, 1.0 - 1.0 * bb / h)

            rv = Model((pw, ph), mesh, ("renpy.texture",), { "uTex0" : rv })

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
        border = 1

        size = surf.get_size()
        w, h = size

        if (w <= self.max_texture_width) and (h <= self.max_texture_height):
            return self.load_one_surface(surf, 0, 0, 0, 0)

        htiles = self.texture_axis(w, self.max_texture_width, border)
        vtiles = self.texture_axis(h, self.max_texture_height, border)

        rv = renpy.display.render.Render(w, h)

        for ty, th, bt, bb in vtiles:
            for tx, tw, bl, br in htiles:
                ss = surf.subsurface((tx - bl, ty - bt, tw + bl + br, th + bt + bb))
                t = self.load_one_surface(ss, bl, bt, br, bb)
                rv.blit(t, (tx, ty))

        return rv

    def render_to_texture(self, what):
        """
        Renders `what` to a texture.
        """

        rv = Texture(what.get_size(), self)
        rv.from_render(what)
        return rv


    def cleanup(self):
        """
        This is called once per frame, to free textures that are no longer used.
        """

        cdef GLuint texnums[1]

        for texture_number in self.free_list:
            texnums[0] = texture_number
            glDeleteTextures(1, texnums)
            self.allocated.remove(texture_number)

        self.free_list = [ ]


    def ready_one_texture(self):
        """
        Called by GL2Draw to implement ready_one_texture.
        """

        while True:

            try:
                tex = self.texture_load_queue.pop()
            except KeyError:
                return False

            if not tex.loaded:
                tex.load()
                return True

        return False

cdef class GLTexture:
    """
    This class represents an OpenGL texture that needs to be loaded by
    Ren'Py. It's responsible for handling deferred loading of textures,
    and using the Python reference counting system to free textures that
    are no longer required.
    """

    def __init__(GLTexture self, size, TextureLoader loader):

        cdef unsigned char *pixels
        cdef unsigned char *data
        cdef unsigned char *p

        # The width and height of this texture.
        self.width, self.height = size

        # The number of the OpenGL texture this texture object
        # represents.
        self.number = 0

        # True if the texture has been loaded into OpenGL, False otherwise.
        self.loaded = False

        # Used for loading surfaces.
        self.data = NULL
        self.surface = None

        # Update the loader.
        self.loader = loader
        self.loader.total_texture_size += self.width * self.height * 4

    def from_surface(GLTexture self, surface):
        """
        Called to indicate this texture should be loaded from a surface.
        """

        # Make a copy of the texture data.
        cdef SDL_Surface *s
        s = PySurface_AsSurface(surface)

        pitch_pixels = s.pitch / 4
        margin = pitch_pixels - s.w

        if s.w and s.h and (margin < 64) and s.w < self.loader.max_texture_width:
            # In-place path.

            self.data = NULL
            self.surface = surface

        else:
            # Copying path.

            pixels = <unsigned char *> s.pixels
            data = <unsigned char *> malloc(s.h * s.w * 4)
            p = data

            if s.pitch == s.w * 4:
                memcpy(p, pixels, s.h * s.w * 4)
            else:
                for 0 <= i < s.h:
                    memcpy(p, pixels, s.w * 4)

                    pixels += s.pitch
                    p += (s.w * 4)

            self.data = data
            self.surface = None

        self.loader.texture_load_queue.add(self)

    def from_render(GLTexture self, what):
        """
        This renders `what` to this texture.
        """

        cw, ch = size = what.get_size()

        loader = self.loader
        draw = self.loader.draw

        # The visible size of the texture.
        tw = min(int(math.ceil(cw * draw.draw_per_virt)), loader.max_texture_width)
        th = min(int(math.ceil(ch * draw.draw_per_virt)), loader.max_texture_height)

        cdef GLuint premultiplied

        glGenTextures(1, &premultiplied)

        # Bind the framebuffer.
        draw.change_fbo(draw.fbo)

        # Set up the viewport.
        glViewport(0, 0, tw, th)

        # Clear the screen.
        clear_r, clear_g, clear_b = renpy.color.Color(renpy.config.gl_clear_color).rgb
        glClearColor(clear_r, clear_g, clear_b, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Project the child from virtual space to the screen space.
        cdef Matrix transform
        transform = renpy.display.matrix.texture_projection(cw, ch)
        if what.reverse:
            transform *= what.reverse

        # Set up the default modes.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        context = renpy.gl2.gl2draw.GL2DrawingContext(draw)
        context.draw(what, transform)

        glBindTexture(GL_TEXTURE_2D, premultiplied)
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, tw, th, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        self.number = premultiplied
        self.loader.allocated.add(self.number)

        self.loaded = True

    def __repr__(self):
        return "<GLTexture {}x{} {}>".format(self.width, self.height, self.number)

    def load_gltexture(GLTexture self):
        """
        Loads this texture. When it's loaded, generation and number are set,
        and the texture is ready to use.
        """

        cdef GLuint tex
        cdef GLuint premultiplied
        cdef Program program
        cdef SDL_Surface *s

        if self.loaded:
            return

        draw = self.loader.draw

        # Generate the old textures.
        glGenTextures(1, &tex)
        glGenTextures(1, &premultiplied)

        # Bind the framebuffer.
        draw.change_fbo(draw.fbo)

        # Load the pixel data into tex, and set it up for drawing.
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        mesh = Mesh()
        mesh.add_attribute("aTexCoord", 2)

        # Load the texture through zero-copy and normal paths.
        if self.surface is not None:
            s = PySurface_AsSurface(self.surface)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, s.pitch / 4, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, s.pixels)
            mesh.add_texture_rectangle(-1.0, -1.0, 1.0, 1.0, 0.0, 0.0, 4.0 * s.w / s.pitch, 1.0)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
            mesh.add_texture_rectangle(-1.0, -1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0)

        # Set up the viewport.
        glViewport(0, 0, self.width, self.height)

        # Set up the blend mode for premultiplication.
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ZERO, GL_ONE, GL_ZERO)

        # Draw.
        program = self.loader.ftl_program
        program.start()
        program.set_uniform("uTex0", tex)
        program.draw(mesh)
        program.finish()

        # Create premultiplied.
        glBindTexture(GL_TEXTURE_2D, premultiplied)
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, self.width, self.height, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # Delete tex.
        glDeleteTextures(1, &tex)

        # Store the loaded texture.
        self.number = premultiplied
        self.loader.allocated.add(self.number)

        self.loaded = True

        # Free the data memory.
        if self.data != NULL:
            free(self.data)
            self.data = NULL

        self.surface = None

    def __dealloc__(self):

        if self.data:
            free(self.data)
            self.data = NULL

    def __del__(self):
        try:
            if self.loaded:
                self.loader.free_list.append(self.number)

            self.loader.total_texture_size -= self.width * self.height * 4
        except TypeError:
            pass # Let's not error on shutdown.


################################################################################

class Model(object):
    """
    A Model can be placed in the render tree, and contains the information
    required to be drawn to a screen.
    """

    def __init__(self, size, mesh, shaders, uniforms):
        # The size of this model's bounding box, in virtual pixels.
        self.size = size

        # The mesh.
        self.mesh = mesh

        # A tuple giving the shaders used with this model.
        self.shaders = shaders

        # Either a dictionary giving uniforms associated with this model,
        # or None.
        self.uniforms = uniforms

        # The cached_texture that comes from this model.
        self.cached_texture = None

    def load(self):
        """
        Loads the textures associated with this model.
        """

        for i in self.uniforms.itervalues():
            if isinstance(i, GLTexture):
                i.load_gltexture()

    def program_uniforms(self, shader):
        """
        Called by the rest of the drawing code to set up the textures associated
        with this model.
        """

        shader.set_uniforms(self.uniforms)

    def get_size(self):
        """
        Returns the size of this Model.
        """

        return self.size

    def subsurface(self, rect):
        """
        Creates Model that fits within `rect`.
        """

        x, y, w, h = rect

        mesh = self.mesh.crop(rectangle(x, y, x+w, y+h))

        if mesh is self.mesh:
            if (x == 0) and (y == 0):
                return self

            mesh = mesh.offset(-x, -y, 0)
        else:
            mesh.offset_inplace(-x, -y, 0)

        rv = Model((w, h), self.mesh, self.shaders, self.uniforms)
        rv.mesh = mesh

        return rv


class Texture(GLTexture, Model):
    """
    A texture is Model and a GLTexture at the same time.

    This also implies that the Model has texture coordinates that range from
    (0.0, 0.0) to (1.0, 1.0) - and hence, that the GLTexture can be used to
    represent it.
    """

    def __init__(self, size, loader):

        GLTexture.__init__(self, size, loader)

        mesh = Mesh()
        mesh.add_attribute("aTexCoord", 2)

        w, h = size

        mesh.add_texture_rectangle(
            0.0, 0.0, w, h,
            0.0, 0.0, 1.0, 1.0,
            )

        Model.__init__(self, size, mesh, ("renpy.texture",), None)

    def load(self):
        self.load_gltexture()

    def program_uniforms(self, shader):
        shader.set_uniform("uTex0", self)

    def subsurface(self, rect):
        rv = Model.subsurface(self, rect)
        if rv is not self:
            rv.uniforms = { "uTex0" : self }
        return rv
