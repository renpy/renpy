# This file contains the code required to set up (and change) OpenGL texture
# environments to implement various effects.

import _renpy_tegl as gl

# Constants, that are used to store the last kind of blend a class was
# used for. (So we can avoid changing the GL state unnecessarily.)
NONE = 0
BLIT = 1
BLEND = 2
IMAGEBLEND = 3

class GLEnviron(object):

    def init_common(self):
        """
        Code that is, for now, common to the different environments, and
        doesn't need to be changed over the course of execution.
        """

        gl.Enable(gl.BLEND)
        gl.BlendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)

    
    def blit_environ(self):
        """
        Set up a normal blit environment. The texture to be blitted should
        be TEXTURE0.
        """

        raise Exception("Not implemented.")

    def blend_environ(self, fraction):
        """
        Set up an environment that blends between TEXTURE0 and
        TEXTURE1.

        `fraction` is the fraction of the blend complete.
        """

        raise Exception("Not implemented.")


    def imageblend_environ(self, fraction, ramp):
        """
        Set up an environment that does an imageblend between TEXTURE0 and
        TEXTURE1. TEXTURE2 should be an alpha texture that controls the
        blending.

        `fraction` is the fraction of the blend complete.
        `ramp` is the length of the ramp.
        """
        raise Exception("Not implemented.")
        
        
class FixedFunctionGLEnviron(GLEnviron):
    """
    This is an OpenGL environment that uses the fixed-function pipeline.

    It requires ARB_texture_env_combine and ARB_texture_env_crossbar to
    work.
    """

    def __init__(self):
        
        # The last blend environ used.
        self.last_environ = NONE

        self.init_common()
        
    def blit_environ(self):

        if self.last_environ != BLIT:

            gl.ActiveTextureARB(gl.TEXTURE0_ARB)
            gl.Enable(gl.TEXTURE_2D)

            gl.TexEnvi(gl.TEXTURE_ENV, gl.TEXTURE_ENV_MODE, gl.MODULATE)
            
            # Disable texture units 1, 2 and 3.
            gl.ActiveTextureARB(gl.TEXTURE1_ARB)
            gl.Disable(gl.TEXTURE_2D)
            gl.ActiveTextureARB(gl.TEXTURE2_ARB)
            gl.Disable(gl.TEXTURE_2D)
            gl.ActiveTextureARB(gl.TEXTURE3_ARB)
            gl.Disable(gl.TEXTURE_2D)
            
            self.last_environ = BLIT

    
            
    
        
        
