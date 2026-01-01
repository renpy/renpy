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


from typing import TYPE_CHECKING, Callable, NamedTuple

import io
import re
import sys
import os
import contextlib
import functools
import linecache

import renpy


def match_logical_word(s: str, pos: int) -> tuple[str, bool, int]: ...
def make_pyexpr(s: str, filename: str, linenumber: int, column: int, text: str, pos: int) -> "renpy.ast.PyExpr": ...


if not TYPE_CHECKING:
    # If Ren'Py is run with system Python, we can't import cython functions.
    try:
        from renpy.lexersupport import match_logical_word
        from renpy.astsupport import make_pyexpr
    except ImportError:
        pass


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
        super().__init__(message, (unicode_filename(filename), lineno, offset, text, end_lineno, end_offset))

    @property
    def message(self) -> str:
        """
        Fully formatted message of the error close to the result of
        `traceback.format_exception_only`.
        """
        if self._message is None:
            filename = self.filename or "<string>"
            lineno = self.lineno or 1
            message = f'File "{filename}", line {lineno}: {self.msg}'
            if self.text is not None:
                # Neither Python nor this class does not support multiline syntax error code.
                # Just strip the first line of provided code.
                text = self.text.split("\n")[0]

                # Remove ending escape chars, so we can render it.
                text = text.rstrip()

                # And also replace any escape chars at the start with an indent.
                message += f"\n    {text.lstrip()}"

                if self.offset is not None:
                    from renpy.error import normalize_renpy_line_offset

                    offset = normalize_renpy_line_offset(filename, lineno, self.offset, self.text)

                    # Fallback to single caret for cases end_offset is before offset.
                    if self.end_offset is None or self.end_offset <= offset:
                        end_offset = offset + 1
                    else:
                        end_offset = normalize_renpy_line_offset(
                            filename, self.end_lineno or lineno, self.end_offset, self.text
                        )

                    left_spaces = len(text) - len(text.lstrip())
                    offset -= left_spaces
                    end_offset -= left_spaces

                    if offset >= 0:
                        caret_space = " " * (offset - 1)
                        carets = "^" * (end_offset - offset)
                        message += f"\n    {caret_space}{carets}"

            for note in getattr(self, "__notes__", ()):
                message += f"\n{note}"

            self._message = message

        return self._message

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


# Matches either a word, or something else. Most magic is taken care of
# before this.
lllword = re.compile(r"__(\w+)|\w+| +|.", re.S)


def munge_filename(fn):
    # The prefix that's used when __ is found in the file.
    rv = os.path.basename(fn)

    if rv.endswith("_ren.py"):
        rv = rv[:-7]

    rv = os.path.splitext(rv)[0]
    rv = rv.replace(" ", "_")

    def munge_char(m):
        return hex(ord(m.group(0)))

    rv = re.sub(r"[^a-zA-Z0-9_]", munge_char, rv)

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
            rv = fn[len(d) :]
            break
    else:
        rv = fn

    return rv


def unelide_filename(fn: str) -> str:
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

        return functools.partial(re.sub, r"\b__(\w+)", munge_string)

    else:

        def munge_string(m: re.Match[str]):
            brackets = m.group(1)

            if len(brackets) % 2 == 0:
                return m.group(0)

            if "__" in m.group(2):
                return m.group(0)

            return brackets + prefix + m.group(2)

        return functools.partial(re.sub, r"(\.|\[+)__(\w+)", munge_string)


# The filename that the start and end positions are relative to.
original_filename = ""

# Matches one operator that contains special characters.
_ANY_OPERATOR_REGEX = re.compile(
    "|".join(
        re.escape(i)
        for i in (
            "//=",
            ">>=",
            "<<=",
            "**=",
            "+=",
            "-=",
            "*=",
            "/=",
            "%=",
            "@=",
            "&=",
            "|=",
            "^=",
            "//",
            ">>",
            "<<",
            "**",
            "+",
            "-",
            "*",
            "/",
            "%",
            "@",
            "&",
            "|",
            "^",
            ":=",
            "<=",
            ">=",
            "==",
            "->",
            "!=",
            ",",
            ":",
            "!",
            ".",
            ";",
            "=",
            "~",
            "<",
            ">",
            "$",
            "?",
        )
    )
)


def list_logical_lines(
    filename: str,
    filedata: str | None = None,
    linenumber: int = 1,
) -> list[tuple[str, int, str]]:
    """
    Reads `filename`, and divides it into logical lines.

    Returns a list of (filename, line number, line text) triples.

    If `filedata` is given, it should be a unicode string giving the file
    contents. In that case, `filename` need not exist.
    """

    global original_filename

    original_filename = filename

    filename = elide_filename(filename)
    prefix = munge_filename(filename)

    munge_string = get_string_munger(prefix)

    # Convert windows and mac newlines to \n, so we don't have to worry about it.
    if filedata is not None:
        data_io = io.StringIO(filedata, None)
    else:
        data_io = open(original_filename, "r", encoding="utf-8")

    with data_io:
        data = data_io.read()

    if filename.endswith("_ren.py"):
        data = ren_py_to_rpy(data, filename)

    # Add couple empty lines, so we can safely check for pos + 2 for triple-string.
    data += "\n\n"

    # The current position we're looking at in the buffer.
    pos = 0

    # Skip the BOM, if any.
    if data[0] == "\ufeff":
        pos += 1

    # Result tuples of (string, start line number, start pos, end pos).
    rv: list[tuple[str, int, int, int]] = []

    # The line number in the physical file.
    number = linenumber

    len_data = len(data)

    # The line number of the start of this logical line.
    start_number = 0

    # The line that we're building up.
    line: list[str] = []

    # Stack of open paren (char, line number, column) tuples.
    open_parens: list[tuple[str, int, int]] = []

    # Position at the beginning of current physical line.
    # This is used to calculate column offset by pos - line_start_pos.
    line_startpos = pos

    # The starting position of the current logical line.
    startpos = pos

    # The ending position of the current logical line without comment and whitespace/newline
    # or None if the same as pos.
    endpos = None

    # Matches any amount of blank lines, comment-only lines, and backslash-newlines.
    ignore_regex = re.compile(r"""(?:\ *\n|\ *\#[^\n]*\n|\ *\\\n)*""")

    operator_regex = _ANY_OPERATOR_REGEX

    # Looping over whole file to find logical lines.
    while match := ignore_regex.match(data, pos):
        pos = match.end()

        if pos >= len_data:
            break

        number += match[0].count("\n")

        start_number = number
        line_startpos = pos
        startpos = pos
        endpos = None
        line.clear()

        # Looping over parts of single logical line.
        while True:
            try:
                c = data[pos]
            except IndexError:
                # This can happen only if we have unclosed parens.
                c, lineno, column = open_parens[-1]
                raise ParseError(
                    f"'{c}' was never closed", filename, lineno, column + 1, linecache.getline(filename, lineno)
                )

            # Name and runs of spaces are the most common cases, so it's first.
            if c in " _" or c.isalnum():
                word, magic, end = match_logical_word(data, pos)

                if magic and word[2] != "_":
                    rest = word[2:]

                    if "__" not in rest:
                        word = prefix + rest

                line.append(word)
                pos = end
                continue

            # Strings are second common case.
            if c in "\"'`":
                string_startpos = pos

                # Compute quote size.
                if data[pos + 1] == c:
                    if data[pos + 2] == c:
                        pos += 3
                        quote_size = 3
                    else:
                        # Empty string.
                        pos += 2
                        line.append(f"{c}{c}")
                        continue
                else:
                    pos += 1
                    quote_size = 1

                quote = c

                end_quote_size = 0
                c = data[pos]
                while end_quote_size != quote_size:
                    # Skip escaped char.
                    while c == "\\":
                        end_quote_size = 0
                        pos += 2
                        c = data[pos]

                    pos += 1

                    if c == "\n":
                        end_quote_size = 0
                        line_startpos = pos
                        number += 1

                    elif c == quote:
                        end_quote_size += 1
                    else:
                        end_quote_size = 0

                    # TODO: disallow same quote nested f-strings.

                    try:
                        c = data[pos]
                    except IndexError:
                        raise ParseError(
                            "unterminated string literal",
                            filename,
                            start_number,
                            text=linecache.getline(filename, start_number),
                        )

                s = data[string_startpos:pos]
                if "__" in s:
                    s = munge_string(s)

                line.append(s)

                continue

            # Operator.
            if match := operator_regex.match(data, pos):
                line.append(match[0])
                pos = match.end()
                continue

            # Newline.
            if c == "\n":
                if open_parens:
                    line.append("\n")
                    pos += 1
                    number += 1
                    line_startpos = pos
                    endpos = None
                    continue

                rv_line = "".join(line)

                if not rv_line.strip():
                    raise Exception(f"{filename}:{start_number}:{startpos} empty line")

                # Add to the results.
                rv.append((rv_line, start_number, startpos, endpos or pos))
                break

            # Parenthesis.
            if c in "([{":
                open_parens.append((c, number, pos - line_startpos))
                line.append(c)
                pos += 1
                continue

            elif c in "}])":
                if not open_parens:
                    raise ParseError(
                        f"unmatched '{c}'",
                        filename,
                        number,
                        pos - line_startpos + 1,
                        linecache.getline(filename, number),
                    )

                open_c, _, _ = open_parens.pop()

                if not (c == ")" and open_c == "(" or c == "]" and open_c == "[" or c == "}" and open_c == "{"):
                    raise ParseError(
                        f"closing parenthesis '{c}' does not match opening parenthesis '{open_c}'",
                        filename,
                        number,
                        pos - line_startpos + 1,
                        linecache.getline(filename, number),
                    )

                line.append(c)
                pos += 1
                continue

            # Comments.
            if c == "#":
                endpos = pos

                pos = data.index("\n", pos)
                continue

            # Backslash/newline.
            if c == "\\" and data[pos + 1] == "\n":
                pos += 2
                number += 1
                line_startpos = pos
                line.append("\\\n")
                continue

            if c == "\t":
                raise ParseError(
                    "Tab characters are not allowed in Ren'Py scripts.",
                    filename,
                    number,
                    text=linecache.getline(filename, number),
                )

            # Some kind of non alpha-numeric character outside of ASCII range.
            else:
                line.append(c)
                pos += 1

    return [(filename, number, line) for line, number, _, _ in rv]


class GroupedLine(NamedTuple):
    # The filename the line is from.
    filename: str
    number: int
    indent: int
    text: str
    block: list["GroupedLine"]


def group_logical_lines(lines: list[tuple[str, int, str]]) -> list[GroupedLine]:
    """
    This takes as input the list of logical line triples output from
    list_logical_lines, and breaks the lines into blocks. Each block
    is represented as a list of (filename, line number, starting column, line text,
    block) tuples, where block is a block list (which may be empty if
    no block is associated with this line.)
    """

    if not lines:
        return []

    filename, number, text = lines[0]

    if text.startswith(" "):
        raise ParseError("Unexpected indentation at start of file.", filename, number, text=text)

    stack: list[tuple[int, list[GroupedLine]]] = [(0, [])]
    block_indent, block = stack[-1]

    for filename, number, text in lines:
        rest = text.lstrip(" ")
        indent = len(text) - len(rest)

        # Indent.
        if indent > block_indent:
            block_indent = indent
            block = block[-1].block
            stack.append((block_indent, block))

        # Dedent.
        elif indent < block_indent:
            stack.pop()  # Safe because indent can't be less than 0, so stack is never empty.
            while stack:
                block_indent, block = stack[-1]
                if indent == block_indent:
                    break

                stack.pop()

            else:
                raise ParseError("Indentation mismatch.", filename, number, text=text)

        block.append(GroupedLine(filename, number, indent, rest, []))

    return stack[0][1]


# A list of keywords which should not be parsed as names, because
# there is a huge chance of confusion.
#
# Note: We need to be careful with what's in here, because these
# are banned in simple_expressions, where we might want to use
# some of them.
KEYWORDS = {
    "as",
    "if",
    "in",
    "return",
    "with",
    "while",
}

IMAGE_KEYWORDS = {
    "behind",
    "at",
    "onlayer",
    "with",
    "zorder",
    "transform",
}

OPERATORS = [
    "<>",
    "<<",
    "<=",
    "<",
    ">>",
    ">=",
    ">",
    "!=",
    "==",
    "|",
    "^",
    "&",
    "+",
    "-",
    "**",
    "*",
    "//",
    "/",
    "%",
    "~",
    "@",
    ":=",
]

ESCAPED_OPERATORS = [
    r"\bor\b",
    r"\band\b",
    r"\bnot\b",
    r"\bin\b",
    r"\bis\b",
]

operator_regexp = "|".join([re.escape(i) for i in OPERATORS] + ESCAPED_OPERATORS)

word_regexp = r"[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*"
image_word_regexp = r"[-0-9a-zA-Z_\u00a0-\ufffd][-0-9a-zA-Z_\u00a0-\ufffd]*"


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

    block: list[GroupedLine]

    def __init__(self, block, init=False, init_offset=0, global_label=None, monologue_delimiter="\n\n", subparses=None):
        # Older version of Lexer had block being a list of tuples. Those lists can be found in UserStatements,
        # and so need to be upgraded.
        if block and not isinstance(block[0], GroupedLine):
            block = [GroupedLine(filename, line, 0, text, subblock) for filename, line, text, subblock in block]

        # Are we underneath an init block?
        self.init = init

        # The priority of the init block we're in, if any.
        self.init_priority = 0

        # The priority of auto-defined init statements.
        self.init_offset = init_offset

        self.block = block
        self.eob = False

        self.line = -1

        # These are set by advance.
        self.filename = ""
        self.text = ""
        self.number = 0
        self.subblock = []
        self.global_label = global_label
        self.pos = 0
        self.word_cache_pos = -1
        self.word_cache_newpos = -1
        self.word_cache = ""

        # The column text starts at.
        self.column = 0

        self.monologue_delimiter = monologue_delimiter

        self.subparses = subparses

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

        self.line += 1

        if self.line >= len(self.block):
            self.eob = True
            return False

        self.filename, self.number, self.column, self.text, self.subblock = self.block[self.line]
        self.pos = 0
        self.word_cache_pos = -1

        return True

    def unadvance(self):
        """
        Puts the parsing point at the end of the previous line. This is used
        after renpy_statement to prevent the advance that Ren'Py statements
        do.
        """

        self.line -= 1
        self.eob = False
        self.filename, self.number, self.column, self.text, self.subblock = self.block[self.line]
        self.pos = len(self.text)
        self.word_cache_pos = -1

    def match_regexp(self, regexp):
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

        m = re.compile(regexp, re.DOTALL).match(self.text, self.pos)

        if not m:
            return None

        self.pos = m.end()

        return m.group(0)

    def skip_whitespace(self):
        """
        Advances the current position beyond any contiguous whitespace.
        """

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
        return ""

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

        if (self.line == -1) and self.block:
            self.filename, self.number, self.column, self.text, self.subblock = self.block[0]

        raise ParseError(msg, self.filename, self.number, self.pos + 1, self.text)

    def deferred_error(self, queue, msg):
        """
        Adds a deferred error to the given queue. This is used for something
        that might be an error, but could be compat-ed away.

        `queue`
            A string giving a list of deferred errors to add to.
        """

        if (self.line == -1) and self.block:
            self.filename, self.number, self.column, self.text, self.subblock = self.block[0]

        ParseError(msg, self.filename, self.number, self.pos + 1, self.text).defer(queue)

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
            self.error("end of line expected.")

    def expect_noblock(self, stmt):
        """
        Called to indicate this statement does not expect a block.
        If a block is found, raises an error.
        """

        if self.subblock:
            ll = self.subblock_lexer()
            ll.advance()
            ll.error(
                "Line is indented, but the preceding {} statement does not expect a block. "
                "Please check this line's indentation. You may have forgotten a colon (:).".format(stmt)
            )

    def expect_block(self, stmt):
        """
        Called to indicate that the statement requires that a non-empty
        block is present.
        """

        if not self.subblock:
            self.error("%s expects a non-empty block." % stmt)

    def has_block(self):
        """
        Called to check if the current line has a non-empty block.
        """
        return bool(self.subblock)

    def subblock_lexer(self, init=False):
        """
        Returns a new lexer object, equipped to parse the block
        associated with this line.
        """

        init = self.init or init

        return Lexer(
            self.subblock,
            init=init,
            init_offset=self.init_offset,
            global_label=self.global_label,
            monologue_delimiter=self.monologue_delimiter,
            subparses=self.subparses,
        )

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

        if s[0] == "r":
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
            elif c[0] == "u":
                group2 = m.group(2)

                if group2:
                    return chr(int(m.group(2), 16))
            else:
                return c

        if not raw:
            # Collapse runs of whitespace into single spaces.
            s = re.sub(r"[ \n]+", " ", s)

            s = re.sub(r"\\(u([0-9a-fA-F]{1,4})|.)", dequote, s)  # type: ignore

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

        if s[0] == "r":
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
            elif c[0] == "u":
                group2 = m.group(2)

                if group2:
                    return chr(int(m.group(2), 16))
            else:
                return c

        if not raw:
            s = re.sub(r" *\n *", "\n", s)

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
                    s = re.sub(r"[ \n]+", " ", s)
                else:
                    s = re.sub(r" +", " ", s)

                s = re.sub(r"\\(u([0-9a-fA-F]{1,4})|.)", dequote, s)  # type: ignore

                rv.append(s)

            return rv

        return s

    def integer(self):
        """
        Tries to parse an integer. Returns a string containing the
        integer, or None.
        """

        return self.match(r"(\+|\-)?\d+")

    def float(self):
        """
        Tries to parse a number (float). Returns a string containing the
        number, or None.
        """

        return self.match(r"(\+|\-)?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?")

    def hash(self):
        """
        Matches the characters in an md5 hash, and then some.
        """

        return self.match(r"\w+")

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
            if self.text[self.pos : self.pos + 1] in ('"', "'", "`"):
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
        if label and label[0] != ".":
            self.global_label = label.split(".")[0]

    def label_name(self, declare=False):
        """
        Try to parse label name. Returns name in form of "global.local" if local
        is present, "global" otherwise; or None if it doesn't parse.

        `declare`
            Unused, retained for public api compatibility.
        """

        old_pos = self.pos
        local_name = None
        global_name = self.name()

        if not global_name:
            # .local label
            if not self.match(r"\.") or not self.global_label:
                self.pos = old_pos
                return None
            global_name = self.global_label
            local_name = self.name()
            if not local_name:
                self.pos = old_pos
                return None
        else:
            if self.match(r"\."):

                local_name = self.name()
                if not local_name:
                    self.pos = old_pos
                    return None

        if not local_name:
            return global_name

        return global_name + "." + local_name

    def image_name_component(self):
        """
        Matches a word that is a component of an image name. (These are
        strings of numbers, letters, and underscores.)
        """

        oldpos = self.pos
        rv = self.match(image_word_regexp)

        if (rv == "r") or (rv == "u"):
            if self.text[self.pos : self.pos + 1] in ('"', "'", "`"):
                self.pos = oldpos
                return None

        if (rv in KEYWORDS) or (rv in IMAGE_KEYWORDS):
            self.pos = oldpos
            return None

        return rv

    def python_string(self):
        """
        This tries to match a python string at the current
        location. If it matches, it returns the string, including
        delimiters. If not, returns None.
        """

        if self.eol():
            return False

        old_pos = self.pos

        # Delimiter.
        start = self.match(r'[urfURF]*("""|\'\'\'|"|\')')

        if not start:
            self.pos = old_pos
            return None

        delim = start.lstrip("urfURF")

        # String contents.
        while True:
            if self.eol():
                self.error("end of line reached while parsing string.")

            if self.match(delim):
                break

            if self.match(r"\\"):
                self.pos += 1
                continue

            self.match(r'.[^\'"\\]*')

        return self.text[old_pos : self.pos]

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

        while self.match(r"\."):
            n = self.name()
            if not n:
                self.error("expecting name.")

            rv += "." + n

        return rv

    def expr(self, s, expr):
        if not expr:
            return s

        pos = self.pos - len(s)

        return make_pyexpr(s, self.filename, self.number, self.column, self.text, pos)

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
                return self.expr(self.text[start : self.pos], expr)

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

        pe = self.delimited_python(":", False)

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

        c = self.text[self.pos]

        if c == "(":
            self.pos += 1
            self.delimited_python(")", False)
            self.pos += 1
            return True

        if c == "[":
            self.pos += 1
            self.delimited_python("]", False)
            self.pos += 1
            return True

        if c == "{":
            self.pos += 1
            self.delimited_python("}", False)
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
            if not (self.python_string() or lex_name() or self.float() or self.parenthesised_python()):
                break

            while True:
                self.skip_whitespace()

                if self.eol():
                    break

                # If we see a dot, expect a dotted name.
                if self.match(r"\."):
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

            if comma and self.match(r","):
                continue

            break

        text = self.text[start : self.pos].strip()

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

    def checkpoint(self):
        """
        Returns an opaque representation of the lexer state. This can be
        passed to revert to back the lexer up.
        """

        return (
            self.line,
            self.filename,
            self.number,
            self.text,
            self.subblock,
            self.pos,
            self.column,
            renpy.ast.PyExpr.checkpoint(),
        )

    def revert(self, state):
        """
        Reverts the lexer to the given state. State must have been returned
        by a previous checkpoint operation on this lexer.
        """

        self.line, self.filename, self.number, self.text, self.subblock, self.pos, self.column, pyexpr_checkpoint = (
            state
        )

        renpy.ast.PyExpr.revert(pyexpr_checkpoint)

        self.word_cache_pos = -1
        if self.line < len(self.block):
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

    rest_statement = rest

    def _process_python_block(self, block, rv, line_holder):
        for _fn, ln, indent, text, subblock in block:
            prefix = " " * indent

            while line_holder.line < ln:
                rv.append(prefix + "\n")
                line_holder.line += 1

            linetext = prefix + text + "\n"

            rv.append(linetext)
            line_holder.line += linetext.count("\n")

            self._process_python_block(subblock, rv, line_holder)

    def python_block(self):
        """
        Returns the subblock of this code, and subblocks of that
        subblock, as indented python code. This tries to insert
        whitespace to ensure line numbers match up.
        """

        rv = []

        line_holder = LineNumberHolder()
        line_holder.line = self.number

        self._process_python_block(self.subblock, rv, line_holder)
        return "".join(rv)

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

        if self.line < 0:
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


def ren_py_to_rpy_offsets(lines: list[str], filename: str):
    """
    Takes a list of lines of _ren.py file, and yields a None if line of equivalent .rpy file
    should be ignored, or an integer of extra indent for that line.
    """

    current_offset = 0

    # Possible states.
    IGNORE = 0
    RENPY = 1
    PYTHON = 2

    # The state the state machine is in.
    state = IGNORE

    open_linenumber = 0

    # Remove BOM.
    if lines and lines[0] and lines[0][0] == "\ufeff":
        lines[0] = lines[0][1:]

    for linenumber, l in enumerate(lines, start=1):
        if state != RENPY:
            if l.startswith('"""renpy'):
                state = RENPY
                open_linenumber = linenumber
                yield None
                continue

        if state == RENPY:
            if l.strip() == '"""':
                yield None

                state = PYTHON
                continue

            # Ignore empty and comments.
            sl = l.strip()
            if not sl or sl[0] == "#":
                yield 0
                continue

            # Determine the prefix.
            current_offset = 0
            for i in l:
                if i != " ":
                    break
                current_offset += 1

            # If the line ends in ":", add 4 spaces to the prefix.
            # XXX: This does not work for 'init python: # Comment'...
            if sl[-1] == ":":
                current_offset += 4

            yield 0
            continue

        if state == PYTHON:
            if l == "\n":
                # Don't add spaces to empty lines to not interfere with multiline strings.
                yield 0
            else:
                yield current_offset
            continue

        if state == IGNORE:
            yield None
            continue

    if state == IGNORE:
        raise ParseError(f'There are no \'"""renpy\' blocks, so every line is ignored.', filename, open_linenumber)

    if state == RENPY:
        raise ParseError(f'\'"""renpy\' block was not terminated by """.', filename, open_linenumber)


def ren_py_to_rpy(text: str, filename: str | None) -> str:
    """
    Transforms an _ren.py file into the equivalent .rpy file. This should retain line numbers.

    `filename`
        If not None, and an error occurs, the error is reported with the given filename.
        Otherwise, errors are ignored and a best effort is used.
    """

    lines = text.splitlines()

    result = []

    # Consume as much as possible from the input
    try:
        for offset, line in zip(ren_py_to_rpy_offsets(lines, filename or "<string>"), lines):
            if offset is None:
                result.append("")
            else:
                result.append(f"{' ' * offset}{line}")

    except Exception:
        if filename is not None:
            raise

    rv = "\n".join(result)

    return rv


def lex_string(text: str, filename: str = "<string>", linenumber: int = 1, advance: bool = True) -> Lexer:
    """
    :doc: lexer

    Returns a Lexer object that can be used to lex the given text.

    `text`
        The text to lex.

    `filename`
        A filename for which errros will be reported.

    `linenumber`
        A line number for which errors will be reported.

    `advance`
        If true, the .advance() method will be called on the lexer.
    """

    lines = list_logical_lines(filename, text, linenumber)
    nested = group_logical_lines(lines)

    rv = Lexer(nested)

    if advance:
        rv.advance()

    return rv
