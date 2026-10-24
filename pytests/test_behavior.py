import unittest
from types import SimpleNamespace
from unittest.mock import patch

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

import renpy
from renpy import pygame
from renpy.display import behavior


class TestSayBehavior(unittest.TestCase):
    def test_disabled_rollback_side_overrides_desktop_preference(self) -> None:
        event = SimpleNamespace(type=pygame.MOUSEBUTTONUP)

        with (
            patch.object(renpy.config, "enable_rollback_side", False),
            patch.object(renpy.exports, "variant", return_value=False),
            patch.object(renpy.game.preferences, "desktop_rollback_side", "left"),
            patch.object(renpy.game.preferences, "using_afm_enable", False),
            patch.object(behavior, "map_event", return_value=True),
            patch.object(behavior.SayBehavior, "is_focused", return_value=True),
            patch.object(renpy.display.focus, "get_grab", return_value=None),
            patch.object(renpy.exports, "rollback") as rollback,
        ):
            result = behavior.SayBehavior().event(event, 0, 0, 0)

        self.assertTrue(result)
        rollback.assert_not_called()
