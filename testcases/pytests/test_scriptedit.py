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


"""Tests that scriptedit.add_to_ast_before reports parse errors and leaves the AST alone when they happen."""

from types import SimpleNamespace

import pytest

import renpy
from renpy import scriptedit


def test_add_to_ast_before_parse_error(mocker):
    """
    A parse error raises ValueError carrying the error text, and the line number shift is undone.

    The script and the node lookups are mocked, since only the handling of load_string's (None, None) result
    is under test. The statement at line 5 is shifted to 6 before parsing, so the undo must shift 6 back.
    """

    old = SimpleNamespace(filename="game/script.rpy", linenumber=5)
    stmts = [old]

    mocker.patch.object(scriptedit, "nodes_on_line_at_or_after", return_value=[old])
    mocker.patch.object(scriptedit, "first_and_last_nodes", return_value=(old, old))
    mocker.patch.object(renpy.game, "script", mocker.Mock(all_stmts=stmts))
    renpy.game.script.load_string.return_value = (None, None)
    mocker.patch.object(renpy.parser, "parse_errors", ["first error", "second error"])
    mocker.patch.object(renpy.parser, "deferred_parse_errors", {})

    with pytest.raises(ValueError) as excinfo:
        scriptedit.add_to_ast_before("bogus (", "game/script.rpy", 5)

    assert str(excinfo.value) == "first error\n\nsecond error"
    assert old.linenumber == 5
    assert renpy.parser.parse_errors == []
