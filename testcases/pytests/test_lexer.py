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


def make_lexer(text: str) -> Lexer:
    """
    Returns a lexer positioned at the start of a logical line containing `text`, which begins on line 10.
    """

    lexer = Lexer([GroupedLine("test_lexer.rpy", 10, 0, text, [])])
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
def test_python_expression_strips_trailing_whitespace(parsed_expressions, text, expected):
    """
    An expression that extends to a delimiter does not include the whitespace before that delimiter, while line
    continuations inside the expression survive.

    A line continuation at the end of the range counts as whitespace. It has to be removed along with its newline,
    since python rejects a source that ends in a backslash.
    """

    expr = make_lexer(text).python_expression()

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
