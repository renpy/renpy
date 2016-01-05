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

import renpy.test.testast as testast
import renpy


def parse_click(l, loc, target):
    return testast.Click(loc, target)


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

    # Single-line statements only below here.

    l.expect_noblock('statement')

    if l.match(r'\$'):

        source = l.require(l.rest)

        code = renpy.ast.PyCode(source, loc)
        return testast.Python(loc, code)

    elif l.keyword('assert'):
        source = l.require(l.rest)
        return testast.Assert(loc, source)

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
