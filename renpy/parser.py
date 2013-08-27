
# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import codecs
import re
import os

import renpy.display
import renpy.ast as ast

# A list of parse error messages.
parse_errors = [ ]

class ParseError(Exception):

    def __init__(self, filename, number, msg, line=None, pos=None, first=False):
        message = u"File \"%s\", line %d: %s" % (unicode_filename(filename), number, msg)

        if line:
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

    fn = os.path.abspath(fn)
    basedir = os.path.abspath(renpy.config.basedir)
    renpy_base = os.path.abspath(renpy.config.renpy_base)

    if fn.startswith(basedir):
        return os.path.relpath(fn, basedir).replace("\\", "/")
    elif fn.startswith(renpy_base):
        return os.path.relpath(fn, renpy_base).replace("\\", "/")
    else:
        return fn.replace("\\", "/")

def unelide_filename(fn):
    fn1 = os.path.join(renpy.config.basedir, fn)
    if os.path.exists(fn1):
        return fn1

    fn2 = os.path.join(renpy.config.basedir, fn)
    if os.path.exists(fn2):
        return fn2

    return fn

def list_logical_lines(filename, filedata=None):
    """
    Reads `filename`, and divides it into logical lines.

    Returns a list of (filename, line number, line text) triples.

    If `filedata` is given, it should be a unicode string giving the file
    contents. In that case, `filename` need not exist.
    """

    if filedata:
        data = filedata
    else:
        f = codecs.open(filename, "r", "utf-8")
        data = f.read()
        f.close()

    data = data.replace("\r\n", "\n")
    data = data.replace("\r", "\n")

    filename = elide_filename(filename)
    prefix = munge_filename(filename)

    # Add some newlines, to fix lousy editors.
    data += "\n\n"

    # The result.
    rv = []

    # The line number in the physical file.
    number = 1

    # The current position we're looking at in the buffer.
    pos = 0

    # Skip the BOM, if any.
    if len(data) and data[0] == u'\ufeff':
        pos += 1

    # Looping over the lines in the file.
    while pos < len(data):

        # The line number of the start of this logical line.
        start_number = number

        # The line that we're building up.
        line = ""

        # The number of open parenthesis there are right now.
        parendepth = 0

        # Looping over the characters in a single logical line.
        while pos < len(data):

            c = data[pos]

            if c == '\t':
                raise ParseError(filename, number, "Tab characters are not allowed in Ren'Py scripts.")

            if c == '\n':
                number += 1

            if c == '\n' and not parendepth:
                # If not blank...
                if not re.match("^\s*$", line):

                    # Add to the results.
                    rv.append((filename, start_number, line))

                pos += 1
                # This helps out error checking.
                line = ""
                break

            # Backslash/newline.
            if c == "\\" and data[pos+1] == "\n":
                pos += 2
                number += 1
                line += "\\\n"
                continue

            # Parenthesis.
            if c in ('(', '[', '{'):
                parendepth += 1

            if c in ('}', ']', ')') and parendepth:
                parendepth -= 1

            # Comments.
            if c == '#':
                while data[pos] != '\n':
                    pos += 1

                continue

            # Strings.
            if c in ('"', "'", "`"):
                delim = c
                line += c
                pos += 1

                escape = False

                while pos < len(data):

                    c = data[pos]

                    if c == '\n':
                        number += 1

                    if escape:
                        escape = False
                        pos += 1
                        line += c
                        continue

                    if c == delim:
                        pos += 1
                        line += c
                        break

                    if c == '\\':
                        escape = True

                    line += c
                    pos += 1

                    continue

                continue

            m = lllword.match(data, pos)

            word = m.group(0)
            rest = m.group(1)

            if rest and "__" not in rest:
                word = prefix + rest

            line += word

            if len(line) > 65536:
                raise ParseError(filename, start_number, "Overly long logical line. (Check strings and parenthesis.)", line=line, first=True)

            pos = m.end(0)

            # print repr(data[pos:])


    if not line == "":
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

class Lexer(object):
    """
    The lexer that is used to lex script files. This works on the idea
    that we want to lex each line in a block individually, and use
    sub-lexers to lex sub-blocks.
    """

    # A list of keywords which should not be parsed as names, because
    # there is a huge chance of confusion.
    #
    # Note: We need to be careful with what's in here, because thse
    # are banned in simple_expressions, where we might want to use
    # some of them.
    keywords = set([
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


    def __init__(self, block, init=False):

        # Are we underneath an init block?
        self.init = init

        self.block = block
        self.eob = False

        self.line = -1

        # These are set by advance.
        self.filename = ""
        self.text = ""
        self.number = 0
        self.subblock = [ ]
        self.pos = 0
        self.word_cache_pos = -1
        self.word_cache_newpos = -1
        self.word_cache = ""

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

        return Lexer(self.subblock, init=init)

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

        if not raw:

            # Collapse runs of whitespace into single spaces.
            s = re.sub(r'\s+', ' ', s)

            s = s.replace("\\n", "\n")
            s = s.replace("\\{", "{{")
            s = s.replace("\\%", "%%")
            s = re.sub(r'\\u([0-9a-fA-F]{1,4})',
                       lambda m : unichr(int(m.group(1), 16)), s)
            s = re.sub(r'\\(.)', r'\1', s)

        return s

    def integer(self):
        """
        Tries to parse an integer. Returns a string containing the
        integer, or None.
        """

        return self.match(r'(\+|\-)?\d+')

    def float(self): #@ReservedAssignment
        """
        Tries to parse a number (float). Returns a string containing the
        number, or None.
        """

        return self.match(r'(\+|\-)?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?')

    def hash(self):
        """
        Matches the chatacters in an md5 hash, and then some.
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
        rv = self.match(ur'[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*')
        self.word_cache = rv
        self.word_cache_newpos = self.pos

        return rv


    def name(self):
        """
        This tries to parse a name. Returns the name or None.
        """

        oldpos = self.pos
        rv = self.word()

        if rv in self.keywords:
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

    def delimited_python(self, delim):
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
                return renpy.ast.PyExpr(self.text[start:self.pos], self.filename, self.number)

            if c == '"' or c == "'":
                self.python_string()
                continue

            if self.parenthesised_python():
                continue

            self.pos += 1

        self.error("reached end of line when expecting '%s'." % delim)

    def python_expression(self):
        """
        Returns a python expression, which is arbitrary python code
        extending to a colon.
        """

        pe = self.delimited_python(':')

        if not pe:
            self.error("expected python_expression")

        rv = renpy.ast.PyExpr(pe.strip(), pe.filename, pe.linenumber) # E1101

        return rv

    def parenthesised_python(self):
        """
        Tries to match a parenthesised python expression. If it can,
        returns true and updates the current position to be after the
        closing parenthesis. Returns False otherewise.
        """

        c = self.text[self.pos]

        if c == '(':
            self.pos += 1
            self.delimited_python(')')
            self.pos += 1
            return True

        if c == '[':
            self.pos += 1
            self.delimited_python(']')
            self.pos += 1
            return True


        if c == '{':
            self.pos += 1
            self.delimited_python('}')
            self.pos += 1
            return True

        return False


    def simple_expression(self):
        """
        Tries to parse a simple_expression. Returns the text if it can, or
        None if it cannot.
        """

        self.skip_whitespace()
        if self.eol():
            return None

        start = self.pos

        # We start with either a name, a python_string, or parenthesized
        # python
        if (not self.python_string() and
            not self.name() and
            not self.float() and
            not self.parenthesised_python()):

            return None

        while not self.eol():
            self.skip_whitespace()

            if self.eol():
                break

            # If we see a dot, expect a dotted name.
            if self.match(r'\.'):
                n = self.name()
                if not n:
                    self.error("expecting name after dot.")

                continue

            # Otherwise, try matching parenthesised python.
            if self.parenthesised_python():
                continue

            break

        return renpy.ast.PyExpr(self.text[start:self.pos], self.filename, self.number)

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

        if isinstance(thing, str):
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
        return self.text[pos:]

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

def parse_image_name(l):
    """
    This parses an image name, and returns it as a tuple. It requires
    that the image name be present.
    """

    rv = [ l.require(l.name) ]

    while True:
        n = l.simple_expression()
        if not n:
            break

        rv.append(n.strip())

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
        image_name = parse_image_name(l)
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

    if layer is None:
        layer = 'master'



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
    set = None #@ReservedAssignment

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
            set = l.require(l.simple_expression) #@ReservedAssignment
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

        if not word in self.words:
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
    label = l.name()
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
        target = l.require(l.name)

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
        target = l.require(l.name)

    # Optional pass, to let someone write:
    # call expression foo pass (bar, baz)
    l.keyword('pass')

    arguments = parse_arguments(l)

    rv = [ ast.Call(loc, target, expression, arguments) ]

    if l.keyword('from'):
        name = l.require(l.name)
        rv.append(ast.Label(loc, name, [], None))
    else:
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
    name = parse_image_name(l)

    if l.match(':'):
        l.expect_eol()
        expr = None
        atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        l.require('=')
        expr = l.rest()
        atl = None
        l.expect_noblock('image statement')

    rv = ast.Image(loc, name, expr, atl)

    if not l.init:
        rv = ast.Init(loc, [ rv ], 990)

    l.advance()

    return rv


@statement("define")
def define_statement(l, loc):

    priority = l.integer()
    if priority:
        priority = int(priority)
    else:
        priority = 0

    name = l.require(l.name)
    l.require('=')
    expr = l.rest()

    l.expect_noblock('define statement')

    rv = ast.Define(loc, name, expr)

    if not l.init:
        rv = ast.Init(loc, [ rv ], priority)

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
        rv = ast.Init(loc, [ rv ], priority)

    l.advance()

    return rv


@statement("$")
def one_line_python(l, loc):
    python_code = l.rest()
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
        store = "store." + l.require(l.name)

    l.require(':')
    l.expect_block('python block')

    python_code = l.python_block()

    l.advance()

    if early:
        return ast.EarlyPython(loc, python_code, hide, store=store)
    else:
        return ast.Python(loc, python_code, hide, store=store)


@statement("label")
def label_statement(l, loc):
    name = l.require(l.name)

    parameters = parse_parameters(l)

    if l.keyword('hide'):
        hide = True
    else:
        hide = False

    l.require(':')
    l.expect_eol()

    # Optional block here. It's empty if no block is associated with
    # this statement.
    block = parse_block(l.subblock_lexer())

    l.advance()
    return ast.Label(loc, name, block, parameters, hide=hide)


@statement("init")
def init_statement(l, loc):

    p = l.integer()

    if p:
        priority = int(p)
    else:
        priority = 0

    if l.keyword('python'):

        hide = False
        if l.keyword('hide'):

            hide = True

        if l.keyword('in'):
            store = "store." + l.require(l.name)
        else:
            store = "store"

        l.require(':')
        l.expect_block('python block')

        python_code = l.python_block()

        l.advance()
        block = [ ast.Python(loc, python_code, hide, store=store) ]

    else:
        l.require(':')

        l.expect_eol()
        l.expect_block('init statement')

        block = parse_block(l.subblock_lexer(True))

        l.advance()

    return ast.Init(loc, block, priority)


@statement("screen")
def screen_statement(l, loc):

    # The guts of screen language parsing is in screenlang.py. It
    # assumes we ate the "screen" keyword before it's called.
    screen = renpy.screenlang.parse_screen(l)
    l.advance()

    if not screen:
        return [ ]

    rv = ast.Screen(loc, screen)

    if not l.init:
        rv = ast.Init(loc, [ rv ], -500)

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
        s = 'u' + s

        try:
            return eval(s)
        except:
            ll.error('could not parse string')

    while ll.advance():

        if ll.keyword('old'):

            if old is not None:
                ll.error("previous string is missing a translation")

            loc = ll.get_location()
            old = parse_string(ll.rest())

        elif ll.keyword('new'):

            if old is None:
                ll.error('no string to translate')

            new = parse_string(ll.rest())

            block.append(renpy.ast.TranslateString(loc, language, old, new))

            old = None
            new = None
            loc = None

        else:
            ll.error('unknown statement')

    if old:
        ll.error('final string is missing a translation')

    l.advance()

    if l.init:
        return block

    return ast.Init(init_loc, block, 0)

def translate_python(loc, language, l):
    l.require(':')
    l.expect_block('python block')

    python_code = l.python_block()

    l.advance()

    return ast.TranslatePython(loc, language, python_code)


@statement("translate")
def translate_statement(l, loc):

    language = l.require(l.name)

    if language == "None":
        language = None

    identifier = l.require(l.hash)

    if identifier == "strings":
        return translate_strings(loc, language, l)
    elif identifier == "python":
        return translate_python(loc, language, l)

    l.require(':')
    l.expect_eol()

    l.expect_block("translate statement")

    block = parse_block(l.subblock_lexer())

    l.advance()

    return [ ast.Translate(loc, identifier, language, block), ast.EndTranslate(loc) ]


@statement("")
def say_statement(l, loc):

    state = l.checkpoint()

    # Try for a single-argument say statement.
    what = l.string()

    if l.keyword('with'):
        with_ = l.require(l.simple_expression)
    else:
        with_ = None

    if what is not None and l.eol():
        # We have a one-argument say statement.
        l.expect_noblock('say statement')
        l.advance()
        return ast.Say(loc, None, what, with_)

    l.revert(state)

    # Try for a two-argument say statement.
    who = l.simple_expression()

    attributes = [ ]
    while True:
        prefix = l.match(r'-')
        if not prefix:
            prefix = ""

        component = l.word()

        if component is None:
            break

        attributes.append(prefix + component)

    if attributes:
        attributes = tuple(attributes)
    else:
        attributes = None

    what = l.string()

    if l.keyword('nointeract'):
        interact = False
    else:
        interact = True

    if l.keyword('with'):
        with_ = l.require(l.simple_expression)
    else:
        with_ = None

    if who and what is not None:
        l.expect_eol()
        l.expect_noblock('say statement')
        l.advance()
        return ast.Say(loc, who, what, with_, attributes=attributes, interact=interact)

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

        except ParseError, e:
            parse_errors.append(e.message)
            l.advance()

    return rv

def parse(fn, filedata=None):
    """
    Parses a Ren'Py script contained within the file `fn`.

    Returns a list of AST objects representing the statements that were found
    at the top level of the file.

    If `filedata` is given, it should be a unicode string giving the file
    contents.
    """

    renpy.game.exception_info = 'While parsing ' + fn + '.'

    try:
        lines = list_logical_lines(fn, filedata)
        nested = group_logical_lines(lines)
    except ParseError, e:
        parse_errors.append(e.message)
        return None

    l = Lexer(nested)

    rv = parse_block(l)

    if parse_errors:
        return None

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

    f, error_fn = renpy.bootstrap.open_error_file("errors.txt", "w")
    f.write(codecs.BOM_UTF8)

    print >>f, "I'm sorry, but errors were detected in your script. Please correct the"
    print >>f, "errors listed below, and try again."
    print >>f

    for i in parse_errors:

        full_text += i
        full_text += "\n\n"

        try:
            i = i.encode("utf-8")
        except:
            pass

        print
        print >>f
        print i
        print >>f, i


    print >>f
    print >>f, "Ren'Py Version:", renpy.version

    f.close()

    renpy.display.error.report_parse_errors(full_text, error_fn)

    try:
        if renpy.game.args.command == "run": #@UndefinedVariable
            renpy.exports.launch_editor([ error_fn ], 1, transient=1)
    except:
        pass

    return True
