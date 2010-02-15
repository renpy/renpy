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

    def disable(self, unit):
        """
        Disables the given texture combiner.
        """

        gl.ActiveTextureARB(unit)
        gl.Disable(gl.TEXTURE_2D)
        
    def combine_mode(self, unit,
                     color_function=gl.MODULATE,
                     color_arg0=gl.TEXTURE,
                     color_arg1=gl.PREVIOUS_ARB,
                     color_arg2=gl.CONSTANT_ARB,
                     color_source0=gl.SRC_COLOR,
                     color_source1=gl.SRC_COLOR,
                     color_source2=gl.SRC_COLOR,
                     color_scale=1.0,
                     alpha_function=gl.MODULATE,
                     alpha_arg0=gl.TEXTURE,
                     alpha_arg1=gl.PREVIOUS_ARB,
                     alpha_arg2=gl.CONSTANT_ARB,
                     alpha_source0=gl.SRC_ALPHA,
                     alpha_source1=gl.SRC_ALPHA,
                     alpha_source2=gl.SRC_ALPHA,
                     alpha_scale=1.0):

        gl.ActiveTextureARB(unit)
        gl.Enable(gl.TEXTURE_2D)

        gl.TexEnvi(gl.TEXTURE_ENV, gl.TEXTURE_ENV_MODE, gl.COMBINE_ARB)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.COMBINE_RGB_ARB, color_function)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.COMBINE_ALPHA_ARB, alpha_function)

        gl.TexEnvi(gl.TEXTURE_ENV, gl.SOURCE0_RGB_ARB, color_arg0)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.OPERAND0_RGB_ARB, color_source0)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.SOURCE1_RGB_ARB, color_arg1)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.OPERAND1_RGB_ARB, color_source1)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.SOURCE2_RGB_ARB, color_arg2)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.OPERAND2_RGB_ARB, color_source2)

        gl.TexEnvi(gl.TEXTURE_ENV, gl.SOURCE0_ALPHA_ARB, alpha_arg0)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.OPERAND0_ALPHA_ARB, alpha_source0)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.SOURCE1_ALPHA_ARB, alpha_arg1)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.OPERAND1_ALPHA_ARB, alpha_source1)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.SOURCE2_ALPHA_ARB, alpha_arg2)
        gl.TexEnvi(gl.TEXTURE_ENV, gl.OPERAND2_ALPHA_ARB, alpha_source2)

        gl.TexEnvf(gl.TEXTURE_ENV, gl.RGB_SCALE_ARB, color_scale)
        gl.TexEnvf(gl.TEXTURE_ENV, gl.ALPHA_SCALE_ARB, alpha_scale)

        
    def blit_environ(self):

        if self.last_environ != BLIT:

            gl.ActiveTextureARB(gl.TEXTURE0_ARB)
            gl.Enable(gl.TEXTURE_2D)

            gl.TexEnvi(gl.TEXTURE_ENV, gl.TEXTURE_ENV_MODE, gl.MODULATE)
            
            # Disable texture units 1, 2 and 3.
            self.disable(gl.TEXTURE1_ARB)
            self.disable(gl.TEXTURE2_ARB)
            self.disable(gl.TEXTURE3_ARB)
            
            self.last_environ = BLIT
        
    def blend_environ(self, fraction):

        if self.last_environ != BLEND:

            # Get texture 0.
            self.combine_mode(gl.TEXTURE0_ARB,
                              color_function=gl.REPLACE)

            # Use interpolate to combine texture 0 with texture 1, as
            # controlled by the constant of texture unit 1.
            self.combine_mode(gl.TEXTURE1_ARB,
                              color_function=gl.INTERPOLATE_ARB,
                              alpha_function=gl.INTERPOLATE_ARB)

            # Combine the interpolated result with the primary color, to
            # allow for tinting and alpha adjustments.
            self.combine_mode(gl.TEXTURE2_ARB,
                              color_function=gl.MODULATE,
                              alpha_function=gl.MODULATE,
                              color_source1=gl.PRIMARY_COLOR_ARB,
                              alpha_source1=gl.PRIMARY_COLOR_ARB)
            
            # Disable texture unit 3.
            self.disable(gl.TEXTURE3_ARB)
            
            self.last_environ = BLEND
                            
        gl.ActiveTextureARB(gl.TEXTURE1_ARB)
        gl.TexEnvfv(gl.TEXTURE_ENV, gl.TEXTURE_ENV_COLOR, (fraction, fraction, fraction, fraction))


            
        
        
