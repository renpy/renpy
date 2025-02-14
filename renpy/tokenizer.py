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


from typing import Iterator, NamedTuple, Literal

import os
import io
import re
import sys
import keyword
import unicodedata
import contextlib
import renpy


def from_string(code: str, filename: str, *, lineno_offset=0, col_offset=0, no_errors=False) -> "Tokenizer":
    lines = io.StringIO(code, newline=None)
    return Tokenizer(
        filename, lines,
        lineno_offset=lineno_offset,
        col_offset=col_offset,
        no_errors=no_errors)


def from_file(filename: str, *, no_errors=False) -> "Tokenizer":
    if os.path.isabs(filename):
        fn = filename
    else:
        fn = renpy.lexer.unelide_filename(filename)

    if not os.path.exists(fn):
        raise FileNotFoundError(fn)

    def lines():
        with open(
            fn,
            encoding="utf-8",
            errors="python_strict",
            newline=None
        ) as f:
            yield from f

    return Tokenizer(filename, lines(), no_errors=no_errors)


class ParseError(SyntaxError):
    """
    Special exception type for syntax errors in Ren'Py.
    This exception includes syntax errors of Python code, converted to
    appropriate report style, and Ren'Py own syntax errors in user script.
    """

    _message: str | None = None

    def __init__(
        self,
        message: str,
        filename: str,
        lineno: int,
        offset: int | None = None,
        text: str | None = None,
        end_lineno: int | None = None,
        end_offset: int | None = None,
    ):
        super().__init__(message, (filename, lineno, offset, text, end_lineno, end_offset))

    @property
    def message(self) -> str:
        """
        Fully formatted message of the error, close to the result of `traceback.print_exception_only`.
        """

        if self._message is not None:
            return self._message

        message = f'File "{self.filename}", line {self.lineno}: {self.msg}'
        if self.text is not None:
            # Neither Python nor this class does not support multiline syntax error code.
            # Just strip the first line of provided code.
            text = self.text.split("\n")[0]

            # Remove ending escape chars, so we can render it.
            text = text.rstrip()

            # And also replace any escape chars at the start with an indent.
            ltext = text.lstrip()
            message += f'\n    {ltext}'

            if self.offset is not None:
                offset = self.offset

                # Fallback to single caret for cases end_offset is before offset.
                if self.end_offset is None or self.end_offset <= offset:
                    end_offset = offset + 1
                else:
                    end_offset = self.end_offset

                left_spaces = len(text) - len(ltext)
                offset -= left_spaces
                end_offset -= left_spaces

                if offset >= 0:
                    caret_space = ' ' * offset
                    carets = '^' * (end_offset - offset)
                    message += f"\n    {caret_space}{carets}"

        for note in getattr(self, "__notes__", ()):
            message += f"\n{note}"

        self._message = message
        return self._message

    def defer(self, queue):
        renpy.parser.deferred_parse_errors[queue].append(self.message)


type TokenKind = Literal[
    "indent",
    "dedent",
    "comment",
    "nl",
    "newline",
    "name",
    "number",
    "string",
    "op",
]
"""
Possible values for Token.kind.
"""

type TokenExactKindName = Literal[
    "keyword",
    "identifier",
    "non_identifier",
]
"""
Possible exact token kinds for tokens with 'name' kind.
"""

type TokenExactKindNumber = Literal[
    "hex",
    "binary",
    "octal",
    "imaginary",
    "float",
    "int",
]
"""
Possible exact token kinds for tokens with 'number' kind.
"""

type TokenExactKindString = Literal[
    "bytes",
    "f_string",
    "raw_triple_string",
    "triple_string",
    "raw_single_string",
    "single_string",
]
"""
Possible exact token kinds for tokens with 'string' kind.
"""

type TokenExactKindOp = Literal[
    "dollar",
    "spaceship",
    "lpar",
    "rpar",
    "lsqb",
    "rsqb",
    "colon",
    "comma",
    "semi",
    "plus",
    "minus",
    "star",
    "slash",
    "vbar",
    "amper",
    "less",
    "greater",
    "equal",
    "dot",
    "percent",
    "lbrace",
    "rbrace",
    "eqequal",
    "notequal",
    "lessequal",
    "greaterequal",
    "tilde",
    "circumflex",
    "leftshift",
    "rightshift",
    "doublestar",
    "plusequal",
    "minequal",
    "starequal",
    "slashequal",
    "percentequal",
    "amperequal",
    "vbarequal",
    "circumflexequal",
    "leftshiftequal",
    "rightshiftequal",
    "doublestarequal",
    "doubleslash",
    "doubleslashequal",
    "at",
    "atequal",
    "rarrow",
    "ellipsis",
    "colonequal",
]
"""
Possible exact token kinds for tokens with 'op' kind.
"""

type TokenExactKind = Literal[
    "indent", "dedent", "comment", "nl", "newline",
    TokenExactKindName,
    TokenExactKindNumber,
    TokenExactKindString,
    TokenExactKindOp,
]
"""
Possible values for Token.exact_kind.
"""

type TokenStringOp = Literal[
    "$",
    "<>",
    "(",
    ")",
    "[",
    "]",
    ":",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "|",
    "&",
    "<",
    ">",
    "=",
    ".",
    "%",
    "{",
    "}",
    "==",
    "!=",
    "<=",
    ">=",
    "~",
    "^",
    "<<",
    ">>",
    "**",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "&=",
    "|=",
    "^=",
    "<<=",
    ">>=",
    "**=",
    "//",
    "//=",
    "@",
    "@=",
    "->",
    "...",
    ":=",
]
"""
Possible string values for tokens with 'op' kind.
"""

TOKEN_OP_TO_VALUE: dict[TokenExactKindOp, TokenStringOp] = {
    "dollar": "$",
    "spaceship": "<>",
    "lpar": "(",
    "rpar": ")",
    "lsqb": "[",
    "rsqb": "]",
    "colon": ":",
    "comma": ",",
    "semi": ";",
    "plus": "+",
    "minus": "-",
    "star": "*",
    "slash": "/",
    "vbar": "|",
    "amper": "&",
    "less": "<",
    "greater": ">",
    "equal": "=",
    "dot": ".",
    "percent": "%",
    "lbrace": "{",
    "rbrace": "}",
    "eqequal": "==",
    "notequal": "!=",
    "lessequal": "<=",
    "greaterequal": ">=",
    "tilde": "~",
    "circumflex": "^",
    "leftshift": "<<",
    "rightshift": ">>",
    "doublestar": "**",
    "plusequal": "+=",
    "minequal": "-=",
    "starequal": "*=",
    "slashequal": "/=",
    "percentequal": "%=",
    "amperequal": "&=",
    "vbarequal": "|=",
    "circumflexequal": "^=",
    "leftshiftequal": "<<=",
    "rightshiftequal": ">>=",
    "doublestarequal": "**=",
    "doubleslash": "//",
    "doubleslashequal": "//=",
    "at": "@",
    "atequal": "@=",
    "rarrow": "->",
    "ellipsis": "...",
    "colonequal": ":=",
}

TOKEN_VALUE_TO_OP: dict[str, TokenExactKindOp] = \
    {v: k for k, v in TOKEN_OP_TO_VALUE.items()}


class PhysicalLocation(NamedTuple):
    """
    Represents a physical location in a file.
    `filename` is elided string of source filename.
    Column offset are 0-indexed and valid for source
    code that has newlines translated to '\n'.
    """

    filename: str
    start_lineno: int
    start_col_offset: int
    end_lineno: int
    end_col_offset: int


class Token(NamedTuple):
    """
    Represents a token in a logical line.
    """

    kind: TokenKind
    """
    Kind of the token, such as 'name', 'op' or 'number'.
    Is the same as a corresponding lower-cased string.
    """

    exact_kind: TokenExactKind
    """
    Exact kind of the token, such as 'keyword', 'dollar' or 'int'.
    Is the same as a corresponding lower-cased string.
    """

    string: str
    """
    String value of the token.
    """

    physical_location: PhysicalLocation
    """
    Physical location of the token.
    """

    def __reduce__(self):
        raise Exception("Can't pickle Token instance.")

    def __repr__(self):
        string = repr(self.string)
        if len(string) > 30:
            string = string[:15] + "..." + string[-15:]

        location = "{} {}:{}-{}:{}".format(*self.physical_location)
        return f"<Token {self.exact_kind!r} {string} in {location}>"


class Line(str):
    """
    Represents a logical line in a file, a string, without indentation
    and comments, and tokens that make up this line.
    Line indentation is stored in the indent_depth field.
    """

    __slots__ = [
        'tokens',
        'offsets',
        'physical_location',
        'indent_size',
    ]

    tokens: tuple[Token, ...]
    """
    Tuple of tokens that make up this line.
    """

    offsets: tuple[int, ...]
    """
    Tuple of offsets of tokens in line.
    """

    physical_location: PhysicalLocation
    """
    Physical location of the line in the file.
    """

    indent_size: int
    """
    Indentation of this line.
    Amount of spaces before the first token.
    """

    def __new__(
        cls,
        text: str,
        tokens: tuple[Token, ...],
        offsets: tuple[int, ...],
        physical_location: PhysicalLocation,
        indent_depth: int,
    ):
        self = str.__new__(cls, text)

        self.tokens = tuple(tokens)
        self.offsets = tuple(offsets)
        self.physical_location = physical_location
        self.indent_size = indent_depth
        return self

    def __reduce__(self):
        raise Exception("Can't pickle Line instance.")

    def __repr__(self):
        location = "{} {}:{}-{}:{}".format(*self.physical_location)
        rv = [f"Line {location}:"]
        for token in self.tokens:
            rv.append(f"    {token.exact_kind} {token.string!r}")

        return "\n".join(rv)


class Tokenizer:
    """
    This class is used to read files and strings as RenPy source code and yield
    physical lines, logical lines or tokens.

    First, this class reads passed buffer one line at a time, and performs
    this normalizations:
        1. Strips the BOM from the start of the file.
        2. Converts _ren.py file to equivalent .rpy file.
        3. Normalizes line endings to \n.
        4. Ensures that file ends with a newline.

    Then, it tokenizes read lines, performing these syntax checks:
        1. Disallows \t as indentation character.
        2. Checks for unbalanced parenthesis.
        3. Checks for wrong order of closing parenthesis.
        4. Most (but not all) syntax restrictions of Python.

    After file is tokenized, it can be used to list logical lines, which are
    string of seen source code without indentation and comments, and tokens
    that make up this line (except INDENT, DEDENT, NL and COMMENT tokens).
    """

    @staticmethod
    def _readline(lines: Iterator[str]) -> Iterator[str]:
        # Strip BOM.
        a = next(lines)
        if a.startswith('\ufeff'):
            a = a[1:]

        # \r\n normalization is done by StringIO or TextIOWrapper.

        # Make sure there is a newline at the end.
        while True:
            try:
                b = next(lines)
                yield a
                a = b
            except StopIteration:
                break

        if not a.endswith("\n"):
            a += "\n"

        yield a

    def _ren_py_to_rpy(self, filename: str, lines: Iterator[str]) -> Iterator[str]:
        """
        Takes an iterator of lines from a _ren.py file, and returns an iterator
        of lines of equivalent .rpy file. This should retain line numbers.
        """

        # The prefix prepended to Python lines.
        prefix = ""

        # Col offset of non-prefixed lines.
        col_offset = self.col_offset

        current_offset = 0

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
                    self.pos_offset = 0
                    yield "\n"
                    continue

            if state == RENPY:
                if l.strip() == '"""':
                    state = PYTHON
                    yield "\n"

                    # All python lines are virtually dedented, so result Python
                    # code has correct column offsets.
                    current_offset = len(prefix)
                    self.col_offset -= current_offset
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

                yield l
                continue

            if state == PYTHON:
                if l == "\n":
                    yield l
                else:
                    # Each line adds len(prefix) offset to position.
                    self.pos_offset -= current_offset
                    yield f"{prefix}{l}"
                continue

            if state == IGNORE:
                yield "\n"
                continue

        if self.no_errors:
            return

        if state == IGNORE:
            raise ParseError(f'There are no \'"""renpy\' blocks, so every line is ignored.',
                             filename, open_linenumber)

        if state == RENPY:
            raise ParseError(f'\'"""renpy\' block was not terminated by """.',
                              filename, open_linenumber)

    def __init__(
        self,
        filename: str,
        lines: Iterator[str], *,
        lineno_offset=0,
        col_offset=0,
        no_errors=False,
    ):
        self.filename: str = renpy.lexer.elide_filename(filename)

        # This can be used to influence physical location of tokenized lines
        # e.g. _ren.py python code can be less indented than corresponding
        # renpy code, or if we tokenize part of file, we can set physical
        # line number so it matches physical line number instead of bunch
        # of empty lines at the beginning.
        self.lineno_offset: int = lineno_offset
        self.col_offset: int = col_offset
        self.pos_offset: int = 0

        self.no_errors: bool = no_errors

        self._physical_lines = lines = self._readline(lines)

        if filename.endswith("_ren.py"):
            lines = self._ren_py_to_rpy(filename, lines)

        # Actual tokenizer.
        self._tokenizer = _Tokenizer(lines, self.filename)

        # True if tokenizer was called, so calling it again
        # will broke the iteration.
        self._exhausted = False

    # Public interface
    def physical_lines(self) -> Iterator[str]:
        """
        Return iterator of normalized physical lines of the file, so that
        tokens physicall locations for that iterator are correct.
        """
        if self._exhausted:
            raise Exception("Tokenizer is exhausted.")

        self._exhausted = True

        for line in self._physical_lines:
            yield line

    @contextlib.contextmanager
    def _no_errors(self):
        try:
            yield

        except ParseError as e:
            if self.no_errors:
                return

            if e.lineno is not None:
                e.lineno += self.lineno_offset

            if e.offset is not None:
                e.offset += self.col_offset

            if e.end_lineno is not None:
                e.end_lineno += self.lineno_offset

            if e.end_offset is not None:
                e.end_offset += self.col_offset

            raise

    def tokens(self) -> Iterator[Token]:
        """
        Return an iterator of Token objects for the tokenized code.
        """

        if self._exhausted:
            raise Exception("Tokenizer is exhausted.")

        self._exhausted = True

        filename = self.filename
        lineno = self.lineno_offset
        tok = self._tokenizer

        with self._no_errors():
            for (
                kind,
                exact_kind,
                string,
            ) in tok:
                location = PhysicalLocation(
                    filename,
                    tok.start_lineno + lineno,
                    tok.start_col_offset + self.col_offset,
                    tok.lineno + lineno,
                    tok.col_offset + self.col_offset,
                )

                yield Token(
                    kind,
                    exact_kind,
                    string,
                    location)

    def logical_lines(self) -> Iterator[Line]:
        """
        Return an iterator of logical line Line objects for the tokenized code.
        """

        if self._exhausted:
            raise Exception("Tokenizer is exhausted.")

        tokens: list[Token] = []
        positions: list[int] = []
        strip_from_to: list[tuple[int, int]] = []
        filename = self.filename
        tok = self._tokenizer
        start_location = None
        line_indent = 0
        position_bias = 0

        iter_tokens = iter(self.tokens())
        for token in iter_tokens:
            # Skip comments-only and empty lines.
            if not tokens:
                while True:
                    if token.kind == "comment":
                        token = next(iter_tokens)

                    if token.kind == "nl":
                        # It may be last token.
                        try:
                            token = next(iter_tokens)
                        except StopIteration:
                            return
                    else:
                        break

            # Compute location of where line starts.
            if start_location is None or token.kind == "indent":
                start_location = (
                    token.physical_location.start_lineno,
                    token.physical_location.start_col_offset,
                )
                line_indent = tok.indents[-1]

            # Remember positions of comments to strip them later.
            if token.kind == "comment":
                strip_from_to.append((tok.start, tok.pos))
                position_bias += tok.pos - tok.start
                continue

            elif token.kind in ("indent", "dedent", "nl"):
                continue

            tokens.append(token)
            positions.append(tok.start - line_indent - position_bias)

            if token.kind == "newline":
                if strip_from_to:
                    last_pos = line_indent
                    line = tok.line
                    parts = []
                    for start, end in strip_from_to:
                        parts.append(line[last_pos:start])
                        last_pos = end
                    parts.append(line[last_pos:])
                    text = ''.join(parts)
                else:
                    text = tok.line[line_indent:]

                location = PhysicalLocation(
                    filename,
                    start_location[0],
                    start_location[1],
                    token.physical_location.end_lineno,
                    token.physical_location.end_col_offset,
                )

                yield Line(
                    text,
                    tuple(tokens),
                    tuple(positions),
                    location,
                    line_indent,
                )

                tokens.clear()
                positions.clear()
                strip_from_to.clear()
                start_location = None
                position_bias = 0


_BINARY_RE = re.compile(r'[bB](?:_?[01])+\b')
_OCTAL_RE = re.compile(r'[oO](?:_?[0-7])+\b')
_HEX_RE = re.compile(r'[xX](?:_?[0-9a-fA-F])+\b')
_FLOAT_IMAG_RE = re.compile(r'(?:_?[0-9])*(?:[eE][+-]?[0-9](?:_?[0-9])*)?[jJ]?\b')
_DIGITPART_RE = re.compile(r'(?:_?[0-9])*')
_ELLIPSIS_RE = re.compile(r'\.\.\.')
_vals = sorted(TOKEN_VALUE_TO_OP, reverse=True)
_vals = map(re.escape, _vals)
_OP_RE = re.compile(f"({"|".join(_vals)})")
del _vals


# Kind of CPython struct tok_state
class _Tokenizer:
    filename: str

    # Rest of input.
    next_lines: Iterator[str]

    # Current logical line.
    line: str

    # Length of current logical line.
    max = 0

    # Position of current char in logical line.
    pos = -1

    # Position of start of current token.
    start = 0

    # Line number at the beginning of a token.
    start_lineno = 0

    # The column offset at the beginning of a token.
    start_col_offset = 0

    # Current line number.
    lineno = 0

    # Current col offset.
    col_offset = -1

    # Stack of indentation levels.
    indents: list[int]

    _pending_dedents = 0

    # Stack of open parens info.
    _parens: list[tuple[Literal["lpar", "lbrace", "lsqb"], str, int, int]]

    # Are we at beginning of line?
    _atbol = False

    # Should we reset line when reading new line?
    _last_was_newline: bool = True

    # Were there any non-comment tokens on the line?
    _blankline = True

    def __init__(self, lines: Iterator[str], filename: str):
        self.next_lines = lines
        self.filename = filename

        self.indents = [0]
        self._parens = []

    @staticmethod
    def is_potential_identifier_start(c: str):
        return (
            c >= 'a' and c <= 'z' or
            c >= 'A' and c <= 'Z' or
            c == '_' or ord(c) >= 128
        )

    @staticmethod
    def is_potential_identifier_char(c: str):
        return (
            c >= 'a' and c <= 'z' or
            c >= 'A' and c <= 'Z' or
            c >= '0' and c <= '9' or
            c == '_' or ord(c) >= 128
        )

    def reset_line(self):
        self.line = ""
        self.max = 0
        self.pos = -1
        self.col_offset = -1

    def getc(self, offset=0) -> str:
        i = self.pos + offset
        if i >= self.max:
            return ""

        return self.line[i]

    def nextc(self) -> str:
        self.pos += 1

        if self.pos >= self.max:
            self.pos = self.max
            self.col_offset = -1
            self.lineno += 1

            try:
                line = next(self.next_lines)
            except StopIteration:
                line = ""

            self.line += line
            self.max += len(line)

        self.col_offset += 1

        c = self.getc()

        if c == '\t':
            raise ParseError("tab character is not allowed in Ren'Py scripts",
                             self.filename, self.lineno, None, self.line)

        return c

    def make_token(self, kind: TokenKind, exact_kind: TokenExactKind, intern: bool = False):
        string = self.line[self.start:self.pos]
        if intern:
            # Normalize unicode characters, so we can't have two
            # names that are different but render the same.
            string = unicodedata.normalize('NFC', string)

            # Intern all names, so we have only a single instance
            # of often overlapping names.
            string = sys.intern(string)

        return (kind, exact_kind, string)

    def match(self, pattern: re.Pattern[str]) -> re.Match[str] | None:
        m = pattern.match(self.line, self.pos)
        if m is not None:
            len = m.end() - self.pos
            self.pos += len
            self.col_offset += len

        return m

    def line_continuation(self, c):
        # If it's not a line continuation, return False.
        # Otherwise read spaces and line continuations until we find a nonspace.
        if c != '\\':
            return False

        while True:
            c = self.nextc()
            # Something like 'text \a'
            if c != '\n':
                break

            c = self.nextc()
            while c == ' ':
                c = self.nextc()

            if c == '\\':
                continue

            if c in '#\n':
                break

            return True

        raise ParseError("unexpected character after line continuation character",
                                self.filename, self.lineno, self.col_offset, self.line)

    def float_or_imaginary(self):
        m = self.match(_FLOAT_IMAG_RE)
        if m is None:
            return None

        # Empty match.
        if m.start() == m.end():
            return None

        c = self.getc(-1)
        if c in 'jJ':
            return self.make_token("number", "imaginary")
        else:
            return self.make_token("number", "float")

    def f_string_expression(self):
        # Called after first '{' of an f-string.
        # Read until the matching '}' is found.

        c = self.nextc()

        # {{ is an escaped opening brace.
        if c == "{":
            return

        open_lineno = self.lineno
        open_col_offset = self.col_offset
        open_quote = None
        brace_depth = 1
        while True:
            if c == "":
                raise ParseError("'{' was never closed", self.filename,
                                 open_lineno, open_col_offset, self.line)

            if c in "'\"`":
                if open_quote == c:
                    open_quote = None
                else:
                    open_quote = c

            elif open_quote is None:
                if c == "{":
                    brace_depth += 1

                elif c == "}":
                    brace_depth -= 1
                    if not brace_depth:
                        return

            c = self.nextc()


    def string_token(self, quote: str):
        # Called at first quote of a string, after mods.
        mods = self.line[self.start:self.pos].lower()
        if "b" in mods:
            exact_kind = "bytes"
        elif "f" in mods:
            exact_kind = "f_string"
        elif "r" in mods:
            exact_kind = "raw_single_string"
        else:
            exact_kind = "single_string"

        f_string = exact_kind == "f_string"

        # Compute quote size.
        quote_size = 1
        if self.nextc() == quote:
            if self.nextc() == quote:
                quote_size = 3
                if exact_kind == "single_string":
                    exact_kind  = "triple_string"
                elif exact_kind == "raw_single_string":
                    exact_kind = "raw_triple_string"
            else:
                # Empty string.
                return self.make_token("string", exact_kind)

        end_quote_size = 0
        c = self.getc()
        while end_quote_size != quote_size:
            if c == "":
                # TODO: I need something clever to tell which quote was faulty.
                if quote_size == 3:
                    raise ParseError(
                        "unterminated triple-quoted string literal"
                        f" (detected at line {self.lineno})", self.filename,
                        self.start_lineno, self.start_col_offset, self.line)
                else:
                    raise ParseError(
                        "unterminated string literal"
                        f" (detected at line {self.lineno})", self.filename,
                        self.start_lineno, self.start_col_offset, self.line)

            while c == '\\':
                end_quote_size = 0
                self.nextc()  # skip escaped char
                c = self.nextc()

            if c == quote:
                end_quote_size += 1
            else:
                end_quote_size = 0

            if f_string and c == "{":
                self.f_string_expression()

            c = self.nextc()

        return self.make_token("string", exact_kind)

    def next_token(self, c: str):
        # Starting at non-space char c - return a token info of the next token.
        # State can't be left mid-token, and after return next line should not
        # be consumed. EOF here always is a ParseError.

        self.start = self.pos
        self.start_lineno = self.lineno
        self.start_col_offset = self.col_offset

        # Identifier (most frequent token!)
        if self.is_potential_identifier_start(c):
            # But maybe it is a prefixed string?
            saw_f = False
            saw_b = False
            saw_u = False
            saw_r = False
            while True:
                if not (saw_b or saw_u or saw_f) and c in 'bB':
                    saw_b = True
                # Since this is a backwards compatibility support literal we don't
                # want to support it in arbitrary order like byte literals.
                elif not (saw_b or saw_u or saw_r or saw_f) and c in 'uU':
                    saw_u = True
                # ur"" and ru"" are not supported
                elif not (saw_r or saw_u) and c in 'rR':
                    saw_r = True
                elif not (saw_f or saw_b or saw_u) and c in 'fF':
                    saw_f = True
                else:
                    break  # invalid prefix, so it is a name.
                c = self.nextc()
                if c in "'\"`":
                    return self.string_token(c)

            while self.is_potential_identifier_char(c):
                c = self.nextc()

            kind, exact_kind, name = \
                self.make_token("name", "non_identifier", True)

            if keyword.iskeyword(name):
                exact_kind = "keyword"
            elif name.isidentifier():
                exact_kind = "identifier"

            return (kind, exact_kind, name)

        # Comment
        if c == '#':
            # Everything on current line except the newline.
            self.pos = self.max - 1
            self.col_offset += (self.pos - self.start)
            return self.make_token("comment", "comment")

        # Newline
        if c == '\n':
            if self._blankline or self._parens:
                kind = "nl"
            else:
                kind = "newline"

            self.pos += 1
            self.col_offset += 1
            return self.make_token(kind, kind)

        if self.match(_ELLIPSIS_RE):
            return self.make_token("op", "ellipsis", True)

        # Period or number starting with period?
        if c == '.':
            self.nextc()
            # Fraction can only start with a digit.
            if self.getc().isdecimal():
                if (rv := self.float_or_imaginary()) is not None:
                    return rv

            # Otherwise it's a DOT followed by something else.
            return self.make_token("op", "dot", True)

        # Hex, octal or binary?
        if c == "0":
            # If any of that matches, it can't be any other kind of number.
            if self.match(_BINARY_RE):
                exact_kind = "binary"
            elif self.match(_OCTAL_RE):
                exact_kind = "octal"
            elif self.match(_HEX_RE):
                exact_kind = "hex"
            else:
                exact_kind = None

            if exact_kind is not None:
                return self.make_token("number", exact_kind)

        # Other number?
        if c.isdecimal():
            # Consume as many digits and underscores as possible.
            self.match(_DIGITPART_RE)
            c = self.getc()

            # It may be float or imaginary like 1.e+3j
            if c == '.':
                self.nextc()
                if (rv := self.float_or_imaginary()) is not None:
                    return rv

                # Rollback the dot.
                self.pos -= 1
                self.col_offset -= 1
                return self.make_token("number", "int")

            # Still can be a float or imaginary like 1e+3j
            if c in 'eE':
                if (rv := self.float_or_imaginary()) is not None:
                    return rv

            # If there is a word border, it is an int.
            if not self.is_potential_identifier_char(c):
                return self.make_token("number", "int")

            # Otherwise it is some kind of NON_IDENTIFIER.
            while self.is_potential_identifier_char(c):
                c = self.nextc()

            return self.make_token("name", "non_identifier", True)

        # String?
        if c in "'\"`":
            return self.string_token(c)

        # Otherwise it should be some kind of OP
        if m := self.match(_OP_RE):
            exact_kind = TOKEN_VALUE_TO_OP[m.group(0)]
            return self.make_token("op", exact_kind, True)

        else:
            raise Exception(f"unknown character {c!r} in {self.filename} at {self.lineno}:{self.col_offset}")

    def __iter__(self):
        return self

    def __next__(self) -> tuple[TokenKind, TokenExactKind, str]:
        # This is Python implementation of some code of Python's C
        # tokenizer and pegen, mostly it is 'tok_get_normal_mode' from tokenizer.c

        # Return pending dedents.
        if self._pending_dedents:
            self._pending_dedents -= 1
            return self.make_token("dedent", "dedent")

        # Advance to next physical line, and probably start a new logical line.
        if self._last_was_newline:
            self._last_was_newline = False
            self._blankline = True

            if not self._parens:
                self._atbol = True
                self.reset_line()

            c = self.nextc()

        # Get current character.
        else:
            c = self.getc()

        # New line just started. Compute indentation size.
        if self._atbol:
            start = self.pos

            # Calculate indentation size.
            indent_size = 0
            while c == ' ':
                c = self.nextc()
                indent_size += 1

            # Indentation cannot be split over multiple physical lines
            # using backslashes. This means that if we found a backslash
            # preceded by whitespace, **the first one we find** determines
            # the level of indentation of whatever comes next.
            if self.line_continuation(c):
                c = self.getc()

            # We are not at beginning of line anymore.
            self._atbol = False

            # Indent/dedent for new logical line, but only if
            # it is not a blank, comment or parenthesed line.
            if not (self._parens or c in "#\n"):
                if self.col_offset > self.indents[-1]:
                    self.start = start
                    self.start_lineno = self.lineno
                    self.start_col_offset = 0

                    self.indents.append(self.col_offset)
                    return self.make_token("indent", "indent")

                elif self.col_offset < self.indents[-1]:
                    self.start = self.pos
                    self.start_lineno = self.lineno
                    self.start_col_offset = self.col_offset

                    pending = -1
                    while self.col_offset < self.indents[-1]:
                        self.indents.pop()
                        pending += 1

                    if self.col_offset != self.indents[-1]:
                        raise ParseError("unindent does not match any outer indentation level",
                                         self.filename, self.lineno, None,
                                         self.line)

                    self._pending_dedents = pending
                    return self.make_token("dedent", "dedent")

        # token on the same line, skip spaces
        else:
            while c == ' ':
                c = self.nextc()

            if self.line_continuation(c):
                c = self.getc()

        # EOF.
        if c == '':
            # Pop remaining indent levels.
            if len(self.indents) > 1:
                self.indents.pop()
                return self.make_token("dedent", "dedent")

            if self._parens:
                _, char, lineno, col_offset = self._parens.pop()
                self._parens.clear()
                raise ParseError(f"'{char}' was never closed", self.filename,
                                 lineno, col_offset, self.line)

            raise StopIteration

        try:
            kind, exact_kind, string = self.next_token(c)
        except StopIteration:
            # All kinds of tokens should handle their EOFs.
            raise Exception("Unhandled EOF in next_token")

        # Get next line when enter this function next time.
        # This is postponed so outer code can read correct self.line and offsets.
        if exact_kind in ("newline", "nl"):
            self._last_was_newline = True

        # If we have a non-comment token, it is not a blank line.
        elif exact_kind != "comment":
            self._blankline = False

        # Track open parens.
        if exact_kind in ("lpar", "lbrace", "lsqb"):
            self._parens.append((exact_kind, string, self.start_lineno, self.start_col_offset))

        elif exact_kind in ("rpar", "rbrace", "rsqb"):
            if not self._parens:
                raise ParseError(f"unmatched '{string}'", self.filename, self.lineno, self.col_offset - 1, self.line)

            open_kind, open, _, _ = self._parens.pop()

            if not (
                exact_kind == "rpar" and open_kind == "lpar" or
                exact_kind == "rbrace" and open_kind == "lbrace" or
                exact_kind == "rsqb" and open_kind == "lsqb"
            ):
                raise ParseError(f"closing parenthesis '{string}' does not match opening parenthesis '{open}'",
                                 self.filename, self.lineno, self.col_offset - 1, self.line)

        return (kind, exact_kind, string)
