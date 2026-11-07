import pytest

import renpy
from renpy.ast import Scene


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
    A hook that accepts tag is called once. A TypeError it raises is not mistaken for a rejected keyword, so it is
    raised and the hook is not rerun without tag.
    """

    calls = []

    def hook(layer="master", tag=None):
        calls.append(tag)
        raise TypeError("something else")

    mocker.patch.object(renpy.config, "scene", hook)

    with pytest.raises(TypeError, match="something else"):
        execute_scene()

    assert calls == ["bg"]
