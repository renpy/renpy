from types import SimpleNamespace

import pytest
from pytest_mock import MockerFixture

import renpy
from renpy.color import Color
from renpy.display.core import IgnoreEvent
from renpy.text import text


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (42, "Can't display 42 as Text."),
        (None, "Can't display None as Text."),
        ("unfinished {", "Open text tag"),
        ("empty {}", "Empty text tag"),
    ],
)
def test_tokenize_raises_without_safe_mode(mocker: MockerFixture, value: str | int | None, message: str) -> None:
    """Invalid values and malformed tags must raise instead of silently disappearing in normal mode."""

    mocker.patch.object(renpy.config, "safe_text", False)
    displayable = SimpleNamespace(safe=False)

    with pytest.raises(Exception, match=message):
        text.Text.tokenize(displayable, [value])


@pytest.mark.parametrize(("config_safe", "displayable_safe"), [(True, False), (False, True), (True, True)])
@pytest.mark.parametrize(
    ("value", "expected"),
    [(42, "42"), (None, "None"), ("unfinished {", "unfinished {"), ("empty {}", "empty {}")],
)
def test_tokenize_safe_mode_uses_literal_strings(
    mocker: MockerFixture,
    config_safe: bool,
    displayable_safe: bool,
    value: str | int | None,
    expected: str,
) -> None:
    """Either safe-mode setting preserves failed inputs as strings and continues with subsequent text."""

    mocker.patch.object(renpy.config, "safe_text", config_safe)
    displayable = SimpleNamespace(safe=displayable_safe)

    tokens = text.Text.tokenize(displayable, ["before", value, "after"])

    assert tokens == [(text.TEXT, "before"), (text.TEXT, expected), (text.TEXT, "after")]


@pytest.fixture
def slow_text():
    """A stand-in for a Text displayable that is still showing slow text and allows it to be aborted."""

    return SimpleNamespace(
        slow=True,
        slow_done=None,
        style=SimpleNamespace(slow_abortable=True),
        get_layout=lambda: None,
    )


@pytest.fixture
def event():
    """An opaque event; map_event is patched, so its contents do not matter."""

    return SimpleNamespace()


def test_slow_abort_does_not_consume_event_while_grabbed(mocker, slow_text, event):
    """
    A dismiss event does not abort slow text while another displayable holds the focus grab.

    The event has to be left for the grabbing displayable (for example, a drag in progress), so
    Text.event returns None instead of raising IgnoreEvent, and the text keeps displaying slowly.
    """

    mocker.patch.object(renpy.display.behavior, "map_event", return_value=True)
    mocker.patch.object(renpy.display.focus, "get_grab", return_value=object())

    result = text.Text.event(slow_text, event, 0, 0, 0)

    assert result is None
    assert slow_text.slow


def test_slow_abort_consumes_dismiss_event_without_grab(mocker, slow_text, event):
    """
    Without a focus grab, a dismiss event finishes every abortable slow text and is consumed.

    The displayable is registered in the module-level slow_text list, which is what Text.event walks
    to finish all slow text at once. IgnoreEvent means the click doesn't also advance the dialogue.
    """

    mocker.patch.object(renpy.display.behavior, "map_event", return_value=True)
    mocker.patch.object(renpy.display.focus, "get_grab", return_value=None)
    mocker.patch.object(text, "slow_text", [slow_text])

    with pytest.raises(IgnoreEvent):
        text.Text.event(slow_text, event, 0, 0, 0)

    assert not slow_text.slow


@pytest.mark.parametrize(
    ("override_color", "outline_color", "alpha", "expected"),
    [
        ((255, 255, 255, 255), None, 0.5, (255, 255, 255, 127)),
        ((255, 255, 224, 255), None, 0.5, (255, 255, 224, 127)),
        ((224, 255, 255, 255), None, 0.5, (224, 255, 255, 127)),
        ((255, 255, 255, 255), None, 0.0, (255, 255, 255, 0)),
        ((255, 255, 255, 255), None, 1.0, (255, 255, 255, 255)),
        (Color("#1238"), None, 0.5, (17, 34, 51, 67)),
        ((255, 255, 255, 255), Color("#f008"), 0.5, (255, 0, 0, 67)),
    ],
    ids=["high-contrast", "hover", "selected", "transparent", "opaque", "outline", "outline-tag"],
)
def test_draw_override_color_preserves_text_alpha(
    mocker: MockerFixture,
    override_color: tuple[int, int, int, int],
    outline_color: Color | None,
    alpha: float,
    expected: tuple[int, int, int, int],
) -> None:
    """
    High-contrast tuple colors and outline Colors retain their RGB values and multiply their opacity by
    the text alpha. Mock only font drawing so the color selection runs without a graphics device.
    """

    segment = text.TextSegment()
    segment.font = "DejaVuSans.ttf"
    segment.size = 24
    segment.bold = False
    segment.italic = False
    segment.hinting = "auto"
    segment.shaper = "harfbuzz"
    segment.underline = 0
    segment.strikethrough = 0
    segment.color = Color("#fff").replace_opacity(alpha)
    segment.outline_color = outline_color

    draw_info = text.DrawInfo()
    draw_info.override_color = override_color
    font = mocker.patch.object(text.font, "get_font").return_value

    segment.draw([], draw_info, 2, 3, SimpleNamespace(oversample=1))

    font.draw.assert_called_once_with(None, 2, 3, expected, [], 0, 0, None)
