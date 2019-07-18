#cython: profile=False
#@PydevCodeAnalysisIgnore
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

from libc.stdlib cimport malloc, free
from sdl2 cimport *
from uguugl cimport *

from pygame_sdl2 cimport *
import_pygame_sdl2()

import renpy
import pygame_sdl2 as pygame
import os
import os.path
import weakref
import array
import time
import math

import uguugl

cimport renpy.display.render as render
from renpy.display.render cimport Render
from renpy.display.matrix cimport Matrix
from renpy.display.matrix import offset

cimport renpy.gl2.gl2texture as gl2texture
import renpy.gl2.gl2texture as gl2texture
import renpy.gl2.gl2geometry as gl2geometry

from renpy.gl2.gl2geometry import Mesh
from renpy.gl2.gl2texture import TexturedMesh, TextureLoader
from renpy.gl2.gl2shadercache import ShaderCache


# Cache various externals, so we can use them more efficiently.
cdef int DISSOLVE, IMAGEDISSOLVE, PIXELLATE
DISSOLVE = renpy.display.render.DISSOLVE
IMAGEDISSOLVE = renpy.display.render.IMAGEDISSOLVE
PIXELLATE = renpy.display.render.PIXELLATE

cdef object IDENTITY
IDENTITY = renpy.display.render.IDENTITY

# Should we try to vsync?
vsync = True

# A list of frame end times, used for the same purpose.
frame_times = [ ]


logo = None


cdef class GL2Draw:

    def __init__(self, renderer_name, gles):

        # Should we use gles or opengl?
        self.gles = gles

        # Did we do the first-time init?
        self.did_init = False

        # The screen.
        self.window = None

        # The virtual size of the screen, as requested by the game.
        self.virtual_size = None

        # The physical size of the window we got.
        self.physical_size = None

        # Is the mouse currently visible?
        self.mouse_old_visible = None

        # The (x, y) and texture of the software mouse.
        self.mouse_info = (0, 0, None)

        # This is used to cache the surface->texture operation.
        self.texture_cache = weakref.WeakKeyDictionary()

        # The time of the last redraw.
        self.last_redraw_time = 0

        # The time between redraws.
        self.redraw_period = .2

        # Info.
        self.info = { "resizable" : True, "additive" : True, "renderer" : renderer_name }

        # The old value of the fullscreen preference.
        self.old_fullscreen = None

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


    def get_texture_size(self):
        """
        Returns the amount of memory locked up in textures.
        """

        return self.texture_loader.total_texture_size, self.texture_loader.texture_count

    def select_physical_size(self, physical_size):
        """
        *Internal* Determines the 'best' physical size to use, and returns
        it.
        """

        # Are we maximized?
        old_surface = pygame.display.get_surface()
        if old_surface is not None:
            maximized = old_surface.get_flags() & pygame.WINDOW_MAXIMIZED
        else:
            maximized = False

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

        if renpy.windows and renpy.windows <= (6, 1):
            visible_h -= 102

        # Determine the visible area of the current head.
        bounds = pygame.display.get_display_bounds(0)

        renpy.display.log.write("primary display bounds: %r", bounds)

        head_full_w = bounds[2]
        head_w = bounds[2] - 102
        head_h = bounds[3] - 102

        # Figure out the default window size.
        bound_w = min(vwidth, visible_w, head_w)
        bound_h = min(vwidth, visible_h, head_h)

        self.info["max_window_size"] = (
            int(round(min(bound_h * virtual_ar, bound_w))),
            int(round(min(bound_w / virtual_ar, bound_h))),
            )

        if (not renpy.mobile) and (not maximized):

            # Limit to the visible area
            pwidth = min(visible_w, pwidth)
            pheight = min(visible_h, pheight)

            # The first time through, constrain the aspect ratio.
            if not self.did_init:
                pwidth = min(pwidth, head_w)
                pheight = min(pheight, head_h)

                pwidth, pheight = min(pheight * virtual_ar, pwidth), min(pwidth / virtual_ar, pheight)

        # Limit to integers.
        pwidth = int(round(pwidth))
        pheight = int(round(pheight))

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

        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, vsync)

        if gles:
            pygame.display.hint("SDL_OPENGL_ES_DRIVER", "1")
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
        else:
            pygame.display.hint("SDL_OPENGL_ES_DRIVER", "0")

    def set_mode(self, virtual_size, physical_size, fullscreen):
        """
        This changes the video mode. It also initializes OpenGL, if it
        can. It returns True if it was successful, or False if OpenGL isn't
        working for some reason.
        """

        if not renpy.config.gl_enable:
            renpy.display.log.write("GL Disabled.")
            return False

        print("Using {} renderer.".format(self.info["renderer"]))

        if self.did_init:
            self.kill_textures()

        if renpy.android:
            fullscreen = False

        # Handle changes in fullscreen mode.
        if fullscreen != self.old_fullscreen:

            self.did_init = False

            if renpy.windows and (self.old_fullscreen is not None):
                pygame.display.quit()

            pygame.display.init()

            if self.display_info is None:
                self.display_info = renpy.display.get_info()

            self.old_fullscreen = fullscreen

            renpy.display.interface.post_init()

        renpy.display.log.write("")


        # Virtual size.
        self.virtual_size = virtual_size
        vwidth, vheight = virtual_size
        virtual_ar = 1.0 * vwidth / vheight

        # Physical size and framerate.
        pwidth, pheight = self.select_physical_size(physical_size)
        self.select_framerate()

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
            try:
                renpy.display.log.write("Windowed mode.")
                self.window = pygame.display.set_mode((pwidth, pheight), window_flags)

            except pygame.error, e:
                renpy.display.log.write("Could not get pygame screen: %r", e)
                return False


        # Get the size of the created screen.
        pwidth, pheight = self.window.get_size()

        self.physical_size = (pwidth, pheight)
        self.drawable_size = pygame.display.get_drawable_size()

        renpy.display.log.write("Screen sizes: virtual=%r physical=%r drawable=%r" % (self.virtual_size, self.physical_size, self.drawable_size))

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
            int(px_padding / 2),
            int(py_padding / 2),
            pwidth - int(px_padding),
            pheight - int(py_padding),
            )

        # The scaling factor of physical_pixels to drawable pixels.
        self.draw_per_phys = 1.0 * self.drawable_size[0] / self.physical_size[0]

        # The location of the viewport, in drawable pixels.
        self.drawable_viewport = tuple(i * self.draw_per_phys for i in self.physical_box)

        # How many drawable pixels there are per virtual pixel?
        self.draw_per_virt = (1.0 * self.drawable_size[0] / pwidth) * (1.0 * view_width / vwidth)

        # Matrices that transform from virtual space to drawable space, and vice versa.
        self.virt_to_draw = Matrix2D(self.draw_per_virt, 0, 0, self.draw_per_virt)
        self.draw_to_virt = Matrix2D(1.0 / self.draw_per_virt, 0, 0, 1.0 / self.draw_per_virt)

        if not self.did_init:
            if not self.init():
                return False

        # This is just to test a late failure, and the switch from GL to GLES.
        if "RENPY_FAIL_" + self.info["renderer"].upper() in os.environ:
            return False

        self.did_init = True

        # Prepare a mouse display.
        self.mouse_old_visible = None

        # If the window is maximized, compute the
        if self.window.get_flags() & pygame.WINDOW_MAXIMIZED:
            self.info["max_window_size"] = self.window.get_size()

        return True

    def quit(self):
        """
        Called when terminating the use of the OpenGL context.
        """

        self.kill_textures()

        if not self.old_fullscreen:
            renpy.display.gl_size = self.physical_size

        self.old_fullscreen = None

    def init(self):
        """
        *Internal*
        This does the first-time initialization of OpenGL, deciding
        which subsystems to use.
        """

        # Load uguu, and init GL.
        uguugl.load()

        # Log the GL version.
        renderer = <char *> glGetString(GL_RENDERER)
        version = <char *> glGetString(GL_VERSION)

        renpy.display.log.write("Vendor: %r", str(<char *> glGetString(GL_VENDOR)))
        renpy.display.log.write("Renderer: %r", renderer)
        renpy.display.log.write("Version: %r", version)
        renpy.display.log.write("Display Info: %s", self.display_info)

        print(renderer, version)

        extensions_string = <char *> glGetString(GL_EXTENSIONS)
        extensions = set(extensions_string.split(" "))

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

        self.shader_cache = ShaderCache("cache/shaders.txt")
        self.shader_cache.load()

        self.texture_loader = TextureLoader(self)

        return True

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
        else:
            # Redraw if the mouse moves.
            mx, my, tex = self.mouse_info

            if tex and (mx, my) != pygame.mouse.get_pos():
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
        if surf in self.texture_cache:
            del self.texture_cache[surf]

    def load_texture(self, surf, transient=False):
        """
        Loads a texture into memory.
        """

        # Turn a surface into a texture grid.
        rv = self.texture_cache.get(surf, None)

        if rv is None:
            rv = self.texture_loader.load_surface(surf)
            self.texture_cache[surf] = rv

        return rv

    def ready_one_texture(self):
        """
        Call from the main thread to make a single texture ready.
        """

#         while True:
#
#             try:
#                 tex = self.ready_texture_queue.pop()
#             except KeyError:
#                 return False
#
#             raise Exception("Not implemented.")

        return False

    def solid_texture(self, w, h, color):
        """
        Returns a texture that represents a solid color.
        """

        mesh = gl2geometry.Mesh()
        mesh.add_rectangle(0, 0, w, h)

        color = tuple(i / 255.0 for i in color)

        return TexturedMesh((w, h), mesh, { }, ("renpy.geometry", "renpy.solid"), { "uSolidColor" : color })

    def flip(self):
        """
        Called to flip the screen after it's drawn.
        """

        self.draw_mouse()

        start = time.time()

        renpy.plog(1, "flip")

        pygame.display.flip()

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


    def draw_screen(self, render_tree, fullscreen_video, flip=True):
        """
        Draws the screen.
        """

        # NOTE: This needs to set interface.text_rect as a side effect.

        renpy.plog(1, "start draw_screen")

        if renpy.display.video.fullscreen:
            surf = renpy.display.video.render_movie("movie", self.virtual_size[0], self.virtual_size[1])
        else:
            surf = render_tree

        if surf is None:
            return

        # Set up the viewport.
        x, y, w, h = self.drawable_viewport
        glViewport(x, y, w, h)

        # Clear the screen.
        clear_r, clear_g, clear_b = renpy.color.Color(renpy.config.gl_clear_color).rgb
        glClearColor(clear_r, clear_g, clear_b, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # TODO: Draw surf

        surf.is_opaque()

        # Project the child from virtual space to the screen space.
        cdef Matrix transform
        transform = renpy.display.matrix.screen_projection(self.virtual_size[0], self.virtual_size[1])

        # Use the context to draw the surface tree.
        context = GL2DrawingContext(self)
        context.draw(surf, transform)

        self.flip()

        self.texture_loader.cleanup()

    def render_to_texture(self, what, alpha):
        """
        Renders `what` to a texture. The texture will have the drawable
        size of `what`.
        """

        width = int(math.ceil(what.width * self.draw_per_virt))
        height = int(math.ceil(what.height * self.draw_per_virt))

        raise


    def is_pixel_opaque(self, what, x, y):
        """
        Returns true if the pixel is not 100% transparent.
        """

        if x < 0 or y < 0 or x >= what.width or y >= what.height:
            return 0

        what = what.subsurface((x, y, 1, 1))

        raise Exception("Not Implemented.")


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

        x = max(0, x)
        x = min(vw, x)
        y = max(0, y)
        y = min(vh, y)

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

    def update_mouse(self):
        # The draw routine updates the mouse. There's no need to
        # redraw it event-by-event.

        return

    def mouse_event(self, ev):
        x, y = getattr(ev, 'pos', pygame.mouse.get_pos())
        return self.translate_point(x, y)

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return self.translate_point(x, y)

    def set_mouse_pos(self, x, y):
        x, y = self.untranslate_point(x, y)
        pygame.mouse.set_pos([x, y])

    # Private.
    def draw_mouse(self):

        hardware, mx, my, tex = renpy.game.interface.get_mouse_info()

        self.mouse_info = (mx, my, tex)

        if self.mouse_old_visible != hardware:
            pygame.mouse.set_visible(hardware)
            self.mouse_old_visible = hardware

        if not tex:
            return

        x, y = pygame.mouse.get_pos()

        x -= mx
        y -= my

        pw, ph = self.physical_size
        pbx, pby, pbw, pbh = self.physical_box

        # Multipliers from mouse coordinates to draw coordinates.
        xmul = 1.0 * self.drawable_size[0] / self.physical_size[0]
        ymul = 1.0 * self.drawable_size[1] / self.physical_size[1]

        # TODO.

    def screenshot(self, render_tree, fullscreen_video):
        cdef unsigned char *pixels
        cdef SDL_Surface *surf

        cdef unsigned char *raw_pixels
        cdef unsigned char *rpp
        cdef int x, y, pitch

        # A surface the size of the framebuffer.
        full = renpy.display.pgrender.surface_unscaled(self.drawable_size, False)
        surf = PySurface_AsSurface(full)

        # Create an array that can hold densely-packed pixels.
        raw_pixels = <unsigned char *> malloc(surf.w * surf.h * 4)

        # Draw the last screen to the back buffer.
        if render_tree is not None:
            self.draw_screen(render_tree, fullscreen_video, flip=False)
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

        with nogil:
            for y from 0 <= y < surf.h:
                for x from 0 <= x < (surf.w * 4):
                    pixels[x] = rpp[x]

                pixels += pitch
                rpp += surf.w * 4

        free(raw_pixels)

        px, py, pw, ph = self.physical_box
        xmul = self.drawable_size[0] / self.physical_size[0]
        ymul = self.drawable_size[1] / self.physical_size[1]

        # Crop and flip it, since it's upside down.
        rv = full.subsurface((px * xmul, py * ymul, pw * xmul, ph * ymul))
        rv = renpy.display.pgrender.flip_unscaled(rv, False, True)

        return rv

    def kill_textures(self):
        self.texture_cache.clear()
        self.texture_loader.end_generation()

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

    # The draw object this context is associated with.
    cdef GL2Draw gl2draw

    def __init__(self, GL2Draw draw):
        self.gl2draw = draw

    def draw_texturedmesh(self, tm, transform):

        shader = self.gl2draw.shader_cache.get(tm.shaders)

        uniforms = tm.uniforms.copy()
        uniforms["uTransform"] = transform

        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        for i, (k, tex) in enumerate(tm.textures.items()):
            tex.load()
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, tex.number)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            uniforms[k] = i

        shader.draw(tm.mesh, uniforms)

    def draw(self, what, Matrix transform):
        """
        This is responsible for walking the surface tree, and drawing any
        TexturedMeshes, Renders, and Surfaces it encounters.

        `transform`
            The matrix that transforms texture space into drawable space.
        """

        if isinstance(what, pygame.Surface):
            what = self.draw.load_texture(what)

        if isinstance(what, TexturedMesh):
            self.draw_texturedmesh(what, transform)
            return

        cdef Render r
        r = what

        if r.text_input:
            renpy.display.interface.text_rect = r.screen_rect(0, 0, transform)

        # TODO: Check r.operation to handle other draw mode. (Or replace this
        # with something new.)

        # TODO: Handle clipping (r.xclipping, r.yclipping, perhaps arbitrary
        # clipping too.)

        # TODO: Handle r.alpha, r.over, r.nearest.

        if (r.reverse is not None) and (r.reverse is not IDENTITY):
            transform = transform * r.reverse

        for child, cx, cy, focus, main in r.visible_children:

            # TODO: figure out if subpixel blitting should be done.

            # The type of cx and cy depends on if this is a subpixel blit or not.
            #             if type(cx) is float:
            #                 subpixel = True


            child_transform = transform

            if (cx or cy):
                child_transform = child_transform * offset(cx, cy, 0)

            self.draw(child, child_transform)

        return 0
