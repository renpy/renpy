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


from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import codecs
import re
import sys
import os
import time
import contextlib

import renpy

from renpy.lexersupport import match_logical_word

# The filename that's in the line text cache.
line_text_filename = ""

# The content of the line text cache.
line_text_cache = [ ]


def get_line_text(filename, lineno):
    """
    Gets the text of a line, in a best-effort way, for debugging purposes. May
    return just a newline, if the line doesn't exist.
    """

    global line_text_filename
    global line_text_cache

    import linecache
    full_filename = renpy.exports.unelide_filename(filename)


    if full_filename != line_text_filename:

        line_text_filename = full_filename

        try:

            with open(full_filename, "rb") as f:
                data = f.read().decode("utf-8", "python_strict")

            if full_filename.endswith("_ren.py"):
                data = ren_py_to_rpy(data, None)

            data += "\n\n"

            line_text_cache = data.split("\n")

        except Exception:
            line_text_cache = [ ]

    if lineno <= len(line_text_cache):
        return line_text_cache[lineno - 1] + "\n"
    else:
        return "\n"


class ParseError(Exception):

    def __init__(self, filename, number, msg, line=None, pos=None, first=False):
        message = u"File \"%s\", line %d: %s" % (unicode_filename(filename), number, msg)

        if line:
            if isinstance(line, list):
                line = "".join(line)

            lines = line.split('\n')

            if len(lines) > 1:
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


# Matches either a word, or something else. Most magic is taken care of
# before this.
lllword = re.compile(r'__(\w+)|\w+| +|.', re.S)


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


def list_logical_lines(filename, filedata=None, linenumber=1, add_lines=False):
    """
    Reads `filename`, and divides it into logical lines.

    Returns a list of (filename, line number, line text) triples.

    If `filedata` is given, it should be a unicode string giving the file
    contents. In that case, `filename` need not exist.
    """

    if renpy.config.munge_in_strings:

        munge_regexp = re.compile(r'\b__(\w+)')

        def munge_string(m):

            g1 = m.group(1)

            if "__" in g1:
                return m.group(0)

            if g1.startswith("_"):
                return m.group(0)

            return prefix + m.group(1)

    else:

        munge_regexp = re.compile(r'(\.|\[+)__(\w+)')

        def munge_string(m):
            brackets = m.group(1)

            if (len(brackets) & 1) == 0:
                return m.group(0)

            if "__" in m.group(2):
                return m.group(0)

            return brackets + prefix + m.group(2)

    global original_filename

    original_filename = filename

    if filedata:
        data = filedata
    else:
        with open(filename, "rb") as f:
            data = f.read().decode("utf-8", "python_strict")

    if filename.endswith("_ren.py"):
        data = ren_py_to_rpy(data, filename)

    filename = elide_filename(filename)
    prefix = munge_filename(filename)

    # Add some newlines, to fix lousy editors.
    data += "\n\n"

    # The result.
    rv = []

    # The line number in the physical file.
    number = linenumber

    # The current position we're looking at in the buffer.
    pos = 0

    # Are we looking at a triple-quoted string?

    # Skip the BOM, if any.
    if len(data) and data[0] == u'\ufeff':
        pos += 1

    if add_lines or renpy.game.context().init_phase:
        lines = renpy.scriptedit.lines
    else:
        lines = { }

    len_data = len(data)

    renpy.scriptedit.files.add(filename)

    line = 0
    start_number = 0

    # Looping over the lines in the file.
    while pos < len_data:

        # The line number of the start of this logical line.
        start_number = number

        # The line that we're building up.
        line = [ ]

        # The number of open parenthesis there are right now.
        parendepth = 0

        loc = (filename, start_number)
        lines[loc] = renpy.scriptedit.Line(original_filename, start_number, pos)

        endpos = None

        while pos < len_data:

            startpos = pos
            c = data[pos]

            if c == u'\t':
                raise ParseError(filename, number, "Tab characters are not allowed in Ren'Py scripts.")

            if c == u'\n' and not parendepth:

                line = ''.join(line)

                # If not blank...
                if not re.match(r"^\s*$", line):

                    # Add to the results.
                    rv.append((filename, start_number, line))

                if endpos is None:
                    endpos = pos

                lines[loc].end_delim = endpos + 1

                while data[endpos - 1] in u' \r':
                    endpos -= 1

                lines[loc].end = endpos
                lines[loc].text = data[lines[loc].start:lines[loc].end]
                lines[loc].full_text = data[lines[loc].start:lines[loc].end_delim]

                pos += 1
                number += 1
                endpos = None
                # This helps out error checking.
                line = [ ]
                break

            if c == u'\n':
                number += 1
                endpos = None

            if c == u"\r":
                pos += 1
                continue

            # Backslash/newline.
            if c == u"\\" and data[pos + 1] == u"\n":
                pos += 2
                number += 1
                line.append(u"\\\n")
                continue

            # Parenthesis.
            if c in u'([{':
                parendepth += 1

            if (c in u'}])') and parendepth:
                parendepth -= 1

            # Comments.
            if c == u'#':
                endpos = pos

                while data[pos] != u'\n':
                    pos += 1

                continue

            # Strings.
            if c in u'"\'`':
                delim = c
                line.append(c)
                pos += 1

                escape = False
                triplequote = False

                if (pos < len_data - 1) and (data[pos] == delim) and (data[pos + 1] == delim):
                    line.append(delim)
                    line.append(delim)
                    pos += 2
                    triplequote = True

                s = [ ]

                while pos < len_data:

                    c = data[pos]

                    if c == u'\n':
                        number += 1

                    if c == u'\r':
                        pos += 1
                        continue

                    if escape:
                        escape = False
                        pos += 1
                        s.append(c)
                        continue

                    if c == delim:

                        if not triplequote:
                            pos += 1
                            s.append(c)
                            break

                        if (pos < len_data - 2) and (data[pos + 1] == delim) and (data[pos + 2] == delim):
                            pos += 3
                            s.append(delim)
                            s.append(delim)
                            s.append(delim)
                            break

                    if c == u'\\':
                        escape = True

                    s.append(c)
                    pos += 1

                    continue

                s = "".join(s)

                if "__" in s:
                    s = munge_regexp.sub(munge_string, s)

                line.append(s)

                continue

            word, magic, end = match_logical_word(data, pos)

            if magic:

                rest = word[2:]

                if u"__" not in rest:
                    word = prefix + rest

            line.append(word)
            pos = end

            if (pos - startpos) > 65536:
                raise ParseError(filename, start_number, "Overly long logical line. (Check strings and parenthesis.)", line=line, first=True)

    if line:
        raise ParseError(filename, start_number, "is not terminated with a newline. (Check strings and parenthesis.)", line=line, first=True)

    return rv


def group_logical_lines(lines):
    """
    This takes as input the list of logical line triples output from
    list_logical_lines, and breaks the lines into blocks. Each block
    is represented as a list of (filename, line number, line text,
    block) triples, where block is a block list (which may be empty if
    no block is associated with this line.)
    """

    # Returns the depth of a line, and the rest of the line.
    def depth_split(l):

        depth = 0
        index = 0

        while True:
            if l[index] == ' ':
                depth += 1
                index += 1
                continue

            # if l[index] == '\t':
            #    index += 1
            #    depth = depth + 8 - (depth % 8)
            #    continue

            break

        return depth, l[index:]

    # i, min_depth -> block, new_i
    def gll_core(i, min_depth):

        rv = []
        depth = None

        while i < len(lines):

            filename, number, text = lines[i]

            line_depth, rest = depth_split(text)

            # This catches a block exit.
            if line_depth < min_depth:
                break

            if depth is None:
                depth = line_depth

            if depth != line_depth:
                raise ParseError(filename, number, "Indentation mismatch.")

            # Advance to the next line.
            i += 1

            # Try parsing a block associated with this line.
            block, i = gll_core(i, depth + 1)

            rv.append((filename, number, rest, block))

        return rv, i

    if lines:

        filename, number, text = lines[0]

        if depth_split(text)[0] != 0:
            raise ParseError(filename, number, "Unexpected indentation at start of file.")

    return gll_core(0, 0)[0]


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

operator_regexp = "|".join([ re.escape(i) for i in OPERATORS ] + ESCAPED_OPERATORS)

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

    def __init__(self, block, init=False, init_offset=0, global_label=None, monologue_delimiter="\n\n", subparses=None):

        # Are we underneath an init block?
        self.init = init

        # The priority of auto-defined init statements.
        self.init_offset = init_offset

        self.block = block
        self.eob = False

        self.line = -1

        # These are set by advance.
        self.filename = ""
        self.text = ""
        self.number = 0
        self.subblock = [ ]
        self.global_label = global_label
        self.pos = 0
        self.word_cache_pos = -1
        self.word_cache_newpos = -1
        self.word_cache = ""

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

        self.filename, self.number, self.text, self.subblock = self.block[self.line]
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
        self.filename, self.number, self.text, self.subblock = self.block[self.line]
        self.pos = len(self.text)
        self.word_cache_pos = -1

    def match_regexp(self, regexp):
        """
        Tries to match the given regexp at the current location on the
        current line. If it succeds, it returns the matched text (if
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

        if (self.line == -1) and self.block:
            self.filename, self.number, self.text, self.subblock = self.block[0]

        raise ParseError(self.filename, self.number, msg, self.text, self.pos)

    def deferred_error(self, queue, msg):
        """
        Adds a deferred error to the given queue. This is used for something
        that might be an error, but could be compat-ed away.

        `queue`
            A string giving a list of deferred errors to add to.
        """

        if (self.line == -1) and self.block:
            self.filename, self.number, self.text, self.subblock = self.block[0]

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

        return Lexer(self.subblock, init=init, init_offset=self.init_offset, global_label=self.global_label, monologue_delimiter=self.monologue_delimiter, subparses=self.subparses)

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

            s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', dequote, s) # type: ignore

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

            rv = [ ]

            for s in sl:
                s = s.strip()

                if not s:
                    continue

                # Collapse runs of whitespace into single spaces.
                if mondel:
                    s = re.sub(r'[ \n]+', ' ', s)
                else:
                    s = re.sub(r' +', ' ', s)

                s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', dequote, s) # type: ignore

                rv.append(s)

            return rv

        return s

    def integer(self):
        """
        Tries to parse an integer. Returns a string containing the
        integer, or None.
        """

        return self.match(r'(\+|\-)?\d+')

    def float(self): # @ReservedAssignment
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

        if (rv in KEYWORDS ) or (rv in IMAGE_KEYWORDS):
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

        rv = self.expr(pe.strip(), expr) # E1101

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

    def checkpoint(self):
        """
        Returns an opaque representation of the lexer state. This can be
        passed to revert to back the lexer up.
        """

        return self.line, self.filename, self.number, self.text, self.subblock, self.pos, renpy.ast.PyExpr.checkpoint()

    def revert(self, state):
        """
        Reverts the lexer to the given state. State must have been returned
        by a previous checkpoint operation on this lexer.
        """

        self.line, self.filename, self.number, self.text, self.subblock, self.pos, pyexpr_checkpoint = state

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

        if isinstance(thing, basestring):
            name = name or thing
            rv = self.match(thing)
        else:
            rv = thing(**kwargs)

        if rv is None:
            if isinstance(thing, basestring):
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

    def python_block(self):
        """
        Returns the subblock of this code, and subblocks of that
        subblock, as indented python code. This tries to insert
        whitespace to ensure line numbers match up.
        """

        rv = [ ]

        o = LineNumberHolder()
        o.line = self.number

        def process(block, indent):

            for _fn, ln, text, subblock in block:

                while o.line < ln:
                    rv.append(indent + '\n')
                    o.line += 1

                linetext = indent + text + '\n'

                rv.append(linetext)
                o.line += linetext.count('\n')

                process(subblock, indent + '    ')

        process(self.subblock, '')
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
            block = [ block ]

        sp = SubParse(block)
        self.subparses.append(sp)

        return sp

    def renpy_block(self, empty=False):

        if self.subparses is None:
            raise Exception("A renpy_block can only be parsed inside a creator-defined statement.")

        if self.line < 0:
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


def ren_py_to_rpy(text, filename):
    """
    Transforms an _ren.py file into the equivalent .rpy file. This should retain line numbers.

    `filename`
        If not None, and an error occurs, the error is reported with the given filename.
        Otherwise, errors are ignored and a best effort is used.
    """

    lines = text.splitlines()
    result = [ ]

    # The prefix prepended to Python lines.
    prefix = ""

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
                result.append('')
                open_linenumber = linenumber
                continue

        if state == RENPY:
            if l == '"""':
                state = PYTHON
                result.append('')
                continue

            # Ignore empty and comments.
            sl = l.strip()
            if not sl:
                result.append(l)
                continue

            if sl[0] == "#":
                result.append(l)
                continue

            # Determine the prefix.
            prefix = ""
            for i in l:
                if i != ' ':
                    break
                prefix += ' '

            # If the line ends in ":", add 4 spaces to the prefix.
            if sl[-1] == ":":
                prefix += "    "

            result.append(l)
            continue

        if state == PYTHON:
            result.append(prefix + l)
            continue

        if state == IGNORE:
            result.append('')
            continue

    if filename is not None:

        if state == IGNORE:
            raise Exception('In {!r}, there are no """renpy blocks, so every line is ignored.'.format(filename))

        if state == RENPY:
            raise Exception('In {!r}, there is a """renpy block at line {} that is not terminated by """.'.format(filename,
                                                                                                                open_linenumber))

    rv = "\n".join(result)

    return rv
