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


from typing import Callable, Iterator, NamedTuple

import enum
import os
import io
import re
import sys
import os
import tokenize
import contextlib
import functools
import keyword

import renpy


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
        super().__init__(message, (
            unicode_filename(filename),
            lineno, offset,
            text,
            end_lineno, end_offset))

    @property
    def message(self) -> str:
        """
        Fully formatted message of the error close to the result of
        `traceback.print_exception_only`.
        """
        if self._message is None:
            message = f'File "{self.filename}", line {self.lineno}: {self.msg}'
            if self.text is not None:
                # Neither Python nor this class does not support multiline syntax error code.
                # Just strip the first line of provided code.
                text = self.text.split("\n")[0]

                # Remove ending escape chars, so we can render it.
                text = text.rstrip()

                # And also replace any escape chars at the start with an indent.
                message += f'\n    {text.lstrip()}'

                if self.offset is not None:
                    offset = self.offset

                    # Fallback to single caret for cases end_offset is before offset.
                    if self.end_offset is None or self.end_offset <= offset:
                        end_offset = offset + 1
                    else:
                        end_offset = self.end_offset

                    left_spaces = len(text) - len(text.lstrip())
                    offset -= left_spaces
                    end_offset -= left_spaces

                    if offset >= 1:
                        caret_space = ' ' * (offset - 1)
                        carets = '^' * (end_offset - offset)
                        message += f"\n    {caret_space}{carets}"

            for note in getattr(self, "__notes__", ()):
                message += f"\n{note}"

            self._message = message

        return self._message

    def defer(self, queue):
        renpy.parser.deferred_parse_errors[queue].append(self.message)


def unicode_filename(fn):
    """
    Converts the supplied filename to unicode.
    """

    if isinstance(fn, str):
        return fn

    # Windows.
    try:
        return fn.decode("mbcs")
    except Exception:
        pass

    # Mac and (sane) Unix
    try:
        return fn.decode("utf-8")
    except Exception:
        pass

    # Insane systems, mojibake.
    return fn.decode("latin-1")


def munge_filename(fn):
    # The prefix that's used when __ is found in the file.
    rv = os.path.basename(fn)

    if rv.endswith("_ren.py"):
        rv = rv[:-7]

    rv = os.path.splitext(rv)[0]
    rv = rv.replace(" ", "_")

    def munge_char(m):
        return hex(ord(m.group(0)))

    rv = re.sub(r'[^a-zA-Z0-9_]', munge_char, rv)

    return "_m1_" + rv + "__"


def elide_filename(fn):
    """
    Returns a version of fn that is either relative to the base directory,
    or relative to the Ren'Py directory.
    """

    fn = fn.replace("\\", "/")

    basedir = os.path.abspath(renpy.config.basedir).replace("\\", "/") + "/"
    renpy_base = os.path.abspath(renpy.config.renpy_base).replace("\\", "/") + "/"

    # This is SDK inside the project, for some reason, or it is the same path
    if renpy_base.startswith(basedir):
        dirs = [renpy_base, basedir]

    # This is a projects dir inside SDK or it's different paths
    else:
        dirs = [basedir, renpy_base]

    for d in dirs:
        if fn.startswith(d):
            rv = fn[len(d):]
            break
    else:
        rv = fn

    return rv


def unelide_filename(fn):
    fn = os.path.normpath(fn)

    if renpy.config.alternate_unelide_path is not None:
        fn0 = os.path.join(renpy.config.alternate_unelide_path, fn)
        if os.path.exists(fn0):
            return fn0

    fn1 = os.path.join(renpy.config.basedir, fn)
    if os.path.exists(fn1):
        return fn1

    fn2 = os.path.join(renpy.config.renpy_base, fn)
    if os.path.exists(fn2):
        return fn2

    return fn


def get_string_munger(prefix: str) -> Callable[[str], str]:
    if renpy.config.munge_in_strings:
        def munge_string(m: re.Match[str]):

            g1 = m.group(1)

            if "__" in g1:
                return m.group(0)

            if g1.startswith("_"):
                return m.group(0)

            return prefix + m.group(1)

        return functools.partial(re.sub, r'\b__(\w+)', munge_string)

    else:
        def munge_string(m: re.Match[str]):
            brackets = m.group(1)

            if len(brackets) % 2 == 0:
                return m.group(0)

            if "__" in m.group(2):
                return m.group(0)

            return brackets + prefix + m.group(2)

        return functools.partial(re.sub, r'(\.|\[+)__(\w+)', munge_string)


# The filename that the start and end positions are relative to.
original_filename = ""

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

            match t.kind:
                case TokenKind.INDENT | TokenKind.DEDENT:
                    raise ValueError("Line can't contain INDENT or DEDENT tokens.")

                case TokenKind.NEWLINE:
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
    Enum of all possible `Token.name` values.

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
    NAME = enum.auto()

    # Numbers.
    NUMBER = enum.auto()

    # Strings.
    STRING = enum.auto()

    # Operators.
    OP = enum.auto()


class TokenExactKind(enum.StrEnum):
    """
    Enum of all possible `Token.exact_name` values.

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
    NAME = enum.auto()
    KEYWORD = enum.auto()
    IDENTIFIER = enum.auto()

    # Numbers.
    HEX = enum.auto()
    BINARY = enum.auto()
    OCTAL = enum.auto()
    IMAG = enum.auto()
    FLOAT = enum.auto()
    INT = enum.auto()

    # Strings.
    STRING = enum.auto()
    BYTES = enum.auto()
    F_STRING = enum.auto()
    RAW_TRIPLE_STRING = enum.auto()
    TRIPLE_STRING = enum.auto()
    RAW_STRING = enum.auto()

    # Operators.
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
        'munged',
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
        match type:
            case tokenize.ERRORTOKEN if string == "$":  # FIXME: In 3.12 it is OP
                kind = TokenKind.OP
                exact_kind = TokenExactKind.DOLLAR
            case tokenize.ERRORTOKEN:
                raise SyntaxError(f"Error token with value: {string!r} on line "
                                  f"{lineno + physical_offset[0]}")

            # Exact name is one of predefined.
            case tokenize.OP:
                kind = TokenKind.OP
                type = tokenize.EXACT_TOKEN_TYPES[string]
                exact_kind = TokenExactKind(tokenize.tok_name[type].lower())

            # f-strings and bytes are expressions in Ren'Py,
            # and raw strings are handled differently.
            case tokenize.STRING:
                kind = TokenKind.STRING

                prefix = re.match(
                    r'([urfbURFB])*("""|\'\'\'|"|\')', string)
                assert prefix is not None
                mods = prefix.group(1) or ""
                quotes = prefix.group(2)

                if "b" in mods or "B" in mods:
                    exact_kind = TokenExactKind.BYTES
                elif "f" in mods or "F" in mods:
                    exact_kind = TokenExactKind.F_STRING
                elif "r" in mods or "R" in mods:
                    if quotes == "'''" or quotes == '"""':
                        exact_kind = TokenExactKind.RAW_TRIPLE_STRING
                    else:
                        exact_kind = TokenExactKind.RAW_STRING
                elif quotes == "'''" or quotes == '"""':
                    exact_kind = TokenExactKind.TRIPLE_STRING
                else:
                    exact_kind = TokenExactKind.STRING

            # Split numbers into complex, float, and integer.
            case tokenize.NUMBER:
                kind = TokenKind.NUMBER
                if string.startswith("0x"):
                    exact_kind = TokenExactKind.HEX
                elif string.startswith("0b"):
                    exact_kind = TokenExactKind.BINARY
                elif string.startswith("0o"):
                    exact_kind = TokenExactKind.OCTAL
                elif string[-1] in "jJ":
                    exact_kind = TokenExactKind.IMAG
                else:
                    symbols = set(string)
                    # Definitely a float.
                    if "." in symbols:
                        exact_kind = TokenExactKind.FLOAT

                    # 00e0 is a float and can be interpreted as hex,
                    # but we assume this is a float.
                    elif symbols.intersection("eE"):
                        exact_kind = TokenExactKind.FLOAT

                    else:
                        exact_kind = TokenExactKind.INT

            # Names can be keywords, soft-keywords (including Ren'Py) or
            # identifiers. Otherwise it is a 0name, which is not an identifier,
            # but e.g. is a valid attribute name.
            case tokenize.NAME:
                kind = TokenKind.NAME

                if keyword.iskeyword(string):
                    exact_kind = TokenExactKind.KEYWORD
                elif string.isidentifier():
                    exact_kind = TokenExactKind.IDENTIFIER
                else:
                    exact_kind = TokenExactKind.NAME

            case _:
                kind = TokenKind(tokenize.tok_name[type].lower())
                exact_kind = TokenExactKind(tokenize.tok_name[type].lower())

        self.kind: TokenKind = kind
        """
        Kind of the token, such as TokenKind.NAME, TokenKind.OP or TokenKind.NUMBER.
        Can be iterpreted as a corresponding lower-cased string.
        """

        self.exact_kind: TokenExactKind = exact_kind
        """
        Exact kind of the token, such as TokenExactKind.KEYWORD, TokenExactKind.DOLLAR or TokenExactKind.INT.
        Can be iterpreted as a corresponding upper-cased string.
        """

        self.string: str = string
        """
        String value of the token.
        """

        self.munged: str = string
        """
        Munged string of the token, if applicable.
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
        4. It disallows non-ASCII characters in names.
        5. It munges names that starts with double underscores
           (e.g. "__foo" -> f"_m1_{filename}__foo").
        6. It also munges words inside strings that start with double
           underscores.
        7. It checks for non-terminated strings and parenthesis.
        8. It checks for parenthesis order of closing.

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
                        hold_number.munged = hold_number.string
                        hold_number.end_lineno = result.end_lineno
                        hold_number.end_col_offset = result.end_col_offset

                        # We don't yield it yet, because '01attr' is 3 Python tokens.
                        continue

                    # 0-prefixed name is a valid in Ren'Py (e.g. image attributes).
                    # NUMBER "$1" and NAME "$2" should appear as NAME "$1$2"
                    elif t.type == tokenize.NAME:
                        result.string = f"{hold_number.string}{result.string}"
                        result.munged = result.string
                        result.lineno = hold_number.lineno
                        result.col_offset = hold_number.col_offset
                        hold_number = None

                    # TODO: ERRORTOKEN "`" ... ERRORTOKEN "`" -> STRING???

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
                raise SyntaxError(f"closing parenthesis '{parens[-1].string}' "
                                  f"does not match opening parenthesis '{token.string}'"
                                  f" at {self.filename}:{lineno}:{col_offset}")

        prefix: str = munge_filename(self.filename)

        munge_regexp = re.compile(r'\b__(\w+)')

        def munge_string(m: re.Match[str]):
            g1 = m.group(1)

            if "__" in g1:
                return m.group(0)

            if g1.startswith("_"):
                return m.group(0)

            return prefix + m.group(1)

        parens: list[Token] = []
        for token in self._tokenize():
            match token.exact_kind:
                case TokenExactKind.RPAR | TokenExactKind.RBRACE | TokenExactKind.RSQB if not parens:
                    unmatched_paren()
                case TokenExactKind.RPAR if parens[-1].exact_kind != TokenExactKind.LPAR:
                    wrong_paren()
                case TokenExactKind.RBRACE if parens[-1].exact_kind != TokenExactKind.LBRACE:
                    wrong_paren()
                case TokenExactKind.RSQB if parens[-1].exact_kind != TokenExactKind.LSQB:
                    wrong_paren()

                case TokenExactKind.LPAR | TokenExactKind.LBRACE | TokenExactKind.LSQB:
                    parens.append(token)
                case TokenExactKind.RPAR | TokenExactKind.RBRACE | TokenExactKind.RSQB:
                    parens.pop()

            match token.kind:
                case TokenKind.NAME | TokenKind.STRING if "__" in token.string:
                    token.munged = munge_regexp.sub(
                        munge_string, token.munged)

                    token.munged = sys.intern(token.munged)

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
            match token.kind:
                # Empty lines and bare comments are not logical lines.
                case TokenKind.NL | TokenKind.COMMENT if not tokens:
                    continue
                case TokenKind.INDENT:
                    depth += 1
                case TokenKind.DEDENT:
                    depth -= 1
                case _:
                    tokens.append(token)

            if token.kind is TokenKind.NEWLINE:
                rv.append(Line(*tokens, indent_depth=depth))
                tokens.clear()

        return rv

    def list_tokens(self) -> list[Token]:
        return list(self._yield_tokens())


word_regexp = r'[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*'


class SubParse:
    """
    This represents the information about a subparse that can be provided to
    a creator-defined statement.
    """

    def __init__(self, block: list[renpy.ast.Node]):
        self.block = block

    def __repr__(self):

        if not self.block:
            return "<SubParse empty>"
        else:
            return "<SubParse {}:{}>".format(self.block[0].filename, self.block[0].linenumber)


class Lexer:
    """
    The lexer that is used to lex script files. This works on the idea
    that we want to lex each line in a block individually, and use
    sub-lexers to lex sub-blocks.
    """

    def __init__(
        self,
        block: list[Line],
        init=False,
        init_offset=0,
        global_label: str | None = None,
        monologue_delimiter="\n\n",
        subparses: list[SubParse] | None = None,
    ):

        # Are we underneath an init block?
        self.init = init

        # The priority of auto-defined init statements.
        self.init_offset = init_offset

        self.global_label = global_label
        self.monologue_delimiter = monologue_delimiter
        self.subparses = subparses

        # List of lines that make up this indentation block.
        self._block = block

        # Index of current logical line in block.
        # Should change only by advace/unadvance.
        # -1 means we are before the first line.
        self._line_index: int = -1

        # Line instance of current logical line.
        self._line: Line | None = None

        # List of tokens in line.
        self._tokens: list[Token] = []
        # List of start positions of token in line.
        self._tokens_pos: list[int] = []
        # Index of current token in tokens, or None if at end of line.
        self._token_index: int | None = None

        # Position of 'cursor' in the line.
        # Most often it is equal to tokens_keys[token_index], but it can be
        # different if the cursor is in the middle of a token after match_regexp.
        self._pos: int = 0

        self.text: str = ""

    @property
    def _mid_token(self):
        idx = self._token_index
        if idx is None:
            return False

        return self._pos != self._tokens_pos[idx]

    def _update_line(self, idx: int):
        self._line_index = idx
        self._line = self._block[idx]
        self._tokens = []
        self._tokens_pos = []
        self._token_index = 0
        self._pos = 0

        pos = 0
        prev_row = self._line.tokens[0].lineno
        prev_col = 0
        cont_line = False
        result: list[str] = []

        for t in self._line.tokens:
            # Don't add spurious spaces before new line.
            if t.kind in (TokenKind.NL, TokenKind.NEWLINE):
                cont_line = False
                prev_col = 0
                continue

            # Comments don't play nicely with some evaluations.
            if t.kind is TokenKind.COMMENT:
                continue

            if row_offset := t.lineno - prev_row:
                if cont_line:
                    result.append(" \\")

                result.append("\n" * row_offset)
                pos += row_offset
                prev_col = 0

            if col_offset := t.col_offset - prev_col:
                result.append(" " * col_offset)
                pos += col_offset

            self._tokens.append(t)
            self._tokens_pos.append(pos)
            result.append(t.munged)
            prev_row = t.end_lineno
            prev_col = t.end_col_offset
            cont_line = True
            pos += len(t.munged)

        self.text = "".join(result)

    @property
    def _current_token(self):
        if self._token_index is None:
            return None

        return self._tokens[self._token_index]

    def _advance_token(self):
        if self._token_index is None:
            return

        self._token_index += 1
        if self._token_index >= len(self._tokens_pos):
            self._pos = len(self.text)
            self._token_index = None
        else:
            self._pos = self._tokens_pos[self._token_index]

    def _yield_subblock_lines(self) -> Iterator[Line]:
        if self._line is None:
            return

        idx = self._line_index + 1
        depth = self._line.indent_depth
        while idx < len(self._block):
            l = self._block[idx]
            if l.indent_depth > depth:
                idx += 1
                yield l
            else:
                break

    @property
    def subblock(self):
        return self.has_block()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: int):
        if value >= len(self.text):
            self._pos = len(self.text)
            self._token_index = None
        else:
            # Since keys are sorted and distinct, we can use
            # bisect to find the right key.
            import bisect

            idx = bisect.bisect(self._tokens_pos, value)

            if value == self._tokens_pos[idx - 1]:
                self._pos = value
                self._token_index = idx - 1
            else:
                # If pos points to spaces, snap it to the beginning
                # of the token.
                while self.text[value] in " \n":
                    value += 1

                self._pos = value
                self._token_index = idx

    @property
    def filename(self) -> str:
        """
        Elided filename where current logical line is located.
        """

        if self._line is None:
            return ""

        return self._line.filename

    @property
    def number(self) -> int:
        """
        Line number where current logical line is located.
        """

        if self._line is None:
            return 0

        return self._line.start[0]

    @property
    def eob(self):
        return self._line_index > len(self._block)

    def eol(self):
        """
        Returns True if, after skipping whitespace, the current
        position is at the end of the end of the current line, or
        False otherwise.
        """

        return self._current_token is None

    def _unmunge_string(self, s: str) -> str:
        prefix = munge_filename(self.filename)
        return s.replace(prefix, "__")

    def advance(self):
        """
        Advances this lexer to the next line in the block. The lexer
        starts off before the first line, so advance must be called
        before any matching can be done. Returns True if we've
        successfully advanced to a line in the block, or False if we
        have advanced beyond all lines in the block. In general, once
        this method has returned False, the lexer is in an undefined
        state, and it doesn't make sense to call any method other than
        advance (which will always return False) on the lexer.
        """

        block_len = len(self._block)
        if not block_len:
            self._line_index = 1
            return False

        idx = self._line_index
        depth = self._block[0].indent_depth

        while (idx := idx + 1) < block_len:
            line = self._block[idx]
            if line.indent_depth == depth:
                break
        else:
            self._line_index = block_len + 1
            self.pos = len(self.text)
            return False

        self._update_line(idx)
        self.pos = 0
        return True

    def unadvance(self):
        """
        Puts the parsing point at the end of the previous line. This is used
        after renpy_statement to prevent the advance that Ren'Py statements
        do.
        """

        idx = min(self._line_index, len(self._block) - 1)
        depth = self._line.indent_depth
        while (idx := idx - 1) >= 0:
            line = self._block[idx]
            if line.indent_depth == depth:
                break
        else:
            self._line_index = 0
            return

        self._update_line(idx)
        self.pos = len(self.text)

    _OP_REGEX = {
        re.escape(k): TokenExactKind(tokenize.tok_name[v].lower())
        for k, v in tokenize.EXACT_TOKEN_TYPES.items()}
    _OP_REGEX |= {
        k: TokenExactKind(tokenize.tok_name[v].lower())
        for k, v in tokenize.EXACT_TOKEN_TYPES.items()}

    def match_regexp(self, regexp: str):
        """
        Tries to match the given regexp at the current location on the
        current line. If it succeeds, it returns the matched text (if
        any), and updates the current position to be after the
        match. Otherwise, returns None and the position is unchanged.
        """

        if self.eob:
            return None

        if self.pos == len(self.text):
            return None

        # Fast path for some simple expressions.
        if not self._mid_token:
            if regexp in self._OP_REGEX:
                kind = self._OP_REGEX[regexp]
                if (tok := self._lookup_exact_token(kind)) is None:
                    return None

                self._advance_token()
                return tok.string

            if keyword.iskeyword(regexp):
                if (tok := self._lookup_exact_token(TokenExactKind.KEYWORD)) is None:
                    return None

                if tok.string != regexp:
                    return None

                self._advance_token()
                return tok.string

            if regexp.isidentifier():
                if (tok := self._lookup_exact_token(TokenExactKind.IDENTIFIER)) is None:
                    return None

                if tok.munged != regexp:
                    return None

                self._advance_token()
                return tok.munged

        p = re.compile(regexp, re.DOTALL)
        m = p.match(self.text, self.pos)

        if m is None:
            return None

        self.pos = m.end()
        return m.group(0)

    def skip_whitespace(self):
        """
        Advances the current position beyond any contiguous whitespace.
        """

        # Does nothing, because tokens does not care about whitespace.

    def match(self, regexp):
        """
        Matches something at the current position, skipping past
        whitespace. Even if we can't match, the current position is
        still skipped past the leading whitespace.
        """

        return self.match_regexp(regexp)

    def match_multiple(self, *regexps):
        """
        Matches multiple regular expressions. Return a tuple of matches
        if all match, and if not returns None.
        """

        oldpos = self.pos

        rv = tuple(self.match(i) for i in regexps)
        if None in rv:
            self.pos = oldpos
            return None

        return rv

    def keyword(self, word):
        """
        Matches a keyword at the current position. A keyword is a word
        that is surrounded by things that aren't words, like
        whitespace. (This prevents a keyword from matching a prefix.)
        """

        oldpos = self.pos
        if self.word() == word:
            return word

        self.pos = oldpos
        return ''

    @contextlib.contextmanager
    def catch_error(self):
        """
        Catches errors, then causes the line to advance if it hasn't been
        advanced already.
        """

        try:
            yield
        except ParseError as e:
            renpy.parser.parse_errors.append(e.message)

    def error(self, msg):
        """
        Convenience function for reporting a parse error at the current
        location.
        """

        if self._line is None and self._block:
            self._update_line(0)

        raise ParseError(
            msg,
            self.filename,
            self.number,
            self.pos,
            self.text)

    def deferred_error(self, queue, msg):
        """
        Adds a deferred error to the given queue. This is used for something
        that might be an error, but could be compat-ed away.

        `queue`
            A string giving a list of deferred errors to add to.
        """

        if self._line is None and self._block:
            self._update_line(0)

        ParseError(
            msg, self.filename,
            self.number, self.pos + 1,
            self.text).defer(queue)

    def expect_eol(self):
        """
        If we are not at the end of the line, raise an error.
        """

        if not self.eol():
            self.error('end of line expected.')

    def expect_noblock(self, stmt):
        """
        Called to indicate this statement does not expect a block.
        If a block is found, raises an error.
        """

        if self.has_block():
            ll = self.subblock_lexer()
            ll.advance()
            ll.error(f"Line is indented, but the preceding {stmt} statement does not expect a block. "
                     "Please check this line's indentation. You may have forgotten a colon (:).")

    def expect_block(self, stmt):
        """
        Called to indicate that the statement requires that a non-empty
        block is present.
        """

        if not self.has_block():
            self.error('%s expects a non-empty block.' % stmt)

    def has_block(self):
        """
        Called to check if the current line has a non-empty block.
        """

        return next(self._yield_subblock_lines(), None) is not None

    def subblock_lexer(self, init=False):
        """
        Returns a new lexer object, equiped to parse the block
        associated with this line.
        """

        init = self.init or init

        return Lexer(
            list(self._yield_subblock_lines()),
            init=init,
            init_offset=self.init_offset,
            global_label=self.global_label,
            monologue_delimiter=self.monologue_delimiter,
            subparses=self.subparses)

    def _lookup_token(self, kind: TokenKind | str | None = None):
        if self._mid_token:
            return None

        current_token = self._current_token
        if current_token is None:
            return None

        if kind is None:
            return current_token

        if isinstance(kind, str):
            kind = TokenKind(kind)

        if current_token.kind is kind:
            return current_token
        else:
            return None

    def _lookup_exact_token(self, kind: TokenExactKind | str):
        if self._mid_token:
            return None

        current_token = self._current_token
        if current_token is None:
            return None

        if isinstance(kind, str):
            kind = TokenExactKind(kind)

        if current_token.exact_kind is kind:
            return current_token
        else:
            return None

    @staticmethod
    def _dequote_string(m: re.Match[str]):
        c: str = m.group(1)

        if c[0] == 'u' and (group2 := m.group(2)):
            return chr(int(group2, 16))
        elif c == "{":
            return "{{"
        elif c == "[":
            return "[["
        elif c == "%":
            return "%%"
        elif c == "n":
            return "\n"
        else:
            return c

    def string(self):
        """
        Lexes a non-triple-quoted string, and returns the string to the user, or None if
        no string could be found. This also takes care of expanding
        escapes and collapsing whitespace.

        Be a little careful, as this can return an empty string, which is
        different than None.
        """

        tok = self._lookup_exact_token(TokenExactKind.RAW_STRING)
        if tok is not None:
            self._advance_token()
            return tok.munged[2:-1]

        tok = self._lookup_exact_token(TokenExactKind.STRING)
        if tok is None:
            return None

        self._advance_token()

        s = tok.munged[1:-1]

        # Collapse runs of whitespace into single spaces.
        s = re.sub(r'[ \n]+', ' ', s)

        s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', self._dequote_string, s)
        return s

    def triple_string(self):
        """
        Lexes a triple quoted string, intended for use with monologue mode.
        This is about the same as the double-quoted strings, except that
        runs of whitespace with multiple newlines are turned into a single
        newline.

        Except in the case of a raw string where this returns a simple string,
        this returns a list of strings.
        """

        tok = self._lookup_exact_token(TokenExactKind.RAW_TRIPLE_STRING)
        if tok is not None:
            self._advance_token()
            return tok.munged[4:-3]

        tok = self._lookup_exact_token(TokenExactKind.TRIPLE_STRING)
        if tok is None:
            return None

        self._advance_token()

        s = tok.munged[3:-3]

        s = re.sub(r' *\n *', '\n', s)

        mondel = self.monologue_delimiter

        if mondel:
            sl = s.split(mondel)
        else:
            sl = [s]

        rv: list[str] = []
        for s in sl:
            s = s.strip()

            if not s:
                continue

            # Collapse runs of whitespace into single spaces.
            if mondel:
                s = re.sub(r'[ \n]+', ' ', s)
            else:
                s = re.sub(r' +', ' ', s)

            s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', self._dequote_string, s)

            rv.append(s)

        return rv

    def integer(self):
        """
        Tries to parse an integer. Returns a string containing the
        integer, or None.
        """

        tok = self._lookup_token()
        if tok is None:
            return None

        pos = self.pos
        if tok.exact_kind is TokenExactKind.PLUS:
            self._advance_token()
            rv = "+"
        elif tok.exact_kind is TokenExactKind.MINUS:
            self._advance_token()
            rv = "-"
        else:
            rv = ""

        tok = self._lookup_exact_token(TokenExactKind.INT)
        if tok is None:
            self.pos = pos
            return None
        else:
            self._advance_token()
            return rv + tok.string

    def float(self):
        """
        Tries to parse a number (float). Returns a string containing the
        number, or None.
        """

        tok = self._lookup_token()
        if tok is None:
            return None

        pos = self.pos
        if tok.exact_kind is TokenExactKind.PLUS:
            self._advance_token()
            rv = "+"
        elif tok.exact_kind is TokenExactKind.MINUS:
            self._advance_token()
            rv = "-"
        else:
            rv = ""

        tok = self._lookup_exact_token(TokenExactKind.FLOAT)
        if tok is None:
            self.pos = pos
            return None
        else:
            self._advance_token()
            return rv + tok.string

    def hash(self):
        """
        Matches the characters in an md5 hash, and then some.
        """

        tok = self._lookup_token(TokenKind.NAME)
        if tok is None:
            return None
        else:
            self._advance_token()
            return tok.munged

    def word(self):
        """
        Parses a name, which may be a keyword or not.
        """

        tok = self._lookup_token(TokenKind.NAME)
        if tok is None:
            return None
        else:
            self._advance_token()
            return tok.munged

    def name(self):
        """
        This tries to parse a name. Returns the name or None.
        """

        tok = self._lookup_token()
        if tok is None:
            return None

        if tok.exact_kind is TokenExactKind.IDENTIFIER:
            self._advance_token()
            return tok.munged

        # Constants are names in old parser.
        if tok.exact_kind is TokenExactKind.KEYWORD:
            if tok.string in ("True", "False", "None"):
                self._advance_token()
                return tok.munged

        return None

    def image_name_component(self):
        """
        Matches a word that is a component of an image name. (These are
        strings of numbers, letters, and underscores.)
        """

        tok = self._lookup_token()
        if tok is None:
            return None

        if tok.kind is TokenKind.NAME:
            pass
        # All digits except those with dot or +- are valid.
        elif tok.kind is TokenKind.NUMBER and tok.string.isalnum():
            pass
        else:
            return None

        if tok.string in (
            'as',
            'if',
            'in',
            'return',
            'with',
            'while',
            'behind',
            'at',
            'onlayer',
            'with',
            'zorder',
            'transform',
        ):
            return None

        self._advance_token()
        return tok.munged

    def set_global_label(self, label):
        """
        Set current global_label, which is used for label_name calculations.
        label can be any valid label or None, but this has only effect if label
        has global part.
        """

        if label and label[0] != '.':
            self.global_label = label.split('.')[0]

    def label_name(self, declare=False):
        """
        Try to parse label name. Returns name in form of "global.local" if local
        is present, "global" otherwise; or None if it doesn't parse.

        If declare is True, allow only such names that are valid for declaration
        (e.g. forbid global name mismatch)
        """

        old_pos = self.pos
        local_name = None
        global_name = self.name()

        dot = bool(self._lookup_exact_token(TokenExactKind.DOT))
        if dot:
            self._advance_token()

        if global_name is None:
            # .local label
            if not dot or not self.global_label:
                self.pos = old_pos
                return None

            global_name = self.global_label
            local_name = self.name()
            if not local_name:
                self.pos = old_pos
                return None
        elif dot:
            # full global.local name
            if declare and global_name != self.global_label:
                self.pos = old_pos
                return None

            local_name = self.name()
            if not local_name:
                self.pos = old_pos
                return None

        if not local_name:
            return global_name

        return global_name + '.' + local_name

    def label_name_declare(self):
        """
        Same as label_name, but set declare to True.
        """
        return self.label_name(declare=True)

    def python_string(self):
        """
        This tries to match a python string at the current
        location. If it matches, it returns True, and the current
        position is updated to the end of the string. Otherwise,
        returns False.
        """

        tok = self._lookup_token(TokenKind.STRING)
        if tok is None:
            return False
        else:
            self._advance_token()
            return True

    def dotted_name(self):
        """
        This tries to match a dotted name, which is one or more names,
        separated by dots. Returns the dotted name if it can, or None
        if it cannot.

        Once this sees the first name, it commits to parsing a
        dotted_name. It will report an error if it then sees a dot
        without a name behind it.
        """

        rv = self.name()

        if not rv:
            return None

        while self._lookup_exact_token(TokenExactKind.DOT):
            self._advance_token()
            n = self.name()
            if not n:
                self.error('expecting name.')

            rv += "." + n

        return rv

    def expr(self, s: str, expr):
        if not expr:
            return s

        s = self._unmunge_string(s)

        return renpy.ast.PyExpr(s, self.filename, self.number)

    def delimited_python(self, delim: str | TokenExactKind, expr=True):
        """
        This matches python code up to, but not including, the non-whitespace
        delimiter characters. Returns a string containing the matched code,
        which may be empty if the first thing is the delimiter. Raises an
        error if EOL is reached before the delimiter.
        """

        if type(delim) is str and delim in self._OP_REGEX:
            delim = self._OP_REGEX[delim]

        start = self.pos
        if isinstance(delim, TokenExactKind):
            while not self.eol():

                tok = self._lookup_token()
                if tok is None:
                    break

                if tok.exact_kind is delim:
                    return self.expr(self.text[start:self.pos], expr)

                if self.python_string():
                    continue

                if self.parenthesised_python():
                    continue

                self._advance_token()
        else:
            while not self.eol():

                c = self.text[self.pos]

                if c in delim:
                    return self.expr(self.text[start:self.pos], expr)

                if self.python_string():
                    continue

                if self.parenthesised_python():
                    continue

                self.pos += 1

        self.error(f"reached end of line when expecting '{delim}'.")

    def python_expression(self, expr=True):
        """
        Returns a python expression, which is arbitrary python code
        extending to a colon.
        """

        pe = self.delimited_python(TokenExactKind.COLON, False)

        if not pe:
            self.error("expected python_expression")

        rv = self.expr(pe.strip(), expr)

        return rv

    def parenthesised_python(self):
        """
        Tries to match a parenthesised python expression. If it can,
        returns true and updates the current position to be after the
        closing parenthesis. Returns False otherwise.
        """

        tok = self._lookup_token()
        if tok is None:
            return False

        if tok.exact_kind is TokenExactKind.LPAR:
            self._advance_token()
            self.delimited_python(TokenExactKind.RPAR, False)
            self._advance_token()
            return True
        elif tok.exact_kind is TokenExactKind.LSQB:
            self._advance_token()
            self.delimited_python(TokenExactKind.RSQB, False)
            self._advance_token()
            return True
        elif tok.exact_kind is TokenExactKind.LBRACE:
            self._advance_token()
            self.delimited_python(TokenExactKind.RBRACE, False)
            self._advance_token()
            return True

        return False

    def _atom(self):
        # https://docs.python.org/3/reference/expressions.html#atoms

        # Some kind of enclosure.
        if self.parenthesised_python():
            return True

        tok = self._lookup_token()
        if tok is None:
            return False

        # Literals.
        if tok.kind is TokenKind.STRING:
            self._advance_token()
            return True

        if tok.kind is TokenKind.NUMBER:
            self._advance_token()
            return True

        return bool(self._simple_expression_func())

    def _primary(self):
        # https://docs.python.org/3/reference/expressions.html#grammar-token-python-grammar-primary

        # All primaries start with atom.
        if not self._atom():
            return False

        while tok := self._lookup_token():
            # attributeref ::= primary "." identifier
            if tok.exact_kind is TokenExactKind.DOT:
                self._advance_token()
                if not self._simple_expression_func():
                    self.error("expecting name after dot.")
            # subscription | slicing ::= primary "[" expression "]"
            elif tok.exact_kind is TokenExactKind.LSQB:
                self._advance_token()
                self.delimited_python(TokenExactKind.RSQB, False)
                self._advance_token()
            # call ::= primary "(" [argument_list] ")"
            elif tok.exact_kind is TokenExactKind.LPAR:
                self._advance_token()
                self.delimited_python(TokenExactKind.RPAR, False)
                self._advance_token()
            else:
                break

        return True

    def _u_expr(self):
        # https://docs.python.org/3/reference/expressions.html#grammar-token-python-grammar-u_expr
        while tok := self._lookup_token():
            # "~" u_expr
            if tok.exact_kind is TokenExactKind.TILDE:
                self._advance_token()
            # "+" u_expr
            elif tok.exact_kind is TokenExactKind.PLUS:
                self._advance_token()
            # "-" u_expr
            elif tok.exact_kind is TokenExactKind.MINUS:
                self._advance_token()
            # "not" u_expr
            elif tok.exact_kind is TokenExactKind.KEYWORD and tok.string == "not":
                self._advance_token()
            else:
                break

        # It is 'power' in Python grammar, but because we don't care about
        # operator precedence we parse primary here.
        return self._primary()

    def _operator(self):
        # Combination of power, binary arithmetic, shift, bitwise, comparison
        # and logical operators.

        # u_expr (OP u_expr)+
        if not self._u_expr():
            return False

        binops = (
            TokenExactKind.PLUS,
            TokenExactKind.MINUS,
            TokenExactKind.STAR,
            TokenExactKind.SLASH,
            TokenExactKind.VBAR,
            TokenExactKind.AMPER,
            TokenExactKind.LESS,
            TokenExactKind.GREATER,
            TokenExactKind.PERCENT,
            TokenExactKind.EQEQUAL,
            TokenExactKind.NOTEQUAL,
            TokenExactKind.LESSEQUAL,
            TokenExactKind.GREATEREQUAL,
            TokenExactKind.CIRCUMFLEX,
            TokenExactKind.LEFTSHIFT,
            TokenExactKind.RIGHTSHIFT,
            TokenExactKind.DOUBLESTAR,
            TokenExactKind.DOUBLESLASH,
            TokenExactKind.AT,
        )
        while tok := self._lookup_token():
            ename = tok.exact_kind
            # "and" u_expr
            if ename is TokenExactKind.KEYWORD and tok.string == "and":
                pass
            # "or" u_expr
            elif ename is TokenExactKind.KEYWORD and tok.string == "or":
                pass
            # "is" u_expr
            # 'not' here is part of u_expr
            elif ename is TokenExactKind.KEYWORD and tok.string == "is":
                pass
            # "in" u_expr
            elif ename is TokenExactKind.KEYWORD and tok.string == "in":
                pass
            # "not in" u_expr
            elif ename is TokenExactKind.KEYWORD and tok.string == "not":
                self._advance_token()
                if not (
                    (tok2 := self._lookup_token()) and
                    tok2.exact_kind is TokenExactKind.KEYWORD and
                    tok2.string == "in"
                ):
                    self.error("expecting 'in' after 'not'.")
            # BINOP u_expr
            elif next((True for n in binops if n is ename), False):
                pass
            else:
                break

            self._advance_token()
            if not self._u_expr():
                self.error("expecting expression after operator.")

            continue

    def _conditional_expression(self):
        # https://docs.python.org/3/reference/expressions.html#conditional-expressions
        if not self._operator():
            return False

        # No condition here.
        if (tok := self._lookup_token()) is None or tok.string != "if":
            return True

        # expression "if" expression "else" expression
        self._advance_token()

        if not self._operator():
            self.error("expecting expression after if.")

        if (tok := self._lookup_token()) is None or tok.string != "else":
            self.error("expecting else after if expression.")

        self._advance_token()

        if not self._operator():
            self.error("expecting expression after else.")

        return True

    def simple_expression(self, comma=False, operator=True, image=False):
        """
        Tries to parse a simple_expression. Returns the text if it can, or
        None if it cannot.

        If comma is True, then a comma is allowed to appear in the
        expression.

        If operator is True, then an operator is allowed to appear in
        the expression.

        If image is True, then the expression is being parsed as part of
        an image, and so keywords that are special in the show/hide/scene
        statements are not allowed.
        """

        # https://docs.python.org/3/reference/expressions.html
        # More technically, when operator is allowed, this parses Python
        # 'conditional_expression', otherwise it parses 'primary'.
        # If comma is True, then it consumes tuple of expressions.
        # If image is True, some bare names are not allowed, unless they
        # parenthesized.

        if self.eol():
            return None

        if self._mid_token:
            raise Exception("Can't start expression in the middle of a token.")

        start = self.pos
        if image:
            self._simple_expression_func = self.image_name_component
        else:
            self._simple_expression_func = self.name

        if operator:
            parse_func = self._conditional_expression
        else:
            parse_func = self._primary

        while not self.eol():
            parse_func()

            if comma and self._lookup_exact_token(TokenExactKind.COMMA):
                self._advance_token()
                continue

            break

        del self._simple_expression_func

        text = self.text[start:self.pos].strip()

        if not text:
            return None

        return self.expr(text, True)

    def comma_expression(self):
        """
        One or more simple expressions, separated by commas, including an
        optional trailing comma.
        """

        return self.simple_expression(comma=True)

    def say_expression(self):
        """
        Parses the name portion of a say statement.
        """
        return self.simple_expression(operator=False)

    class _Checkpoint(NamedTuple):
        def __reduce__(self):
            raise TypeError("Can't pickle Lexer checkpoints.")

        line_index: int
        pos: int
        pyexpr_checkpoint: Any

    def checkpoint(self) -> _Checkpoint:
        """
        Returns an opaque representation of the lexer state. This can be
        passed to revert to back the lexer up.
        """

        return self._Checkpoint(
            self._line_index,
            self.pos,
            renpy.ast.PyExpr.checkpoint())

    def revert(self, state: _Checkpoint):
        """
        Reverts the lexer to the given state. State must have been returned
        by a previous checkpoint operation on this lexer.
        """

        line_index, pos, pyexpr_checkpoint = state

        self._update_line(line_index)
        self.pos = pos
        renpy.ast.PyExpr.revert(pyexpr_checkpoint)

    def get_location(self):
        """
        Returns a (filename, line number) tuple representing the current
        physical location of the start of the current logical line.
        """

        return self.filename, self.number

    def require(self, thing, name=None, **kwargs):
        """
        Tries to parse thing, and reports an error if it cannot be done.

        If thing is a string, tries to parse it using
        self.match(thing). Otherwise, thing must be a method on this lexer
        object, which is called directly.
        """

        if isinstance(thing, str):
            rv = self.match(thing)
        else:
            rv = thing(**kwargs)

        if rv is None:
            if isinstance(thing, str):
                name = name or thing
            else:
                name = name or thing.__func__.__name__

            self.error("expected '%s' not found." % name)

        return rv

    def rest(self):
        """
        Skips whitespace, then returns the rest of the current
        line, and advances the current position to the end of
        the current line.
        """

        pos = self.pos
        self.pos = len(self.text)
        return self.expr(self.text[pos:].strip(), True)

    def rest_statement(self):
        """
        Like rest, but returns a string rather than a PyExpr.
        """

        pos = self.pos
        self.pos = len(self.text)
        return self.text[pos:].strip()

    def python_block(self):
        """
        Returns the subblock of this code, and subblocks of that
        subblock, as indented python code. This tries to insert
        whitespace to ensure line numbers match up.
        """

        prev_row = self._line.tokens[-1].lineno + 1
        depth = self._line.indent_depth + 1
        result: list[str] = []

        for line in self._yield_subblock_lines():
            first = line.tokens[0]

            if row_offset := first.lineno - prev_row:
                result.append("\n" * row_offset)

            # Remove indent from the beginning of the line.
            result.append("    " * (line.indent_depth - depth))

            prev_row = first.lineno
            prev_col = first.col_offset
            cont_line = False

            for t in line.tokens:
                # Don't add spurious spaces before new line.
                if t.kind in (TokenKind.NL, TokenKind.NEWLINE):
                    cont_line = False
                    prev_col = 0
                    continue

                # Comments don't play nicely with some evaluations.
                if t.kind is TokenKind.COMMENT:
                    continue

                if row_offset := t.lineno - prev_row:
                    if cont_line:
                        result.append(" \\")

                    result.append("\n" * row_offset)
                    prev_col = 0

                if col_offset := t.col_offset - prev_col:
                    result.append(" " * col_offset)

                result.append(t.munged)
                prev_row = t.end_lineno
                prev_col = t.end_col_offset
                cont_line = True

        return "".join(result)

    def arguments(self):
        """
        Returns an Argument object if there is a list of arguments, or None
        there is not one.
        """

        return renpy.parser.parse_arguments(self)

    def renpy_statement(self):
        """
        Parses the remainder of the current line as a statement in the
        Ren'Py script language. Returns a SubParse corresponding to the
        AST node generated by that statement.
        """

        if self.subparses is None:
            raise Exception("A renpy_statement can only be parsed inside a creator-defined statement.")

        block = renpy.parser.parse_statement(self)
        self.unadvance()

        if not isinstance(block, list):
            block = [ block ]

        sp = SubParse(block)
        self.subparses.append(sp)

        return sp

    def renpy_block(self, empty=False):

        if self.subparses is None:
            raise Exception("A renpy_block can only be parsed inside a creator-defined statement.")

        if self._line_index < 0:
            self.advance()

        block = [ ]

        while not self.eob:
            try:

                stmt = renpy.parser.parse_statement(self)

                if isinstance(stmt, list):
                    block.extend(stmt)
                else:
                    block.append(stmt)

            except ParseError as e:
                renpy.parser.parse_errors.append(e.message)
                self.advance()

        if not block:
            if empty:
                block.append(renpy.ast.Pass(self.get_location()))
            else:
                self.error("At least one Ren'Py statement is expected.")

        sp = SubParse(block)
        self.subparses.append(sp)

        return sp
