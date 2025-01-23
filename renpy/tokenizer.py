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


from typing import Iterator, NamedTuple

import os
import io
import re
import sys
import keyword
import unicodedata
import contextlib
import renpy

# All possible Token.kind and Token.exact_kind values.
class TokenKind(str):
    def __new__(cls, value: str, /) -> "TokenKind":
        return sys.intern(value)  # type: ignore


# Special tokens.
INDENT = TokenKind("indent")
DEDENT = TokenKind("dedent")
COMMENT = TokenKind("comment")

# Non-terminating and terminating new lines.
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
IMAGINARY = TokenKind("imaginary")
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
SPACESHIP = TokenKind("spaceship")
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

TOKEN_OP_TO_VALUE = {
    DOLLAR: "$",
    SPACESHIP: "<>",
    LPAR: "(",
    RPAR: ")",
    LSQB: "[",
    RSQB: "]",
    COLON: ":",
    COMMA: ",",
    SEMI: ";",
    PLUS: "+",
    MINUS: "-",
    STAR: "*",
    SLASH: "/",
    VBAR: "|",
    AMPER: "&",
    LESS: "<",
    GREATER: ">",
    EQUAL: "=",
    DOT: ".",
    PERCENT: "%",
    LBRACE: "{",
    RBRACE: "}",
    EQEQUAL: "==",
    NOTEQUAL: "!=",
    LESSEQUAL: "<=",
    GREATEREQUAL: ">=",
    TILDE: "~",
    CIRCUMFLEX: "^",
    LEFTSHIFT: "<<",
    RIGHTSHIFT: ">>",
    DOUBLESTAR: "**",
    PLUSEQUAL: "+=",
    MINEQUAL: "-=",
    STAREQUAL: "*=",
    SLASHEQUAL: "/=",
    PERCENTEQUAL: "%=",
    AMPEREQUAL: "&=",
    VBAREQUAL: "|=",
    CIRCUMFLEXEQUAL: "^=",
    LEFTSHIFTEQUAL: "<<=",
    RIGHTSHIFTEQUAL: ">>=",
    DOUBLESTAREQUAL: "**=",
    DOUBLESLASH: "//",
    DOUBLESLASHEQUAL: "//=",
    AT: "@",
    ATEQUAL: "@=",
    RARROW: "->",
    ELLIPSIS: "...",
    COLONEQUAL: ":=",
}
TOKEN_VALUE_TO_OP = \
    {v: k for k, v in TOKEN_OP_TO_VALUE.items()}

class PhysicalLocation(NamedTuple):
    """
    Represents a physical location in a file.
    Column offset are 0-indexed and valid for source
    code that has newlines translated to '\n'.
    """
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
    Kind of the token, such as tokenizer.NAME, tokenizer.OP or tokenizer.NUMBER.
    Is the same as a corresponding lower-cased string.
    """

    exact_kind: TokenKind
    """
    Exact kind of the token, such as tokenizer.KEYWORD, tokenizer.DOLLAR or tokenizer.INT.
    Is the same as a corresponding lower-cased string.
    """

    string: str
    """
    String value of the token.
    """

    filename: str
    """
    Elided filename where token is located.
    """

    physical_location: PhysicalLocation
    """
    Physical location of the token in the file.
    """

    def __reduce__(self):
        raise Exception("Can't pickle Token instance.")

    def __repr__(self):
        string = repr(self.string)
        if len(string) > 30:
            string = string[:15] + "..." + string[-15:]

        location = " {}:{}-{}:{}".format(*self.physical_location)
        return f"<Token {self.exact_kind!r} {string} in {self.filename}{location}>"


class Line(str):
    """
    Represents a logical line in a file, a string, without indentation
    and comments, and tokens that make up this line.
    Line indentation is stored in the indent_depth field.
    """

    __slots__ = [
        'tokens',
        'offsets',
        'filename',
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

    filename: str
    """
    Elided filename where line is located.
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
        filename: str,
        physical_location: PhysicalLocation,
        indent_depth: int,
    ):
        self = str.__new__(cls, text)

        self.tokens = tuple(tokens)
        self.offsets = tuple(offsets)
        self.filename = filename
        self.physical_location = physical_location
        self.indent_size = indent_depth
        return self

    def __reduce__(self):
        raise Exception("Can't pickle Line instance.")

    def __repr__(self):
        location = "{}:{}-{}:{}".format(*self.physical_location)
        rv = [f"<Line {self.filename} {location}:"]
        for token in self.tokens:
            rv.append(f"    {token.exact_kind} {token.string!r}")

        rv.append(">")
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
            raise SyntaxError(f'In {filename!r}, there are no """renpy blocks, so every line is ignored.')

        if state == RENPY:
            raise SyntaxError(f'In {filename!r}, there is a """renpy block '
                              f'at line {open_linenumber} that is not terminated by """.')

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
        self._tokenizer = _Tokenizer(lines)

        # True if tokenizer was called, so calling it again
        # will broke the iteration.
        self._exhausted = False

    # Public interface
    @classmethod
    def from_string(
        cls,
        code: str,
        filename: str, *,
        lineno_offset=0,
        col_offset=0,
        no_errors=False,
    ):
        lines = io.StringIO(code, newline=None)
        return cls(
            filename, lines,
            lineno_offset=lineno_offset,
            col_offset=col_offset,
            no_errors=no_errors)

    @classmethod
    def from_file(
        cls,
        filename: str, *,
        no_errors=False,
    ):
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

        return cls(filename, lines(), no_errors=no_errors)

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
        except SyntaxError as e:
            if not self.no_errors:
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
                    tok.start_lineno + lineno,
                    tok.start_col_offset + self.col_offset,
                    tok.lineno + lineno,
                    tok.col_offset + self.col_offset,
                )

                yield Token(
                    kind,
                    exact_kind,
                    string,
                    filename,
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
                    if token.kind is COMMENT:
                        token = next(iter_tokens)

                    if token.kind is NL:
                        # It may be last token.
                        try:
                            token = next(iter_tokens)
                        except StopIteration:
                            return
                    else:
                        break

            # Compute location of where line starts.
            if start_location is None or token.kind is INDENT:
                start_location = (
                    token.physical_location.start_lineno,
                    token.physical_location.start_col_offset,
                )
                line_indent = tok.indents[-1]

            # Remember positions of comments to strip them later.
            if token.kind is COMMENT:
                strip_from_to.append((tok.start, tok.pos))
                position_bias += tok.pos - tok.start
                continue
            elif (
                token.kind is INDENT or
                token.kind is DEDENT or
                token.kind is NL
            ):
                continue

            tokens.append(token)
            positions.append(tok.start - line_indent - position_bias)

            if token.kind is NEWLINE:
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
                    start_location[0],
                    start_location[1],
                    token.physical_location.end_lineno,
                    token.physical_location.end_col_offset,
                )

                yield Line(
                    text,
                    tuple(tokens),
                    tuple(positions),
                    filename,
                    location,
                    line_indent,
                )

                tokens.clear()
                positions.clear()
                strip_from_to.clear()
                start_location = None
                position_bias = 0


BINARY_RE = re.compile(r'[bB](?:_?[01])+\b')
OCTAL_RE = re.compile(r'[oO](?:_?[0-7])+\b')
HEX_RE = re.compile(r'[xX](?:_?[0-9a-fA-F])+\b')
FLOAT_IMAG_RE = re.compile(r'(?:_?[0-9])*(?:[eE][+-]?[0-9](?:_?[0-9])*)?[jJ]?\b')
DIGITPART_RE = re.compile(r'(?:_?[0-9])*')
ELLIPSIS_RE = re.compile(r'\.\.\.')
_vals = sorted(TOKEN_VALUE_TO_OP, reverse=True)
_vals = map(re.escape, _vals)
OP_RE = re.compile(f"({"|".join(_vals)})")
del _vals


# Kind of CPython struct tok_state
class _Tokenizer:
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
    indents = [0]

    # Pending indents (if > 0) or dedents (if < 0)
    _pending = 0

    # Stack of open parens info.
    _parens: list[tuple[TokenKind, TokenKind, str]] = []

    # Are we at beginning of line?
    _atbol = False

    # Are we need to enter next line?
    # NEWLINE creates a new logical line.
    # NL creates new logical line iif parens are empty.
    _last_was_newline = NEWLINE

    # Were there any non-comment tokens on the line?
    _blankline = True

    def __init__(self, lines: Iterator[str]):
        self.next_lines = lines

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

            line = next(self.next_lines)
            self.line += line
            self.max += len(line)

        self.col_offset += 1

        c = self.line[self.pos]

        if c == '\t':
            raise SyntaxError("tab character is not allowed in Ren'Py scripts")

        return c

    def make_token(self, kind: TokenKind, exact_kind: TokenKind, intern: bool = False):
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
        if c == '\\':
            nextc = self.nextc()
            if nextc == '\n':
                return True
            else:
                raise SyntaxError("unexpected character after line continuation character")

        return False

    def float_or_imaginary(self):
        m = self.match(FLOAT_IMAG_RE)
        if m is None:
            return None

        # Empty match.
        if m.start() == m.end():
            return None

        c = self.getc(-1)
        if c == 'j' or c == 'J':
            return self.make_token(NUMBER, IMAGINARY)
        else:
            return self.make_token(NUMBER, FLOAT)

    def f_string_expression(self):
        # Called after first '{' of an f-string.
        # Read until the matching '}' is found.

        try:
            c = self.nextc()

            # {{ is an escaped opening brace.
            if c == "{":
                return

            open_quote = None
            brace_depth = 1
            while True:
                if c == "'" or c == '"':
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

        except StopIteration:
            raise SyntaxError("f-string: expecting '}'")

    def string_token(self, quote: str):
        # Called at first quote of a string, after mods.
        mods = self.line[self.start:self.pos].lower()
        if "b" in mods:
            exact_kind = BYTES
        elif "f" in mods:
            exact_kind = F_STRING
        elif "r" in mods:
            exact_kind = RAW_SINGLE_STRING
        else:
            exact_kind = SINGLE_STRING

        f_string = exact_kind is F_STRING

        # Compute quote size.
        quote_size = 1
        if self.nextc() == quote:
            if self.nextc() == quote:
                quote_size = 3
                if exact_kind is SINGLE_STRING:
                    exact_kind  = TRIPLE_STRING
                elif exact_kind is RAW_SINGLE_STRING:
                    exact_kind = RAW_TRIPLE_STRING
            else:
                # Empty string.
                return self.make_token(STRING, exact_kind)

        end_quote_size = 0
        try:
            c = self.getc()
            while end_quote_size != quote_size:
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

            return self.make_token(STRING, exact_kind)

        except StopIteration:
            # When we are in an f-string, before raising the
            # unterminated string literal error, check whether
            # does the initial quote matches with f-strings quotes
            # and if it is, then this must be a missing '}' token
            # so raise the proper error
            if quote_size == 3:
                raise SyntaxError(
                    "unterminated triple-quoted string literal"
                    f" (detected at line {self.start_lineno})")
            else:
                raise SyntaxError(
                    "unterminated string literal"
                    f" (detected at line {self.start_lineno})")

    def next_token(self, c: str):
        # Starting at non-space char c - return a token info of the next token.
        # State can't be left mid-token, and after return next line should not
        # be consumed. EOF here always is SyntaxError.

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
                if not (saw_b or saw_u or saw_f) and (c == 'b' or c == 'B'):
                    saw_b = True
                # Since this is a backwards compatibility support literal we don't
                # want to support it in arbitrary order like byte literals.
                elif not (saw_b or saw_u or saw_r or saw_f) and (c == 'u' or c == 'U'):
                    saw_u = True
                # ur"" and ru"" are not supported
                elif not (saw_r or saw_u) and (c == 'r' or c == 'R'):
                    saw_r = True
                elif not (saw_f or saw_b or saw_u) and (c == 'f' or c == 'F'):
                    saw_f = True
                else:
                    break  # invalid prefix, so it is a name.
                c = self.nextc()
                if c == '"' or c == "'" or c == "`":
                    return self.string_token(c)

            while self.is_potential_identifier_char(c):
                c = self.nextc()

            kind, _, name = \
                self.make_token(NAME, NAME, True)

            if keyword.iskeyword(name):
                exact_kind = KEYWORD
            elif name.isidentifier():
                exact_kind = IDENTIFIER
            else:
                exact_kind = NON_IDENTIFIER

            return (kind, exact_kind, name)

        # Comment
        if c == '#':
            # Everything on current line except the newline.
            self.pos = self.max - 1
            self.col_offset += (self.pos - self.start)
            return self.make_token(COMMENT, COMMENT)

        # Newline
        if c == '\n':
            if self._blankline or self._parens:
                kind = NL
            else:
                kind = NEWLINE

            self.pos += 1
            self.col_offset += 1
            return self.make_token(kind, kind)

        if self.match(ELLIPSIS_RE):
            return self.make_token(OP, ELLIPSIS, True)

        # Period or number starting with period?
        if c == '.':
            self.nextc()
            # Fraction can only start with a digit.
            if self.getc().isdecimal():
                if (rv := self.float_or_imaginary()) is not None:
                    return rv

            # Otherwise it's a DOT followed by something else.
            return self.make_token(OP, DOT, True)

        # Hex, octal or binary?
        if c == "0":
            # If any of that matches, it can't be any other kind of number.
            if self.match(BINARY_RE):
                exact_kind = BINARY
            elif self.match(OCTAL_RE):
                exact_kind = OCTAL
            elif self.match(HEX_RE):
                exact_kind = HEX
            else:
                exact_kind = None

            if exact_kind is not None:
                return self.make_token(NUMBER, exact_kind)

        # Other number?
        if c.isdecimal():
            # Consume as many digits and underscores as possible.
            self.match(DIGITPART_RE)
            c = self.getc()

            # It may be float or imaginary like 1.e+3j
            if c == '.':
                self.nextc()
                if (rv := self.float_or_imaginary()) is not None:
                    return rv

                # Rollback the dot.
                self.pos -= 1
                self.col_offset -= 1
                return self.make_token(NUMBER, INT)

            # Still can be a float or imaginary like 1e+3j
            if c == 'e' or c == 'E':
                if (rv := self.float_or_imaginary()) is not None:
                    return rv

            # If there is a word border, it is an int.
            if not self.is_potential_identifier_char(c):
                return self.make_token(NUMBER, INT)

            # Otherwise it is some kind of NON_IDENTIFIER.
            while self.is_potential_identifier_char(c):
                c = self.nextc()

            return self.make_token(NAME, NON_IDENTIFIER, True)

        # String?
        if c == '"' or c == "'" or c == "`":
            return self.string_token(c)

        # Otherwise it should be some kind of OP
        if m := self.match(OP_RE):
            exact_kind = TOKEN_VALUE_TO_OP[m.group()]
            return self.make_token(OP, exact_kind, True)

        else:
            raise SyntaxError(f"unknown character {c!r} at {self.lineno}:{self.col_offset}")

    def __iter__(self):
        return self

    def __next__(self) -> tuple[TokenKind, TokenKind, str]:
        # This is Python implementation of some code of Python's C
        # tokenizer and pegen, mostly it is 'tok_get_normal_mode' from tokenizer.c

        try:
            # Advance to next physical line, and probably
            # start a new logical line.
            if self._last_was_newline is None:
                c = self.getc()
                if c == '':
                    raise StopIteration

            elif self._last_was_newline is NEWLINE:
                self._last_was_newline = None
                self._blankline = True
                self.reset_line()
                self._atbol = True
                c = self.nextc()

            elif self._last_was_newline is NL:
                self._last_was_newline = None
                self._blankline = True
                if not self._parens:
                    self.reset_line()
                    self._atbol = True

                c = self.nextc()

            else:
                raise RuntimeError(self._last_was_newline)

            if self._atbol:
                # Compute indentation size.
                # Indentation cannot be split over multiple physical lines
                # using backslashes. This means that if we found a backslash
                # preceded by whitespace, **the first one we find** determines
                # the level of indentation of whatever comes next.
                line_continuation_indent = None
                while True:
                    # Values for INDENT/DEDENT tokens.
                    self.start = self.pos
                    self.start_lineno = self.lineno
                    self.start_col_offset = self.col_offset

                    # Calculate indentation size.
                    indent_size = 0
                    while c == ' ':
                        c = self.nextc()
                        indent_size += 1

                    if line_continuation_indent is not None:
                        indent_size = line_continuation_indent
                        line_continuation_indent = None

                    if self.line_continuation(c):
                        line_continuation_indent = indent_size
                        self.nextc()  # Enter next line.
                        continue

                    break

                # We are not at beginning of line anymore.
                self._atbol = False

                # Indent/dedent for new logical line, but only if
                # it is not a blank, comment or parenthesed line.
                if not (c == '#' or c == '\n') and not self._parens:
                    if self.col_offset > self.indents[-1]:
                        self.indents.append(self.col_offset)
                        self._pending += 1
                    else:
                        for val in reversed(self.indents):
                            if self.col_offset == val:
                                break
                            elif self.col_offset < val:
                                self._pending -= 1
                                self.indents.pop()
                            else:
                                raise SyntaxError("unindent does not match any outer indentation level")

            # token on the same line, skip spaces
            else:
                while True:
                    if c == ' ':
                        c = self.nextc()

                    elif self.line_continuation(c):
                        c = self.nextc()  # Enter next line.

                    else:
                        break

            # Return pending indents/dedents.
            if self._pending > 0:
                self._pending -= 1
                return self.make_token(INDENT, INDENT)
            elif self._pending < 0:
                self._pending += 1
                return self.make_token(DEDENT, DEDENT)

            try:
                rv = self.next_token(c)
            except StopIteration:
                raise SyntaxError(f"unexpected EOF while parsing")

            exact_kind = rv[1]

            # Get next line when enter this function next time.
            if exact_kind is NEWLINE or exact_kind is NL:
                self._last_was_newline = exact_kind

            # If we have a non-comment token, it is not a blank line.
            elif exact_kind is not COMMENT:
                self._blankline = False

            # Track open parens.
            if exact_kind is LPAR or exact_kind is LBRACE or exact_kind is LSQB:
                self._parens.append(rv)
            elif exact_kind is RPAR or exact_kind is RBRACE or exact_kind is RSQB:
                if not self._parens:
                    raise SyntaxError(f"unmatched '{rv[2]}'")

                _, open_kind, open, *_ = self._parens.pop()

                if exact_kind is RPAR and open_kind is LPAR:
                    pass
                elif exact_kind is RBRACE and open_kind is LBRACE:
                    pass
                elif exact_kind is RSQB and open_kind is LSQB:
                    pass
                else:
                    raise SyntaxError(
                        f"closing parenthesis '{rv[2]}' does not match "
                        f"opening parenthesis '{open}'")

            return rv

        except StopIteration:
            # Pop remaining indent levels.
            if len(self.indents) > 1:
                self.indents.pop()
                return self.make_token(DEDENT, DEDENT)

            if self._parens:
                (
                    _, _,
                    char,
                ) = self._parens[-1]
                self._parens.clear()
                raise SyntaxError(f"'{char}' was never closed")

            raise
