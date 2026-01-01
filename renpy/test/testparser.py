# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

from typing import Any, Collection

import renpy.test.testast as testast
import renpy
from renpy.lexer import Lexer
from renpy.test.types import NodeLocation, HookType

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

    block, _ = parse_block(l.subblock_lexer(False), loc)
    entries.append((condition, block))

    l.advance()

    while l.keyword("elif"):
        new_loc = l.get_location()
        condition = parse_condition(l, loc)
        l.require(":")
        l.expect_eol()
        l.expect_block("elif clause")

        block, _ = parse_block(l.subblock_lexer(False), new_loc)
        entries.append((condition, block))

        l.advance()

    if l.keyword("else"):
        new_loc = l.get_location()
        l.require(":")
        l.expect_eol()
        l.expect_block("else clause")

        block, _ = parse_block(l.subblock_lexer(False), new_loc)
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
def drag_statement(l: Lexer, loc: NodeLocation) -> testast.Drag:
    l.expect_noblock("drag statement")

    start_point = testast.SelectorDrivenNode(loc)
    end_point = testast.SelectorDrivenNode(loc)
    rv = testast.Drag(loc, start_point, end_point)

    while True:
        if l.keyword("button"):
            rv.button = int(l.require(l.integer))

        elif l.keyword("steps"):
            rv.steps = int(l.require(l.integer))

        elif l.keyword("pos"):
            start_point.position = l.require(l.simple_expression)

        elif selector := parse_selector(l, loc):
            start_point.selector = selector

        elif l.keyword("to"):
            break

        else:
            raise l.error("Expected 'to' or drag start specification.")

    while True:
        if l.keyword("button"):
            rv.button = int(l.require(l.integer))

        elif l.keyword("steps"):
            rv.steps = int(l.require(l.integer))

        elif l.keyword("pos"):
            end_point.position = l.require(l.simple_expression)

        elif selector := parse_selector(l, loc):
            end_point.selector = selector

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
    l.expect_noblock("scroll statement")

    rv = testast.Scroll(loc)

    while True:
        if l.keyword("amount"):
            rv.amount = int(l.require(l.integer))

        elif l.keyword("pos"):
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
    setup: testast.TestHook | None = None
    before_testsuite: testast.TestHook | None = None
    before_testcase: testast.TestHook | None = None
    after_testcase: testast.TestHook | None = None
    after_testsuite: testast.TestHook | None = None
    teardown: testast.TestHook | None = None
    children: list[testast.TestCase] = []

    name = l.require(l.dotted_name)
    # global_testsuite_name = renpy.test.testexecution.global_testsuite_name

    # if name == global_testsuite_name:
    #     l.error(f"The name {global_testsuite_name!r} is reserved for a testsuite that runs all tests.")

    l.require(":")
    l.expect_eol()
    l.expect_block("testsuite statement")

    ll = l.subblock_lexer(False)
    ll.advance()

    kwargs: dict[str, Any] = {}
    statements_started = False

    while not ll.eob:
        oldpos = ll.pos
        keyword = ll.word()

        if keyword in ("xfail", "enabled", "only", "description", "parameter"):
            if statements_started:
                ll.error(f"Property {keyword} must be defined before any test statements.")

            if keyword == "parameter":
                kwargs.setdefault("parameters", [])
                kwargs["parameters"].append(parse_testcase_parameters(ll, loc))
            elif keyword == "xfail":
                expr = ll.require(ll.simple_expression)
                kwargs["xfail_expr"] = expr
                ll.expect_eol()
                ll.advance()
            else:
                expr = ll.require(ll.simple_expression)
                kwargs[keyword] = renpy.python.py_eval(expr)
                ll.expect_eol()
                ll.advance()

        else:
            statements_started = True
            ll.pos = oldpos

            if ll.keyword("setup"):
                if setup is not None:
                    ll.error("Only one 'setup' block is allowed in a testsuite.")
                setup = parse_hook(ll, ll.get_location(), HookType.SETUP)

            elif ll.keyword("before"):
                if ll.keyword("testsuite"):
                    if before_testsuite is not None:
                        ll.error("Only one 'before testsuite' block is allowed in a testsuite.")
                    before_testsuite = parse_hook(ll, ll.get_location(), HookType.BEFORE_TESTSUITE)

                elif ll.keyword("testcase"):
                    if before_testcase is not None:
                        ll.error("Only one 'before testcase' block is allowed in a testsuite.")
                    before_testcase = parse_hook(ll, ll.get_location(), HookType.BEFORE_TESTCASE)

                else:
                    ll.error("Expected 'before testsuite' or 'before testcase'.")

            elif ll.keyword("after"):
                if ll.keyword("testcase"):
                    if after_testcase is not None:
                        ll.error("Only one 'after testcase' block is allowed in a testsuite.")
                    after_testcase = parse_hook(ll, ll.get_location(), HookType.AFTER_TESTCASE)

                elif ll.keyword("testsuite"):
                    if after_testsuite is not None:
                        ll.error("Only one 'after testsuite' block is allowed in a testsuite.")
                    after_testsuite = parse_hook(ll, ll.get_location(), HookType.AFTER_TESTSUITE)

                else:
                    ll.error("Expected 'after testsuite' or 'after testcase'.")

            elif ll.keyword("teardown"):
                if teardown is not None:
                    ll.error("Only one 'teardown' block is allowed in a testsuite.")
                teardown = parse_hook(ll, ll.get_location(), HookType.TEARDOWN)

            elif ll.keyword("testcase"):
                children.append(testcase_statement(ll, ll.get_location()))

            elif ll.keyword("testsuite"):
                children.append(testsuite_statement(ll, ll.get_location()))

            else:
                ll.error("Unexpected statement in testsuite.")

    l.advance()

    rv = testast.TestSuite(
        loc,
        name,
        parent=None,
        setup=setup,
        before_testsuite=before_testsuite,
        before_testcase=before_testcase,
        after_testcase=after_testcase,
        after_testsuite=after_testsuite,
        teardown=teardown,
        subtests=children,
        **kwargs,
    )

    return rv


@test_statement("testcase")
def testcase_statement(l: Lexer, loc: NodeLocation) -> testast.TestCase:
    name = l.require(l.dotted_name)
    # signature: renpy.parameter.Signature | None = renpy.parser.parse_parameters(l)
    # extra_kwargs = {}
    # if signature:
    #     signature.apply_defaults(extra_kwargs)

    # global_testsuite_name = renpy.test.testexecution.global_testsuite_name
    # if name == global_testsuite_name:
    #     l.error(f"The name {global_testsuite_name!r} is reserved for a testsuite that runs all tests.")

    l.require(":")
    l.expect_eol()
    l.expect_block("testcase statement")

    test_block, kwargs = parse_block(
        l.subblock_lexer(False), loc, keywords=("xfail", "enabled", "only", "description", "parameter")
    )

    l.advance()

    rv = testast.TestCase(
        loc,
        block=test_block.block,
        name=name,
        parent=None,
        **kwargs,
    )

    return rv


@test_statement("assert")
def assert_statement(l: Lexer, loc: NodeLocation) -> testast.Assert:
    condition = parse_condition(l, loc)
    kwargs: dict[str, Any] = {}

    while True:
        if l.keyword("timeout"):
            kwargs["timeout"] = l.require(l.simple_expression)
        elif l.keyword("xfail"):
            kwargs["xfail_expr"] = l.require(l.simple_expression)
        else:
            break

    l.expect_noblock("assert statement")
    l.expect_eol()
    l.advance()

    return testast.Assert(loc, condition, **kwargs)


@test_statement("screenshot")
def screenshot_statement(l: Lexer, loc: NodeLocation) -> testast.Screenshot:
    l.expect_noblock("screenshot statement")

    name = l.require(l.simple_expression)
    rv = testast.Screenshot(loc, name)

    while True:
        if l.keyword("max_pixel_difference"):
            rv.max_pixel_difference = l.require(l.simple_expression)
        elif l.keyword("crop"):
            rv.crop = l.require(l.simple_expression)
        else:
            break

    l.expect_eol()
    l.advance()

    return rv


@test_statement("python")
def python_statement(l: Lexer, loc: NodeLocation) -> testast.Python:
    hide = l.keyword("hide")

    l.require(":")
    l.expect_eol()

    l.expect_block("python block")

    source = l.python_block()

    l.advance()

    return testast.Python(loc, source, hide == "hide")


@test_statement("$")
def one_line_python_statement(l: Lexer, loc: NodeLocation) -> testast.Python:
    source = l.require(l.rest)

    l.expect_noblock("one-line python statement")
    l.expect_eol()
    l.advance()

    return testast.Python(loc, source)


##############################################################################
# Functions called to parse things.


def parse_block(
    l: Lexer, loc: NodeLocation, keywords: Collection[str] | None = None
) -> tuple[testast.Block, dict[str, Any]]:
    """
    Parses a named block of testcase statements.

    This is the entry point for parsing test statements since it is called
    by renpy.parser on encountering a "testcase" statement
    """

    l.advance()

    block: list[testast.Node] = []
    kwargs: dict[str, Any] = {}
    statements_started = False

    while not l.eob:
        oldpos = l.pos
        keyword = l.word()

        if keywords and isinstance(keyword, str) and keyword in keywords:
            if statements_started:
                l.error(f"Property {keyword} must be defined before any test statements.")

            if keyword == "parameter":
                kwargs.setdefault("parameters", [])
                kwargs["parameters"].append(parse_testcase_parameters(l, loc))
            elif keyword == "xfail":
                expr = l.require(l.simple_expression)
                kwargs["xfail_expr"] = expr
                l.expect_eol()
                l.advance()
            else:
                expr = l.require(l.simple_expression)
                kwargs[keyword] = renpy.python.py_eval(expr)
                l.expect_eol()
                l.advance()
        else:
            l.pos = oldpos
            statements_started = True
            stmt = parse_statement(l, l.get_location())
            if isinstance(stmt, (testast.TestSuite, testast.TestCase)):
                l.unadvance()
                l.error(
                    "A testsuite or testcase may not be nested inside a block. "
                    "It must be at the top level, or within a testsuite."
                )
            block.append(stmt)

    return testast.Block(loc, block), kwargs


def parse_hook(l: Lexer, loc: NodeLocation, hook_type: HookType) -> testast.TestHook:
    l.require(":")
    l.expect_eol()
    l.expect_block(f"hook block: {hook_type}")

    block, kwargs = parse_block(l.subblock_lexer(False), loc, keywords=("xfail", "depth"))

    l.advance()

    if hook_type in (HookType.BEFORE_TESTCASE, HookType.AFTER_TESTCASE):
        kwargs.setdefault("depth", -1)
    elif hook_type in (HookType.BEFORE_TESTSUITE, HookType.AFTER_TESTSUITE):
        kwargs.setdefault("depth", 0)

    return testast.TestHook(loc, block=block.block, name=hook_type.value, parent=None, **kwargs)


def parse_testcase_parameters(l: Lexer, loc: NodeLocation) -> list[dict[str, Any]]:
    l.expect_noblock("parameter statement")

    #  Input: parameter x = [1, 2]
    # Output: [{"x": 1}, {"x": 2}]

    #  Input: parameter (x, y) = [(1,1), (2,2)]
    # Output: [{"x": 1, "y": 1}, {"x": 2, "y": 2}]

    rv: list[dict[str, Any]] = []
    names: list[str] = []

    if l.match(r"\("):
        while True:
            if l.match(r"\)"):
                break
            if l.match(r","):
                continue
            names.append(l.require(l.name))
    else:
        names = [l.require(l.name)]

    if len(names) == 0:
        l.error("Expected at least one name in parameter statement.")
    elif len(names) != len(set(names)):
        l.error("Parameter names in a parameter statement must be unique.")

    l.require("=")

    values_expr = l.require(l.simple_expression)
    values = renpy.python.py_eval(values_expr)

    if not isinstance(values, list) or isinstance(values, str):
        l.error("Expected a list of values in parameter statement.")

    if len(names) == 1:
        rv = []
        for v in values:
            rv.append({names[0]: v})
    else:
        rv = []
        for v in values:
            if not isinstance(v, tuple) or isinstance(v, str):
                l.error("Values must be tuples in parameter statement with multiple parameters.")
            if len(v) != len(names):
                l.error("Length of value tuples must match number of parameters in parameter statement.")
            rv.append(dict(zip(names, v)))

    l.expect_eol()
    l.advance()

    return rv


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
    raw = False

    while True:
        if l.keyword("screen"):
            screen = l.require(l.simple_expression, operator=False)

        elif l.keyword("id"):
            id = l.require(l.simple_expression, operator=False)

        elif l.keyword("layer"):
            layer = l.require(l.simple_expression, operator=False)

        elif l.keyword("focused"):
            focused = True

        elif l.keyword("raw"):
            raw = True

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
        return testast.TextSelector(loc, focused, pattern, raw)

    return testast.DisplayableSelector(loc, screen, id, layer, focused)


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
            return testast.Repeat(loc, left, right, timeout)
        else:
            return testast.Repeat(loc, left, right)

    return None
