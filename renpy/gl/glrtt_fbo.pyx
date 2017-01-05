#@PydevCodeAnalysisIgnore
#cython: profile=False
# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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
from gldraw cimport *
from gldraw import Rtt

import renpy

# The framebuffer object we use.
cdef GLuint fbo

# The root framebuffer.
cdef GLint root_fbo

class FboRtt(Rtt):
    """
    This class uses texture copying to implement Render-to-texture.
    """

    def init(self):
        glGenFramebuffersEXT(1, &fbo)

        cdef int i

        glGetIntegerv(GL_MAX_TEXTURE_SIZE, &i)
        self.size_limit = i
        renpy.display.log.write("FBO Maximum Texture Size: %d", i)

        glGetIntegerv(GL_FRAMEBUFFER_BINDING_EXT, &root_fbo);
        renpy.display.log.write("Root FBO is: %d", root_fbo)

    def deinit(self):
        """
        Called before changing the GL context.
        """

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, root_fbo)
        glDeleteFramebuffersEXT(1, &fbo)

    def begin(self):
        """
        This function should be called when a Render-to-texture
        session begins. It's responsible for setting the GPU to
        RTT mode.
        """

    def render(self, Environ environ, texture, x, y, w, h, draw_func):
        """
        This function is called to trigger a rendering to a texture.
        `x`, `y`, `w`, and `h` specify the location and dimensions of
        the sub-image to render to the texture. `draw_func` is called
        to render the texture.
        """

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)

        glFramebufferTexture2DEXT(
            GL_FRAMEBUFFER_EXT,
            GL_COLOR_ATTACHMENT0_EXT,
            GL_TEXTURE_2D,
            texture,
            0)

        environ.viewport(0, 0, w, h)
        environ.ortho(x, x + w, y, y + h, -1, 1)

        draw_func(x, y, w, h)

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, root_fbo)


    def get_size_limit(self, dimension):
        return self.size_limit
