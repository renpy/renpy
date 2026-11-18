from types import SimpleNamespace

import pytest

import renpy
from renpy import pygame
from renpy.display import behavior
from renpy.display.displayable import Displayable
from renpy.display.render import Render


def make_style(**properties: object) -> SimpleNamespace:
    """
    Returns a stand-in for the style properties used when rendering a displayable, as styles are not built
    in unit tests.
    """

    return SimpleNamespace(xmaximum=None, ymaximum=None, debug=False, **properties)


class FailingMask(Displayable):
    """
    A focus mask whose render fails like an image with a missing file, recording the value of
    renpy.display.im.thread_local.raise_image_load_exceptions seen while rendering.
    """

    def __init__(self) -> None:
        super().__init__()
        self.style = make_style()
        self.raise_image_load_exceptions: list[object] = []
        self.config_raise_image_load_exceptions: list[object] = []

    def render(self, width: int, height: int, st: float, at: float) -> Render:
        self.raise_image_load_exceptions.append(renpy.display.im.thread_local.raise_image_load_exceptions)
        self.config_raise_image_load_exceptions.append(renpy.config.raise_image_load_exceptions)
        raise FileNotFoundError("Couldn't find file 'missing_mask.png'.")


class CallableMask(Displayable):
    """
    A focus mask that is both a displayable and callable, like a Transform.
    """

    def __init__(self) -> None:
        super().__init__()
        self.style = make_style()

    def render(self, width: int, height: int, st: float, at: float) -> Render:
        return Render(width, height)

    def __call__(self, *args: object) -> bool:
        raise AssertionError("A displayable focus mask must be rendered, not called.")


@pytest.fixture(autouse=True)
def clear_logged_focus_mask_errors() -> None:
    """Clear the focus-mask error cache, which is keyed by repr(mask), so each test logs its own failures."""
    behavior.focus_mask_errors_logged.clear()


def render_mask(mocker, mask: object, raise_image_load_exceptions: bool) -> object:
    """
    Renders the focus mask with the thread-local image-load flag set to ``raise_image_load_exceptions``, and
    asserts afterwards that rendering left that flag unchanged, even when it raised.
    """

    thread_local = renpy.display.im.thread_local
    mocker.patch.object(thread_local, "raise_image_load_exceptions", raise_image_load_exceptions)

    try:
        return behavior.render_focus_mask(mask, 40, 20, 0, 0)
    finally:
        assert thread_local.raise_image_load_exceptions is raise_image_load_exceptions


def test_broken_mask_raises_original_exception_when_load_exceptions_enabled(mocker) -> None:
    """A mask whose render fails re-raises the original exception, annotated with focus-mask context, when load exceptions are enabled."""
    mask = FailingMask()

    with pytest.raises(FileNotFoundError) as excinfo:
        render_mask(mocker, mask, True)

    assert "While rendering the focus_mask" in "\n".join(excinfo.value.__notes__)


def test_broken_mask_is_ignored_and_logged_once_when_load_exceptions_disabled(mocker) -> None:
    """A failing mask renders to None and is logged only once across repeated renders when load exceptions are disabled."""
    mask = FailingMask()

    log = mocker.patch.object(renpy.display, "log")
    assert render_mask(mocker, mask, False) is None
    assert render_mask(mocker, mask, False) is None

    assert mask.raise_image_load_exceptions == [True, True]
    assert mask.config_raise_image_load_exceptions == [renpy.config.raise_image_load_exceptions] * 2
    log.write.assert_called_once()
    log.exception.assert_called_once()


def test_control_exceptions_are_not_ignored(mocker) -> None:
    """Engine control-flow exceptions raised by a mask propagate even when load exceptions are disabled."""
    mask = FailingMask()
    mask.render = mocker.Mock(side_effect=renpy.game.JumpException("start"))

    with pytest.raises(renpy.game.JumpException):
        render_mask(mocker, mask, False)


def test_mask_kinds(mocker) -> None:
    """None, True, a callable, a callable displayable, and a non-mask value are each handled as their kind requires."""
    true_mask = Render(40, 20)
    function = mocker.Mock()

    assert behavior.render_focus_mask(None, 40, 20, 0, 0, true_mask) is None
    assert behavior.render_focus_mask(True, 40, 20, 0, 0, true_mask) is true_mask
    assert behavior.render_focus_mask(function, 40, 20, 0, 0) is function
    assert isinstance(behavior.render_focus_mask(CallableMask(), 40, 20, 0, 0), Render)

    with pytest.raises(TypeError):
        behavior.render_focus_mask(42, 40, 20, 0, 0)


def hover(mocker, focus_mask: object, x: int, y: int) -> bool:
    """
    Sends a mouse event at (x, y) to a 40x20 MouseArea with ``focus_mask`` and returns whether it became hovered.
    Grabs, focus type, and logging are stubbed so only the focus-mask decision is exercised.
    """

    mousearea = behavior.MouseArea()
    mousearea.style = make_style(focus_mask=focus_mask)
    mousearea.width = 40
    mousearea.height = 20

    mocker.patch.object(renpy.display.focus, "get_grab", return_value=None)
    mocker.patch.object(renpy.display.focus, "pending_focus_type", "mouse")
    mocker.patch.object(renpy.display.im.thread_local, "raise_image_load_exceptions", False)
    mocker.patch.object(renpy.display, "log")
    mousearea.event(mocker.Mock(type=0), x, y, 0)

    return mousearea.is_hovered


def test_mouse_area_callable_mask(mocker) -> None:
    """A MouseArea with a callable focus mask is hovered only at points the mask accepts."""
    mask = mocker.Mock(side_effect=lambda x, y: x < 10)

    assert hover(mocker, mask, 5, 5)
    assert not hover(mocker, mask, 15, 5)
    assert not hover(mocker, mask, -5, 5)


def test_mouse_area_broken_mask_falls_back_to_area(mocker) -> None:
    """A MouseArea whose focus mask fails to render falls back to its rectangular area for hover."""
    assert hover(mocker, FailingMask(), 5, 5)
    assert not hover(mocker, FailingMask(), 50, 5)


def test_disabled_rollback_side_overrides_desktop_preference(mocker):
    """
    When config.enable_rollback_side is False, clicking the rollback side doesn't roll back, even if the
    player's desktop preference says to.

    The click happens at x=0, which is inside the left rollback area that the "left" preference would
    act on. Instead, SayBehavior treats it as an ordinary dismiss click and returns True. The variant
    is patched so the desktop preference, not the mobile one, would apply, and auto-forward is off so it
    can't consume the click first.
    """

    event = SimpleNamespace(type=pygame.MOUSEBUTTONUP)

    mocker.patch.object(renpy.config, "enable_rollback_side", False)
    mocker.patch.object(renpy.exports, "variant", return_value=False)
    mocker.patch.object(renpy.game.preferences, "desktop_rollback_side", "left")
    mocker.patch.object(renpy.game.preferences, "using_afm_enable", False)
    mocker.patch.object(behavior, "map_event", return_value=True)
    mocker.patch.object(behavior.SayBehavior, "is_focused", return_value=True)
    mocker.patch.object(renpy.display.focus, "get_grab", return_value=None)
    rollback = mocker.patch.object(renpy.exports, "rollback")

    result = behavior.SayBehavior().event(event, 0, 0, 0)

    assert result
    rollback.assert_not_called()
