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


"""Tests for the text tokenizer in renpy.text.textsupport."""

import pytest

from renpy.text import textsupport


def tokenize_text(s: str) -> tuple[str, ...]:
    """
    Returns the text runs of the tokenized string `s`, with the tags dropped.
    """

    return tuple(value for kind, value in textsupport.tokenize(s) if kind == textsupport.TEXT)


@pytest.mark.parametrize(
    "source, expected",
    [
        ("abc【", ("abc", "【")),
        ("啊【", ("啊", "【")),
        ("【", ("【",)),
        ("abc【a｜b】", ("abc", "a", "b")),
    ],
)
def test_dangling_lenticular_bracket_is_kept(source: str, expected: tuple[str, ...]) -> None:
    """
    A 【 that ends a text run is kept instead of being dropped.

    GH-7393: The final flush in lenticular_bracket_ruby() only ran for a non-empty buffer, so a text
    run ending in 【 was silently dropped, while a 【 followed by any text survived.
    """

    assert tokenize_text(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        ("【啊", ("【啊",)),
        ("【【", ("【",)),
        ("abc", ("abc",)),
        ("", ()),
        ("【a】", ("【a】",)),
        ("【a｜b", ("a", "b")),
    ],
)
def test_unterminated_lenticular_bracket_behaviour_unchanged(source: str, expected: tuple[str, ...]) -> None:
    """
    Text runs that the final flush already handled keep their existing output.

    The GH-7393 fix must not change these cases, which include brackets that are unterminated or that
    hold no text.
    """

    assert tokenize_text(source) == expected


def test_bracketed_run_becomes_ruby_tags() -> None:
    """
    A complete 【a｜b】 run is still turned into the base and ruby text with rb and rt tags around them.
    """

    tokens = list(textsupport.tokenize("【a｜b】"))

    assert [value for kind, value in tokens if kind == textsupport.TEXT] == ["a", "b"]
    assert [value for kind, value in tokens if kind == textsupport.TAG] == ["rb", "/rb", "rt", "/rt"]
