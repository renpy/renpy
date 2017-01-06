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

from gl1 cimport *
from gldraw cimport *
import renpy

NONE = 0
BLIT = 1
BLEND = 2
IMAGEBLEND = 3

cdef int round(double d):
    return <int> (d + .5)

cdef class LimitedEnviron(Environ):
    """
    This is an OpenGL environment that uses a limited fixed-function
    pipeline. This will work with any GL or GLES system that has at
    least 2 texture units.

    (It's missing some functionality, like the ability to change the
     alpha of an imagedissolve or dissolve, and the ability to
     imagedissolve.)
    """

    cdef object last

    def init(self):

        # The last blend environ used.
        self.last = NONE

        # Disable imagedissolve.
        renpy.display.less_imagedissolve = True

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
                     color_arg1=GL_PREVIOUS,
                     color_arg2=GL_CONSTANT,
                     color_source0=GL_SRC_COLOR,
                     color_source1=GL_SRC_COLOR,
                     color_source2=GL_SRC_COLOR,
                     color_scale=1.0,
                     alpha_function=GL_MODULATE,
                     alpha_arg0=GL_TEXTURE,
                     alpha_arg1=GL_PREVIOUS,
                     alpha_arg2=GL_CONSTANT,
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

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_RGB, color_function)
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_ALPHA, alpha_function)

        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE0_RGB, color_arg0)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND0_RGB, color_source0)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE1_RGB, color_arg1)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND1_RGB, color_source1)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE2_RGB, color_arg2)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND2_RGB, color_source2)

        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE0_ALPHA, alpha_arg0)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND0_ALPHA, alpha_source0)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE1_ALPHA, alpha_arg1)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND1_ALPHA, alpha_source1)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE2_ALPHA, alpha_arg2)
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND2_ALPHA, alpha_source2)

        glTexEnvf(GL_TEXTURE_ENV, GL_RGB_SCALE, color_scale)
        glTexEnvf(GL_TEXTURE_ENV, GL_ALPHA_SCALE, alpha_scale)


    cdef void blit(self):

        if self.last != BLIT:

            # Set unit 0 to modulate.

            self.combine_mode(GL_TEXTURE0,
                              color_function=GL_MODULATE,
                              alpha_function=GL_MODULATE)


            # Disable unit 1.
            self.disable(GL_TEXTURE1)

            self.last = BLIT

    cdef void blend(self, double fraction):

        if self.last != BLEND:

            # Get texture 0.
            self.combine_mode(GL_TEXTURE0,
                              color_function=GL_REPLACE,
                              alpha_function=GL_REPLACE)

            # Use interpolate to combine texture 0 with texture 1, as
            # controlled by the constant of texture unit 1.
            self.combine_mode(GL_TEXTURE1,
                              color_function=GL_INTERPOLATE,
                              alpha_function=GL_INTERPOLATE)

            self.last = BLEND

        cdef float *fractions = [ fraction, fraction, fraction, fraction ]

        glActiveTextureARB(GL_TEXTURE1)
        glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, fractions)

    cdef void imageblend(self, double fraction, int ramp):
        # Imageblend doesn't work on GLES.
        pass

    cdef void set_vertex(self, float *vertices):
        glVertexPointer(2, GL_FLOAT, 0, <GLubyte *> vertices)
        glEnableClientState(GL_VERTEX_ARRAY)

    cdef void set_texture(self, int unit, float *coords):
        if unit == 0:
            glClientActiveTextureARB(GL_TEXTURE0)
        elif unit == 1:
            glClientActiveTextureARB(GL_TEXTURE1)
        elif RENPY_THIRD_TEXTURE and unit == 2:
            glClientActiveTextureARB(GL_TEXTURE2)
        else:
            return

        if coords is not NULL:
            glTexCoordPointer(2, GL_FLOAT, 0, <GLubyte *> coords)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        else:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    cdef void set_color(self, float r, float g, float b, float a):
        glColor4f(r, g, b, a)


    cdef void ortho(self, double left, double right, double bottom, double top, double near, double far):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(left, right, bottom, top, near, far)
        glMatrixMode(GL_MODELVIEW)

    cdef void set_clip(self, tuple clip_box, GLDraw draw):

        cdef double minx, miny, maxx, maxy
        cdef double vwidth, vheight
        cdef double px, py, pw, ph
        cdef int cx, cy, cw, ch
        cdef int psw, psh

        minx, miny, maxx, maxy = clip_box
        psw, psh = draw.physical_size

        if draw.clip_rtt_box is None:

            vwidth, vheight = draw.virtual_size
            px, py, pw, ph = draw.physical_box

            minx = px + (minx / vwidth) * pw
            maxx = px + (maxx / vwidth) * pw

            miny = py + (miny / vheight) * ph
            maxy = py + (maxy / vheight) * ph

            miny = psh - miny
            maxy = psh - maxy

            glEnable(GL_SCISSOR_TEST)
            glScissor(<GLint> round(minx), <GLint> round(maxy), <GLint> round(maxx - minx), <GLsizei> round(miny - maxy))

        else:

            cx, cy, cw, ch = draw.clip_rtt_box

            glEnable(GL_SCISSOR_TEST)
            glScissor(<GLint> round(minx - cx), <GLint> round(miny - cy), <GLint> round(maxx - minx), <GLint> round(maxy - miny))

    cdef void unset_clip(self, GLDraw draw):
        glDisable(GL_SCISSOR_TEST)

    cdef void viewport(self, int x, int y, int width, int height):
        glViewport(x, y, width, height)
