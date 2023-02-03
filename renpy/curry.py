# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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


import functools


class Curry(object):
    # essentialy the same as Partial, kept for compatibility

    hash = None

    def __init__(self, callable, *args, **kwargs):  # @ReservedAssignment
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.__doc__ = getattr(self.callable, "__doc__", None)
        self.__name__ = getattr(self.callable, "__name__", None)

    def __call__(self, *args, **kwargs):

        merged_kwargs = dict(self.kwargs)
        merged_kwargs.update(kwargs)

        return self.callable(*(self.args + args), **merged_kwargs)

    def __repr__(self):
        return "<curry %s %r %r>" % (self.callable, self.args, self.kwargs)

    def __eq__(self, other):

        return (
            isinstance(other, Curry) and
            self.callable == other.callable and
            self.args == other.args and
            self.kwargs == other.kwargs)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):

        if self.hash is None:
            self.hash = hash(self.callable) ^ hash(self.args)

            for i in self.kwargs.items():
                self.hash ^= hash(i)

        return self.hash


class Partial(functools.partial):
    """
    Stores a callable and some arguments. When called, calls the
    callable with the stored arguments and the additional arguments
    supplied to the call.
    """

    __slots__ = ("hash",)


    def __repr__(self):
        return "<partial %s %r %r>" % (self.func, self.args, self.keywords)

    def __eq__(self, other):

        return (
            isinstance(other, Partial) and
            self.func == other.func and
            self.args == other.args and
            self.keywords == other.keywords)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        _hash = getattr(self, 'hash', None)

        if _hash is None:
            _hash = hash(self.func) ^ hash(self.args)

            for i in self.keywords.items():
                _hash ^= hash(i)

            setattr(self, 'hash', _hash)

        return _hash


def curry(fn):
    """
    Takes a callable, and returns something that, when called, returns
    something that when called again, calls the function. So
    basically, the thing returned from here when called twice does the
    same thing as the function called once.
    """

    rv = Partial(Partial, fn)
    rv.__doc__ = getattr(fn, "__doc__", None)
    rv.__name__ = getattr(fn, "__name__", None) # type: ignore
    return rv


def partial(function, *args, **kwargs):
    """
    Stores the arguments and keyword arguments of function, and
    returns something that, when called, calls the function with
    a combination of the supplied arguments and the arguments of
    the second call.
    """

    return Partial(function, *args, **kwargs)
