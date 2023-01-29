# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

# Other text-related things.

from __future__ import annotations
from typing import Any, overload

from .text import Text

from ..display.core import DisplayableArguments

# This checks the text tags in a string to be sure they are all matched, and
# properly nested. It returns an error message, or None if the line is okay.


def check_text_tags(s: str, /) -> str | None:
    ...


@overload
def filter_text_tags(s: str, /, *, allow: set[str]) -> str:
    ...


@overload
def filter_text_tags(s: str, /, *, deny: set[str]) -> str:
    ...


class ParameterizedText(object):
    def __init__(self, style: str = 'default', **properties: Any) -> None:
        self.style = style
        self.properties = properties

    _duplicatable = True

    def _duplicate(self, args: DisplayableArguments | None) -> Text:
        ...
