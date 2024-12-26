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

            if t.kind is INDENT or t.kind is DEDENT:
                raise ValueError("Line can't contain INDENT or DEDENT tokens.")

            if t.kind is NEWLINE:
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
                if t.kind is NL or t.kind is NEWLINE:
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


# All possible Token.kind and Token.exact_kind values.
class TokenKind(str):
    def __new__(cls, value: str, /) -> TokenKind:
        return sys.intern(value)  # type: ignore


# Special tokens.
INDENT = TokenKind("indent")
DEDENT = TokenKind("dedent")
COMMENT = TokenKind("comment")

# Non-terminating and terminating new lines.
# This is always \n in Ren'Py.
NL = TokenKind("nl")
NEWLINE = TokenKind("newline")

# Names.
NAME = TokenKind("name")  # Any name.
KEYWORD = TokenKind("keyword")
IDENTIFIER = TokenKind("identifier")
NON_IDENTIFIER = TokenKind("non_identifier")

# Numbers.
NUMBER = TokenKind("number")  # Any number.
HEX = TokenKind("hex")
BINARY = TokenKind("binary")
OCTAL = TokenKind("octal")
IMAG = TokenKind("imag")
FLOAT = TokenKind("float")
INT = TokenKind("int")

# Strings.
STRING = TokenKind("string")  # Any string.
BYTES = TokenKind("bytes")
F_STRING = TokenKind("f_string")
RAW_TRIPLE_STRING = TokenKind("raw_triple_string")
TRIPLE_STRING = TokenKind("triple_string")
RAW_SINGLE_STRING = TokenKind("raw_single_string")
SINGLE_STRING = TokenKind("single_string")

# Operators.
OP = TokenKind("op")  # Any operator.
DOLLAR = TokenKind("dollar")
LPAR = TokenKind("lpar")
RPAR = TokenKind("rpar")
LSQB = TokenKind("lsqb")
RSQB = TokenKind("rsqb")
COLON = TokenKind("colon")
COMMA = TokenKind("comma")
SEMI = TokenKind("semi")
PLUS = TokenKind("plus")
MINUS = TokenKind("minus")
STAR = TokenKind("star")
SLASH = TokenKind("slash")
VBAR = TokenKind("vbar")
AMPER = TokenKind("amper")
LESS = TokenKind("less")
GREATER = TokenKind("greater")
EQUAL = TokenKind("equal")
DOT = TokenKind("dot")
PERCENT = TokenKind("percent")
LBRACE = TokenKind("lbrace")
RBRACE = TokenKind("rbrace")
EQEQUAL = TokenKind("eqequal")
NOTEQUAL = TokenKind("notequal")
LESSEQUAL = TokenKind("lessequal")
GREATEREQUAL = TokenKind("greaterequal")
TILDE = TokenKind("tilde")
CIRCUMFLEX = TokenKind("circumflex")
LEFTSHIFT = TokenKind("leftshift")
RIGHTSHIFT = TokenKind("rightshift")
DOUBLESTAR = TokenKind("doublestar")
PLUSEQUAL = TokenKind("plusequal")
MINEQUAL = TokenKind("minequal")
STAREQUAL = TokenKind("starequal")
SLASHEQUAL = TokenKind("slashequal")
PERCENTEQUAL = TokenKind("percentequal")
AMPEREQUAL = TokenKind("amperequal")
VBAREQUAL = TokenKind("vbarequal")
CIRCUMFLEXEQUAL = TokenKind("circumflexequal")
LEFTSHIFTEQUAL = TokenKind("leftshiftequal")
RIGHTSHIFTEQUAL = TokenKind("rightshiftequal")
DOUBLESTAREQUAL = TokenKind("doublestarequal")
DOUBLESLASH = TokenKind("doubleslash")
DOUBLESLASHEQUAL = TokenKind("doubleslashequal")
AT = TokenKind("at")
ATEQUAL = TokenKind("atequal")
RARROW = TokenKind("rarrow")
ELLIPSIS = TokenKind("ellipsis")
COLONEQUAL = TokenKind("colonequal")


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
        if type == tokenize.ERRORTOKEN:
            raise SyntaxError(f"Error token with value: {string!r} on line "
                              f"{lineno + physical_offset[0]}")

        # Exact name is one of predefined.
        elif type == tokenize.OP:
            if string == "$":
                kind = OP
                exact_kind = DOLLAR
            else:
                kind = OP
                type = tokenize.EXACT_TOKEN_TYPES[string]
                exact_kind = TokenKind(tokenize.tok_name[type].lower())

        # f-strings and bytes are expressions in Ren'Py,
        # and raw strings are handled differently.
        elif type == tokenize.STRING:
            kind = STRING

            prefix = re.match(
                r'([urfbURFB])*("|\'|"""|\'\'\')', string)
            assert prefix is not None
            mods = prefix.group(1) or ""
            quotes = prefix.group(2)

            if "b" in mods or "B" in mods:
                exact_kind = BYTES
            elif "f" in mods or "F" in mods:
                exact_kind = F_STRING
            elif quotes == "'''" or quotes == '"""':
                if "r" in mods or "R" in mods:
                    exact_kind = RAW_TRIPLE_STRING
                else:
                    exact_kind = TRIPLE_STRING
            else:
                if "r" in mods or "R" in mods:
                    exact_kind = RAW_SINGLE_STRING
                else:
                    exact_kind = SINGLE_STRING

        # Split numbers into complex, float, and integer.
        elif type == tokenize.NUMBER:
            kind = NUMBER
            if string.startswith("0x"):
                exact_kind = HEX
            elif string.startswith("0b"):
                exact_kind = BINARY
            elif string.startswith("0o"):
                exact_kind = OCTAL
            elif string[-1] in "jJ":
                exact_kind = IMAG
            else:
                symbols = set(string)
                # Definitely a float.
                if "." in symbols:
                    exact_kind = FLOAT

                # 00e0 is a float and can be interpreted as hex,
                # but we assume this is a float.
                elif symbols.intersection("eE"):
                    exact_kind = FLOAT

                else:
                    exact_kind = INT

        # Names can be keywords or identifiers.
        # Otherwise it is a 0name, which is not an identifier,
        # but e.g. is a valid attribute name.
        elif type == tokenize.NAME:
            kind = NAME

            if keyword.iskeyword(string):
                exact_kind = KEYWORD
            elif string.isidentifier():
                exact_kind = IDENTIFIER
            else:
                exact_kind = NON_IDENTIFIER

            # Intern all names, so we have only a single instance
            # of often overlapping names.
            string = sys.intern(string)

        else:
            kind = exact_kind = TokenKind(tokenize.tok_name[type].lower())

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
        return f"<Token {self.exact_kind!r} {string} {self.filename} {location}>"


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
        parens: list[str] = []
        f_string_depth = 0
        f_string_parts: list[str] = []
        hold_number = None

        def unmatched_paren():
            if not self.no_errors:
                lineno = start_lineno + self.linenumber
                col_offset = start_colno + self.col_offset
                raise SyntaxError(f"unmatched '{string}' at {self.filename}:{lineno}:{col_offset}")

        def wrong_paren():
            if not self.no_errors:
                lineno = start_lineno + self.linenumber
                col_offset = start_colno + self.col_offset
                raise SyntaxError(f"closing parenthesis '{string}' "
                                  f"does not match opening parenthesis '{parens[-1]}'"
                                  f" at {self.filename}:{lineno}:{col_offset}")

        try:
            for (
                type,
                string,
                (start_lineno, start_colno),
                (end_lineno, end_colno),
                _,
            ) in tokenize.generate_tokens(self._readline):
                if type == tokenize.ENDMARKER:
                    continue

                # Tokenize doesn't report unmatched parens and bad order of
                # parens, but Python itself does, so we do too.
                elif string == "(":
                    parens.append("(")
                elif string == ")":
                    if not parens:
                        unmatched_paren()
                    elif parens[-1] != "(":
                        wrong_paren()
                    else:
                        parens.pop()

                elif string == "[":
                    parens.append("[")
                elif string == "]":
                    if not parens:
                        unmatched_paren()
                    elif parens[-1] != "[":
                        wrong_paren()
                    else:
                        parens.pop()

                elif string == "{":
                    parens.append("{")
                elif string == "}":
                    if not parens:
                        unmatched_paren()
                    elif parens[-1] != "{":
                        wrong_paren()
                    else:
                        parens.pop()

                # We care only about first depth. Inners is Python's realm.
                # We do not provide PEP 701 tokens, but if someone really wants
                # them, they can tokenize our token string again at parse time.
                elif type == tokenize.FSTRING_START:
                    f_string_depth += 1

                elif type == tokenize.FSTRING_END:
                    f_string_depth -= 1
                    if not f_string_depth:
                        type = tokenize.STRING
                        string = "".join(f_string_parts)
                        f_string_parts.clear()

                if f_string_depth:
                    f_string_parts.append(string)
                    continue

                if hold_number is None and type == tokenize.NUMBER:
                    hold_number = Token(
                        type,
                        string,
                        self.filename,
                        start_lineno,
                        start_colno,
                        end_lineno,
                        end_colno,
                        (self.linenumber, self.col_offset),
                    )
                    continue

                if hold_number is not None:
                    # Tokens are next to each other and next token is a NAME,
                    # which is a valid RenPy non-identifier (e.g. image attribute).
                    if (
                        type == tokenize.NAME and
                        hold_number.end_col_offset == start_colno and
                        hold_number.end_lineno == start_lineno
                    ):
                        string = f"{hold_number.string}{string}"
                        start_colno = hold_number.col_offset
                        hold_number = None

                    # Otherwise we yield a hold number and the result.
                    else:
                        yield hold_number
                        hold_number = None

                yield Token(
                    type,
                    string,
                    self.filename,
                    start_lineno,
                    start_colno,
                    end_lineno,
                    end_colno,
                    (self.linenumber, self.col_offset),
                )

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

        for token in self._tokenize():
            self._tokens.append(token)
            yield token

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
            if (token.kind is NL or token.kind is COMMENT) and not tokens:
                continue

            if token.kind is INDENT:
                depth += 1
            elif token.kind is DEDENT:
                depth -= 1
            else:
                tokens.append(token)

            if token.kind is NEWLINE:
                rv.append(Line(*tokens, indent_depth=depth))
                tokens.clear()

        return rv

    def list_tokens(self) -> list[Token]:
        return list(self._yield_tokens())
