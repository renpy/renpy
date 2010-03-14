# IMPORTANT NOTE: The drawing code should handle cases where a surface is
# added to a Render (instead of a TextureGrid) by uploading that surface to
# the graphics card.

# IMPORTANT NOTE: This code should fail gracefully-ish if _renpy_tegl can't be
# imported.

import renpy
from renpy.display.render import IDENTITY, DISSOLVE, IMAGEDISSOLVE, PIXELLATE


import pygame
import os
import sys

import _renpy_tegl as gl
import _renpy_pysdlgl as pysdlgl

import gltexture
import glenviron

if sys.byteorder == 'little':
    MASKS = (
        0x00FF0000,
        0x0000FF00,
        0x000000FF,
        -16777216) # 0xFF000000, but that's not representable as a short int.
else:
    MASKS = (
        0x0000FF00,
        0x00FF0000,
        -16777216,
        0x000000FF)

    
class GLDraw(object):

    def __init__(self):

        # Did we do the first-time init?
        self.did_init = False

        # The GL environment to use.
        self.environ = None

        # The GL render-to-texture to use.
        self.rtt = None

        # The screen.
        self.window = None
        
        # The OpenGL logfile.
        # TODO: Compute the path a bit better.
        try:
            self.log_file = file("opengl.txt", "w")
        except:
            self.log_file = None
            
        # The virtual size of the screen, as requested by the game.
        self.virtual_size = None

        # The physical size of the window we got.
        self.physical_size = None

        # Should we draw? This is for debugging purposes, to help
        # catch glitches.
        self.should_draw = True
        
        
    def log(self, msg, *args):
        """
        Logs a message to the logfile.
        """

        if self.log_file is not None:
            self.log_file.write(msg % args)
            self.log_file.write("\n")
            
            
    def set_mode(self, virtual_size, physical_size, fullscreen):
        """
        This changes the video mode. It also initializes OpenGL, if it
        can. It returns True if it was succesful, or False of OpenGL isn't
        working for some reason.
        """

        if self.rtt:
            self.rtt.deinit()
        if self.environ:
            self.environ.deinit()
        
        gltexture.dealloc_textures()
        
        self.log(renpy.version)
        
        self.virtual_size = virtual_size

        vwidth, vheight = virtual_size
        pwidth, pheight = physical_size

        # Handle swap control.
        vsync = os.environ.get("RENPY_GL_VSYNC", "1")
        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, int(vsync))
        
        try:
            if fullscreen:
                self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            else:
                self.window = pygame.display.set_mode((pwidth, pheight), pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF)        

        except pygame.error, e:
            self.log("Could not get pygame screen: %r", e)

            return False

        pwidth, pheight = self.window.get_size()
        self.physical_size = (pwidth, pheight)
        
        self.log("Screen sizes: virtual=%r physical=%r" % (self.virtual_size, self.physical_size))

        # Figure out the virtual box.
        physical_ar = 1.0 * pwidth / pheight
        virtual_ar = 1.0 * vwidth / vheight
        
        x_padding = vwidth * max(0, physical_ar - virtual_ar)
        y_padding = vheight * max(0, (1.0 / physical_ar) - (1.0 / virtual_ar))

        
        self.virtual_box = (
            -x_padding / 2.0,
            -y_padding / 2.0,
             vwidth + x_padding / 2.0,
             vheight + y_padding / 2.0)

        
        # Set some default settings.
        gl.Enable(gl.BLEND)
        gl.BlendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA)
        gl.Enable(gl.CLIP_PLANE0)
        gl.Enable(gl.CLIP_PLANE1)
        gl.Enable(gl.CLIP_PLANE2)
        gl.Enable(gl.CLIP_PLANE3)

        if not self.did_init:
            if not self.init():
                return False

        self.did_init = True

        self.environ.init()
        self.rtt.init()
        renpy.display.im.rebuild_textures()
            

        return True


    def init(self):
        """
        This does the first-time initialization of OpenGL, deciding
        which subsystems to use.
        """

        # Init glew.
        pysdlgl.init_glew()
        
        # Log the GL version.
        self.log("Vendor: %r", pysdlgl.get_string(gl.VENDOR))
        self.log("Renderer: %r", pysdlgl.get_string(gl.RENDERER))
        self.log("Version: %r", pysdlgl.get_string(gl.VERSION))

        extensions = set(pysdlgl.get_string(gl.EXTENSIONS).split(" "))

        self.log("Extensions:")

        for i in sorted(extensions):
            self.log("    %s", i)
        
        def use_subsystem(envvar, envval, *req_ext):
            """
            Decides if we should used a particular subsystem, based on
            environment variables and/or extensions. If the `envvar`
            environment variable exists, this will return true iff
            its value is `envval`. Otherwise, this will return true if
            all of the required extensions are present, and false
            otherwise.
            """
            
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

        # Pick a texture environment subsystem.
        
        if use_subsystem(
            "RENPY_GL_ENVIRON",
            "shader",
            "GL_ARB_vertex_shader",
            "GL_ARB_fragment_shader"):

            self.log("Using shader environment.")
            self.environ = glenviron.ShaderEnviron()

        elif use_subsystem(
            "RENPY_GL_ENVIRON",
            "fixed",
            "GL_ARB_texture_env_crossbar",
            "GL_ARB_texture_env_combine"):

            self.log("Using fixed-function environment (clause 1).")
            self.environ = glenviron.FixedFunctionEnviron()
        
        elif use_subsystem(
            "RENPY_GL_ENVIRON",
            "fixed",
            "GL_NV_texture_env_combine4"):

            self.log("Using fixed-function environment (clause 2).")
            self.environ = glenviron.FixedFunctionEnviron()

        else:
            self.log("Can't find a workable environment.")
            return False

        # Pick a Render-to-texture subsystem.
        
        if use_subsystem(
            "RENPY_GL_RTT",
            "fbo",
            "GL_EXT_framebuffer_object"):

            self.log("Using framebuffer_object RTT.")
            self.rtt = glenviron.FramebufferRtt()
        
        else:

            self.log("Using copy RTT.")
            self.rtt = glenviron.CopyRtt()

        # Do additional setup needed.
        renpy.display.pgrender.set_sample_masks(MASKS)
            
        return True


    def should_redraw(self, needs_redraw, first_pass):
        # GL does redraws as fast as possible, and lets Sync-to-vblank
        # handle slowing us down.

        return True

    def mutated_surface(self, surf):
        # There's no reason to care about surface mutation.

        return

    def load_texture(self, surf, transient=False):
        # Turn a surface into a texture grid.

        return gltexture.texture_grid_from_surface(surf)

    def unload_texture(self, surf):
        # Texture grids die automatically, we don't have to do anything
        # particularly special.
        
        return

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
    def set_clip(self, clip):

        if self.clip_cache == clip:
            return

        self.clip_cache = clip

        minx, miny, maxx, maxy = clip
        
        # OpenGL clipping works by only allowing coordinates where:
        # a*x + b*y + c*z + d >= 0. 
        
        gl.ClipPlane(gl.CLIP_PLANE0, [1.0, 0.0, 0.0, -minx])
        gl.ClipPlane(gl.CLIP_PLANE1, [0.0, 1.0, 0.0, -miny])
        gl.ClipPlane(gl.CLIP_PLANE2, [-1.0, 0.0, 0.0, maxx])
        gl.ClipPlane(gl.CLIP_PLANE3, [0.0, -1.0, 0.0, maxy])
        
        
    def draw_screen(self, surftree, fullscreen_video):
        """
        Draws the screen.
        """

        forward = reverse = IDENTITY

        surftree.is_opaque()

        self.draw_render_textures(surftree, forward, reverse)
        
        gl.Viewport(0, 0, self.physical_size[0], self.physical_size[1])

        gl.MatrixMode(gl.PROJECTION)
        gl.LoadIdentity()

        gl.Ortho(self.virtual_box[0], self.virtual_box[2], self.virtual_box[3], self.virtual_box[1], -1.0, 1.0)
        gl.MatrixMode(gl.MODELVIEW)
        
        gl.ClearColor(0.0, 0.0, 0.0, 0.0)
        gl.Clear(gl.COLOR_BUFFER_BIT)

        clip = (0, 0, self.virtual_size[0], self.virtual_size[1])

        if self.should_draw:

            self.undefine_clip()
            self.draw_transformed(surftree, clip, 0, 0, 1.0, forward, reverse)

            pygame.display.flip()
            

    def draw_render_textures(self, what, forward, reverse):
        """
        This is responsible for rendering things to textures,
        as necessary.
        """

        if not isinstance(what, renpy.display.render.Render):
            return
        
        render_what = False

        if what.clipping:
            if forward.xdy != 0 or forward.ydx != 0:
                render_what = True
                forward = reverse = IDENTITY
        
        
        for child, cxo, cyo, focus, main in what.visible_children:

            if what.forward:
                child_forward = forward * what.forward
                child_reverse = what.reverse * reverse
            else:
                child_forward = forward
                child_reverse = reverse

            self.draw_render_textures(child, child_forward, child_reverse)

            if what.operation == DISSOLVE or what.operation == IMAGEDISSOLVE:
                child.render_to_texture(what.operation_alpha)

            if what.operation == PIXELLATE:
                p = what.operation_parameter
                pc = child
                
                while p > 1:
                    p /= 2
                    pc = self.get_half(pc)
                    
                    
                
        if render_what:
            what.render_to_texture(True)

            
        
    def draw_transformed(self, what, clip, xo, yo, alpha, forward, reverse):

        # If our alpha has hit 0, don't do anything.
        if alpha <= 0.003: # (1 / 256)
            return

        if isinstance(what, gltexture.TextureGrid):

            self.set_clip(clip)
            
            gltexture.blit(
                what,
                xo,
                yo,
                reverse,
                alpha,
                self.environ)

            return

        if not isinstance(what, renpy.display.render.Render):
            raise Exception("Unknown drawing type. " + repr(what))

        # TODO: Implement other draw modes here.

        if what.operation == DISSOLVE:

            self.set_clip(clip)
            
            gltexture.blend(
                what.children[0][0].render_to_texture(what.operation_alpha),
                what.children[1][0].render_to_texture(what.operation_alpha),
                xo,
                yo,
                reverse,
                alpha,
                what.operation_complete,
                self.environ)

            return

        elif what.operation == IMAGEDISSOLVE:

            self.set_clip(clip)

            gltexture.imageblend(
                what.children[0][0].render_to_texture(what.operation_alpha),
                what.children[1][0].render_to_texture(what.operation_alpha),
                what.children[2][0].render_to_texture(what.operation_alpha),
                xo,
                yo,
                reverse,
                alpha,
                what.operation_complete,
                what.operation_parameter,
                self.environ)

            return


        if what.operation == PIXELLATE:
            self.set_clip(clip)

            p = what.operation_parameter
            pc = what.children[0][0]
            
            while p > 1:
                p /= 2
                pc = self.get_half(pc)


            reverse *= renpy.display.render.Matrix2D(1.0 * what.width / pc.width, 0, 0, 1.0 * what.height / pc.height)
                
            # TODO: Make this switch us to nearest-neighbor mode.
            gltexture.blit(
                pc,
                xo,
                yo,
                reverse,
                alpha,
                self.environ,
                nearest=True)

            return
            

                
        # Compute clipping.
        if what.clipping:

            # Non-aligned clipping uses RTT.
            if forward.ydx != 0 or forward.xdy != 0:
                tex = what.render_to_texture(True)
                self.draw_transformed(tex, clip, xo, yo, alpha, forward, reverse)
                return
                
            minx, miny, maxx, maxy = clip

            # Figure out the transformed width and height of this
            # surface.
            tw, th = reverse.transform(what.width, what.height)
            
            minx = max(minx, min(xo, xo + tw))
            maxx = min(maxx, max(xo, xo + tw))
            miny = max(miny, min(yo, yo + th))
            maxy = min(maxy, max(yo, yo + th))

            clip = (minx, miny, maxx, maxy)
            
        
        for child, cxo, cyo, focus, main in what.visible_children:

            cxo, cyo = reverse.transform(cxo, cyo)

            if what.forward:
                child_forward = forward * what.forward
                child_reverse = what.reverse * reverse
            else:
                child_forward = forward
                child_reverse = reverse

            self.draw_transformed(child, clip, xo + cxo, yo + cyo, alpha * what.alpha, child_forward, child_reverse)


    def render_to_texture(self, what, alpha):

        forward = reverse = IDENTITY

        def draw_func():

            if alpha:
                gl.ClearColor(0.0, 0.0, 0.0, 0.0)
            else:
                gl.ClearColor(0.0, 0.0, 0.0, 1.0)
                
            gl.Clear(gl.COLOR_BUFFER_BIT)
            self.undefine_clip()
        
            clip = (0, 0, what.width, what.height)
        
            self.draw_transformed(what, clip, 0, 0, 1.0, forward, reverse)

        what.is_opaque()

        rv = gltexture.texture_grid_from_drawing(what.width, what.height, draw_func, self.rtt)
        return rv
        


    def get_half(self, what):
        """
        Gets a texture grid that's half the size of what..
        """

        if what.half_cache:
            return what.half_cache

        reverse = renpy.display.render.Matrix2D(0.5, 0, 0, .5)
        forward = renpy.display.render.Matrix2D(2.0, 0, 0, 2.0)

        width = max(what.width / 2, 1)
        height = max(what.height / 2, 1)

        def draw_func():
            
            gl.ClearColor(0.0, 0.0, 0.0, 1.0)
                
            gl.Clear(gl.COLOR_BUFFER_BIT)
            self.undefine_clip()

            clip = (0, 0, width, height)
            
            self.draw_transformed(what, clip, 0, 0, 1.0, forward, reverse)

        if isinstance(what, renpy.display.render.Render):
            what.is_opaque()

        rv = gltexture.texture_grid_from_drawing(width, height, draw_func, self.rtt)

        what.half_cache = rv

        return rv

        
            
    def update_mouse(self):
        # The draw routine updates the mouse.

        return


    def mouse_event(self, ev):

        if ev.type == pygame.MOUSEMOTION or \
                ev.type == pygame.MOUSEBUTTONDOWN or \
                ev.type == pygame.MOUSEBUTTONUP:
            
            pass

        x, y = getattr(ev, 'pos', pygame.mouse.get_pos())

        # Screen sizes.
        pw, ph = self.physical_size
        vw, vh = self.virtual_size
        vx0, vy0, vx1, vy1 = self.virtual_box
        
        # Translate to fractional screen.
        x = 1.0 * x / pw
        y = 1.0 * y / ph

        # Translate to virtual size.
        x = vx0 + (vx1 - vx0) * x
        y = vy0 + (vy1 - vy0) * y

        x = int(x)
        y = int(y)

        x = max(0, x)
        x = min(vw, x)
        y = max(0, y)
        y = min(vh, y)

        return x, y
        
        
    def save_screenshot(self, filename):
        """
        Saves a full-size screenshot in the given filename.
        """

        return


    def screenshot(self, scale):
        """
        Returns a string containing the contents of the window, as a PNG.
        """

        return

    def free_memory(self):
        gltexture.dealloc_textures()
    
