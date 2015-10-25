# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.sl2
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
childbearing_statements = set()

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

        global parser
        parser = self

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

    def parse_statement(self, loc, l, layout_mode=False):
        word = l.word() or l.match(r'\$')

        if word and word in self.children:
            if layout_mode:
                c = self.children[word].parse_layout(loc, l, self)
            else:
                c = self.children[word].parse(loc, l, self)

            return c
        else:
            return None

    def parse_layout(self, loc, l, parent):
        l.error("The %s statement cannot be used as a container for the has statement." % self.name)

    def parse(self, loc, l, parent):
        """
        This is expected to parse a function statement, and to return
        a list of python ast statements.

        `loc`
            The location of the current statement.

        `l`
            The lexer.

        `parent`
            The parent Parser of the current statement.
        """

        raise Exception("Not Implemented")

    def parse_contents(self, l, target, layout_mode=False, can_has=False, can_tag=False, block_only=False):
        """
        Parses the remainder of the current line of `l`, and all of its subblock,
        looking for keywords and children.

        `layout_mode`
            If true, parsing continues to the end of `l`, rather than stopping
            with the end of the first logical line.

        `can_has`
            If true, we should parse layouts.

        `can_tag`
            If true, we should parse the ``tag`` keyword, as it's used by
            screens.

        `block_only`
            If true, only parse the
        """

        seen_keywords = set()

        # Parses a keyword argument from the lexer.
        def parse_keyword(l, expect):
            name = l.word()

            if name is None:
                l.error(expect)

            if can_tag and name == "tag":
                if target.tag is not None:
                    l.error('keyword argument %r appears more than once in a %s statement.' % (name, self.name))

                target.tag = l.require(l.word)

                return True

            if name not in self.keyword:
                l.error('%r is not a keyword argument or valid child for the %s statement.' % (name, self.name))

            if name in seen_keywords:
                l.error('keyword argument %r appears more than once in a %s statement.' % (name, self.name))

            seen_keywords.add(name)


            expr = l.comma_expression()

            target.keyword.append((name, expr))

        if block_only:
            l.expect_eol()
            l.expect_block(self.name)
            block = True

        else:

            # If not block_only, we allow keyword arguments on the starting
            # line.
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

                parse_keyword(l, 'expected a keyword argument, colon, or end of line.')


        # The index of the child we're adding to this statement.
        child_index = 0

        # A list of lexers we need to parse the contents of.
        lexers = [ ]

        if block:
            lexers.append(l.subblock_lexer())

        if layout_mode:
            lexers.append(l)

        # If we have a block, parse it. This also takes care of parsing the
        # block after a has clause.

        for l in lexers:

            while l.advance():

                state = l.checkpoint()
                loc = l.get_location()

                if l.keyword(r'has'):
                    if self.nchildren != 1:
                        l.error("The %s statement does not take a layout." % self.name)

                    if child_index != 0:
                        l.error("The has statement may not be given after a child has been supplied.")

                    c = self.parse_statement(loc, l, layout_mode=True)

                    if c is None:
                        l.error('Has expects a child statement.')

                    target.children.append(c)

                    continue

                c = self.parse_statement(loc, l)

                # Ignore passes.
                if isinstance(c, slast.SLPass):
                    continue

                # If not none, add the child to our AST.
                if c is not None:
                    target.children.append(c)
                    child_index += 1
                    continue

                l.revert(state)

                if not l.eol():
                    parse_keyword(l, "expected a keyword argument or child statement.")

                while not l.eol():
                    parse_keyword(l, "expected a keyword argument or end of line.")


    def add_positional(self, name):
        global parser
        parser = self

        Positional(name)
        return self

    def add_property(self, name):
        global parser
        parser = self

        Keyword(name)
        return self

    def add_style_property(self, name):
        global parser
        parser = self

        Style(name)
        return self

    def add_prefix_style_property(self, prefix, name):
        global parser
        parser = self

        PrefixStyle(prefix, name)
        return self

    def add_property_group(self, group, prefix=''):
        global parser
        parser = self

        if group not in renpy.sl2.slproperties.property_groups:
            raise Exception("{!r} is not a known property group.".format(group))

        for prop in renpy.sl2.slproperties.property_groups[group]:
            if isinstance(prop, Keyword):
                Keyword(prefix + prop.name)
            else:
                PrefixStyle(prefix, prop.name)

        return self


def add(thing):
    parser.add(thing)

# A singleton value.
many = renpy.object.Sentinel("many")


def register_sl_displayable(*args, **kwargs):
    """
    :doc: custom_sl class
    :args: (name, displayable, style, nchildren=0, scope=False, replaces=False, default_keywords={})

    Registers a screen language statement that creates a displayable.

    `name`
        The name of the screen language statement, a string containing a Ren'Py
        keyword. This keyword is used to introduce the new statement.

    `displayable`
        This is a function that, when called, returns a displayable
        object. All position arguments, properties, and style properties
        are passed as arguments to this function. Other keyword arguments
        are also given to this function, a described below.

        This must return a Displayable. If it returns multiple displayables,
        the _main attribute of the outermost displayable should be set to
        the "main" displayable - the one that children should be added
        to.

    `style`
        The base name of the style of this displayable. If the style property
        is not given, this will have the style prefix added to it. The
        computed style is passed to the `displayable` function as the
        ``style`` keyword argument.

    `nchildren`
        The number of children of this displayable. One of:

        0
            The displayable takes no children.
        1
            The displayable takes 1 child. If more than one child is given,
            the children are placed in a Fixed.
        "many"
            The displayable takes more than one child.


    The following arguments should be passed in using keyword arguments:

    `replaces`
        If true, and the displayable replaces a prior displayable, that displayable
        is passed as a parameter to the new displayable.

    `default_keywords`
        The default set of keyword arguments to supply to the displayable.

    Returns an object that can have positional arguments and properties
    added to it by calling the following methods. Each of these methods
    returns the object it is called on, allowing methods to be chained
    together.

    .. method:: add_positional(name)

        Adds a positional argument with `name`

    .. method:: add_property(name):

        Adds a property with `name`. Properties are passed as keyword
        arguments.

    .. method:: add_style_property(name):

        Adds a family of properties, ending with `name` and prefixed with
        the various style property prefixes. For example, if called with
        ("size"), this will define size, idle_size, hover_size, etc.

    .. method:: add_prefix_style_property(prefix, name):

        Adds a family of properties with names consisting of `prefix`,
        a style property prefix, and `name`. For example, if called
        with a prefix of `text_` and a name of `size`, this will
        create text_size, text_idle_size, text_hover_size, etc.

    .. method:: add_property_group(group, prefix=''):

        Adds a group of properties, prefixed with `prefix`. `Group` may
        be one of the strings:

        * "bar"
        * "box"
        * "button"
        * "position"
        * "text"
        * "window"

        These correspond to groups of :ref:`style-properties`. Group can
        also be "ui", in which case it adds the :ref:`common ui properties <common-properties>`.
    """

    rv = DisplayableParser(*args, **kwargs)

    for i in childbearing_statements:
        i.add(rv)

    screen_parser.add(rv)

    if rv.nchildren != 0:
        childbearing_statements.add(rv)

        for i in all_statements:
            rv.add(i)

    return rv


class DisplayableParser(Parser):

    def __init__(self, name, displayable, style, nchildren=0, scope=False,
        pass_context=False, imagemap=False, replaces=False, default_keywords={},
        hotspot=False, default_properties=True):

        """
        `scope`
            If true, the scope is passed into the displayable functionas a keyword
            argument named "scope".

        `pass_context`
            If true, the context is passed as the first positional argument of the
            displayable.

        `imagemap`
            If true, the displayable is treated as defining an imagemap. (The imagemap
            is added to and removed from renpy.ui.imagemap_stack as appropriate.)

        `hotspot`
            If true, the displayable is treated as a hotspot. (It needs to be
            re-created if the imagemap it belongs to has changed.)

        `default_properties`
            If true, the ui and positional properties are added by default.
        """

        super(DisplayableParser, self).__init__(name)

        # The displayable that is called when this statement runs.
        self.displayable = displayable

        if nchildren == "many":
            nchildren = many

        # The number of children we have.
        self.nchildren = nchildren

        if nchildren != 0:
            childbearing_statements.add(self)

        self.style = style
        self.scope = scope
        self.pass_context = pass_context
        self.imagemap = imagemap
        self.hotspot = hotspot
        self.replaces = replaces
        self.default_keywords = default_keywords

        Keyword("arguments")
        Keyword("properties")

        if default_properties:
            add(renpy.sl2.slproperties.ui_properties)
            add(renpy.sl2.slproperties.position_properties)


    def parse_layout(self, loc, l, parent):
        return self.parse(loc, l, parent, True)

    def parse(self, loc, l, parent, layout_mode=False):

        rv = slast.SLDisplayable(
            loc,
            self.displayable,
            scope=self.scope,
            child_or_fixed=(self.nchildren == 1),
            style=self.style,
            pass_context=self.pass_context,
            imagemap=self.imagemap,
            replaces=self.replaces,
            default_keywords=self.default_keywords,
            hotspot=self.hotspot,
            )

        for _i in self.positional:
            expr = l.simple_expression()

            if expr is None:
                break

            rv.positional.append(expr)

        can_has = (self.nchildren == 1)
        self.parse_contents(l, rv, layout_mode=layout_mode, can_has=can_has, can_tag=False)

        if len(rv.positional) != len(self.positional):
            for i in rv.keyword:
                if i[0] == 'arguments':
                    break
            else:
                l.error("{} statement expects {} positional arguments, got {}.".format(self.name, len(self.positional), len(rv.positional)))

        return rv

class IfParser(Parser):

    def __init__(self, name, node_type, parent_contents):
        """
        `node_type`
            The type of node to create.

        `parent_contents`
            If true, our children must be children of our parent. Otherwise,
            our children must be children of ourself.
        """

        super(IfParser, self).__init__(name)

        self.node_type = node_type
        self.parent_contents = parent_contents

        if not parent_contents:
            childbearing_statements.add(self)


    def parse(self, loc, l, parent):

        if self.parent_contents:
            contents_from = parent
        else:
            contents_from = self

        rv = self.node_type(loc)

        condition = l.require(l.python_expression)

        l.require(':')

        block = slast.SLBlock(loc)
        contents_from.parse_contents(l, block, block_only=True)

        rv.entries.append((condition, block))

        state = l.checkpoint()

        while l.advance():

            loc = l.get_location()

            if l.keyword("elif"):

                condition = l.require(l.python_expression)
                l.require(':')

                block = slast.SLBlock(loc)
                contents_from.parse_contents(l, block, block_only=True)

                rv.entries.append((condition, block))

                state = l.checkpoint()

            elif l.keyword("else"):

                condition = None
                l.require(':')

                block = slast.SLBlock(loc)
                contents_from.parse_contents(l, block, block_only=True)

                rv.entries.append((condition, block))

                state = l.checkpoint()

                break

            else:
                l.revert(state)
                break

        return rv

if_statement = IfParser("if", slast.SLIf, True)
IfParser("showif", slast.SLShowIf, False)


class ForParser(Parser):

    def __init__(self, name):
        super(ForParser, self).__init__(name)
        childbearing_statements.add(self)

    def name_or_tuple_pattern(self, l):
        """
        Matches either a name or a tuple pattern. If a single name is being
        matched, returns it. Otherwise, returns None.
        """

        name = None
        pattern = False

        while True:

            if l.match(r"\("):
                name = self.name_or_tuple_pattern(l)
                l.require(r'\)')
            else:
                name = l.name()

                if name is None:
                    break

            if l.match(r","):
                pattern = True
            else:
                break

        if pattern:
            return None

        if name is not None:
            return name

        l.error("expected variable or tuple pattern.")

    def parse(self, loc, l, parent):

        l.skip_whitespace()

        tuple_start = l.pos
        name = self.name_or_tuple_pattern(l)

        if not name:
            name = "_sl2_i"
            pattern = l.text[tuple_start:l.pos]
            stmt = pattern + " = " + name
            code = renpy.ast.PyCode(stmt, loc)
        else:
            code = None

        l.require('in')

        expression = l.require(l.python_expression)

        l.require(':')
        l.expect_eol()

        rv = slast.SLFor(loc, name, expression)

        if code:
            rv.children.append(slast.SLPython(loc, code))

        self.parse_contents(l, rv, block_only=True)

        return rv

ForParser("for")


class OneLinePythonParser(Parser):

    def parse(self, loc, l, parent):

        loc = l.get_location()
        source = l.require(l.rest)

        l.expect_eol()
        l.expect_noblock("one-line python")

        code = renpy.ast.PyCode(source, loc)
        return slast.SLPython(loc, code)

OneLinePythonParser("$")


class MultiLinePythonParser(Parser):

    def parse(self, loc, l, parent):

        loc = l.get_location()

        l.require(':')

        l.expect_eol()
        l.expect_block("python block")

        source = l.python_block()

        code = renpy.ast.PyCode(source, loc)
        return slast.SLPython(loc, code)

MultiLinePythonParser("python")


class PassParser(Parser):

    def parse(self, loc, l, parent):

        l.expect_eol()

        return slast.SLPass(loc)

PassParser("pass")


class DefaultParser(Parser):

    def parse(self, loc, l, parent):

        name = l.require(l.word)
        l.require(r'=')
        rest = l.rest()

        l.expect_eol()
        l.expect_noblock('default statement')

        return slast.SLDefault(loc, name, rest)

DefaultParser("default")


class UseParser(Parser):

    def __init__(self, name):
        super(UseParser, self).__init__(name)
        childbearing_statements.add(self)

    def parse(self, loc, l, parent):

        target = l.require(l.word)
        args = renpy.parser.parse_arguments(l)

        if l.keyword('id'):
            id_expr = l.simple_expression()
        else:
            id_expr = None

        if l.match(':'):
            l.expect_eol()
            l.expect_block("use statement")

            block = slast.SLBlock(loc)
            self.parse_contents(l, block, block_only=True)

        else:
            l.expect_eol()
            l.expect_noblock("use statement")

            block = None

        return slast.SLUse(loc, target, args, id_expr, block)

UseParser("use")


class TranscludeParser(Parser):

    def parse(self, loc, l, parent):
        l.expect_eol()
        return slast.SLTransclude(loc)

TranscludeParser("transclude")


class CustomParser(Parser):
    """
    :doc: custom_sl class
    :name: renpy.register_sl_statement

    Registers a custom screen language statement with Ren'Py.

    `name`
        This must be a word. It's the name of the custom screen language
        statement.

    `positional`
        The number of positional parameters this statement takes.

    `children`
        The number of children this custom statement takes. This should
        be 0, 1, or "many", which means zero or more.

    `screen`
        The screen to use. If not given, defaults to `name`.

    Returns an object that can have positional arguments and properties
    added to it. This object has the same .add_ methods as the objects
    returned by :class:`renpy.register_sl_displayable`.
    """

    def __init__(self, name, positional=0, children="many", screen=None):
        Parser.__init__(self, name)

        if children == "many":
            children = many

        for i in childbearing_statements:
            i.add(self)

        screen_parser.add(self)

        self.nchildren = children

        if self.nchildren != 0:
            childbearing_statements.add(self)

            for i in all_statements:
                self.add(i)

        global parser
        parser = None

        # The screen to use.
        if screen is not None:
            self.screen = screen
        else:
            self.screen = name

        # The number of positional parameters required.
        self.positional = positional

    def parse(self, loc, l, parent):

        arguments = [ ]

        # Parse positional arguments.
        for _i in range(self.positional):
            expr = l.require(l.simple_expression)
            arguments.append((None, expr))

        # Parser keyword arguments and children.
        block = slast.SLBlock(loc)
        can_has = (self.nchildren == 1)
        self.parse_contents(l, block, can_has=can_has, can_tag=False)

        # Add the keyword arguments, and create an ArgumentInfo object.
        arguments.extend(block.keyword)
        block.keyword = [ ]

        args = renpy.ast.ArgumentInfo(arguments, None, None)

        # We only need a SLBlock if we have children.
        if not block.children:
            block = None

        # Create the Use statement.
        return slast.SLUse(loc, self.screen, args, None, block)


class ScreenParser(Parser):

    def __init__(self):
        super(ScreenParser, self).__init__("screen")

    def parse(self, loc, l, parent, name="_name"):

        screen = slast.SLScreen(loc)

        screen.name = l.require(l.word)
        screen.parameters = renpy.parser.parse_parameters(l)

        self.parse_contents(l, screen, can_tag=True)

        keyword = dict(screen.keyword)

        screen.modal = keyword.get("modal", "False")
        screen.zorder = keyword.get("zorder", "0")
        screen.variant = keyword.get("variant", "None")
        screen.predict = keyword.get("predict", "None")

        return screen

screen_parser = ScreenParser()
Keyword("modal")
Keyword("zorder")
Keyword("variant")
Keyword("predict")
Keyword("style_group")

def init():
    screen_parser.add(all_statements)

    for i in all_statements:

        if i in childbearing_statements:
            i.add(all_statements)
        else:
            i.add(if_statement)


def parse_screen(l, loc):
    """
    Parses the screen statement.
    """

    return screen_parser.parse(loc, l, None)

