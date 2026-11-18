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


"""Tests for the keyword error messages of the screen language statement parsers in renpy.sl2.slparser."""

import pytest

from renpy.sl2 import slparser


@pytest.fixture(autouse=True)
def screen_children(mocker):
    """
    Gives the screen statement its vbox child for the duration of a test.

    A running game fills in the children of the screen statement in slparser.init(), which the pytest
    engine does not run, so without this "vbox" is not a candidate for the suggestion. Patching a single
    child avoids changing the parser for the other tests.
    """

    mocker.patch.dict(slparser.statements["screen"].children, {"vbox": slparser.statements["vbox"]})


@pytest.mark.parametrize(
    "statement, keyword, expected",
    [
        (
            "text",
            "text_outlines",
            "The text statement does not accept 'text_' prefixed properties. Did you mean: 'outlines'?",
        ),
        (
            "text",
            "selectedidle_color",
            "'selectedidle' is not a valid style property prefix. Did you mean: 'selected_idle'?",
        ),
        (
            "text",
            "outline",
            "'outline' is not a keyword argument or valid child of the text statement. Did you mean: 'outlines'?",
        ),
        (
            "screen",
            "vboz",
            "'vboz' is not a keyword argument or valid child of the screen statement. Did you mean: 'vbox'?",
        ),
        (
            "textbutton",
            "text_outline",
            (
                "'text_outline' is not a keyword argument or valid child of the textbutton statement."
                " Did you mean: 'text_outlines'?"
            ),
        ),
        (
            "text",
            "not_a_property",
            "'not_a_property' is not a keyword argument or valid child of the text statement.",
        ),
    ],
)
def test_keyword_error_suggestions(statement: str, keyword: str, expected: str) -> None:
    """
    A misspelled or misplaced keyword gets an error that names the statement, and suggests the closest
    valid keyword or style prefix when there is one (and no suggestion when nothing is close).
    """

    assert slparser.statements[statement].get_keyword_error(keyword) == expected
