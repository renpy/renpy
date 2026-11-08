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


"""Tests that scriptedit.add_to_ast_before inserts parsed statements into the AST, and leaves it alone on errors."""

from types import SimpleNamespace

import pytest

import renpy
from renpy import scriptedit
from renpy.script import Script

FILENAME = "game/script.rpy"

SOURCE = """\
e "one"
e "two"
e "three"
"""


@pytest.fixture
def script(mocker):
    """
    Installs a Script whose AST was parsed from SOURCE, and returns the first statement of the chain.

    The parser and Script.load_string are real, so inserted code goes through the same parse and name
    assignment as in the interactive director. The Script is built without __init__, which would scan the real
    game, and the line text that scriptedit reads from disk, the context stack, and the rollback log are
    replaced, since the test only looks at the AST. Parse errors are collected into a fresh list.
    """

    script = Script.__new__(Script)
    script.namemap = {}
    script.all_stmts = []
    script.all_pycode = []
    script.need_analysis = []
    script.need_compress = []
    script.record_pycode = True
    script.serial = 0
    script.translator = renpy.translation.ScriptTranslator()

    mocker.patch.object(renpy.game, "script", script)
    mocker.patch.object(renpy.game, "contexts", [])
    mocker.patch.object(renpy.game, "log", SimpleNamespace(replace_node=lambda old, new: None))
    mocker.patch.object(renpy.parser, "parse_errors", [])
    mocker.patch.object(renpy.parser, "deferred_parse_errors", {})
    # Script.load_string rebinds this module global; patching it lets mocker restore the engine's list.
    mocker.patch.object(renpy.parser, "parsed_expressions", [])
    mocker.patch.object(scriptedit, "files", {FILENAME})

    stmts = renpy.parser.parse(FILENAME, SOURCE)
    renpy.ast.chain_block(stmts, None)
    script.all_stmts = renpy.script.collapse_stmts(stmts)

    for number, node in enumerate(script.all_stmts):
        node.name = ("scriptedit", number)

    return stmts[0]


def walk_chain(first):
    """
    Returns the (line number, text) of each statement reachable from `first`, which is the order the game would
    run them in. The text is None for statements without any, like the return at the end.
    """

    rv = []
    node = first

    while node is not None:
        rv.append((node.linenumber, getattr(node, "what", None)))
        node = node.next

    return rv


def test_add_to_ast_before_inserts_statement(script):
    """
    Code added before a line runs before that line's statement, and the statements from that line on move down
    one line, so later edits to the same line numbers still find the right statements.
    """

    scriptedit.add_to_ast_before('e "new"', FILENAME, 2)

    assert walk_chain(script)[:4] == [(1, "one"), (2, "new"), (3, "two"), (4, "three")]


def test_add_to_ast_before_parse_error(script):
    """
    A parse error raises ValueError naming the file and line of the bad code, and the AST is as it was.

    The statements from the given line on are shifted down one line before parsing, so the failure has to
    shift them back up. A shift that is not undone leaves every later statement on the wrong line.
    """

    before = walk_chain(script)

    with pytest.raises(ValueError) as excinfo:
        scriptedit.add_to_ast_before("bogus (", FILENAME, 2)

    assert str(excinfo.value).startswith(f'File "{FILENAME}", line 2')
    assert walk_chain(script) == before
    assert [node.linenumber for node in renpy.game.script.all_stmts] == [number for number, _what in before]
    assert renpy.parser.parse_errors == []
