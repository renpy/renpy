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

"""
A fast, incremental tokenizer for Ren'Py scripts and the Python embedded
in them.

Tokens are coarser than Python's `tokenize`:

- `WORD` covers both names and numbers. `1.5` comes out as `WORD`, `OP`,
  `WORD`, and `1e-3` as `WORD`, `OP`, `WORD`. The parser puts them back
  together.
- `OP` covers Python operators plus `$` and `?`. Brackets are tracked, and
  a closing bracket that doesn't match is reported as an error.
- Indentation isn't tokenized. Spaces and backslash-newline continuations
  between tokens are skipped, and every newline in code becomes a
  `NEWLINE` token, even inside brackets. Line structure is left to the
  parser.
- A string literal is split the way PEP 701 splits f-strings:
  `STRING_START`, then any number of `STRING_MIDDLE` and replacement
  fields, then `STRING_END`. Plain strings use the same tokens. Quotes can
  be `'`, `"` or `` ` ``, single or tripled. The prefix is any of r, u, b,
  f, rb, br, rf or fr, in any case. Escapes are kept as written, not
  decoded. A newline inside a string is part of `STRING_MIDDLE`, even if
  the string isn't triple-quoted.
- In f-strings, `{` opens a replacement field and `{{` is literal text.
  The field's contents are tokenized as code until the matching `}`. A `:`
  at the field's top level starts a format spec, which is literal text
  that can contain nested `{...}` fields. There's no special handling for
  `!r`-style conversions or for `=`. They're just operators.
- `Tokenizer.renpy_substitution_string` tokenizes the inside of a Ren'Py
  string. There are no quotes, the text ends with the data, and fields
  are `[...]`. A Ren'Py format spec is plain text up to `]`, so `[` and
  `{` don't nest there.

Errors don't raise. Each one becomes an `ERRORTOKEN`: its `string` is the
message and its span covers the bad input. The tokenizer then moves on.
Errors include tabs, control characters, a stray backslash, unmatched or
mismatched brackets, and nesting deeper than 255. At the end of the data,
each construct that's still open produces one error, innermost first,
followed by `ENDMARKER`.
"""

from collections.abc import Iterator
from enum import IntEnum
from typing import final

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
    def depth(self) -> int:
        """Number of currently open brackets and strings."""

    def __init__(self, data: str, pos: int = 0, lineno: int = 1) -> None: ...
    @classmethod
    def renpy_substitution_string(cls, data: str) -> Tokenizer:
        """
        Tokenizes `data` as the content of a Ren'Py string: literal text
        with [substitutions] terminated by the end of the data.
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
