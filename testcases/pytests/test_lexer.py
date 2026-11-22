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


"""Tests for the way the lexer turns ranges of script text into python expressions."""

import types

import pytest

import renpy
from renpy.lexer import GroupedLine, Lexer


@pytest.fixture
def parsed_expressions(mocker):
    """
    Replaces the global list of expressions awaiting compilation, so that the expressions these tests make are not
    left behind for other tests to compile.
    """

    return mocker.patch.object(renpy.parser, "parsed_expressions", [])


def make_lexer(text: str, strict_expression: bool = True, subblock: list | None = None) -> Lexer:
    """
    Returns a lexer positioned at the start of a logical line containing `text`, which begins on line 10.
    """

    lexer = Lexer(
        [GroupedLine("test_lexer.rpy", 10, 0, text, subblock or [])],
        strict_expression=strict_expression,
    )
    lexer.advance()

    return lexer


@pytest.mark.parametrize(
    "text, expected",
    [
        ("x:", "x"),
        ("x   :", "x"),
        ("x\n   :", "x"),
        ("x \\\n   :", "x"),
        ("x \\\n   \\\n   :", "x"),
        ("x + \\\n   y \\\n   :", "x + \\\n   y"),
    ],
)
@pytest.mark.parametrize("strict_expression", [True, False])
def test_python_expression_strips_trailing_whitespace(parsed_expressions, text, expected, strict_expression):
    """
    An expression that extends to a delimiter does not include the whitespace before that delimiter, while line
    continuations inside the expression survive.

    A line continuation at the end of the range counts as whitespace. It has to be removed along with its newline,
    since python rejects a source that ends in a backslash. Lenient expressions are stripped the same way.
    """

    expr = make_lexer(text, strict_expression).python_expression()

    assert str(expr) == expected
    assert parsed_expressions == [(expr, "eval")]

    compile(f"(\n{expr}\n)", "test_lexer.rpy", "eval")


def test_stripped_expression_keeps_location(parsed_expressions):
    """
    Stripping both ends leaves the expression located at its first character, and leaves the lexer at the delimiter
    so the caller can still match it.
    """

    lexer = make_lexer("\n    x   :")
    expr = lexer.python_expression()

    assert str(expr) == "x"
    assert (expr.linenumber, expr.column) == (11, 4)
    assert lexer.text[lexer.pos] == ":"


def test_blank_expression_is_empty(parsed_expressions):
    """
    A range holding only whitespace and line continuations gives an empty expression, which is not queued for
    compilation since an empty expression can't be compiled.
    """

    lexer = make_lexer(" \\\n   :")
    expr = lexer.python_expression()

    assert str(expr) == ""
    assert parsed_expressions == []


def test_exec_expression_keeps_whitespace(parsed_expressions):
    """
    Only eval expressions are stripped. Python blocks depend on their exact text for indentation and line numbers.
    """

    text = "    x = 1\n    "
    expr = make_lexer(text)._expr_from_range(0, len(text), "exec")

    assert str(expr) == text


################################################################################
# Strict and lenient expressions.

EVAL_METHODS = {
    "simple_expression": lambda l, **kw: l.simple_expression(**kw),
    "comma_expression": lambda l, **kw: l.comma_expression(**kw),
    "say_expression": lambda l, **kw: l.say_expression(**kw),
    "python_expression": lambda l, **kw: l.python_expression(**kw),
    "delimited_python": lambda l, **kw: l.delimited_python(":", **kw),
}
"""Makes an eval expression from a lexer positioned at "(a):", by each public method that takes `expr`."""

EXPRESSION_METHODS = {
    **EVAL_METHODS,
    "rest": lambda l: l.rest(),
    "arguments": lambda l: l.arguments().arguments[0][1],
}
"""Makes an expression from a lexer positioned at "(a):", by each public method that returns one."""


@pytest.mark.parametrize("method", EXPRESSION_METHODS)
@pytest.mark.parametrize("strict_expression", [True, False])
def test_expression_follows_lexer_mode(parsed_expressions, method, strict_expression):
    """
    By default, an expression is strict when the lexer's mode is. Strictness decides whether update_bytecode
    reports the expression's syntax errors.
    """

    lexer = make_lexer("(a):", strict_expression)
    expr = EXPRESSION_METHODS[method](lexer)

    assert expr.strict is strict_expression


@pytest.mark.parametrize("method", EVAL_METHODS)
def test_expr_true_is_strict(parsed_expressions, method):
    """expr=True makes a strict expression, even in a lenient lexer, without changing the lexer's mode."""

    lexer = make_lexer("(a):", strict_expression=False)
    expr = EVAL_METHODS[method](lexer, expr=True)

    assert expr.strict is True
    assert lexer.strict_expression is False


@pytest.mark.parametrize("method", EVAL_METHODS)
def test_expr_false_is_plain_string(parsed_expressions, method):
    """expr=False returns the expression as a plain string, which is never compiled, so it's never checked."""

    expr = EVAL_METHODS[method](make_lexer("(a):"), expr=False)

    assert type(expr) is str
    assert expr.strip() == "(a)"
    assert parsed_expressions == []


@pytest.mark.parametrize("strict_expression, strict", [(True, False), (False, True)])
def test_rest_strict_overrides_lexer_mode(parsed_expressions, strict_expression, strict):
    """rest's `strict` argument decides the strictness of its exec expression when it isn't None."""

    lexer = make_lexer("x = 1", strict_expression)

    assert lexer.rest(strict=strict).strict is strict
    assert lexer.strict_expression is strict_expression


def test_subblock_lexer_inherits_strictness():
    """A creator-defined statement that lexes its own block keeps its strictness there."""

    child = GroupedLine("test_lexer.rpy", 11, 4, "x", [])
    lexer = make_lexer("parent", strict_expression=False, subblock=[child])

    assert lexer.subblock_lexer().strict_expression is False


@pytest.mark.parametrize("statement", [True, False])
def test_renpy_statements_are_strict(parsed_expressions, mocker, statement):
    """
    Ren'Py statements parsed by a lenient creator-defined statement make strict expressions, and the lexer goes back
    to being lenient afterwards.

    The python statement records its code on the script, which doesn't exist during tests, so a stand-in replaces it.
    """

    mocker.patch.object(renpy.game, "script", types.SimpleNamespace(record_pycode=False, all_pycode=[]))

    lexer = make_lexer("$ x = 1", strict_expression=False)
    lexer.subparses = []

    if statement:
        lexer.renpy_statement()
    else:
        lexer.renpy_block()

    assert [(str(e), e.strict) for e, _ in parsed_expressions] == [("x = 1", True)]
    assert lexer.strict_expression is False
