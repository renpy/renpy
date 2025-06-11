# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import renpy.test.testast as testast
import renpy
from renpy.lexer import Lexer
from renpy.test.types import NodeLocation


def parse_click(l: Lexer, loc: NodeLocation, target: str | None) -> testast.Click:
    rv = testast.Click(loc, target)

    while True:
        if l.keyword("button"):
            rv.button = int(l.require(l.integer))

        elif l.keyword("pos"):
            rv.position = l.require(l.simple_expression)

        elif (target is not None) and l.keyword("always"):
            rv.always = True

        else:
            break

    return rv


def parse_type(l: Lexer, loc: NodeLocation, keys: list[str]) -> testast.Type:
    rv = testast.Type(loc, keys)

    while True:
        if l.keyword("pattern"):
            rv.pattern = l.require(l.string)

        elif l.keyword("pos"):
            rv.position = l.require(l.simple_expression)

        else:
            break

    return rv


def parse_move(l: Lexer, loc: NodeLocation) -> testast.Move:
    rv = testast.Move(loc)

    rv.position = l.require(l.simple_expression)

    while True:

        if l.keyword("pattern"):
            rv.pattern = l.require(l.string)

        else:
            break

    return rv


def parse_drag(l: Lexer, loc: NodeLocation) -> testast.Drag:
    points = l.require(l.simple_expression)

    rv = testast.Drag(loc, points)

    while True:
        if l.keyword("button"):
            rv.button = int(l.require(l.integer))

        elif l.keyword("pattern"):
            rv.pattern = l.require(l.string)

        elif l.keyword("steps"):
            rv.steps = int(l.require(l.integer))

        else:
            break

    return rv


def parse_not(l: Lexer, loc: NodeLocation) -> testast.Not | testast.Clause:
    if l.keyword("not"):
        return testast.Not(loc, parse_not(l, loc))
    else:
        return parse_clause(l, loc)

def parse_and(l: Lexer, loc: NodeLocation) -> testast.And | testast.Clause:
    rv = parse_not(l, loc)
    while l.keyword("and"):
        rv = testast.And(loc, rv, parse_not(l, loc))
    return rv

def parse_or(l: Lexer, loc: NodeLocation) -> testast.Or | testast.Clause:
    rv = parse_and(l, loc)
    while l.keyword("or"):
        rv = testast.Or(loc, rv, parse_and(l, loc))
    return rv

def parse_clause(l: Lexer, loc: NodeLocation) -> testast.Clause:
    if l.match(r"\("):
        rv = parse_or(l, loc)
        l.require(r"\)")
        return rv

    elif l.keyword("run"):

        expr = l.require(l.simple_expression)
        return testast.Action(loc, expr)

    elif l.keyword("pause"):
        expr = l.require(l.simple_expression)
        return testast.Pause(loc, expr)

    elif l.keyword("label"):
        name = l.require(l.label_name)
        return testast.Label(loc, name)

    elif l.keyword("eval"):

        source = l.require(l.simple_expression)
        return testast.Eval(loc, source)

    elif l.keyword("type"):
        name = l.name()
        if name is not None:
            return parse_type(l, loc, [name])

        string = l.require(l.string)

        return parse_type(l, loc, list(string))

    elif l.keyword("drag"):
        return parse_drag(l, loc)

    elif l.keyword("move"):
        return parse_move(l, loc)

    elif l.keyword("click"):
        return parse_click(l, loc, None)

    elif l.keyword("scroll"):
        pattern = l.require(l.string)
        return testast.Scroll(loc, pattern)

    elif l.keyword("pass"):
        return testast.Pass(loc)

    else:
        target = l.string()
        if target:
            return parse_click(l, loc, target)

    l.error("Expected a test language statement or clause.")
    # return testast.Click(loc, target)


def parse_statement(l: Lexer, loc: NodeLocation) -> testast.Node:

    if l.keyword("python"):

        hide = l.keyword("hide")
        l.require(":")

        l.expect_block("python block")

        source = l.python_block()

        code = renpy.ast.PyCode(source, loc, "hide" if hide else "exec")
        return testast.Python(loc, code, hide=="hide")

    if l.keyword("if"):
        l.expect_block("if block")

        condition = parse_clause(l, loc)
        l.require(":")
        block = parse_block(l.subblock_lexer(False), loc)

        return testast.If(loc, condition, block)

    # Single-line statements only below here.

    l.expect_noblock("statement")

    if l.match(r"\$"):
        source = l.require(l.rest)

        code = renpy.ast.PyCode(source, loc)
        return testast.Python(loc, code)

    elif l.keyword("assert"):
        check = parse_clause(l, loc)
        return testast.Assert(loc, check)

    elif l.keyword("jump"):
        target = l.require(l.name)
        return testast.Jump(loc, target)

    elif l.keyword("call"):
        target = l.require(l.name)
        return testast.Call(loc, target)

    elif l.keyword("exit"):
        return testast.Exit(loc)

    rv = parse_clause(l, loc)

    if l.keyword("until"):
        right = parse_clause(l, loc)
        rv = testast.Until(loc, rv, right)

    return rv


def parse_block(l: Lexer, loc: NodeLocation) -> testast.Block:
    """
    Parses a named block of testcase statements.
    """

    block = []

    while l.advance():
        stmt = parse_statement(l, l.get_location())
        block.append(stmt)

        l.expect_eol()

    return testast.Block(loc, block)
