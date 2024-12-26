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

from typing import Any, Callable, Iterator, TypeAlias

import os
import io
import re
import sys
import tokenize
import contextlib
import keyword

import renpy

# The filename that's in the line text cache.
line_text_filename = ""

# The content of the line text cache.
line_text_cache = []


def get_line_text(filename, lineno):
    """
    Gets the text of a line, in a best-effort way, for debugging purposes. May
    return just a newline, if the line doesn't exist.
    """

    global line_text_filename
    global line_text_cache

    full_filename = renpy.exports.unelide_filename(filename)

    if full_filename != line_text_filename:

        line_text_filename = full_filename

        t = Tokenizer.from_file(full_filename, no_errors=True)
        line_text_cache = t.list_physical_lines()

    if lineno <= len(line_text_cache):
        return line_text_cache[lineno - 1]
    else:
        return "\n"


class ParseError(Exception):

    def __init__(self, filename, number, msg, line=None, pos=None, first=False):
        message = u"File \"%s\", line %d: %s" % (unicode_filename(filename), number, msg)

        if line:
            if isinstance(line, list):
                line = "".join(line)

            lines = line.split('\n')

            if '"""' in lines[0]:
                pass
            elif "'''" in lines[0]:
                pass
            elif len(lines) > 1:
                open_string = None
                i = 0

                while i < len(lines[0]):
                    c = lines[0][i]

                    if c == "\\":
                        i += 1
                    elif c == open_string:
                        open_string = None
                    elif open_string:
                        pass
                    elif c == '`' or c == '\'' or c == '"':
                        open_string = c

                    i += 1

                if open_string:
                    message += "\n(Perhaps you left out a %s at the end of the first line.)" % open_string

            for l in lines:
                message += "\n    " + l

                if pos is not None:
                    if pos <= len(l):
                        message += "\n    " + " " * pos + "^"
                        pos = None
                    else:
                        pos -= len(l)

                if first:
                    break

        self.message = message

        Exception.__init__(self, message)

    def __unicode__(self):
        return self.message

    def defer(self, queue):
        renpy.parser.deferred_parse_errors[queue].append(self.message)

# Something to hold the expected line number.


class LineNumberHolder(object):
    """
    Holds the expected line number.
    """

    def __init__(self):
        self.line = 0


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


# The filename that the start and end positions are relative to.
original_filename = ""


class Line:
    """
    Represents a logical line in a file, which is a sequence of tokens.

    If line starts with INDENT, it is a first line of a new indentation block.
    If line starts with one or more DEDENT, it ends block(s) of indentation.
    Otherwise this line is a next logical line of current indentation block.
    Line always ends with a NEWLINE token.
    """

    __slots__ = ['tokens', 'dedent_line', '_text', '_full_text']

    def __init__(self, token: Token, *tokens: Token, dedent_line: bool):
        self.tokens: tuple[Token, ...] = (token, *tokens)
        """
        List of tokens that make up this line.
        """

        self.dedent_line: bool = dedent_line
        """
        If True, `self.text` is automatically dedented as if it were a
        line outside of any block.
        """

        self._text = None
        self._full_text = None

        if "RENPY_DEBUG_TOKENIZATION" not in os.environ:
            return

        has_indent = False
        has_dedent = False
        has_newline = False
        stop_dent = False
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

            match t.name:
                case "INDENT" if has_indent:
                    raise ValueError("Line can start with only one INDENT token.")
                case "INDENT" if has_dedent:
                    raise ValueError("Line can have either INDENT or DEDENT tokens, not both.")
                case "INDENT" if stop_dent:
                    raise ValueError("INDENT token can appear only as first token.")
                case "INDENT":
                    has_indent = True

                case "DEDENT" if has_indent:
                    raise ValueError("Line can have either INDENT or DEDENT tokens, not both.")
                case "DEDENT" if stop_dent:
                    raise ValueError("DEDENT token can not appear after non-DEDENT token.")
                case "DEDENT":
                    has_dedent = True

                case "NEWLINE":
                    has_newline = True
                    break

                case _:
                    stop_dent = True

        if list(tokens_iter):
            raise ValueError("NEWLINE must be the last token.")

        if not has_newline:
            raise ValueError("NEWLINE must be the last token.")

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

    class _Untokenize:
        def __init__(self, tokens: tuple[Token, ...], token_text: Callable[[Token], str]):
            self.tokens = tokens
            self.token_text = token_text

            self.data: list[str] = []
            self.prev_row = self.tokens[0].lineno
            self.prev_col = 0
            self.cont_line = False

        def add_whitespace(self, row: int, col: int):
            row_offset = row - self.prev_row
            if row_offset:
                if self.cont_line:
                    # Assume people continue lines with single space before splash.
                    self.data.append(" \\")

                self.data.append("\n" * row_offset)
                self.prev_col = 0

            col_offset = col - self.prev_col
            if col_offset:
                self.data.append(" " * col_offset)

        def untokenize(self):
            for t in self.tokens:
                name = t.name
                if name == "INDENT" or name == "DEDENT":
                    self.prev_row = t.end_lineno
                    continue

                # Don't add spurious spaces before new line.
                if name != "NL" and name != "NEWLINE":
                    self.add_whitespace(t.lineno, t.col_offset)

                self.data.append(self.token_text(t))
                self.prev_row = t.end_lineno
                self.prev_col = t.end_col_offset
                self.cont_line = True

                if name == "NL":
                    self.cont_line = False
                    self.prev_row += 1
                    self.prev_col = 0

            return "".join(self.data)

    @property
    def text(self) -> str:
        """
        Text of logical line except insignificant whitespace and comments.
        """

        if self._text is not None:
            return self._text

        def token_text(t: Token) -> str:
            if t.name == "NEWLINE" or t.name == "COMMENT":
                return ""

            return t.munged

        result = Line._Untokenize(self.tokens, token_text).untokenize()
        if self.dedent_line:
            result = result.lstrip(" ")

            # XXX: Maybe this is better?
            # import textwrap
            # result = textwrap.dedent(result)

        self._text = result
        return result

    @property
    def full_text(self) -> str:
        """
        Full text of logical line including whitespaces and comments.
        """

        if self._full_text is not None:
            return self._full_text

        def token_text(t: Token) -> str:
            return t.string

        result = Line._Untokenize(self.tokens, token_text).untokenize()
        self._full_text = result
        return result

    def __str__(self):
        return self.full_text

    def __iter__(self):
        return iter((self.filename, self.start[0], self.text))

    def __repr__(self):
        return f"<Line {self.filename} {self.start}-{self.end}>"


class Token:
    """
    Represents a token in a file.
    """

    __slots__ = [
        'name',
        'exact_name',
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
                name = "OP"
                exact_name = "DOLLAR"
            case tokenize.ERRORTOKEN:
                raise ValueError(f"Error token with value: {string!r}")

            # Exact name is one of predefined.
            case tokenize.OP:
                name = "OP"
                type = tokenize.EXACT_TOKEN_TYPES[string]
                exact_name = tokenize.tok_name[type]

            # f-strings and bytes are expressions in Ren'Py,
            # and raw strings are handled differently.
            case tokenize.STRING:
                name = "STRING"

                prefix = re.match(
                    r'([urfbURFB])*("""|\'\'\'|"|\')', string)
                assert prefix is not None
                mods = prefix.group(1) or ""
                kind = prefix.group(2)

                if "b" in mods or "B" in mods:
                    if "f" in mods or "F" in mods:
                        exact_name = "F_BYTES"
                    else:
                        exact_name = "BYTES"
                elif "f" in mods or "F" in mods:
                    exact_name = "F_STRING"
                elif "r" in mods or "R" in mods:
                    if kind == "'''" or kind == '"""':
                        exact_name = "RAW_TRIPLE_STRING"
                    else:
                        exact_name = "TRIPLE_STRING"
                elif kind == "'''" or kind == '"""':
                    exact_name = "RAW_STRING"
                else:
                    exact_name = "STRING"

            # Split numbers into complex, float, and integer.
            case tokenize.NUMBER:
                name = "NUMBER"
                if string.startswith("0x"):
                    exact_name = "HEX"
                elif string.startswith("0b"):
                    exact_name = "BINARY"
                elif string.startswith("0o"):
                    exact_name = "OCTAL"
                elif string[-1] in "jJ":
                    exact_name = "IMAG"
                else:
                    symbols = set(string)
                    # Definitely a float.
                    if "." in symbols:
                        exact_name = "FLOAT"

                    # 00e0 is a float and can be interpreted as hex,
                    # but we assume this is a float.
                    elif symbols.intersection("eE"):
                        exact_name = "FLOAT"

                    else:
                        exact_name = "INT"

            # Names can be keywords, soft-keywords (including Ren'Py) or
            # identifiers. Otherwise it is a 0name, which is not an identifier,
            # but e.g. is a valid attribute name.
            case tokenize.NAME:
                name = "NAME"

                if keyword.iskeyword(string):
                    exact_name = "KEYWORD"
                elif string in IMAGE_KEYWORDS:
                    exact_name = "IMAGE_KEYWORD"
                elif string.isidentifier():
                    exact_name = "IDENTIFIER"
                else:
                    exact_name = "NAME"

            case _:
                name = exact_name = tokenize.tok_name[type]

        self.name: str = name
        """
        String name of the token, such as "NAME", "OP" or "NUMBER".
        """

        self.exact_name: str = exact_name
        """
        String exact name of the token, such as "KW", "DOLLAR" or "INT".
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
        return f"<Token {self.exact_name!r} {string} {self.filename} {location}>"


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

        def non_ascii_name():
            if not self.no_errors:
                bad = next(i for i in token.string if ord(i) > 127)
                lineno = token.lineno + token.physical_offset[0]
                col_offset = token.col_offset + token.physical_offset[1]
                raise SyntaxError(f"Non-ASCII character '{bad}' in name '{token.string}'"
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
            match token.exact_name:
                case "RPAR" | "RBRACE" | "RSQB" if not parens:
                    unmatched_paren()
                case "RPAR" if parens[-1].exact_name != "LPAR":
                    wrong_paren()
                case "RBRACE" if parens[-1].exact_name != "LBRACE":
                    wrong_paren()
                case "RSQB" if parens[-1].exact_name != "LSQB":
                    wrong_paren()

                case "LPAR" | "LBRACE" | "LSQB":
                    parens.append(token)
                case "RPAR" | "RBRACE" | "RSQB":
                    parens.pop()

            match token.name:
                case "NAME" if not token.string.isascii():
                    non_ascii_name()  # Should I remove it???

                case "NAME" | "STRING" if "__" in token.string:
                    token.munged = munge_regexp.sub(munge_string, token.munged)

            self._tokens.append(token)
            yield token

        # Here we might raise SyntaxError for unclosed paren or string literal.

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
        tokens: list[Token] = []

        for token in self._yield_tokens():
            name = token.name

            # Empty lines and bare comments are not logical lines.
            if not tokens and (name == "NL" or name == "COMMENT"):
                continue

            else:
                tokens.append(token)

            if name == "NEWLINE":
                assert tokens, "NEWLINE without tokens?"

                rv.append(Line(*tokens, dedent_line=False))
                tokens.clear()

        return rv

    _Group: TypeAlias = tuple[Line, list["_Group"]]

    def list_grouped_lines(self) -> list[_Group]:
        stack: list[list[Tokenizer._Group]] = [[]]
        for line in self.list_logical_lines():
            for token in line.tokens:
                if token.name == "INDENT":
                    stack.append(stack[-1][-1][1])
                elif token.name == "DEDENT":
                    stack.pop()
                else:
                    break

            new_line = Line(*line.tokens, dedent_line=True)
            new_line._text = line._text
            new_line._full_text = line._full_text
            stack[-1].append((new_line, []))

        return stack[0]

    def list_tokens(self) -> list[Token]:
        return list(self._yield_tokens())


# A list of keywords which should not be parsed as names, because
# there is a huge chance of confusion.
#
# Note: We need to be careful with what's in here, because these
# are banned in simple_expressions, where we might want to use
# some of them.
KEYWORDS = {
    'as',
    'if',
    'in',
    'return',
    'with',
    'while',
}

IMAGE_KEYWORDS = {
    'behind',
    'at',
    'onlayer',
    'with',
    'zorder',
    'transform',
}

OPERATORS = [
    '<>',
    '<<',
    '<=',
    '<',
    '>>',
    '>=',
    '>',
    '!=',
    '==',
    '|',
    '^',
    '&',
    '+',
    '-',
    '**',
    '*',
    '//',
    '/',
    '%',
    '~',
    '@',
    ':=',
]

ESCAPED_OPERATORS = [
    r'\bor\b',
    r'\band\b',
    r'\bnot\b',
    r'\bin\b',
    r'\bis\b',
]

operator_regexp = "|".join([re.escape(i) for i in OPERATORS] + ESCAPED_OPERATORS)

word_regexp = r'[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*'
image_word_regexp = r'[-0-9a-zA-Z_\u00a0-\ufffd][-0-9a-zA-Z_\u00a0-\ufffd]*'


class SubParse(object):
    """
    This represents the information about a subparse that can be provided to
    a creator-defined statement.
    """

    def __init__(self, block):
        self.block = block

    def __repr__(self):

        if not self.block:
            return "<SubParse empty>"
        else:
            return "<SubParse {}:{}>".format(self.block[0].filename, self.block[0].linenumber)


class Lexer(object):
    """
    The lexer that is used to lex script files. This works on the idea
    that we want to lex each line in a block individually, and use
    sub-lexers to lex sub-blocks.
    """

    def __init__(
        self,
        block: list[Tokenizer._Group],
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

        self.block = block
        self.eob = False

        self.global_label = global_label
        self.monologue_delimiter = monologue_delimiter
        self.subparses = subparses

        # Index of current logical line in block.
        # Should change only by advace/unadvance.
        self._line_index: int = -1

        # Line instance of current logical line.
        self._line: Line | None = None

        # Subblock of current logical line.
        self._subblock: list[Tokenizer._Group] = []

        # Position of cursor in line.
        self.pos: int = 0

        self.word_cache_pos: int = -1
        self.word_cache_newpos: int = -1
        self.word_cache: str | None = None

    @property
    def filename(self) -> str:
        if self._line is None:
            return ""

        return self._line.filename

    @property
    def number(self) -> int:
        if self._line is None:
            return 0

        return self._line.start[0]

    @property
    def text(self) -> str:
        if self._line is None:
            return ""

        # Cached in Line class.
        return self._line.text

    @property
    def line(self) -> int:
        return self._line_index

    @property
    def subblock(self) -> list[Tokenizer._Group]:
        return self._subblock

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

        self._line_index += 1

        if self._line_index >= len(self.block):
            self.eob = True
            return False

        self._line, self._subblock = self.block[self._line_index]

        self.pos = 0
        self.word_cache_pos = -1

        return True

    def unadvance(self):
        """
        Puts the parsing point at the end of the previous line. This is used
        after renpy_statement to prevent the advance that Ren'Py statements
        do.
        """

        self._line_index -= 1
        self.eob = False

        self._line, self._subblock = self.block[self._line_index]

        self.pos = len(self.text)
        self.word_cache_pos = -1

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

        p = re.compile(regexp, re.DOTALL)
        m = p.match(self.text, self.pos)

        if not m:
            return None

        self.pos = m.end()

        return m.group(0)

    def skip_whitespace(self):
        """
        Advances the current position beyond any contiguous whitespace.
        """

        # print self.text[self.pos].encode('unicode_escape')

        self.match_regexp(r"(\s+|\\\n)+")

    def match(self, regexp):
        """
        Matches something at the current position, skipping past
        whitespace. Even if we can't match, the current position is
        still skipped past the leading whitespace.
        """

        self.skip_whitespace()
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

        if (self._line_index == -1) and self.block:
            self._line, self._subblock = self.block[0]

        raise ParseError(self.filename, self.number, msg, self.text, self.pos)

    def deferred_error(self, queue, msg):
        """
        Adds a deferred error to the given queue. This is used for something
        that might be an error, but could be compat-ed away.

        `queue`
            A string giving a list of deferred errors to add to.
        """

        if (self._line_index == -1) and self.block:
            self._line, self._subblock = self.block[0]

        ParseError(self.filename, self.number, msg, self.text, self.pos).defer(queue)

    def eol(self):
        """
        Returns True if, after skipping whitespace, the current
        position is at the end of the end of the current line, or
        False otherwise.
        """

        self.skip_whitespace()
        return self.pos >= len(self.text)

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

        if self.subblock:
            ll = self.subblock_lexer()
            ll.advance()
            ll.error("Line is indented, but the preceding {} statement does not expect a block. "
                     "Please check this line's indentation. You may have forgotten a colon (:).".format(stmt))

    def expect_block(self, stmt):
        """
        Called to indicate that the statement requires that a non-empty
        block is present.
        """

        if not self.subblock:
            self.error('%s expects a non-empty block.' % stmt)

    def has_block(self):
        """
        Called to check if the current line has a non-empty block.
        """

        return bool(self.subblock)

    def subblock_lexer(self, init=False):
        """
        Returns a new lexer object, equiped to parse the block
        associated with this line.
        """

        init = self.init or init

        return Lexer(
            self.subblock,
            init=init,
            init_offset=self.init_offset,
            global_label=self.global_label,
            monologue_delimiter=self.monologue_delimiter,
            subparses=self.subparses)

    def string(self):
        """
        Lexes a non-triple-quoted string, and returns the string to the user, or None if
        no string could be found. This also takes care of expanding
        escapes and collapsing whitespace.

        Be a little careful, as this can return an empty string, which is
        different than None.
        """

        s = self.match(r'r?"([^\\"]|\\.)*"')

        if s is None:
            s = self.match(r"r?'([^\\']|\\.)*'")

        if s is None:
            s = self.match(r"r?`([^\\`]|\\.)*`")

        if s is None:
            return None

        if s[0] == 'r':
            raw = True
            s = s[1:]
        else:
            raw = False

        # Strip off delimiters.
        s = s[1:-1]

        def dequote(m):
            c = m.group(1)

            if c == "{":
                return "{{"
            elif c == "[":
                return "[["
            elif c == "%":
                return "%%"
            elif c == "n":
                return "\n"
            elif c[0] == 'u':
                group2 = m.group(2)

                if group2:
                    return chr(int(m.group(2), 16))
            else:
                return c

        if not raw:

            # Collapse runs of whitespace into single spaces.
            s = re.sub(r'[ \n]+', ' ', s)

            s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', dequote, s)  # type: ignore

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

        s = self.match(r'r?"""([^\\"]|\\.|"(?!""))*"""')

        if s is None:
            s = self.match(r"r?'''([^\\']|\\.|'(?!''))*'''")

        if s is None:
            s = self.match(r"r?```([^\\`]|\\.|`(?!``))*```")

        if s is None:
            return None

        if s[0] == 'r':
            raw = True
            s = s[1:]
        else:
            raw = False

        # Strip off delimiters.
        s = s[3:-3]

        def dequote(m):
            c = m.group(1)

            if c == "{":
                return "{{"
            elif c == "[":
                return "[["
            elif c == "%":
                return "%%"
            elif c == "n":
                return "\n"
            elif c[0] == 'u':
                group2 = m.group(2)

                if group2:
                    return chr(int(m.group(2), 16))
            else:
                return c

        if not raw:

            s = re.sub(r' *\n *', '\n', s)

            mondel = self.monologue_delimiter

            if mondel:
                sl = s.split(mondel)
            else:
                sl = [s]

            rv = []

            for s in sl:
                s = s.strip()

                if not s:
                    continue

                # Collapse runs of whitespace into single spaces.
                if mondel:
                    s = re.sub(r'[ \n]+', ' ', s)
                else:
                    s = re.sub(r' +', ' ', s)

                s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', dequote, s)  # type: ignore

                rv.append(s)

            return rv

        return s

    def integer(self):
        """
        Tries to parse an integer. Returns a string containing the
        integer, or None.
        """

        return self.match(r'(\+|\-)?\d+')

    def float(self):  # @ReservedAssignment
        """
        Tries to parse a number (float). Returns a string containing the
        number, or None.
        """

        return self.match(r'(\+|\-)?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?')

    def hash(self):
        """
        Matches the characters in an md5 hash, and then some.
        """

        return self.match(r'\w+')

    def word(self):
        """
        Parses a name, which may be a keyword or not.
        """

        if self.pos == self.word_cache_pos:
            self.pos = self.word_cache_newpos
            return self.word_cache

        self.word_cache_pos = self.pos
        rv = self.match(word_regexp)
        self.word_cache = rv
        self.word_cache_newpos = self.pos

        if rv:
            rv = sys.intern(rv)

        return rv

    def name(self):
        """
        This tries to parse a name. Returns the name or None.
        """

        oldpos = self.pos
        rv = self.word()

        if (rv == "r") or (rv == "u") or (rv == "ur"):
            if self.text[self.pos:self.pos + 1] in ('"', "'", "`"):
                self.pos = oldpos
                return None

        if rv in KEYWORDS:
            self.pos = oldpos
            return None

        return rv

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

        if not global_name:
            # .local label
            if not self.match(r'\.') or not self.global_label:
                self.pos = old_pos
                return None
            global_name = self.global_label
            local_name = self.name()
            if not local_name:
                self.pos = old_pos
                return None
        else:
            if self.match(r'\.'):
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

    def image_name_component(self):
        """
        Matches a word that is a component of an image name. (These are
        strings of numbers, letters, and underscores.)
        """

        oldpos = self.pos
        rv = self.match(image_word_regexp)

        if (rv == "r") or (rv == "u"):
            if self.text[self.pos:self.pos + 1] in ('"', "'", "`"):
                self.pos = oldpos
                return None

        if (rv in KEYWORDS) or (rv in IMAGE_KEYWORDS):
            self.pos = oldpos
            return None

        return rv

    def python_string(self):
        """
        This tries to match a python string at the current
        location. If it matches, it returns True, and the current
        position is updated to the end of the string. Otherwise,
        returns False.
        """

        if self.eol():
            return False

        old_pos = self.pos

        # Delimiter.
        start = self.match(r'[urfURF]*("""|\'\'\'|"|\')')

        if not start:
            self.pos = old_pos
            return False

        delim = start.lstrip('urfURF')

        # String contents.
        while True:
            if self.eol():
                self.error("end of line reached while parsing string.")

            if self.match(delim):
                break

            if self.match(r'\\'):
                self.pos += 1
                continue

            self.match(r'.[^\'"\\]*')

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

        while self.match(r'\.'):
            n = self.name()
            if not n:
                self.error('expecting name.')

            rv += "." + n

        return rv

    def expr(self, s, expr):
        if not expr:
            return s

        return renpy.ast.PyExpr(s, self.filename, self.number)

    def delimited_python(self, delim, expr=True):
        """
        This matches python code up to, but not including, the non-whitespace
        delimiter characters. Returns a string containing the matched code,
        which may be empty if the first thing is the delimiter. Raises an
        error if EOL is reached before the delimiter.
        """

        start = self.pos

        while not self.eol():

            c = self.text[self.pos]

            if c in delim:
                return self.expr(self.text[start:self.pos], expr)

            if c in "'\"":
                self.python_string()
                continue

            if self.parenthesised_python():
                continue

            self.pos += 1

        self.error("reached end of line when expecting '%s'." % delim)

    def python_expression(self, expr=True):
        """
        Returns a python expression, which is arbitrary python code
        extending to a colon.
        """

        pe = self.delimited_python(':', False)

        if not pe:
            self.error("expected python_expression")

        rv = self.expr(pe.strip(), expr)  # E1101

        return rv

    def parenthesised_python(self):
        """
        Tries to match a parenthesised python expression. If it can,
        returns true and updates the current position to be after the
        closing parenthesis. Returns False otherwise.
        """

        c = self.text[self.pos]

        if c == '(':
            self.pos += 1
            self.delimited_python(')', False)
            self.pos += 1
            return True

        if c == '[':
            self.pos += 1
            self.delimited_python(']', False)
            self.pos += 1
            return True

        if c == '{':
            self.pos += 1
            self.delimited_python('}', False)
            self.pos += 1
            return True

        return False

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

        start = self.pos

        if image:
            def lex_name():
                oldpos = self.pos
                n = self.name()
                if n in IMAGE_KEYWORDS:
                    self.pos = oldpos
                    return None

                return n
        else:
            lex_name = self.name

        # Operator.
        while True:

            while self.match(operator_regexp):
                pass

            if self.eol():
                break

            # We start with either a name, a python_string, or parenthesized
            # python
            if not (self.python_string() or
                    lex_name() or
                    self.float() or
                    self.parenthesised_python()):

                break

            while True:
                self.skip_whitespace()

                if self.eol():
                    break

                # If we see a dot, expect a dotted name.
                if self.match(r'\.'):
                    n = self.word()
                    if not n:
                        self.error("expecting name after dot.")

                    continue

                # Otherwise, try matching parenthesised python.
                if self.parenthesised_python():
                    continue

                break

            if operator and self.match(operator_regexp):
                continue

            if comma and self.match(r','):
                continue

            break

        text = self.text[start:self.pos].strip()

        if not text:
            return None

        return renpy.ast.PyExpr(text, self.filename, self.number)

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

    _Checkpoint: TypeAlias = tuple[int, int, Any]

    def checkpoint(self) -> _Checkpoint:
        """
        Returns an opaque representation of the lexer state. This can be
        passed to revert to back the lexer up.
        """

        return self._line_index, self.pos, renpy.ast.PyExpr.checkpoint()

    def revert(self, state: _Checkpoint):
        """
        Reverts the lexer to the given state. State must have been returned
        by a previous checkpoint operation on this lexer.
        """

        self._line_index, self.pos, pyexpr_checkpoint = state
        self._line, self._subblock = self.block[self._line_index]

        renpy.ast.PyExpr.revert(pyexpr_checkpoint)

        self.word_cache_pos = -1
        if self._line_index < len(self.block):
            self.eob = False
        else:
            self.eob = True

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

        if isinstance(thing, bytes):
            thing = thing.decode("utf-8")

        if isinstance(thing, str):
            name = name or thing
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

        self.skip_whitespace()

        pos = self.pos
        self.pos = len(self.text)
        return renpy.ast.PyExpr(self.text[pos:].strip(), self.filename, self.number)

    def rest_statement(self):
        """
        Like rest, but returns a string rather than a PyExpr.
        """

        pos = self.pos
        self.pos = len(self.text)
        return self.text[pos:].strip()

    def _process_python_block(self, block, indent, rv, line_holder):
        for (_fn, ln, text), subblock in block:

            while line_holder.line < ln:
                rv.append(indent + '\n')
                line_holder.line += 1

            linetext = indent + text + '\n'

            rv.append(linetext)
            line_holder.line += linetext.count('\n')

            self._process_python_block(subblock, indent + '    ', rv, line_holder)

    def python_block(self):
        """
        Returns the subblock of this code, and subblocks of that
        subblock, as indented python code. This tries to insert
        whitespace to ensure line numbers match up.
        """

        rv = []

        line_holder = LineNumberHolder()
        line_holder.line = self.number

        self._process_python_block(self.subblock, '', rv, line_holder)
        return ''.join(rv)

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
            block = [block]

        sp = SubParse(block)
        self.subparses.append(sp)

        return sp

    def renpy_block(self, empty=False):

        if self.subparses is None:
            raise Exception("A renpy_block can only be parsed inside a creator-defined statement.")

        if self._line_index < 0:
            self.advance()

        block = []

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
