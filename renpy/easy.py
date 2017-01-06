# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

# Functions that make the user's life easier.

from __future__ import print_function
import renpy.display
import renpy.styledata
import contextlib
import time

Color = renpy.color.Color
color = renpy.color.Color


def displayable_or_none(d, scope=None, dynamic=True):

    if isinstance(d, renpy.display.core.Displayable):
        return d

    if d is None:
        return d

    if isinstance(d, basestring):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif ("[" in d) and renpy.config.dynamic_images and dynamic:
            return renpy.display.image.DynamicImage(d, scope=scope)
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


def displayable(d, scope=None):
    """
    :doc: udd_utility
    :name: renpy.displayable

    This takes `d`, which may be a displayable object or a string. If it's
    a string, it converts that string into a displayable using the usual
    rules.
    """

    if isinstance(d, renpy.display.core.Displayable):
        return d

    if isinstance(d, basestring):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif ("[" in d) and renpy.config.dynamic_images:
            return renpy.display.image.DynamicImage(d, scope=scope)
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


def dynamic_image(d, scope=None, prefix=None):
    """
    Substitutes a scope into `d`, then returns a displayable.

    If `prefix` is given, and a prefix has been given a prefix search is
    performed until a file is found. (Only a file can be used in this case.)
    """

    if not isinstance(d, list):
        d = [ d ]

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

                if renpy.loader.loadable(rv):
                    return displayable_or_none(rv)

                if renpy.exports.image_exists(rv):
                    return displayable_or_none(rv)

        else:

            rv = renpy.substitutions.substitute(i, scope=scope, force=True, translate=False)[0]

            if renpy.loader.loadable(rv):
                return displayable_or_none(rv)

            if renpy.exports.image_exists(rv):
                return displayable_or_none(rv)

    else:

        return displayable_or_none(d[-1], dynamic=False)


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

    For example, this code splits properties beginning with text from
    those that do not::

        text_properties, button_properties = renpy.split_properties("text_", "")
    """

    rv = [ ]

    for _i in prefixes:
        rv.append({})

    if not properties:
        return rv

    prefix_d = list(zip(prefixes, rv))

    for k, v in properties.iteritems():
        for prefix, d in prefix_d:
            if k.startswith(prefix):
                d[k[len(prefix):]] = v
                break
        else:
            raise Exception("Property {} begins with an unknown prefix.".format(k))

    return rv
