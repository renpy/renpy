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


@pytest.fixture
def declare_screen(mocker):
    """
    Returns a function that declares a real screen, as a script's screen statement would, so the layer
    lookups under test go through the screen registry. The registries are patched so the test screens don't
    leak into other tests.
    """

    mocker.patch.dict(screen.screens)
    mocker.patch.dict(screen.screens_by_name)

    def declare(name, **definition):
        screen.Screen(name, lambda **kwargs: None, **definition)

    return declare


@pytest.mark.parametrize(
    ("definition", "declared"),
    [({"layer": "dialogue"}, "dialogue"), ({}, "screens")],
    ids=["declared-layer", "default-layer"],
)
@pytest.mark.parametrize(
    ("configured", "explicit", "precedence"),
    [
        (None, None, "declared"),
        ("configured", None, "configured"),
        (None, "explicit", "explicit"),
        ("configured", "explicit", "explicit"),
    ],
)
def test_say_layer_precedence_and_keyword_omission(
    mocker, declare_screen, definition, declared, configured, explicit, precedence
):
    """
    The layer for a say statement is the explicit layer argument if given, otherwise config.say_layer if
    set, otherwise the layer the say screen declares. A screen declared without layer= is on the "screens"
    layer, and one declared with layer= is on that layer. When neither config.say_layer nor the layer
    argument is set, the _layer keyword is left out of show_screen so the screen's own default applies.
    """

    expected = {"declared": declared, "configured": configured, "explicit": explicit}[precedence]
    declare_screen("say", **definition)
    mocker.patch.object(renpy.config, "say_layer", configured)
    show = mocker.patch.object(screen, "show_screen")

    result = character.show_display_say("Speaker", "Text", screen="say", layer=explicit)
    assert result == ("say", "what", expected)
    if configured is None and explicit is None:
        assert "_layer" not in show.call_args.kwargs
    else:
        assert show.call_args.kwargs["_layer"] == expected


@pytest.mark.parametrize(
    ("options", "name", "tag", "layer"),
    [
        ({"retain": "retained"}, "say", "retained", "say_layer"),
        ({"multiple": (1, 2)}, "multiple_say", "block1_multiple2_say", "multiple_say_layer"),
    ],
    ids=["retain", "multiple"],
)
def test_retained_and_multiple_dialogue_resolve_screen_not_tag(mocker, declare_screen, options, name, tag, layer):
    """
    A retained say, or one with multiple=, uses its transient tag (the retain name or the block/multiple
    tag) for the displayed widget, but its layer is looked up by the screen name (`say` or
    `multiple_say`). The two screens are declared on different layers, so the layer in the result shows which
    screen was consulted. The screen is shown with that name and no _layer keyword, since no layer is
    configured.
    """

    declare_screen("say", layer="say_layer")
    declare_screen("multiple_say", layer="multiple_say_layer")
    mocker.patch.object(renpy.config, "say_layer", None)
    mocker.patch.object(character, "compute_widget_properties", return_value={})
    show = mocker.patch.object(screen, "show_screen")

    result = character.show_display_say("Speaker", "Text", screen="say", **options)
    assert result == (tag, "what", layer)
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
