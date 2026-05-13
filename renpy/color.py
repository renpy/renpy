# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

from typing import final, overload

import re
import colorsys


_SHORT_COLOR_STRING_RE = re.compile(
    r"#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})?",
)
_LONG_COLOR_STRING_RE = re.compile(
    r"#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})?",
)

type ColorLike = "Color" | tuple[int, int, int, int] | tuple[int, int, int] | str
"""
The color, in one of the standard formats Ren'Py understands. These are:
- A Color object.
- An (r, g, b) or (r, g, b, a) tuple, in which all the numbers are between 0 and 255.
- A string giving a hexadecimal color, in the form "#rgb", "#rgba", "#rrggbb", or "#rrggbbaa".
"""


@final
class Color(tuple[int, int, int, int]):
    """
    :doc: color class
    :args: (color=None, hls=None, hsv=None, rgb=None, alpha=1.0)
    :name: Color

    The Color class is used to represent and manipulate colors and convert
    between various color spaces. It also represents opacity in the form
    of an alpha.

    When creating a Color, at most one of the `color`, `hls`, `hsv`, or
    `rgb` arguments should be supplied. (If all are None, None is returned.)

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

    .. attribute:: rgba

        Returns the color as a tuple of four floating point numbers giving
        the red, green, blue and alpha components as 0.0 to 1.0 values.

    .. attribute:: premultiplied

        Returns the color as a tuple of four floating point numbers giving
        the red, green, blue and alpha components as 0.0 to 1.0 values, with
        the red, green, and blue components premultiplied by the alpha.

    .. attribute:: alpha

        Returns the alpha (opacity) of this Color as a number between 0.0 and
        1.0, where 0.0 is transparent and 1.0 is opaque.

    .. attribute:: hexcode

        Returns a string containing a hex color code of the form #rrggbbaa
        or #rrggbb.

    Color objects have the following methods. Since Colors are immutable,
    these methods always return a new Color object.
    """

    _rgb: tuple[float, float, float] | None = None
    _hls: tuple[float, float, float] | None = None
    _hsv: tuple[float, float, float] | None = None
    _alpha: float | None = None
    _rgba: tuple[float, float, float, float] | None = None

    @overload
    # Color object
    def __new__(cls, color: "Color") -> "Color": ...

    @overload
    # 4-tuple - no alpha
    def __new__(cls, color: tuple[int, int, int, int]) -> "Color": ...

    @overload
    # 3-tuple or string, optional alpha
    def __new__(cls, color: tuple[int, int, int] | str, *, alpha: float = 1.0) -> "Color": ...

    @overload
    # 3-tuple of HLS, optional alpha
    def __new__(cls, *, hls: tuple[float, float, float], alpha: float = 1.0) -> "Color": ...

    @overload
    # 3-tuple of HSV, optional alpha
    def __new__(cls, *, hsv: tuple[float, float, float], alpha: float = 1.0) -> "Color": ...

    @overload
    # 3-tuple of RGB, optional alpha
    def __new__(cls, *, rgb: tuple[float, float, float], alpha: float = 1.0) -> "Color": ...

    @overload
    # No arguments - None
    def __new__(cls, *, alpha: float = 1.0) -> None: ...

    def __new__(
        cls,
        color: ColorLike | None = None,
        hls: tuple[float, float, float] | None = None,
        hsv: tuple[float, float, float] | None = None,
        rgb: tuple[float, float, float] | None = None,
        alpha: float = 1.0,
    ) -> "Color | None":
        if isinstance(color, str):
            if m := re.fullmatch(_SHORT_COLOR_STRING_RE, color):
                r, g, b, a = m.groups()
                r = int(r, 16) * 0x11
                g = int(g, 16) * 0x11
                b = int(b, 16) * 0x11
                if a is None:
                    a = int(alpha * 255)
                else:
                    a = int(a, 16) * 0x11

            elif m := re.fullmatch(_LONG_COLOR_STRING_RE, color):
                r, g, b, a = m.groups()
                r = int(r, 16)
                g = int(g, 16)
                b = int(b, 16)
                if a is None:
                    a = int(alpha * 255)
                else:
                    a = int(a, 16)

            else:
                raise Exception(f"Color string {color!r} must be 3, 4, 6, or 8 hex digits long.")

            return super().__new__(cls, (r, g, b, a))

        elif isinstance(color, Color):
            return color

        elif color is not None:
            c = tuple(color)
            lenc = len(c)

            if lenc == 3:
                return super().__new__(cls, (*c, int(alpha * 255)))

            elif lenc == 4:
                return super().__new__(cls, c)

            else:
                raise Exception(f"Color tuple {color!r} must be 3 or 4 elements long.")

        elif hsv is not None:
            hls = None
            rgb = colorsys.hsv_to_rgb(*hsv)

        elif hls is not None:
            hsv = None
            rgb = colorsys.hls_to_rgb(*hls)

        elif rgb is not None:
            hls = None
            hsv = None

        else:
            return None

        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)
        a = int(alpha * 255)

        rv = super().__new__(cls, (r, g, b, a))
        rv._rgb = rgb
        rv._hls = hls
        rv._hsv = hsv
        rv._alpha = alpha
        rv._rgba = (*rgb, alpha)
        return rv

    @property
    def hexcode(self) -> str:
        """
        Returns a string containing a hex color code of the form #rrggbbaa
        or #rrggbb.
        """

        r, g, b, a = self
        if a == 255:
            return f"#{r:02x}{g:02x}{b:02x}"
        else:
            return f"#{r:02x}{g:02x}{b:02x}{a:02x}"

    def __repr__(self):
        return f"renpy.color.Color({self.hexcode!r})"

    def __getnewargs__(self):
        return (tuple(self),)

    @property
    def rgb(self) -> tuple[float, float, float]:
        """
        Returns the color as a tuple of three floating point numbers giving
        the red, green, and blue components. Each component ranges between 0.0
        and 1.0.
        """

        if self._rgb is None:
            self._rgb = (
                self[0] / 255.0,
                self[1] / 255.0,
                self[2] / 255.0,
            )

        return self._rgb

    @property
    def rgba(self):
        """
        Returns the color as a tuple of four floating point numbers giving
        the red, green, blue and alpha components as 0.0 to 1.0 values.
        """

        if self._rgba is None:
            self._rgba = (
                self[0] / 255.0,
                self[1] / 255.0,
                self[2] / 255.0,
                self[3] / 255.0,
            )

        return self._rgba

    @property
    def premultiplied(self):
        """
        Returns the color as a tuple of four floating point numbers giving
        the red, green, blue and alpha components as 0.0 to 1.0 values, with
        the red, green, and blue components premultiplied by the alpha.
        """

        r, g, b, a = self.rgba

        return (r * a, g * a, b * a, a)

    @property
    def hls(self):
        """
        Returns the color as a tuple of three floating point numbers giving
        hue, lightness, and saturation. Each component ranges between 0.0 and 1.0.
        """

        if self._hls is None:
            self._hls = colorsys.rgb_to_hls(*self.rgb)

        return self._hls

    @property
    def hsv(self):
        """
        Returns the color as a tuple of three floating point numbers giving
        hue, saturation, and value. Each component ranges between 0.0 and 1.0.
        """

        if self._hsv is None:
            self._hsv = colorsys.rgb_to_hsv(*self.rgb)

        return self._hsv

    @property
    def alpha(self):
        """
        Returns the alpha (opacity) of this Color as a number between 0.0 and
        1.0, where 0.0 is transparent and 1.0 is opaque.
        """

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

    def __add__(self, other: ColorLike):
        r1, g1, b1, a1 = self

        try:
            r2, g2, b2, a2 = Color(other)
        except Exception:
            return NotImplemented

        return Color((r1 + r2, g1 + g2, b1 + b2, a1 + a2))

    __radd__ = __add__

    def __sub__(self, other: ColorLike):
        r1, g1, b1, a1 = self

        try:
            r2, g2, b2, a2 = Color(other)
        except Exception:
            return NotImplemented

        return Color((r1 - r2, g1 - g2, b1 - b2, a1 - a2))

    def __rsub__(self, other: ColorLike):
        r1, g1, b1, a1 = self

        try:
            r2, g2, b2, a2 = Color(other)
        except Exception:
            return NotImplemented

        return Color((r2 - r1, g2 - g1, b2 - b1, a2 - a1))

    def __mul__(self, other: ColorLike):
        r1, g1, b1, a1 = self

        try:
            r2, g2, b2, a2 = Color(other)
        except Exception:
            return NotImplemented

        return Color((r1 * r2, g1 * g2, b1 * b2, a1 * a2))

    __rmul__ = __mul__  # type: ignore

    def _interpolate_tuple[T: tuple](self, a: T, b: T, fraction: float) -> T:
        i = self._interpolate_num
        return type(a)(tuple(i(ac, bc, fraction) for ac, bc in zip(a, b)))

    def _interpolate_num[T: (float, int)](self, a: T, b: T, fraction: float) -> T:
        return type(a)(a + (b - a) * fraction)

    def interpolate(self, other: ColorLike, fraction: float) -> "Color":
        """
        :doc: color method

        Interpolates between this Color and `other` in the RGB color
        space, returning a new Color as the result. If `fraction` is 0.0, the
        result is the same as this color, if 1.0, it is the same as `other`.
        """

        return self._interpolate_tuple(self, Color(other), fraction)

    def interpolate_hsv(self, other: "str | Color | tuple[float, float, float]", fraction: float) -> "Color":
        """
        :doc: color method

        Interpolates between this Color and `other` in the HSV color
        space, returning a new Color as the result. If `fraction` is 0.0, the
        result is the same as this color, if 1.0, it is the same as `other`.

        `other` may be a string, Color or an HSV tuple.
        """

        if isinstance(other, str):
            other = Color(other, alpha=self.alpha)
        elif not isinstance(other, Color):
            other = Color(hsv=other, alpha=self.alpha)

        hsv = self._interpolate_tuple(self.hsv, other.hsv, fraction)
        alpha = self._interpolate_num(self.alpha, other.alpha, fraction)

        return Color(hsv=hsv, alpha=alpha)

    def interpolate_hls(self, other: "str | Color | tuple[float, float, float]", fraction: float) -> "Color":
        """
        :doc: color method

        Interpolates between this Color and `other` in the HLS color
        space, returning a new Color as the result. If `fraction` is 0.0, the
        result is the same as this color, if 1.0, it is the same as `other`.

        `other` may be a string, Color or an HLS tuple.
        """

        if isinstance(other, str):
            other = Color(other, alpha=self.alpha)
        elif not isinstance(other, Color):
            other = Color(hls=other, alpha=self.alpha)

        hls = self._interpolate_tuple(self.hls, other.hls, fraction)
        alpha = self._interpolate_num(self.alpha, other.alpha, fraction)

        return Color(hls=hls, alpha=alpha)

    def tint(self, fraction: float) -> "Color":
        """
        :doc: color method

        Creates a tint of this color by mixing it with white. `fraction` is
        the fraction of this color that is in the new color. If `fraction` is
        1.0, the color is unchanged, if 0.0, white is returned.

        The alpha channel is unchanged.
        """

        return self._interpolate_tuple(self, Color((255, 255, 255, self[3])), (1.0 - fraction))

    def shade(self, fraction: float) -> "Color":
        """
        :doc: color method

        Creates a shade of this color by mixing it with black. `fraction` is
        the fraction of this color that is in the new color. If `fraction` is
        1.0, the color is unchanged, if 0.0, black is returned.

        The alpha channel is unchanged.
        """

        return self._interpolate_tuple(self, Color((0, 0, 0, self[3])), (1.0 - fraction))

    def opacity(self, opacity: float) -> "Color":
        """
        :doc: color method

        Multiplies the alpha channel of this color by `opacity`, and returns
        the new color.
        """

        r, g, b, a = self
        return Color((r, g, b, int(a * opacity)))

    def rotate_hue(self, rotation: float) -> "Color":
        """
        :doc: color method

        Rotates this color's hue by `rotation`, and returns the new Color. `rotation`
        is a fraction of a full rotation (between 0.0 and 1.0). Divide by 360.0 to
        convert to degrees.
        """

        h, l, s = self.hls  # noqa: E741
        h = (h + rotation) % 1.0
        return Color(hls=(h, l, s), alpha=self.alpha)

    def replace_hue(self, hue: float) -> "Color":
        """
        :doc: color method

        Replaces this color's hue with `hue`, which should be between 0.0 and
        1.0. Returns the new Color.
        """

        _, l, s = self.hls  # noqa: E741
        h = hue
        return Color(hls=(h, l, s), alpha=self.alpha)

    def multiply_hls_saturation(self, saturation: float) -> "Color":
        """
        :doc: color method

        Multiplies this color's saturation by `saturation`, and returns
        the result as a new Color. This is performed in the HLS color space.
        """

        h, l, s = self.hls  # noqa: E741
        s = min(s * saturation, 1.0)
        return Color(hls=(h, l, s), alpha=self.alpha)

    def multiply_hsv_saturation(self, saturation: float) -> "Color":
        """
        :doc: color method

        Multiplies this color's saturation by `saturation`, and returns
        the result as a new Color. This is performed in the HSV color space.
        """

        h, s, v = self.hsv
        s = min(s * saturation, 1.0)
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def multiply_value(self, value: float) -> "Color":
        """
        :doc: color method

        Multiples this color's value by `value` and returns the result as a
        new Color. This is performed in the HSV color space.
        """

        h, s, v = self.hsv
        v = min(v * value, 1.0)
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def replace_hls_saturation(self, saturation: float) -> "Color":
        """
        :doc: color method

        Replaces this color's saturation with `saturation`, and returns
        the result as a new Color. This is performed in the HLS color space.
        """

        h, l, _ = self.hls  # noqa: E741
        s = saturation
        return Color(hls=(h, l, s), alpha=self.alpha)

    def replace_hsv_saturation(self, saturation: float) -> "Color":
        """
        :doc: color method

        Replace this color's saturation with `saturation`, and returns
        the result as a new Color. This is performed in the HSV color space.
        """

        h, _, v = self.hsv
        s = saturation
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def replace_value(self, value: float) -> "Color":
        """
        :doc: color method

        Replaces this color's value with `value` and returns the result as a
        new Color. This is performed in the HSV color space.
        """

        h, s, _ = self.hsv
        v = value
        return Color(hsv=(h, s, v), alpha=self.alpha)

    def replace_lightness(self, lightness: float) -> "Color":
        """
        :doc: color method

        Replaces this color's lightness with `lightness`, and returns
        the result as a new Color. This is performed in the HLS color space.
        """

        h, _, s = self.hls
        l = lightness  # noqa: E741
        return Color(hls=(h, l, s), alpha=self.alpha)

    def replace_opacity(self, opacity: float) -> "Color":
        """
        :doc: color method

        Replaces this color's alpha channel with `opacity`, and
        returns the result as a new Color.
        """

        alpha = min(max(opacity, 0.0), 1.0)
        return Color((self[0], self[1], self[2]), alpha=alpha)
