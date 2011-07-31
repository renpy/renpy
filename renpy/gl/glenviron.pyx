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

# This file contains the code required to set up (and change) OpenGL texture
# environments to implement various effects.

from gl cimport *

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
        
