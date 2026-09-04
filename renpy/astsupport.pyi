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

from typing import Any, final

def hash32(s: Any) -> int:
    """
    Returns a stable 32-bit hash of the string `s`.

    `s`
        A unicode string. Other types will be coerced to unicode before hashing.
    """

def hash64(s: Any) -> int:
    """
    Returns a stable 64-bit hash of the string `s`.

    `s`
        A unicode string. Other types will be coerced to unicode before hashing.
    """

@final
class PyExpr(str):
    """
    Represents a string containing a python expression.
    """

    filename: str
    linenumber: int
    column: int
    hashcode: int

    def __new__(
        cls,
        s: str,
        /,
        *,
        filename: str,
        linenumber: int,
        column: int = 0,
    ) -> PyExpr:
        """
        Creates a PyExpr from `s`, the code found at `filename`, `linenumber`,
        `column`. The hash is computed automatically from `s`.
        """

    @staticmethod
    def from_logical_line(
        text: str,
        start: int,
        end: int,
        filename: str,
        linenumber: int,
        column: int,
        /,
    ) -> PyExpr:
        """
        Used by the lexer to make a PyExpr, rapidly adjusting `linenumber` and
        `column` to account for any newlines found in `text` between the start
        of the logical line and `start`.

        `text`
            The full text of the logical line that `text[start:end]` is drawn
            from.

        `start`, `end`
            The span within `text` that is the expression.

        `filename`
            The name of the file the expression is in.

        `linenumber`
            The line number the logical line starts at.

        `column`
            The column the logical line starts at.
        """
