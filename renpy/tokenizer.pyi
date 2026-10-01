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

from collections.abc import Iterator
from enum import IntEnum
from typing import Literal, final

class TokenKind(IntEnum):
    """Enumeration of token kinds."""

    NEWLINE = 1
    "A single '\n'."
    COMMENT = 2
    "A '#' up to, but not including, the terminating newline."
    WORD = 3
    "The intersection of Python NAME and NUMBER, but less strict."
    OP = 4
    "Python OP, plus '$' and '?'."
    STRING_START = 5
    "The prefix and opening quote of a string literal."
    STRING_MIDDLE = 6
    "A run of literal text inside a string literal."
    STRING_END = 7
    "The closing quote of a string literal."
    ENDMARKER = 8
    "The end of the data."
    ERRORTOKEN = 9
    "An erroneous token."

@final
class TokenInfo:
    """Information about a single token."""

    kind: TokenKind
    """The kind of the token."""
    string: str
    """The string representation of the token."""

    @property
    def span(self) -> tuple[int, int]:
        """The (start, end) positions of the token in the source."""

    @property
    def start(self) -> tuple[int, int]:
        """The starting (line number, 1-based column) of the token."""

    @property
    def end(self) -> tuple[int, int]:
        """The ending (line number, 1-based column) of the token."""

    def __init__(
        self,
        kind: TokenKind,
        string: str,
        start_pos: int,
        end_pos: int,
        start_lineno: int,
        start_column: int,
        end_lineno: int,
        end_column: int,
    ) -> None: ...

class Tokenizer:
    """
    Incremental tokenizer for Ren'Py/Python source, with support for
    (f-)string literals, replacement fields and format specs.
    """

    @property
    def data(self) -> str:
        """The source being tokenized."""

    @property
    def pos(self) -> int:
        """Current position in the data."""

    @property
    def lineno(self) -> int:
        """Current (1-based) line number."""

    @property
    def line_start(self) -> int:
        """Position of the start of the current physical line."""

    @property
    def split_char(self) -> Literal["{", "["]:
        """
        The bracket that opens a substitution. With "{", replacement
        fields follow Python f-string rules (only f-strings split).
        With "[", every string may contain Ren'Py-style "[...]"
        substitutions, and "{...}" is literal text.
        """

    @property
    def depth(self) -> int:
        """Number of currently open brackets and strings."""

    def __init__(
        self,
        data: str,
        pos: int = 0,
        lineno: int = 1,
        split_char: Literal["{", "["] = "{",
    ) -> None:
        """
        Raises `ValueError` if `pos` is out of range or `split_char`
        is not '{' or '['.
        """

    def next_token(self) -> TokenInfo:
        """
        Return the next token and advance the position. Returns an
        `ENDMARKER` token at the end of the data.

        Erroneous input (unterminated strings, unclosed or mismatched
        brackets, tabs, control characters, or a stray backslash) is
        reported as `ERRORTOKEN` tokens whose string is the error message
        and whose span is the erroneous input, and skipped over.
        """

    def iter_tokens(self) -> Iterator[TokenInfo]:
        """
        Yield tokens from the current position until and including the
        ENDMARKER token.
        """
