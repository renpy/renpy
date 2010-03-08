# IMPORTANT NOTE: The drawing code should handle cases where a surface is
# added to a Render (instead of a TextureGrid) by uploading that surface to
# the graphics card.

# IMPORTANT NOTE: This code should fail gracefully-ish if _renpy_tegl can't be
# imported.

import renpy

import pygame
import os
import sys
import math

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

        self.log(renpy.version)
        
        self.virtual_size = virtual_size

        try:
        
            if fullscreen:
                self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            else:
                self.window = pygame.display.set_mode(physical_size, pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF)        

        except pygame.error, e:
            self.log("Could not get pygame screen: %r", e)

            return False

        self.physical_size = self.window.get_size()

        self.log("Screen sizes: virtual=%r physical=%r" % (self.virtual_size, self.physical_size))

        # Set some default settings.
        gl.ClearColor(0.0, 0.0, 0.0, 0.0)
        gl.Enable(gl.BLEND)
        gl.BlendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)
        
        if not self.did_init:
            return self.init()
        else:
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
        
        def use_subsystem(self, envvar, envval, *req_ext):
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
            "shader",
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

        
    def draw_screen(self, surftree, fullscreen_video):
        """
        Draws the screen.
        """

        forward = reverse = renpy.display.render.IDENTITY

        surftree.is_opaque()

        # TODO: Clipping.
        # TODO: Work out the actual viewport width and height.
        
        gl.Viewport(0, 0, self.physical_size[0], self.physical_size[1])

        gl.MatrixMode(gl.PROJECTION)
        gl.LoadIdentity()
        gl.Ortho(0.0, self.virtual_size[0], self.virtual_size[1], 0.0, -1.0, 1.0)
        gl.MatrixMode(gl.MODELVIEW)

        gl.Clear(gl.COLOR_BUFFER_BIT)
        
        self.draw_transformed(surftree, 0, 0, 1.0, forward, reverse)

        pygame.display.flip()
        

        
    def draw_transformed(self, what, xo, yo, alpha, forward, reverse):

        # If our alpha has hit 0, don't do anything.
        if alpha <= 0.003: # (1 / 256)
            return

        if isinstance(what, gltexture.TextureGrid):

            gltexture.blit(
                [ (what, xo, yo) ],
                reverse,
                alpha,
                self.environ)

            return

        if not isinstance(what, renpy.display.render.Render):
            raise Exception("Unknown drawing type. " + repr(what))

        # TODO: Implement other draw modes here.

        # TODO: Deal with clipping.

        for child, cxo, cyo, focus, main in what.visible_children:

            cxo, cyo = reverse.transform(cxo, cyo)

            if what.forward:
                child_forward = forward * what.forward
                child_reverse = what.reverse * reverse
            else:
                child_forward = forward
                child_reverse = reverse

            self.draw_transformed(child, xo + cxo, yo + cyo, alpha * what.alpha, child_forward, child_reverse)


    def update_mouse(self):
        # The draw routine updates the mouse.

        return


    def mouse_event(self, ev):

        if ev.type == pygame.MOUSEMOTION or \
                ev.type == pygame.MOUSEBUTTONDOWN or \
                ev.type == pygame.MOUSEBUTTONUP:
            
            pass



        
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
        pass

    
    
