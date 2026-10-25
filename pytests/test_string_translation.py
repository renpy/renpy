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
    """Starts with a fresh translation table and restores unknown-string recording after the test."""

    mocker.patch.object(translation, "update_translations", False)
    return translation.StringTranslator()


@pytest.mark.parametrize(
    "old, entries, expected",
    [
        ("Item", {}, "Item"),
        ("Item", {"Item": "Objet"}, "Objet"),
        ("Item", {"Item": ""}, ""),
        ("Item {#gallery}", {"Item ": "Objet"}, "Objet"),
        ("Item {#gallery}", {"Item {#gallery}": "Exact", "Item ": "Fallback"}, "Exact"),
        ("Item {#gallery}", {}, "Item {#gallery}"),
        ("{#one}Item{#two}", {"Item": "Objet"}, "Objet"),
        ("Item {#unfinished", {"Item ": "Wrong"}, "Item {#unfinished"),
        ("Item {#two\nlines}", {"Item ": "Wrong"}, "Item {#two\nlines}"),
        ("", {}, ""),
        ("{color=#fff}Item{/color}", {}, "{color=#fff}Item{/color}"),
        ("Élément [item]", {}, "Élément [item]"),
    ],
)
def test_string_translation_results(translator, old, entries, expected):
    """Exact translations, empty results and complete context tags retain their existing precedence."""

    translator.translations.update(entries)
    assert translator.translate(old) == expected


def test_plain_translation_miss_does_not_scan_for_context_tags(mocker, translator):
    """Plain screen labels do not need the regex used to remove translation context tags."""

    scan = mocker.spy(translation.re, "sub")
    assert translator.translate("Item [item]") == "Item [item]"
    scan.assert_not_called()


def test_unknown_string_tracking_still_precedes_tag_lookup(mocker, translator):
    """Update mode records an unknown original once while still returning its tagless translation."""

    mocker.patch.object(translation, "update_translations", True)
    translator.translations["Item "] = "Objet"
    assert translator.translate("Item {#gallery}") == "Objet"
    assert translator.unknown == ["Item {#gallery}"]
    assert translator.translations["Item {#gallery}"] == "Item {#gallery}"
    assert translator.translate("Item {#gallery}") == "Item {#gallery}"
    assert translator.unknown == ["Item {#gallery}"]


def test_plain_unknown_string_is_recorded_once(mocker, translator):
    """Avoiding tag scanning does not bypass update-mode insertion or duplicate unknown recording."""

    mocker.patch.object(translation, "update_translations", True)
    assert translator.translate("Item") == "Item"
    assert translator.translate("Item") == "Item"
    assert translator.unknown == ["Item"]
    assert translator.translations == {"Item": "Item"}


def test_translation_table_changes_are_visible_without_invalidation(translator):
    """A previous miss cannot mask a later translation addition, replacement or removal."""

    assert translator.translate("Item") == "Item"
    translator.add("Item", "Objet", None)
    assert translator.translate("Item") == "Objet"
    translator.translations["Item"] = "Article"
    assert translator.translate("Item") == "Article"
    del translator.translations["Item"]
    assert translator.translate("Item") == "Item"


def test_custom_mapping_retains_both_lookups(translator):
    """A custom mapping can return a result on the second lookup even for a string without tags."""

    class ChangingMapping(dict):
        def __init__(self):
            super().__init__()
            self.keys_read = []

        def get(self, key, default=None):
            self.keys_read.append(key)
            return default if len(self.keys_read) == 1 else "Second lookup"

    mapping = ChangingMapping()
    translator.translations = mapping
    assert translator.translate("Item") == "Second lookup"
    assert mapping.keys_read == ["Item", "Item"]


def test_str_subclass_does_not_gain_contains_callback(mocker, translator):
    """The exact-string optimization must not introduce contains callbacks on string subclasses."""

    class CustomString(str):
        def __contains__(self, other):
            raise AssertionError("The previous regex path never called __contains__")

    scan = mocker.spy(translation.re, "sub")
    assert translator.translate(CustomString("Item")) == "Item"
    scan.assert_called_once()


@pytest.mark.parametrize("old", [123, b"Item", ["Item"]])
def test_invalid_translation_input_still_raises(translator, old):
    """Non-string misses retain their existing type errors instead of taking a new return path."""

    with pytest.raises(TypeError):
        translator.translate(old)


def test_public_substitution_updates_scope_and_translations(mocker, translator):
    """The public text-substitution path still observes changing values and translation tables."""

    mocker.patch.object(translation, "translate_string", translator.translate)
    mocker.patch.object(renpy.config, "new_substitutions", True)
    mocker.patch.object(renpy.config, "interpolate_exprs", True)
    mocker.patch.object(renpy, "store", SimpleNamespace())
    mocker.patch.dict(renpy.python.store_dicts, {}, clear=True)
    scope = {"item": 1}
    assert renpy.substitutions.substitute("Item [item]", scope)[0] == "Item 1"
    scope["item"] = 2
    assert renpy.substitutions.substitute("Item [item]", scope)[0] == "Item 2"
    translator.add("Item [item]", "Objet [item]", None)
    assert renpy.substitutions.substitute("Item [item]", scope)[0] == "Objet 2"


def test_empty_builtin_table_does_not_scan_tagged_text(mocker, translator):
    """Removing tags cannot find a fallback translation in an empty built-in table."""

    scan = mocker.spy(translation.re, "sub")
    assert translator.translate("Item {#gallery}") == "Item {#gallery}"
    scan.assert_not_called()


def test_public_substitution_observes_language_switches(mocker):
    """An empty default-language table cannot mask a translation after switching languages."""

    tables = {None: translation.StringTranslator(), "fr": translation.StringTranslator()}
    tables["fr"].add("Item [item]", "Objet [item]", None)
    preferences = SimpleNamespace(language=None)
    mocker.patch.object(renpy.game, "preferences", preferences)
    mocker.patch.object(renpy.game, "script", SimpleNamespace(translator=SimpleNamespace(strings=tables)))
    mocker.patch.object(renpy.config, "new_substitutions", True)
    mocker.patch.object(renpy.config, "interpolate_exprs", True)
    mocker.patch.object(renpy, "store", SimpleNamespace())
    mocker.patch.dict(renpy.python.store_dicts, {}, clear=True)
    mocker.patch.object(translation, "update_translations", False)

    assert renpy.substitutions.substitute("Item [item]", {"item": 1})[0] == "Item 1"
    preferences.language = "fr"
    assert renpy.substitutions.substitute("Item [item]", {"item": 1})[0] == "Objet 1"
    preferences.language = None
    assert renpy.substitutions.substitute("Item [item]", {"item": 2})[0] == "Item 2"
