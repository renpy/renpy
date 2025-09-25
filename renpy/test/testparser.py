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

# The current test case name
current_testsuite_name = ""

# The root of the parse trie.
test_statements = renpy.parser.ParseTrie()


def test_statement(keywords):
    """
    A function decorator used to declare a statement. Keywords is a string
    giving the keywords that precede the statement.
    """

    keywords = keywords.split()

    def wrap(f):
        test_statements.add(keywords, f)
        return f

    return wrap


##############################################################################
# Statement functions: Control Flow


@test_statement("exit")
def exit_statement(l: Lexer, loc: NodeLocation) -> testast.Exit:
    l.expect_noblock("exit statement")
    l.expect_eol()
    l.advance()

    return testast.Exit(loc)


@test_statement("if")
def if_statement(l: Lexer, loc: NodeLocation) -> testast.If:
    entries = []

    condition = parse_condition(l, loc)
    l.require(":")
    l.expect_eol()
    l.expect_block("if statmeent")

    block = parse_block(l.subblock_lexer(False), loc)
    entries.append((condition, block))

    l.advance()

    while l.keyword("elif"):
        new_loc = l.get_location()
        condition = parse_condition(l, loc)
        l.require(":")
        l.expect_eol()
        l.expect_block("elif clause")

        block = parse_block(l.subblock_lexer(False), new_loc)
        entries.append((condition, block))

        l.advance()

    if l.keyword("else"):
        new_loc = l.get_location()
        l.require(":")
        l.expect_eol()
        l.expect_block("else clause")

        block = parse_block(l.subblock_lexer(False), new_loc)
        entries.append((testast.Eval(new_loc, "True"), block))

        l.advance()

    return testast.If(loc, entries)


@test_statement("pass")
def pass_statement(l: Lexer, loc: NodeLocation) -> testast.Pass:
    l.expect_noblock("pass statement")
    l.expect_eol()
    l.advance()

    return testast.Pass(loc)


##############################################################################
# Statement functions: Actions


@test_statement("advance")
def advance_statement(l: Lexer, loc: NodeLocation) -> testast.Advance | testast.Until:
    l.expect_noblock("advance statement")

    rv = testast.Advance(loc)

    if until := parse_until(l, loc, rv):
        rv = until

    l.expect_eol()
    l.advance()

    return rv


@test_statement("click")
def click_statement(l: Lexer, loc: NodeLocation) -> testast.Click | testast.Until:
    l.expect_noblock("click statement")

    rv = testast.Click(loc)

    while True:
        if l.keyword("button"):
            rv.button = int(l.require(l.integer))

        elif l.keyword("pos"):
            rv.position = l.require(l.simple_expression)

        elif l.keyword("always"):
            rv.always = True

        elif selector := parse_selector(l, loc):
            rv.selector = selector

        elif until := parse_until(l, loc, rv):
            rv = until
            break

        else:
            break

    l.expect_eol()
    l.advance()
    return rv


@test_statement("drag")
def drag_statement(l: Lexer, loc: NodeLocation) -> testast.Drag | testast.Until:
    # TODO: Transition off of "pattern"
    l.expect_noblock("drag statement")

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

    l.expect_eol()
    l.advance()
    return rv


@test_statement("keysym")
def keysym_statement(l: Lexer, loc: NodeLocation) -> testast.Keysym | testast.Until:
    l.expect_noblock("keysym statement")

    text = l.require(l.string)
    rv = testast.Keysym(loc, text)

    while True:
        if l.keyword("pos"):
            rv.position = l.require(l.simple_expression)

        elif selector := parse_selector(l, loc):
            rv.selector = selector

        elif until := parse_until(l, loc, rv):
            rv = until
            break

        else:
            break

    l.expect_eol()
    l.advance()
    return rv


@test_statement("move")
def move_statement(l: Lexer, loc: NodeLocation) -> testast.Move | testast.Until:
    l.expect_noblock("move statement")

    rv = testast.Move(loc)

    while True:
        if selector := parse_selector(l, loc):
            rv.selector = selector

        elif until := parse_until(l, loc, rv):
            rv = until
            break

        elif temp := l.simple_expression():
            if isinstance(temp, tuple):
                rv.position = temp
            else:
                l.error("Expected a position tuple for move statement.")

        else:
            break

    l.expect_eol()
    l.advance()
    return rv


@test_statement("pause")
def pause_statement(l: Lexer, loc: NodeLocation) -> testast.Pause | testast.Until:
    """
    Provide a default delay if none is specified with an until clause
    """
    l.expect_noblock("pause statement")

    if until := parse_until(l, loc, testast.Pause(loc, "0.1")):
        rv = until

    else:
        delay = l.require(l.simple_expression)
        rv = testast.Pause(loc, delay)

        if until := parse_until(l, loc, rv):
            rv = until

    l.expect_eol()
    l.advance()
    return rv


@test_statement("run")
def run_statement(l: Lexer, loc: NodeLocation) -> testast.Action | testast.Until:
    l.expect_noblock("run statement")

    expr = l.require(l.simple_expression)
    rv = testast.Action(loc, expr)

    if until := parse_until(l, loc, rv):
        rv = until

    l.expect_eol()
    l.advance()
    return rv


@test_statement("scroll")
def scroll_statement(l: Lexer, loc: NodeLocation) -> testast.Scroll | testast.Until:
    # TODO: Transition off of "pattern"
    l.expect_noblock("scroll statement")

    ## TODO: Update to selector
    pattern = l.require(l.string)
    rv = testast.Scroll(loc, pattern)

    if until := parse_until(l, loc, rv):
        rv = until

    l.expect_eol()
    l.advance()
    return rv


@test_statement("skip")
def skip_statement(l: Lexer, loc: NodeLocation) -> testast.Skip | testast.Until:
    l.expect_noblock("skip statement")

    rv = testast.Skip(loc)

    if l.keyword("fast"):
        rv.fast = True

    if until := parse_until(l, loc, rv):
        rv = until

    l.expect_eol()
    l.advance()

    return rv


@test_statement("type")
def type_statement(l: Lexer, loc: NodeLocation) -> testast.Type | testast.Until:
    l.expect_noblock("type statement")

    text = l.require(l.string)
    rv = testast.Type(loc, text)

    while True:
        if l.keyword("pos"):
            rv.position = l.require(l.simple_expression)

        elif selector := parse_selector(l, loc):
            rv.selector = selector

        elif until := parse_until(l, loc, rv):
            rv = until
            break

        else:
            break

    l.expect_eol()
    l.advance()
    return rv


##############################################################################
# Statement functions: Other (Python, test functions)


@test_statement("testsuite")
def testsuite_statement(l: Lexer, loc: NodeLocation) -> testast.TestSuite:
    global current_testsuite_name

    after: testast.TestHook | None = None
    after_each_case: testast.TestHook | None = None
    after_each_suite: testast.TestHook | None = None
    before: testast.TestHook | None = None
    before_each_case: testast.TestHook | None = None
    before_each_suite: testast.TestHook | None = None
    children: list[testast.TestCase] = []

    name = l.require(l.dotted_name)
    signature = renpy.parser.parse_parameters(l)
    global_testsuite_name = renpy.test.testexecution.global_testsuite_name

    if name == global_testsuite_name and current_testsuite_name:
        l.error(f"The name {global_testsuite_name!r} is reserved for a testsuite that runs all tests.")

    l.require(":")
    l.expect_eol()
    l.expect_block("testsuite statement")

    old_current_testsuite_name = current_testsuite_name
    if current_testsuite_name:
        current_testsuite_name += "." + name
    else:
        current_testsuite_name = name

    ll = l.subblock_lexer(False)
    ll.advance()

    while not ll.eob:
        if ll.keyword("after"):
            if after is not None:
                ll.error("Only one 'after' block is allowed in a testsuite.")
            after = parse_hook(ll, ll.get_location(), "after")

        elif ll.keyword("after_each_case"):
            if after_each_case is not None:
                ll.error("Only one 'after_each_case' block is allowed in a testsuite.")
            after_each_case = parse_hook(ll, ll.get_location(), "after_each_case")

        elif ll.keyword("after_each_suite"):
            if after_each_suite is not None:
                ll.error("Only one 'after_each_suite' block is allowed in a testsuite.")
            after_each_suite = parse_hook(ll, ll.get_location(), "after_each_suite")

        elif ll.keyword("before"):
            if before is not None:
                ll.error("Only one 'before' block is allowed in a testsuite.")
            before = parse_hook(ll, ll.get_location(), "before")

        elif ll.keyword("before_each_case"):
            if before_each_case is not None:
                ll.error("Only one 'before_each_case' block is allowed in a testsuite.")
            before_each_case = parse_hook(ll, ll.get_location(), "before_each_case")

        elif ll.keyword("before_each_suite"):
            if before_each_suite is not None:
                ll.error("Only one 'before_each_suite' block is allowed in a testsuite.")
            before_each_suite = parse_hook(ll, ll.get_location(), "before_each_suite")

        elif ll.keyword("testcase"):
            children.append(testcase_statement(ll, ll.get_location()))

        elif ll.keyword("testsuite"):
            children.append(testsuite_statement(ll, ll.get_location()))

        else:
            ll.error(f"Unexpected statement in testsuite.")

    l.advance()

    extra_kwargs = {}
    if signature:
        signature.apply_defaults(extra_kwargs)

    rv = testast.TestSuite(
        loc,
        current_testsuite_name,
        after=after,
        after_each_case=after_each_case,
        after_each_suite=after_each_suite,
        before=before,
        before_each_case=before_each_case,
        before_each_suite=before_each_suite,
        subtests=children,
        **extra_kwargs,
    )

    current_testsuite_name = old_current_testsuite_name

    return rv


@test_statement("testcase")
def testcase_statement(l: Lexer, loc: NodeLocation) -> testast.TestCase:
    global current_testsuite_name

    name = l.require(l.dotted_name)
    signature: renpy.parameter.Signature | None = renpy.parser.parse_parameters(l)

    global_testsuite_name = renpy.test.testexecution.global_testsuite_name
    if name == global_testsuite_name:
        l.error(f"The name {global_testsuite_name!r} is reserved for a testsuite that runs all tests.")

    l.require(":")
    l.expect_eol()
    l.expect_block("testcase statement")

    test_block = parse_block(l.subblock_lexer(False), loc)

    l.advance()

    extra_kwargs = {}
    if signature:
        signature.apply_defaults(extra_kwargs)

    rv = testast.TestCase(
        loc,
        current_testsuite_name + "." + name if current_testsuite_name else name,
        block=test_block.block,
        **extra_kwargs,
    )

    return rv


@test_statement("assert")
def assert_statement(l: Lexer, loc: NodeLocation) -> testast.Assert:
    condition = parse_condition(l, loc)

    if l.keyword("timeout"):
        timeout = l.require(l.simple_expression)
        timeout = renpy.python.py_eval(timeout)

        if not isinstance(timeout, (int, float)):
            l.error("Expected a number or None for timeout.")

    else:
        timeout = 0.0

    l.expect_noblock("assert statement")
    l.expect_eol()
    l.advance()

    return testast.Assert(loc, condition, timeout)


@test_statement("python")
def python_statement(l: Lexer, loc: NodeLocation) -> testast.Python:
    hide = l.keyword("hide")

    l.require(":")
    l.expect_eol()

    l.expect_block("python block")

    source = l.python_block()

    l.advance()

    code = renpy.ast.PyCode(source, loc, "hide" if hide else "exec")
    return testast.Python(loc, code, hide == "hide")


@test_statement("$")
def one_line_python_statement(l: Lexer, loc: NodeLocation) -> testast.Python:
    source = l.require(l.rest)
    code = renpy.ast.PyCode(source, loc)

    l.expect_noblock("one-line python statement")
    l.expect_eol()
    l.advance()

    return testast.Python(loc, code)


##############################################################################
# Functions called to parse things.


def parse_block(l: Lexer, loc: NodeLocation) -> testast.Block:
    """
    Parses a named block of testcase statements.

    This is the entry point for parsing test statements since it is called
    by renpy.parser on encountering a "testcase" statement
    """

    l.advance()
    block = []

    while not l.eob:
        stmt = parse_statement(l, l.get_location())
        if isinstance(stmt, (testast.TestSuite, testast.TestCase)):
            l.unadvance()
            l.error(
                "A testsuite or testcase may not be nested inside a block. "
                "It must be at the top level, or within a testsuite."
            )
        block.append(stmt)

    return testast.Block(loc, block)


def parse_hook(l: Lexer, loc: NodeLocation, name: str) -> testast.TestHook:
    signature: renpy.parameter.Signature | None = renpy.parser.parse_parameters(l)

    global_testsuite_name = renpy.test.testexecution.global_testsuite_name
    if name == global_testsuite_name:
        l.error(f"The name {global_testsuite_name!r} is reserved for a testsuite that runs all tests.")

    l.require(":")
    l.expect_eol()
    l.expect_block(f"hook block: {name}")

    block = parse_block(l.subblock_lexer(False), loc)

    l.advance()

    extra_kwargs = {}
    if name in ("before_each_case", "after_each_case"):
        extra_kwargs["depth"] = -1
    elif name in ("before_each_suite", "after_each_suite"):
        extra_kwargs["depth"] = 0

    if signature:
        signature.apply_defaults(extra_kwargs)

    return testast.TestHook(loc, f"{current_testsuite_name}.{name}", block.block, **extra_kwargs)


def parse_statement(l: Lexer, loc: NodeLocation) -> testast.Node:
    """
    This parses a Ren'Py test statement. l is expected to be a Ren'Py lexer
    that has been advanced to a logical line.
    """

    pf = test_statements.parse(l)

    if pf is None:
        l.error(f"Expected statement. {l.filename}:{l.line}.")

    return pf(l, loc)


def parse_selector(l: Lexer, loc: NodeLocation) -> testast.Selector | None:
    """
    Parses a selector, which is currently either a pattern (string) or displayable (screen/id).
    """

    pattern = None
    screen = None
    id = None
    layer = None
    focused = False

    while True:
        if l.keyword("screen"):
            screen = l.require(l.word)

        elif l.keyword("id"):
            id = l.require(l.string)

        elif l.keyword("layer"):
            layer = l.require(l.string)

        elif l.keyword("focused"):
            focused = True

        else:
            temp = l.string()
            if temp is not None:
                if pattern is not None:
                    l.error("Only one text pattern may be specified in a selector.")
                pattern = temp
            else:
                break

    if pattern is None and screen is None and id is None:
        return None

    if pattern is not None and (screen is not None or id is not None):
        l.error("A text pattern may not be specified with a screen or id.")

    if pattern is not None:
        return testast.TextSelector(loc, pattern, wait_for_focus=focused)

    return testast.DisplayableSelector(loc, screen, id, layer, wait_for_focus=focused)


def parse_condition(l: Lexer, loc: NodeLocation, left: testast.Condition | None = None) -> testast.Condition:
    """
    Parses a condition that may start with a selector, or
    have one or more "and", "or", "not", or parenthesized conditions.
    """
    if l.keyword("not"):
        right = parse_condition(l, loc)
        return testast.Not(loc, right)

    elif l.keyword("and"):
        if left is None:
            l.error('Expected a left-hand side for "and" condition.')
        right = parse_condition(l, loc)
        return testast.And(loc, left, right)

    elif l.keyword("or"):
        if left is None:
            l.error('Expected a left-hand side for "or" condition.')
        right = parse_condition(l, loc)
        return testast.Or(loc, left, right)

    else:
        if l.match(r"\("):
            rv = parse_condition(l, loc)  # Ensure we are at the start of a condition
            l.require(r"\)")

        elif l.keyword("True"):
            rv = testast.Eval(loc, "True")

        elif l.keyword("False"):
            rv = testast.Eval(loc, "False")

        elif l.keyword("eval"):
            source = l.require(l.simple_expression)
            rv = testast.Eval(loc, source)

        elif l.keyword("label"):
            name = l.require(l.label_name)
            rv = testast.Label(loc, name)

        elif rv := parse_selector(l, loc):
            pass

        else:
            l.error("Invalid condition.")

        ## Check if we have another condition after this one
        old_pos = l.pos
        if l.keyword("and") or l.keyword("or"):
            l.pos = old_pos
            rv = parse_condition(l, loc, left=rv)

        return rv


def parse_until(l: Lexer, loc: NodeLocation, left: testast.Node) -> testast.Until | None:
    """
    Parses an "until" statement. It expects the left side to be a Node,
    and then looks for the "until" keyword, followed by a right side condition.

    If an Until node is returned, the calling function MUST stop parsing
    and return the Until node.
    """
    if l.keyword("until"):
        right = parse_condition(l, loc)

        if l.keyword("timeout"):
            timeout = l.require(l.simple_expression)
            timeout = renpy.python.py_eval(timeout)

            if not isinstance(timeout, (int, float, type(None))):
                l.error("Expected a number or None for timeout.")

            return testast.Until(loc, left, right, timeout)
        else:
            return testast.Until(loc, left, right)

    elif l.keyword("repeat"):
        right = l.require(l.simple_expression)
        right = renpy.python.py_eval(right)
        if not isinstance(right, int):
            l.error("Expected a number for repeat count.")

        if l.keyword("timeout"):
            timeout = l.require(l.simple_expression)
            timeout = renpy.python.py_eval(timeout)

            if not isinstance(timeout, (int, float, type(None))):
                l.error("Expected a number or None for timeout.")

            return testast.Repeat(loc, left, right, timeout)
        else:
            return testast.Repeat(loc, left, right)

    return None
