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


from __future__ import annotations

from typing import Iterator

import os
import io
import re
import sys
import tokenize
import keyword
import enum

_DEBUG_TOKENIZATION = "RENPY_DEBUG_TOKENIZATION" in os.environ


class Line:
    """
    Represents a logical line in a file, which is a sequence of tokens.
    Line should ends with a NEWLINE token.
    """

    __slots__ = ['tokens', 'indent_depth', '_text']

    def __init__(self, token: Token, *tokens: Token, indent_depth: int):
        self.tokens: tuple[Token, ...] = (token, *tokens)
        """
        List of tokens that make up this line.
        """

        self.indent_depth: int = indent_depth
        """
        Indentation depth of this line.
        """

        self._text = None

        if not _DEBUG_TOKENIZATION:
            return

        has_newline = False
        physical_offset = token.physical_offset
        prev_row = -1
        prev_col = -1
        tokens_iter = iter(self.tokens)
        for t in tokens_iter:
            # If there is a change in physical offset in between tokens, it
            # is impossible to locate the line in the file.
            if t.physical_offset != physical_offset:
                raise ValueError("Tokens in logical line must be contiguous.")

            if t.lineno < prev_row or t.lineno == prev_row and t.col_offset < prev_col:
                raise ValueError(f"start ({t.lineno}, {t.lineno}) precedes "
                                 f"previous end ({prev_row}, {prev_col})")

            prev_row = t.end_lineno
            prev_col = t.end_col_offset

            if t.kind is TokenKind.INDENT or t.kind is TokenKind.DEDENT:
                raise ValueError("Line can't contain INDENT or DEDENT tokens.")

            if t.kind is TokenKind.NEWLINE:
                has_newline = True
                break

        if list(tokens_iter):
            raise ValueError("NEWLINE must be the last token.")

        if not has_newline:
            raise ValueError("Line must end with NEWLINE token.")

    @property
    def filename(self) -> str:
        """
        Elided filename where line is located.
        """

        return self.tokens[0].filename

    @property
    def start(self) -> tuple[int, int]:
        """
        Linenumber, col offset of start of logical line.
        """

        return (self.tokens[0].lineno, self.tokens[0].col_offset)

    @property
    def end(self) -> tuple[int, int]:
        """
        Linenumber, col offset of end of logical line.
        """

        return (self.tokens[-1].end_lineno, self.tokens[-1].end_col_offset)

    @property
    def text(self) -> str:
        """
        Full text of logical line including whitespaces and comments.
        """

        if self._text is None:
            prev_row = self.tokens[0].lineno
            prev_col = 0
            cont_line = False
            result: list[str] = []

            for t in self.tokens:
                # Don't add spurious spaces before new line.
                if t.kind in (TokenKind.NL, TokenKind.NEWLINE):
                    cont_line = False
                    prev_row += 1
                    prev_col = 0
                    continue

                if row_offset := t.lineno - prev_row:
                    if cont_line:
                        # Assume people continue lines with single space before slash.
                        result.append(" \\")

                    result.append("\n" * row_offset)
                    prev_col = 0

                if col_offset := t.col_offset - prev_col:
                    result.append(" " * col_offset)

                result.append(t.string)
                prev_row = t.end_lineno
                prev_col = t.end_col_offset
                cont_line = True

            self._text = "".join(result)

        return self._text

    def __repr__(self):
        return f"<Line {self.filename} {self.start}-{self.end}>"


class TokenKind(enum.StrEnum):
    """
    Enum of all possible `Token.kind` values.

    Equality can be checked as lower-case string value.
    """

    # Special tokens.
    INDENT = enum.auto()
    DEDENT = enum.auto()
    COMMENT = enum.auto()

    # Non-terminating and terminating new lines.
    # This is always \n in Ren'Py.
    NL = enum.auto()
    NEWLINE = enum.auto()

    # Names.
    NAME = enum.auto()  # Any name.
    KEYWORD = enum.auto()
    IDENTIFIER = enum.auto()
    NON_IDENTIFIER = enum.auto()

    # Numbers.
    NUMBER = enum.auto()  # Any number.
    HEX = enum.auto()
    BINARY = enum.auto()
    OCTAL = enum.auto()
    IMAG = enum.auto()
    FLOAT = enum.auto()
    INT = enum.auto()

    # Strings.
    STRING = enum.auto()  # Any string.
    BYTES = enum.auto()
    F_STRING = enum.auto()
    RAW_TRIPLE_STRING = enum.auto()
    TRIPLE_STRING = enum.auto()
    RAW_SINGLE_STRING = enum.auto()
    SINGLE_STRING = enum.auto()

    # Operators.
    OP = enum.auto()  # Any operator.
    DOLLAR = enum.auto()
    LPAR = enum.auto()
    RPAR = enum.auto()
    LSQB = enum.auto()
    RSQB = enum.auto()
    COLON = enum.auto()
    COMMA = enum.auto()
    SEMI = enum.auto()
    PLUS = enum.auto()
    MINUS = enum.auto()
    STAR = enum.auto()
    SLASH = enum.auto()
    VBAR = enum.auto()
    AMPER = enum.auto()
    LESS = enum.auto()
    GREATER = enum.auto()
    EQUAL = enum.auto()
    DOT = enum.auto()
    PERCENT = enum.auto()
    LBRACE = enum.auto()
    RBRACE = enum.auto()
    EQEQUAL = enum.auto()
    NOTEQUAL = enum.auto()
    LESSEQUAL = enum.auto()
    GREATEREQUAL = enum.auto()
    TILDE = enum.auto()
    CIRCUMFLEX = enum.auto()
    LEFTSHIFT = enum.auto()
    RIGHTSHIFT = enum.auto()
    DOUBLESTAR = enum.auto()
    PLUSEQUAL = enum.auto()
    MINEQUAL = enum.auto()
    STAREQUAL = enum.auto()
    SLASHEQUAL = enum.auto()
    PERCENTEQUAL = enum.auto()
    AMPEREQUAL = enum.auto()
    VBAREQUAL = enum.auto()
    CIRCUMFLEXEQUAL = enum.auto()
    LEFTSHIFTEQUAL = enum.auto()
    RIGHTSHIFTEQUAL = enum.auto()
    DOUBLESTAREQUAL = enum.auto()
    DOUBLESLASH = enum.auto()
    DOUBLESLASHEQUAL = enum.auto()
    AT = enum.auto()
    ATEQUAL = enum.auto()
    RARROW = enum.auto()
    ELLIPSIS = enum.auto()
    COLONEQUAL = enum.auto()


class Token:
    """
    Represents a token in a file.
    """

    __slots__ = [
        'kind',
        'exact_kind',
        'string',
        'filename',
        'lineno',
        'col_offset',
        'end_lineno',
        'end_col_offset',
        'physical_offset',
    ]

    def __init__(
        self,
        type: int,
        string: str,
        filename: str,
        lineno: int,
        col_offset: int,
        end_lineno: int,
        end_col_offset: int,
        physical_offset: tuple[int, int],
    ):
        if type == tokenize.ERRORTOKEN and string == "$":  # FIXME: In 3.12 it is OP
            kind = TokenKind.OP
            exact_kind = TokenKind.DOLLAR
        elif type == tokenize.ERRORTOKEN:
            raise SyntaxError(f"Error token with value: {string!r} on line "
                              f"{lineno + physical_offset[0]}")

        # Exact name is one of predefined.
        elif type == tokenize.OP:
            kind = TokenKind.OP
            type = tokenize.EXACT_TOKEN_TYPES[string]
            exact_kind = TokenKind(tokenize.tok_name[type].lower())

        # f-strings and bytes are expressions in Ren'Py,
        # and raw strings are handled differently.
        elif type == tokenize.STRING:
            kind = TokenKind.STRING

            prefix = re.match(
                r'([urfbURFB])*("|\'|"""|\'\'\')', string)
            assert prefix is not None
            mods = prefix.group(1) or ""
            quotes = prefix.group(2)

            if "b" in mods or "B" in mods:
                exact_kind = TokenKind.BYTES
            elif "f" in mods or "F" in mods:
                exact_kind = TokenKind.F_STRING
            elif quotes == "'''" or quotes == '"""':
                if "r" in mods or "R" in mods:
                    exact_kind = TokenKind.RAW_TRIPLE_STRING
                else:
                    exact_kind = TokenKind.TRIPLE_STRING
            else:
                if "r" in mods or "R" in mods:
                    exact_kind = TokenKind.RAW_SINGLE_STRING
                else:
                    exact_kind = TokenKind.SINGLE_STRING

        # Split numbers into complex, float, and integer.
        elif type == tokenize.NUMBER:
            kind = TokenKind.NUMBER
            if string.startswith("0x"):
                exact_kind = TokenKind.HEX
            elif string.startswith("0b"):
                exact_kind = TokenKind.BINARY
            elif string.startswith("0o"):
                exact_kind = TokenKind.OCTAL
            elif string[-1] in "jJ":
                exact_kind = TokenKind.IMAG
            else:
                symbols = set(string)
                # Definitely a float.
                if "." in symbols:
                    exact_kind = TokenKind.FLOAT

                # 00e0 is a float and can be interpreted as hex,
                # but we assume this is a float.
                elif symbols.intersection("eE"):
                    exact_kind = TokenKind.FLOAT

                else:
                    exact_kind = TokenKind.INT

        # Names can be keywords or identifiers.
        # Otherwise it is a 0name, which is not an identifier,
        # but e.g. is a valid attribute name.
        elif type == tokenize.NAME:
            kind = TokenKind.NAME

            if keyword.iskeyword(string):
                exact_kind = TokenKind.KEYWORD
            elif string.isidentifier():
                exact_kind = TokenKind.IDENTIFIER
            else:
                exact_kind = TokenKind.NON_IDENTIFIER

        else:
            kind = TokenKind(tokenize.tok_name[type].lower())
            exact_kind = TokenKind(tokenize.tok_name[type].lower())

        self.kind: TokenKind = kind
        """
        Kind of the token, such as TokenKind.NAME, TokenKind.OP or TokenKind.NUMBER.
        Can be iterpreted as a corresponding lower-cased string.
        """

        self.exact_kind: TokenKind = exact_kind
        """
        Exact kind of the token, such as TokenKind.KEYWORD, TokenKind.DOLLAR or TokenKind.INT.
        Can be iterpreted as a corresponding lower-cased string.
        """

        self.string: str = string
        """
        String value of the token.
        """

        self.filename: str = filename
        """
        Elided filename where token is located.
        """

        # Positions of the token in the source.
        self.lineno: int = lineno
        self.col_offset: int = col_offset
        self.end_lineno: int = end_lineno
        self.end_col_offset: int = end_col_offset

        # Offset from logical positions to physical positions.
        self.physical_offset: tuple[int, int] = physical_offset

    def __repr__(self):
        string = repr(self.string)
        if len(string) > 30:
            string = string[:15] + "..." + string[-15:]

        location = f"{self.lineno}:{self.col_offset}-{self.end_lineno}:{self.end_col_offset}"
        return f"<Token {self.exact_kind._name_!r} {string} {self.filename} {location}>"


class Tokenizer:
    """
    This class is used to read files and strings as RenPy source code.

    First, this class reads passed buffer one line at a time, saving normalized
    physical lines.

    List of normalization and checks that this class performs during file read:
        1. Strips the BOM from the start of the file.
        2. Converts _ren.py files to equivalent .rpy files.
        3. Normalizes line endings to \n.
        4. Disallows \t and \f characters.

    Then, it tokenizes read lines saving result tokens into a list.
    Tokenization works the same as Python `tokenize.generate_tokens` function
    with the following additional normalizations and checks:
        1. It produces Token objects instead of tuples.
        2. It allow 0-prefix non-zero numbers (e.g. 001).
        3. It allows for names to start with numbers (e.g. 1foo).
        4. It checks for non-terminated strings and parenthesis.
        5. It checks for parenthesis order of closing.

    After file is tokenized, it can be used to list logical lines and group them
    into indented blocks.
    """

    @staticmethod
    def _strip_bom(lines: Iterator[str]) -> Iterator[str]:
        first = next(lines)
        if first.startswith('\ufeff'):
            yield first[1:]
        else:
            yield first

        yield from lines

    def _ren_py_to_rpy(self, filename: str, lines: Iterator[str]) -> Iterator[str]:
        """
        Takes an iterator of lines from a _ren.py file, and returns an iterator
        of lines of equivalent .rpy file. This should retain line numbers.
        """

        # The prefix prepended to Python lines.
        prefix = ""

        # Col offset of non-prefixed lines.
        col_offset = self.col_offset

        # Possible states.
        IGNORE = 0
        RENPY = 1
        PYTHON = 2

        # The state the state machine is in.
        state = IGNORE

        open_linenumber = 0

        for linenumber, l in enumerate(lines, start=1):
            if state != RENPY:
                if l.startswith('"""renpy'):
                    state = RENPY
                    open_linenumber = linenumber
                    self.col_offset = col_offset
                    yield "\n"
                    continue

            if state == RENPY:
                if l.strip() == '"""':
                    state = PYTHON
                    yield "\n"
                    continue

                # Ignore empty and comments.
                sl = l.strip()
                if not sl:
                    yield l
                    continue

                if sl[0] == "#":
                    yield l
                    continue

                # Determine the prefix.
                prefix = ""
                for i in l:
                    if i != ' ':
                        break
                    prefix += ' '

                # If the line ends in ":", add 4 spaces to the prefix.
                # XXX: This does not work for 'init python: # Comment'...
                if sl[-1] == ":":
                    prefix += "    "

                # Deduct the column offset, so error positions will be correct
                # for python code.
                self.col_offset -= len(prefix)

                yield l
                continue

            if state == PYTHON:
                if l == "\n":
                    yield l
                else:
                    yield f"{prefix}{l}"
                continue

            if state == IGNORE:
                yield "\n"
                continue

        if self.no_errors:
            return

        if state == IGNORE:
            raise SyntaxError(f'In {filename!r}, there are no """renpy blocks, so every line is ignored.')

        if state == RENPY:
            raise SyntaxError(f'In {filename!r}, there is a """renpy block '
                              f'at line {open_linenumber} that is not terminated by """.')

    @staticmethod
    def _disallow_bad_whitespaces(lines: Iterator[str]) -> Iterator[str]:
        for l in lines:
            if "\t" in l:
                raise SyntaxError(f"Tab character is not allowed in Ren'Py scripts.")

            if "\f" in l:
                raise SyntaxError(f"Form feed character is not allowed in Ren'Py scripts.")

            yield l

    @classmethod
    def from_string(
        cls,
        filename: str,
        code: str, *,
        lineno=0,
        col_offset=0,
        no_errors=False,
    ):
        return cls(filename, io.StringIO(code, newline=None),
                   lineno=lineno, col_offset=col_offset, no_errors=no_errors)

    @classmethod
    def from_file(
        cls,
        filename: str, *,
        no_errors=False,
    ):
        if os.path.isabs(filename):
            fn = filename
        else:
            from renpy.lexer import unelide_filename
            fn = unelide_filename(filename)

        return cls(filename, open(fn, encoding="utf-8", errors="python_strict", newline=None),
                   no_errors=no_errors)

    def __init__(
        self,
        filename: str,
        lines: Iterator[str], *,
        lineno=0,
        col_offset=0,
        no_errors=False,
    ):
        from collections import deque
        self.original_filename: str = filename
        from renpy.lexer import elide_filename
        self.filename: str = elide_filename(filename)

        self.linenumber: int = lineno
        self.col_offset: int = col_offset

        self.no_errors: bool = no_errors

        lines = self._strip_bom(lines)

        if filename.endswith("_ren.py"):
            lines = self._ren_py_to_rpy(filename, lines)

        if not no_errors:
            lines = self._disallow_bad_whitespaces(lines)

        # List of tokenized, normalized physical lines.
        self._physical_lines: list[str] = []

        # This is used to buffer lines that are read but not tokenized,
        # so one can list physical lines without more expensive tokenization
        # pass.
        self._next_lines_buffer: deque[str] = deque()

        # Generator of lines that are yet to be read.
        self._next_lines = lines

        # List of result tokens.
        self._tokens: list[Token] = []

        self._tokenized = None

    def _readline(self):
        if self._next_lines_buffer:
            line = self._next_lines_buffer.popleft()
        else:
            line = next(self._next_lines)

        self._physical_lines.append(line)
        return line

    def _tokenize(self) -> Iterator[Token]:
        hold_number = None

        try:
            for t in tokenize.generate_tokens(self._readline):
                if t.type == tokenize.ENDMARKER:
                    continue

                start_lineno, start_colno = t.start
                end_lineno, end_colno = t.end

                result = Token(
                    t.type,
                    t.string,
                    self.filename,
                    start_lineno,
                    start_colno,
                    end_lineno,
                    end_colno,
                    (self.linenumber, self.col_offset),
                )

                if hold_number is None and t.type == tokenize.NUMBER:
                    hold_number = result
                    continue

                # If we have '0' on hold check if we can collapse it
                # with next token.
                if hold_number is not None:
                    # Tokens are not next to each other, yield both.
                    if (
                        hold_number.end_col_offset != result.col_offset or
                        hold_number.end_lineno != result.lineno
                    ):
                        yield hold_number
                        hold_number = None

                    # Python 2 style octal numbers are still valid in Ren'Py.
                    # Tokenize report this as two numbers next to each other.
                    # This is no longer needed in Python 3.12+
                    elif t.type == tokenize.NUMBER:
                        hold_number.string += result.string
                        hold_number.end_lineno = result.end_lineno
                        hold_number.end_col_offset = result.end_col_offset

                        # We don't yield it yet, because '01attr' is 3 Python tokens.
                        continue

                    # 0-prefixed names are valid in Ren'Py (e.g. image attributes).
                    # NUMBER "$1" and NAME "$2" should appear as NAME "$1$2"
                    elif t.type == tokenize.NAME:
                        result.string = f"{hold_number.string}{result.string}"
                        result.lineno = hold_number.lineno
                        result.col_offset = hold_number.col_offset
                        hold_number = None

                    # Otherwise we yield a hold number and the result.
                    else:
                        yield hold_number
                        hold_number = None

                yield result

        except IndentationError as err:
            line, column = err.args[1][1:3]
            line += self.linenumber
            column += self.col_offset
            if not self.no_errors:
                raise SyntaxError(f"Indentation error in {self.filename}:{line}:{column}") from None

        except tokenize.TokenError as err:
            line, column = err.args[1]
            line += self.linenumber
            column += self.col_offset
            if not self.no_errors:
                raise SyntaxError(f"{err.args[0]} at {self.filename}:{line}:{column}") from None

    def _yield_tokens(self) -> Iterator[Token]:
        if self._tokenized:
            yield from self._tokens
            return

        if self._tokenized is not None:
            raise RuntimeError("_yield_tokens() called twice.")

        self._tokenized = False

        def unmatched_paren():
            if not self.no_errors:
                lineno = token.lineno + token.physical_offset[0]
                col_offset = token.col_offset + token.physical_offset[1]
                raise SyntaxError(f"unmatched '{token.string}' at {self.filename}:{lineno}:{col_offset}")

        def wrong_paren():
            if not self.no_errors:
                lineno = token.lineno + token.physical_offset[0]
                col_offset = token.col_offset + token.physical_offset[1]
                raise SyntaxError(f"closing parenthesis '{token.string}' "
                                  f"does not match opening parenthesis '{parens[-1]}'"
                                  f" at {self.filename}:{lineno}:{col_offset}")

        parens: list[str] = []
        LPAR = "("
        LBRACE = "{"
        LSQB = "["
        for token in self._tokenize():
            # Intern all names, so we have only a single instance
            # of often overlapping names.
            if token.kind is TokenKind.NAME:
                token.string = sys.intern(token.string)

            elif token.exact_kind is TokenKind.LPAR:
                parens.append(LPAR)
            elif token.exact_kind is TokenKind.RPAR:
                if not parens:
                    unmatched_paren()
                elif parens[-1] is not LPAR:
                    wrong_paren()
                else:
                    parens.pop()

            elif token.exact_kind is TokenKind.LBRACE:
                parens.append(LBRACE)
            elif token.exact_kind is TokenKind.RBRACE:
                if not parens:
                    unmatched_paren()
                elif parens[-1] is not LBRACE:
                    wrong_paren()
                else:
                    parens.pop()

            elif token.exact_kind is TokenKind.LSQB:
                parens.append(LSQB)
            elif token.exact_kind is TokenKind.RSQB:
                if not parens:
                    unmatched_paren()
                elif parens[-1] is not LSQB:
                    wrong_paren()
                else:
                    parens.pop()

            self._tokens.append(token)
            yield token

        # self._tokenize will raise SyntaxError for unclosed paren or string literal.
        self._tokenized = True

    def list_physical_lines(self) -> list[str]:
        """
        Return a list of physical lines of tokenized code, such that
        `"".join(physical lines)` is the lines that tokenizer sees.
        """

        rv = [*self._physical_lines, *self._next_lines_buffer]
        while True:
            try:
                line = next(self._next_lines)
                self._next_lines_buffer.append(line)
                rv.append(line)
            except StopIteration:
                return rv

    def list_logical_lines(self) -> list[Line]:
        """
        Return a list of logical lines of tokenized code.
        """

        rv: list[Line] = []

        depth = 0
        tokens: list[Token] = []

        for token in self._yield_tokens():
            # Empty lines and bare comments are not logical lines.
            if (token.kind is TokenKind.NL or token.kind is TokenKind.COMMENT) and not tokens:
                continue

            if token.kind is TokenKind.INDENT:
                depth += 1
            elif token.kind is TokenKind.DEDENT:
                depth -= 1
            else:
                tokens.append(token)

            if token.kind is TokenKind.NEWLINE:
                rv.append(Line(*tokens, indent_depth=depth))
                tokens.clear()

        return rv

    def list_tokens(self) -> list[Token]:
        return list(self._yield_tokens())
