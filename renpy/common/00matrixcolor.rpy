# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

    class HueMatrix(ColorMatrix):
        """
        :doc: colormatrix

        Returns a matrix that can be used with :tpref:`matrixcolor` to
        rotate the hue by `value` degrees. While `value` can be any number,
        positive or negative, 360 degrees makes a complete rotation.
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
