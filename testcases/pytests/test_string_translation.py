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

from types import SimpleNamespace

import pytest

import renpy
from renpy import translation


@pytest.fixture
def translator(mocker):
    """Gives the test a fresh translator, with recording of unknown strings disabled."""

    mocker.patch.object(translation, "update_translations", False)
    return translation.StringTranslator()


@pytest.fixture
def substitution_config(mocker):
    """Configures the engine so substitute() can run outside a game."""

    mocker.patch.object(renpy.config, "new_substitutions", True)
    mocker.patch.object(renpy.config, "interpolate_exprs", True)
    mocker.patch.object(renpy, "store", SimpleNamespace())
    mocker.patch.dict(renpy.python.store_dicts, {}, clear=True)


@pytest.mark.parametrize(
    "old, entries, expected",
    [
        ("Item", {}, "Item"),
        ("Item", {"Item": "Objet"}, "Objet"),
        ("Item", {"Item": ""}, ""),
        ("Item", {"Other": "Autre"}, "Item"),
        ("Item {#gallery}", {"Item ": "Objet"}, "Objet"),
        ("Item {#gallery}", {"Item {#gallery}": "Exact", "Item ": "Fallback"}, "Exact"),
        ("Item {#gallery}", {}, "Item {#gallery}"),
        ("Item {#gallery}", {"Other": "Autre"}, "Item {#gallery}"),
        ("{#one}Item{#two}", {"Item": "Objet"}, "Objet"),
        ("Item {#unfinished", {"Item ": "Wrong"}, "Item {#unfinished"),
        ("Item {#two\nlines}", {"Item ": "Wrong"}, "Item {#two\nlines}"),
        ("", {}, ""),
        ("{color=#fff}Item{/color}", {}, "{color=#fff}Item{/color}"),
        ("Élément [item]", {}, "Élément [item]"),
    ],
)
def test_translate(translator, old, entries, expected):
    """Exact matches win, then matches with {#...} tags removed, and otherwise the original is returned."""

    translator.translations.update(entries)
    assert translator.translate(old) == expected


def test_unknown_tagged_string_is_recorded(mocker, translator):
    """In update mode, an unknown tagged string is recorded once, and its tagless translation is still used."""

    mocker.patch.object(translation, "update_translations", True)
    translator.translations["Item "] = "Objet"

    assert translator.translate("Item {#gallery}") == "Objet"
    assert translator.unknown == ["Item {#gallery}"]

    # The recorded identity translation is now an exact match.
    assert translator.translate("Item {#gallery}") == "Item {#gallery}"
    assert translator.unknown == ["Item {#gallery}"]


def test_unknown_plain_string_is_recorded(mocker, translator):
    """In update mode, an unknown plain string is recorded once."""

    mocker.patch.object(translation, "update_translations", True)

    assert translator.translate("Item") == "Item"
    assert translator.translate("Item") == "Item"
    assert translator.unknown == ["Item"]
    assert translator.translations == {"Item": "Item"}


def test_table_changes_are_seen(translator):
    """An earlier miss does not hide translations added, replaced or removed later."""

    assert translator.translate("Item") == "Item"

    translator.add("Item", "Objet", None)
    assert translator.translate("Item") == "Objet"

    translator.translations["Item"] = "Article"
    assert translator.translate("Item") == "Article"

    del translator.translations["Item"]
    assert translator.translate("Item") == "Item"


@pytest.mark.parametrize("old", [123, b"Item {#tag}"])
def test_non_string_raises(translator, old):
    """Translating something that is not a string raises TypeError."""

    with pytest.raises(TypeError):
        translator.translate(old)


@pytest.mark.usefixtures("substitution_config")
def test_substitute_sees_scope_and_table_changes(mocker, translator):
    """substitute() translates and interpolates using the current scope and translation table."""

    mocker.patch.object(translation, "translate_string", translator.translate)
    scope = {"item": 1}

    assert renpy.substitutions.substitute("Item [item]", scope)[0] == "Item 1"

    scope["item"] = 2
    assert renpy.substitutions.substitute("Item [item]", scope)[0] == "Item 2"

    translator.add("Item [item]", "Objet [item]", None)
    assert renpy.substitutions.substitute("Item [item]", scope)[0] == "Objet 2"


@pytest.mark.usefixtures("substitution_config")
def test_substitute_sees_language_changes(mocker):
    """substitute() uses the table for the current language, including after switching languages."""

    tables = {None: translation.StringTranslator(), "fr": translation.StringTranslator()}
    tables["fr"].add("Item [item]", "Objet [item]", None)

    preferences = SimpleNamespace(language=None)
    mocker.patch.object(renpy.game, "preferences", preferences)
    mocker.patch.object(renpy.game, "script", SimpleNamespace(translator=SimpleNamespace(strings=tables)))
    mocker.patch.object(translation, "update_translations", False)

    assert renpy.substitutions.substitute("Item [item]", {"item": 1})[0] == "Item 1"

    preferences.language = "fr"
    assert renpy.substitutions.substitute("Item [item]", {"item": 1})[0] == "Objet 1"

    preferences.language = None
    assert renpy.substitutions.substitute("Item [item]", {"item": 2})[0] == "Item 2"


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
