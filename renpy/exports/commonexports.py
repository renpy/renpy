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

from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
)
from typing import Any, Callable, overload  # type: ignore
from renpy.compat import (
    PY2,
    basestring,
    bchr,
    bord,
    chr,
    open,
    pystr,
    range,
    round,
    str,
    tobytes,
    unicode,
)  # *

from renpy.pyanalysis import const, pure, not_const


@overload
def renpy_pure(fn: str) -> str: ...


@overload
def renpy_pure[T](fn: Callable[..., T]) -> Callable[..., T]: ...


def renpy_pure(fn: str | Callable[..., Any]) -> str | Callable[..., Any]:
    """
    Marks renpy.`fn` as a pure function.
    """

    if isinstance(fn, str):
        name = fn
    else:
        name = fn.__name__

    pure(f"renpy.{name}")

    return fn
