# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import renpy


def absolute_wrap(func):
    """
    Wraps func into a method of absolute. The wrapped method
    converts a float result back to absolute.
    """

    def wrapper(*args):
        rv = func(*args)

        if type(rv) is float:
            return absolute(rv)
        else:
            return rv

    return wrapper


class absolute(float):
    """
    This represents an absolute float coordinate.
    """

    __slots__ = ()

    def __divmod__(self, value):
        return self//value, self%value

    def __rdivmod__(self, value):
        return value//self, value%self

    def __repr__(self):
        return "absolute({})".format(float.__repr__(self))

    @staticmethod
    def compute_raw(value, room):
        """
        Converts a position from one of the many supported position types
        into an absolute number of pixels, without regard for the return type.
        """
        if isinstance(value, position):
            return value.relative * room + value.absolute
        elif isinstance(value, (absolute, int)):
            return value
        elif isinstance(value, float):
            return value * room
        raise TypeError("Value {} of type {} not recognized as a position.".format(value, type(value)))

    @staticmethod
    def compute(value, room):
        """
        Does the same, but converts the result to the absolute type.
        """
        return absolute(absolute.compute_raw(value, room))


for fn in (
    '__coerce__', # PY2
    '__div__', # PY2
    '__long__', # PY2
    '__nonzero__', # PY2
    '__rdiv__', # PY2

    '__abs__',
    '__add__',
    # '__bool__', # non-float
    '__ceil__',
    # '__divmod__', # special-cased above, tuple of floats
    # '__eq__', # non-float
    '__floordiv__',
    # '__format__', # non-float
    # '__ge__', # non-float
    # '__gt__', # non-float
    # '__hash__', # non-float
    # '__int__', # non-float
    # '__le__', # non-float
    # '__lt__', # non-float
    '__mod__',
    '__mul__',
    # '__ne__', # non-float
    '__neg__',
    '__pos__',
    '__pow__',
    '__radd__',
    # '__rdivmod__', # special-cased above, tuple of floats
    '__rfloordiv__',
    '__rmod__',
    '__rmul__',
    '__round__',
    '__rpow__',
    '__rsub__',
    '__rtruediv__',
    # '__str__', # non-float
    '__sub__',
    '__truediv__',
    # '__trunc__', # non-float

    # 'as_integer_ratio', # tuple of non-floats
    'conjugate',
    'fromhex',
    # 'hex', # non-float
    # 'is_integer', # non-float
):
    f = getattr(float, fn, None)
    if f is not None: # for PY2-only and PY3-only methods
        setattr(absolute, fn, absolute_wrap(f))

del absolute_wrap, fn, f # type: ignore


class position(object):
    """
    A combination of relative and absolute coordinates.
    """

    __slots__ = ('absolute', 'relative')

    def __new__(cls, absolute, relative=None):
        """
        If passed two parameters, takes them as an absolute and a relative.
        If passed only one parameter, converts it.
        Using __new__ so that passing a position returns it unchanged.
        """

        if relative is None:
            typ = type(absolute)

            if typ is cls:
                return absolute

            if typ is float:
                relative = absolute
                absolute = 0
            else:
                relative = 0

        self = object.__new__(cls)
        self.absolute = absolute
        self.relative = relative

        return self

    from_any = classmethod(__new__)

    def __add__(self, other):
        if isinstance(other, position):
            return position(self.absolute + other.absolute,
                            self.relative + other.relative)

        return NotImplemented

    __radd__ = __add__

    def __eq__(self, other):
        if isinstance(other, position):
            return self.absolute == other.absolute and \
                   self.relative == other.relative

        simple = self.simplify()

        return type(simple) is not position and simple == other

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return position(self.absolute * other,
                            self.relative * other)

        return NotImplemented

    __rmul__ = __mul__

    def __neg__(self):
        return position(-self.absolute, -self.relative)

    def __pos__(self):
        return self

    def __repr__(self):
        return "position(absolute={}, relative={})".format(self.absolute, self.relative)

    def __rsub__(self, other):
        if isinstance(other, position):
            return position(other.absolute - self.absolute,
                            other.relative - self.relative)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, position):
            return position(self.absolute - other.absolute,
                            self.relative - other.relative)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return position(self.absolute / other,
                            self.relative / other)

        return NotImplemented

    __div__ = __truediv__ # PY2

    def simplify(self):
        """
        Tries to represent this position as an int, float, or absolute, if
        possible.
        """

        if self.relative == 0.0:
            if self.absolute == int(self.absolute):
                return int(self.absolute)
            else:
                return absolute(self.absolute)
        elif self.absolute == 0:
            return float(self.relative)
        else:
            return self


class DualAngle(object):
    @classmethod
    def from_any(cls, other):
        if isinstance(other, cls):
            return other
        elif type(other) is float:
            return cls(other, other)
        raise TypeError("Cannot convert {} to DualAngle".format(type(other)))

    def __init__(self, absolute, relative): # for tests, convert to PY2 after
        self.absolute = absolute
        self.relative = relative

    def __add__(self, other):
        if isinstance(other, DualAngle):
            return DualAngle(self.absolute + other.absolute, self.relative + other.relative)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DualAngle(self.absolute * other, self.relative * other)
        return NotImplemented

    __rmul__ = __mul__

    def __neg__(self):
        return -1 * self

    def __sub__(self, other):
        return self + -other


def any_object(x):
    return x


def bool_or_none(x):
    if x is None:
        return x
    return bool(x)


def float_or_none(x):
    if x is None:
        return x
    return float(x)


def matrix(x):
    if x is None:
        return None
    elif callable(x):
        return x
    else:
        return renpy.display.matrix.Matrix(x)


def mesh(x):
    if isinstance(x, (renpy.gl2.gl2mesh2.Mesh2, renpy.gl2.gl2mesh3.Mesh3, tuple)):
        return x

    return bool(x)


def position_or_none(x):
    if x is None:
        return None
    return position.from_any(x)
