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


"""Tests that py_compile honors the location embedded in a PyExpr when it returns an AST."""

import pytest

import renpy
from renpy.ast import PyExpr
from renpy.pyanalysis import CompilerCache
from renpy.python import py_compile
from renpy.sl2.slast import compile_expr

FILENAME = "game/x.rpy"
LINE = 42


def test_eval_node_has_pyexpr_line():
    """An expression's AST carries the line of its PyExpr, not a line relative to the expression's source."""

    node = py_compile(PyExpr("a + b", FILENAME, LINE), "eval", ast_node=True)

    assert node.lineno == LINE


def test_exec_nodes_have_pyexpr_line():
    """A block's statement nodes are offset from the PyExpr's line, one source line per statement."""

    nodes = py_compile(PyExpr("x = 1\ny = 2", FILENAME, LINE), "exec", ast_node=True)

    assert [i.lineno for i in nodes] == [LINE, LINE + 1]


def test_eval_node_has_pyexpr_column():
    """The PyExpr's column shifts the first line, so carets in errors point into the .rpy source line."""

    node = py_compile(PyExpr("a + b", FILENAME, LINE, 3, None, 7), "eval", ast_node=True)

    assert (node.col_offset, node.end_col_offset) == (7, 12)


def test_multiline_eval_node_has_pyexpr_line():
    """
    A multi-line expression is compiled wrapped in parentheses on lines of their own. That wrapping must not
    shift the result off the PyExpr's line.
    """

    node = py_compile(PyExpr("a +\nb", FILENAME, LINE), "eval", ast_node=True)

    assert (node.lineno, node.end_lineno) == (LINE, LINE + 1)


def test_syntax_error_reports_pyexpr_location():
    """A syntax error found while building the AST names the PyExpr's file and line."""

    with pytest.raises(SyntaxError) as excinfo:
        py_compile(PyExpr("1 +", FILENAME, LINE), "eval", ast_node=True)

    assert excinfo.value.filename == FILENAME
    assert excinfo.value.lineno == LINE


def test_screen_expression_traceback_line(mocker):
    """
    An exception raised by a compiled screen expression reports the expression's .rpy line.

    This follows the path screen language uses, from the compiler cache through slast.compile_expr. The traceback is
    checked rather than co_firstlineno, which does not follow the AST for eval code. new_ccache is patched so that the
    test's entry is not written to the analysis cache.
    """

    mocker.patch.object(renpy.pyanalysis, "new_ccache", CompilerCache())

    code = compile_expr((FILENAME, LINE), CompilerCache().ast_eval(PyExpr("undefined_name", FILENAME, LINE)))

    with pytest.raises(NameError) as excinfo:
        eval(code, {})

    # The first entry is this test's frame, and the next is the compiled expression's.
    expression_tb = excinfo.tb.tb_next

    assert expression_tb.tb_frame.f_code.co_filename == FILENAME
    assert expression_tb.tb_lineno == LINE


def test_repeated_expression_on_line_keeps_own_column(mocker):
    """
    The same expression text twice on one line, as in `xpos a ypos a`, gets a separate AST for each column.

    A PyExpr compares as a plain string, so the compiler cache has to key on the column explicitly. Otherwise the second
    expression would reuse the first one's node, and errors in it would point at the first one.
    """

    mocker.patch.object(renpy.pyanalysis, "new_ccache", CompilerCache())

    cache = CompilerCache()

    first = cache.ast_eval(PyExpr("a", FILENAME, LINE, 3, None, 5))
    second = cache.ast_eval(PyExpr("a", FILENAME, LINE, 3, None, 20))

    assert (first.col_offset, second.col_offset) == (5, 20)

    first = cache.ast_exec(PyExpr("a", FILENAME, LINE, 3, None, 5))
    second = cache.ast_exec(PyExpr("a", FILENAME, LINE, 3, None, 20))

    assert (first[0].col_offset, second[0].col_offset) == (5, 20)
