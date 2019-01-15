# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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


from __future__ import print_function

import renpy.display
import colorsys


class Color(tuple):
    """
    :doc: color class
    :args: (color=None, hls=None, hsv=None, rgb=None, alpha=1.0)
    :name: Color

    The Color class is used to represent and manipulate colors and convert
    between various color spaces. It also represents opacity in the form
    of an alpha.

    When creating a Color, at one of the `color`, `hls`, `hsv`, or `rgb`
    arguments should be supplied. (If all are None, None is returned.)

    `color`
        The color, in one of the standard formats Ren'Py understands. These
        are:

        * A Color object.
        * An (r, g, b) or (r, g, b, a) tuple, in which all the numbers are
          between 0 and 255.
        * A string giving a hexadecimal color, in the form "#rgb", "#rgba",
          "#rrggbb", or "#rrggbbaa".

    `hls`
        A color in the hue-lightness-saturation color space. This should
        be supplied a three-component tuple, where each component is between
        0.0 and 1.0.

    `hsv`
        A color in the hue-saturation-value color space. This should
        be supplied a three-component tuple, where each component is between
        0.0 and 1.0.

    `rgb`
        A color in the red-green-blue color space. This should
        be supplied a three-component tuple, where each component is between
        0.0 and 1.0.

    If the supplied color does not contain an alpha value, `alpha` is used.
    `alpha` must be between 0.0 and 1.0.

    Color objects can be used as 4-component tuples, where the components
    are (red, green, blue, and alpha). When used as a tuple, the value
    of each component is between 0 and 255.

    Color objects support the +, -, and * operators, representing
    component-wise addition, subtraction, and multiplication. Some uses
    of these operators can cause the creation of colors with components
    that are not in the supported range. Such colors should not be passed
    to other parts of Ren'Py. (The normalize method can be called to return
    a new color with the components limited to the proper range.)

    A Color object has the following properties:

    .. attribute:: hls

        Returns the color as a tuple of three floating point numbers giving
        hue, lightness, and saturation. Each component ranges between 0.0 and 1.0.

    .. attribute:: hsv

        Returns the color as a tuple of three floating point numbers giving
        hue, saturation, and value. Each component ranges between 0.0 and 1.0.

    .. attribute:: rgb

        Returns the color as a tuple of three floating point numbers giving
        the red, green, and blue components. Each component ranges between 0.0
        and 1.0.

    .. attribute:: alpha

        Returns the alpha (opacity) of this Color as a number between 0.0 and
        1.0, where 0.0 is transparent and 1.0 is opaque.

    .. attribute:: hexcode

        Returns a string containing a hex color code of the form #rrggbbaa
        or #rrggbb.

    Color objects have the following methods. Since Colors are immutable,
    these methods always return a new Color object.
    """

    _rgb = None
    _hls = None
    _hsv = None
    _alpha = None

    def __new__(cls, color=None, hls=None, hsv=None, rgb=None, alpha=1.0):

        if color is not None:
            c = color

            if isinstance(c, tuple):
                if isinstance(c, Color):
                    return c

                if len(c) == 4:
                    return tuple.__new__(cls, c)

                if len(c) == 3:
                    return tuple.__new__(cls, c + (int(255 * alpha),))

            if isinstance(c, basestring):
                if c[0] == '#':
                    c = c[1:]

                if len(c) == 6:
                    r = int(c[0]+c[1], 16)
                    g = int(c[2]+c[3], 16)
                    b = int(c[4]+c[5], 16)
                    a = int(alpha * 255)
                elif len(c) == 8:
                    r = int(c[0]+c[1], 16)
                    g = int(c[2]+c[3], 16)
                    b = int(c[4]+c[5], 16)
                    a = int(c[6]+c[7], 16)
                elif len(c) == 3:
                    r = int(c[0], 16) * 0x11
                    g = int(c[1], 16) * 0x11
                    b = int(c[2], 16) * 0x11
                    a = int(alpha * 255)
                elif len(c) == 4:
                    r = int(c[0], 16) * 0x11
                    g = int(c[1], 16) * 0x11
                    b = int(c[2], 16) * 0x11
                    a = int(c[3], 16) * 0x11
                else:
                    raise Exception("Color string {!r} must be 3, 4, 6, or 8 hex digits long.".format(c))

                return tuple.__new__(cls, (r, g, b, a))

        if hsv is not None:
            rgb = colorsys.hsv_to_rgb(*hsv)

        if hls is not None:
            hsv = None
            rgb = colorsys.hls_to_rgb(*hls)

        if rgb is not None:
            r = int(rgb[0] * 255)
            g = int(rgb[1] * 255)
            b = int(rgb[2] * 255)
            a = int(alpha * 255)

            rv = tuple.__new__(cls, (r, g, b, a))
            rv._rgb = rgb
            rv._hls = hls
            rv._hsv = hsv
            rv._alpha = alpha

            return rv

        if color is None:
            return None

        raise Exception("Not a color: %r" % (color,))

    @property
    def hexcode(self):
        if self.alpha != 1.0:
            return "#{self[0]:02x}{self[1]:02x}{self[2]:02x}{self[3]:02x}".format(self=self)
        else:
            return "#{self[0]:02x}{self[1]:02x}{self[2]:02x}".format(self=self)

    def __repr__(self):
        return "<Color {}>".format(self.hexcode)

    def __getnewargs__(self):
        return (tuple(self), )

    @property
    def rgb(self):
        if self._rgb is None:
            self._rgb = (
                self[0] / 255.0,
                self[1] / 255.0,
                self[2] / 255.0,
                )

        return self._rgb

    @property
    def hls(self):
        if self._hls is None:
            self._hls = colorsys.rgb_to_hls(*self.rgb)

        return self._hls

    @property
    def hsv(self):
        if self._hsv is None:
            self._hsv = colorsys.rgb_to_hsv(*self.rgb)

        return self._hsv

    @property
    def alpha(self):
        if self._alpha is None:
            self._alpha = self[3] / 255.0

        return self._alpha

    def normalize(self):
        """
        :doc: color method

        Returns a normalized version of this Color where all components fall
        between 0 and 255.
        """

        r = max(min(self[0], 255), 0)
        g = max(min(self[1], 255), 0)
        b = max(min(self[2], 255), 0)
        a = max(min(self[3], 255), 0)

        return Color((r, g, b, a))

    def __add__(self, other):
        other = Color(other)

        return Color((
            self[0] + other[0],
            self[1] + other[1],
            self[2] + other[2],
            self[3] + other[3]))

    __radd__ = __add__

    def __sub__(self, other):
        other = Color(other)

        return Color((
            self[0] - other[0],
            self[1] - other[1],
            self[2] - other[2],
            self[3] - other[3]))

    def __rsub__(self, other):
        other = Color(other)
        return other - self

    def __mul__(self, other):

        if isinstance(other, renpy.display.im.matrix):
            return Color(tuple(int(i) for i in other.vector_mul(self)[:4]))

        other = Color(other)

        return Color((
            self[0] * other[0],
            self[1] * other[1],
            self[2] * other[2],
            self[3] * other[3]))

    __rmul__ = __mul__

    def interpolate_core(self, a, b, fraction):

        if isinstance(a, tuple):
            rv = tuple(self.interpolate_core(ac, bc, fraction) for ac, bc in zip(a, b))
        else:
            rv = a + (b - a) * fraction

        return type(a)(rv)

    def interpolate(self, other, fraction):
        """
        :doc: color method

        Interpolates between this Color and `other` in the RGB color
        space, returning a new Color as the result. If `fraction` is 0.0, the
        result is the same as this color, if 1.0, it is the same as `other`.
        """

        other = Color(other)

        return self.interpolate_core(self, other, fraction)

    def interpolate_hsv(self, other, fraction):
        """
        :doc: color method

        Interpolates between this Color and `other` in the HSV color
        space, returning a new Color as the result. If `fraction` is 0.0, the
        result is the same as this color, if 1.0, it is the same as `other`.

        `other` may be a string, Color or an HSV tuple.
        """

        if isinstance(other, basestring):
            other = Color(other, alpha=self.alpha)
        elif not isinstance(other, Color):
            other = Color(hsv=other, alpha=self.alpha)

        hsv = self.interpolate_core(self.hsv, other.hsv, fraction)
        alpha = self.interpolate_core(self.alpha, other.alpha, fraction)

        return Color(hsv=hsv, alpha=alpha)

    def interpolate_hls(self, other, fraction):
        """
        :doc: color method

        Interpolates between this Color and `other` in the HLS color
        space, returning a new Color as the result. If `fraction` is 0.0, the
        result is the same as this color, if 1.0, it is the same as `other`.

        `other` may be a string, Color or an HLS tuple.
        """

        if isinstance(other, basestring):
            other = Color(other, alpha=self.alpha)
        elif not isinstance(other, Color):
            other = Color(hls=other, alpha=self.alpha)

        hls = self.interpolate_core(self.hls, other.hls, fraction)
        alpha = self.interpolate_core(self.alpha, other.alpha, fraction)

        return Color(hls=hls, alpha=alpha)

    def tint(self, fraction):
        """
        :doc: color method

        Creates a tint of this color by mixing it with white. `fraction` is
        the fraction of this color that is in the new color. If `fraction` is
        1.0, the color is unchanged, if 0.0, white is returned.

        The alpha channel is unchanged.
        """

        return self.interpolate_core(self, (255, 255, 255, self[3]), (1.0 - fraction))

    def shade(self, fraction):
        """
        :doc: color method

        Creates a shade of this color by mixing it with black. `fraction` is
        the fraction of this color that is in the new color. If `fraction` is
        1.0, the color is unchanged, if 0.0, black is returned.

        The alpha channel is unchanged.
        """

        return self.interpolate_core(self, (0, 0, 0, self[3]), (1.0 - fraction))

    def opacity(self, opacity):
        """
        :doc: color method

        Multiplies the alpha channel of this color by `opacity`, and returns
        the new color.
        """

        return Color((
            self[0],
            self[1],
            self[2],
            int(self[3] * opacity)))

    def rotate_hue(self, rotation):
        """
        :doc: color method

        Rotates this color's hue by `rotation`, and returns the new Color. `rotation`
        is a fraction of a full rotation, to convert degrees divide by 360.0.
        """

        h, l, s = self.hls
        h = (h + rotation) % 1.0
        return Color(hls=(h, l, s), alpha=self.alpha)

    def replace_hue(self, hue):
        """
        :doc: color method

        Replaces this color's hue with `hue`, which should be between 0.0 and
        1.0. Returns the new Color.
        """

        _, l, s = self.hls
        h = hue
        return Color(hls=(h, l, s), alpha=self.alpha)

    def multiply_hls_saturation(self, saturation):
        """
        :doc: color method

        Multiplies this color's saturation by `saturation`, and returns
        the result as a new Color. This is performed in the HLS color space.
        """

        h, l, s = self.hls
        s = min(s * saturation, 1.0)
        return Color(hls=(h, l, s), alpha=self.alpha)

    def multiply_hsv_saturation(self, saturation):
        """
        :doc: color method

        Multiplies this color's saturation by `saturation`, and returns
        the result as a new Color. This is performed in the HSV color space.
        """

        h, s, v = self.hsv
        s = min(s * saturation, 1.0)
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def multiply_value(self, value):
        """
        :doc: color method

        Multiples this color's value by `value` and returns the result as a
        new Color. This is performed in the HSV color space.
        """

        h, s, v = self.hsv
        v = min(v * value, 1.0)
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def replace_hls_saturation(self, saturation):
        """
        :doc: color method

        Replaces this color's saturation with `saturation`, and returns
        the result as a new Color. This is performed in the HLS color space.
        """

        h, l, _ = self.hls
        s = saturation
        return Color(hls=(h, l, s), alpha=self.alpha)

    def replace_hsv_saturation(self, saturation):
        """
        :doc: color method

        Replace this color's saturation with `saturation`, and returns
        the result as a new Color. This is performed in the HSV color space.
        """

        h, _, v = self.hsv
        s = saturation
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def replace_value(self, value):
        """
        :doc: color method

        Replaces this color's value with `value` and returns the result as a
        new Color. This is performed in the HSV color space.
        """

        h, s, _ = self.hsv
        v = value
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def replace_lightness(self, lightness):
        """
        :doc: color method

        Replaces this color's lightness with `lightness`, and returns
        the result as a new Color. This is performed in the HLS color space.
        """

        h, _, s = self.hls
        l = lightness
        return Color(hls=(h, l, s), alpha=self.alpha)

    def replace_opacity(self, opacity):
        """
        :doc: color method

        Replaces this color's alpha channel with `opacity`, and
        returns the result as a new Color.
        """

        alpha = min(max(opacity, 0.0), 1.0)
        return Color((self[0], self[1], self[2]), alpha=alpha)
