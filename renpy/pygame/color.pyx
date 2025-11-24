# Copyright 2014 Tom Rothamel <tom@rothamel.us>
# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from sdl2 cimport *
import binascii
import struct

include "color_dict.pxi"

cdef Uint32 map_color(SDL_Surface *surface, color) except? 0xaabbccdd:
    """
    Maps `color` into an RGBA color value that can be used with `surface`.
    """

    cdef Uint8 r, g, b, a

    if isinstance(color, (tuple, list, Color)) and len(color) == 4:
        r, g, b, a = color
    elif isinstance(color, (tuple, list, Color)) and len(color) == 3:
        r, g, b = color
        a = 255
    elif isinstance(color, int):
        return color
    else:
        raise TypeError("Expected a color.")

    return SDL_MapRGBA(surface.format, r, g, b, a)

cdef object get_color(Uint32 pixel, SDL_Surface *surface):
    cdef Uint8 r
    cdef Uint8 g
    cdef Uint8 b
    cdef Uint8 a

    SDL_GetRGBA(pixel, surface.format, &r, &g, &b, &a)

    return Color(r, g, b, a)

cdef to_sdl_color(color, SDL_Color *out):
    if not isinstance(color, Color):
        color = Color(color)
    out.r = color.r
    out.g = color.g
    out.b = color.b
    out.a = color.a

cdef class Color:
    cdef from_rgba(self, Uint8 r, Uint8 g, Uint8 b, Uint8 a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    cdef from_hex(self, c):
        # Handle short hex strings.
        if len(c) == 3 or len(c) == 4:
            c = "".join(map(lambda x: x*2, c))

        try:
            if len(c) == 6:
                r, g, b = struct.unpack('BBB', binascii.unhexlify(c))
                a = 255
            elif len(c) == 8:
                r, g, b, a = struct.unpack('BBBB', binascii.unhexlify(c))
            else:
                raise ValueError(c)
        except TypeError as e:
            raise ValueError(c)

        self.from_rgba(r, g, b, a)

    cdef from_name(self, c):
        # Remove all whitespace.
        c = "".join(c.split()).lower()

        try:
            r, g, b = colors[c]
        except KeyError as e:
            raise ValueError(c)
        self.from_rgba(r, g, b, 255)

    def __richcmp__(Color x, y, int op):
        if op == 3:
            return not (x == y)

        if isinstance(y, tuple):
            y = Color(y)
        if not isinstance(y, Color):
            return False
        if op == 2:
            return x.r == y.r and x.g == y.g and x.b == y.b and x.a == y.a

    def __cinit__(self):
        self.length = 4
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 255

    def __init__(self, *args):
        self.length = 4

        if len(args) == 1:
            c = args[0]
            if isinstance(c, basestring):
                if c.startswith('#'):
                    self.from_hex(c[1:])
                elif c.startswith('0x'):
                    self.from_hex(c[2:])
                else:
                    self.from_name(c)
            elif isinstance(c, (tuple, list, Color)):
                if len(c) == 4:
                    self.from_rgba(c[0], c[1], c[2], c[3])
                elif len(c) == 3:
                    self.from_rgba(c[0], c[1], c[2], 255)
                else:
                    raise ValueError(c)
            else:
                self.from_hex("%08x" % c)

        elif len(args) == 3:
            r, g, b = args
            self.from_rgba(r, g, b, 255)
        elif len(args) == 4:
            r, g, b, a = args
            self.from_rgba(r, g, b, a)

    def __repr__(self):
        return str((self.r, self.g, self.b, self.a))

    def __int__(self):
        packed = struct.pack('BBBB', self.r, self.g, self.b, self.a)
        return struct.unpack('>L', packed)[0]

    def __hex__(self):
        return hex(int(self))

    def __oct__(self):
        return oct(int(self))

    def __float__(self):
        return float(int(self))

    def __reduce__(self):
        d = {}
        d['rgba'] = (self.r, self.g, self.b, self.a)
        return (Color, (), d)

    def __setstate__(self, d):
        self.r, self.g, self.b, self.a = d['rgba']

    def __setitem__(self, key, val):
        if not isinstance(val, int):
            raise ValueError(val)
        if key >= self.length:
            raise IndexError(key)
        if val < 0 or val > 255:
            raise ValueError(val)

        if key == 0: self.r = val
        elif key == 1: self.g = val
        elif key == 2: self.b = val
        elif key == 3: self.a = val
        else:
            raise IndexError(key)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return tuple(self)[key]
        if key >= self.length:
            raise IndexError(key)
        if key == 0: return self.r
        elif key == 1: return self.g
        elif key == 2: return self.b
        elif key == 3: return self.a
        else:
            raise IndexError(key)

    def __len__(self):
        return self.length

    def __mul__(self not None, Color rhs not None):
        # Multiplying this way doesn't make much sense,
        # but it's how pygame does it.

        r = min(255, self.r * rhs.r)
        g = min(255, self.g * rhs.g)
        b = min(255, self.b * rhs.b)
        a = min(255, self.a * rhs.a)

        return type(self)(r, g, b, a)

    def __add__(self not None, Color rhs not None):
        r = min(255, self.r + rhs.r)
        g = min(255, self.g + rhs.g)
        b = min(255, self.b + rhs.b)
        a = min(255, self.a + rhs.a)

        return type(self)(r, g, b, a)

    def __sub__(self not None, Color rhs not None):
        r = max(0, self.r - rhs.r)
        g = max(0, self.g - rhs.g)
        b = max(0, self.b - rhs.b)
        a = max(0, self.a - rhs.a)

        return type(self)(r, g, b, a)

    def __mod__(self not None, Color rhs not None):

        def mod(l, r):
            if r == 0:
                return 0

            return l % r

        r = mod(self.r, rhs.r)
        g = mod(self.g, rhs.g)
        b = mod(self.b, rhs.b)
        a = mod(self.a, rhs.a)

        return type(self)(r, g, b, a)

    def __div__(self not None, Color rhs not None):
        r = min(255, self.r / rhs.r)
        g = min(255, self.g / rhs.g)
        b = min(255, self.b / rhs.b)
        a = min(255, self.a / rhs.a)

        return type(self)(r, g, b, a)

    def __floordiv__(self not None, Color rhs not None):

        def div(a, b):
            if b == 0:
                return b

            return min(255, a // b)

        r = div(self.r, rhs.r)
        g = div(self.g, rhs.g)
        b = div(self.b, rhs.b)
        a = div(self.a, rhs.a)

        return type(self)(r, g, b, a)

    property cmy:
        def __get__(self):
            return 1 - (self.r / 255.0), 1 - (self.g / 255.0), 1 - (self.b / 255.0)

        def __set__(self, val):
            c, m, y = val
            self.r = (1 - c) * 255
            self.g = (1 - m) * 255
            self.b = (1 - y) * 255

    property hsva:
        def __get__(self):
            cdef double r = self.r / 255.0
            cdef double g = self.g / 255.0
            cdef double b = self.b / 255.0

            cdef double cmax = max(r, g, b)
            cdef double cmin = min(r, g, b)
            cdef double delta = cmax - cmin

            cdef double h, s, v, a

            if r == g == b:
                h = 0.0
                s = 0.0
            else:
                if cmax == r:
                    h = 60.0 * ((g - b) / delta % 6)
                elif cmax == g:
                    h = 60.0 * ((b - r) / delta + 2)
                else:
                    h = 60.0 * ((r - g) / delta + 4)

                if cmax == 0.0:
                    s = 0.0
                else:
                    s = delta / cmax * 100

            v = cmax * 100
            a = self.a / 255.0 * 100
            return h, s, v, a

        def __set__(self, val):
            cdef double h, s, v, a
            if len(val) == 3:
                h, s, v = val
                a = 0.0
            else:
                h, s, v, a = val

            h = h % 360.0

            # These should be in a range of [0.0, 1.0]
            s /= 100.0
            v /= 100.0
            a /= 100.0

            cdef double c = v * s
            cdef double x = c * (1 - abs((h / 60.0) % 2 - 1))
            cdef double m = v - c

            cdef double r, g, b

            if 0 <= h < 60:
                r, g, b = c, x, 0
            elif 60 <= h < 120:
                r, g, b = x, c, 0
            elif 120 <= h < 180:
                r, g, b = 0, c, x
            elif 180 <= h < 240:
                r, g, b = 0, x, c
            elif 240 <= h < 300:
                r, g, b = x, 0, c
            elif 300 <= h < 360:
                r, g, b = c, 0, x
            else:
                raise ValueError()

            self.r = int(255 * (r + m))
            self.g = int(255 * (g + m))
            self.b = int(255 * (b + m))
            self.a = int(255 * a)

    property hsla:
        def __get__(self):
            cdef double h, s, l, a
            cdef double r, g, b
            cdef double cmin, cmax, delta

            h = self.hsva[0] % 360.0

            r = self.r / 255.0
            g = self.g / 255.0
            b = self.b / 255.0

            cmin = min(r, g, b)
            cmax = max(r, g, b)
            delta = cmax - cmin

            l = (cmax + cmin) / 2.0

            if delta == 0:
                s = 0.0
            else:
                s = delta / (1 - abs(2 * l - 1))

            a = self.a / 255.0 * 100

            s = min(100.0, s * 100)
            l = min(100.0, l * 100)

            return h, s, l, a

        def __set__(self, val):
            cdef double h, s, l, a
            if len(val) == 3:
                h, s, l = val
                a = 0.0
            else:
                h, s, l, a = val

            s /= 100.0
            l /= 100.0
            a /= 100.0

            cdef double c = (1 - abs(2*l - 1)) * s
            cdef double x = c * (1 - abs((h / 60.0) % 2 - 1))
            cdef double m = l - c / 2.0

            cdef double r, g, b
            if 0 <= h < 60:
                r, g, b = c, x, 0
            elif 60 <= h < 120:
                r, g, b = x, c, 0
            elif 120 <= h < 180:
                r, g, b = 0, c, x
            elif 180 <= h < 240:
                r, g, b = 0, x, c
            elif 240 <= h < 300:
                r, g, b = x, 0, c
            elif 300 <= h < 360:
                r, g, b = c, 0, x
            else:
                raise ValueError()

            self.r = int(255 * (r + m))
            self.g = int(255 * (g + m))
            self.b = int(255 * (b + m))
            self.a = int(255 * a)

    property i1i2i3:
        def __get__(self):
            # Take the dot product as described here:
            # http://de.wikipedia.org/wiki/I1I2I3-Farbraum

            cdef double i1, i2, i3
            cdef double r, g, b

            r = self.r / 255.0
            g = self.g / 255.0
            b = self.b / 255.0

            i1 = (r + g + b) / 3.0
            i2 = (r - b) / 2.0
            i3 = (2*g - r - b) / 4.0

            return i1, i2, i3

        def __set__(self, val):
            # Dot product with the inverted matrix.

            cdef double i1, i2, i3
            cdef double r, g, b

            i1, i2, i3 = val

            r = i1 + i2 - (2.0/3.0 * i3)
            g = i1 + (4.0/3.0 * i3)
            b = i1 - i2  - (2.0/3.0 * i3)

            # Don't change alpha.
            self.r = int(r * 255)
            self.g = int(g * 255)
            self.b = int(b * 255)

    def normalize(self):
        return self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0

    def correct_gamma(self, gamma):
        m = map(lambda x: int(round(pow(x / 255.0, gamma) * 255)), tuple(self))
        c = type(self)(tuple(m))
        return c

    def set_length(self, n):
        if n > 4 or n < 1:
            raise ValueError(n)
        self.length = n
