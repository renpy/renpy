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


"""Tests for creator-defined statements registered with renpy.statements.register."""

import types

import pytest

import renpy


@pytest.fixture
def registered(mocker):
    """
    Lets a test register creator-defined statements, and removes them afterwards, by restoring the registry and the
    top level of both parse tries.

    Returns a function that registers a statement whose parse function reads a simple expression and then the rest
    of the line, like the statement in issue #7540. The parse function reports an error if the rest is "fail".
    """

    mocker.patch.dict(renpy.statements.registry)
    mocker.patch.dict(renpy.parser.statements.words)
    mocker.patch.dict(renpy.statements.parsers.words)

    def parse_showcg(l):
        rv = (l.simple_expression(), l.rest())

        if rv[1] == "fail":
            l.error("failed")

        return rv

    def register(name, **kwargs):
        renpy.statements.register(name, parse=parse_showcg, execute=lambda o: None, **kwargs)

    return register


def parse_and_compile(mocker, source: str) -> tuple[list, list[str]]:
    """
    Parses `source` the way a script file is loaded, then compiles its expressions. Returns the root statements and
    the parse errors reported by either step.
    """

    errors = mocker.patch.object(renpy.parser, "parse_errors", [])
    mocker.patch.object(renpy.parser, "parsed_expressions", [])

    # The engine isn't loading a game during tests, so there's no Script object. Parsing python statements records
    # their code on it, and update_bytecode compiles that code, so a stand-in with just those fields is enough.
    script = types.SimpleNamespace(record_pycode=True, all_pycode=[])
    mocker.patch.object(renpy.game, "script", script)

    stmts = renpy.parser.parse("game/test_statements.rpy", source)
    renpy.script.Script.update_bytecode(script, renpy.parser.parsed_expressions)  # type: ignore

    return stmts, errors


@pytest.mark.parametrize("rest", ["foo bar", "0foo", "pre underwear"])
def test_lenient_statement_accepts_non_python(registered, mocker, rest):
    """
    By default a creator-defined statement may take text that isn't Python from the lexer, as it could before 8.6.
    The text only fails if the statement evaluates it at runtime. (#7540)
    """

    registered("showcg")

    stmts, errors = parse_and_compile(mocker, f"showcg cg {rest}\n")

    assert errors == []
    assert stmts[0].parsed[1] == ("cg", rest)


def test_strict_statement_reports_non_python(registered, mocker):
    """A statement registered with strict_expression=True reports text that isn't Python when the game loads."""

    registered("showcg", strict_expression=True)

    _, errors = parse_and_compile(mocker, "showcg cg foo bar\n")

    assert len(errors) == 1
    assert "invalid syntax" in errors[0]


@pytest.mark.parametrize("first", ["showcg cg foo bar", "showcg cg fail"])
def test_lenient_statement_does_not_leak(registered, mocker, first):
    """
    Leniency covers only the creator-defined statement, not the Ren'Py statements after it, including when the
    statement's parse function reports an error.

    The return statement is used because its expression is only checked through the strict flag. A python statement
    would be reported anyway, when its code is compiled.
    """

    registered("showcg")

    _, errors = parse_and_compile(mocker, f"{first}\nreturn 1 +\n")

    assert [i for i in errors if "line 2" in i] != []
    assert all("line 2: invalid syntax" in i or "line 1" in i for i in errors)


def test_renpy_block_inside_lenient_statement_is_strict(mocker):
    """
    Ren'Py statements that a lenient creator-defined statement parses with renpy_block are checked like any other
    Ren'Py statement.
    """

    mocker.patch.dict(renpy.statements.registry)
    mocker.patch.dict(renpy.parser.statements.words)
    mocker.patch.dict(renpy.statements.parsers.words)

    def parse_wrapper(l):
        name = l.rest()
        return (name, l.subblock_lexer().renpy_block())

    renpy.statements.register("wrapper", parse=parse_wrapper, block=True, execute=lambda o: None)

    _, errors = parse_and_compile(mocker, "wrapper not python\n    return 1 +\n")

    assert len(errors) == 1
    assert "line 2: invalid syntax" in errors[0]
