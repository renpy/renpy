"""
Tests for ATL analysis that do not need a running game.
"""

import pytest

import renpy


def analyze_atl(source: str) -> renpy.atl.RawBlock:
    """
    Parses `source` as the body of a transform statement, analyzes it, and returns its raw ATL block.
    """

    body = "".join("    " + line + "\n" for line in source.splitlines())

    # Errors accumulate across parses, and parse returns None while there are any.
    renpy.parser.parse_errors.clear()
    nodes = renpy.parser.parse("atl_probe.rpy", "transform atl_probe(child):\n" + body)
    assert nodes is not None, renpy.parser.parse_errors

    # The transform statement is wrapped in an init block.
    atl = nodes[0].block[0].atl
    atl.analyze()

    return atl


@pytest.mark.parametrize(
    "source",
    [
        "pause 1.0 xpos 0.5",
        "pause 1.0",
        "xpos 0.5\npause 0.5\nrepeat",
        "time 1.0",
        "event done",
        "function renpy.curry(print)",
        "parallel:\n    alpha 0.5\nparallel:\n    pause 1.0 xpos 0.5",
    ],
)
def test_no_child(source):
    """
    ATL with no statement that could show a displayable does not need its child statements replaced.
    """

    assert not analyze_atl(source).has_child


@pytest.mark.parametrize(
    "source",
    [
        "child",
        "'img'",
        "alpha 0.5\nchild",
        "parallel:\n    child\nparallel:\n    alpha 0.5",
        "choice:\n    child",
        "on show:\n    'img'",
        "block:\n    child\n    repeat",
        "contains child",
        "contains:\n    'img'",
    ],
)
def test_child(source):
    """
    ATL with a statement that may show a displayable, at any depth, has its child statements replaced.
    """

    assert analyze_atl(source).has_child
