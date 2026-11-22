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


"""Tests for the PyExpr strings that hold python expressions in the script."""

import pickle

import pytest

from renpy.astsupport import PY_STRICT, PyExpr, make_pyexpr


@pytest.mark.parametrize(
    "args",
    [
        ("x", "a.rpy", 1),
        ("x", "a.rpy", 1, 3),
        ("x", "a.rpy", 1, 3, 1234),
        ("x", "a.rpy", 1, 3, 1234, 5),
    ],
)
def test_existing_pyexprs_are_not_strict(args):
    """
    PyExprs pickled before strictness existed are rebuilt from these argument lists, and must stay lenient, so that
    loading an old .rpyc doesn't turn errors that would happen at runtime into errors that stop the game starting.
    """

    assert PyExpr(*args).strict is False


@pytest.mark.parametrize("strict", [True, False])
def test_strictness_survives_pickling(strict):
    """Strictness is stored in .rpyc files and saves along with the rest of the expression."""

    expr = make_pyexpr("x + 1", "a.rpy", 3, 0, "x + 1", 0, strict)
    loaded = pickle.loads(pickle.dumps(expr))

    assert loaded == "x + 1"
    assert loaded.strict is strict
    assert (loaded.filename, loaded.linenumber, loaded.hashcode) == (expr.filename, expr.linenumber, expr.hashcode)


def test_strictness_does_not_change_hash():
    """The hash keys the bytecode cache, so strict and lenient copies of an expression share compiled code."""

    assert make_pyexpr("x", "a.rpy", 1, 0, "x", 0, True).hashcode == make_pyexpr("x", "a.rpy", 1, 0, "x", 0).hashcode


@pytest.mark.parametrize("py", [4, 4 | PY_STRICT])
def test_invalid_python_version_is_rejected(py):
    """The strict flag doesn't hide an invalid python version in the low bits."""

    with pytest.raises(ValueError):
        PyExpr("x", "a.rpy", 1, py)
