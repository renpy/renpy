# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from typing import Any, Callable, ClassVar, final

# Allow pickling NoneType.
import builtins

builtins.NoneType = type(None)  # type: ignore


class Object:
    """
    Base class for various things in Ren'Py.
    Contains methods to simplify serialization.
    """

    __version__: ClassVar[int] = 0
    """
    Version of the type. Setting this on instance would be silently ignored.

    This is used when type is changed in a way that requires a some extra
    work to be done when unpickling the object. When you only add a new field,
    you could use class variable with a sensible default value.
    """

    nosave: list[str] = []
    """
    A list of field names that would be automatically removed from the
    pickle data. This is used to prevent storing unpickleable, cached
    or otherwise unnecessary data.
    """

    def __getstate__(self) -> dict[str, Any]:
        rv = vars(self).copy()

        for f in self.nosave:
            if f in rv:
                del rv[f]

        rv["__version__"] = self.__version__

        return rv

    after_setstate: Callable[[], Any] | None = None
    """
    A function that is called after the object is unpickled.
    This is mostly used to set values for `nosave` fields.
    """

    def after_upgrade(self, version: int):
        """
        This is called after the object is unpickled, and the version
        in pickled object is less than the current version.

        `version` is the version of the pickled object.
        """

    def __setstate__(self, new_dict: dict[str, Any]):
        version = new_dict.pop("__version__", 0)

        vars(self).update(new_dict)

        if version != self.__version__:
            self.after_upgrade(version)

        if self.after_setstate is not None:
            self.after_setstate()

    def __init_subclass__(cls) -> None:
        # Check that type doesn't have slots.
        if getattr(cls, "__slots__", ()):
            raise TypeError("nonempty __slots__ not supported for subtype of 'renpy.object.Object")


sentinels: dict[str, "Sentinel"] = {}


@final
class Sentinel:
    """
    This is used to represent a sentinel object. There will be exactly one
    sentinel object with a name existing in the system at any time.
    """

    # NOTE: This is intentionally returns Any, not Sentinel, so one could
    # type hint arguments like `str | None = Sentinel` or check `if x is Sentinel`
    # and not see type errors, but that mean that from typing perspective
    # different sentinels are the same.

    def __new__(cls, name: str) -> Any:
        rv = sentinels.get(name, None)

        if rv is None:
            rv = object.__new__(cls)
            sentinels[name] = rv

        return rv

    def __init__(self, name: str):
        self.name: str = name

    def __repr__(self):
        return f"{type(self).__module__}.{type(self).__name__}({self.name!r})"

    def __reduce__(self):
        return (Sentinel, (self.name,))
