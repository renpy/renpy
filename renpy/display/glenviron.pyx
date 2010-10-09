#cython: profile=False
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

# This file contains the code required to set up (and change) OpenGL texture
# environments to implement various effects.

from gl cimport *

try:
    import _renpy_tegl as gl; gl
    import _renpy_pysdlgl as pysdlgl; pysdlgl
except ImportError:
    gl = None
    pysdlgl = None

import glshader

# Constants, that are used to store the last kind of blend a class was
# used for. (So we can avoid changing the GL state unnecessarily.)
NONE = 0
BLIT = 1
BLEND = 2
IMAGEBLEND = 3

class Environ(object):

    def blit(self):
        """
        Set up a normal blit environment. The texture to be blitted should
        be TEXTURE0.
        """

        raise Exception("Not implemented.")

    def blend(self, fraction):
        """
        Set up an environment that blends from TEXTURE0 to TEXTURE1.

        `fraction` is the fraction of the blend complete.
        """

        raise Exception("Not implemented.")


    def imageblend(self, fraction, ramp):
        """
        Setup an environment that does an imageblend from TEXTURE1 to TEXTURE2.
        The controlling image is TEXTURE0.

        `fraction` is the fraction of the blend complete.
        `ramp` is the length of the ramp.
        """

        raise Exception("Not implemented.")
        
        
class FixedFunctionEnviron(Environ):
    """
    This is an OpenGL environment that uses the fixed-function pipeline.

    It requires ARB_texture_env_combine and ARB_texture_env_crossbar to
    work.
    """

    def init(self):
        
        # The last blend environ used.
        self.last = NONE

        # The last ramp length asked for.
        self.last_ramp = -1

        # The last ramplen actually used.
        self.last_ramplen = -1

        # A table that maps ramp lengths to the setup of the fixed-function
        # units.        
        self.ramp_setup = [
            # Fields are:
            # ramp length,
            # unit 1 scale,
            # unit 2 function,
            # unit 2 scale,

            (256, 1.0, GL_REPLACE, 1.0),
            (128, 1.0, GL_REPLACE, 2.0),
            (64, 1.0, GL_REPLACE, 4.0),
            (32, 1.0, GL_ADD, 4.0),
            (16, 2.0, GL_ADD, 4.0),
            (8, 4.0, GL_ADD, 4.0),
            ]
            

    def deinit(self):
        """
        Called before changing the GL context.
        """

        return

    def disable(self, unit):
        """
        Disables the given texture combiner.
        """

        glActiveTextureARB(unit)
        glDisable(GL_TEXTURE_2D)
        
    def combine_mode(self, unit,
                     color_function=GL_MODULATE,
                     color_arg0=GL_TEXTURE,
                     color_arg1=GL_PREVIOUS_ARB,
                     color_arg2=GL_CONSTANT_ARB,
                     color_source0=GL_SRC_COLOR,
                     color_source1=GL_SRC_COLOR,
                     color_source2=GL_SRC_COLOR,
                     color_scale=1.0,
                     alpha_function=GL_MODULATE,
                     alpha_arg0=GL_TEXTURE,
                     alpha_arg1=GL_PREVIOUS_ARB,
                     alpha_arg2=GL_CONSTANT_ARB,
                     alpha_source0=GL_SRC_ALPHA,
                     alpha_source1=GL_SRC_ALPHA,
                     alpha_source2=GL_SRC_ALPHA,
                     alpha_scale=1.0,
                     enable=True):

        
        glActiveTextureARB(unit)

        if enable:
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)
            
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE_ARB)
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_RGB_ARB, color_function)
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_ALPHA_ARB, alpha_function)

        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE0_RGB_ARB, color_arg0)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND0_RGB_ARB, color_source0)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE1_RGB_ARB, color_arg1)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND1_RGB_ARB, color_source1)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE2_RGB_ARB, color_arg2)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND2_RGB_ARB, color_source2)

        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE0_ALPHA_ARB, alpha_arg0)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND0_ALPHA_ARB, alpha_source0)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE1_ALPHA_ARB, alpha_arg1)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND1_ALPHA_ARB, alpha_source1)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE2_ALPHA_ARB, alpha_arg2)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND2_ALPHA_ARB, alpha_source2)

        glTexEnvf(GL_TEXTURE_ENV, GL_RGB_SCALE_ARB, color_scale)
        glTexEnvf(GL_TEXTURE_ENV, GL_ALPHA_SCALE, alpha_scale)

        
    def blit(self):

        if self.last != BLIT:

            # Set unit 0 to modulate.

            self.combine_mode(GL_TEXTURE0_ARB,
                              color_function=GL_MODULATE,
                              alpha_function=GL_MODULATE)


            # Disable units 1, 2 and 3.
            self.disable(GL_TEXTURE1_ARB)
            self.disable(GL_TEXTURE2_ARB)
            self.disable(GL_TEXTURE3_ARB)
            
            self.last = BLIT
        
    def blend(self, fraction):

        if self.last != BLEND:

            # Get texture 0.
            self.combine_mode(GL_TEXTURE0_ARB,
                              color_function=GL_REPLACE,
                              alpha_function=GL_REPLACE)

            # Use interpolate to combine texture 0 with texture 1, as
            # controlled by the constant of texture unit 1.
            self.combine_mode(GL_TEXTURE1_ARB,
                              color_function=GL_INTERPOLATE_ARB,
                              color_arg0=GL_TEXTURE1_ARB,
                              color_arg1=GL_TEXTURE0_ARB,
                              alpha_function=GL_INTERPOLATE_ARB,
                              alpha_arg0=GL_TEXTURE1_ARB,
                              alpha_arg1=GL_TEXTURE0_ARB)

            # Combine the interpolated result with the primary color, to
            # allow for tinting and alpha adjustments.
            self.combine_mode(GL_TEXTURE2_ARB,
                              color_function=GL_MODULATE,
                              color_arg0=GL_PREVIOUS_ARB,
                              color_arg1=GL_PRIMARY_COLOR_ARB,
                              alpha_function=GL_MODULATE,
                              alpha_arg0=GL_PREVIOUS_ARB,
                              alpha_arg1=GL_PRIMARY_COLOR_ARB,
                              enable=False)
            
            # Disable texture unit 3.
            self.disable(GL_TEXTURE3_ARB)
            
            self.last = BLEND

        cdef float *fractions = [ fraction, fraction, fraction, fraction ]
                    
        glActiveTextureARB(GL_TEXTURE1_ARB)
        glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, fractions)

        
        
    def imageblend(self, fraction, ramp):

        if self.last != IMAGEBLEND or self.last_ramp != ramp:

            # Figure out the details of the ramp.
            for i in self.ramp_setup:
                ramplen, t0scale, t1function, t1scale = i

                # We round the ramplen down, unless we're below the
                # smallest size, in which case we increase it.
                if ramplen <= ramp:
                    break

            # Unit 0 loads in the control image, and adds/subtracts an
            # offset to/from it. (We'll set it up to subtract here,
            # and change this later on as necessary.)
            # 
            # It multiplies this result by up to 4.
            self.combine_mode(GL_TEXTURE0_ARB,
                              color_function=GL_SUBTRACT_ARB,
                              alpha_function=GL_SUBTRACT_ARB,
                              color_arg1=GL_CONSTANT_ARB,
                              alpha_arg1=GL_CONSTANT_ARB,
                              color_scale=t0scale,
                              alpha_scale=t0scale)

            # Unit 1 will multiply the result of stage 1 by up to 8. 
            #
            # It also takes the first source texture, but we don't
            # access it directly yet.
            self.combine_mode(GL_TEXTURE1_ARB,
                              color_function=t1function,
                              alpha_function=t1function,
                              color_arg0=GL_PREVIOUS_ARB,
                              color_arg1=GL_PREVIOUS_ARB,
                              alpha_arg0=GL_PREVIOUS_ARB,
                              alpha_arg1=GL_PREVIOUS_ARB,
                              color_scale=t1scale,
                              alpha_scale=t1scale)

            # Unit 2 uses the result of unit 1 to interpolate between the
            # unit 1 and unit 2 textures.
            self.combine_mode(GL_TEXTURE2_ARB,
                              color_function=GL_INTERPOLATE_ARB,
                              alpha_function=GL_INTERPOLATE_ARB,
                              color_arg0=GL_TEXTURE2_ARB,
                              color_arg1=GL_TEXTURE1_ARB,
                              color_arg2=GL_PREVIOUS_ARB,
                              alpha_arg0=GL_TEXTURE2_ARB,
                              alpha_arg1=GL_TEXTURE1_ARB,
                              alpha_arg2=GL_PREVIOUS_ARB)

            # Finally, Unit 3 modulates the result of unit 2 with the color.
            self.combine_mode(GL_TEXTURE3_ARB,
                              color_function=GL_MODULATE,
                              color_arg0=GL_PREVIOUS_ARB,
                              color_arg1=GL_PRIMARY_COLOR_ARB,
                              alpha_function=GL_MODULATE,
                              alpha_arg0=GL_PREVIOUS_ARB,
                              alpha_arg1=GL_PRIMARY_COLOR_ARB,
                              enable=False)
            
            self.last = IMAGEBLEND
            self.last_ramp = ramp
            self.last_ramplen = ramplen

        # Compute the offset to apply to the alpha.            
        start = -1.0
        end = self.last_ramplen / 256.0        
        offset = start + ( end - start) * fraction

        # Decide if we're adding or subtracting.
        if offset < 0:
            function = GL_SUBTRACT_ARB
            offset = -offset
        else:
            function = GL_ADD

        # Setup unit 0 as appropriate.
        glActiveTextureARB(GL_TEXTURE0_ARB)
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_RGB_ARB, function)
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_ALPHA_ARB, function)

        cdef float *offsets = [ offset, offset, offset, offset ]

        glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, offsets)

                              
class ShaderEnviron(object):
    """
    This is an environment that uses shaders.
    """

    def init(self):

        self.blit_program = glshader.blit_program()
        self.blit_tex0_uniform = glGetUniformLocationARB(
            self.blit_program,
            "tex0")

        self.blend_program = glshader.blend_program()
        self.blend_done_uniform = glGetUniformLocationARB(
            self.blend_program,
            "done")
        self.blend_tex0_uniform = glGetUniformLocationARB(
            self.blend_program,
            "tex0")
        self.blend_tex1_uniform = glGetUniformLocationARB(
            self.blend_program,
            "tex1")

        self.imageblend_program = glshader.imageblend_program()
        self.imageblend_tex0_uniform = glGetUniformLocationARB(
            self.imageblend_program,
            "tex0")
        self.imageblend_tex1_uniform = glGetUniformLocationARB(
            self.imageblend_program,
            "tex1")
        self.imageblend_tex2_uniform = glGetUniformLocationARB(
            self.imageblend_program,
            "tex2")
        self.imageblend_offset_uniform = glGetUniformLocationARB(
            self.imageblend_program,
            "offset")
        self.imageblend_multiplier_uniform = glGetUniformLocationARB(
            self.imageblend_program,
            "multiplier")

        self.last = NONE
        

    def deinit(self):
        """
        Called before changing the GL context.
        """

        glDeleteObjectARB(self.blit_program)
        glDeleteObjectARB(self.blend_program)
        glDeleteObjectARB(self.imageblend_program)
        
        return

    def blit(self):

        if self.last != BLIT:

            glUseProgramObjectARB(self.blit_program)
            glUniform1iARB(self.blit_tex0_uniform, 0)
            
            self.last = BLIT
        
    def blend(self, fraction):

        if self.last != BLEND:

            glUseProgramObjectARB(self.blend_program)
            glUniform1iARB(self.blend_tex0_uniform, 0)
            glUniform1iARB(self.blend_tex1_uniform, 1)
            
            self.last = BLEND

        glUniform1fARB(self.blend_done_uniform, fraction)
        
        
    def imageblend(self, fraction, ramp):

        if self.last != IMAGEBLEND:
            glUseProgramObjectARB(self.imageblend_program)
            glUniform1iARB(self.imageblend_tex0_uniform, 0)
            glUniform1iARB(self.imageblend_tex1_uniform, 1)
            glUniform1iARB(self.imageblend_tex2_uniform, 2)

            self.last = IMAGEBLEND

        # Prevent a DBZ if the user gives us a 0 ramp.
        if ramp < 1:
            ramp = 1
            
        # Compute the offset to apply to the alpha.            
        start = -1.0
        end = ramp / 256.0        
        offset = start + ( end - start) * fraction

        # Setup the multiplier and the offset.
        glUniform1fARB(self.imageblend_multiplier_uniform, 256.0 / ramp)
        glUniform1fARB(self.imageblend_offset_uniform, offset)



class Rtt(object):
    """
    Subclasses of this class handle rendering to a texture.
    """

    def begin(self):
        """
        This function should be called when a Render-to-texture
        session begins. It's responsible for setting the GPU to
        RTT mode.
        """

        raise Exception("Not implemented.")

    def render(self, texture, x, y, w, h, draw_func):
        """
        This function is called to trigger a rendering to a texture.
        `x`, `y`, `w`, and `h` specify the location and dimensions of
        the sub-image to render to the texture. `draw_func` is called
        to render the texture.
        """

        raise Exception("Not implemented.")

    def end(self):
        """
        This is called when a Render-to-texture session ends.
        """

        raise Exception("Not implemented.")



class CopyRtt(object):
    """
    This class uses texture copying to implement Render-to-texture.
    """

    def init(self):
        pass
    
    
    def deinit(self):
        """
        Called before changing the GL context.
        """

        return

    def begin(self):
        """
        This function should be called when a Render-to-texture
        session begins. It's responsible for setting the GPU to
        RTT mode.
        """

    def render(self, texture, x, y, w, h, draw_func):
        """
        This function is called to trigger a rendering to a texture.
        `x`, `y`, `w`, and `h` specify the location and dimensions of
        the sub-image to render to the texture. `draw_func` is called
        to render the texture.
        """

        glViewport(0, 0, w, h)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(x, x + w, y, y + h, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        draw_func()
        
        glBindTexture(GL_TEXTURE_2D, texture)

        glCopyTexSubImage2D(
            GL_TEXTURE_2D,
            0,
            0,
            0,
            0,
            0,
            w,
            h)        
            

    def end(self):
        """
        This is called when a Render-to-texture session ends.
        """


class FramebufferRtt(object):
    """
    This class uses the framebuffer object to do RTT.
    """

    def init(self):

        # This maps a texture to the framebuffer object that
        # can write to that texture.
        self.texture_to_fbo = { }
        
    def deinit(self):
        """
        Called before changing the GL context.
        """

        cdef GLuint i
        
        for i in self.texture_to_fbo.itervalues():
            glDeleteFramebuffersEXT(1, &i)

        self.texture_to_fbo.clear()
            

    def get_fbo(self, texture):

        if texture in self.texture_to_fbo:
            return self.texture_to_fbo[texture]

        cdef GLuint fbo
        
        glGenFramebuffersEXT(1, &fbo)

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)

        glFramebufferTexture2DEXT(
           GL_FRAMEBUFFER_EXT,
           GL_COLOR_ATTACHMENT0_EXT,
           GL_TEXTURE_2D,
           texture,
           0)

        self.texture_to_fbo[texture] = fbo
        return fbo
        
    
    def begin(self):
        """
        This function should be called when a Render-to-texture
        session begins. It's responsible for setting the GPU to
        RTT mode.
        """
        
    def render(self, texture, x, y, w, h, draw_func):
        """
        This function is called to trigger a rendering to a texture.
        `x`, `y`, `w`, and `h` specify the location and dimensions of
        the sub-image to render to the texture. `draw_func` is called
        to render the texture. 
        """

        fbo = self.get_fbo(texture)
        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)

        glViewport(0, 0, w, h)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(x, x + w, y, y + h, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        draw_func()


    def end(self):
        """
        This is called when a Render-to-texture session ends.
        """

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

