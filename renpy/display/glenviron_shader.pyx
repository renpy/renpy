#cython: profile=False
# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

from gl cimport *

from renpy.display.glenviron import *
import renpy.display.glshader as glshader

class ShaderEnviron(Environ):
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
