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

"""Functions that make the user's life easier."""

from typing import Any, Callable
from collections.abc import Iterable

import contextlib
import time

import renpy

from renpy.types import Displayable, DisplayableLike

# Kept for backwards compatibility.
from renpy.color import Color as Color, Color as color  # noqa: F401


def lookup_displayable_prefix(d: str) -> Displayable | None:
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


def displayable_or_none(
    d: DisplayableLike | None,
    scope: dict[str, Any] | None = None,
    dynamic: bool = True,
) -> Displayable | None:
    if isinstance(d, renpy.display.displayable.Displayable):
        return d

    if d is None:
        return d

    if isinstance(d, str):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif ("[" in d) and renpy.config.dynamic_images and dynamic:
            return renpy.display.image.DynamicImage(d, scope=scope)

        rv = lookup_displayable_prefix(d)

        if rv is not None:
            return rv
        elif d[0] == "#":
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
    if hasattr(d, "_duplicate"):
        return d

    if d is True or d is False:
        return d  # type: ignore

    raise Exception(f"Not a displayable: {d!r}")


def displayable(d: DisplayableLike, scope: dict[str, Any] | None = None) -> Displayable:
    """
    :doc: udd_utility
    :name: renpy.displayable

    This takes `d`, which may be a displayable object or a string. If it's
    a string, it converts that string into a displayable using the usual
    rules.
    """

    if isinstance(d, renpy.display.displayable.Displayable):
        return d

    if isinstance(d, str):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif ("[" in d) and renpy.config.dynamic_images:
            return renpy.display.image.DynamicImage(d, scope=scope)

        rv = lookup_displayable_prefix(d)

        if rv is not None:
            return rv
        elif d[0] == "#":
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
    if hasattr(d, "_duplicate"):
        return d

    if d is True or d is False:
        return d  # type: ignore

    raise Exception("Not a displayable: %r" % (d,))


def dynamic_image(
    d: Any,
    scope: dict[str, Any] | None = None,
    prefix: str | None = None,
    search: list[str] | None = None,
) -> Displayable | None:
    """
    Substitutes a scope into `d`, then returns a displayable.

    If `prefix` is given, and a prefix has been given a prefix search is
    performed until a file is found. (Only a file can be used in this case.)
    """

    if not isinstance(d, list):
        d = [d]

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
        if not isinstance(i, str):
            continue

        if (prefix is not None) and ("[prefix_" in i):
            if scope:
                scope = dict(scope)
            else:
                scope = {}

            for p in renpy.styledata.stylesets.prefix_search[prefix]:
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


def predict(d: Any):
    d = renpy.easy.displayable_or_none(d)

    if d is not None:
        renpy.display.predict.displayable(d)


@contextlib.contextmanager
def timed(name: str):
    start = time.time()
    yield
    print(f"{name}: {(time.time() - start) * 1000.0:.2f} ms")


def split_properties(properties: dict[str, Any], *prefixes: str) -> list[dict[str, Any]]:
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

    rv = [{} for _ in prefixes]
    if not properties:
        return rv

    prefix_d = list(zip(prefixes, rv))

    for k, v in properties.items():
        for prefix, d in prefix_d:
            if k.startswith(prefix):
                d[k.removeprefix(prefix)] = v
                break
        else:
            raise Exception(f"Property {k} begins with an unknown prefix.")

    return rv


def to_list[T](value: T | Iterable[T], copy: bool = False) -> list[T]:
    """
    If the value is an iterable, turns it into a list, otherwise wraps it into one.
    If a list is provided and `copy` is True, a new list will be returned.
    """

    if isinstance(value, list):
        return list(value) if copy else value

    elif isinstance(value, str):
        return [value]  # type: ignore

    elif isinstance(value, Iterable):
        return list(value)

    else:
        return [value]


def to_tuple[T](value: T | Iterable[T]) -> tuple[T, ...]:
    """
    Same as to_list, but with tuples.
    """

    if isinstance(value, tuple):
        return value

    elif isinstance(value, str):
        return (value,)  # type: ignore

    elif isinstance(value, Iterable):
        return tuple(value)

    else:
        return (value,)


def run_callbacks[**P, R](
    cb: Callable[P, R] | list[Callable[P, R]] | None,
    *args: P.args,
    **kwargs: P.kwargs,
) -> R | None:
    """
    Runs a callback or list of callbacks applying the arguments.

    Returns the result of the last callback that returns a value, or None if
    no callback returns a value.
    """

    if cb is None:
        return None

    if not isinstance(cb, (list, tuple)):
        cb = [cb]

    rv = None

    for i in cb:
        new_rv = i(*args, **kwargs)
        if new_rv is not None:
            rv = new_rv

    return rv
