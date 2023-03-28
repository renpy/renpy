#@PydevCodeAnalysisIgnore
#cython: profile=False
# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.uguu.gl cimport *
from renpy.gl2.gl2draw cimport GL2Draw

from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2mesh2 cimport Mesh2
from renpy.gl2.gl2model cimport GL2Model

from renpy.display.matrix cimport Matrix

# This has different names in GL and GLES, but the same value.
cdef GLenum RGBA8 = 0x8058

# An extension here,
cdef GLenum TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE
cdef GLenum MAX_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FF

################################################################################

cdef class TextureLoader:

    def __init__(TextureLoader self, GL2Draw draw):
        self.allocated = set()
        self.free_list = [ ]
        self.total_texture_size = 0
        self.texture_load_queue = weakref.WeakSet()
        self.draw = draw

    def init(self):

        if self.allocated:
            self.quit()

        self.ftl_program = self.draw.shader_cache.get(("renpy.ftl",))

        self.allocated = set()
        self.free_list = [ ]
        self.total_texture_size = 0
        self.texture_load_queue = weakref.WeakSet()

        if not self.draw.gles:
            glGetFloatv(MAX_TEXTURE_MAX_ANISOTROPY_EXT, &self.max_anisotropy)

    def quit(self):
        """
        Gets rid of this TextureLoader.
        """

        cdef GLuint texnums[1]

        for texture_number in self.allocated:
            texnums[0] = texture_number
            glDeleteTextures(1, texnums)

        self.allocated = set()

    def get_texture_size(self):
        """
        Returns the amount of memory locked up in textures.
        """

        return self.total_texture_size, len(self.allocated)

    def load_one_surface(self, surf, bl, bt, br, bb, properties):
        """
        Converts a surface into a texture.
        """

        size = surf.get_size()

        rv = Texture(size, self)
        rv.from_surface(surf, properties)

        if bl or bt or br or bb:
            w, h = size

            pw = w - bl - br
            ph = h - bt - bb

            if (w and h):

                mesh = Mesh2.texture_rectangle(
                    0.0, 0.0, pw, ph,
                    1.0 * bl / w, 1.0 * bt / h, 1.0 - 1.0 * br / w, 1.0 - 1.0 * bb / h)
            else:
                mesh = Mesh2.texture_rectangle(
                    0.0, 0.0, pw, ph,
                    0.0, 0.0, 0.0, 0.0)

            rv = GL2Model((pw, ph), mesh, ("renpy.texture",), { "tex0" : rv })

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


    def load_surface(self, surf, properties):
        border = 1

        size = surf.get_size()
        w, h = size

        if (w <= self.max_texture_width) and (h <= self.max_texture_height):
            return self.load_one_surface(surf, 0, 0, 0, 0, properties)

        htiles = self.texture_axis(w, self.max_texture_width, border)
        vtiles = self.texture_axis(h, self.max_texture_height, border)

        rv = renpy.display.render.Render(w, h)

        for ty, th, bt, bb in vtiles:
            for tx, tw, bl, br in htiles:
                ss = surf.subsurface((tx - bl, ty - bt, tw + bl + br, th + bt + bb))
                t = self.load_one_surface(ss, bl, bt, br, bb, properties)
                rv.blit(t, (tx, ty))

        return rv

    def render_to_texture(self, what, properties):
        """
        Renders `what` to a texture.
        """

        rv = Texture(what.get_size(), self)
        rv.from_render(what, properties)
        return rv


    def cleanup(self):
        """
        This is called once per frame, to free textures that are no longer used.
        """

        cdef GLuint texnums[1]

        for texture_number in self.free_list:
            texnums[0] = texture_number
            glDeleteTextures(1, texnums)

            if texture_number not in self.allocated:
                print("Leaking texture:", texture_number)

            self.allocated.discard(texture_number)

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

cdef class GLTexture(GL2Model):
    """
    This class represents an OpenGL texture that needs to be loaded by
    Ren'Py. It's responsible for handling deferred loading of textures,
    and using the Python reference counting system to free textures that
    are no longer required.
    """

    def __init__(GLTexture self, size, TextureLoader loader, generate=False):

        cdef unsigned char *pixels
        cdef unsigned char *data
        cdef unsigned char *p
        cdef GLuint number

        width, height = size

        GL2Model.__init__(self, size, None, ("renpy.texture",), None)

        # The number of the OpenGL texture this texture object
        # represents.
        self.number = 0

        # True if the texture has been loaded into OpenGL, False otherwise.
        self.loaded = False

        # Used for loading surfaces.
        self.surface = None

        # Update the loader.
        self.loader = loader

        if renpy.emscripten and generate:
            # Generate a texture name to access video frames for web
            glGenTextures(1, &number)
            self.number = number
            self.loaded = True
            self.loader.allocated.add(self.number)
            self.mesh = Mesh2.texture_rectangle(
                0.0, 0.0, width, height,
                0.0, 0.0, 1.0, 1.0,
                )
            self.properties = { }

    def has_mipmaps(GLTexture self):
        """
        Returns true if this texture has mipmaps (or will have mipmaps
        when it's loaded).
        """

        return self.properties.get("mipmap", True)

    def get_number(GLTexture self):
        return self.number if renpy.emscripten else None

    def from_surface(GLTexture self, surface, properties):
        """
        Called to indicate this texture should be loaded from a surface.
        """

        self.surface = surface
        self.properties = properties

        self.mesh = Mesh2.texture_rectangle(
            0.0, 0.0, self.width, self.height,
            0.0, 0.0, 1.0, 1.0,
            )

        self.loader.texture_load_queue.add(self)

    def from_render(GLTexture self, what, properties):
        """
        This renders `what` to this texture.
        """

        self.properties = {
            "mipmap" : properties.get("mipmap", True),
            "pixel_perfect" : properties.get("pixel_perfect", False),
            }

        cw, ch = size = what.get_size()

        loader = self.loader
        draw = self.loader.draw

        # The visible size of the texture.

        drawable = properties.get("drawable_resolution", True)

        if drawable:

            tw, th = draw.virt_to_draw.transform(cw, ch)

            tw = round(tw)
            th = round(th)

        else:

            tw = cw = round(cw)
            th = ch = round(ch)

        tw = min(tw, loader.max_texture_width)
        th = min(th, loader.max_texture_height)

        tw = max(tw, 1)
        th = max(th, 1)

        cw = max(cw, 1)
        ch = max(ch, 1)

        self.mesh = Mesh2.texture_rectangle(
            0.0, 0.0, cw, ch,
            0.0, 0.0, 1.0, 1.0,
            )

        cdef GLuint premultiplied

        glGenTextures(1, &premultiplied)

        # Bind the framebuffer.
        draw.change_fbo(draw.fbo)

        # Project the child from virtual space to the screen space.
        cdef Matrix transform
        transform = Matrix.ctexture_projection(cw, ch)

        self.allocate_texture(premultiplied, tw, th, properties)

        # Set up the viewport.
        glViewport(0, 0, tw, th)

        # Clear the screen.
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Set up the default modes.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        context = renpy.gl2.gl2draw.GL2DrawingContext(draw, tw, th)
        context.draw(what, transform)

        glBindTexture(GL_TEXTURE_2D, premultiplied)
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, tw, th, 0)

        self.mipmap_texture(premultiplied, tw, th, properties)

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
        cdef GLuint pixel_buffer

        if self.loaded:
            return

        draw = self.loader.draw

        s = PySurface_AsSurface(self.surface)

        # Generate the old textures.
        glGenTextures(1, &tex)
        glGenTextures(1, &premultiplied)

        # Bind the framebuffer.
        draw.change_fbo(draw.fbo)

        # Load the pixel data into tex, and set it up for drawing.
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)

        # Setup the non-premultiplied texture.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # Use a pixel buffer to create a texture.
        # Why use a Pixel Buffer? Apart from potentially being faster, this
        # works around a bug in Samsung android devices running Android 11,
        # where glTexImage2D doesn't seem to work when the pixels are not
        # aligned.

        # But it doesn't seem to work with ANGLE or emscripten, so we avoid using PBOs when
        # angle is in use.

        if not renpy.emscripten and not draw.angle:

            glGenBuffers(1, &pixel_buffer)
            glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pixel_buffer)
            glBufferData(GL_PIXEL_UNPACK_BUFFER, s.h * s.pitch, s.pixels, GL_STATIC_DRAW)
            glPixelStorei(GL_UNPACK_ROW_LENGTH, s.pitch // 4)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, <void *> 0)
            glUnmapBuffer(GL_PIXEL_UNPACK_BUFFER)
            glDeleteBuffers(1, &pixel_buffer)

        else:
            glPixelStorei(GL_UNPACK_ROW_LENGTH, s.pitch // 4)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, s.pixels)


        mesh = Mesh2.texture_rectangle(-1.0, -1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0)

        # Set up the viewport.
        glViewport(0, 0, self.width, self.height)

        # Set up the blend mode for premultiplication.
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ZERO, GL_ONE, GL_ZERO)

        # Draw.
        program = self.loader.ftl_program
        program.start()
        program.set_uniform("tex0", tex)
        program.draw(mesh, {})
        program.finish()

        # Create premultiplied.
        self.allocate_texture(premultiplied, self.width, self.height, self.properties)

        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, self.width, self.height, 0)

        self.mipmap_texture(premultiplied, self.width, self.height, self.properties)

        # Delete tex.
        glDeleteTextures(1, &tex)

        # Store the loaded texture.
        self.number = premultiplied
        self.loader.allocated.add(self.number)

        self.loaded = True
        self.surface = None

    def allocate_texture(GLTexture self, GLuint tex, int tw, int th, properties={}):
        """
        Allocates the VRAM required to store `tex`, which is a `tw` x `th`
        texture, including all mipmap levels.
        """

        # It's not 100% clear why we need this function, but it does seem to
        # significantly speed things up on my GeForce GTX 1060 3GB/PCIe/SSE2.
        # Going from a single to multiple mipmap levels takes ~9ms when loading
        # each mipmap, while allocating the space first reduces that to ~1ms.

        if self.has_mipmaps():
            self.loader.total_texture_size += int(self.width * self.height * 4 * 1.34)
        else:
            self.loader.total_texture_size += int(self.width * self.height * 4)

        glBindTexture(GL_TEXTURE_2D, tex)

        max_level = renpy.config.max_mipmap_level

        if not properties.get("mipmap", True):
            max_level = 0

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, max_level)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if max_level:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        wrap_s, wrap_t = properties.get("texture_wrap", (GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE))

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)

        if (not self.loader.draw.gles) and properties.get("anisotropic", True):
            glTexParameterf(GL_TEXTURE_2D, TEXTURE_MAX_ANISOTROPY_EXT, self.loader.max_anisotropy)

        # Store the texture size that was loaded.
        self.texture_width = tw
        self.texture_height = th

        cdef GLuint level = 0

        while True:

            glTexImage2D(GL_TEXTURE_2D, level, GL_RGBA, tw, th, 0, GL_RGBA, GL_UNSIGNED_BYTE, NULL);

            if tw == 1 and th == 1:
                break

            tw = max(tw >> 1, 1)
            th = max(th >> 1, 1)
            level += 1

            if level > max_level:
                break

    def mipmap_texture(GLTexture self, GLuint tex, int tw, int th, properties={}):
        """
        Generate the mipmaps for a texture.
        """

        cdef GLuint level = renpy.config.max_mipmap_level

        if not properties.get("mipmap", True):
            level = 0

        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, level)

        if level == 0:
            return

        if tw == 0 or th == 0:
            return

        glHint(GL_GENERATE_MIPMAP_HINT, GL_NICEST)
        glGenerateMipmap(GL_TEXTURE_2D)

    def __del__(self):
        try:
            if self.loaded:
                self.loader.free_list.append(self.number)

                if self.has_mipmaps():
                    self.loader.total_texture_size -= int(self.width * self.height * 4 * 1.34)
                else:
                    self.loader.total_texture_size -= int(self.width * self.height * 4)
        except TypeError:
            pass # Let's not error on shutdown.

    def load(self):
        self.load_gltexture()

    def program_uniforms(self, shader):
        shader.set_uniform("tex0", self)

    cpdef subsurface(self, rect):
        rv = GL2Model.subsurface(self, rect)
        if rv is not self:
            rv.uniforms = { "tex0" : self }
        return rv

class Texture(GLTexture):
    """
    Use a Python class to make  sure __del__ works.
    """

    pass
