import ast
import os
from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace

import pytest

import renpy
from renpy import character
from renpy.display import screen
from renpy.exports import menuexports


@pytest.fixture(autouse=True)
def say_environment(mocker):
    """
    Stubs the engine state that show_display_say and display_menu consult (the shown window, screen,
    rollback and log state, the current context, and the say and auto-choice settings), so only the layer
    selection runs. The patches last until the test ends.
    """

    mocker.patch.object(renpy.exports, "shown_window")
    mocker.patch.object(screen, "has_screen", return_value=True)
    mocker.patch.object(renpy.exports, "has_screen", return_value=True)
    mocker.patch.object(renpy.exports, "roll_forward_info", return_value=None)
    mocker.patch.object(renpy.exports, "in_fixed_rollback", return_value=False)
    mocker.patch.object(renpy.exports, "in_rollback", return_value=False)
    mocker.patch.object(renpy.exports, "log")
    mocker.patch.object(renpy.game, "context", return_value=SimpleNamespace(current="test"))
    mocker.patch.object(renpy.config, "auto_choice_delay", None)
    mocker.patch.object(renpy.config, "old_say_args", False)


@pytest.mark.parametrize(
    ("declared", "configured", "explicit", "expected"),
    [
        ("dialogue", None, None, "dialogue"),
        ("dialogue", "configured", None, "configured"),
        ("dialogue", None, "explicit", "explicit"),
        ("dialogue", "configured", "explicit", "explicit"),
        ("screens", None, None, "screens"),
        ("screens", "configured", None, "configured"),
        ("screens", None, "explicit", "explicit"),
        ("screens", "configured", "explicit", "explicit"),
    ],
)
def test_say_layer_precedence_and_keyword_omission(mocker, declared, configured, explicit, expected):
    """
    The layer for a say statement is the explicit layer argument if given, otherwise config.say_layer if
    set, otherwise the layer the say screen declares. The declared layer is what get_screen_layer returns
    here. When neither config.say_layer nor the layer argument is set, the _layer keyword is left out of
    show_screen so the screen's own default applies.
    """

    mocker.patch.object(renpy.config, "say_layer", configured)
    mocker.patch.object(screen, "get_screen_layer", return_value=declared)
    show = mocker.patch.object(screen, "show_screen")

    result = character.show_display_say("Speaker", "Text", screen="say", layer=explicit)
    assert result == ("say", "what", expected)
    if configured is None and explicit is None:
        assert "_layer" not in show.call_args.kwargs
    else:
        assert show.call_args.kwargs["_layer"] == expected


@pytest.mark.parametrize(
    ("options", "name", "tag"),
    [
        ({"retain": "retained"}, "say", "retained"),
        ({"multiple": (1, 2)}, "multiple_say", "block1_multiple2_say"),
    ],
    ids=["retain", "multiple"],
)
def test_retained_and_multiple_dialogue_resolve_screen_not_tag(mocker, options, name, tag):
    """
    A retained say, or one with multiple=, uses its transient tag (the retain name or the block/multiple
    tag) for the displayed widget, but its layer is looked up by the screen name (`say` or
    `multiple_say`). The screen is shown with that name and no _layer keyword, since no layer is configured.
    """

    mocker.patch.object(renpy.config, "say_layer", None)
    mocker.patch.object(character, "compute_widget_properties", return_value={})
    get_layer = mocker.patch.object(screen, "get_screen_layer", return_value="dialogue")
    show = mocker.patch.object(screen, "show_screen")

    result = character.show_display_say("Speaker", "Text", screen="say", **options)
    assert result == (tag, "what", "dialogue")
    get_layer.assert_called_once_with(name)
    assert show.call_args.args == (name,)
    assert "_layer" not in show.call_args.kwargs


@pytest.mark.parametrize(("menu_type", "setting"), [("menu", "choice_layer"), ("nvl", "nvl_choice_layer")])
@pytest.mark.parametrize(
    ("configured", "explicit", "expected"),
    [
        (None, None, None),
        ("configured", None, "configured"),
        (None, "explicit", "explicit"),
        ("configured", "explicit", "explicit"),
    ],
)
def test_menu_layer_precedence_and_keyword_omission(mocker, menu_type, setting, configured, explicit, expected):
    """
    For ordinary menus the layer is the explicit _layer argument if given, otherwise the matching setting
    (config.choice_layer for "menu", config.nvl_choice_layer for "nvl"). When neither is set, _layer is left
    out of show_screen. The parametrization covers both menu types against each precedence case.
    """

    mocker.patch.object(renpy.config, setting, configured)
    show = mocker.patch.object(renpy.exports, "show_screen")

    menuexports.display_menu([], interact=False, type=menu_type, _layer=explicit, _args=(), _kwargs={})
    if expected is None:
        assert "_layer" not in show.call_args.kwargs
    else:
        assert show.call_args.kwargs["_layer"] == expected


def test_menu_argument_layer_override(mocker):
    """
    A _layer in the menu's keyword arguments (_kwargs) takes precedence over both the _layer parameter and
    config.choice_layer, because display_menu pops it from the menu's keyword arguments first.
    """

    mocker.patch.object(renpy.config, "choice_layer", "configured")
    show = mocker.patch.object(renpy.exports, "show_screen")

    menuexports.display_menu([], interact=False, _layer="explicit", _args=(), _kwargs={"_layer": "argument"})
    assert show.call_args.kwargs["_layer"] == "argument"


@pytest.mark.parametrize(
    ("definition", "expected"),
    [({}, "screens"), ({"layer": "dialogue"}, "dialogue")],
    ids=["default", "declared"],
)
def test_screen_declared_layer_and_default(mocker, definition, expected):
    """
    A screen declared without layer= is placed on the "screens" layer, and one declared with layer= is
    placed on that layer. The screen registries are patched so the test screen doesn't leak into other
    tests.
    """

    mocker.patch.dict(screen.screens)
    mocker.patch.dict(screen.screens_by_name)
    screen.Screen("_test_screen_layer", lambda **kwargs: None, **definition)
    assert screen.get_screen_layer("_test_screen_layer") == expected


def test_configuration_defaults_are_unset():
    """
    The say, choice, and NVL choice layer settings default to None, so the layer comes from the screen
    declaration unless a script version sets them (see the compatibility test).
    """

    for setting in ("say_layer", "choice_layer", "nvl_choice_layer"):
        assert getattr(renpy.config, setting) is None, setting


def load_compat_namespace():
    """
    Returns a namespace holding the _set_script_version function from the "init -1100 python" block of
    renpy/common/00compat.rpy. The function is extracted from the script source and executed on its own,
    because it lives in a Renpy script rather than in an importable module.
    """

    path = Path(renpy.config.renpy_base) / "renpy/common/00compat.rpy"
    source = path.read_text(encoding="utf-8-sig").split("init -1100 python:", 1)[1]
    source = source.split("\npython early ", 1)[0]
    module = ast.parse(dedent(source))
    functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    namespace = {}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), "exec"), namespace)  # noqa: S102
    return namespace


@pytest.mark.parametrize(
    ("version", "expected"),
    [((8, 5, 0), "screens"), ((8, 5, 99), "screens"), ((8, 6, 0), None), (None, None)],
    ids=["8.5.0", "8.5.99", "8.6.0", "no-version"],
)
def test_script_version_sets_layers_for_compatibility(mocker, version, expected):
    """
    Scripts declaring a version up to 8.5.99 get all three layer settings set to "screens", preserving
    their old behavior. A version of 8.6.0 or later, or no version at all, leaves them unset. The
    RENPY_EXPERIMENTAL environment variable disables the version override, so it is removed for the test
    and restored at teardown.
    """

    settings = ("say_layer", "choice_layer", "nvl_choice_layer")
    mocker.patch.dict(os.environ)
    os.environ.pop("RENPY_EXPERIMENTAL", None)

    config = SimpleNamespace(**dict.fromkeys(settings))
    namespace = load_compat_namespace()
    namespace["config"] = config
    namespace["_set_script_version"](version)
    for setting in settings:
        assert getattr(config, setting) == expected, setting
