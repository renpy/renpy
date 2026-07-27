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

from functools import partial
from typing import Callable

import renpy
from renpy.pyanalysis import pure


def renpy_pure(fn):
    """
    Marks renpy.`fn` as a pure function.
    """

    name = fn

    if not isinstance(name, str):
        name = fn.__name__

    pure("renpy." + name)

    return fn


def callback(f: str | Callable | None = None, name: str | None = None, *, late: bool = False) -> Callable:
    """
    :doc: other

    Registers a callback with Ren'Py.

    `f`
        The callback function to register. If None, this function returns a decorator
        that can be used to register a callback, with name initialized to this value
        (which should be a string), and late given the same value.

    `name`
        The name of the callback to register. If None, the name of the function is used. If
        the function name ends with 'callback' or '_callback', that suffix is removed.
        this then searches config for a variable with that name suffixed with '_callbacks'
        or '_callback', in that order.

    `late`
        Registers the callback when :var:`config.after_init_callbacks` is run.

    This function is intended to be use as a decorator. For example::

        init python:

            @renpy.callback
            def start_callback():
                # Registers with config.start_callbacks.
                pass

            @renpy.callback("label")
            def handle_label(label, abnormal):
                # Registers with config.label_callbacks.
                pass
    """

    if f is None:
        return partial(callback, name=name, late=late)

    if isinstance(f, str):
        if name is not None:
            raise Exception("renpy.callback: f is a string, but name is not None.")
        else:
            return partial(callback, name=f, late=late)

    if name is None:
        name = f.__name__.removesuffix("_callback").removesuffix("_callbacks")

    for i in (f"{name}_callbacks", f"{name}_callback"):
        if hasattr(renpy.config, i):
            if late:

                def late_callback():
                    callback(f, name=name, late=False)

                renpy.config.after_init_callbacks.append(late_callback)
                return f

            target = getattr(renpy.config, i)
            if isinstance(target, list) and f not in target:
                target.append(f)
            elif target is None:
                setattr(renpy.config, i, f)
            else:
                raise Exception(
                    f"renpy.callback: config.{i} is not a list or None - has it already been set to a callback?"
                )
            return f
    else:
        raise Exception(f"renpy.callback: Neither config.{name}_callbacks nor config.{name}_callback exists.")
