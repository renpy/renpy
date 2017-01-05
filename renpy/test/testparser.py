# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.test.testast as testast
import renpy


def parse_click(l, loc, target):

    rv = testast.Click(loc, target)

    while True:
        if l.keyword('button'):
            rv.button = int(l.require(l.integer))

        elif l.keyword('pos'):
            rv.position = l.require(l.simple_expression)

        elif l.keyword('always'):
            rv.always = True

        else:
            break

    return rv


def parse_type(l, loc, keys):
    rv = testast.Type(loc, keys)

    while True:

        if l.keyword('pattern'):
            rv.pattern = l.require(l.string)

        elif l.keyword('pos'):
            rv.position = l.require(l.simple_expression)

        else:
            break

    return rv


def parse_move(l, loc):
    rv = testast.Move(loc)

    rv.position = l.require(l.simple_expression)

    while True:

        if l.keyword('pattern'):
            rv.pattern = l.require(l.string)

        else:
            break

    return rv


def parse_drag(l, loc):

    points = l.require(l.simple_expression)

    rv = testast.Drag(loc, points)

    while True:
        if l.keyword('button'):
            rv.button = int(l.require(l.integer))

        elif l.keyword('pattern'):
            rv.pattern = l.require(l.string)

        elif l.keyword('steps'):
            rv.steps = int(l.require(l.integer))

        else:
            break

    return rv


def parse_clause(l, loc):
    if l.keyword("run"):

        expr = l.require(l.simple_expression)
        return testast.Action(loc, expr)

    elif l.keyword("pause"):

        expr = l.require(l.simple_expression)
        return testast.Pause(loc, expr)

    elif l.keyword("label"):

        name = l.require(l.name)
        return testast.Label(loc, name)

    elif l.keyword("type"):

        name = l.name()
        if name is not None:
            return parse_type(l, loc, [ name ])

        string = l.require(l.string)

        return parse_type(l, loc, list(string))

    elif l.keyword("drag"):

        return parse_drag(l, loc)

    elif l.keyword("move"):
        return parse_move(l, loc)

    elif l.keyword("click"):
        return parse_click(l, loc, None)

    else:
        target = l.string()
        if target:
            return parse_click(l, loc, target)

    l.error("Expected a test language statement or clause.")
    return testast.Click(loc, target)


def parse_statement(l, loc):

    if l.keyword('python'):

        l.require(':')

        l.expect_block("python block")

        source = l.python_block()

        code = renpy.ast.PyCode(source, loc)
        return testast.Python(loc, code)

    if l.keyword("if"):
        l.expect_block("if block")

        condition = parse_clause(l, loc)
        l.require(':')
        block = parse_block(l.subblock_lexer(False), loc)

        return testast.If(condition, block)

    # Single-line statements only below here.

    l.expect_noblock('statement')

    if l.match(r'\$'):

        source = l.require(l.rest)

        code = renpy.ast.PyCode(source, loc)
        return testast.Python(loc, code)

    elif l.keyword('assert'):
        source = l.require(l.rest)
        return testast.Assert(loc, source)

    elif l.keyword('jump'):
        target = l.require(l.name)
        return testast.Jump(target)

    elif l.keyword('call'):
        target = l.require(l.name)
        return testast.Call(target)

    rv = parse_clause(l, loc)

    if l.keyword("until"):
        right = parse_clause(l, loc)
        rv = testast.Until(rv, right)

    return rv


def parse_block(l, loc):
    """
    Parses a named block of testcase statements.
    """

    block = [ ]

    while l.advance():
        stmt = parse_statement(l, l.get_location())
        block.append(stmt)

        l.expect_eol()

    return testast.Block(loc, block)
