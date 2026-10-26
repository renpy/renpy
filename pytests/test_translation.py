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
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tests for generation of translation identifiers from translatable statements.
"""

from types import SimpleNamespace

import pytest

import renpy
from renpy import ast, translation


class TranslatableStatement(ast.Node):
    """
    A minimal non-say translatable node used to verify which statement code contributes to translation IDs.
    """

    translatable = True
    code: str = ""

    def __init__(self, code: str) -> None:
        super().__init__(("game/translation.rpy", 2))
        self.code = code

    def get_code(self) -> str:
        return self.code


@pytest.fixture
def translation_environment(mocker):
    """
    Provides an empty translator so generated translation IDs are not changed by existing identifiers.
    """

    mocker.patch.object(
        renpy.game,
        "script",
        SimpleNamespace(translator=SimpleNamespace(default_translates={})),
    )


def create_translation_id(non_say_code: str) -> str:
    """
    Creates an identifier for a Say node followed by a non-say translatable node.
    """

    say = ast.Say(("game/translation.rpy", 1), "e", "Hello.", None)
    say.name = ("translation",)

    statements = [say, TranslatableStatement(non_say_code)]
    return translation.Restructurer([]).create_translate(statements)[0].identifier


def test_tlid_only_considers_say_excludes_non_say_code(mocker, translation_environment):
    """
    Checks that the default configuration keeps non-say statements from changing identifiers for dialogue.
    """

    mocker.patch.object(renpy.config, "tlid_only_considers_say", True)

    first = create_translation_id("voice first.ogg")
    second = create_translation_id("voice second.ogg")

    assert first == second


def test_tlid_includes_non_say_code_when_configured(mocker, translation_environment):
    """
    Checks that disabling the say-only compatibility behavior includes non-say statements in identifiers.
    """

    mocker.patch.object(renpy.config, "tlid_only_considers_say", False)

    first = create_translation_id("voice first.ogg")
    second = create_translation_id("voice second.ogg")

    assert first != second
