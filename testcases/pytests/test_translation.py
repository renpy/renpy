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
Tests for renpy.translation: generation of translation identifiers from translatable statements, and the
translation of strings.
"""

from types import SimpleNamespace

import pytest

import renpy
from renpy import ast, translation

################################################################################
# Restructurer translation ids
################################################################################


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


GOLDEN_SCRIPT = """\
label start:
    e "Hello."
    e "Hello."
    e happy "Goodbye, \\"friend\\"." (what_italic=True)
    "Narration."
    e "Hello." id explicit_one

label other.sub:
    e "Hello."
"""
"A small script that exercises label prefixes, duplicate lines, explicit ids, and quoting."


def test_translation_ids_are_stable(mocker, translation_environment):
    """
    The identifiers generated for a fixed script are pinned to the values below.

    A translation identifier is the translate statement's name in saves and in translators' tl/ files, so a
    change in how it is computed silently orphans every existing translation. If this test fails because
    the algorithm was changed on purpose, the change needs a compatibility switch like
    config.tlid_only_considers_say, rather than an update to these values.

    The ids come from parsing real script text. A line's id is a hash of its canonical say statement,
    including the speaker, attributes, and arguments, prefixed with the enclosing label. A repeated line gets
    a numeric suffix, a dotted label has its dot replaced, and an explicit id wins, with the generated id
    kept as the alternate.
    """

    mocker.patch.object(renpy.config, "tlid_only_considers_say", True)
    mocker.patch.object(renpy.parser, "parsed_expressions", [])

    stmts = renpy.parser.parse("game/translation.rpy", GOLDEN_SCRIPT)

    for number, node in enumerate(renpy.script.collapse_stmts(stmts)):
        # The restructurer reads names, which the script loader normally assigns. Labels already have theirs.
        if not isinstance(node, ast.Label):
            node.name = ("golden", number)

    translation.restructure(stmts)

    says = [node for node in renpy.script.collapse_stmts(stmts) if isinstance(node, ast.TranslateSay)]

    assert [(node.what, node.identifier, node.alternate) for node in says] == [
        ("Hello.", "start_4e73b00f", None),
        ("Hello.", "start_4e73b00f_1", None),
        ('Goodbye, "friend".', "start_5fc7bae6", None),
        ("Narration.", "start_822c98ab", None),
        ("Hello.", "explicit_one", "start_ffcfebec"),
        ("Hello.", "other_sub_4e73b00f", None),
    ]


################################################################################
# StringTranslator
################################################################################


@pytest.fixture
def translator(mocker):
    """Gives the test a fresh translator, with recording of unknown strings disabled."""

    mocker.patch.object(translation, "update_translations", False)
    return translation.StringTranslator()


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


################################################################################
# is_translatable / require_translatable
################################################################################


@pytest.fixture
def mark_translatable_strings(mocker):
    """Enables the config flag that makes _() mark strings."""

    mocker.patch.object(renpy.config, "mark_translatable_strings", True)


def test_is_translatable(mark_translatable_strings):
    """Strings returned by _() are marked; plain strings and non-strings are not."""

    assert translation.is_translatable(renpy.minstore._("Marked"))
    assert not translation.is_translatable("Marked")
    assert not translation.is_translatable(123)


def test_is_translatable_disabled():
    """When the feature is disabled, no strings are recognized as marked."""

    assert not translation.is_translatable("Marked")
    assert not translation.is_translatable(renpy.minstore._("Marked"))


def test_translatable_str_acts_like_str(mark_translatable_strings):
    """A TranslatableStr compares and hashes like the plain string it wraps."""

    marked = renpy.minstore._("Item {#gallery}")

    assert marked == "Item {#gallery}"
    assert hash(marked) == hash("Item {#gallery}")
    assert isinstance(marked, str)
    assert marked.startswith("Item")


def test_translatable_str_pickles_as_plain_str(mark_translatable_strings):
    """Pickling a marked string produces a plain str, so saves stay simple."""

    import pickle

    marked = renpy.minstore._("Marked")
    unpickled = pickle.loads(pickle.dumps(marked))

    assert unpickled == "Marked"
    assert type(unpickled) is str


def test_require_translatable_passes_when_marked(mocker, mark_translatable_strings):
    """Marked and empty values do not raise."""

    mocker.patch.object(renpy.config, "developer", True)

    translation.require_translatable("name", renpy.minstore._("Marked"))
    translation.require_translatable("name", "")


def test_require_translatable_raises_when_unmarked(mocker, mark_translatable_strings):
    """An unmarked non-empty string raises in developer mode."""

    mocker.patch.object(renpy.config, "developer", True)

    with pytest.raises(Exception):
        translation.require_translatable("name", "Unmarked")


def test_require_translatable_ignored_outside_developer_mode(mocker, mark_translatable_strings):
    """Outside developer mode, require_translatable is a no-op."""

    mocker.patch.object(renpy.config, "developer", False)

    translation.require_translatable("name", "Unmarked")


def test_require_translatable_ignored_when_disabled(mocker):
    """When the feature is disabled, require_translatable is a no-op even in developer mode."""

    mocker.patch.object(renpy.config, "developer", True)

    translation.require_translatable("name", "Unmarked")
