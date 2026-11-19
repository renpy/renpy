from types import SimpleNamespace

import pytest

import renpy
from renpy.ast import Scene

################################################################################
# Scene and config.scene
################################################################################


@pytest.fixture(autouse=True)
def stub_statement_state(mocker):
    """
    Stubs the context-dependent parts of Scene.execute (advancing to the next node, naming the statement,
    and showing the image), and makes the image's tag "bg", so only the config.scene call runs and it is
    given a tag that differs from the default of None.
    """

    mocker.patch.object(renpy.ast, "next_node")
    mocker.patch.object(renpy.ast, "statement_name")
    mocker.patch.object(renpy.ast, "get_imspec_tag", return_value="bg")
    mocker.patch.object(renpy.ast, "show_imspec")


def execute_scene() -> None:
    """
    Executes a scene statement with an (otherwise unused) image, on the master layer.
    """

    Scene(("test.rpy", 1), (("bg",), [], None), "master").execute()


def test_hook_without_tag_is_called_without_it(mocker):
    """
    A pre-8.6 game hook, def f(layer="master"), would raise TypeError if passed tag, so it is called without it.
    """

    calls = []

    def hook(layer="master"):
        calls.append(layer)

    mocker.patch.object(renpy.config, "scene", hook)

    execute_scene()

    assert calls == ["master"]


def test_hook_accepting_tag_receives_it(mocker):
    """
    A hook that accepts tag is called once, with the tag keyword.
    """

    calls = []

    def hook(layer="master", tag=None):
        calls.append((layer, tag))

    mocker.patch.object(renpy.config, "scene", hook)

    execute_scene()

    assert calls == [("master", "bg")]


def test_type_error_in_hook_propagates(mocker):
    """
    A TypeError raised inside a hook that accepts tag is not mistaken for a rejected keyword, so it propagates and
    the hook is not rerun without tag.
    """

    calls = []

    def hook(layer="master", tag=None):
        calls.append(tag)
        raise TypeError("something else")

    mocker.patch.object(renpy.config, "scene", hook)

    with pytest.raises(TypeError, match="something else"):
        execute_scene()

    assert calls == ["bg"]


################################################################################
# TranslateSay scry
################################################################################


class NVLClear(renpy.ast.Node):
    """
    A non-interacting node whose scry reports an upcoming ``nvl clear``, like the nvl clear statement does.
    """

    def scry(self):
        rv = super().scry()
        rv.nvl_clear = True
        return rv


def make_translate_say(identifier: str, what: str, language: str | None = None) -> renpy.ast.TranslateSay:
    """
    Creates a narrator TranslateSay, which needs no character to be defined in the store.
    """

    return renpy.ast.TranslateSay(("test.rpy", 1), None, what, None, identifier=identifier, language=language)


@pytest.fixture
def translated_script(mocker):
    """
    Builds two default-language lines followed by an nvl clear, with a translation of each line into "test", and
    selects that language. The translated lines are chained to the line after their default line, as
    ScriptTranslator.chain_translates does, and returned as a dict along with the other nodes.
    """

    first = make_translate_say("first", "One.")
    second = make_translate_say("second", "Two.")
    clear = NVLClear(("test.rpy", 3))

    first.chain(second)
    second.chain(clear)

    first_tl = make_translate_say("first", "Un.", "test")
    second_tl = make_translate_say("second", "Deux.", "test")

    first_tl.chain(second)
    second_tl.chain(clear)

    translator = renpy.translation.ScriptTranslator()
    translator.default_translates.update(first=first, second=second)
    translator.language_translates.update({("first", "test"): first_tl, ("second", "test"): second_tl})

    mocker.patch.object(renpy.game, "script", SimpleNamespace(translator=translator))
    preferences = SimpleNamespace(language="test")
    mocker.patch.object(renpy.game, "preferences", preferences)

    return {"first": first, "first_tl": first_tl, "second": second, "clear": clear, "preferences": preferences}


def test_translated_say_scries_the_next_translated_say(translated_script):
    """
    The scry after a translated line describes the next translated line, which interacts, so ``nvl clear`` two
    lines later is not reported as coming before the next interaction (#7537). Previously, the default-language
    line's scry skipped over its translation, so every translated line seemed to end an NVL page.
    """

    scry = translated_script["first_tl"].scry().next()

    assert scry.say
    assert scry.interacts
    assert not scry.nvl_clear

    scry = scry.next()

    assert scry.nvl_clear


def test_default_line_scries_its_translation(translated_script):
    """
    Scrying a default-language line that has a translation describes the translation, which runs in its place.
    """

    scry = translated_script["first"].scry()

    assert scry.say
    assert scry.interacts


def test_translation_scries_itself_after_language_change(translated_script):
    """
    A translated line that is scried after the language changes back to the default describes itself, not the
    default line, just as executing it says its own text. The translated line is made non-interacting so that its
    scry can be told apart from the default line's.
    """

    translated_script["first_tl"].interact = False
    translated_script["preferences"].language = None

    scry = translated_script["first_tl"].scry()

    assert scry.say
    assert not scry.interacts
