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

"""Tests for renpy.test.testcli: the output of `test --list`."""

import pytest

from renpy.test import testcli


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        ([], []),
        (["s", "s.case(x=1)"], ["s", "s.case(x=1)"]),
        (
            ["s", "s.case(x=nan)", "s.case(x=1)", "s.obj(o=<Thing object at 0x1>)", "s.c(t=x) : (y)"],
            ["s", "s.case(x=nan) *", "s.case(x=1)", "s.obj(o=<Thing object at 0x1>) *", "s.c(t=x) : (y) *", "",
             testcli.INVALID_NAME_WARNING],
        ),
    ],
    ids=["empty", "all-valid", "some-invalid"],
)
def test_format_test_list_marks_invalid_names(paths, expected):
    """
    Names that can't be used as filters, because a parameter's repr isn't a Python literal, are marked with an
    asterisk, and the warning explaining the asterisk is printed once at the end. Valid names are printed as they
    are, so they can be pasted into a filter, and no warning is printed when every name is valid.

    The invalid names cover a value that parses but isn't a literal (nan), a repr that isn't valid Python, and a
    repr that closes the parameter parenthesis itself, leaving a colon outside it, which the filter parser rejects
    with DeprecationWarning rather than KeyError.
    """

    assert testcli.format_test_list(paths) == expected
