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

"""Tests for renpy.parser."""

import pytest

import renpy


def test_translate_strings_are_not_stored_as_expressions(mocker):
    """The strings in a translate strings block are literals, so they shouldn't be stored for compilation."""

    mocker.patch.object(renpy.parser, "parsed_expressions", [])

    source = 'translate french strings:\n    old "Hello"\n    new "Bonjour"\n'
    stmts = renpy.parser.parse("game/tl/french/test.rpy", source)

    assert renpy.parser.parsed_expressions == []

    assert [(i.old, i.new) for i in stmts[0].block] == [("Hello", "Bonjour")]


@pytest.mark.parametrize("text", ['"a" + "b"', "config.version", 'print("a")'])
def test_translate_strings_only_accept_literals(mocker, text):
    """The strings in a translate strings block are never evaluated as Python expressions."""

    errors = mocker.patch.object(renpy.parser, "parse_errors", [])
    mocker.patch.object(renpy.parser, "parsed_expressions", [])

    renpy.parser.parse("game/tl/french/test.rpy", f'translate french strings:\n    old {text}\n    new "b"\n')

    assert len(errors) == 1
    assert "parse string" in errors[0]


@pytest.mark.parametrize("text", ["1", "None", "True", 'b"a"', '["a"]'])
@pytest.mark.parametrize("template", ['old {}\n    new "b"', 'old "a"\n    new {}'])
def test_translate_strings_reject_non_string_literals(mocker, template, text):
    """Both sides of a string translation must be strings."""

    errors = mocker.patch.object(renpy.parser, "parse_errors", [])
    mocker.patch.object(renpy.parser, "parsed_expressions", [])

    renpy.parser.parse("game/tl/french/test.rpy", f"translate french strings:\n    {template.format(text)}\n")

    assert len(errors) == 1
    assert "expected a string" in errors[0]
