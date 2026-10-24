from types import SimpleNamespace

import renpy
from renpy import pygame
from renpy.display import behavior


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
