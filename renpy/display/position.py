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

from typing import final, overload, SupportsIndex, Any

from renpy.types import Position


@final
class absolute(float):
    """
    This represents an absolute float coordinate, where the fractional part is a subpixel value.
    """

    __slots__ = ()

    def __repr__(self):
        return f"absolute({float.__repr__(self)})"

    # Special case, should return floats.
    def __divmod__(self, value: float,):
        return self // value, self % value

    def __rdivmod__(self, value: float):
        return value // self, value % self

    # Wrap all dunder methods that return floats to return absolutes.
    def __add__(self, value: float) -> "absolute":
        rv = super().__add__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __radd__(self, value: float) -> "absolute":
        rv = super().__radd__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __sub__(self, value: float) -> "absolute":
        rv = super().__sub__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __rsub__(self, value: float) -> "absolute":
        rv = super().__rsub__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __mul__(self, value: float) -> "absolute":
        rv = super().__mul__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __rmul__(self, value: float) -> "absolute":
        rv = super().__rmul__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __truediv__(self, value: float) -> "absolute":
        rv = super().__truediv__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __rtruediv__(self, value: float) -> "absolute":
        rv = super().__rtruediv__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __floordiv__(self, value: float) -> "absolute":
        rv = super().__floordiv__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __rfloordiv__(self, value: float) -> "absolute":
        rv = super().__rfloordiv__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __mod__(self, value: float) -> "absolute":
        rv = super().__mod__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __rmod__(self, value: float) -> "absolute":
        rv = super().__rmod__(value)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __pow__(self, value: float, mod: None = None) -> Any:
        rv = super().__pow__(value, mod)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __rpow__(self, value: float, mod: None = None) -> Any:
        rv = super().__rpow__(value, mod)
        if rv is NotImplemented:
            return NotImplemented

        return absolute(rv)

    def __neg__(self) -> "absolute":
        return absolute(super().__neg__())

    def __pos__(self) -> "absolute":
        return absolute(super().__pos__())

    def __abs__(self) -> "absolute":
        return absolute(super().__abs__())

    @overload
    def __round__(self, ndigits: None = None) -> int: ...
    @overload
    def __round__(self, ndigits: SupportsIndex) -> "absolute": ...

    def __round__(self, ndigits: SupportsIndex | None = None) -> "absolute | int":
        rv = super().__round__(ndigits)
        if isinstance(rv, float):
            return absolute(rv)
        else:
            return rv

    def conjugate(self) -> "absolute":
        return absolute(super().conjugate())

    def fromhex(self, s: str) -> "absolute":
        return absolute(super().fromhex(s))

    # Other methods should return non-floats.

    @overload
    @staticmethod
    def compute_raw(value: "position", room: float) -> float: ...

    @overload
    @staticmethod
    def compute_raw[T: ("int | float | absolute")](value: T, room: float) -> T: ...

    @staticmethod
    def compute_raw(value: Position, room: float) -> "int | float | absolute":
        """
        Converts a position from one of the Ren'Py position types into an
        absolute number of pixels, without regard for the return type.
        """

        if isinstance(value, position):
            return value.relative * room + value.absolute

        elif isinstance(value, (absolute, int)):
            return value

        elif isinstance(value, float):
            return value * room

        else:
            raise TypeError(f"Value {value} of type {type(value)} not recognized as a position.")

    @staticmethod
    def compute(value: Position, room: float) -> "absolute":
        """
        Converts a position from one of the Ren'Py position types into an
        absolute number of pixels, and returns it as an absolute instance.
        """

        return absolute(absolute.compute_raw(value, room))


_absolute = absolute


@final
class position:
    """
    A combination of relative and absolute coordinates.
    """

    __slots__ = ["absolute", "relative"]

    absolute: _absolute
    relative: float

    @overload
    def __new__(cls, _: "position") -> "position": ...

    @overload
    def __new__(cls, absolute: int | _absolute = 0) -> "position": ...

    @overload
    def __new__(cls, relative: float = 0.0) -> "position": ...

    @overload
    def __new__(cls, absolute: int | float, relative: float) -> "position": ...

    def __new__(
        cls,
        absolute: "int | float | position" = 0,
        relative: "float | None" = None,
    ) -> "position":
        """
        If passed two parameters, takes them as an absolute and a relative values of the position.
        If passed only one parameter, convert it with the following rules:
        - If it is a position, return it unchanged.
        - If it is an integer or absolute, use it as an absolute value.
        - Otherwise it should be a float which is treated as a relative value.
        """

        # Using __new__ so that passing a position returns it unchanged.
        if relative is None:
            return cls.from_any(absolute)
        else:
            if isinstance(absolute, position):
                raise TypeError("When absolute is a position, relative must be None.")

            self = super().__new__(cls)
            self.absolute = _absolute(absolute)
            self.relative = float(relative)
            return self

    @classmethod
    def from_any(cls, value: Position) -> "position":
        if isinstance(value, position):
            return value
        elif isinstance(value, (int, absolute)):
            return cls(value, 0)
        else:
            return cls(0, value)

    def simplify(self) -> Position:
        """
        Tries to represent this position as an int, float, or absolute, if possible.
        """

        if self.relative == 0.0:
            if self.absolute.is_integer():
                return int(self.absolute)
            else:
                return absolute(self.absolute)
        elif self.absolute == 0:
            return float(self.relative)
        else:
            return self

    def __eq__(self, other):
        if isinstance(other, position):
            return self.absolute == other.absolute and \
                   self.relative == other.relative

        simple = self.simplify()

        return type(simple) is not position and simple == other

    def __add__(self, value: "position") -> "position":
        if isinstance(value, position):
            return position(self.absolute + value.absolute, self.relative + value.relative)

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, value: "position") -> "position":
        if isinstance(value, position):
            return position(self.absolute - value.absolute, self.relative - value.relative)

        return NotImplemented

    def __rsub__(self, value: "position") -> "position":
        if isinstance(value, position):
            return position(value.absolute - self.absolute, value.relative - self.relative)

        return NotImplemented

    def __mul__(self, value: int | float) -> "position":
        if isinstance(value, (int, float)):
            return position(self.absolute * value, self.relative * value)

        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, value: int | float) -> "position":
        if isinstance(value, (int, float)):
            return position(self.absolute / value, self.relative / value)

        return NotImplemented

    def __rtruediv__(self, value: int | float) -> "position":
        if isinstance(value, (int, float)):
            return position(value / self.absolute, value / self.relative)

        return NotImplemented

    def __pos__(self) -> "position":
        return self

    def __neg__(self) -> "position":
        return position(-self.absolute, -self.relative)

    def __repr__(self) -> str:
        absolute = self.absolute
        if self.absolute.is_integer():
            absolute = int(self.absolute)

        return f"position({absolute}, {self.relative})"

    def __hash__(self) -> int:
        return hash((self.absolute, self.relative))
