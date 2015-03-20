#cython: profile=False
#@PydevCodeAnalysisIgnore
# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

DEF ANGLE = False

from libc.stdlib cimport malloc, free
from sdl2 cimport *
from gl cimport *

from pygame_sdl2 cimport *
import_pygame_sdl2()

import renpy
import pygame_sdl2 as pygame
import os
import os.path
import weakref
import array
import time

cimport renpy.display.render as render
cimport gltexture
import gltexture
import glblacklist


cdef extern from "glcompat.h":
    GLenum glewInit()
    GLubyte *glewGetErrorString(GLenum)
    GLboolean glewIsSupported(char *)

    enum:
        GLEW_OK

cdef extern from "eglsupport.h":
    int egl_available()
    char *egl_init(int)
    void egl_swap()
    void egl_quit()


# EGL is a flag we check to see if we have EGL on this platform.
cdef bint EGL
EGL = egl_available()

# Cache various externals, so we can use them more efficiently.
cdef int DISSOLVE, IMAGEDISSOLVE, PIXELLATE
DISSOLVE = renpy.display.render.DISSOLVE
IMAGEDISSOLVE = renpy.display.render.IMAGEDISSOLVE
PIXELLATE = renpy.display.render.PIXELLATE

cdef object IDENTITY
IDENTITY = renpy.display.render.IDENTITY

cdef class GLDraw:

    def __init__(self, allow_fixed=True):

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
        self.info = { "resizable" : True, "additive" : True }

        if not ANGLE:
            self.info["renderer"] = "gl"
        else:
            self.info["renderer"] = "angle"

        # Old value of fullscreen.
        self.old_fullscreen = None

        # We don't use a fullscreen surface, so this needs to be set
        # to None at all times.
        self.fullscreen_surface = None

        # The display info, from pygame.
        self.display_info = None

        # The amount we're upscaling by.
        self.upscale_factor = 1.0

        # Should we use the fast (but incorrect) dissolve mode?
        self.fast_dissolve = False # renpy.android

        # Should we always report pixels as being always opaque?
        self.always_opaque = renpy.android

        # Should we allow the fixed-function environment?
        self.allow_fixed = allow_fixed

        # Did we do the texture test at least once?
        self.did_texture_test = False

    def set_mode(self, virtual_size, physical_size, fullscreen):
        """
        This changes the video mode. It also initializes OpenGL, if it
        can. It returns True if it was succesful, or False if OpenGL isn't
        working for some reason.
        """

        cdef char *egl_error

        if not renpy.config.gl_enable:
            renpy.display.log.write("GL Disabled.")
            return False

        if self.did_init:
            self.deinit()

        if renpy.android:
            fullscreen = False

        if fullscreen != self.old_fullscreen:

            self.did_init = False

            if self.old_fullscreen is not None:
                pygame.display.quit()

            pygame.display.init()

            if self.display_info is None:
                self.display_info = renpy.display.get_info()

            self.old_fullscreen = fullscreen

            renpy.display.interface.post_init()

        renpy.display.log.write("")

        self.virtual_size = virtual_size

        vwidth, vheight = virtual_size
        pwidth, pheight = physical_size

        if pwidth is None:
            pwidth = vwidth
            pheight = vheight

        virtual_ar = 1.0 * vwidth / vheight

        pwidth = max(vwidth / 2, pwidth)
        pheight = max(vheight / 2, pheight)

        if not renpy.mobile:
            pwidth = min(self.display_info.current_w - 102, pwidth)
            pheight = min(self.display_info.current_h - 102, pheight)

            # The first time through.
            if not self.did_init:
                pwidth, pheight = min(pheight * virtual_ar, pwidth), min(pwidth / virtual_ar, pheight)

        pwidth = int(pwidth)
        pheight = int(pheight)

        pwidth = max(pwidth, 256)
        pheight = max(pheight, 256)

        # Handle swap control.
        vsync = int(os.environ.get("RENPY_GL_VSYNC", "1"))

        if ANGLE:
            opengl = 0
            resizable = pygame.RESIZABLE

        elif EGL:
            opengl = 0
            resizable = 0

        elif renpy.android:
            opengl = pygame.OPENGL
            resizable = 0

            pwidth = 0
            pheight = 0

        elif renpy.ios:
            opengl = pygame.OPENGL
            resizable = pygame.RESIZABLE

            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2);
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0);

            pwidth = 0
            pheight = 0

        else:
            opengl = pygame.OPENGL

            if renpy.config.gl_resize:
                resizable = pygame.RESIZABLE
            else:
                resizable = 0

        if opengl:
            pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, vsync)
            pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

        try:
            if fullscreen:
                renpy.display.log.write("Fullscreen mode.")
                self.window = pygame.display.set_mode((0, 0), pygame.WINDOW_FULLSCREEN_DESKTOP | opengl | pygame.DOUBLEBUF)
            else:
                renpy.display.log.write("Windowed mode.")
                self.window = pygame.display.set_mode((pwidth, pheight), resizable | opengl | pygame.DOUBLEBUF)

        except pygame.error, e:
            renpy.display.log.write("Could not get pygame screen: %r", e)
            return False

        # Use EGL to get the OpenGL ES 2 context, if necessary.
        if EGL:

            # This ensures the display is shown.
            pygame.display.flip()

            egl_error = egl_init(vsync)

            if egl_error is not NULL:
                renpy.display.log.write("Initializing EGL: %s" % egl_error)
                return False

        # Get the size of the created screen.
        pwidth, pheight = self.window.get_size()
        self.physical_size = (pwidth, pheight)

        renpy.display.log.write("Screen sizes: virtual=%r physical=%r" % (self.virtual_size, self.physical_size))


        if renpy.config.adjust_view_size is not None:
            view_width, view_height = renpy.config.adjust_view_size(pwidth, pheight)
        else:

            # Figure out the virtual box, which includes padding around
            # the borders.
            physical_ar = 1.0 * pwidth / pheight

            ratio = min(1.0 * pwidth / vwidth, 1.0 * pheight / vheight)

            view_width = int(vwidth * ratio)
            view_height = int(vheight * ratio)

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

        if not self.did_init:
            if not self.init():
                return False

        if "RENPY_FAIL_" + self.info["renderer"].upper() in os.environ:
            return False

        self.did_init = True

        # Set some default settings.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        # Prepare a mouse display.
        self.mouse_old_visible = None

        self.environ.init()
        self.rtt.init()

        return True

    def deinit(self):
        """
        De-initializes the system in preparation for a restart, or
        quit. Flushes out all the textures while it's at it.
        """

        renpy.display.interface.kill_textures()

        self.texture_cache.clear()

        gltexture.dealloc_textures()

        if self.rtt:
            self.rtt.deinit()

        if self.environ:
            self.environ.deinit()

    def quit(self):

        if not self.old_fullscreen:
            renpy.display.gl_size = self.physical_size

        gltexture.dealloc_textures()

        self.old_fullscreen = None

    def init(self):
        """
        This does the first-time initialization of OpenGL, deciding
        which subsystems to use.
        """

        if not EGL:

            # Init glew.
            err = glewInit()

            if err != GLEW_OK:
                renpy.display.log.write("Glew init failed: %s" % <char *> glewGetErrorString(err))
                return False

        # Log the GL version.
        renderer = <char *> glGetString(GL_RENDERER)
        version = <char *> glGetString(GL_VERSION)

        renpy.display.log.write("Vendor: %r", str(<char *> glGetString(GL_VENDOR)))
        renpy.display.log.write("Renderer: %r", renderer)
        renpy.display.log.write("Version: %r", version)
        renpy.display.log.write("Display Info: %s", self.display_info)


        allow_shader = True
        allow_fixed = self.allow_fixed

        for r, v, allow_shader_, allow_fixed_ in glblacklist.BLACKLIST:
            if r in renderer and v in version:
                allow_shader = allow_shader and allow_shader_
                allow_fixed = allow_fixed and allow_fixed_
                break

        if not allow_shader:
            renpy.display.log.write("Shaders are blacklisted.")
        if not allow_fixed:
            renpy.display.log.write("Fixed-function is blacklisted.")

        if not allow_shader and not allow_fixed:
            renpy.display.log.write("GL is totally blacklisted.")
            return False

        if EGL:
            gltexture.use_gles()

        elif renpy.android or renpy.ios:
            self.redraw_period = 1.0
            self.always_opaque = True
            gltexture.use_gles()

        else:
            gltexture.use_gl()

        extensions_string = <char *> glGetString(GL_EXTENSIONS)
        extensions = set(extensions_string.split(" "))

        renpy.display.log.write("Extensions:")

        for i in sorted(extensions):
            renpy.display.log.write("    %s", i)

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
        glGetIntegerv(GL_MAX_TEXTURE_UNITS, &texture_units)

        renpy.display.log.write("Number of texture units: %d", texture_units)

        # Pick a texture environment subsystem.

        if EGL or renpy.android or renpy.ios or (allow_shader and use_subsystem(
            glenviron_shader,
            "RENPY_GL_ENVIRON",
            "shader",
            "GL_ARB_vertex_shader",
            "GL_ARB_fragment_shader")):

            try:
                renpy.display.log.write("Using shader environment.")
                self.environ = glenviron_shader.ShaderEnviron()
                self.info["environ"] = "shader"
                self.environ.init()

            except Exception, e:
                renpy.display.log.write("Initializing shader environment failed:")
                renpy.display.log.exception()
                self.environ = None

        if self.environ is None:

            if allow_fixed and use_subsystem(
                glenviron_fixed,
                "RENPY_GL_ENVIRON",
                "fixed",
                "GL_ARB_texture_env_crossbar",
                "GL_ARB_texture_env_combine"):

                renpy.display.log.write("Using fixed-function environment (clause 1).")
                self.environ = glenviron_fixed.FixedFunctionEnviron()
                self.info["environ"] = "fixed"
                self.environ.init()

            elif allow_fixed and use_subsystem(
                glenviron_fixed,
                "RENPY_GL_ENVIRON",
                "fixed",
                "GL_NV_texture_env_combine4"):

                renpy.display.log.write("Using fixed-function environment (clause 2).")
                self.environ = glenviron_fixed.FixedFunctionEnviron()
                self.info["environ"] = "fixed"
                self.environ.init()

            elif use_subsystem(
                glenviron_limited,
                "RENPY_GL_ENVIRON",
                "limited",
                "RENPY_bogus_extension"):

                renpy.display.log.write("Using limited environment.")
                self.environ = glenviron_limited.LimitedEnviron()
                self.info["environ"] = "limited"
                self.environ.init()

            else:
                renpy.display.log.write("Can't find a workable environment.")
                return False

        # Pick a Render-to-texture method.

        # 2015-3-3 - had a problem with 2012-era Nvidia drivers that prevented
        # ANGLE from working with fbo on Windows.

        use_fbo = (
            renpy.ios or renpy.android or (EGL and not ANGLE) or
            use_subsystem(
                glrtt_fbo,
                "RENPY_GL_RTT",
                "fbo",
                # "GL_ARB_framebuffer_object"
                "RENPY_bogus_extension"))

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
            return False


        renpy.display.log.write("Using {0} renderer.".format(self.info["renderer"]))

        # Figure out the sizes of texture that render properly.
        if not self.did_texture_test:
            rv = gltexture.test_texture_sizes(self.environ, self)
        else:
            rv = True

        self.rtt.deinit()
        self.environ.deinit()

        if not rv:
            return False

        self.did_texture_test = True

        # Do additional setup needed.
        renpy.display.pgrender.set_rgba_masks()

        return True


    def should_redraw(self, needs_redraw, first_pass):
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
        elif time.time() > self.last_redraw_time + self.redraw_period:
            rv = True
        else:
            # Redraw if the mouse moves.
            mx, my, tex = self.mouse_info
            if tex and (mx, my) != pygame.mouse.get_pos():
                rv = True

        # Store the redraw time.
        if rv:
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
            rv = gltexture.texture_grid_from_surface(surf, transient)
            self.texture_cache[surf] = rv

        return rv

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


    def draw_screen(self, surftree, fullscreen_video, flip=True):
        """
        Draws the screen.
        """

        forward = reverse = IDENTITY

        surftree.is_opaque()

        self.draw_render_textures(surftree, 0)

        self.environ.viewport(self.physical_box[0], self.physical_box[1], self.physical_box[2], self.physical_box[3])
        self.environ.ortho(0, self.virtual_size[0], self.virtual_size[1], 0, -1.0, 1.0)

        self.clip_mode_screen()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.default_clip = (0, 0, self.virtual_size[0], self.virtual_size[1])
        clip = self.default_clip

        self.upscale_factor = 1.0 * self.physical_size[0] / self.virtual_size[0]

        if renpy.audio.music.get_playing("movie") and renpy.display.video.fullscreen:
            surf = renpy.display.video.render_movie(self.virtual_size[0], self.virtual_size[1])
            if surf is not None:
                self.draw_transformed(surf, clip, 0, 0, 1.0, 1.0, reverse, False)

        else:
            self.draw_transformed(surftree, clip, 0, 0, 1.0, 1.0, reverse, False)

        if flip:

            self.draw_mouse()

            if EGL:
                egl_swap()
            else:
                pygame.display.flip()

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

        if rend.clipping and non_aligned:
            if rend.forward.xdy != 0 or rend.forward.ydx != 0:
                render_what = True
                non_aligned = False

        first = True

        if rend.forward:
            non_aligned |= (rend.forward.xdy != 0)
            non_aligned |= (rend.forward.ydy != 0)

        for child, cxo, cyo, focus, main in rend.visible_children:

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
        render.Matrix2D reverse,
        bint nearest) except 1:

        cdef render.Render rend
        cdef double cxo, cyo, tcxo, tcyo
        cdef render.Matrix2D child_reverse

        if not isinstance(what, render.Render):

            if isinstance(what, gltexture.TextureGrid):

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
                self.draw_transformed(tex, clip, xo, yo, alpha, over, reverse, nearest)
                return 0

            raise Exception("Unknown drawing type. " + repr(what))

        rend = what

        if rend.text_input:
            renpy.display.interface.text_rect = rend.screen_rect(xo, yo, reverse)


        # Other draw modes.

        if rend.operation == DISSOLVE:

            if self.fast_dissolve:

                # This is a fast version of dissolve that's used on
                # GLES systems. The semantics are different than that
                # of dissolve on Ren'Py proper.

                self.draw_transformed(rend.children[0][0],
                                      clip, xo, yo, alpha, over, reverse, nearest)

                self.draw_transformed(rend.children[1][0],
                                      clip, xo, yo, alpha * what.operation_complete, over, reverse, nearest)

            else:

                self.set_clip(clip)

                gltexture.blend(
                    rend.children[0][0].render_to_texture(what.operation_alpha),
                    rend.children[1][0].render_to_texture(what.operation_alpha),
                    xo,
                    yo,
                    reverse,
                    alpha,
                    over,
                    rend.operation_complete,
                    self.environ)

            return 0

        elif rend.operation == IMAGEDISSOLVE:

            self.set_clip(clip)

            gltexture.imageblend(
                rend.children[0][0].render_to_texture(True),
                rend.children[1][0].render_to_texture(what.operation_alpha),
                rend.children[2][0].render_to_texture(what.operation_alpha),
                xo,
                yo,
                reverse,
                alpha,
                over,
                rend.operation_complete,
                rend.operation_parameter,
                self.environ)

            return 0


        if rend.operation == PIXELLATE:
            self.set_clip(clip)

            p = rend.operation_parameter
            pc = rend.children[0][0]

            while p > 1:
                p /= 2
                pc = self.get_half(pc)

            reverse *= renpy.display.render.Matrix2D(1.0 * what.width / pc.width, 0, 0, 1.0 * what.height / pc.height)

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


        # Compute clipping.
        if rend.clipping:

            # Non-aligned clipping uses RTT.
            if reverse.ydx != 0 or reverse.xdy != 0:
                tex = what.render_to_texture(True)
                self.draw_transformed(tex, clip, xo, yo, alpha, over, reverse, nearest)
                return 0

            minx, miny, maxx, maxy = clip

            # Figure out the transformed width and height of this
            # surface.
            tw, th = reverse.transform(what.width, what.height)

            minx = max(minx, min(xo, xo + tw))
            maxx = min(maxx, max(xo, xo + tw))
            miny = max(miny, min(yo, yo + th))
            maxy = min(maxy, max(yo, yo + th))

            clip = (minx, miny, maxx, maxy)

        alpha = alpha * rend.alpha
        over = over * rend.over
        nearest = nearest or rend.nearest

        # If our alpha has hit 0, don't do anything.
        if alpha <= 0.003: # (1 / 256)
            return 0

        if rend.reverse is not None and rend.reverse is not IDENTITY:
            child_reverse = rend.reverse * reverse
        else:
            child_reverse = reverse

        for child, cxo, cyo, focus, main in rend.visible_children:
            tcxo = reverse.xdx * cxo + reverse.xdy * cyo
            tcyo = reverse.ydx * cxo + reverse.ydy * cyo

            self.draw_transformed(child, clip, xo + tcxo, yo + tcyo, alpha, over, child_reverse, nearest)

        return 0

    def render_to_texture(self_, what, alpha):

        cdef GLDraw self = self_

        forward = reverse = IDENTITY

        def draw_func(x, y, w, h):

            self.clip_mode_rtt(x, y, w, h)

            if alpha:
                glClearColor(0.0, 0.0, 0.0, 0.0)
            else:
                glClearColor(0.0, 0.0, 0.0, 1.0)

            glClear(GL_COLOR_BUFFER_BIT)

            self.default_clip = (0, 0, what.width, what.height)
            clip = self.default_clip

            self.draw_transformed(what, clip, 0, 0, 1.0, 1.0, reverse, False)

        if isinstance(what, render.Render):
            what.is_opaque()

        self.upscale_factor = 1.0

        rv = gltexture.texture_grid_from_drawing(what.width, what.height, draw_func, self.rtt, self.environ)

        return rv


    def is_pixel_opaque(self, what, x, y):
        """
        Returns true if the pixel is not 100% transparent.
        """

        if x < 0 or y < 0 or x >= what.width or y >= what.height:
            return 0

        if self.always_opaque:
            return 255

        what = what.subsurface((x, y, 1, 1))

        forward = reverse = IDENTITY

        self.environ.viewport(0, 0, 1, 1)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT)

        self.environ.ortho(0, 1, 0, 1, -1, 1)

        self.clip_mode_rtt(0, 0, 1, 1)

        clip = (0, 0, 1, 1)

        self.draw_transformed(what, clip, 0, 0, 1.0, 1.0, reverse, False)

        cdef unsigned char pixel[4]

        glReadPixels(0, 0, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, pixel)

        a = pixel[3]

        what.kill()

        return a


    def get_half(self, what):
        """
        Gets a texture grid that's half the size of what..
        """
        # Used to work around a bug in cython where self was not getting
        # the right type when being assigned to the closure.
        cdef GLDraw draw = self

        if what.half_cache:
            return what.half_cache

        reverse = renpy.display.render.Matrix2D(0.5, 0, 0, .5)
        forward = renpy.display.render.Matrix2D(2.0, 0, 0, 2.0)

        width = max(what.width / 2, 1)
        height = max(what.height / 2, 1)

        def draw_func(x, y, w, h):

            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            draw.clip_mode_rtt(x, y, w, h)

            clip = (0, 0, width, height)

            draw.draw_transformed(what, clip, 0, 0, 1.0, 1.0, reverse, False)

        if isinstance(what, render.Render):
            what.is_opaque()

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

        # Translate from virtual size.
        x = ( x - vx ) / vbw
        y = ( y - vy ) / vbh

        # Translate from fractional screen.
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

        self.environ.viewport(0, 0, pw, ph)
        self.environ.ortho(0, pw, ph, 0, -1.0, 1.0)

        self.clip_mode_screen()
        self.set_clip((-pbx, -pby, pw, ph))

        gltexture.blit(
            tex,
            x,
            y,
            IDENTITY,
            1.0,
            1.0,
            self.environ,
            False)

    def screenshot(self, surftree, fullscreen_video):
        cdef unsigned char *pixels
        cdef SDL_Surface *surf

        cdef unsigned char *raw_pixels
        cdef unsigned char *rpp
        cdef int x, y, pitch

        # A surface the size of the framebuffer.
        full = renpy.display.pgrender.surface_unscaled(self.physical_size, False)
        surf = PySurface_AsSurface(full)

        # Create an array that can hold densely-packed pixels.
        raw_pixels = <unsigned char *> malloc(surf.w * surf.h * 4)

        # Draw the last screen to the back buffer.
        if surftree is not None:
            self.draw_screen(surftree, fullscreen_video, flip=False)
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

        for y from 0 <= y < surf.h:
            for x from 0 <= x < (surf.w * 4):
                pixels[x] = rpp[x]

            pixels += pitch
            rpp += surf.w * 4

        free(raw_pixels)

        # Crop and flip it, since it's upside down.
        rv = full.subsurface(self.physical_box)
        rv = renpy.display.pgrender.flip_unscaled(rv, False, True)

        return rv

    def free_memory(self):
        self.texture_cache.clear()
        gltexture.dealloc_textures()

    def event_peek_sleep(self):
        pass

    def get_physical_size(self):
        return self.physical_size


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
    import glrtt_copy
except:
    glrtt_copy = None

# Copy doesn't work on iOS.
if renpy.ios:
    glrtt_copy = None

try:
    import glrtt_fbo
except ImportError:
    glrtt_fbo = None

try:
    import glenviron_fixed
except ImportError:
    glenviron_fixed = None

try:
    import glenviron_shader
except ImportError:
    glenviron_shader = None

try:
    import glenviron_limited
except ImportError:
    glenviron_limited = None

