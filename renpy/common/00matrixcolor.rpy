# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

# This contains ColorMatrix and the various *Matrix classes.

init -1500 python:
    import math as _math

    class ColorMatrix(object):
        """
        :undocumented:

        Documented in text. The base class for various *Matrix classes
        that are intended to return a Matrix that transforms colors.
        """

        def __init__(self, value=1.0):
            self.value = value

        def __call__(self, other, done):

            if type(other) is not type(self):
                return self.get(self.value)

            value = other.value + (self.value - other.value) * done
            return self.get(value)

        def __mul__(self, other):
            return _MultiplyMatrix(self, other)

        def __eq__(self, other):
            if type(self) != type(other):
                return False

            return self.__dict__ == other.__dict__

        def __ne__(self, other):
            return not (self == other)

    class _MultiplyMatrix(ColorMatrix):
        """
        :undocumented:

        This created when two ColorMatrixes are multiplied together.
        """

        def __init__(self, left, right):
            self.left = left
            self.right = right
            self.value = 1.0

        def __call__(self, other, done):
            if type(other) is not type(self):
                return self.left(None, 1.0) * self.right(None, 1.0)

            return self.left(other.left, done) * self.right(other.right, done)


    class IdentityMatrix(ColorMatrix):
        """
        :doc: colormatrix
        :args: ()

        A ColorMatrix that can be used with :tpref:`matrixcolor` that does not
        change the color or alpha of what is supplied to it.

        `value`
            Is ignored.
        """

        def get(self, value):
            return Matrix([ 1.0, 0.0, 0.0, 0.0,
                            0.0, 1.0, 0.0, 0.0,
                            0.0, 0.0, 1.0, 0.0,
                            0.0, 0.0, 0.0, 1.0, ])


    class SaturationMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` that alters
        the saturation of an image, while leaving the alpha channel
        alone.

        `value`
            The amount of saturation in the resulting image. 1.0 is
            the unaltered image, while 0.0 is grayscale.

        `desat`
            This is a 3-element tuple that controls how much of the
            red, green, and blue channels will be placed into all
            three channels of a fully desaturated image. The default
            is based on the constants used for the luminance channel
            of an NTSC television signal. Since the human eye is
            mostly sensitive to green, more of the green channel is
            kept then the other two channels.
        """

        def __init__(self, value, desat=(0.2126, 0.7152, 0.0722)):
            self.value = value
            self.desat = desat

        def get(self, value):
            r, g, b = self.desat

            def I(a, b):
                return a + (b - a) * value

            return Matrix([ I(r, 1), I(g, 0), I(b, 0), 0,
                            I(r, 0), I(g, 1), I(b, 0), 0,
                            I(r, 0), I(g, 0), I(b, 1), 0,
                            0, 0, 0, 1 ])

    class TintMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix can be used with :tpref:`matrixcolor` to tint
        an image, while leaving the alpha channel alone.

        `color`
            The color that the matrix will tint things to. This is passed
            to :func:`Color`, and so may be anything that Color supports
            as its first argument.

        """

        def __init__(self, color):
            self.color = Color(color)

        def __call__(self, other, done):

            if type(other) is not type(self):

                # When not using an old color, we can take
                # r, g, b, and a from self.color.
                r, g, b = self.color.rgb
                a = self.color.alpha

            else:

                # Otherwise, we have to extract from self.color
                # and other.color, and interpolate the results.
                oldr, oldg, oldb = other.color.rgb
                olda = other.color.alpha
                r, g, b = self.color.rgb
                a = self.color.alpha

                r = oldr + (r - oldr) * done
                g = oldg + (g - oldg) * done
                b = oldb + (b - oldb) * done
                a = olda + (a - olda) * done

            # To properly handle premultiplied alpha, the color channels
            # have to be multiplied by the alpha channel.
            r *= a
            g *= a
            b *= a

            # Return a Matrix.
            return Matrix([ r, 0, 0, 0,
                            0, g, 0, 0,
                            0, 0, b, 0,
                            0, 0, 0, a ])

    class BrightnessMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` to change
        the brightness of an image, while leaving the Alpha channel
        alone.

        `value`
            The amount of change in image brightness. This should be
            a number between -1 and 1, with -1 the darkest possible
            image and 1 the brightest.
        """

        def get(self, value):

            return Matrix([ 1, 0, 0, value,
                            0, 1, 0, value,
                            0, 0, 1, value,
                            0, 0, 0, 1 ])

    class OpacityMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` to change
        the opacity of an image, while leaving color channels alone.

        `value`
            The amount the alpha channel should be multiplied by,
            a number between 0.0 and 1.0.
        """

        def get(self, value):

            return Matrix([ value, 0, 0, 0,
                            0, value, 0, 0,
                            0, 0, value, 0,
                            0, 0, 0, value, ])



    class ContrastMatrix(ColorMatrix):

        def get(self, value):
            """
            :doc: colormatrix

            A ColorMatrix that can be used with :tpref:`matrixcolor` to change
            the brightness of an image, while leaving the Alpha channel
            alone.

            `value`
                The contrast value. Values between 0.0 and 1.0 decrease
                the contrast, while values above 1.0 increase the contrast.
            """

            v = value

            step1 = Matrix([ 1, 0, 0, -.5,
                             0, 1, 0, -.5,
                             0, 0, 1, -.5,
                             0, 0, 0, 1, ])

            step2 = Matrix([ v, 0, 0, 0,
                             0, v, 0, 0,
                             0, 0, v, 0,
                             0, 0, 0, 1, ])

            step3 = Matrix([ 1, 0, 0, -.5,
                             0, 1, 0, -.5,
                             0, 0, 1, -.5,
                             0, 0, 0, 1, ])

            return step3 * step2 * step1


    class ColorizeMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` to colorize
        black and white displayables. It uses the color of each pixel
        in the black and white to interpolate between the black color
        and the white color.

        The alpha channel is not touched.

        This is inteded for use with a black and white image (or one that
        has been desaturated with :func:`SaturationMatrix`), and will yield
        strange results when used with images that are not black and white.

        `black_color`, `white_color`
            The colors used in the interpolation.
        """

        def __init__(self, black_color, white_color):
            self.black = Color(black_color)
            self.white = Color(white_color)


        def __call__(self, other, done):

            if type(other) is not type(self):
                other = self

            # Break the colors up into variables.
            obr, obg, obb = other.black.rgb
            owr, owg, owb = other.white.rgb
            nbr, nbg, nbb = self.black.rgb
            nwr, nwg, nwb = self.white.rgb

            # Interpolate to get black and white colors.
            br = obr + (nbr - obr) * done
            bg = obg + (nbg - obg) * done
            bb = obb + (nbb - obb) * done
            wr = owr + (nwr - owr) * done
            wg = owg + (nwg - owg) * done
            wb = owb + (nwb - owb) * done

            # Return the matrix.
            return Matrix([ (wr - br), 0, 0, br,
                            0, (wg - bg), 0, bg,
                            0, 0, (wb - bb), bb,
                            0, 0, 0, 1, ])


    class HueMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` to rotate the hue by
        `value` degrees. While `value` can be any number, positive or negative,
        360 degrees makes a complete rotation. The alpha channel is left alone.
        """

        # from http://www.gskinner.com/blog/archives/2005/09/flash_8_source.html

        def get(self, value):

            h = _math.pi * value / 180.0

            cosVal = _math.cos(h)
            sinVal = _math.sin(h)

            lumR = 0.213
            lumG = 0.715
            lumB = 0.072

            return Matrix([
                lumR + cosVal * (1 - lumR) + sinVal * (-lumR), lumG + cosVal * (-lumG) + sinVal * (-lumG), lumB + cosVal * (-lumB) + sinVal * (1 - lumB), 0.0,
                lumR + cosVal * (-lumR) + sinVal * (0.143), lumG + cosVal * (1 - lumG) + sinVal * (0.140), lumB + cosVal * (-lumB) + sinVal * (-0.283), 0.0,
                lumR + cosVal * (-lumR) + sinVal * (-(1 - lumR)), lumG + cosVal * (-lumG) + sinVal * (lumG), lumB + cosVal * (1 - lumB) + sinVal * (lumB), 0.0,
                0, 0, 0, 1.0 ])


    class InvertMatrix(ColorMatrix):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` to invert
        each of the color channels. The alpha channel is left alone.

        `value`
            The amount to inverty by. 0.0 is not inverted, 1.0 is fully
            inverted. Used to animate inversion.
        """

        def get(self, value):
            d = 1.0 - 2 * value
            v = value

            return Matrix([ d, 0, 0, v,
                            0, d, 0, v,
                            0, 0, d, v,
                            0, 0, 0, 1, ])

    def SepiaMatrix(tint="#ffeec2", desat=(0.2126, 0.7152, 0.0722)):
        """
        :doc: colormatrix

        A function that returns a ColorMatrix that can be used with :tpref:`matrixcolor`
        to sepia-tone a displayable. This is the equivalent of::

            TintMatrix(tint) * SaturationMatrix(0.0, desat)
        """

        return TintMatrix(tint) * SaturationMatrix(0.0, desat)
