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


from typing import Any, Callable, Iterator, NamedTuple, LiteralString, cast

import os
import re
import contextlib
import functools

import renpy

from renpy.tokenizer import (
    Line,
    TokenKind,
    Tokenizer,
    TOKEN_VALUE_TO_OP,
    NEWLINE,
    NAME,
    KEYWORD,
    IDENTIFIER,
    NUMBER,
    FLOAT,
    INT,
    STRING,
    RAW_TRIPLE_STRING,
    TRIPLE_STRING,
    RAW_SINGLE_STRING,
    SINGLE_STRING,
    SPACESHIP,
    LPAR,
    RPAR,
    LSQB,
    RSQB,
    COLON,
    COMMA,
    PLUS,
    MINUS,
    STAR,
    SLASH,
    VBAR,
    AMPER,
    LESS,
    GREATER,
    DOT,
    PERCENT,
    LBRACE,
    RBRACE,
    EQEQUAL,
    NOTEQUAL,
    LESSEQUAL,
    GREATEREQUAL,
    TILDE,
    CIRCUMFLEX,
    LEFTSHIFT,
    RIGHTSHIFT,
    DOUBLESTAR,
    DOUBLESLASH,
    AT,
)


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

type LegacyLexerBlock = list[tuple[str, int, str, LegacyLexerBlock]]

class Lexer:
    """
    The lexer that is used to lex script files. This works on the idea
    that we want to lex each line in a block individually, and use
    sub-lexers to lex sub-blocks.
    """

    def __init__(
        self,
        block: list[Line] | LegacyLexerBlock,
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

        # Convert pre 8.4 list of grouped logical lines to
        # tokenized list of Line's.
        if block and not isinstance(block[0], Line):
            block = cast("LegacyLexerBlock", block)

            # 'block' here is a pre 8.4 way to represent Lexer subblock -
            # list of (filename, linenumber, line, line subblock) tuples.
            # We reconstruct source code from this and then tokenize it,
            # as if it were read from a file, and pass it to parse function.
            # This _may_ have incorrect line numbers and column offsets.

            filename = block[0][0]
            start_lineno = last_lineno = block[0][1]
            queue = [
                (0, linenumber, line, subblock)
                for (_, linenumber, line, subblock)
                in reversed(block)]

            lines = []
            while queue:
                indent_depth, linenumber, line, subblock = queue.pop()

                for _ in range(linenumber - last_lineno):
                    lines.append("\n")
                last_lineno = linenumber

                lines.append(" " * indent_depth)
                lines.append(line)

                for _, linenumber, line, subblock in reversed(subblock):
                    queue.append((indent_depth + 4, linenumber, line, subblock))

            # Source code should already have newlines at the end.
            tok = Tokenizer.from_string(
                "".join(lines),
                filename,
                lineno_offset=start_lineno - 1)

            block = list(tok.logical_lines())

        # List of lines that make up this indentation block.
        self._block = cast("list[Line]", block)

        # Index of current logical line in block.
        # Should change only by advace/unadvance.
        # -1 means we are before the first line.
        self._line_index: int = -1

        # Line instance of current logical line or None if before the first
        # line, or after the last line.
        self._line: Line | None = None

        # Index of current token in tokens, or None if at end of line.
        self._token_index: int | None = None

        # Position of 'cursor' in the line.
        # Most often it is equal to tokens_keys[token_index], but it can be
        # different if the cursor is in the middle of a token after match_regexp.
        self._pos: int = 0

        # Munged str value of self._line
        self.text: str = ""

    @classmethod
    def from_string(
        cls,
        source: str,
        filename: str,
        lineno_offset=0,
        init=False,
        init_offset=0,
    ):
        """
        Tokenizes a string and creates a Lexer object from results logical
        lines.
        """

        tok = Tokenizer.from_string(
            source,
            filename,
            lineno_offset=lineno_offset)

        return Lexer(
            list(tok.logical_lines()),
            init=init,
            init_offset=init_offset,
        )

    def __reduce__(self):
        raise TypeError("Can't pickle Lexer instance.")

    @staticmethod
    def _get_munged_string(filename: str, string: str) -> str:
        if "__" not in string:
            return string

        prefix = munge_filename(filename)

        if renpy.config.munge_in_strings:

            munge_regexp = re.compile(r'\b__(\w+)')

            def munge_string(m: re.Match):

                g1 = m.group(1)

                if "__" in g1:
                    return m.group(0)

                if g1.startswith("_"):
                    return m.group(0)

                return prefix + m.group(1)

        else:

            munge_regexp = re.compile(r'(\.|\[+)__(\w+)')

            def munge_string(m: re.Match):
                brackets = m.group(1)

                if (len(brackets) & 1) == 0:
                    return m.group(0)

                if "__" in m.group(2):
                    return m.group(0)

                return brackets + prefix + m.group(2)

        return munge_regexp.sub(munge_string, string)

    def _update_line(self, idx: int):
        self._line_index = idx
        self._line = line = self._block[idx]
        self._token_index = 0
        self._pos = 0

        text = self._get_munged_string(self.filename, line)
        if line is text:
            # No munging occurred, offsets are correct,
            # just make sure text is str, not Line.
            self.text = str(text)
            return

        # Вместо токенизации нужно проходится по всей строке и мунжить _токены_,
        # но оставлять позиции токенов неизменными. Если токен мунжится, можно
        # вычислить байас оффсета для следующих токенов.
        # Также в питон нужно передавать не мунженный текст и делать замену
        # на уровне AST а не исходного кода. Так в трейсбеках будет правильно
        # отображаться исходный код с позициями токенов.

        # Otherwise we need to fix up the offsets, retokenize munged text.
        # It should return the same tokens, but with correct offsets.
        tok = Tokenizer.from_string(text, line.filename)
        self._line = next(tok.logical_lines())
        self._line.indent_size = line.indent_size
        self.text = text

    @property
    def _mid_token(self):
        idx = self._token_index
        if idx is None:
            return False

        return self._pos != self._line.offsets[idx]

    @property
    def _current_token(self):
        if self._token_index is None:
            return None

        return self._line.tokens[self._token_index]

    def _advance_token(self):
        if self._token_index is None:
            return

        self._token_index += 1
        if self._token_index >= len(self._line.tokens):
            self._pos = len(self.text)
            self._token_index = None
        else:
            self._pos = self._line.offsets[self._token_index]

    def _yield_subblock_lines(self) -> Iterator[Line]:
        if self._line is None:
            return

        idx = self._line_index + 1
        depth = self._line.indent_size
        while idx < len(self._block):
            l = self._block[idx]
            if l.indent_size > depth:
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
            self._pos = value
            for i, p in enumerate(self._line.offsets):
                if p >= value:
                    self._token_index = i
                    return

            # Value is greater than all offsets, i.e. it is mid-token
            # in last token.
            self._token_index = len(self._line.tokens) - 1

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

        return self._line.physical_location.start_lineno

    @property
    def eob(self):
        return self._line_index > len(self._block)

    def eol(self):
        """
        Returns True if, after skipping whitespace, the current
        position is at the end of the end of the current line, or
        False otherwise.
        """

        if self._lookup_token(NEWLINE):
            self._advance_token()

        return self._token_index is None

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
        depth = self._block[0].indent_size

        while (idx := idx + 1) < block_len:
            line = self._block[idx]
            if line.indent_size == depth:
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
        depth = self._line.indent_size
        while (idx := idx - 1) >= 0:
            line = self._block[idx]
            if line.indent_size == depth:
                break
        else:
            self._line_index = 0
            return

        self._update_line(idx)
        self.pos = len(self.text)

    # The regexes that match single operator.
    _OP_REGEX = TOKEN_VALUE_TO_OP.copy()

    # Ditto, but escaped.
    _OP_REGEX |= {re.escape(k): v for k, v in TOKEN_VALUE_TO_OP.items()}

    def match_regexp(self, regexp: LiteralString):
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

        # Fast path for single operator checks.
        if regexp in self._OP_REGEX and not self._mid_token:
            kind = self._OP_REGEX[regexp]
            if (tok := self._lookup_exact_token(kind)) is None:
                return None

            self._advance_token()
            return tok.string

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

        pos = self._pos
        text = self.text
        len_text = len(text)
        while pos < len_text:
            c = text[pos]
            if c == " " or c == "\n":
                pos += 1

            elif c == "\\" and text[pos + 1] == "\n":
                pos += 2

            else:
                break

        self.pos = pos

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

    def _lookup_token(self, kind: TokenKind | None = None):
        self.skip_whitespace()
        if self._mid_token:
            return None

        current_token = self._current_token
        if current_token is None:
            return None

        if kind is None:
            return current_token

        if current_token.kind is TokenKind(kind):
            return current_token
        else:
            return None

    def _lookup_exact_token(self, kind: TokenKind):
        self.skip_whitespace()
        if self._mid_token:
            return None

        current_token = self._current_token
        if current_token is None:
            return None

        if current_token.exact_kind is TokenKind(kind):
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

        tok = self._lookup_exact_token(RAW_SINGLE_STRING)
        if tok is None:
            tok = self._lookup_exact_token(SINGLE_STRING)
            raw = False
        else:
            raw = True

        if tok is None:
            return None

        self._advance_token()

        s = self._get_munged_string(tok.filename, tok.string)

        # Strip mods and quotes.
        for i, c in enumerate(s):
            if c in "\"'`":
                s = s[i + 1:-1]
                break

        if raw:
            return s

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

        tok = self._lookup_exact_token(RAW_TRIPLE_STRING)
        if tok is None:
            tok = self._lookup_exact_token(TRIPLE_STRING)
            raw = False
        else:
            raw = True

        if tok is None:
            return None

        self._advance_token()

        s = self._get_munged_string(tok.filename, tok.string)

        # Strip mods and quotes.
        for i, c in enumerate(s):
            if c in "\"'`":
                s = s[i + 3:-3]
                break

        if raw:
            return s

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
        if tok.exact_kind is PLUS:
            self._advance_token()
            rv = "+"
        elif tok.exact_kind is MINUS:
            self._advance_token()
            rv = "-"
        else:
            rv = ""

        tok = self._lookup_exact_token(INT)
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
        if tok.exact_kind is PLUS:
            self._advance_token()
            rv = "+"
        elif tok.exact_kind is MINUS:
            self._advance_token()
            rv = "-"
        else:
            rv = ""

        tok = self._lookup_exact_token(FLOAT)
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

        tok = self._lookup_token(NAME)
        if tok is None:
            return None
        else:
            self._advance_token()
            return tok.string

    def word(self):
        """
        Parses a name, which may be a keyword or not.
        """

        tok = self._lookup_token(NAME)
        if tok is None:
            return None
        else:
            self._advance_token()
            return tok.string

    def name(self):
        """
        This tries to parse a name. Returns the name or None.
        """

        tok = self._lookup_token()
        if tok is None:
            return None

        if tok.exact_kind is IDENTIFIER:
            self._advance_token()
            return self._get_munged_string(tok.filename, tok.string)

        # Constants are names in old parser.
        if tok.exact_kind is KEYWORD:
            if tok.string in ("True", "False", "None"):
                self._advance_token()
                return tok.string

        return None

    def image_name_component(self):
        """
        Matches a word that is a component of an image name. (These are
        strings of numbers, letters, and underscores.)
        """

        tok = self._lookup_token()
        if tok is None:
            return None

        if tok.kind is NAME:
            pass
        # All digits except those with dot or +- are valid.
        elif tok.kind is NUMBER and tok.string.isalnum():
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
        return self._get_munged_string(tok.filename, tok.string)

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

        dot = bool(self._lookup_exact_token(DOT))
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

        tok = self._lookup_token(STRING)
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

        while self._lookup_exact_token(DOT):
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

    def _delimited_python(self, delim: TokenKind):
        while (tok := self._lookup_token()) is not None:
            if tok.exact_kind is delim:
                return True

            if self.python_string():
                continue

            if self.parenthesised_python():
                continue

            self._advance_token()

        return False

    def delimited_python(self, delim: LiteralString, expr=True):
        """
        This matches python code up to, but not including, the non-whitespace
        delimiter characters. Returns a string containing the matched code,
        which may be empty if the first thing is the delimiter. Raises an
        error if EOL is reached before the delimiter.
        """

        start = self.pos
        if delim in self._OP_REGEX:
            if self._delimited_python(self._OP_REGEX[delim]):
                return self.expr(self.text[start:self.pos], expr)
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

        start = self.pos

        if self.filename.endswith("inventory/rcode.rpy"):
            print(repr(self._line))
            print(repr(self.text[start:]))

        if not self._delimited_python(COLON):
            self.error("expected python_expression")

        return self.expr(self.text[start:self.pos].strip(), expr)

    def parenthesised_python(self):
        """
        Tries to match a parenthesised python expression. If it can,
        returns true and updates the current position to be after the
        closing parenthesis. Returns False otherwise.
        """

        tok = self._lookup_token()
        if tok is None:
            return False

        if tok.exact_kind is LPAR:
            self._advance_token()
            self._delimited_python(RPAR)
            self._advance_token()
            return True
        elif tok.exact_kind is LSQB:
            self._advance_token()
            self._delimited_python(RSQB)
            self._advance_token()
            return True
        elif tok.exact_kind is LBRACE:
            self._advance_token()
            self._delimited_python(RBRACE)
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
        if tok.kind is STRING:
            self._advance_token()
            return True

        if tok.kind is NUMBER:
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
            if tok.exact_kind is DOT:
                self._advance_token()
                if not self._simple_expression_func():
                    self.error("expecting name after dot.")
            # subscription | slicing ::= primary "[" expression "]"
            elif tok.exact_kind is LSQB:
                self._advance_token()
                self._delimited_python(RSQB)
                self._advance_token()
            # call ::= primary "(" [argument_list] ")"
            elif tok.exact_kind is LPAR:
                self._advance_token()
                self._delimited_python(RPAR)
                self._advance_token()
            else:
                break

        return True

    def _u_expr(self):
        # https://docs.python.org/3/reference/expressions.html#grammar-token-python-grammar-u_expr
        while tok := self._lookup_token():
            # "~" u_expr
            if tok.exact_kind is TILDE:
                self._advance_token()
            # "+" u_expr
            elif tok.exact_kind is PLUS:
                self._advance_token()
            # "-" u_expr
            elif tok.exact_kind is MINUS:
                self._advance_token()
            # "not" u_expr
            elif tok.exact_kind is KEYWORD and tok.string == "not":
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
            SPACESHIP,
            PLUS,
            MINUS,
            STAR,
            SLASH,
            VBAR,
            AMPER,
            LESS,
            GREATER,
            PERCENT,
            EQEQUAL,
            NOTEQUAL,
            LESSEQUAL,
            GREATEREQUAL,
            CIRCUMFLEX,
            LEFTSHIFT,
            RIGHTSHIFT,
            DOUBLESTAR,
            DOUBLESLASH,
            AT,
        )
        while tok := self._lookup_token():
            ename = tok.exact_kind
            # "and" u_expr
            if ename is KEYWORD and tok.string == "and":
                pass
            # "or" u_expr
            elif ename is KEYWORD and tok.string == "or":
                pass
            # "is" u_expr
            # 'not' here is part of u_expr
            elif ename is KEYWORD and tok.string == "is":
                pass
            # "in" u_expr
            elif ename is KEYWORD and tok.string == "in":
                pass
            # "not in" u_expr
            elif ename is KEYWORD and tok.string == "not":
                self._advance_token()
                if not (
                    (tok2 := self._lookup_token()) and
                    tok2.exact_kind is KEYWORD and
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

            if comma and self._lookup_exact_token(COMMA):
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

        if line_index != self._line_index:
            try:
                self._update_line(line_index)
            except Exception:
                exc = Exception("Revert outsite of this lexer.")
                exc.add_note("Are you sure you revert the same "
                             "lexer that you checkpointed?")
                raise exc

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

        self.skip_whitespace()

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

        result: list[str] = []

        prev_row = self._line.physical_location.end_lineno + 1
        base_indent = None
        for line in self._yield_subblock_lines():
            if delta := line.physical_location.start_lineno - prev_row:
                result.append("\n" * delta)
            prev_row = line.physical_location.end_lineno

            if base_indent is None:
                base_indent = line.indent_size
            elif delta := line.indent_size - base_indent:
                result.append(" " * delta)

            result.append(self._get_munged_string(
                line.filename, line))

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
