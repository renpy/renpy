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


# Allow pickling NoneType.
import builtins

builtins.NoneType = type(None)  # type: ignore


class Object:
    """
    Our own base class. Contains methods to simplify serialization.
    """

    __version__ = 0
    """
    Version of the type. Setting this on instance would be silently ignored.
    This is used when type is changed in a way that requires a some extra
    work to be done when unpickling the object. When you only add a new field,
    you could use class variable with a sensible default value.
    """

    nosave = []
    """
    A list of field names that would be automatically removed from the
    pickle data. This is used to prevent storing unpickleable, cached
    or otherwise unnecessary data.

    This is a class variable, and setting it on an instance would be
    silently ignored.
    """

    def __getstate__(self):
        rv = self.__dict__.copy()

        for f in self.nosave:
            rv.pop(f, None)

        rv["__version__"] = self.__version__

        return rv

    after_setstate = None
    """
    If not None, this should be a method that is called with no arguments
    after the object is unpickled.

    This is mostly used to set values for `nosave` fields.
    """

    def after_upgrade(self, version):
        """
        This is called after the object is unpickled, and the version
        in pickled object is different from the version of the type.
        `version` is the version of the pickled object.
        """

        raise NotImplementedError

    def __setstate__(self, new_dict):
        version = new_dict.pop("__version__", 0)

        self.__dict__.update(new_dict)

        if version != self.__version__:
            self.after_upgrade(version)

        if self.after_setstate:
            self.after_setstate()

    def __init_subclass__(cls):
        if getattr(cls, "__slots__", None):
            raise TypeError("nonempty __slots__ not supported for subtype of 'renpy.object.Object'")

        if cls.__version__ and cls.after_upgrade is Object.after_upgrade:
            raise TypeError(f"class {cls.__name__} does not override 'after_upgrade' method")


sentinels = {}


class Sentinel:
    """
    This is used to represent a sentinel object. There will be exactly one
    sentinel object with a name existing in the system at any time.
    """

    def __new__(cls, name):
        rv = sentinels.get(name, None)

        if rv is None:
            rv = object.__new__(cls)
            sentinels[name] = rv

        return rv

    def __init__(self, name):
        self.name = name

    def __reduce__(self):
        return (Sentinel, (self.name,))
