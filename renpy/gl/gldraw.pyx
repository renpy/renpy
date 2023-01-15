#cython: profile=False
#@PydevCodeAnalysisIgnore
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

from libc.stdlib cimport malloc, free
from sdl2 cimport *
from renpy.uguu.gl cimport *

from pygame_sdl2 cimport *
import_pygame_sdl2()

import renpy
import renpy.uguu.gl
import renpy.gl.glfunctions
import pygame_sdl2 as pygame
import os
import os.path
import weakref
import array
import time
import math

cimport renpy.display.render as render
cimport renpy.gl.gltexture as gltexture
import renpy.gl.gltexture as gltexture

# Cache various externals, so we can use them more efficiently.
cdef int DISSOLVE, IMAGEDISSOLVE, PIXELLATE, FLATTEN
DISSOLVE = renpy.display.render.DISSOLVE
IMAGEDISSOLVE = renpy.display.render.IMAGEDISSOLVE
PIXELLATE = renpy.display.render.PIXELLATE
FLATTEN  = renpy.display.render.FLATTEN

cdef object IDENTITY
IDENTITY = renpy.display.render.IDENTITY

# Should we try to vsync?
vsync = True

# A list of frame end times, used for the same purpose.
frame_times = [ ]

cdef class GLDraw:

    def __init__(self, name):

        # Are we in gles mode?
        self.gles = (name == "gles") or (name == "angle")

        # How about angle mode?
        self.angle = (name == "angle")

        # Did we do the first-time init?
        self.did_init = False

        # The GL environment to use.
        self.environ = None

        # The GL render-to-texture to use.
        self.rtt = None

        # The screen.
        self.window = None

        # The virtual size of the screen, as requested by the game.
        self.virtual_size = None

        # The physical size of the window we got.
        self.physical_size = None

        # This is used to cache the surface->texture operation.
        self.texture_cache = weakref.WeakKeyDictionary()

        # The time of the last redraw.
        self.last_redraw_time = 0

        # The time between redraws.
        self.redraw_period = .2

        # Info.
        self.info = { "resizable" : True, "additive" : True, "renderer" : name }

        # Old value of fullscreen.
        self.old_fullscreen = None

        # We don't use a fullscreen surface, so this needs to be set
        # to None at all times.
        self.fullscreen_surface = None

        # The display info, from pygame.
        self.display_info = None

        # Should we use the fast (but incorrect) dissolve mode?
        self.fast_dissolve = False # renpy.android

        # Did we do the texture test at least once?
        self.did_texture_test = False

        # Did we do a render_to_texture?
        self.did_render_to_texture = False

        # The DPI scale factor.
        self.dpi_scale = renpy.display.interface.dpi_scale

        # The number of frames to draw fast if the screen needs to be
        # updated.
        self.fast_redraw_frames = 0

        # The queue of textures that might need to be made ready.
        self.ready_texture_queue = weakref.WeakSet()


    def get_texture_size(self):
        """
        Returns the amount of memory locked up in textures.
        """

        return gltexture.total_texture_size, gltexture.texture_count

    def on_resize(self):
        """
        This is called after the main window has changed size.
        """

        self.environ.deinit()
        self.rtt.deinit()

        gltexture.dealloc_textures()
        gltexture.free_texture_numbers()


        if renpy.android or renpy.ios or renpy.emscripten:
            pygame.display.get_window().recreate_gl_context(always=renpy.emscripten)

        # Are we in fullscreen mode?
        fullscreen = bool(pygame.display.get_window().get_window_flags() & (pygame.WINDOW_FULLSCREEN_DESKTOP | pygame.WINDOW_FULLSCREEN))

        # Get the size of the created screen.
        pwidth, pheight = renpy.display.core.get_size()
        vwidth, vheight = self.virtual_size

        renpy.game.preferences.fullscreen = fullscreen
        renpy.game.interface.fullscreen = fullscreen

        self.physical_size = (pwidth, pheight)
        self.drawable_size = pygame.display.get_drawable_size()

        if not fullscreen:
            renpy.game.preferences.physical_size = self.get_physical_size()

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
        # physical pixels. (May not be 100% accurate, but it's good
        # enough for screenshots.)
        self.physical_box = (
            int(px_padding / 2),
            int(py_padding / 2),
            pwidth - int(px_padding),
            pheight - int(py_padding),
            )

        # Scale from the rtt size to the virtual size.
        if renpy.config.use_drawable_resolution:
            self.draw_per_virt = (1.0 * self.drawable_size[0] / pwidth) * (1.0 * view_width / vwidth)
        else:
            self.draw_per_virt = 1.0

        self.virt_to_draw = Matrix2D(self.draw_per_virt, 0, 0, self.draw_per_virt)
        self.draw_to_virt = Matrix2D(1.0 / self.draw_per_virt, 0, 0, 1.0 / self.draw_per_virt)

        # Set some default settings.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        try:
            self.rtt.init()
            self.environ.init()
        except Exception:
            renpy.display.interface.display_reset = True

    def resize(self):

        fullscreen = renpy.game.preferences.fullscreen

        if renpy.android or renpy.ios:
            fullscreen = True

        if renpy.game.preferences.physical_size:
            width = renpy.game.preferences.physical_size[0] or self.virtual_size[0]
            height = renpy.game.preferences.physical_size[1] or self.virtual_size[1]
        else:
            width = self.virtual_size[0]
            height = self.virtual_size[1]

        width *= self.dpi_scale
        height *= self.dpi_scale

        max_w, max_h = self.info["max_window_size"]
        width = min(width, max_w)
        height = min(height, max_h)
        width = max(width, 256)
        height = max(height, 256)

        pygame.display.get_window().restore()
        pygame.display.get_window().resize((width, height), opengl=True, fullscreen=fullscreen)

    def update(self, force=False):
        """
        Documented in renderer.
        """

        fullscreen = bool(pygame.display.get_window().get_window_flags() & (pygame.WINDOW_FULLSCREEN_DESKTOP | pygame.WINDOW_FULLSCREEN))

        size = renpy.display.core.get_size()

        if force or (fullscreen != renpy.display.interface.fullscreen) or (size != self.physical_size):
            renpy.display.interface.before_resize()
            self.on_resize()

            return True
        else:
            return False


    def init(self, virtual_size):
        """
        This changes the video mode. It also initializes OpenGL, if it
        can. It returns True if it was successful, or False if OpenGL isn't
        working for some reason.
        """

        global vsync

        if not renpy.config.gl_enable:
            renpy.display.log.write("GL Disabled.")
            return False

        if renpy.mobile or renpy.game.preferences.physical_size is None: # @UndefinedVariable
            physical_size = (None, None)
        else:
            physical_size = renpy.game.preferences.physical_size

        if renpy.android or renpy.ios:
            fullscreen = True
        else:
            fullscreen = renpy.game.preferences.fullscreen

        self.virtual_size = virtual_size

        vwidth, vheight = virtual_size
        pwidth, pheight = physical_size

        if pwidth is None:
            pwidth = vwidth
            pheight = vheight

        virtual_ar = 1.0 * vwidth / vheight

        pwidth *= self.dpi_scale
        pheight *= self.dpi_scale

        window_args = { }

        info = renpy.display.get_info()

        visible_w = info.current_w
        visible_h = info.current_h

        if renpy.windows and renpy.windows <= (6, 1):
            visible_h -= 102

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

        if renpy.windows or renpy.linux or renpy.macintosh:

            # Are we maximized?
            old_surface = pygame.display.get_surface()
            if old_surface is not None:
                maximized = old_surface.get_flags() & pygame.WINDOW_MAXIMIZED
            else:
                maximized = False

            if not maximized:

                pwidth = min(visible_w, pwidth, head_w)
                pheight = min(visible_h, pheight, head_h)
                pwidth, pheight = min(pheight * virtual_ar, pwidth), min(pwidth / virtual_ar, pheight)

        pwidth = round(pwidth)
        pheight = round(pheight)

        pwidth = max(pwidth, 256)
        pheight = max(pheight, 256)

        # Handle swap control.
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

        # Set the display mode.

        pygame.display.gl_reset_attributes()

        if self.gles:
            pygame.display.hint("SDL_OPENGL_ES_DRIVER", "1")
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)

        else:
            pygame.display.hint("SDL_OPENGL_ES_DRIVER", "0")

        if renpy.android:
            opengl = pygame.OPENGL
            resizable = 0

            pwidth = 0
            pheight = 0

        elif renpy.ios:
            opengl = pygame.OPENGL | pygame.WINDOW_ALLOW_HIGHDPI
            resizable = pygame.RESIZABLE

            pwidth = 0
            pheight = 0

        else:
            opengl = pygame.OPENGL

            if self.dpi_scale == 1.0:
                opengl |= pygame.WINDOW_ALLOW_HIGHDPI

            if renpy.config.gl_resize:
                resizable = pygame.RESIZABLE
            else:
                resizable = 0

        if opengl:
            pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, vsync)
            pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

        if renpy.config.gl_set_attributes is not None:
            renpy.config.gl_set_attributes()

        self.window = None

        if (self.window is None) and fullscreen:
            try:
                renpy.display.log.write("Fullscreen mode.")
                self.window = pygame.display.set_mode((0, 0), pygame.WINDOW_FULLSCREEN_DESKTOP | resizable | opengl | pygame.DOUBLEBUF)
            except pygame.error as e:
                renpy.display.log.write("Opening in fullscreen failed: %r", e)
                self.window = None

        if self.window is None:
            try:
                renpy.display.log.write("Windowed mode.")
                self.window = pygame.display.set_mode((pwidth, pheight), resizable | opengl | pygame.DOUBLEBUF, **window_args)

            except pygame.error as e:
                renpy.display.log.write("Could not get pygame screen: %r", e)
                return False

        renpy.uguu.gl.clear_missing_functions()
        renpy.uguu.gl.load()
        if renpy.uguu.gl.check_missing_functions(renpy.gl.glfunctions.required_functions):
            self.quit()
            return False

        # Log the GL version.
        renderer = <char *> glGetString(GL_RENDERER)
        version = <char *> glGetString(GL_VERSION)

        renpy.display.log.write("Vendor: %r", str(<char *> glGetString(GL_VENDOR)))
        renpy.display.log.write("Renderer: %r", renderer)
        renpy.display.log.write("Version: %r", version)
        renpy.display.log.write("Display Info: %s", self.display_info)

        if self.gles:
            gltexture.use_gles()
        else:
            gltexture.use_gl()

        if renpy.android or renpy.ios:
            self.redraw_period = 1.0
        elif renpy.emscripten:
            # give back control to browser regularly
            self.redraw_period = 0.1

        extensions_string = <char *> glGetString(GL_EXTENSIONS)
        extensions = set(i.decode("utf-8") for i in extensions_string.split(b" "))

        if renpy.config.log_gl_extensions:

            renpy.display.log.write("Extensions:")

            for i in sorted(extensions):
                renpy.display.log.write("    %s", i)

        if "RENPY_FAIL_" + self.info["renderer"].upper() in os.environ:
            self.quit()
            return False

        def use_subsystem(module, envvar, envval, *req_ext):
            """
            Decides if we should used a particular subsystem, based on
            environment variables and/or extensions. If the `envvar`
            environment variable exists, this will return true iff
            its value is `envval`. Otherwise, this will return true if
            all of the required extensions are present, and false
            otherwise.
            """

            if module is None:
                return False

            value = os.environ.get(envvar, "")

            if value:
                if value == envval:
                    return True
                else:
                    return False

            for i in req_ext:
                if i not in extensions:
                    return False

            return True

        # Count the number of texture units.
        cdef GLint texture_units = 0
        glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS, &texture_units)

        renpy.display.log.write("Number of texture units: %d", texture_units)

        # Pick a texture environment subsystem.

        try:
            renpy.display.log.write("Using shader environment.")
            self.environ = glenviron_shader.ShaderEnviron()
            self.info["environ"] = "shader"
            self.environ.init()

        except Exception as e:
            renpy.display.log.write("Initializing shader environment failed:")
            renpy.display.log.exception()
            self.environ = None

        if self.environ is None:
            renpy.display.log.write("Can't find a workable environment.")
            self.quit()
            return False

        # Pick a Render-to-texture method.
        use_fbo = self.gles or use_subsystem(
                glrtt_fbo,
                "RENPY_GL_RTT",
                "fbo",
                "GL_ARB_framebuffer_object")

        if use_fbo:
            renpy.display.log.write("Using FBO RTT.")
            self.rtt = glrtt_fbo.FboRtt()
            self.info["rtt"] = "fbo"
            self.rtt.init()

        elif glrtt_copy:
            renpy.display.log.write("Using copy RTT.")
            self.rtt = glrtt_copy.CopyRtt()
            self.info["rtt"] = "copy"
            self.rtt.init()

        else:
            renpy.display.log.write("Can't find a workable rtt.")
            self.quit()
            return False

        renpy.display.log.write("Using {0} renderer.".format(self.info["renderer"]))

        # Figure out the sizes of texture that render properly.
        if not self.did_texture_test:
            rv = gltexture.test_texture_sizes(self.environ, self)
        else:
            rv = True

        if not rv:
            return False

        self.did_texture_test = True

        # Do additional setup needed.
        renpy.display.pgrender.set_rgba_masks()

        self.on_resize()

        return True

    def quit(self):
        """
        This shuts down the module and all use of the GL context.
        """

        self.kill_textures()

        if self.rtt:
            self.rtt.deinit()

        if self.environ:
            self.environ.deinit()

        if not self.old_fullscreen:
            renpy.display.gl_size = self.physical_size

        gltexture.dealloc_textures()
        gltexture.free_texture_numbers()

        self.old_fullscreen = None

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
        if surf in self.texture_cache:
            del self.texture_cache[surf]

    def load_texture(self, surf, transient=False, properties={}):
        """
        Loads a texture into memory.
        """

        # Turn a surface into a texture grid.

        rv = self.texture_cache.get(surf, None)

        if rv is None:
            rv = gltexture.texture_grid_from_surface(surf, transient)
            self.texture_cache[surf] = rv
            self.ready_texture_queue.add(rv)

        return rv

    def ready_one_texture(self):
        """
        Call from the main thread to make a single texture ready.
        """

        while True:

            try:
                tex = self.ready_texture_queue.pop()
            except KeyError:
                return False

            if not tex.ready:
                tex.make_ready(False)
                return True

        return False

    def solid_texture(self, w, h, color):
        surf = renpy.display.pgrender.surface((w + 4, h + 4), True)
        surf.fill(color)
        surf = surf.subsurface((2, 2, w, h))

        return self.load_texture(surf)

    # private
    def clip_mode_screen(self):
        """
        This does two things. First, it shuts down clipping, and clears
        the cache so it will be reset by the next call to set_clip. Then
        it flags that we are in the screen clip mode, which control how
        coordinates are mapped to the scissor box.
        """

        self.clip_cache = None
        self.clip_rtt_box = None

        self.environ.unset_clip(self)

    # private
    def clip_mode_rtt(self, x, y, w, h):
        """
        The same thing, except the screen is projected in RTT mode.
        """

        self.clip_cache = None
        self.clip_rtt_box = (x, y, w, h)

        self.environ.unset_clip(self)

    # private
    cpdef set_clip(GLDraw self, tuple clip):

        if self.clip_cache == clip:
            return

        self.clip_cache = clip

        self.environ.set_clip(clip, self)


    def draw_screen(self, surftree, flip=True):
        """
        Draws the screen.
        """

        renpy.plog(1, "start draw_screen")

        if renpy.config.use_drawable_resolution:
            reverse = self.virt_to_draw
        else:
            reverse = IDENTITY

        self.draw_render_textures(surftree, 0)

        xmul = 1.0 * self.drawable_size[0] / self.physical_size[0]
        ymul = 1.0 * self.drawable_size[1] / self.physical_size[1]

        if reverse != IDENTITY:
            xsize = xmul * self.physical_box[2]
            ysize = ymul * self.physical_box[3]
        else:
            xsize = self.virtual_size[0]
            ysize = self.virtual_size[1]

        self.environ.viewport(xmul * self.physical_box[0], ymul * self.physical_box[1], xmul * self.physical_box[2], ymul * self.physical_box[3])
        self.environ.ortho(0, xsize, ysize, 0, -1.0, 1.0)

        self.clip_mode_screen()

        clear_r, clear_g, clear_b = renpy.color.Color(renpy.config.gl_clear_color).rgb
        glClearColor(clear_r, clear_g, clear_b, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.default_clip = (0, 0, xsize, ysize)
        clip = self.default_clip

        if renpy.display.video.fullscreen:
            surf = renpy.display.video.render_movie("movie", self.virtual_size[0], self.virtual_size[1])
            if surf is not None:
                self.draw_transformed(surf, clip, 0, 0, 1.0, 1.0, reverse, renpy.config.nearest_neighbor, False)
            else:
                flip = False

        else:
            self.draw_transformed(surftree, clip, 0, 0, 1.0, 1.0, reverse, renpy.config.nearest_neighbor, False)

        if flip:

            start = time.time()

            renpy.plog(1, "flip")

            try:
                pygame.display.flip()
            except pygame.error:
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


        gltexture.cleanup()

    cpdef int draw_render_textures(GLDraw self, what, bint non_aligned) except 1:
        """
        This is responsible for rendering things to textures,
        as necessary.
        """

        cdef render.Render rend
        cdef bint render_what

        if not isinstance(what, render.Render):
            return 0

        rend = <render.Render> what

        render_what = False

        if (rend.xclipping or rend.yclipping) and non_aligned:
            if rend.forward.xdy != 0 or rend.forward.ydx != 0:
                render_what = True
                non_aligned = False

        first = True

        if rend.forward:
            non_aligned |= (rend.forward.xdy != 0)
            non_aligned |= (rend.forward.ydy != 0)

        for child, cxo, cyo, focus, main in rend.children:

            self.draw_render_textures(child, non_aligned)

            if rend.operation == DISSOLVE:
                if not self.fast_dissolve:
                    child.render_to_texture(what.operation_alpha)

            elif rend.operation == IMAGEDISSOLVE:
                child.render_to_texture(first or what.operation_alpha)
                first = False

            elif rend.operation == PIXELLATE:
                p = rend.operation_parameter
                pc = child

                while p > 1:
                    p /= 2
                    pc = self.get_half(pc)

            elif rend.operation == FLATTEN:
                child.render_to_texture(True)

        if render_what:
            what.render_to_texture(True)

    cpdef int draw_transformed(
        GLDraw self,
        object what,
        tuple clip,
        double xo,
        double yo,
        double alpha,
        double over,
        Matrix reverse,
        bint nearest,
        bint subpixel) except 1:

        cdef render.Render rend
        cdef double cxo, cyo, tcxo, tcyo
        cdef Matrix child_reverse

        if not isinstance(what, render.Render):

            if isinstance(what, gltexture.TextureGrid):

                if (not subpixel) and reverse.is_unit_aligned():
                    xo = float(round(xo))
                    yo = float(round(yo))

                self.set_clip(clip)

                gltexture.blit(
                    <gltexture.TextureGrid> what,
                    xo,
                    yo,
                    reverse,
                    alpha,
                    over,
                    self.environ,
                    nearest)

                return 0

            if isinstance(what, pygame.Surface):

                tex = self.load_texture(what)
                self.draw_transformed(tex, clip, xo, yo, alpha, over, reverse, nearest, subpixel)
                return 0

            raise Exception("Unknown drawing type. " + repr(what))

        rend = what

        if rend.text_input:
            renpy.display.interface.text_rect = rend.screen_rect(xo, yo, reverse)

        # Other draw modes.

        if rend.operation == DISSOLVE:

            if not rend.children:
                return 0

            if self.fast_dissolve:

                # This is a fast version of dissolve that's used on
                # GLES systems. The semantics are different than that
                # of dissolve on Ren'Py proper.

                self.draw_transformed(rend.children[0][0], clip, xo, yo, alpha, over, reverse, nearest, subpixel)

                self.draw_transformed(rend.children[1][0], clip, xo, yo, alpha * what.operation_complete, over, reverse, nearest, subpixel)

            else:

                self.set_clip(clip)

                gltexture.blend(
                    rend.children[0][0].render_to_texture(what.operation_alpha),
                    rend.children[1][0].render_to_texture(what.operation_alpha),
                    xo,
                    yo,
                    reverse * self.draw_to_virt,
                    alpha,
                    over,
                    rend.operation_complete,
                    self.environ,
                    nearest)

            return 0

        elif rend.operation == IMAGEDISSOLVE:

            if not rend.children:
                return 0

            self.set_clip(clip)

            gltexture.imageblend(
                rend.children[0][0].render_to_texture(True),
                rend.children[1][0].render_to_texture(what.operation_alpha),
                rend.children[2][0].render_to_texture(what.operation_alpha),
                xo,
                yo,
                reverse * self.draw_to_virt,
                alpha,
                over,
                rend.operation_complete,
                rend.operation_parameter,
                self.environ,
                nearest)

            return 0

        elif rend.operation == PIXELLATE:

            if not rend.children:
                return 0

            self.set_clip(clip)

            p = rend.operation_parameter
            pc = rend.children[0][0]

            while p > 1:
                p /= 2
                pc = self.get_half(pc)

            reverse *= Matrix2D(1.0 * what.width / pc.width, 0, 0, 1.0 * what.height / pc.height)

            gltexture.blit(
                pc,
                xo,
                yo,
                reverse,
                alpha,
                over,
                self.environ,
                True)

            return 0

        elif rend.operation == FLATTEN:

            if not rend.children:
                return 0

            self.set_clip(clip)

            gltexture.blit(
                rend.children[0][0].render_to_texture(True),
                xo,
                yo,
                reverse * self.draw_to_virt,
                alpha,
                over,
                self.environ,
                nearest)

            return 0


        # Compute clipping.
        if rend.xclipping or rend.yclipping:

            # Non-aligned clipping uses RTT.
            if reverse.ydx != 0 or reverse.xdy != 0:
                tex = what.render_to_texture(True)
                self.draw_transformed(tex, clip, xo, yo, alpha, over, reverse * self.draw_to_virt, nearest, subpixel)
                return 0

            minx, miny, maxx, maxy = clip

            # Figure out the transformed width and height of this
            # surface.
            tw, th = reverse.transform(what.width, what.height)

            if rend.xclipping:
                minx = max(minx, min(xo, xo + tw))
                maxx = min(maxx, max(xo, xo + tw))

            if rend.yclipping:
                miny = max(miny, min(yo, yo + th))
                maxy = min(maxy, max(yo, yo + th))

            clip = (minx, miny, maxx, maxy)

        alpha = alpha * rend.alpha
        over = over * rend.over

        if rend.nearest is not None:
            nearest = rend.nearest

        # If our alpha has hit 0, don't do anything.
        if alpha <= 0.003: # (1 / 256)
            return 0

        if rend.reverse is not None and rend.reverse is not IDENTITY:
            child_reverse = reverse * rend.reverse
        else:
            child_reverse = reverse

        for child, cx, cy, focus, main in rend.children:

            # The type of cx and cy depends on if this is a subpixel blit or not.
            if type(cx) is float:
                subpixel = True

            cxo = cx
            cyo = cy

            tcxo = reverse.xdx * cxo + reverse.xdy * cyo
            tcyo = reverse.ydx * cxo + reverse.ydy * cyo

            self.draw_transformed(child, clip, xo + tcxo, yo + tcyo, alpha, over, child_reverse, nearest, subpixel)

        return 0

    def render_to_texture(self, what, alpha):

        width = int(math.ceil(what.width * self.draw_per_virt))
        height = int(math.ceil(what.height * self.draw_per_virt))

        def draw_func(x, y, w, h):

            self.clip_mode_rtt(x, y, w, h)

            if alpha:
                glClearColor(0.0, 0.0, 0.0, 0.0)
            else:
                glClearColor(0.0, 0.0, 0.0, 1.0)

            glClear(GL_COLOR_BUFFER_BIT)

            self.default_clip = (0, 0, width, height)
            clip = self.default_clip

            self.draw_transformed(what, clip, 0, 0, 1.0, 1.0, self.virt_to_draw, renpy.config.nearest_neighbor, False)

        rv = gltexture.texture_grid_from_drawing(width, height, draw_func, self.rtt, self.environ)

        self.did_render_to_texture = True

        return rv


    def is_pixel_opaque(self, what, x, y):
        """
        Returns true if the pixel is not 100% transparent.
        """

        if x < 0 or y < 0 or x >= what.width or y >= what.height:
            return 0

        what = what.subsurface((x, y, 1, 1))

        reverse = IDENTITY

        alpha_holder = [ 0 ]

        def draw_func(x, y, w, h):
            self.environ.viewport(0, 0, 1, 1)
            self.environ.ortho(0, 1, 0, 1, -1, 1)

            self.clip_mode_rtt(0, 0, 1, 1)
            clip = (0, 0, 1, 1)

            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.draw_transformed(what, clip, 0, 0, 1.0, 1.0, reverse, renpy.config.nearest_neighbor, False)

            cdef unsigned char pixel[4]
            glReadPixels(0, 0, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, pixel)

            alpha_holder[0] = (pixel[3])

        self.did_render_to_texture = False

        # We need to render a second time if a render-to-texture occurs, as it
        # has overwritten the buffer we're drawing to.
        for _i in range(2):

            gltexture.texture_grid_from_drawing(1, 1, draw_func, self.rtt, self.environ)

            if not self.did_render_to_texture:
                break

        what.kill()

        return alpha_holder[0]


    def get_half(self, what):
        """
        Gets a texture grid that's half the size of what..
        """
        # Used to work around a bug in cython where self was not getting
        # the right type when being assigned to the closure.
        cdef GLDraw draw = self

        if what.half_cache:
            return what.half_cache

        reverse = Matrix2D(0.5, 0, 0, .5)

        width = max(what.width / 2, 1)
        height = max(what.height / 2, 1)

        def draw_func(x, y, w, h):

            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            draw.clip_mode_rtt(x, y, w, h)

            clip = (0, 0, width, height)

            draw.draw_transformed(what, clip, 0, 0, 1.0, 1.0, reverse, renpy.config.nearest_neighbor, False)

        rv = gltexture.texture_grid_from_drawing(width, height, draw_func, self.rtt, self.environ)

        what.half_cache = rv

        return rv


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

    def screenshot(self, surftree):
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
        if surftree is not None:
            self.draw_screen(surftree, flip=False)
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
        gltexture.dealloc_textures()

    def event_peek_sleep(self):
        pass

    def get_physical_size(self):
        x, y = self.physical_size

        x = int(x / self.dpi_scale)
        y = int(y / self.dpi_scale)

        return (x, y)


class Rtt(object):
    """
    Subclasses of this class handle rendering to a texture.
    """

    def init(self):
        return

    def deinit(self):
        return

    def render(self, texture, x, y, w, h, draw_func):
        """
        This function is called to trigger a rendering to a texture.
        `x`, `y`, `w`, and `h` specify the location and dimensions of
        the sub-image to render to the texture. `draw_func` is called
        to render the texture.
        """

        raise Exception("Not implemented.")

    def get_size_limit(self, dimension):
        """
        Get the maximum size of a texture.
        """

        raise Exception("Not implemented.")


cdef class Environ(object):

    cdef void blit(self):
        """
        Set up a normal blit environment. The texture to be blitted should
        be TEXTURE0.
        """

    cdef void blend(self, double fraction):
        """
        Set up an environment that blends from TEXTURE0 to TEXTURE1.

        `fraction` is the fraction of the blend complete.
        """

    cdef void imageblend(self, double fraction, int ramp):
        """
        Setup an environment that does an imageblend from TEXTURE1 to TEXTURE2.
        The controlling image is TEXTURE0.

        `fraction` is the fraction of the blend complete.
        `ramp` is the length of the ramp.
        """

    cdef void set_vertex(self, float *vertices):
        """
        Sets the array of vertices to be shown. Vertices should be an packed
        array of 2`n` floats.
        """

    cdef void set_texture(self, int unit, float *coords):
        """
        Sets the array of texture coordinates for unit `unit`.
        """

    cdef void set_color(self, float r, float g, float b, float a):
        """
        Sets the color to be shown.
        """

    cdef void set_clip(self, tuple clip_box, GLDraw draw):
        """
        Sets the clipping rectangle.
        """

    cdef void unset_clip(self, GLDraw draw):
        """
        Removes the clipping rectangle.
        """

    cdef void ortho(self, double left, double right, double bottom, double top, double near, double far):
        """
        Enables orthographic projection. `left`, `right`, `top`, `bottom` are the coordinates of the various
        sides of the viewport. `top` and `bottom` are the depth limits.
        """

    cdef void viewport(self, int x, int y, int w, int h):
        """
        Sets the GL viewport.
        """


# These imports need to be down at the bottom, after the Rtt and Environ
# classes have been created.
try:
    from . import glrtt_copy
except Exception:
    glrtt_copy = None

# Copy doesn't work on iOS.
if renpy.ios:
    glrtt_copy = None

try:
    from . import glrtt_fbo
except ImportError:
    glrtt_fbo = None

try:
    from . import glenviron_shader
except ImportError:
    glenviron_shader = None
