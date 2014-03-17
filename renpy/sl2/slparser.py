# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

import renpy

import renpy.sl2.slast as slast

# A list of style prefixes that we know of.
STYLE_PREFIXES = [
    '',
    'insensitive_',
    'hover_',
    'idle_',
    'activate_',
    'selected_',
    'selected_insensitive_',
    'selected_hover_',
    'selected_idle_',
    'selected_activate_',
]

##############################################################################
# Parsing.

# The parser that things are being added to.
parser = None

# All statements we know about.
all_statements = [ ]

# Statements that can contain children.
childbearing_statements = [ ]

class Positional(object):
    """
    This represents a positional parameter to a function.
    """

    def __init__(self, name):
        self.name = name

        if parser:
            parser.add(self)

# Used to generate the documentation
all_keyword_names = set()

class Keyword(object):
    """
    This represents an optional keyword parameter to a function.
    """

    def __init__(self, name):
        self.name = name

        all_keyword_names.add(self.name)

        if parser:
            parser.add(self)

class Style(object):
    """
    This represents a style parameter to a function.
    """

    def __init__(self, name):
        self.name = name

        for j in STYLE_PREFIXES:
            all_keyword_names.add(j + self.name)

        if parser:
            parser.add(self)


class PrefixStyle(object):
    """
    This represents a prefixed style parameter to a function.
    """

    def __init__(self, prefix, name):
        self.prefix = prefix
        self.name = name

        for j in STYLE_PREFIXES:
            all_keyword_names.add(prefix + j + self.name)

        if parser:
            parser.add(self)


class Parser(object):

    def __init__(self, name):

        # The name of this object.
        self.name = name

        # The positional arguments, keyword arguments, and child
        # statements of this statement.
        self.positional = [ ]
        self.keyword = { }
        self.children = { }

        all_statements.append(self)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def add(self, i):
        """
        Adds a clause to this parser.
        """

        if isinstance(i, list):
            for j in i:
                self.add(j)

            return

        if isinstance(i, Positional):
            self.positional.append(i)

        elif isinstance(i, Keyword):
            self.keyword[i.name] = i

        elif isinstance(i, Style):
            for j in STYLE_PREFIXES:
                self.keyword[j + i.name] = i

        elif isinstance(i, PrefixStyle):
            for j in STYLE_PREFIXES:
                self.keyword[i.prefix + j + i.name] = i

        elif isinstance(i, Parser):
            self.children[i.name] = i

    def parse_statement(self, l, layout_mode=False):
        word = l.word() or l.match(r'\$')

        if word and word in self.children:
            if layout_mode:
                c = self.children[word].parse_layout(l)
            else:
                c = self.children[word].parse(l)

            return c
        else:
            return None

    def parse_layout(self, l):
        l.error("The %s statement cannot be used as a container for the has statement." % self.name)

    def parse(self, l):
        """
        This is expected to parse a function statement, and to return
        a list of python ast statements.

        `l` the lexer.

        `name` the name of the variable containing the name of the
        current statement.
        """

        raise Exception("Not Implemented")

def add(thing):
    parser.add(thing)

class ScreenLangScreen(renpy.object.Object):
    """
    This represents a screen defined in the screen language.
    """

    __version__ = 1

    variant = "None"

    # Predict should be false for screens created before
    # prediction existed.
    predict = "False"

    parameters = None

    def __init__(self):

        # The name of the screen.
        self.name = None

        # Should this screen be declared as modal?
        self.modal = "False"

        # The screen's zorder.
        self.zorder = "0"

        # The screen's tag.
        self.tag = None

        # The PyCode object containing the screen's code.
        self.code = None

        # The variant of screen we're defining.
        self.variant = "None" # expr.

        # Should we predict this screen?
        self.predict = "None" # expr.

        # The parameters this screen takes.
        self.parameters = None

    def after_upgrade(self, version):
        if version < 1:
            self.modal = "False"
            self.zorder = "0"

    def define(self):
        """
        Defines a screen.
        """

        renpy.display.screen.define_screen(
            self.name,
            self,
            modal=self.modal,
            zorder=self.zorder,
            tag=self.tag,
            variant=renpy.python.py_eval(self.variant),
            predict=renpy.python.py_eval(self.predict),
            parameters=self.parameters,
            )

    def __call__(self, *args, **kwargs):
        scope = kwargs["_scope"]

        if self.parameters:

            args = scope.get("_args", ())
            kwargs = scope.get("_kwargs", { })

            values = renpy.ast.apply_arguments(self.parameters, args, kwargs)
            scope.update(values)

        renpy.python.py_exec_bytecode(self.code.bytecode, locals=scope)


class ScreenParser(Parser):

    def __init__(self):
        super(ScreenParser, self).__init__("screen")

    def parse(self, l, name="_name"):

        location = l.get_location()
        screen = ScreenLangScreen()

        def parse_keyword(l):
            if l.match('modal'):
                screen.modal = l.require(l.simple_expression)
                return True

            if l.match('zorder'):
                screen.zorder = l.require(l.simple_expression)
                return True

            if l.match('tag'):
                screen.tag = l.require(l.word)
                return True

            if l.match('variant'):
                screen.variant = l.require(l.simple_expression)
                return True

            if l.match('predict'):
                screen.predict = l.require(l.simple_expression)
                return True

            return False

        lineno = l.number

        screen.name = l.require(l.word)
        screen.parameters = renpy.parser.parse_parameters(l)

        while parse_keyword(l):
            continue

        l.require(':')
        l.expect_eol()
        l.expect_block('screen statement')

        l = l.subblock_lexer()

        rv = [ ]
        count = 0

        while l.advance():

            if parse_keyword(l):
                while parse_keyword(l):
                    continue

                l.expect_eol()
                continue

            c = self.parse_statement(l)

            if c is None:
                l.error('Expected a screen language statement.')

            rv.append(c)
            count += 1

        # TODO: Turn rv into something useful.
        for i in rv:
            ctx = slast.SLContext()
            i.prepare()
            i.execute(ctx)

        return screen

class DisplayableParser(Parser):
    """
    This is responsible for parsing statements that create displayables.
    """

    def __init__(self, name, displayable, nchildren=0, scope=False):

        super(DisplayableParser, self).__init__(name)

        # The displayable that is called when this statement runs.
        self.displayable = displayable

        # The number of children we have.
        self.nchildren = nchildren

        # Add us to the appropriate lists.
        global parser
        parser = self

        if nchildren != 0:
            childbearing_statements.append(self)

        self.scope = scope

    def parse_layout(self, l):
        return self.parse(l, True)

    def parse(self, l, layout_mode=False):
        seen_keywords = set()

        # Parses a keyword argument from the lexer.
        def parse_keyword(l):
            name = l.word()

            if name is None:
                l.error('expected a keyword argument, colon, or end of line.')

            if name not in self.keyword:
                l.error('%r is not a keyword argument or valid child for the %s statement.' % (name, self.name))

            if name in seen_keywords:
                l.error('keyword argument %r appears more than once in a %s statement.' % (name, self.name))

            seen_keywords.add(name)

            expr = l.simple_expression()

            rv.keyword.append((name, expr))

        rv = slast.SLDisplayable(self.displayable, scope=self.scope, child_or_fixed=(self.nchildren == 1))

        # We assume that the initial keyword has been parsed already,
        # so we start with the positional arguments.

        for _i in self.positional:
            rv.positional.append(l.simple_expression())

        # Next, we allow keyword arguments on the starting line.
        while True:
            if l.match(':'):
                l.expect_eol()
                l.expect_block(self.name)
                block = True
                break

            if l.eol():
                l.expect_noblock(self.name)
                block = False
                break

            parse_keyword(l)

        # The index of the child we're adding to this statement.
        child_index = 0

        # A list of lexers we need to parse the contents of.
        lexers = [ ]

        if block:
            lexers.append(l.subblock_lexer())

        if layout_mode:
            lexers.append(l)

        # If we have a block, parse it. This also takes care of parsing the
        # block of a has clause.

        for l in lexers:

            while l.advance():

                state = l.checkpoint()

                if l.keyword(r'has'):
                    if self.nchildren != 1:
                        l.error("The %s statement does not take a layout." % self.name)

                    if child_index != 0:
                        l.error("The has statement may not be given after a child has been supplied.")

                    c = self.parse_statement(l, layout_mode=True)

                    if c is None:
                        l.error('Has expects a child statement.')

                    rv.children.append(c)

                    continue

                c = self.parse_statement(l)

                if c is not None:
                    rv.children.append(c)

                    child_index += 1

                    continue

                l.revert(state)

                while not l.eol():
                    parse_keyword(l)

        return rv


screen_parser = ScreenParser()

def init():
    screen_parser.add(all_statements)

    for i in childbearing_statements:
        i.add(all_statements)

def parse_screen(l):
    """
    Parses the screen statement.
    """

    screen_parser.parse(l)

