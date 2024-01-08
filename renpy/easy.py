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

"""Functions that make the user's life easier."""

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Any

import contextlib
import time

import renpy

Color = renpy.color.Color
color = renpy.color.Color

if PY2:
    from collections import Iterable # type: ignore
else:
    from collections.abc import Iterable


def lookup_displayable_prefix(d):
    """
    Given `d`, a string given a displayable, returns the displayable it
    corresponds to or None if it does not correspond to one.
    """

    prefix, colon, arg = d.partition(":")

    if not colon:
        return None

    fn = renpy.config.displayable_prefix.get(prefix, None)
    if fn is None:
        return None

    return displayable(fn(arg))


def displayable_or_none(d, scope=None, dynamic=True): # type: (Any, dict|None, bool) -> renpy.display.displayable.Displayable|None

    if isinstance(d, renpy.display.displayable.Displayable):
        return d

    if d is None:
        return d

    if isinstance(d, basestring):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif ("[" in d) and renpy.config.dynamic_images and dynamic:
            return renpy.display.image.DynamicImage(d, scope=scope)

        rv = lookup_displayable_prefix(d)

        if rv is not None:
            return rv
        elif d[0] == '#':
            return renpy.store.Solid(d)
        elif "." in d:
            return renpy.store.Image(d)
        else:
            return renpy.store.ImageReference(tuple(d.split()))

    if isinstance(d, Color):
        return renpy.store.Solid(d) # type: ignore

    if isinstance(d, list):
        return renpy.display.image.DynamicImage(d, scope=scope) # type: ignore

    # We assume the user knows what he's doing in this case.
    if hasattr(d, '_duplicate'):
        return d

    if d is True or d is False:
        return d

    raise Exception("Not a displayable: %r" % (d,))


def displayable(d, scope=None): # type(d, dict|None=None) -> renpy.display.displayable.Displayable|None
    """
    :doc: udd_utility
    :name: renpy.displayable

    This takes `d`, which may be a displayable object or a string. If it's
    a string, it converts that string into a displayable using the usual
    rules.
    """

    if isinstance(d, renpy.display.displayable.Displayable):
        return d

    if isinstance(d, basestring):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif ("[" in d) and renpy.config.dynamic_images:
            return renpy.display.image.DynamicImage(d, scope=scope)

        rv = lookup_displayable_prefix(d)

        if rv is not None:
            return rv
        elif d[0] == '#':
            return renpy.store.Solid(d)
        elif "." in d:
            return renpy.store.Image(d)
        else:
            return renpy.store.ImageReference(tuple(d.split()))

    if isinstance(d, Color):
        return renpy.store.Solid(d)

    if isinstance(d, list):
        return renpy.display.image.DynamicImage(d, scope=scope)

    # We assume the user knows what he's doing in this case.
    if hasattr(d, '_duplicate'):
        return d

    if d is True or d is False:
        return d

    raise Exception("Not a displayable: %r" % (d,))


def dynamic_image(d, scope=None, prefix=None, search=None): # type: (Any, dict|None, str|None, list|None) -> renpy.display.displayable.Displayable|None
    """
    Substitutes a scope into `d`, then returns a displayable.

    If `prefix` is given, and a prefix has been given a prefix search is
    performed until a file is found. (Only a file can be used in this case.)
    """

    if not isinstance(d, list):
        d = [ d ]

    def find(name):

        if renpy.exports.image_exists(name):
            return True

        if renpy.loader.loadable(name, directory="images"):
            return True

        if lookup_displayable_prefix(name):
            return True

        if (len(d) == 1) and (renpy.config.missing_image_callback is not None):
            if renpy.config.missing_image_callback(name):
                return True

        return False

    for i in d:

        if not isinstance(i, basestring):
            continue

        if (prefix is not None) and ("[prefix_" in i):

            if scope:
                scope = dict(scope)
            else:
                scope = { }

            for p in renpy.styledata.stylesets.prefix_search[prefix]:  # @UndefinedVariable
                scope["prefix_"] = p

                rv = renpy.substitutions.substitute(i, scope=scope, force=True, translate=False)[0]

                if find(rv):
                    return displayable_or_none(rv)

                if search is not None:
                    search.append(rv)

        else:

            rv = renpy.substitutions.substitute(i, scope=scope, force=True, translate=False)[0]

            if find(rv):
                return displayable_or_none(rv)

            if search is not None:
                search.append(rv)

    rv = d[-1]

    if find(rv):
        return displayable_or_none(rv, dynamic=False)

    return None


def predict(d):
    d = renpy.easy.displayable_or_none(d)

    if d is not None:
        renpy.display.predict.displayable(d)


@contextlib.contextmanager
def timed(name):
    start = time.time()
    yield
    print("{0}: {1:.2f} ms".format(name, (time.time() - start) * 1000.0))


def split_properties(properties, *prefixes):
    """
    :doc: other

    Splits up `properties` into multiple dictionaries, one per `prefix`. This
    function checks each key in properties against each prefix, in turn.
    When a prefix matches, the prefix is stripped from the key, and the
    resulting key is mapped to the value in the corresponding dictionary.

    If no prefix matches, an exception is thrown. (The empty string, "",
    can be used as the last prefix to create a catch-all dictionary.)

    For example, this splits properties beginning with text from
    those that do not::

        text_properties, button_properties = renpy.split_properties(properties, "text_", "")
    """

    rv = [ ]

    for _i in prefixes:
        rv.append({})

    if not properties:
        return rv

    prefix_d = list(zip(prefixes, rv))

    for k, v in properties.items():
        for prefix, d in prefix_d:
            if k.startswith(prefix):
                d[k[len(prefix):]] = v
                break
        else:
            raise Exception("Property {} begins with an unknown prefix.".format(k))

    return rv

def to_list(value, copy=False):
    """
    If the value is an iterable, turns it into a list, otherwise wraps it into one.
    If a list is provided and `copy` is True, a new list will be returned.
    """
    if isinstance(value, list):
        return list(value) if copy else value

    if not isinstance(value, str) and isinstance(value, Iterable):
        return list(value)

    return [value]

def to_tuple(value):
    """
    Same as to_list, but with tuples.
    """
    if isinstance(value, tuple):
        return value

    if not isinstance(value, str) and isinstance(value, Iterable):
        return tuple(value)

    return (value,)

def run_callbacks(cb, *args, **kwargs):
    """
    Runs a callback or list of callbacks that do not expect results
    """

    if cb is None:
        return None

    if isinstance(cb, (list, tuple)):
        rv = None

        for i in cb:
            new_rv = run_callbacks(i, *args, **kwargs)

            if new_rv is not None:
                rv = new_rv

        return rv

    return cb(*args, **kwargs)
