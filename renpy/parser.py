# Copyright 2004-2006 PyTom <pytom@bishoujo.us>
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
# called when parsing is necessary, and creats an AST from the script.

import codecs
import re
import os
import sets

import renpy
import renpy.ast as ast

class ParseError(Exception):

    def __init__(self, filename, number, msg, line=None, pos=None):
        message = u"On line %d of %s: %s" % (number, filename, msg)

        if line is not None:
            message += "\n\n" + line

        if pos is not None:
            message += "\n" + " " * pos + "^"

        self.message = message

        Exception.__init__(self, message.encode('unicode_escape'))

    def __unicode__(self):
        return self.message


def list_logical_lines(filename):
    """
    This reads the specified filename, and divides it into logical
    line. The return value of this function is a list of (filename,
    line number, line text) triples.
    """

    f = codecs.open(filename, "rU", "utf-8")
    data = f.read()
    f.close()

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
                raise Exception("%s contains a tab character on line %d. Tab characters are not allowed in Ren'Py scripts." % (filename, number))

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
                line += "\n"
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
            
            line += c
            pos += 1


    if not line == "":
        raise ParseError(filename, start_number, "is not terminated with a newline (check quotes and parenthesis).")

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
    keywords = sets.Set([
        'as',
        'at',
        'call',
        'expression',
        'hide',
        'if',
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
        ])
        

    def __init__(self, block, init=False):

        # Are we underneath an init block?
        self.init = init
        
        self.block = block        
        self.eob = False
        
        self.line = -1
        

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
            return

        self.filename, self.number, self.text, self.subblock = self.block[self.line]
        self.pos = 0

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

        self.match_regexp(ur"\s+")

    def match(self, regexp):
        """
        Matches something at the current position, skipping past
        whitespace. Even if we can't match, the current position is
        still skipped past the leading whitespace.
        """

        self.skip_whitespace()
        return self.match_regexp(regexp) 
        

    def keyword(self, regexp):
        """
        Matches a keyword at the current position. A keyword is a word
        that is surrounded by things that aren't words, like
        whitespace. (This prevents a keyword from matching a prefix.)
        """

        return self.match(regexp + r'\b')


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
            self.error('%s does not expect a block.' % stmt)

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

        self.skip_whitespace()

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
            s = re.sub(r'\\u([0-9a-fA-F]{1,4})',
                       lambda m : unichr(int(m.group(1), 16)), s)
            s = re.sub(r'\\(.)', r'\1', s)

        return s

    def integer(self):
        """
        Tries to parse an integer. Returns a string containing the
        integer, or None.
        """

        self.skip_whitespace()

        return self.match(r'(\+|\-)?\d+')

    def name(self):
        """
        This tries to parse a name. Returns the name or None.
        """        

        self.skip_whitespace()

        oldpos = self.pos

        rv = self.match(ur'[a-zA-Z_\u00a0-\ufffd][0-9a-zA-Z_\u00a0-\ufffd]*')

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
        delimiter character. Returns a string containing the matched code,
        which may be empty if the first thing is the delimiter. Raises an
        error if EOL is reached before the delimiter.
        """

        start = self.pos

        while not self.eol():

            c = self.text[self.pos]

            if c == delim:
                return self.text[start:self.pos]

            if c == '"' or c == "'":
                self.python_string()
                continue

            if self.parenthesised_python():
                continue

            self.pos += 1

        self.error("reached eol when expecting '%s'." % delim)

    def python_expression(self):
        """
        Returns a python expression, which is arbitrary python code
        extending to a colon.
        """

        rv = self.delimited_python(':')

        if rv:
            rv = rv.strip()

        if not rv:
            self.error("expected python_expression")


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
            not self.integer() and 
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

        return self.text[start:self.pos]

    def checkpoint(self):
        """
        Returns an opaque representation of the lexer state. This can be
        passed to revert to back the lexer up.
        """

        return self.filename, self.number, self.text, self.subblock, self.pos

    def revert(self, state):
        """
        Reverts the lexer to the given state. State must have been returned
        by a previous checkpoint operation on this lexer.
        """

        self.filename, self.number, self.text, self.subblock, self.pos = state 

    def get_location(self):
        """
        Returns a (filename, line number) tuple representing the current
        physical location of the start of the current logical line.
        """

        return self.filename, self.number

    def require(self, thing):
        """
        Tries to parse thing, and reports an error if it cannot be done.

        If thing is a string, tries to parse it using
        self.match(thing). Otherwise, thing must be a method on this lexer
        object, which is called directly.
        """

        if isinstance(thing, str):
            name = thing
            rv = self.match(thing)            
        else:
            name = thing.im_func.func_name
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

        # Something to hold the expected line number.
        class Object(object):
            pass
        o = Object()
        o.line = self.number

        def process(block, indent):

            for fn, ln, text, subblock in block:

                if o.line > ln:
                    assert False

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

    if l.keyword("expression"):
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
                
        break

    if layer is None:
        layer = 'master'

    return image_name, expression, tag, at_list, layer, zorder

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

    
    
def parse_menu(l, loc):

    has_say = False
    has_caption = False

    with = None
    set = None

    say_who = None
    say_what = None

    # Tuples of (label, condition, block)
    items = [ ]

    l.advance()

    while not l.eob:

        if l.keyword('with'):
            with = l.require(l.simple_expression)
            l.expect_eol()
            l.expect_noblock('with clause')
            l.advance()

            continue

        if l.keyword('set'):
            set = l.require(l.simple_expression)
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
            l.expect_noblock('caption menuitem')

            if label and has_say:
                l.error("Captions and say menuitems may not exist in the same menu.")

            # Only set this if the caption is not "".
            if label:
                has_caption = True

            items.append((label, "True", None))
            l.advance()

            continue

        # Otherwise, we have a choice.
        condition = "True"

        if l.keyword('if'):
            condition = l.require(l.python_expression)

        l.require(':')
        l.expect_eol()
        l.expect_block('choice menuitem')

        block = parse_block(l.subblock_lexer())

        items.append((label, condition, block))
        l.advance()

    rv = [ ]
    if has_say:
        rv.append(ast.Say(loc, say_who, say_what, None, interact=False))

    rv.append(ast.Menu(loc, items, set, with))

    return rv


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

    ### If statement
    if l.keyword('if'):
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

    if l.keyword('elif'):
        l.error('elif clause must be associated with an if statement.')

    if l.keyword('else'):
        l.error('else clause must be associated with an if statement.')
        

    ### While statement
    if l.keyword('while'):
        condition = l.require(l.python_expression)
        l.require(':')
        l.expect_eol()
        l.expect_block('while statement')
        block = parse_block(l.subblock_lexer())
        l.advance()

        return ast.While(loc, condition, block)
        

    ### Pass statement
    if l.keyword('pass'):
        l.expect_noblock('pass statement')
        l.expect_eol()
        l.advance()

        return ast.Pass(loc)

    
    ### Menu statement.
    if l.keyword('menu'):
        l.expect_block('menu statement')
        label = l.name()
        l.require(':')
        l.expect_eol()

        menu = parse_menu(l.subblock_lexer(), loc)

        l.advance()

        rv = [ ]

        if label:
            rv.append(ast.Label(loc, label, []))

        rv.extend(menu)

        return rv
        
    ### Return statement.
    if l.keyword('return'):
        l.expect_noblock('return statement')
        l.expect_eol()
        l.advance()

        return ast.Return(loc)

    ### Jump statement
    if l.keyword('jump'):
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
    

    ### Call/From statement.
    if l.keyword('call'):
        l.expect_noblock('call statment')

        if l.keyword('expression'):
            expression = True
            target = l.require(l.simple_expression)
        else:
            expression = False            
            target = l.require(l.name)

        rv = [ ast.Call(loc, target, expression) ]

        if l.keyword('from'):
            name = l.require(l.name)
            rv.append(ast.Label(loc, name, []))
        else:
            rv.append(ast.Pass(loc))

        l.expect_eol()
        l.advance()

        return rv

    ### Scene statement.
    if l.keyword('scene'):
        l.expect_noblock('scene statement')

        if l.keyword('onlayer'):
            layer = l.require(l.name)
        else:
            layer = "master"

        # Empty.
        if l.eol():
            l.advance()
            return ast.Scene(loc, None, layer)

        imspec = parse_image_specifier(l)
        rv = parse_with(l, ast.Scene(loc, imspec, imspec[4]))

        l.expect_eol()
        l.advance()

        return rv

    ### Show statement.
    if l.keyword('show'):
        imspec = parse_image_specifier(l)
        rv = parse_with(l, ast.Show(loc, imspec))

        l.expect_eol()
        l.expect_noblock('show statement')
        l.advance()

        return rv
        
    ### Hide statement.
    if l.keyword('hide'):
        imspec = parse_image_specifier(l)
        rv = parse_with(l, ast.Hide(loc, imspec))

        l.expect_eol()
        l.expect_noblock('hide statement')
        l.advance()

        return rv
        
    ### With statement.
    if l.keyword('with'):
        expr = l.require(l.simple_expression)
        l.expect_eol()
        l.expect_noblock('with statement')
        l.advance()

        return ast.With(loc, expr)
    
    ### Image statement.
    if l.keyword('image'):

        if not l.init:
            l.error('image statements may only appear in init blocks.')
        
        name = parse_image_name(l)
        l.require('=')
        expr = l.rest()

        l.expect_noblock('image statement')
        l.advance()

        return ast.Image(loc, name, expr)

    ### One-line python statement.
    if l.match(r'\$'):
        python_code = l.rest()
        l.expect_noblock('one-line python statement')
        l.advance()

        return ast.Python(loc, python_code)

    ### Python block.
    if l.keyword('python'):

        hide = False
        if l.keyword('hide'):
            hide = True

        l.require(':')
        l.expect_block('python block')

        python_code = l.python_block()

        l.advance()
        return ast.Python(loc, python_code, hide)

    ### Label Statement
    if l.keyword('label'):
        name = l.require(l.name)
        l.require(':')
        l.expect_eol()

        # Optional block here. It's empty if no block is associated with
        # this statement.
        block = parse_block(l.subblock_lexer())

        l.advance()
        return ast.Label(loc, name, block)

    ### Init Statement
    if l.keyword('init'):

        p = l.integer()

        if p:
            priority = int(p)
        else:
            priority = 0
            
        l.require(':')

        l.expect_eol()
        l.expect_block('init statement')

        block = parse_block(l.subblock_lexer(True))

        l.advance()
        return ast.Init(loc, block, priority)


    # The one and two arguement say statements are ambiguous in terms
    # of lookahead. So we first try parsing as a one-argument, then a
    # two-argument.

    state = l.checkpoint()
    what = l.string()

    if l.keyword('with'):
        with = l.require(l.simple_expression)
    else:
        with = None

    if what is not None and l.eol():
        # We have a one-argument say statement.
        l.expect_noblock('say statement')
        l.advance()
        return ast.Say(loc, None, what, with)

    l.revert(state)

    # Try for a two-argument say statement.
    who = l.simple_expression()
    what = l.string()

    if l.keyword('with'):
        with = l.require(l.simple_expression)
    else:
        with = None

    if who and what is not None:
        l.expect_eol()
        l.expect_noblock('say statement')
        l.advance()
        return ast.Say(loc, who, what, with)

    l.error('expected statement.')

def parse_block(l):
    """
    This parses a block of Ren'Py statements. It returns a list of the
    statements contained within the block. l is a new Lexer object, for
    this block.
    """

    l.advance()
    rv = [ ]

    while not l.eob:
        stmt = parse_statement(l)
        if isinstance(stmt, list):
            rv.extend(stmt)
        else:
            rv.append(stmt)

    return rv


def parse(fn):
    """
    Parses an Ren'Py script contained within the file with the given
    filename. Returns a list of AST objects representing the
    statements that were found at the top level of the file.
    """

    renpy.game.exception_info = 'While parsing ' + fn + '.'

    lines = list_logical_lines(fn)
    nested = group_logical_lines(lines)

    l = Lexer(nested)
    
    return parse_block(l)
