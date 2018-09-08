# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

# This module contains the parser for the Ren'Py script language. It's
# called when parsing is necessary, and creates an AST from the script.

from __future__ import print_function
import codecs
import re
import os
import time

import renpy.display
import renpy.test

import renpy.ast as ast
import renpy.sl2

# A list of parse error messages.
parse_errors = [ ]

from renpy.parsersupport import match_logical_word


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

    if isinstance(fn, unicode):
        return fn

    # Windows.
    try:
        return fn.decode("mbcs")
    except:
        pass

    # Mac and (sane) Unix
    try:
        return fn.decode("utf-8")
    except:
        pass

    # Insane systems, mojibake.
    return fn.decode("latin-1")


# Matches either a word, or something else. Most magic is taken care of
# before this.
lllword = re.compile(r'__(\w+)|\w+| +|.', re.S)


def munge_filename(fn):
    # The prefix that's used when __ is found in the file.
    rv = os.path.basename(fn)
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

    ofn = fn
    fn = os.path.abspath(fn)
    basedir = os.path.abspath(renpy.config.basedir)
    renpy_base = os.path.abspath(renpy.config.renpy_base)

    if fn.startswith(basedir):
        return os.path.relpath(fn, basedir).replace("\\", "/")
    elif fn.startswith(renpy_base):
        return os.path.relpath(fn, renpy_base).replace("\\", "/")
    else:
        return ofn.replace("\\", "/")


def unelide_filename(fn):
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
        f = open(filename, "rb")
        data = f.read().decode("utf-8")
        f.close()

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
                if not re.match(u"^\s*$", line):

                    # Add to the results.
                    rv.append((filename, start_number, line))

                if endpos is None:
                    endpos = pos

                lines[loc].end_delim = endpos + 1

                while data[endpos-1] in u' \r':
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
            if c == u"\\" and data[pos+1] == u"\n":
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

                if (pos < len_data - 1) and (data[pos] == delim) and (data[pos+1] == delim):
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

                        if (pos < len_data - 2) and (data[pos+1] == delim) and (data[pos+2] == delim):
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

                if "[__" in s:

                    # Munge substitutions.
                    s = re.sub(r'(\.|\[+)__(\w+)', munge_string, s)

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
                raise ParseError(filename, number, "indentation mismatch.")

            # Advance to the next line.
            i += 1

            # Try parsing a block associated with this line.
            block, i = gll_core(i, depth + 1)

            rv.append((filename, number, rest, block))

        return rv, i

    return gll_core(0, 0)[0]


# A list of keywords which should not be parsed as names, because
# there is a huge chance of confusion.
#
# Note: We need to be careful with what's in here, because these
# are banned in simple_expressions, where we might want to use
# some of them.
KEYWORDS = set([
    '$',
    'as',
    'at',
    'behind',
    'call',
    'expression',
    'hide',
    'if',
    'in',
    'image',
    'init',
    'jump',
    'menu',
    'onlayer',
    'python',
    'return',
    'scene',
    'set',
    'show',
    'with',
    'while',
    'zorder',
    'transform',
    ])

OPERATORS = [
    '<',
    '<=',
    '>',
    '>=',
    '<>',
    '!=',
    '==',
    '|',
    '^',
    '&',
    '<<',
    '>>',
    '+',
    '-',
    '*',
    '/',
    '//',
    '%',
    '~',
    '**',
    ]

ESCAPED_OPERATORS = [
    r'\bor\b',
    r'\band\b',
    r'\bnot\b',
    r'\bin\b',
    r'\bis\b',
    ]

operator_regexp = "|".join([ re.escape(i) for i in OPERATORS ] + ESCAPED_OPERATORS)

word_regexp = ur'[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*'
image_word_regexp = ur'[-0-9a-zA-Z_\u00a0-\ufffd][-0-9a-zA-Z_\u00a0-\ufffd]*'


class Lexer(object):
    """
    The lexer that is used to lex script files. This works on the idea
    that we want to lex each line in a block individually, and use
    sub-lexers to lex sub-blocks.
    """

    def __init__(self, block, init=False, init_offset=0, global_label=None, monologue_delimiter="\n\n"):

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

        self.match_regexp(ur"(\s+|\\\n)+")

    def match(self, regexp):
        """
        Matches something at the current position, skipping past
        whitespace. Even if we can't match, the current position is
        still skipped past the leading whitespace.
        """

        self.skip_whitespace()
        return self.match_regexp(regexp)

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

    def error(self, msg):
        """
        Convenience function for reporting a parse error at the current
        location.
        """

        raise ParseError(self.filename, self.number, msg, self.text, self.pos)

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
            ll.error("Line is indented, but the preceding %s statement does not expect a block. Please check this line's indentation." % stmt)

    def expect_block(self, stmt):
        """
        Called to indicate that the statement requires that a non-empty
        block is present.
        """

        if not self.subblock:
            self.error('%s expects a non-empty block.' % stmt)

    def subblock_lexer(self, init=False):
        """
        Returns a new lexer object, equiped to parse the block
        associated with this line.
        """

        init = self.init or init

        return Lexer(self.subblock, init=init, init_offset=self.init_offset, global_label=self.global_label, monologue_delimiter=self.monologue_delimiter)

    def string(self):
        """
        Lexes a string, and returns the string to the user, or none if
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
                    return unichr(int(m.group(2), 16))
            else:
                return c

        if not raw:

            # Collapse runs of whitespace into single spaces.
            s = re.sub(r'\s+', ' ', s)
            s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', dequote, s)

        return s

    def triple_string(self):
        """
        Lexes a triple quoted string, intended for use with monologue mode.
        This is about the same as the double-quoted strings, except that
        runs of whitespace with multiple newlines are turned into a single
        newline.
        """

        s = self.match(r'r?"""([^\\"]|\\.)*"""')

        if s is None:
            s = self.match(r"r?'''([^\\']|\\.)*'''")

        if s is None:
            s = self.match(r"r?```([^\\`]|\\.)*```")

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
                    return unichr(int(m.group(2), 16))
            else:
                return c

        if not raw:

            # Collapse runs of whitespace into single spaces.
            s = re.sub(r' *\n *', '\n', s)

            rv = [ ]

            for s in s.split(self.monologue_delimiter):
                s = s.strip()

                if not s:
                    continue

                s = re.sub(r'\s+', ' ', s)
                s = re.sub(r'\\(u([0-9a-fA-F]{1,4})|.)', dequote, s)

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

        return rv

    def name(self):
        """
        This tries to parse a name. Returns the name or None.
        """

        oldpos = self.pos
        rv = self.word()

        if (rv == "r") or (rv == "u"):
            if self.text[self.pos:self.pos+1] in ( '"', "'", "`"):
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
            if not self.match('\.') or not self.global_label:
                self.pos = old_pos
                return None
            global_name = self.global_label
            local_name = self.name()
            if not local_name:
                self.pos = old_pos
                return None
        else:
            if self.match('\.'):
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

        return global_name+'.'+local_name

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
            if self.text[self.pos:self.pos+1] in ( '"', "'", "`"):
                self.pos = oldpos
                return None

        if rv in KEYWORDS:
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

        c = self.text[self.pos]

        # Allow unicode strings.
        if c == 'u':
            self.pos += 1

            if self.pos == len(self.text):
                self.pos -= 1
                return False

            c = self.text[self.pos]

            if c not in ('"', "'"):
                self.pos -= 1
                return False

        elif c not in ('"', "'"):
            return False

        delim = c

        while True:
            self.pos += 1

            if self.eol():
                self.error("end of line reached while parsing string.")

            c = self.text[self.pos]

            if c == delim:
                break

            if c == '\\':
                self.pos += 1

        self.pos += 1
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

    def simple_expression(self, comma=False, operator=True):
        """
        Tries to parse a simple_expression. Returns the text if it can, or
        None if it cannot.
        """

        start = self.pos

        # Operator.
        while True:

            while self.match(operator_regexp):
                pass

            if self.eol():
                break

            # We start with either a name, a python_string, or parenthesized
            # python
            if not (self.python_string() or
                    self.name() or
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

        return renpy.ast.PyExpr(self.text[start:self.pos].strip(), self.filename, self.number)

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

        return self.line, self.filename, self.number, self.text, self.subblock, self.pos

    def revert(self, state):
        """
        Reverts the lexer to the given state. State must have been returned
        by a previous checkpoint operation on this lexer.
        """

        self.line, self.filename, self.number, self.text, self.subblock, self.pos = state
        self.word_cache_pos = -1

    def get_location(self):
        """
        Returns a (filename, line number) tuple representing the current
        physical location of the start of the current logical line.
        """

        return self.filename, self.number

    def require(self, thing, name=None):
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
            name = name or thing.im_func.func_name
            rv = thing()

        if rv is None:
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


def parse_image_name(l, string=False, nodash=False):
    """
    This parses an image name, and returns it as a tuple. It requires
    that the image name be present.
    """

    points = [ l.checkpoint() ]
    rv = [ l.require(l.image_name_component) ]

    while True:

        points.append(l.checkpoint())

        n = l.image_name_component()

        if not n:
            points.pop()
            break

        rv.append(n.strip())

    if string:
        points.append(l.checkpoint())

        s = l.simple_expression()

        if s is not None:
            rv.append(unicode(s))
        else:
            points.pop()

    if nodash:
        for i, p in zip(rv, points):
            if i and i[0] == '-':
                l.revert(p)
                l.skip_whitespace()
                l.error("image name components may not begin with a '-'.")

    return tuple(rv)


def parse_simple_expression_list(l):
    """
    This parses a comma-separated list of simple_expressions, and
    returns a list of strings. It requires at least one
    simple_expression be present.
    """

    rv = [ l.require(l.simple_expression) ]

    while True:
        if not l.match(','):
            break

        e = l.simple_expression()

        if not e:
            break

        rv.append(e)

    return rv


def parse_image_specifier(l):
    """
    This parses an image specifier.
    """

    tag = None
    layer = None
    at_list = [ ]
    zorder = None
    behind = [ ]

    if l.keyword("expression") or l.keyword("image"):
        expression = l.require(l.simple_expression)
        image_name = ( expression.strip(), )
    else:
        image_name = parse_image_name(l, True)
        expression = None

    while True:

        if l.keyword("onlayer"):
            if layer:
                l.error("multiple onlayer clauses are prohibited.")
            else:
                layer = l.require(l.name)

            continue

        if l.keyword("at"):

            if at_list:
                l.error("multiple at clauses are prohibited.")
            else:
                at_list = parse_simple_expression_list(l)

            continue

        if l.keyword("as"):

            if tag:
                l.error("multiple as clauses are prohibited.")
            else:
                tag = l.require(l.name)

            continue

        if l.keyword("zorder"):

            if zorder is not None:
                l.error("multiple zorder clauses are prohibited.")
            else:
                zorder = l.require(l.simple_expression)

            continue

        if l.keyword("behind"):

            if behind:
                l.error("multiple behind clauses are prohibited.")

            while True:
                bhtag = l.require(l.name)
                behind.append(bhtag)
                if not l.match(','):
                    break

            continue

        break

    return image_name, expression, tag, at_list, layer, zorder, behind


def parse_with(l, node):
    """
    Tries to parse the with clause associated with this statement. If
    one exists, then the node is wrapped in a list with the
    appropriate pair of With nodes. Otherwise, just returns the
    statement by itself.
    """

    loc = l.get_location()

    if not l.keyword('with'):
        return node

    expr = l.require(l.simple_expression)

    return [ ast.With(loc, "None", expr),
             node,
             ast.With(loc, expr) ]


def parse_menu(stmtl, loc):

    l = stmtl.subblock_lexer()

    has_choice = False

    has_say = False
    has_caption = False

    with_ = None
    set = None  # @ReservedAssignment

    say_who = None
    say_what = None

    # Tuples of (label, condition, block)
    items = [ ]

    l.advance()

    while not l.eob:

        if l.keyword('with'):
            with_ = l.require(l.simple_expression)
            l.expect_eol()
            l.expect_noblock('with clause')
            l.advance()

            continue

        if l.keyword('set'):
            set = l.require(l.simple_expression)  # @ReservedAssignment
            l.expect_eol()
            l.expect_noblock('set menuitem')
            l.advance()

            continue

        # Try to parse a say menuitem.
        state = l.checkpoint()

        who = l.simple_expression()
        what = l.string()

        if who is not None and what is not None:

            l.expect_eol()
            l.expect_noblock("say menuitem")

            if has_caption:
                l.error("Say menuitems and captions may not exist in the same menu.")

            if has_say:
                l.error("Only one say menuitem may exist per menu.")

            has_say = True
            say_who = who
            say_what = what

            l.advance()

            continue

        l.revert(state)

        label = l.string()

        if label is None:
            l.error('expected menuitem')

        # A string on a line by itself is a caption.
        if l.eol():

            if l.subblock:
                l.error("Line is followed by a block, despite not being a menu choice. Did you forget a colon at the end of the line?")

            if label and has_say:
                l.error("Captions and say menuitems may not exist in the same menu.")

            # Only set this if the caption is not "".
            if label:
                has_caption = True

            items.append((label, "True", None))
            l.advance()

            continue

        # Otherwise, we have a choice.
        has_choice = True

        condition = "True"

        if l.keyword('if'):
            condition = l.require(l.python_expression)

        l.require(':')
        l.expect_eol()
        l.expect_block('choice menuitem')

        block = parse_block(l.subblock_lexer())

        items.append((label, condition, block))
        l.advance()

    if not has_choice:
        stmtl.error("Menu does not contain any choices.")

    rv = [ ]
    if has_say:
        rv.append(ast.Say(loc, say_who, say_what, None, interact=False))

    rv.append(ast.Menu(loc, items, set, with_))

    return rv


def parse_parameters(l):

    parameters = [ ]
    positional = [ ]
    extrapos = None
    extrakw = None

    add_positional = True

    names = set()

    if not l.match(r'\('):
        return None

    while True:

        if l.match('\)'):
            break

        if l.match(r'\*\*'):

            if extrakw is not None:
                l.error('a label may have only one ** parameter')

            extrakw = l.require(l.name)

            if extrakw in names:
                l.error('parameter %s appears twice.' % extrakw)

            names.add(extrakw)

        elif l.match(r'\*'):

            if not add_positional:
                l.error('a label may have only one * parameter')

            add_positional = False

            extrapos = l.name()

            if extrapos is not None:

                if extrapos in names:
                    l.error('parameter %s appears twice.' % extrapos)

                names.add(extrapos)

        else:

            name = l.require(l.name)

            if name in names:
                l.error('parameter %s appears twice.' % name)

            names.add(name)

            if l.match(r'='):
                l.skip_whitespace()
                default = l.delimited_python("),")
            else:
                default = None

            parameters.append((name, default))

            if add_positional:
                positional.append(name)

        if l.match(r'\)'):
            break

        l.require(r',')

    return renpy.ast.ParameterInfo(parameters, positional, extrapos, extrakw)


def parse_arguments(l):
    """
    Parse a list of arguments, if one is present.
    """

    arguments = [ ]
    extrakw = None
    extrapos = None

    if not l.match(r'\('):
        return None

    while True:

        if l.match('\)'):
            break

        if l.match(r'\*\*'):

            if extrakw is not None:
                l.error('a call may have only one ** argument')

            extrakw = l.delimited_python("),")

        elif l.match(r'\*'):
            if extrapos is not None:
                l.error('a call may have only one * argument')

            extrapos = l.delimited_python("),")

        else:

            state = l.checkpoint()

            name = l.name()
            if not (name and l.match(r'=')):
                l.revert(state)
                name = None

            l.skip_whitespace()
            arguments.append((name, l.delimited_python("),")))

        if l.match(r'\)'):
            break

        l.require(r',')

    return renpy.ast.ArgumentInfo(arguments, extrapos, extrakw)


##############################################################################
# The parse trie.

class ParseTrie(object):
    """
    This is a trie of words, that's used to pick a parser function.
    """

    def __init__(self):
        self.default = None
        self.words = { }

    def add(self, name, function):

        if not name:
            self.default = function
            return

        first = name[0]
        rest = name[1:]

        if first not in self.words:
            self.words[first] = ParseTrie()

        self.words[first].add(rest, function)

    def parse(self, l):
        old_pos = l.pos

        word = l.word() or l.match(r'\$')

        if word not in self.words:
            l.pos = old_pos
            return self.default

        return self.words[word].parse(l)


# The root of the parse trie.
statements = ParseTrie()


def statement(keywords):
    """
    A function decorator used to declare a statement. Keywords is a string
    giving the keywords that precede the statement.
    """

    keywords = keywords.split()

    def wrap(f):
        statements.add(keywords, f)
        return f

    return wrap


##############################################################################
# Statement functions.

@statement("if")
def if_statement(l, loc):

    entries = [ ]

    condition = l.require(l.python_expression)
    l.require(':')
    l.expect_eol()
    l.expect_block('if statement')

    block = parse_block(l.subblock_lexer())

    entries.append((condition, block))

    l.advance()

    while l.keyword('elif'):

        condition = l.require(l.python_expression)
        l.require(':')
        l.expect_eol()
        l.expect_block('elif clause')

        block = parse_block(l.subblock_lexer())

        entries.append((condition, block))

        l.advance()

    if l.keyword('else'):
        l.require(':')
        l.expect_eol()
        l.expect_block('else clause')

        block = parse_block(l.subblock_lexer())

        entries.append(('True', block))

        l.advance()

    return ast.If(loc, entries)


@statement("while")
def while_statement(l, loc):
    condition = l.require(l.python_expression)
    l.require(':')
    l.expect_eol()
    l.expect_block('while statement')
    block = parse_block(l.subblock_lexer())
    l.advance()

    return ast.While(loc, condition, block)


@statement("pass")
def pass_statement(l, loc):
    l.expect_noblock('pass statement')
    l.expect_eol()
    l.advance()

    return ast.Pass(loc)


@statement("menu")
def menu_statement(l, loc):
    l.expect_block('menu statement')
    label = l.label_name_declare()
    l.set_global_label(label)
    l.require(':')
    l.expect_eol()

    menu = parse_menu(l, loc)

    l.advance()

    rv = [ ]

    if label:
        rv.append(ast.Label(loc, label, [], None))

    rv.extend(menu)

    return rv


@statement("return")
def return_statement(l, loc):
    l.expect_noblock('return statement')

    rest = l.rest()
    if not rest:
        rest = None

    l.expect_eol()
    l.advance()

    return ast.Return(loc, rest)


@statement("jump")
def jump_statement(l, loc):
    l.expect_noblock('jump statement')

    if l.keyword('expression'):
        expression = True
        target = l.require(l.simple_expression)
    else:
        expression = False
        target = l.require(l.label_name)

    l.expect_eol()
    l.advance()

    return ast.Jump(loc, target, expression)


@statement("call")
def call_statement(l, loc):
    l.expect_noblock('call statment')

    if l.keyword('expression'):
        expression = True
        target = l.require(l.simple_expression)

    else:
        expression = False
        target = l.require(l.label_name)

    # Optional pass, to let someone write:
    # call expression foo pass (bar, baz)
    l.keyword('pass')

    arguments = parse_arguments(l)

    rv = [ ast.Call(loc, target, expression, arguments) ]

    if l.keyword('from'):
        name = l.require(l.label_name_declare)
        l.set_global_label(name)
        rv.append(ast.Label(loc, name, [], None))
    else:
        if renpy.scriptedit.lines and (loc in renpy.scriptedit.lines):
            if expression:
                renpy.add_from.report_missing("expression", original_filename, renpy.scriptedit.lines[loc].end)
            else:
                renpy.add_from.report_missing(target, original_filename, renpy.scriptedit.lines[loc].end)

    rv.append(ast.Pass(loc))

    l.expect_eol()
    l.advance()

    return rv


@statement("scene")
def scene_statement(l, loc):
    if l.keyword('onlayer'):
        layer = l.require(l.name)
    else:
        layer = "master"

    # Empty.
    if l.eol():
        l.advance()
        return ast.Scene(loc, None, layer)

    imspec = parse_image_specifier(l)
    stmt = ast.Scene(loc, imspec, imspec[4])
    rv = parse_with(l, stmt)

    if l.match(':'):
        stmt.atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        l.expect_noblock('scene statement')

    l.expect_eol()
    l.advance()

    return rv


@statement("show")
def show_statement(l, loc):
    imspec = parse_image_specifier(l)
    stmt = ast.Show(loc, imspec)
    rv = parse_with(l, stmt)

    if l.match(':'):
        stmt.atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        l.expect_noblock('show statement')

    l.expect_eol()
    l.advance()

    return rv


@statement("show layer")
def show_layer_statement(l, loc):

    layer = l.require(l.name)

    if l.keyword("at"):
        at_list = parse_simple_expression_list(l)
    else:
        at_list = [ ]

    if l.match(':'):
        atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        atl = None
        l.expect_noblock('show layer statement')

    l.expect_eol()
    l.advance()

    rv = ast.ShowLayer(loc, layer, at_list, atl)

    return rv


@statement("hide")
def hide_statement(l, loc):
    imspec = parse_image_specifier(l)
    rv = parse_with(l, ast.Hide(loc, imspec))

    l.expect_eol()
    l.expect_noblock('hide statement')
    l.advance()

    return rv


@statement("with")
def with_statement(l, loc):
    expr = l.require(l.simple_expression)
    l.expect_eol()
    l.expect_noblock('with statement')
    l.advance()

    return ast.With(loc, expr)


@statement("image")
def image_statement(l, loc):
    name = parse_image_name(l, nodash=True)

    if l.match(':'):
        l.expect_eol()
        expr = None
        atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        l.require('=')

        expr = l.rest()

        if not expr:
            l.error('expected expression')

        atl = None
        l.expect_noblock('image statement')

    rv = ast.Image(loc, name, expr, atl)

    if not l.init:
        rv = ast.Init(loc, [ rv ], 500 + l.init_offset)

    l.advance()

    return rv


@statement("define")
def define_statement(l, loc):

    priority = l.integer()
    if priority:
        priority = int(priority)
    else:
        priority = 0

    store = 'store'
    name = l.require(l.word)

    while l.match(r'\.'):
        store = store + "." + name
        name = l.require(l.word)

    l.require('=')
    expr = l.rest()

    if not expr:
        l.error("expected expression")

    l.expect_noblock('define statement')

    rv = ast.Define(loc, store, name, expr)

    if not l.init:
        rv = ast.Init(loc, [ rv ], priority + l.init_offset)

    l.advance()

    return rv


@statement("default")
def default_statement(l, loc):

    priority = l.integer()
    if priority:
        priority = int(priority)
    else:
        priority = 0

    store = 'store'
    name = l.require(l.word)

    while l.match(r'\.'):
        store = store + "." + name
        name = l.require(l.word)

    l.require('=')
    expr = l.rest()

    if not expr:
        l.error("expected expression")

    l.expect_noblock('default statement')

    rv = ast.Default(loc, store, name, expr)

    if not l.init:
        rv = ast.Init(loc, [ rv ], priority + l.init_offset)

    l.advance()

    return rv


@statement("transform")
def transform_statement(l, loc):

    priority = l.integer()
    if priority:
        priority = int(priority)
    else:
        priority = 0

    name = l.require(l.name)
    parameters = parse_parameters(l)

    if parameters and (parameters.extrakw or parameters.extrapos):
        l.error('transform statement does not take a variable number of parameters')

    l.require(':')
    l.expect_eol()

    atl = renpy.atl.parse_atl(l.subblock_lexer())

    rv = ast.Transform(loc, name, atl, parameters)

    if not l.init:
        rv = ast.Init(loc, [ rv ], priority + l.init_offset)

    l.advance()

    return rv


@statement("$")
def one_line_python(l, loc):
    python_code = l.rest_statement()

    if not python_code:
        l.error('expected python code')

    l.expect_noblock('one-line python statement')
    l.advance()

    return ast.Python(loc, python_code, store="store")


@statement("python")
def python_statement(l, loc):
    hide = False
    early = False
    store = 'store'

    if l.keyword('early'):
        early = True

    if l.keyword('hide'):
        hide = True

    if l.keyword('in'):
        store = "store." + l.require(l.dotted_name)

    l.require(':')
    l.expect_block('python block')

    python_code = l.python_block()

    l.advance()

    if early:
        return ast.EarlyPython(loc, python_code, hide, store=store)
    else:
        return ast.Python(loc, python_code, hide, store=store)


@statement("label")
def label_statement(l, loc, init=False):

    name = l.require(l.label_name_declare)
    l.set_global_label(name)
    parameters = parse_parameters(l)

    if l.keyword('hide'):
        hide = True
    else:
        hide = False

    l.require(':')
    l.expect_eol()

    # Optional block here. It's empty if no block is associated with
    # this statement.
    block = parse_block(l.subblock_lexer(init))

    l.advance()
    return ast.Label(loc, name, block, parameters, hide=hide)


@statement("init offset")
def init_offset_statement(l, loc):

    l.require('=')
    offset = l.require(l.integer)

    l.expect_eol()
    l.expect_noblock('init offset statement')
    l.advance()

    l.init_offset = int(offset)
    return [ ]


@statement("init label")
def init_label_statement(l, loc):
    return label_statement(l, loc, init=True)


@statement("init")
def init_statement(l, loc):

    p = l.integer()

    if p:
        priority = int(p)
    else:
        priority = 0

    if l.match(':'):

        l.expect_eol()
        l.expect_block('init statement')

        block = parse_block(l.subblock_lexer(True))

        l.advance()

    else:

        try:
            old_init = l.init
            l.init = True

            block = [ parse_statement(l) ]

        finally:
            l.init = old_init

    return ast.Init(loc, block, priority + l.init_offset)


@statement("rpy monologue")
def rpy_statement(l, loc):

    if l.keyword("double"):
        l.monologue_delimiter = "\n\n"
    elif l.keyword("single"):
        l.monologue_delimiter = "\n"
    else:
        l.error("rpy monologue expects either single or double.")

    l.expect_eol()
    l.expect_noblock('rpy monologue')
    l.advance()

    return [ ]


def screen1_statement(l, loc):

    # The guts of screen language parsing is in screenlang.py. It
    # assumes we ate the "screen" keyword before it's called.
    screen = renpy.screenlang.parse_screen(l)

    l.advance()

    if not screen:
        return [ ]

    rv = ast.Screen(loc, screen)

    if not l.init:
        rv = ast.Init(loc, [ rv ], -500 + l.init_offset)

    return rv


def screen2_statement(l, loc):

    # The guts of screen language parsing is in screenlang.py. It
    # assumes we ate the "screen" keyword before it's called.
    screen = renpy.sl2.slparser.parse_screen(l, loc)

    l.advance()

    rv = ast.Screen(loc, screen)

    if not l.init:
        rv = ast.Init(loc, [ rv ], -500 + l.init_offset)

    return rv


# The version of screen language to use by default.
default_screen_language = int(os.environ.get("RENPY_SCREEN_LANGUAGE", "2"))


@statement("screen")
def screen_statement(l, loc):

    screen_language = default_screen_language

    slver = l.integer()
    if slver is not None:
        screen_language = int(slver)

    if screen_language == 1:
        return screen1_statement(l, loc)
    elif screen_language == 2:
        return screen2_statement(l, loc)
    else:
        l.error("Bad screen language version.")


@statement("testcase")
def testcase_statement(l, loc):
    name = l.require(l.name)
    l.require(':')
    l.expect_eol()
    l.expect_block('testcase statement')

    test = renpy.test.testparser.parse_block(l.subblock_lexer(), loc)

    l.advance()

    rv = ast.Testcase(loc, name, test)

    if not l.init:
        rv = ast.Init(loc, [ rv ], 500 + l.init_offset)

    return rv


def translate_strings(init_loc, language, l):
    l.require(':')
    l.expect_eol()
    l.expect_block('translate strings statement')

    ll = l.subblock_lexer()

    block = [ ]

    old = None
    loc = None

    def parse_string(s):
        s = s.strip()

        try:
            bc = compile(s, "<string>", "eval", renpy.python.new_compile_flags, 1)
            return eval(bc, renpy.store.__dict__)
        except:
            raise
            ll.error('could not parse string')

    while ll.advance():

        if ll.keyword('old'):

            if old is not None:
                ll.error("previous string is missing a translation")

            loc = ll.get_location()

            try:
                old = parse_string(ll.rest())
            except:
                ll.error("Could not parse string.")

        elif ll.keyword('new'):

            if old is None:
                ll.error('no string to translate')

            newloc = ll.get_location()
            try:
                new = parse_string(ll.rest())
            except:
                ll.error("Could not parse string.")

            block.append(renpy.ast.TranslateString(loc, language, old, new, newloc))

            old = None
            new = None
            loc = None
            newloc = None

        else:
            ll.error('unknown statement')

    if old:
        ll.error('final string is missing a translation')

    l.advance()

    if l.init:
        return block

    return ast.Init(init_loc, block, l.init_offset)


@statement("translate")
def translate_statement(l, loc):

    language = l.require(l.name)

    if language == "None":
        language = None

    identifier = l.require(l.hash)

    if identifier == "strings":
        return translate_strings(loc, language, l)

    elif identifier == "python":
        try:
            old_init = l.init
            l.init = True

            block = [ python_statement(l, loc) ]
            return [ ast.TranslateEarlyBlock(loc, language, block) ]
        finally:
            l.init = old_init

    elif identifier == "style":
        try:
            old_init = l.init
            l.init = True

            block = [ style_statement(l, loc) ]
            return [ ast.TranslateBlock(loc, language, block) ]
        finally:
            l.init = old_init

    l.require(':')
    l.expect_eol()

    l.expect_block("translate statement")

    block = parse_block(l.subblock_lexer())

    l.advance()

    return [ ast.Translate(loc, identifier, language, block), ast.EndTranslate(loc) ]


@statement("style")
def style_statement(l, loc):

    # Parse priority and name.
    name = l.require(l.word)
    parent = None

    rv = ast.Style(loc, name)

    # Function that parses a clause. This returns true if a clause has been
    # parsed, False otherwise.
    def parse_clause(l):

        if l.keyword("is"):
            if parent is not None:
                l.error("parent clause appears twice.")

            rv.parent = l.require(l.word)
            return True

        if l.keyword("clear"):
            rv.clear = True
            return True

        if l.keyword("take"):
            if rv.take is not None:
                l.error("take clause appears twice.")

            rv.take = l.require(l.name)
            return True

        if l.keyword("del"):
            propname = l.require(l.name)

            if propname not in renpy.style.prefixed_all_properties:  # @UndefinedVariable
                l.error("style property %s is not known." % propname)

            rv.delattr.append(propname)
            return True

        if l.keyword("variant"):
            if rv.variant is not None:
                l.error("variant clause appears twice.")

            rv.variant = l.require(l.simple_expression)

            return True

        propname = l.name()

        if propname is not None:
            if (propname != "properties") and (propname not in renpy.style.prefixed_all_properties):  # @UndefinedVariable
                l.error("style property %s is not known." % propname)

            if propname in rv.properties:
                l.error("style property %s appears twice." % propname)

            rv.properties[propname] = l.require(l.simple_expression)

            return True

        return False

    while parse_clause(l):
        pass

    if not l.match(':'):
        l.expect_noblock("style statement")
        l.expect_eol()
    else:
        l.expect_block("style statement")
        l.expect_eol()

        ll = l.subblock_lexer()

        while ll.advance():

            while parse_clause(ll):
                pass

            ll.expect_eol()

    if not l.init:
        rv = ast.Init(loc, [ rv ], l.init_offset)

    l.advance()

    return rv


def finish_say(l, loc, who, what, attributes=None):

    if what is None:
        return None

    interact = True
    with_ = None
    arguments = None

    while True:

        if l.keyword('nointeract'):
            interact = False

        elif l.keyword('with'):
            if with_ is not None:
                l.error('say can only take a single with clause')

            with_ = l.require(l.simple_expression)

        else:
            args = parse_arguments(l)

            if args is None:
                break

            if arguments is not None:
                l.error('say can only take a single set of arguments')

            arguments = args

    if isinstance(what, list):

        rv = [ ]

        for i in what:

            if i == "{clear}":
                rv.append(ast.UserStatement(loc, "nvl clear", [ ]))
            else:
                rv.append(ast.Say(loc, who, i, with_, attributes=attributes, interact=interact, arguments=arguments))

        return rv

    else:
        return ast.Say(loc, who, what, with_, attributes=attributes, interact=interact, arguments=arguments)


@statement("")
def say_statement(l, loc):

    state = l.checkpoint()

    # Try for a single-argument say statement.
    what = l.triple_string() or l.string()

    rv = finish_say(l, loc, None, what)

    if (rv is not None) and l.eol():

        # We have a one-argument say statement.
        l.expect_noblock('say statement')
        l.advance()

        return rv

    l.revert(state)

    # Try for a two-argument say statement.
    who = l.say_expression()

    attributes = [ ]
    while True:
        prefix = l.match(r'-')
        if not prefix:
            prefix = ""

        component = l.image_name_component()

        if component is None:
            break

        attributes.append(prefix + component)

    if attributes:
        attributes = tuple(attributes)
    else:
        attributes = None

    what = l.triple_string() or l.string()

    if (who is not None) and (what is not None):

        rv = finish_say(l, loc, who, what, attributes)

        l.expect_eol()
        l.expect_noblock('say statement')
        l.advance()

        return rv

    # This reports a parse error for any bad statement.
    l.error('expected statement.')


##############################################################################
# Functions called to parse things.

def parse_statement(l):
    """
    This parses a Ren'Py statement. l is expected to be a Ren'Py lexer
    that has been advanced to a logical line. This function will
    advance l beyond the last logical line making up the current
    statement, and will return an AST object representing this
    statement, or a list of AST objects representing this statement.
    """

    # Store the current location.
    loc = l.get_location()

    pf = statements.parse(l)

    if pf is None:
        l.error("expected statement.")

    return pf(l, loc)


def parse_block(l):
    """
    This parses a block of Ren'Py statements. It returns a list of the
    statements contained within the block. l is a new Lexer object, for
    this block.
    """

    l.advance()
    rv = [ ]

    while not l.eob:
        try:

            stmt = parse_statement(l)

            if isinstance(stmt, list):
                rv.extend(stmt)
            else:
                rv.append(stmt)

        except ParseError as e:
            parse_errors.append(e.message)
            l.advance()

    return rv


def parse(fn, filedata=None, linenumber=1):
    """
    Parses a Ren'Py script contained within the file `fn`.

    Returns a list of AST objects representing the statements that were found
    at the top level of the file.

    If `filedata` is given, it should be a unicode string giving the file
    contents.

    If `linenumber` is given, the parse starts at `linenumber`.
    """

    renpy.game.exception_info = 'While parsing ' + fn + '.'

    try:
        lines = list_logical_lines(fn, filedata, linenumber)
        nested = group_logical_lines(lines)
    except ParseError, e:
        parse_errors.append(e.message)
        return None

    l = Lexer(nested)

    rv = parse_block(l)

    if parse_errors:
        return None

    if rv:
        rv.append(ast.Return( (rv[-1].filename, rv[-1].linenumber), None ))

    return rv


def get_parse_errors():
    global parse_errors
    rv = parse_errors
    parse_errors = [ ]
    return rv


def report_parse_errors():

    if not parse_errors:
        return False

    full_text = ""

    f, error_fn = renpy.error.open_error_file("errors.txt", "w")
    f.write(codecs.BOM_UTF8)

    print("I'm sorry, but errors were detected in your script. Please correct the", file=f)
    print("errors listed below, and try again.", file=f)
    print(file=f)

    for i in parse_errors:

        full_text += i
        full_text += "\n\n"

        try:
            i = i.encode("utf-8")
        except:
            pass

        print()
        print(file=f)
        print(i)
        print(i, file=f)

    print(file=f)
    print("Ren'Py Version:", renpy.version, file=f)
    print(time.ctime(), file=f)

    f.close()

    renpy.display.error.report_parse_errors(full_text, error_fn)

    try:
        if renpy.game.args.command == "run":  # @UndefinedVariable
            renpy.exports.launch_editor([ error_fn ], 1, transient=1)
    except:
        pass

    return True
