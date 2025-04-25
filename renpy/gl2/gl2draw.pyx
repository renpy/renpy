#cython: profile=False
#@PydevCodeAnalysisIgnore
# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from libc.stdlib cimport malloc, free
from libc.math cimport roundf
from sdl2 cimport *
from renpy.uguu.gl cimport *
import renpy.gl2.gl2functions

from pygame_sdl2 cimport *
import_pygame_sdl2()

import renpy
import pygame_sdl2 as pygame
from pygame_sdl2 import Surface

import os
import os.path
import weakref
import array
import time
import math
import random

import renpy.uguu.gl as uguugl

cimport renpy.display.render as render
from renpy.display.render cimport Render, MATRIX_PROJECTION, MATRIX_VIEW, MATRIX_MODEL
from renpy.display.matrix cimport Matrix

cimport renpy.gl2.gl2texture as gl2texture

from renpy.gl2.gl2mesh cimport Mesh
from renpy.gl2.gl2mesh3 cimport Mesh3
from renpy.gl2.gl2polygon cimport Polygon
from renpy.gl2.gl2model cimport GL2Model

from renpy.gl2.gl2texture import Texture, TextureLoader
from renpy.gl2.gl2shadercache import ShaderCache

try:
    import emscripten
except ImportError:
    emscripten = None

# Cache various externals, so we can use them more efficiently.
cdef int DISSOLVE, IMAGEDISSOLVE, PIXELLATE
DISSOLVE = renpy.display.render.DISSOLVE
IMAGEDISSOLVE = renpy.display.render.IMAGEDISSOLVE
PIXELLATE = renpy.display.render.PIXELLATE

cdef Matrix IDENTITY
IDENTITY = renpy.display.render.IDENTITY

# Should we try to vsync?
vsync = True

# A list of frame end times, used for the same purpose.
frame_times = [ ]



cdef class GL2Draw:

    def __init__(self, name):

        # Are we in gles mode?
        self.gles = (name == "gles2") or (name == "angle2")

        # How about angle mode?
        self.angle = (name == "angle2")

        # The screen.
        self.window = None

        # The virtual size of the screen, as requested by the game.
        self.virtual_size = None

        # The physical size of the window we got.
        self.physical_size = None

        # The time of the last redraw.
        self.last_redraw_time = 0

        # The time between redraws.
        self.redraw_period = .2

        # Info.
        self.info = { "resizable" : True, "additive" : True, "renderer" : name, "models" : True }

        # We don't use a fullscreen surface, so this needs to be set
        # to None at all times.
        self.fullscreen_surface = None

        # The display info, from pygame.
        self.display_info = None

        # The DPI scale factor.
        self.dpi_scale = renpy.display.interface.dpi_scale

        # The number of frames to draw fast if the screen needs to be
        # updated.
        self.fast_redraw_frames = 0

        # The shader cache,
        self.shader_cache = None

        # Has the position of this window ever been set?
        self.ever_set_position = False

        # Was the window maximized the last time update was called?
        self.maximized = False

        # The old value of fullscreen.
        self.old_fullscreen = False

        # Should mipmaps be generated when mipmap == "auto"?
        self.auto_mipmap = False

    def get_texture_size(self):
        """
        Returns the amount of memory locked up in textures.
        """

        if self.texture_loader is None:
            return 0, 0

        return self.texture_loader.get_texture_size()

    def select_physical_size(self, physical_size):
        """
        *Internal* Determines the 'best' physical size to use, and returns
        it.
        """

        limit_physical_size = True

        if physical_size and renpy.game.preferences.window_position_layout == renpy.game.interface.get_display_layout():
            limit_physical_size = False

        # Are we maximized?
        old_surface = pygame.display.get_surface()
        if old_surface is not None:
            flags = old_surface.get_flags()
            maximized = (flags & pygame.WINDOW_MAXIMIZED) and not (flags & (pygame.WINDOW_FULLSCREEN|pygame.WINDOW_FULLSCREEN_DESKTOP))
        else:
            maximized = renpy.game.preferences.maximized

        # Information about the virtual size.
        vwidth, vheight = self.virtual_size
        virtual_ar = 1.0 * vwidth / vheight

        # The requested size.
        pwidth, pheight = physical_size

        if pwidth is None:
            pwidth = vwidth
            pheight = vheight

        # If a DPI scale is present, take it into account.
        pwidth *= self.dpi_scale
        pheight *= self.dpi_scale

        # Determine the visible area of the screen.
        info = renpy.display.get_info()

        visible_w = info.current_w
        visible_h = info.current_h

        # Determine the visible area of the current head.
        bounds = pygame.display.get_display_bounds(0)

        renpy.display.log.write("primary display bounds: %r", bounds)

        head_w = bounds[2] - 102
        head_h = bounds[3] - 102

        # Figure out the default window size.
        bound_w = min(visible_w, head_w)
        bound_h = min(visible_h, head_h)

        self.info["max_window_size"] = (
            round(min(bound_h * virtual_ar, bound_w)),
            round(min(bound_w / virtual_ar, bound_h)),
            )

        if (not renpy.mobile) and (not maximized):

            if limit_physical_size:

                # Limit to the visible area
                pwidth = min(visible_w, pwidth)
                pheight = min(visible_h, pheight)

                pwidth = min(pwidth, head_w)
                pheight = min(pheight, head_h)

            # Has to be a one-liner as the two values depend on each other.
            pwidth, pheight = min(pheight * virtual_ar, pwidth), min(pwidth / virtual_ar, pheight)

        # Limit to integers.
        pwidth = round(pwidth)
        pheight = round(pheight)

        # Keep a minimum size.
        pwidth = max(pwidth, 256)
        pheight = max(pheight, 256)

        return pwidth, pheight

    def select_framerate(self):
        """
        *Internal*
        This selects the framerate to use, the GL swap interval, and various
        other framerate-related intervals and parameters.
        """

        global vsync

        info = renpy.display.get_info()

        target_framerate = renpy.game.preferences.gl_framerate
        refresh_rate = info.refresh_rate

        if not refresh_rate:
            refresh_rate = 60

        if target_framerate is None:
            sync_frames = 1
        else:
            sync_frames = int(round(1.0 * refresh_rate) / target_framerate)
            if sync_frames < 1:
                sync_frames = 1

        if renpy.game.preferences.gl_tearing:
            sync_frames = -sync_frames

        vsync = int(os.environ.get("RENPY_GL_VSYNC", sync_frames))

        renpy.display.interface.frame_duration = 1.0 * abs(vsync) / refresh_rate

        renpy.display.log.write("swap interval: %r frames", vsync)

    def select_gl_attributes(self, gles):
        """
        *Internal*
        Selects the GL attributes and hints to use.
        """

        pygame.display.gl_reset_attributes()

        pygame.display.gl_set_attribute(pygame.GL_RED_SIZE, 8)
        pygame.display.gl_set_attribute(pygame.GL_GREEN_SIZE, 8)
        pygame.display.gl_set_attribute(pygame.GL_BLUE_SIZE, 8)
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

        if renpy.config.depth_size:
            pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, renpy.config.depth_size)

        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, vsync)

        if gles:
            pygame.display.hint("SDL_OPENGL_ES_DRIVER", "1")
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
        else:
            pygame.display.hint("SDL_OPENGL_ES_DRIVER", "0")
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)

        if renpy.config.gl_set_attributes is not None:
            renpy.config.gl_set_attributes()


    def get_window_position(self, physical_size=None):
        """
        Determines the position of the window, based on what's stored
        in preferences.

        The stored position is used only when the total display size hasn't
        changed, and the window would not overlap the edge of the screen.
        """

        default = (pygame.WINDOWPOS_CENTERED, pygame.WINDOWPOS_CENTERED)

        if "RENPY_CENTER_WINDOW" in os.environ:
            return default

        if renpy.display.interface.safe_mode:
            return default

        if not (renpy.linux or renpy.windows or renpy.macintosh):
            return default

        if not renpy.game.preferences.restore_window_position:
            return default

        layout = renpy.game.interface.get_display_layout()

        if renpy.game.preferences.window_position_layout != layout:
            return default

        pos = renpy.game.preferences.window_position

        for rect in layout:

            if pos[0] < rect[0] or pos[1] < rect[1]:
                continue

            if physical_size is not None:
                pwidth, pheight = physical_size
                if pos[0] + pwidth > rect[2] and pos[1] + pheight > rect[3]:
                    continue

            return pos

        return default

    def init(self, virtual_size):
        """
        This changes the video mode. It also initializes OpenGL, if it
        can. It returns True if it was successful, or False if OpenGL isn't
        working for some reason.
        """

        self.virtual_size = virtual_size
        vwidth, vheight = virtual_size

        global vsync

        if not renpy.config.gl_enable:
            renpy.display.log.write("GL Disabled.")
            return False

        if renpy.mobile:
            physical_size = (None, None)
        elif renpy.game.preferences.physical_size is None:
            physical_size = (renpy.config.physical_width, renpy.config.physical_height)
        else:
            physical_size = renpy.game.preferences.physical_size

        pwidth, pheight = self.select_physical_size(physical_size)

        if renpy.android or renpy.ios:
            fullscreen = True
        elif renpy.emscripten:
            fullscreen = False
        else:
            fullscreen = renpy.game.preferences.fullscreen

        # Handle swap control.
        target_framerate = renpy.game.preferences.gl_framerate
        refresh_rate = renpy.display.get_info().refresh_rate

        if not refresh_rate:
            refresh_rate = 60

        if target_framerate is None:
            sync_frames = 1
        else:
            sync_frames = int(round(1.0 * refresh_rate) / target_framerate)
            if sync_frames < 1:
                sync_frames = 1

        if renpy.game.preferences.gl_tearing:
            sync_frames = -sync_frames

        vsync = int(os.environ.get("RENPY_GL_VSYNC", sync_frames))

        renpy.display.interface.frame_duration = 1.0 * abs(vsync) / refresh_rate

        renpy.display.log.write("swap interval: %r frames", vsync)

        # Determine the GLES mode, the actual window size to request, and the
        # window flags to use. (These are platform dependent.)
        gles = self.gles
        window_flags = pygame.OPENGL | pygame.DOUBLEBUF

        if renpy.android:
            pwidth = 0
            pheight = 0
            gles = True

        elif renpy.ios:
            window_flags |= pygame.WINDOW_ALLOW_HIGHDPI | pygame.RESIZABLE
            pwidth = 0
            pheight = 0
            gles = True

        else:
            if self.dpi_scale == 1.0:
                window_flags |= pygame.WINDOW_ALLOW_HIGHDPI

            if renpy.config.gl_resize:
                window_flags |= pygame.RESIZABLE

        if renpy.config.gl2_modify_window_flags is not None:
            window_flags = renpy.config.gl2_modify_window_flags(window_flags)

        # Select the GL attributes and hints.
        self.select_gl_attributes(gles)

        # Opens the window.
        #
        # If we're in fullscreen, tries to get a fullscreen window. If that fails,
        # or fullscreen is False, tries to open a normal window.

        self.window = None

        if (self.window is None) and fullscreen:
            try:
                renpy.display.log.write("Fullscreen mode.")
                self.window = pygame.display.set_mode((0, 0), pygame.WINDOW_FULLSCREEN_DESKTOP | window_flags)
            except pygame.error as e:
                renpy.display.log.write("Opening in fullscreen failed: %r", e)
                self.window = None

        if self.window is None:

            if renpy.game.preferences.maximized:
                window_flags |= pygame.WINDOW_MAXIMIZED
                pos = (pygame.WINDOWPOS_UNDEFINED, pygame.WINDOWPOS_UNDEFINED)
            else:
                self.ever_set_position = True
                pos = self.get_window_position((pwidth, pheight))

            try:
                renpy.display.log.write("Windowed mode.")
                self.window = pygame.display.set_mode((pwidth, pheight), window_flags, pos=pos)
            except pygame.error as e:
                renpy.display.log.write("Could not get pygame screen: %r", e)
                return False

        # Initialize OpenGL.

        if "RENPY_FAIL_" + self.info["renderer"].upper() in os.environ:
            self.quit()
            return False

        if renpy.emscripten:
            emscripten.webgl_enable_extension("EXT_texture_filter_anisotropic")

        # Load uguu, and init GL.
        renpy.uguu.gl.clear_missing_functions()
        renpy.uguu.gl.load()
        if renpy.uguu.gl.check_missing_functions(renpy.gl2.gl2functions.required_functions):
            return False

        # Log the GL version.
        renderer = <char *> glGetString(GL_RENDERER)
        version = <char *> glGetString(GL_VERSION)

        renpy.display.log.write("Vendor: %r", str(<char *> glGetString(GL_VENDOR)))
        renpy.display.log.write("Renderer: %r", renderer)
        renpy.display.log.write("Version: %r", version)
        renpy.display.log.write("Display Info: %s", self.display_info)

        extensions_string = <char *> glGetString(GL_EXTENSIONS)
        extensions = set(extensions_string.decode("utf-8").split(" "))

        if renpy.config.log_gl_extensions:

            renpy.display.log.write("Extensions:")

            for i in sorted(extensions):
                renpy.display.log.write("    %s", i)

        # Do additional setup needed.
        renpy.display.pgrender.set_rgba_masks()

        if renpy.android or renpy.ios:
            self.redraw_period = 1.0

        elif renpy.emscripten:
            # give back control to browser regularly
            self.redraw_period = 0.1

        self.shader_cache = ShaderCache("cache/shaders.txt", self.gles)

        # Initialize the texture loader.
        self.texture_loader = TextureLoader(self)

        self.on_resize(first=True)

        return True

    def on_resize(self, first=False):

        if not first:
            self.quit_fbo()
            self.shader_cache.clear()

        if renpy.android or renpy.ios or renpy.emscripten:
            pygame.display.get_window().recreate_gl_context(always=renpy.emscripten)

        # Are we in fullscreen mode?
        if renpy.emscripten:
            fullscreen = bool(emscripten.run_script_int("isFullscreen()"))
        else:
            fullscreen = bool(pygame.display.get_window().get_window_flags() & (pygame.WINDOW_FULLSCREEN_DESKTOP | pygame.WINDOW_FULLSCREEN))

        # Are we maximized?
        maximized = bool(pygame.display.get_window().get_window_flags() & pygame.WINDOW_MAXIMIZED) and not fullscreen and renpy.config.gl_resize

        # See if we've ever set the screen position, and if not, center the window.
        if not fullscreen and not maximized and not self.ever_set_position and not renpy.emscripten:
            self.ever_set_position = True
            pygame.display.get_window().set_position(self.get_window_position())

        # Get the size of the created screen.
        pwidth, pheight = renpy.display.core.get_size()

        vwidth, vheight = self.virtual_size

        self.physical_size = (pwidth, pheight)
        self.drawable_size = pygame.display.get_drawable_size()

        renpy.display.log.write("Screen sizes: virtual=%r physical=%r drawable=%r" % (self.virtual_size, self.physical_size, self.drawable_size))

        # Update the preferences.
        renpy.game.preferences.fullscreen = fullscreen
        renpy.game.interface.fullscreen = fullscreen

        if not fullscreen:
            renpy.game.preferences.maximized = maximized

        if not fullscreen and not maximized:
            renpy.game.preferences.physical_size = self.get_physical_size()

        if renpy.config.adjust_view_size is not None:
            view_width, view_height = renpy.config.adjust_view_size(pwidth, pheight)
        else:

            # Figure out the virtual box, which includes padding around
            # the borders.
            physical_ar = 1.0 * pwidth / pheight

            ratio = min(1.0 * pwidth / vwidth, 1.0 * pheight / vheight)

            view_width = max(int(vwidth * ratio), 1)
            view_height = max(int(vheight * ratio), 1)

        px_padding = pwidth - view_width
        py_padding = pheight - view_height

        x_padding = px_padding * vwidth / view_width
        y_padding = py_padding * vheight / view_height

        # The position of the physical screen, in virtual pixels
        # (x, y, w, h). Since the physical screen will always contain
        # the virtual screen, the corners are often off the virtual
        # screen.
        self.virtual_box = (
            -x_padding / 2.0,
            -y_padding / 2.0,
             vwidth + x_padding,
             vheight + y_padding)

        # The location of the virtual screen on the physical screen, in
        # physical pixels.
        self.physical_box = (
            px_padding / 2,
            py_padding / 2,
            pwidth - px_padding,
            pheight - py_padding,
            )

        # The scaling factor of physical_pixels to drawable pixels.
        self.draw_per_phys = 1.0 * self.drawable_size[0] / self.physical_size[0]

        # The location of the viewport, in drawable pixels.
        self.drawable_viewport = tuple(i * self.draw_per_phys for i in self.physical_box)

        dwidth = self.drawable_viewport[2]
        dheight = self.drawable_viewport[3]

        # How many drawable pixels there are per virtual pixel?
        self.draw_per_virt = 1.0 * self.drawable_viewport[2] / vwidth

        # Matrices that transform from virtual space to drawable space, and vice versa.
        self.virt_to_draw = Matrix2D(1.0 * dwidth / vwidth, 0, 0, 1.0 * dheight / vheight)
        self.draw_to_virt = Matrix2D(1.0 * vwidth / dwidth, 0, 0, 1.0 * vheight / dheight)

        self.draw_transform = Matrix.cscreen_projection(self.drawable_viewport[2], self.drawable_viewport[3])

        self.shader_cache.load()
        self.init_fbo()
        self.texture_loader.init()

        self.auto_mipmap = self.draw_per_virt < 0.75

    def resize(self):
        """
        Documented in renderer.
        """

        fullscreen = renpy.game.preferences.fullscreen

        if renpy.emscripten:
            fullscreen = False
        elif renpy.android or renpy.ios:
            fullscreen = True

        if renpy.game.preferences.physical_size:
            width = renpy.game.preferences.physical_size[0] or self.virtual_size[0]
            height = renpy.game.preferences.physical_size[1] or self.virtual_size[1]
        else:
            width = self.virtual_size[0]
            height = self.virtual_size[1]

        width *= self.dpi_scale
        height *= self.dpi_scale

        if not renpy.android or renpy.ios or renpy.emscripten:
            max_w, max_h = self.info["max_window_size"]
            width = min(width, max_w)
            height = min(height, max_h)

        width = max(width, 256)
        height = max(height, 256)

        if fullscreen:
            maximized = False
        else:
            maximized = renpy.game.preferences.maximized

        pygame.display.get_window().resize((width, height), opengl=True, fullscreen=fullscreen, maximized=maximized)

    def update(self, force=False):
        """
        Documented in renderer.
        """

        flags = pygame.display.get_window().get_window_flags()

        if renpy.emscripten:
            fullscreen = bool(emscripten.run_script_int("isFullscreen()"))
        else:
            fullscreen = bool(flags & (pygame.WINDOW_FULLSCREEN_DESKTOP | pygame.WINDOW_FULLSCREEN))

        maximized = bool(flags & pygame.WINDOW_MAXIMIZED)

        size = renpy.display.core.get_size()
        drawable_size = pygame.display.get_drawable_size()

        if (
            (force) or
            (fullscreen != renpy.display.interface.fullscreen) or
            (size != self.physical_size) or
            (drawable_size != self.drawable_size) or
            (self.maximized != maximized)
        ):

            self.maximized = maximized
            renpy.display.interface.before_resize()
            self.on_resize()

            return True
        else:
            return False

    def quit(GL2Draw self):
        """
        Called when terminating the use of the OpenGL context.
        """

        self.kill_textures()

        if self.texture_loader is not None:
            self.texture_loader.quit()
            self.texture_loader = None

        self.quit_fbo()

        if self.shader_cache is not None:
            self.shader_cache.save()


    cdef void change_fbo(self, GLuint fbo):
        """
        *Internal*
        Change the FBO.
        """
        if self.current_fbo != fbo:
            glBindFramebuffer(GL_FRAMEBUFFER, fbo)
            self.current_fbo = fbo



    def init_fbo(GL2Draw self):
        """
        *Internal*
        Create the FBO.
        """

        # Determine the width and height of textures and the renderbuffer.
        cdef GLint max_renderbuffer_size
        cdef GLint max_texture_size

        # Store the default FBO.
        glGetIntegerv(GL_FRAMEBUFFER_BINDING, <GLint *> &self.default_fbo);
        self.current_fbo = self.default_fbo

        # Store the default RBO
        cdef GLuint default_renderbuffer
        glGetIntegerv(GL_RENDERBUFFER_BINDING, <GLint *> &default_renderbuffer);

        # Generate the framebuffer.
        glGenFramebuffers(1, &self.fbo)
        glGenFramebuffers(1, &self.fbo_1px)

        glGenRenderbuffers(1, &self.color_renderbuffer)
        glGenRenderbuffers(1, &self.color_renderbuffer_1px)

        if renpy.config.depth_size:
            glGenRenderbuffers(1, &self.depth_renderbuffer)
            glGenRenderbuffers(1, &self.depth_renderbuffer_1px)

        glGetIntegerv(GL_MAX_TEXTURE_SIZE, &max_texture_size)
        glGetIntegerv(GL_MAX_RENDERBUFFER_SIZE, &max_renderbuffer_size)

        max_texture_size = max(max_texture_size, 1024)
        max_renderbuffer_size = max(max_renderbuffer_size, 1024)

        # The number of pixels of additional border, so we can load textures with
        # higher pitch.
        BORDER = 64

        width, height = renpy.config.max_texture_size

        width = max(self.virtual_size[0] + BORDER, self.drawable_size[0] + BORDER, width)
        width = min(width, max_texture_size, max_renderbuffer_size)
        height = max(self.virtual_size[1] + BORDER, self.drawable_size[1] + BORDER, height)
        height = min(height, max_texture_size, max_renderbuffer_size)

        if "RENPY_MAX_TEXTURE_SIZE" in os.environ:
            width = height = int(os.environ["RENPY_MAX_TEXTURE_SIZE"])

        renpy.display.log.write("Maximum texture size: %dx%d", width, height)

        self.texture_loader.max_texture_width = width
        self.texture_loader.max_texture_height = height

        # Full-size fbo.
        self.change_fbo(self.fbo)

        glBindRenderbuffer(GL_RENDERBUFFER, self.color_renderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8, width, height)

        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER,
            GL_COLOR_ATTACHMENT0,
            GL_RENDERBUFFER,
            self.color_renderbuffer)

        if renpy.config.depth_size:

            glBindRenderbuffer(GL_RENDERBUFFER, self.depth_renderbuffer)

            if self.gles:
                if renpy.config.depth_size >= 24:
                    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)
                else:
                    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, width, height)

            else:
                glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)

            glFramebufferRenderbuffer(
                GL_FRAMEBUFFER,
                GL_DEPTH_ATTACHMENT,
                GL_RENDERBUFFER,
                self.depth_renderbuffer)

        # 1px fbo.
        self.change_fbo(self.fbo_1px)

        glBindRenderbuffer(GL_RENDERBUFFER, self.color_renderbuffer_1px)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8,  1, 1)

        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER,
            GL_COLOR_ATTACHMENT0,
            GL_RENDERBUFFER,
            self.color_renderbuffer_1px)

        if renpy.config.depth_size:

            glBindRenderbuffer(GL_RENDERBUFFER, self.depth_renderbuffer_1px)

            if self.gles:
                if renpy.config.depth_size >= 24:
                    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, 1, 1)
                else:
                    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, 1, 1)

            else:
                glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, 1, 1)

            glFramebufferRenderbuffer(
                GL_FRAMEBUFFER,
                GL_DEPTH_ATTACHMENT,
                GL_RENDERBUFFER,
                self.depth_renderbuffer_1px)

        glBindRenderbuffer(GL_RENDERBUFFER, default_renderbuffer)
        self.change_fbo(self.default_fbo)


    def quit_fbo(GL2Draw self):

        self.change_fbo(self.default_fbo)

        # Full-size fbo.
        glDeleteFramebuffers(1, &self.fbo)
        glDeleteRenderbuffers(1, &self.color_renderbuffer)

        if renpy.config.depth_size:
            glDeleteRenderbuffers(1, &self.depth_renderbuffer)

        # 1px fbo.
        glDeleteFramebuffers(1, &self.fbo_1px)
        glDeleteRenderbuffers(1, &self.color_renderbuffer_1px)

        if renpy.config.depth_size:
            glDeleteRenderbuffers(1, &self.depth_renderbuffer_1px)


    def can_block(self):
        """
        Returns True if we can block to wait for input, False if the screen
        needs to be immediately redrawn.
        """

        powersave = renpy.game.preferences.gl_powersave

        if not powersave:
            return False

        return not self.fast_redraw_frames

    def should_redraw(self, needs_redraw, first_pass, can_block):
        """
        Redraw whenever the screen needs it, but at least once every
        .2 seconds. We rely on VSYNC to slow down our maximum
        draw speed.
        """

        rv = False

        if needs_redraw:
            rv = True
        elif first_pass:
            rv = True

        # Handle fast redraw.
        if rv:
            self.fast_redraw_frames = renpy.config.fast_redraw_frames
        elif self.fast_redraw_frames > 0:
            self.fast_redraw_frames -= 1
            rv = True

        if time.time() > self.last_redraw_time + self.redraw_period:
            rv = True

        # Store the redraw time.
        if rv or (not can_block):
            self.last_redraw_time = time.time()
            return True
        else:
            return False

    def mutated_surface(self, surf):
        return

    def load_texture(self, surf, transient=False, properties={}):
        """
        Loads a texture into memory.
        """

        return self.texture_loader.load_surface(surf, properties)

    def ready_one_texture(self):
        """
        Call from the main thread to make a single texture ready.
        """

        if self.texture_loader is None:
            return False

        return self.texture_loader.ready_one_texture()

    def solid_texture(self, w, h, color):
        """
        Returns a texture that represents a solid color.
        """

        mesh = Mesh3.rectangle(0, 0, w, h)

        a = color[3] / 255.0
        r = a * color[0] / 255.0
        g = a * color[1] / 255.0
        b = a * color[2] / 255.0

        color = (r, g, b, a)

        return GL2Model((w, h), mesh, ("renpy.solid", ), { "u_renpy_solid_color" : color })

    def flip(self):
        """
        Called to flip the screen after it's drawn.
        """

        start = time.time()

        renpy.plog(1, "flip")

        try:
            pygame.display.flip()
        except pygame.error as e:
            renpy.display.log.write("Flip failed %r", e)
            renpy.game.interface.display_reset = True

        end = time.time()

        if vsync:

            # When the window is covered, we can get into a state where no
            # drawing occurs and everything goes fast. Detect that and
            # sleep.

            frame_times.append(end)

            if len(frame_times) > 10:
                frame_times.pop(0)

                # If we're running at over 1000 fps, vsync is broken.
                if (frame_times[-1] - frame_times[0] < .001 * 10):
                    time.sleep(1.0 / 120.0)
                    renpy.plog(1, "after broken vsync sleep")


    def draw_screen(self, render_tree, flip=True, screenshot=False):
        """
        Draws the screen.
        """

        renpy.plog(1, "start draw_screen")

        if renpy.display.video.fullscreen:
            surf = renpy.display.video.render_movie("movie", self.virtual_size[0], self.virtual_size[1])
        else:
            surf = render_tree

        if surf is None:
            return

        # Load all the textures and RTTs.
        self.load_all_textures(surf)

        # Switch to the right FBO, and the right viewport.
        if screenshot:
            self.change_fbo(self.fbo)
        else:
            self.change_fbo(self.default_fbo)

        # Set up the viewport.
        if screenshot:
            x = 0
            y = 0
            w = surf.width * self.draw_per_virt
            h = surf.height * self.draw_per_virt
        else:
            x, y, w, h = self.drawable_viewport

        glViewport(x, y, w, h)

        # Clear the screen.
        clear_r, clear_g, clear_b = renpy.color.Color(renpy.config.gl_clear_color).rgb
        glClearColor(clear_r, clear_g, clear_b, 0.0 if screenshot else 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Project the child from virtual space to the screen space.
        cdef Matrix transform
        if screenshot:
            transform = Matrix.cscreen_projection(surf.width, surf.height)
        else:
            transform = Matrix.cscreen_projection(self.virtual_size[0], self.virtual_size[1])

        # Set up the default modes.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        # Use the context to draw the render tree.
        draw_render(surf, w, h, transform)

        if flip:
            self.flip()
            self.texture_loader.cleanup()

    def load_all_textures(self, what):
        """
        This loads all textures from the surface tree before drawing to
        the actual framebuffer. This is responsible for walking the
        surface tree, and loading framebuffers and texture.
        """

        if isinstance(what, Surface):
            what = self.load_texture(what)
            self.load_all_textures(what)
            return

        if isinstance(what, GL2Model):
            what.load()
            return

        # what is a Render.

        cdef Render r = what
        cdef GL2Model model
        cdef int i

        if r.loaded:
            return

        r.loaded = True

        # Load the child textures.
        for c in r.children:
            self.load_all_textures(c[0])

        # This needs to be outside of r.mesh, as it handles all uniform texture loading,
        # even if uniforms isn't used.
        # If we have a mesh (or mesh=True), create the GL2Model.
        if r.mesh:

            if (r.mesh is True) and (not r.children):
                return

            if not r.uniforms:
                uniforms = None

            elif r.uniforms_has_render:

                uniforms = dict()

                for k, v in r.uniforms.items():
                    if isinstance(v, Render):
                        self.load_all_textures(v)
                        uniforms[k] = ctex = self.render_to_texture(v, properties=r.properties)
                        uniforms.setdefault(k + "_res", (ctex.texture_width, ctex.texture_height))
                    else:
                        uniforms[k] = v
            else:
                uniforms = r.uniforms

            model = r.cached_model = GL2Model(
                (r.width, r.height),
                None,
                r.shaders,
                uniforms)

            for i, c in enumerate(r.children):
                model.set_texture(i, self.render_to_texture(c[0], properties=r.properties))

            if r.mesh is True:
                model.mesh = model.get_texture(0).mesh
            else:
                model.mesh = r.mesh

            r.cached_model.properties = r.properties

        elif r.uniforms_has_render:
            for v in r.uniforms.values():
                if isinstance(v, Render):
                    self.load_all_textures(v)
                    self.render_to_texture(v, properties=r.properties)

    def render_to_texture(self, what, alpha=True, properties={}):
        """
        Renders `what` to a texture. The texture will have the drawable
        size of `what`.
        """

        if properties is None:
            properties = {}

        if isinstance(what, Surface):
            what = self.load_texture(what)
            self.load_all_textures(what)

        if isinstance(what, Texture):
            return what

        if what.cached_texture is not None:
            return what.cached_texture

        rv = self.texture_loader.render_to_texture(what, properties)
        what.cached_texture = rv

        return rv

    def is_pixel_opaque(self, what):
        """
        Returns true if the pixel is not 100% transparent.

        `what`
            A 1x1 Render.
        """

        # Load all the textures and RTTs.
        self.load_all_textures(what)

        # Switch to the right FBO, and the right viewport.
        self.change_fbo(self.fbo_1px)

        # Set up the viewport.
        glViewport(0, 0, 1, 1)

        # Clear the screen.
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Project the child from virtual space to the screen space.
        cdef Matrix transform
        transform = renpy.display.render.IDENTITY
        transform = Matrix.cscreen_projection(1, 1)

        # Set up the default modes.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        # Use the context to draw the surface tree.
        draw_render(what, 1, 1, transform)

        cdef unsigned char pixel[4]
        glReadPixels(0, 0, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, pixel)

        return pixel[3]


    def translate_point(self, x, y):
        """
        Translates (x, y) from physical to virtual coordinates.
        """

        # Screen sizes.
        pw, ph = self.physical_size
        vw, vh = self.virtual_size
        vx, vy, vbw, vbh = self.virtual_box

        # Translate to fractional screen.
        x = 1.0 * x / pw
        y = 1.0 * y / ph

        # Translate to virtual size.
        x = vx + vbw * x
        y = vy + vbh * y

        x = int(x)
        y = int(y)

        return x, y

    def untranslate_point(self, x, y):
        """
        Untranslates (x, y) from virtual to physical coordinates.
        """

        # Screen sizes.
        pw, ph = self.physical_size
        vx, vy, vbw, vbh = self.virtual_box

        # Translate from virtual to fractional screen.
        x = ( x - vx ) / vbw
        y = ( y - vy ) / vbh

        # Translate from fractional screen to physical.
        x = x * pw
        y = y * ph

        x = int(x)
        y = int(y)

        return x, y

    def mouse_event(self, ev):
        x, y = getattr(ev, 'pos', pygame.mouse.get_pos())
        return self.translate_point(x, y)

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return self.translate_point(x, y)

    def set_mouse_pos(self, x, y):
        x, y = self.untranslate_point(x, y)
        pygame.mouse.set_pos([x, y])

    def screenshot(self, render_tree):
        cdef unsigned char *pixels
        cdef SDL_Surface *surf

        cdef unsigned char *raw_pixels
        cdef unsigned char *rpp
        cdef int x, y, pitch

        if render_tree is not None:
            sw = render_tree.width * self.draw_per_virt
            sh = render_tree.height * self.draw_per_virt
        else:
            sw, sh = self.drawable_size

        full = renpy.display.pgrender.surface_unscaled((sw, sh), True)
        surf = PySurface_AsSurface(full)

        # Create an array that can hold densely-packed pixels.
        raw_pixels = <unsigned char *> malloc(surf.w * surf.h * 4)

        # Draw the last screen to the back buffer.
        if render_tree is not None:
            self.draw_screen(render_tree, flip=False, screenshot=True)
            glFinish()

        # Read the pixels.
        glReadPixels(
            0,
            0,
            surf.w,
            surf.h,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            raw_pixels)

        # Copy the pixels from raw_pixels to the surface.
        pixels = <unsigned char *> surf.pixels
        pitch = surf.pitch
        rpp = raw_pixels

        cdef unsigned char r
        cdef unsigned char g
        cdef unsigned char b
        cdef unsigned char a

        with nogil:
            for y in range(surf.h):
                for x in range(surf.w):
                    r = rpp[x * 4 + 0]
                    g = rpp[x * 4 + 1]
                    b = rpp[x * 4 + 2]
                    a = rpp[x * 4 + 3]

                    if 0 < a < 255:
                        r = r * 255 // a
                        g = g * 255 // a
                        b = b * 255 // a

                    pixels[x * 4 + 0] = r
                    pixels[x * 4 + 1] = g
                    pixels[x * 4 + 2] = b
                    pixels[x * 4 + 3] = a

                pixels += pitch
                rpp += surf.w * 4

        free(raw_pixels)

        rv = renpy.display.pgrender.flip_unscaled(full, False, True)

        return rv

    def kill_textures(self):
        if self.texture_loader is not None:
            self.texture_loader.cleanup()

    def event_peek_sleep(self):
        pass

    def get_physical_size(self):
        x, y = self.physical_size

        x = int(x / self.dpi_scale)
        y = int(y / self.dpi_scale)

        return (x, y)


cdef class GL2DrawingContext:
    """
    This is an object that represents the state of the GL rendering
    system. It's responsible for walking the tree of Renders and
    TextureMeshes, updating its state as appropriate. When it hits
    a node where drawing is involved, it's responsible for issuing
    the appropriate draw calls to OpenGL, using the saved state.
    """

    def __init__(self):
        # Most initialization is done in draw_render, below.
        self.projection_matrix = Matrix(None)
        self.view_matrix = Matrix(None)
        self.projectionview_matrix = Matrix(None)
        self.model_matrix = Matrix(None)

    cdef GL2DrawingContext child_context(self):
        """
        Returns the child GL2DrawingContext, with its fields and matrices
        having the same values as this GL2DrawingContex.
        """

        cdef GL2DrawingContext rv

        rv = self._child_context
        if rv is None:
            rv = GL2DrawingContext()
            self._child_context = rv

        rv.width = self.width
        rv.height = self.height
        rv.debug = self.debug

        rv.projection_matrix.ctake(self.projection_matrix)
        rv.view_matrix.ctake(self.view_matrix)
        rv.projectionview_matrix.ctake(self.projectionview_matrix)
        rv.model_matrix.ctake(self.model_matrix)

        rv.clip_polygon = self.clip_polygon

        rv.shaders = self.shaders
        rv.uniforms = self.uniforms
        rv.properties = self.properties

        rv.pixel_perfect = self.pixel_perfect
        rv.has_depth = self.has_depth

        return rv

    cdef dict merge_properties(self, dict old, dict child):
        """
        Merges the child properties into the old properties,
        returning new properties.
        """

        rv = dict(old)

        if not child:
            return rv

        rv.update(child)

        rv.pop("depth", None)
        rv.pop("pixel_perfect", None)
        return rv

    cdef void correct_pixel_perfect(self):
        """
        Computes an offset for the projection transform such that the (0, 0) pixel
        is aligned with a drawable pixel.
        """

        cdef float halfwidth
        cdef float halfheight

        cdef float sx, sy, sz, sw

        halfwidth = self.width / 2.0
        halfheight = self.height / 2.0

        sx = 0
        sy = 0
        sz = 0
        sw = 1

        self.model_matrix.transform4(&sx, &sy, &sz, &sw, sx, sy, sz, sw)
        self.view_matrix.transform4(&sx, &sy, &sz, &sw, sx, sy, sz, sw)
        self.projection_matrix.transform4(&sx, &sy, &sz, &sw, sx, sy, sz, sw)

        sx = roundf(sx * 10000) / 10000
        sy = roundf(sy * 10000) / 10000

        sx = sx * halfwidth + halfwidth
        sy = sy * halfheight + halfheight

        cdef float xoff = roundf(sx) - sx
        cdef float yoff = roundf(sy) - sy

        self.projection_matrix.inplace_reverse_offset(xoff / halfwidth, yoff / halfheight)
        self.projectionview_matrix.ctake(self.projection_matrix)
        self.projectionview_matrix.inplace_multiply(self.view_matrix)

    cdef object draw_model(self, model):

        cdef GL2Draw gl2draw = renpy.display.draw
        cdef Mesh mesh = model.mesh

        # If a clip polygon is in place, clip the mesh with it.
        if self.clip_polygon is not None:

            if model.reverse is not IDENTITY:
                self.clip_polygon = self.clip_polygon.multiply_matrix(model.forward)

            mesh = mesh.crop(self.clip_polygon)

        if not mesh.triangles:
            return

        if model.properties:
            self.properties = self.merge_properties(self.properties, model.properties)

        if model.reverse is not IDENTITY:
            self.model_matrix.inplace_multiply(model.reverse)

        if model.shaders:
            self.shaders = self.shaders + model.shaders

        if model.uniforms:
            uniforms = dict(model.uniforms)
            uniforms.update(self.uniforms)
            self.uniforms = uniforms

        if self.debug:
            import renpy.gl2.gl2debug as gl2debug
            gl2debug.geometry(mesh, self.model_matrix, self.width, self.height)

        program = gl2draw.shader_cache.get(self.shaders)

        program.draw(self, model, mesh)

    cdef void set_text_rect(self, Render r):
        """
        Sets the text rect.
        """

        cdef:
            int wvirt
            int hvirt

            float x0
            float y0
            float x1
            float y1

            float xmin
            float xmax
            float ymin
            float ymax

            Matrix tovirt

        wvirt, hvirt = renpy.display.draw.virtual_size

        tovirt = Matrix.cscreen_projection(wvirt, hvirt).inverse() * self.projection_matrix * self.view_matrix * self.model_matrix

        x0, y0 = tovirt.transform(0, 0)
        x1, y1 = tovirt.transform(r.width, r.height)

        xmin = min(x0, x1)
        xmax = max(x0, x1)
        ymin = min(y0, y1)
        ymax = max(y0, y1)

        renpy.display.interface.text_rect = (xmin, ymin, xmax - xmin, ymax - ymin)

    cdef object draw_one(self, what):
        """
        This is responsible for walking the surface tree, and drawing any
        GL2Models, Renders, and Surfaces it encounters.

        `transform`
            The matrix that transforms texture space into drawable space.

        `clip_polygon`
            The polygon used to clip children, if known.

        `shaders`
            A tuple giving the shaders to use.

        `uniforms`
            A dictionary of uniforms.

        `properties`
            Various properties that control how things are drawn, that are updated
            and passed to the shader.
        """

        cdef GL2DrawingContext ctx
        cdef Polygon new_clip_polygon
        cdef bint has_reverse

        if what.__class__ is not Render:

            if isinstance(what, GL2Model):
                ctx = self.child_context()
                ctx.draw_model(what)
                return

            if isinstance(what, Surface):
                what = (<GL2Draw> renpy.display.draw).load_texture(what)

        cdef Render r = what

        if r.text_input:
            # Allocate memory with a call price.
            self.set_text_rect(r)

        # Handle clipping.
        if (r.xclipping or r.yclipping):
            new_clip_polygon = Polygon.rectangle(0, 0, r.width, r.height)

            if self.clip_polygon is not None:
                clip_polygon = new_clip_polygon.intersect(self.clip_polygon)
                if clip_polygon is None:
                    return
            else:
                self.clip_polygon = new_clip_polygon

        has_reverse = (r.reverse is not None) and (r.reverse is not IDENTITY)
        has_depth = False

        if r.properties:

            self.properties = self.merge_properties(self.properties, r.properties)

            if r.properties.get("pixel_perfect", False) and self.pixel_perfect:
                self.correct_pixel_perfect()
                self.pixel_perfect = False

            has_depth = not self.has_depth and r.properties.get("depth", False)

            if has_depth:
                glClear(GL_DEPTH_BUFFER_BIT)
                glEnable(GL_DEPTH_TEST)
                glDepthFunc(GL_LEQUAL)

                self.has_depth = True

        if has_reverse:
            self.pixel_perfect = False

        if r.shaders is not None:
            self.shaders = self.shaders + r.shaders

        children = r.children

        if r.cached_model is not None:
            children = [ (r.cached_model, 0, 0, False, False) ]
        else:
            if r.uniforms is not None:
                self.uniforms = dict(self.uniforms)

                for k, v in r.uniforms.items():
                    if (k in self.uniforms) and (k in renpy.config.merge_uniforms):
                        self.uniforms[k] = renpy.config.merge_uniforms[k](self.uniforms[k], v)
                    else:
                        self.uniforms[k] = v

        for child, cx, cy, focus, main in children:

            ctx = self.child_context()

            if (cx or cy):
                if type(cx) is not int:
                    ctx.pixel_perfect = False

                ctx.model_matrix.inplace_offset(cx, cy)

                if ctx.clip_polygon is not None:
                    ctx.clip_polygon = ctx.clip_polygon.offset(-cx, -cy)

            if has_reverse:
                ctx.model_matrix.inplace_multiply(r.reverse)

                if r.matrix_kind == MATRIX_PROJECTION:
                    ctx.projection_matrix.inplace_multiply(ctx.view_matrix)
                    ctx.projection_matrix.inplace_multiply(ctx.model_matrix)

                    ctx.view_matrix.ctake(IDENTITY)
                    ctx.model_matrix.ctake(IDENTITY)

                    ctx.projectionview_matrix.ctake(ctx.projection_matrix)

                elif r.matrix_kind == MATRIX_VIEW:
                    ctx.view_matrix.inplace_multiply(ctx.model_matrix)
                    ctx.model_matrix.ctake(IDENTITY)

                    ctx.projectionview_matrix.ctake(ctx.projection_matrix)
                    ctx.projectionview_matrix.inplace_multiply(ctx.view_matrix)

                if ctx.clip_polygon is not None:
                    ctx.clip_polygon = ctx.clip_polygon.multiply_matrix(r.forward)

            ctx.draw_one(child)

        if has_depth:
            glDisable(GL_DEPTH_TEST)

        return 0


# The root of allocated linked list of GL2DrawingContexts.
root_context = GL2DrawingContext()


def draw_render(what, int drawable_width, int drawable_height, Matrix projection):
    """
    Renders `what` to the current OpenGL context.

    `what`
        The object to draw. This is usually a Render, but can be a
        GL2Model or a Surface.

    `drawable_width`
        The width of the drawable area, in pixels.

    `drawable_height`
        The height of the drawable area, in pixels.

    `projection`
        The projection matrix to use to transform from view space
        to the viewport.
    """

    cdef GL2DrawingContext ctx = root_context

    ctx.width = drawable_width
    ctx.height = drawable_height
    ctx.debug = False

    ctx.projection_matrix.ctake(projection)
    ctx.view_matrix.ctake(IDENTITY)
    ctx.projectionview_matrix.ctake(projection)
    ctx.model_matrix.ctake(IDENTITY)

    ctx.shaders = ()
    ctx.uniforms = { }
    ctx.properties = { }

    ctx.clip_polygon = None
    ctx.pixel_perfect = True

    if renpy.config.nearest_neighbor:
        ctx.properties["texture_scaling"] = "nearest"

    ctx.draw_one(what)

    while ctx is not None:
        ctx.uniforms.clear()
        ctx.properties.clear()

        ctx = ctx._child_context



# A set of uniforms that are defined by Ren'Py, and shouldn't be set in ATL.
standard_uniforms = { "u_transform", "u_projection", "u_view", "u_projectionview", "u_model", "u_time", "u_random", "u_drawable_size" }


_types = """
standard_uniforms : set[str]
"""
