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

# This module contains the parser for the Ren'Py script language. It's
# called when parsing is necessary, and creates an AST from the script.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import collections
import time

import renpy
import renpy.ast as ast

from renpy.parameter import Parameter

from renpy.lexer import (
    list_logical_lines,
    group_logical_lines,
    ParseError,
    Lexer,

    # Kept imported for older games.
    munge_filename,
    elide_filename,
    unelide_filename,
    get_line_text,
    SubParse,
)

# A list of parse error messages.
parse_errors = [ ]

# A list of deferred parser error. These are potential parse errors that
# can be released or not when parse errors are reported.
deferred_parse_errors = collections.defaultdict(list)

################################################################################
# Parsing of structures that are less than a full statement.

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

        s = l.simple_expression(image=True)

        if s is not None:
            rv.append(str(s))
        else:
            points.pop()

    if nodash:
        for i, p in zip(rv, points):
            if i and i[0] == '-':
                l.revert(p)
                l.skip_whitespace()
                l.error("image name components may not begin with a '-'.")

    return tuple(rv)


def parse_simple_expression_list(l, image=False):
    """
    This parses a comma-separated list of simple_expressions, and
    returns a list of strings. It requires at least one
    simple_expression be present.
    """

    rv = [ l.require(l.simple_expression, image=image) ]

    while True:
        if not l.match(','):
            break

        e = l.simple_expression(image=image)

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
        expression = l.require(l.simple_expression, image=True)
        image_name = (expression.strip(),)
    else:
        image_name = parse_image_name(l, True)
        expression = None

    while True:

        if l.keyword("onlayer"):
            if layer:
                l.error("multiple onlayer clauses are prohibited.")
            else:
                layer = l.require(l.image_name_component)

            continue

        if l.keyword("at"):

            if at_list:
                l.error("multiple at clauses are prohibited.")
            else:
                at_list = parse_simple_expression_list(l, image=True)

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
                zorder = l.require(l.simple_expression, image=True)

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


def parse_menu(stmtl, loc, arguments):

    l = stmtl.subblock_lexer()

    has_choice = False

    say_ast = None
    has_caption = False

    with_ = None
    set = None # @ReservedAssignment


    # Tuples of (label, condition, block)
    items = [ ]
    item_arguments = [ ]

    while l.advance():

        if l.keyword('with'):
            with_ = l.require(l.simple_expression)
            l.expect_eol()
            l.expect_noblock('with clause')

            continue

        if l.keyword('set'):
            set = l.require(l.simple_expression) # @ReservedAssignment
            l.expect_eol()
            l.expect_noblock('set menuitem')

            continue

        # Try to parse a say menuitem.
        state = l.checkpoint()

        who = l.simple_expression()

        attributes = say_attributes(l)

        if l.match(r'\@'):
            temporary_attributes = say_attributes(l)
        else:
            temporary_attributes = None

        what = l.triple_string() or l.string()

        if who is not None and what is not None:

            if has_caption:
                l.error("Say menuitems and captions may not exist in the same menu.")

            if say_ast:
                l.error("Only one say menuitem may exist per menu.")

            say_ast = finish_say(l, l.get_location(), who, what, attributes, temporary_attributes, interact=False)

            l.expect_eol()
            l.expect_noblock("say menuitem")
            continue

        l.revert(state)

        label = l.string()

        if label is None:
            l.error('expected menuitem')

        # A string on a line by itself is a caption.
        if l.eol():

            if l.subblock:
                l.error("Line is followed by a block, despite not being a menu choice. Did you forget a colon at the end of the line?")

            if label and say_ast:
                l.error("Captions and say menuitems may not exist in the same menu.")

            # Only set this if the caption is not "".
            if label:
                has_caption = True

            items.append((label, "True", None))
            item_arguments.append(None)

            continue

        # Otherwise, we have a choice.
        has_choice = True

        condition = "True"

        item_arguments.append(parse_arguments(l))

        if l.keyword('if'):
            condition = l.require(l.python_expression)

        l.require(':')
        l.expect_eol()
        l.expect_block('choice menuitem')

        block = parse_block(l.subblock_lexer())

        items.append((label, condition, block))

    if not has_choice:
        stmtl.error("Menu does not contain any choices.")

    rv = [ ]
    if say_ast:
        rv.append(say_ast)

    rv.append(ast.Menu(loc, items, set, with_, say_ast is not None or has_caption, arguments, item_arguments))

    for index, i in enumerate(rv):
        if index:
            i.rollback = "normal"
        else:
            i.rollback = "force"

    return rv


def parse_parameters(l):
    """
    Parse a list of parameters according to PEP 570 semantic, if one is present.
    """

    if not l.match(r'\('):
        return None

    # Result list of parameters, by (name, default value) pairs
    parameters = collections.OrderedDict()

    # Encountered a slash
    got_slash = False

    # Encountered a star or a *args
    now_kwonly = False

    kind = Parameter.POSITIONAL_OR_KEYWORD

    # Got a lone * and no parameter after it
    missing_kwonly = False

    # Encountered a defaulted parameter
    now_default = False

    def name_parsed(name):
        if name in parameters:
            l.error("duplicate parameter name {!r}".format(name))

    while not l.match(r'\)'):

        if l.match(r'\*\*'):

            extrakw = l.require(l.name)
            name_parsed(extrakw)
            parameters[extrakw] = Parameter(extrakw, Parameter.VAR_KEYWORD)

            if l.match(r'='):
                l.error("a var-keyword parameter (**{}) cannot have a default value".format(extrakw))

            # Allow trailing comma
            l.match(r',')

            # extrakw is always last parameter
            if not l.match(r'\)'):
                l.error("no parameter can follow a var-keyword parameter (**{})".format(extrakw))

            break

        elif l.match(r'\*'):

            if now_kwonly:
                l.error("* may appear only once")

            now_kwonly = True
            kind = Parameter.KEYWORD_ONLY

            # we can have a defaulted pos-or-kw and then a required kw-only
            now_default = False

            extrapos = l.name()

            if extrapos is not None:

                name_parsed(extrapos)
                parameters[extrapos] = Parameter(extrapos, Parameter.VAR_POSITIONAL)

                if l.match(r'='):
                    l.error("a var-positional parameter (*{}) cannot have a default value".format(extrapos))

            else:
                missing_kwonly = True

        elif l.match(r'/\*'):
            l.error("expected comma between / and *")

        elif l.match('/'):

            if now_kwonly:
                l.error("/ must be ahead of *")

            elif got_slash:
                l.error("/ may appear only once")

            elif not parameters:
                l.error("at least one parameter must precede /")

            # All previous parameters are actually positional-only
            parameters = collections.OrderedDict((k, p.replace(kind=p.POSITIONAL_ONLY)) for k, p in parameters.items())

            got_slash = True

        else:

            name = l.require(l.name)

            missing_kwonly = False

            default = Parameter.empty

            if l.match(r'='):
                l.skip_whitespace()
                default = l.delimited_python("),").strip()
                now_default = True

                if not default:
                    l.error("empty default value for parameter {!r}".format(name))

            elif now_default and not now_kwonly:
                l.error("non-default parameter {!r} follows a default parameter".format(name))

            name_parsed(name)
            parameters[name] = Parameter(name, kind=kind, default=default)

        if l.match(r'\)'):
            break

        l.require(r',')

    if missing_kwonly:
        l.error("a bare * must be followed by a parameter")

    return renpy.parameter.Signature(parameters.values())


def parse_arguments(l):
    """
    Parse a list of arguments according to PEP 448 semantics, if one is present.
    """

    if not l.match(r'\('):
        return None

    arguments = [ ]
    starred_indexes = set()
    doublestarred_indexes = set()

    index = 0
    keyword_parsed = False
    names = set()

    while True:
        expect_starred = False
        expect_doublestarred = False
        name = None

        if l.match(r'\)'):
            break

        if l.match(r'\*\*'):
            expect_doublestarred = True
            doublestarred_indexes.add(index)

        elif l.match(r'\*'):
            expect_starred = True
            starred_indexes.add(index)

        state = l.checkpoint()

        if not (expect_starred or expect_doublestarred):
            name = l.word()

            if name and l.match(r'=') and not l.match('='):
                if name in names:
                    l.error("keyword argument repeated: '%s'" % name)
                else:
                    names.add(name)
                keyword_parsed = True

            elif keyword_parsed:
                l.error("positional argument follows keyword argument")

            # If we have not '=' after name, the name itself may be expression.
            else:
                l.revert(state)
                name = None

        l.skip_whitespace()
        arguments.append((name, l.delimited_python("),")))

        if l.match(r'\)'):
            break

        l.require(r',')
        index += 1

    return renpy.parameter.ArgumentInfo(arguments, starred_indexes, doublestarred_indexes)

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


@statement("IF")
def IF_statement(l, loc):

    rv = None

    condition = l.require(l.python_expression)
    l.require(':')
    l.expect_eol()
    l.expect_block('IF statement')

    if renpy.python.py_eval(condition):
        rv = parse_block(l.subblock_lexer())

    l.advance()

    while l.keyword('ELIF'):

        condition = l.require(l.python_expression)
        l.require(':')
        l.expect_eol()
        l.expect_block('ELIF clause')

        if (rv is None) and renpy.python.py_eval(condition):
            rv = parse_block(l.subblock_lexer())

        l.advance()

    if l.keyword('ELSE'):
        l.require(':')
        l.expect_eol()
        l.expect_block('ELSE clause')

        if rv is None:
            rv = parse_block(l.subblock_lexer())

        l.advance()

    if rv is None:
        rv = [ ]

    return rv

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

    arguments = parse_arguments(l)

    l.require(':')
    l.expect_eol()

    menu = parse_menu(l, loc, arguments)

    l.advance()

    rv = [ ]

    if label:
        rv.append(ast.Label(loc, label, [], None))

    rv.extend(menu)

    for i in rv:
        i.statement_start = rv[0]

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

    return ast.Jump(loc, target, expression, (expression and l.global_label or ""))


@statement("call")
def call_statement(l, loc):
    l.expect_noblock('call statement')

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

    rv = [ ast.Call(loc, target, expression, arguments, (expression and l.global_label or "")) ] # type: list[ast.Call|ast.Label|ast.Pass]

    if l.keyword('from'):
        name = l.require(l.label_name_declare)
        rv.append(ast.Label(loc, name, [], None))
    else:
        if renpy.scriptedit.lines and (loc in renpy.scriptedit.lines):
            if expression:
                renpy.add_from.report_missing("expression", renpy.lexer.original_filename, renpy.scriptedit.lines[loc].end)
            else:
                renpy.add_from.report_missing(target, renpy.lexer.original_filename, renpy.scriptedit.lines[loc].end)

    rv.append(ast.Pass(loc))

    l.expect_eol()
    l.advance()

    return rv


@statement("scene")
def scene_statement(l, loc):
    layer = None
    if l.keyword('onlayer'):
        layer = l.require(l.image_name_component)
        l.expect_eol()

    if layer or l.eol():
        # No displayable.
        l.advance()
        return ast.Scene(loc, None, layer)

    imspec = parse_image_specifier(l)
    stmt = ast.Scene(loc, imspec, imspec[4])
    rv = parse_with(l, stmt)

    if l.match(':'):
        l.expect_block('scene statement')
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
        l.expect_block('show statement')
        stmt.atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        l.expect_noblock('show statement')

    l.expect_eol()
    l.advance()

    return rv


@statement("show layer")
def show_layer_statement(l, loc):

    layer = l.require(l.image_name_component)

    if l.keyword("at"):
        at_list = parse_simple_expression_list(l)
    else:
        at_list = [ ]

    if l.match(':'):
        l.expect_block('show layer statement')
        atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        atl = None
        l.expect_noblock('show layer statement')

    l.expect_eol()
    l.advance()

    rv = ast.ShowLayer(loc, layer, at_list, atl)

    return rv


@statement("camera")
def camera_statement(l, loc):

    layer = l.image_name_component() or 'master'

    if l.keyword("at"):
        at_list = parse_simple_expression_list(l)
    else:
        at_list = [ ]

    if l.match(':'):
        l.expect_block('camera statement')
        atl = renpy.atl.parse_atl(l.subblock_lexer())
    else:
        atl = None
        l.expect_noblock('camera statement')

    l.expect_eol()
    l.advance()

    rv = ast.Camera(loc, layer, at_list, atl)

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
        l.expect_block('image statement')
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

    if l.match(r'\['):
        index = l.delimited_python(r']', True)
        l.require(r']')
    else:
        index = None

    if l.match(r'\+='):
        operator = "+="
    elif l.match(r'\|='):
        operator = "|="
    else:
        l.require('=')
        operator = "="

    expr = l.rest()

    if not expr:
        l.error("expected expression")

    l.expect_noblock('define statement')

    rv = ast.Define(loc, store, name, index, operator, expr)

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

    store = 'store'
    name = l.require(l.name)

    while l.match(r'\.'):
        store = store + "." + name
        name = l.require(l.word)

    parameters = parse_parameters(l)

    if parameters:
        found_pos_only = False
        for p in parameters.parameters.values():
            if p.kind == p.POSITIONAL_ONLY and not found_pos_only:
                found_pos_only = True
                l.deferred_error("atl_pos_only", "the transform statement does not take positional-only parameters ({} is not allowed)".format(p))
            elif p.kind == p.VAR_POSITIONAL:
                l.error("the transform statement does not take *args ({} is not allowed)".format(p))
            elif p.kind == p.VAR_KEYWORD:
                l.error("the transform statement does not take **kwargs ({} is not allowed)".format(p))
            elif (p.kind == p.KEYWORD_ONLY) and (p.default is p.empty):
                l.error("the transform statement does not take required keyword-only parameters ({} is not allowed)".format(p))

    l.require(':')
    l.expect_eol()
    l.expect_block('transform statement')

    atl = renpy.atl.parse_atl(l.subblock_lexer())

    rv = ast.Transform(loc, store, name, atl, parameters) #type: ignore

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
    l.expect_eol()

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

        old_init = l.init

        try:
            l.init = True

            checkpoint = l.checkpoint()

            stmt = parse_statement(l)

            if not isinstance(stmt, ast.Node):
                l.revert(checkpoint)
                l.error("init expects a block or statement")

            block = [ stmt ]

        finally:
            l.init = old_init

    return ast.Init(loc, block, priority + l.init_offset)


@statement("rpy monologue")
def rpy_statement(l, loc):

    if l.keyword("double"):
        l.monologue_delimiter = "\n\n"
    elif l.keyword("single"):
        l.monologue_delimiter = "\n"
    elif l.keyword("none"):
        l.monologue_delimiter = ""
    else:
        l.error("rpy monologue expects either none, single or double.")

    l.expect_eol()
    l.expect_noblock('rpy monologue')
    l.advance()

    return [ ]


@statement("screen")
def screen_statement(l, loc):

    slver = l.integer()
    if slver is not None:
        screen_language = int(slver)
        if screen_language < 0 or screen_language > 2:
            l.error("Bad screen language version.")

    screen = renpy.sl2.slparser.parse_screen(l, loc)

    l.advance()

    rv = ast.Screen(loc, screen)

    if not l.init:
        rv = ast.Init(loc, [ rv ], -500 + l.init_offset)

    return rv


@statement("testcase")
def testcase_statement(l, loc):
    name = l.require(l.name)
    l.require(':')
    l.expect_eol()
    l.expect_block('testcase statement')

    ll = l.subblock_lexer()
    ll.set_global_label(name)

    test = renpy.test.testparser.parse_block(ll, loc)

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
            bc = compile(s, "<string>", "eval", renpy.python.new_compile_flags, True)
            return eval(bc, renpy.store.__dict__)
        except Exception:
            ll.error('could not parse string')

    while ll.advance():

        if ll.keyword('old'):

            if old is not None:
                ll.error("previous string is missing a translation")

            loc = ll.get_location()

            try:
                old = parse_string(ll.rest())
            except Exception:
                ll.error("Could not parse string.")

        elif ll.keyword('new'):

            if old is None:
                ll.error('no string to translate')

            newloc = ll.get_location()

            try:
                new = parse_string(ll.rest())
            except Exception:
                ll.error("Could not parse string.")
                new = None

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

translate_none_files = set()

@statement("translate")
def translate_statement(l, loc):

    language = l.require(l.name)

    if language == "None":
        language = None

    identifier = l.require(l.hash)

    if identifier == "strings":
        return translate_strings(loc, language, l)

    elif identifier == "python":
        old_init = l.init

        try:
            l.init = True

            block = [ python_statement(l, loc) ]
            return [ ast.TranslateEarlyBlock(loc, language, block) ]
        finally:
            l.init = old_init

    elif identifier == "style":
        old_init = l.init

        try:
            l.init = True

            block = [ style_statement(l, loc) ]
            return [ ast.TranslateBlock(loc, language, block) ]
        finally:
            l.init = old_init

    l.require(':')
    l.expect_eol()

    if language is None and (loc[0] not in translate_none_files):
        l.deferred_error("check_translate_none", "The `translate None` statement (without style or python) is not allowed. Use say with id instead. (https://www.renpy.org/doc/html/translation.html#tips)")
        translate_none_files.add(loc[0])

    l.expect_block("translate statement")

    block = parse_block(l.subblock_lexer())

    l.advance()

    return [ ast.Translate(loc, identifier, language, block), ast.EndTranslate(loc) ]


@statement("style")
def style_statement(l, loc):

    # Parse priority and name.
    name = l.require(l.word)

    rv = ast.Style(loc, name)

    # Function that parses a clause. This returns true if a clause has been
    # parsed, False otherwise.
    def parse_clause(l):

        if l.keyword("is"):
            if rv.parent is not None:
                l.error("parent clause appears twice.")

            rv.parent = l.require(l.word) # type: ignore
            return True

        if l.keyword("clear"):
            rv.clear = True # type: ignore
            return True

        if l.keyword("take"):
            if rv.take is not None: # type: ignore
                l.error("take clause appears twice.")

            rv.take = l.require(l.name) # type: ignore
            return True

        if l.keyword("del"):
            propname = l.require(l.name)

            if propname not in renpy.style.prefixed_all_properties: # @UndefinedVariable
                l.error("style property %s is not known." % propname)

            rv.delattr.append(propname) # type: ignore
            return True

        if l.keyword("variant"):
            if rv.variant is not None: # type: ignore
                l.error("variant clause appears twice.")

            rv.variant = l.require(l.simple_expression) # type: ignore

            return True

        propname = l.name()

        if propname is not None:
            if (propname != "properties") and (propname not in renpy.style.prefixed_all_properties): # @UndefinedVariable
                l.error("style property %s is not known." % propname)

            if propname in rv.properties: # type: ignore
                l.error("style property %s appears twice." % propname)

            rv.properties[propname] = l.require(l.simple_expression) # type: ignore

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


@statement("rpy python")
def rpy_python(l, loc):

    rv = []

    while (not rv) or l.match(","):

        r = l.match("3") # for compatibility with old code.
        if not r:
            r = l.require(l.word, "__future__ name")

        rv.append(ast.RPY(loc, ("python", r)))

    l.expect_eol()
    l.expect_noblock("rpy statement")

    l.advance()
    return rv


def finish_say(l, loc, who, what, attributes=None, temporary_attributes=None, interact=True):

    if what is None:
        return None

    with_ = None
    arguments = None
    identifier = None

    while True:

        if l.keyword('nointeract'):
            interact = False

        elif l.keyword('with'):
            if with_ is not None:
                l.error('say can only take a single with clause')

            with_ = l.require(l.simple_expression)

        elif l.keyword("id"):

            identifier = l.require(l.name)

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
                rv.append(ast.UserStatement(loc, "nvl clear", [ ], (("nvl", "clear"), { })))
            else:
                rv.append(ast.Say(loc, who, i, with_, attributes=attributes, interact=interact, arguments=arguments, temporary_attributes=temporary_attributes, identifier=identifier))

        return rv

    else:
        return ast.Say(loc, who, what, with_, attributes=attributes, interact=interact, arguments=arguments, temporary_attributes=temporary_attributes, identifier=identifier)


def say_attributes(l):
    """
    Returns a list of say attributes, or None if there aren't any.
    """

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

    return attributes


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

    attributes = say_attributes(l)

    if l.match(r'\@'):
        temporary_attributes = say_attributes(l)
    else:
        temporary_attributes = None

    what = l.triple_string() or l.string()

    if (who is not None) and (what is not None):

        rv = finish_say(l, loc, who, what, attributes, temporary_attributes)

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
    except ParseError as e:
        parse_errors.append(e.message)
        return None

    l = Lexer(nested)

    rv = parse_block(l)

    if parse_errors:
        return None

    if rv:
        rv.append(ast.Return((rv[-1].filename, rv[-1].linenumber), None))

    return rv

def release_deferred_errors():
    """
    Determine which deferred errors should be released, and adds them to  the
    parse_errors list. As new kinds of deferred errors are added, logic should
    be added here to determine which should be released.

    Logic should only depend on early config variables - marked as such
    in ast.EARLY_CONFIG.
    """

    def pop(queue):
        """
        Remove the given queue from the list of deferred errors
        """
        return deferred_parse_errors.pop(queue, ())

    def release(queue):
        """
        Trigger the specified deferred as parse errors.
        """
        parse_errors.extend(pop(queue))

    if renpy.config.check_conflicting_properties:
        release("check_conflicting_properties")
    else:
        pop("check_conflicting_properties")

    if renpy.config.early_developer and renpy.config.check_translate_none:
        release("check_translate_none")
    else:
        pop("check_translate_none")

    if renpy.config.early_developer:
        release("duplicate_id")
    else:
        pop("duplicate_id")

    if renpy.config.atl_pos_only:
        pop("atl_pos_only")
    else:
        release("atl_pos_only")

    if deferred_parse_errors:
        raise Exception("Unknown deferred error label(s) : {}".format(tuple(deferred_parse_errors)))


def get_parse_errors():
    global parse_errors

    release_deferred_errors()

    rv = parse_errors
    parse_errors = [ ]
    return rv


def report_parse_errors():

    release_deferred_errors()

    if not parse_errors:
        return False

    # The sound system may not be ready during exception handling.
    renpy.config.debug_sound = False

    full_text = ""

    f, error_fn = renpy.error.open_error_file("errors.txt", "w")
    with f:
        f.write("\ufeff") # BOM

        print("I'm sorry, but errors were detected in your script. Please correct the", file=f)
        print("errors listed below, and try again.", file=f)
        print("", file=f)

        for i in parse_errors:

            full_text += i
            full_text += "\n\n"

            if not isinstance(i, str):
                i = str(i, "utf-8", "replace")

            print("", file=f)
            print(i, file=f)

            try:
                print("")
                print(i)
            except Exception:
                pass

        print("", file=f)
        print("Ren'Py Version:", renpy.version, file=f)
        print(str(time.ctime()), file=f)

    renpy.display.error.report_parse_errors(full_text, error_fn)

    try:
        if renpy.game.args.command == "run" or renpy.game.args.errors_in_editor: # type: ignore
            renpy.exports.launch_editor([ error_fn ], 1, transient=True)
    except Exception:
        pass

    return True
