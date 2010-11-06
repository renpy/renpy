#cython: profile=True
# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

from pygame cimport *
from gl cimport *

import renpy
import pygame
import os
import os.path
import weakref
import array
import time

cimport renpy.display.gltexture as gltexture
cimport renpy.display.render as render

import renpy.display.gltexture as gltexture
import renpy.display.glenviron as glenviron
import renpy.display.glrtt_copy as glrtt_copy

try:
    import renpy.display.glenviron_fixed as glenviron_fixed
except ImportError:
    glenviron_fixed = None

try:
    import renpy.display.glenviron_shader as glenviron_shader
except ImportError:
    glenviron_shader = None


cdef extern from "glcompat.h":
    GLenum glewInit()
    GLubyte *glewGetErrorString(GLenum)

    enum:
        GLEW_OK

# This is used by gl_error_check in gl.pxd.
class GLError(Exception):
    """
    This is used to report OpenGL errors.
    """

    pass

# Cache various externals, so we can use them more efficiently.
cdef int DISSOLVE, IMAGEDISSOLVE, PIXELLATE
DISSOLVE = renpy.display.render.DISSOLVE
IMAGEDISSOLVE = renpy.display.render.IMAGEDISSOLVE
PIXELLATE = renpy.display.render.PIXELLATE

cdef object IDENTITY
IDENTITY = renpy.display.render.IDENTITY

cdef void gl_clip(GLenum plane, GLdouble a, GLdouble b, GLdouble c, GLdouble d):
    """
    Utility function that takes care of setting up an OpenGL clip plane.
    """

    cdef GLdouble equation[4]

    equation[0] = a
    equation[1] = b
    equation[2] = c
    equation[3] = d
    glClipPlane(plane, equation)
        

# A list of cards that cause system/software crashes. There's no
# reason to put merely slow or incapable cards here, only ones for
# which GL operation is unsafe.
#
# 

BLACKLIST = [
    ("S3 Graphics DeltaChrome", "1.4 20.00"),
    ]

# The logfile we use.
log_file = None

def open_log_file():
    global log_file
    
    if log_file is not None:
        return log_file

    # The OpenGL logfile.
    try:
        log_file = file(os.path.join(renpy.config.renpy_base, "opengl.txt"), "w")
    except:
        try:
            log_file = file(os.path.join(renpy.config.savedir, "opengl.txt"), "w")
        except:
            log_file = None
            

cdef class GLDraw:

    def __init__(self):

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

        # Info.
        self.info = { "renderer" : "gl" }

        # Old value of fullscreen.
        self.old_fullscreen = None

        # We don't use a fullscreen surface.
        self.fullscreen_surface = None

        # The display info, from pygame.
        self.display_info = None

        # The amount we're upscaling by.
        self.upscale_factor = 1.0

        open_log_file()
        
        
    def log(self, msg, *args):
        """
        Logs a message to the logfile.
        """

        if log_file is not None:
            log_file.write(msg % args)
            log_file.write("\n")
            log_file.flush()
            
            
    def set_mode(self, virtual_size, physical_size, fullscreen):
        """
        This changes the video mode. It also initializes OpenGL, if it
        can. It returns True if it was succesful, or False if OpenGL isn't
        working for some reason.
        """

        if not renpy.config.gl_enable:
            self.log("GL Disabled.")
            return False
        
        if self.did_init:
            self.deinit()

        if fullscreen != self.old_fullscreen:

            pygame.display.quit()
            pygame.display.init()

            self.display_info = pygame.display.Info()
            
            renpy.display.interface.post_init()
            
            self.old_fullscreen = fullscreen
            
        self.log("")
        self.log(renpy.version)
        
        self.virtual_size = virtual_size

        vwidth, vheight = virtual_size
        pwidth, pheight = physical_size

        # On a restart, restore the size.
        if renpy.display.gl_size is not None and not fullscreen:
            pwidth, pheight = renpy.display.gl_size

        renpy.display.gl_size = None

        # Ensure we're always at least 256x256, so we have a shot at rendering
        # textures.
        pwidth = max(pwidth, 256)
        pheight = max(pheight, 256)

        pwidth = min(self.display_info.current_w, pwidth)
        pheight = min(self.display_info.current_h, pheight)
        
        # Handle swap control.
        vsync = os.environ.get("RENPY_GL_VSYNC", "1")
        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, int(vsync))
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

        try:
            if fullscreen:
                self.log("fullscreen mode.")
                self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            else:
                self.log("windowed mode.")
                self.window = pygame.display.set_mode((pwidth, pheight), pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF)

        except pygame.error, e:
            self.log("Could not get pygame screen: %r", e)

            return False

        pwidth, pheight = self.window.get_size()
        self.physical_size = (pwidth, pheight)

        self.log("Screen sizes: virtual=%r physical=%r" % (self.virtual_size, self.physical_size))

        pwidth = max(1, pwidth)
        pheight = max(1, pheight)
        
        # Figure out the virtual box, which includes padding around
        # the borders.
        physical_ar = 1.0 * pwidth / pheight
        virtual_ar = 1.0 * vwidth / vheight

        if physical_ar >= virtual_ar:
            x_padding = physical_ar * vheight - vwidth
            y_padding = 0
            px_padding = x_padding * pheight / vheight
            py_padding = 0
        else:
            x_padding = 0
            y_padding = ( 1.0 / physical_ar ) * vwidth - vheight
            px_padding = 0
            py_padding = y_padding * pwidth / vwidth

            
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

        self.did_init = True

        # Set some default settings.
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CLIP_PLANE0)
        glEnable(GL_CLIP_PLANE1)
        glEnable(GL_CLIP_PLANE2)
        glEnable(GL_CLIP_PLANE3)
        gl_error_check()
        
        self.environ.init()
        self.rtt.init()

        # Prepare a mouse call.
        self.mouse_old_visible = None
        
        return True

    def deinit(self):
        """
        De-initializes the system in preparation for a restart, or
        quit. Flushes out all the textures while it's at it.
        """
    
        # This should get rid of all of the cached textures.
        renpy.display.render.free_memory()
        
        self.texture_cache.clear()

        gltexture.dealloc_textures()
        
        if self.rtt:
            self.rtt.deinit()

        if self.environ:
            self.environ.deinit()

    def quit(self):

        if not self.old_fullscreen:
            renpy.display.gl_size = self.physical_size
        
        self.log("Deallocating textures.")
        gltexture.dealloc_textures()
        self.log("Done deallocating textures.")
        
        self.log("About to quit GL.")
        pygame.display.quit()
        self.log("Finished quit GL.")
        
    def init(self):
        """
        This does the first-time initialization of OpenGL, deciding
        which subsystems to use.
        """

        # Init glew.
        err = glewInit()

        if err != GLEW_OK:
            raise Exception("Glew init failed: %s" % <char *> glewGetErrorString(err))
        
        # Log the GL version.
        renderer = <char *> glGetString(GL_RENDERER)
        version = <char *> glGetString(GL_VERSION)

        self.log("Vendor: %r", str(<char *> glGetString(GL_VENDOR)))
        self.log("Renderer: %r", renderer)
        self.log("Version: %r", version)
        self.log("Display Info: %s", self.display_info)

        for r, v in BLACKLIST:
            if renderer == r and version.startswith(v):
                self.log("Blacklisted renderer/version.")
                return False

        extensions_string = <char *> glGetString(GL_EXTENSIONS)            
        extensions = set(extensions_string.split(" "))
        
        self.log("Extensions:")

        for i in sorted(extensions):
            self.log("    %s", i)
        
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

        self.log("Number of texture units: %d", texture_units)

        if texture_units < 4:
            self.log("Not enough texture units.")
            return False


        # Count the number of clip planes.
        cdef GLint clip_planes = 0
        
        glGetIntegerv(GL_MAX_CLIP_PLANES, &clip_planes)
        self.log("Number of clipping planes: %d", clip_planes)

        
        # Pick a texture environment subsystem.
        
        if use_subsystem(
            glenviron_shader,
            "RENPY_GL_ENVIRON",
            "shader",
            "GL_ARB_vertex_shader",
            "GL_ARB_fragment_shader"):

            try:
                self.log("Using shader environment.")
                self.environ = glenviron_shader.ShaderEnviron()
                self.info["environ"] = "shader"
            except Exception, e:
                self.log("Initializing shader environment failed:")
                self.log(str(e))
                
        if self.environ is None:
            
            if use_subsystem(
                glenviron_fixed,
                "RENPY_GL_ENVIRON",
                "fixed",
                "GL_ARB_texture_env_crossbar",
                "GL_ARB_texture_env_combine"):

                self.log("Using fixed-function environment (clause 1).")
                self.environ = glenviron_fixed.FixedFunctionEnviron()
                self.info["environ"] = "fixed"

            elif use_subsystem(
                glenviron_fixed,
                "RENPY_GL_ENVIRON",
                "fixed",
                "GL_NV_texture_env_combine4"):

                self.log("Using fixed-function environment (clause 2).")
                self.environ = glenviron_fixed.FixedFunctionEnviron()
                self.info["environ"] = "fixed"

            else:
                self.log("Can't find a workable environment.")
                return False

        # Pick a Render-to-texture subsystem.        
        self.log("Using copy RTT.")
        self.rtt = glrtt_copy.CopyRtt()
        self.info["rtt"] = "copy"

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
        elif time.time() > self.last_redraw_time + .20:
            rv = True

        else:
            # Redraw if the mouse moves.
            mx, my, tex = self.mouse_info
            if tex and (mx, my) != pygame.mouse.get_pos():
                rv = True
            
        # Log the redraw time.
        if rv:
            self.last_redraw_time = time.time()
            return True
        else:        
            return False

    def mutated_surface(self, surf):
        if surf in self.texture_cache:
            del self.texture_cache[surf]

    def load_texture(self, surf, transient=False):
        # Turn a surface into a texture grid.

        rv = self.texture_cache.get(surf, None)

        if rv is None:
            rv = gltexture.texture_grid_from_surface(surf)
            self.texture_cache[surf] = rv

        return rv

    # private
    def undefine_clip(self):
        """
        This makes the clipping undefined. It needs to be called when the
        various matrices change, to ensure that the next call to set_clip
        will re-set-up the clipping. Note that it does not remove the
        clipping, but rather merely causes set_clip to change it.
        """

        self.clip_cache = None
    

    # private
    cpdef set_clip(GLDraw self, tuple clip):

        if self.clip_cache == clip:
            return

        self.clip_cache = clip

        cdef double minx, miny, maxx, maxy
        minx, miny, maxx, maxy = clip

        gl_clip(GL_CLIP_PLANE0, 1.0, 0.0, 0.0, -minx)
        gl_clip(GL_CLIP_PLANE1, 0.0, 1.0, 0.0, -miny)
        gl_clip(GL_CLIP_PLANE2, -1.0, 0.0, 0.0, maxx)
        gl_clip(GL_CLIP_PLANE3, 0.0, -1.0, 0.0, maxy)
        
        
    def draw_screen(self, surftree, fullscreen_video):
        """
        Draws the screen.
        """

        forward = reverse = IDENTITY

        surftree.is_opaque()

        self.draw_render_textures(surftree, 0)

        glViewport(self.physical_box[0], self.physical_box[1], self.physical_box[2], self.physical_box[3])
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.virtual_size[0], self.virtual_size[1], 0, -1.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.undefine_clip()

        clip = (0, 0, self.virtual_size[0], self.virtual_size[1])

        self.upscale_factor = 1.0 * self.physical_size[0] / self.virtual_size[0]

        if renpy.audio.music.get_playing("movie") and renpy.display.video.fullscreen:
            tex = renpy.display.video.get_movie_texture(self.virtual_size)

            # self.load_texture(self.fullscreen_surface, transient=True)
            self.draw_transformed(tex, clip, 0, 0, 1.0, reverse)           
        else:
            self.draw_transformed(surftree, clip, 0, 0, 1.0, reverse)

        self.draw_mouse()

        # Release the CPU while we're waiting for things to actually
        # draw to the screen.
        renpy.display.core.cpu_idle.set()
        pygame.display.flip()
        renpy.display.core.cpu_idle.clear()
            

    cpdef int draw_render_textures(GLDraw self, what, bint non_aligned):
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
        render.Matrix2D reverse):

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
                    self.environ,
                    False)

                return 0

            if isinstance(what, renpy.display.pgrender.Surface):

                tex = self.load_texture(what)
                self.draw_transformed(tex, clip, xo, yo, alpha, reverse)
                return 0

            raise Exception("Unknown drawing type. " + repr(what))

        rend = what
        
        # Other draw modes.
        
        if rend.operation == DISSOLVE:

            self.set_clip(clip)
            
            gltexture.blend(
                rend.children[0][0].render_to_texture(what.operation_alpha),
                rend.children[1][0].render_to_texture(what.operation_alpha),
                xo,
                yo,
                reverse,
                alpha,
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
                self.environ,
                True)

            return 0
                

        # Compute clipping.
        if rend.clipping:

            # Non-aligned clipping uses RTT.
            if reverse.ydx != 0 or reverse.xdy != 0:
                tex = what.render_to_texture(True)
                self.draw_transformed(tex, clip, xo, yo, alpha, reverse)
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

            self.draw_transformed(child, clip, xo + tcxo, yo + tcyo, alpha, child_reverse)

        return 0

    def render_to_texture(self_, what, alpha):

        cdef GLDraw self = self_
        
        forward = reverse = IDENTITY

        def draw_func():

            if alpha:
                glClearColor(0.0, 0.0, 0.0, 0.0)
            else:
                glClearColor(0.0, 0.0, 0.0, 1.0)
                
            glClear(GL_COLOR_BUFFER_BIT)
            self.undefine_clip()
        
            clip = (0, 0, what.width, what.height)
        
            self.draw_transformed(what, clip, 0, 0, 1.0, reverse)

        if isinstance(what, render.Render):
            what.is_opaque()

        self.upscale_factor = 1.0

        rv = gltexture.texture_grid_from_drawing(what.width, what.height, draw_func, self.rtt)

        return rv
        

    def is_pixel_opaque(self, what, x, y):
        """
        Returns true if the pixel is not 100% transparent.
        """

        if x < 0 or y < 0 or x >= what.width or y >= what.height:
            return 0

        what = what.subsurface((x, y, 1, 1))
        
        forward = reverse = IDENTITY

        glViewport(0, 0, 1, 1)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        self.undefine_clip()
        
        clip = (0, 0, 1, 1)
        
        self.draw_transformed(what, clip, 0, 0, 1.0, reverse)

        cdef unsigned char a = 0
        
        glReadPixels(0, 0, 1, 1, GL_ALPHA, GL_BYTE, &a)

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

        def draw_func():
            
            glClearColor(0.0, 0.0, 0.0, 1.0)                
            glClear(GL_COLOR_BUFFER_BIT)
            
            draw.undefine_clip()

            clip = (0, 0, width, height)
            
            draw.draw_transformed(what, clip, 0, 0, 1.0, reverse)

        if isinstance(what, render.Render):
            what.is_opaque()

        rv = gltexture.texture_grid_from_drawing(width, height, draw_func, self.rtt)

        what.half_cache = rv

        return rv
            
    def update_mouse(self):
        # The draw routine updates the mouse. There's no need to
        # redraw it event-by-event.

        return

    def translate_mouse(self, x, y):
        
        # Screen sizes.
        pw, ph = self.physical_size
        vw, vh = self.virtual_size
        vx, vy, vw, vh = self.virtual_box
        
        # Translate to fractional screen.
        x = 1.0 * x / pw
        y = 1.0 * y / ph

        # Translate to virtual size.
        x = vx + vw * x
        y = vy + vh * y

        x = int(x)
        y = int(y)

        x = max(0, x)
        x = min(vw, x)
        y = max(0, y)
        y = min(vh, y)

        return x, y

    def mouse_event(self, ev):
        x, y = getattr(ev, 'pos', pygame.mouse.get_pos())
        return self.translate_mouse(x, y)

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return self.translate_mouse(x, y)
    
    
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
        
        glViewport(0, 0, pw, ph)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, pw, ph, 0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

        self.undefine_clip()
        self.set_clip((0, 0, pw, ph))
        
        gltexture.blit(
            tex,
            x,
            y,
            IDENTITY,
            1.0,
            self.environ,
            False)

    def screenshot(self):
        cdef unsigned char *pixels = NULL
        cdef SDL_Surface *surf

        # A surface the size of the framebuffer
        full = renpy.display.pgrender.surface_unscaled(self.physical_size, False)

        # Use GL to read the full framebuffer in.
        surf = PySurface_AsSurface(full)
        pixels = <unsigned char *> surf.pixels

        glPixelStorei(GL_PACK_ROW_LENGTH, surf.pitch / 4)

        glReadPixels(
            0,
            0,
            surf.w,
            surf.h,
            GL_BGRA,
            GL_UNSIGNED_BYTE,
            pixels)

        # Crop and flip it, since it's upside down.
        rv = full.subsurface(self.physical_box)
        rv = renpy.display.pgrender.flip_unscaled(rv, False, True)
        return rv
        
    def free_memory(self):
        self.texture_cache.clear()
        gltexture.dealloc_textures()
       
    def event_peek_sleep(self):
        pass
        
