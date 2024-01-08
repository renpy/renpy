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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *
from typing import Any, Callable, Literal


import collections

import renpy
import renpy.sl2.slast as slast

from ast import literal_eval

# A tuple of style prefixes that we know of.
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

# The names of all statements known to SL.
# a map of "parser_name": Parser
statements = dict()

# A list of statements that are valid anywhere a child can be placed.
all_child_statements = [ ]

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


# This is a map from (prefix, use_style_prefixes) to a set of property names.
properties = collections.defaultdict(set)


class Keyword(object):
    """
    This represents an optional keyword parameter to a function.
    """

    def __init__(self, name):
        self.name = name

        properties['', False].add(name)

        if parser:
            parser.add(self)


class Style(object):
    """
    This represents a style parameter to a function.
    """

    def __init__(self, name):
        self.name = name

        properties['', True].add(self.name)

        if parser:
            parser.add(self)


class PrefixStyle(object):
    """
    This represents a prefixed style parameter to a function.
    """

    def __init__(self, prefix, name):
        self.prefix = prefix
        self.name = name

        properties[prefix, True].add(self.name)

        if parser:
            parser.add(self)


from renpy.styledata.stylesets import proxy_properties as incompatible_props

def check_incompatible_props(new, olds):
    """
    Takes a property and a set of already-seen properties, and checks
    to see if the new is incompatible with any of the old ones.
    """
    newly_set = incompatible_props.get(new, set()) | {new}

    for old in olds:
        if newly_set.intersection(incompatible_props.get(old, (old,))):
            return old

    return False

class Parser(object):

    # The number of children this statement takes, out of 0, 1, or "many".
    # This defaults to "many" so the has statement errors out when not
    # inside something that takes a single child.
    nchildren = "many"

    def __init__(self, name, child_statement=True):

        # The name of this object.
        self.name = name

        # The positional arguments, keyword arguments, and child
        # statements of this statement.
        self.positional = [ ]
        self.keyword = { }
        self.children = { }

        statements[name] = self

        # True if this parser takes "as".
        self.variable = False

        if child_statement:
            all_child_statements.append(self)

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

    def parse_statement(self, loc, l, layout_mode=False, keyword=True):
        word = l.word() or l.match(r'\$')

        if word and word in self.children:
            if layout_mode:
                c = self.children[word].parse_layout(loc, l, self, keyword)
            else:
                c = self.children[word].parse(loc, l, self, keyword)

            return c
        else:
            return None

    def parse_layout(self, loc, l, parent, keyword):
        l.error("The %s statement cannot be used as a container for the has statement." % self.name)

    def parse(self, loc, l, parent, keyword):
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

    def parse_contents(self, l, target, layout_mode=False, can_has=False, can_tag=False, block_only=False, keyword=True):
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
            If true, only parse the block and not the initial properties.
        """

        seen_keywords = set()
        block = False

        # Parses a keyword argument from the lexer.
        def parse_keyword(l, expect, first_line):
            name = l.word()

            if name is None:
                l.error(expect)

            if can_tag and name == "tag":
                if target.tag is not None:
                    l.error('the tag keyword argument appears more than once in a %s statement.' % (self.name,))

                target.tag = l.require(l.word)
                l.expect_noblock(name)
                return True

            if self.variable:
                if name == "as":
                    if target.variable is not None:
                        l.error('an as clause may only appear once in a %s statement.' % (self.name,))

                    target.variable = l.require(l.word)
                    return

            if name not in self.keyword:
                if name == "continue" or name == "break":
                    l.error("The %s statement may only appear inside a for statement, or an if statement inside a for statement." % name)
                elif name in statements:
                    l.error('The %s statement is not a valid child of the %s statement.' % (name, self.name))
                else:
                    l.error('%r is not a keyword argument or valid child of the %s statement.' % (name, self.name))

            if name == "at" and l.keyword("transform"):

                if target.atl_transform is not None:
                    l.error("More than one 'at transform' block is given.")

                l.require(":")
                l.expect_eol()
                l.expect_block("ATL block")
                expr = renpy.atl.parse_atl(l.subblock_lexer())
                target.atl_transform = expr
                return

            if name in seen_keywords:
                l.error('keyword argument %r appears more than once in a %s statement.' % (name, self.name))
            incomprop = check_incompatible_props(name, seen_keywords)
            if incomprop:
                l.deferred_error("check_conflicting_properties", 'keyword argument {!r} is incompatible with {!r}.'.format(name, incomprop))

            if name == "at" and target.atl_transform:
                l.error("The 'at' property must occur before the 'at transform' block.")

            seen_keywords.add(name)

            expr = l.comma_expression()
            if expr is None:
                l.error("the {} keyword argument was not given a value.".format(name))

            if (not keyword) and (not renpy.config.keyword_after_python):
                try:
                    literal_eval(expr)
                except Exception:
                    l.error("a non-constant keyword argument like '%s %s' is not allowed after a python block." % (name, expr))

            target.keyword.append((name, expr))

            if not first_line:
                l.expect_noblock(name)

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
                    if not target.atl_transform:
                        l.expect_noblock(self.name)
                    block = False
                    break

                parse_keyword(l, 'expected a keyword argument, colon, or end of line.', True)

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
                    if not can_has:
                        l.error("The has statement is not allowed here.")

                    if target.has_noncondition_child():
                        l.error("The has statement may not be given after a child has been supplied.")

                    c = self.parse_statement(loc, l, layout_mode=True, keyword=keyword)

                    if c is None:
                        l.error('Has expects a child statement.')

                    target.children.append(c)

                    if c.has_python():
                        keyword = False

                    continue

                c = self.parse_statement(loc, l)

                # Ignore passes.
                if isinstance(c, slast.SLPass):
                    continue

                # If not none, add the child to our AST.
                if c is not None:
                    target.children.append(c)

                    if c.has_python():
                        keyword = False

                    continue

                l.revert(state)

                if not l.eol():
                    parse_keyword(l, "expected a keyword argument or child statement.", False)

                while not l.eol():
                    parse_keyword(l, "expected a keyword argument or end of line.", False)

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
    
    def copy_properties(self, name):
        global parser
        parser = self

        parser_to_copy = statements.get(name, None)
        if parser_to_copy is None:
            raise Exception("{!r} is not a known screen statement".format(name))
    
        for p in parser_to_copy.positional:
            Positional(p.name)
        
        for v in set(parser_to_copy.keyword.values()):
            if isinstance(v, Keyword):
                Keyword(v.name)

            elif isinstance(v, Style):
                Style(v.name)

            elif isinstance(v, PrefixStyle):
                PrefixStyle(v.prefix, v.name)

        return self


def add(thing):
    parser.add(thing)


# A singleton value.
many = renpy.object.Sentinel("many")


def register_sl_displayable(*args, **kwargs):
    """
    :doc: custom_sl class
    :args: (name, displayable, style, nchildren=0, scope=False, *, replaces=False, default_keywords={}, default_properties=True, unique=False)

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


    `unique`
        This should be set to true if the function returns a  displayable with
        no other references to it.

    The following arguments should be passed in using keyword arguments:

    `replaces`
        If true, and the displayable replaces a prior displayable, that displayable
        is passed as a parameter to the new displayable.

    `default_keywords`
        The default set of keyword arguments to supply to the displayable.

    `default_properties`
        If true, the ui and position properties are added by default.

    Returns an object that can have positional arguments and properties
    added to it by calling the following methods. Each of these methods
    returns the object it is called on, allowing methods to be chained
    together.

    .. method:: add_positional(name)

        Adds a positional argument with `name`

    .. method:: add_property(name)

        Adds a property with `name`. Properties are passed as keyword
        arguments.

    .. method:: add_style_property(name)

        Adds a family of properties, ending with `name` and prefixed with
        the various style property prefixes. For example, if called with
        ("size"), this will define size, idle_size, hover_size, etc.

    .. method:: add_prefix_style_property(prefix, name)

        Adds a family of properties with names consisting of `prefix`,
        a style property prefix, and `name`. For example, if called
        with a prefix of `text_` and a name of `size`, this will
        create text_size, text_idle_size, text_hover_size, etc.

    .. method:: add_property_group(group, prefix='')

        Adds a group of properties, prefixed with `prefix`. `Group` may
        be one of the strings:

        * "bar"
        * "box"
        * "button"
        * "position"
        * "text"
        * "window"

        These correspond to groups of :doc:`style_properties`. Group can
        also be "ui", in which case it adds the :ref:`common ui properties <common-properties>`.
    
    .. method:: copy_properties(name)

        Adds all styles and positional/keyword arguments that can be passed to the `name` screen statement.
    """

    kwargs.setdefault("unique", False)

    rv = DisplayableParser(*args, **kwargs)

    for i in childbearing_statements:
        i.add(rv)

    screen_parser.add(rv)

    if rv.nchildren != 0:
        childbearing_statements.add(rv)

        for i in all_child_statements:
            rv.add(i)

    rv.add(if_statement)
    rv.add(pass_statement)

    return rv


class DisplayableParser(Parser):

    def __init__(self, name, displayable, style, nchildren=0, scope=False,
                 pass_context=False, imagemap=False, replaces=False, default_keywords={},
                 hotspot=False, default_properties=True, unique=False): # type: (str, Callable, str|None, int|Literal["many"]|renpy.object.Sentinel, bool, bool, bool, bool, dict[str, Any], bool, bool, bool) -> None
        """
        `scope`
            If true, the scope is passed into the displayable function as a keyword
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
        self.variable = True
        self.unique = unique

        Keyword("arguments")
        Keyword("properties")
        Keyword("prefer_screen_to_id")

        if default_properties:
            add(renpy.sl2.slproperties.ui_properties)
            add(renpy.sl2.slproperties.position_properties)

    def parse_layout(self, loc, l, parent, keyword):
        return self.parse(loc, l, parent, keyword, layout_mode=True)

    def parse(self, loc, l, parent, keyword, layout_mode=False):

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
            name=self.name,
            unique=self.unique,
            )

        for _i in self.positional:
            expr = l.simple_expression()

            if expr is None:
                break

            rv.positional.append(expr)

        can_has = (self.nchildren == 1)
        self.parse_contents(l, rv, layout_mode=layout_mode, can_has=can_has, can_tag=False)

        if len(rv.positional) != len(self.positional):
            if not rv.keyword_exist("arguments"):
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

    def parse(self, loc, l, parent, keyword):

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
                contents_from.parse_contents(l, block, block_only=True, keyword=keyword)

                rv.entries.append((condition, block))

                state = l.checkpoint()

            elif l.keyword("else"):

                condition = None
                l.require(':')

                block = slast.SLBlock(loc)
                contents_from.parse_contents(l, block, block_only=True, keyword=keyword)

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
                pattern = True
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

    def parse(self, loc, l, parent, keyword):

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

        if l.match('index'):
            index_expression = l.require(l.say_expression)
        else:
            index_expression = None

        l.require('in')

        expression = l.require(l.python_expression)

        l.require(':')
        l.expect_eol()

        rv = slast.SLFor(loc, name, expression, index_expression)

        if code:
            rv.children.append(slast.SLPython(loc, code))

        self.parse_contents(l, rv, block_only=True)

        return rv


for_parser = ForParser("for")


class BreakParser(Parser):

    def parse(self, loc, l, parent, keyword):

        l.expect_eol()
        l.expect_noblock('break statement')

        return slast.SLBreak(loc)

for_parser.add(BreakParser("break", False))

class ContinueParser(Parser):

    def parse(self, loc, l, parent, keyword):

        l.expect_eol()
        l.expect_noblock('continue statement')

        return slast.SLContinue(loc)

for_parser.add(ContinueParser("continue", False))


class OneLinePythonParser(Parser):

    def parse(self, loc, l, parent, keyword):

        loc = l.get_location()
        source = l.require(l.rest_statement)

        l.expect_eol()
        l.expect_noblock("one-line python")

        code = renpy.ast.PyCode(source, loc)
        return slast.SLPython(loc, code)


OneLinePythonParser("$")


class MultiLinePythonParser(Parser):

    def parse(self, loc, l, parent, keyword):

        loc = l.get_location()

        l.require(':')

        l.expect_eol()
        l.expect_block("python block")

        source = l.python_block()

        code = renpy.ast.PyCode(source, loc)
        return slast.SLPython(loc, code)


MultiLinePythonParser("python")


class PassParser(Parser):

    def parse(self, loc, l, parent, keyword):

        l.expect_eol()
        l.expect_noblock('pass statement')

        return slast.SLPass(loc)


pass_statement = PassParser("pass")


class DefaultParser(Parser):

    def parse(self, loc, l, parent, keyword):

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

    def parse(self, loc, l, parent, keyword):

        if l.keyword('expression'):
            target = l.require(l.simple_expression)
            l.keyword('pass')
        else:
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
            self.parse_contents(l, block, can_has=True, block_only=True)

        else:
            l.expect_eol()
            l.expect_noblock("use statement")

            block = None

        return slast.SLUse(loc, target, args, id_expr, block)


UseParser("use")
Keyword("style_prefix")
Keyword("style_group")


class TranscludeParser(Parser):

    def parse(self, loc, l, parent, keyword):
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

    `children`
        The number of children this custom statement takes. This should
        be 0, 1, or "many", which means zero or more.

    `screen`
        The screen to use. If not given, defaults to `name`.

    Returns an object that can have positional arguments and properties
    added to it. This object has the same .add_ methods as the objects
    returned by :class:`renpy.register_sl_displayable`.
    """

    def __init__(self, name, children="many", screen=None):
        Parser.__init__(self, name)

        if children == "many":
            children = many

        for i in childbearing_statements:
            i.add(self)

        screen_parser.add(self)

        self.nchildren = children

        if self.nchildren != 0:
            childbearing_statements.add(self)

            for i in all_child_statements:
                self.add(i)

        self.add_property("arguments")
        self.add_property("properties")

        self.add(if_statement)
        self.add(pass_statement)

        global parser
        parser = None

        # The screen to use.
        if screen is not None:
            self.screen = screen
        else:
            self.screen = name

    def parse(self, loc, l, parent, keyword):

        arguments = [ ]

        # Parse positional arguments.
        for _i in self.positional:
            expr = l.simple_expression()

            if expr is None:
                break

            arguments.append(expr)

        # Parser keyword arguments and children.
        block = slast.SLBlock(loc)
        can_has = (self.nchildren == 1)
        self.parse_contents(l, block, can_has=can_has, can_tag=False)

        if len(arguments) != len(self.positional):
            if not block.keyword_exist("arguments"):
                l.error("{} statement expects {} positional arguments, got {}.".format(self.name, len(self.positional), len(arguments)))

        return slast.SLCustomUse(loc, self.screen, arguments, block)


class ScreenParser(Parser):

    def __init__(self):
        super(ScreenParser, self).__init__("screen", child_statement=False)

    def parse(self, loc, l, parent, name="_name", keyword=True):

        screen = slast.SLScreen(loc)

        screen.name = l.require(l.word)
        screen.parameters = renpy.parser.parse_parameters(l) # type: ignore

        self.parse_contents(l, screen, can_tag=True)

        keyword = dict(screen.keyword)

        screen.modal = keyword.get("modal", "False")
        screen.zorder = keyword.get("zorder", "0")
        screen.variant = keyword.get("variant", "None")
        screen.predict = keyword.get("predict", "None")
        screen.layer = keyword.get("layer", "'screens'")
        screen.sensitive = keyword.get("sensitive", "True")
        screen.roll_forward = keyword.get("roll_forward", "None")

        return screen


screen_parser = ScreenParser()
Keyword("modal")
Keyword("zorder")
Keyword("variant")
Keyword("predict")
Keyword("style_group")
Keyword("style_prefix")
Keyword("layer")
Keyword("sensitive")
Keyword("roll_forward")
parser = None


def init():
    screen_parser.add(all_child_statements)

    for i in all_child_statements:

        if i in childbearing_statements:
            i.add(all_child_statements)
        else:
            i.add(if_statement)
            i.add(pass_statement)


def parse_screen(l, loc):
    """
    Parses the screen statement.
    """

    return screen_parser.parse(loc, l, None)