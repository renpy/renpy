import unittest
from types import SimpleNamespace
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.gl2.gl2draw import GL2Draw
from renpy.test import testexecution


class TestTestWindowSize(unittest.TestCase):
    def test_normal_execution_has_no_size_override(self):
        with patch.object(testexecution, "initialized", False):
            self.assertIsNone(testexecution.get_test_window_size())

    def test_mobile_execution_has_no_size_override(self):
        with (
            patch.object(testexecution, "initialized", True),
            patch.object(renpy, "mobile", True),
        ):
            self.assertIsNone(testexecution.get_test_window_size())

    def test_test_execution_uses_virtual_resolution(self):
        with (
            patch.object(testexecution, "initialized", True),
            patch.object(renpy, "mobile", False),
            patch.object(renpy.config, "screen_width", 800),
            patch.object(renpy.config, "screen_height", 600),
        ):
            self.assertEqual(testexecution.get_test_window_size(), (800, 600))

    def test_resize_ignores_saved_size_dpi_and_fullscreen(self):
        draw = GL2Draw.__new__(GL2Draw)
        draw.virtual_size = (800, 600)
        draw.dpi_scale = 2.0
        draw.info = {"max_window_size": (640, 480)}

        with (
            patch.object(testexecution, "get_test_window_size", return_value=(800, 600)),
            patch.object(renpy.game, "preferences") as preferences,
            patch.object(renpy.display, "interface"),
            patch.object(renpy.display.log, "write"),
            patch.object(renpy.pygame.display, "get_window") as get_window,
        ):
            preferences.fullscreen = True
            preferences.maximized = True
            preferences.physical_size = (1920, 1080)
            draw.resize()
            self.assertEqual(draw.dpi_scale, 1.0)

        get_window.return_value.resize.assert_called_once_with(
            (800, 600), opengl=True, fullscreen=False, maximized=False
        )

    def test_initial_size_ignores_display_limits_and_dpi(self):
        draw = GL2Draw.__new__(GL2Draw)
        draw.virtual_size = (800, 600)
        draw.dpi_scale = 2.0
        draw.info = {}

        with (
            patch.object(testexecution, "get_test_window_size", return_value=(800, 600)),
            patch.object(renpy.game, "preferences") as preferences,
            patch.object(renpy.game, "interface"),
            patch.object(renpy.display, "interface"),
            patch.object(renpy.display.log, "write"),
            patch.object(renpy.display, "get_info", return_value=SimpleNamespace(current_w=640, current_h=480)),
            patch.object(renpy.pygame.display, "get_surface", return_value=None),
            patch.object(renpy.pygame.display, "get_display_bounds", return_value=[(0, 0, 640, 480)]),
        ):
            preferences.maximized = False
            self.assertEqual(draw.select_physical_size((1920, 1080)), (800, 600))

        self.assertEqual(draw.dpi_scale, 1.0)
        self.assertEqual(draw.info["max_window_size"], (800, 600))

    def test_normal_resize_keeps_existing_policy(self):
        draw = GL2Draw.__new__(GL2Draw)
        draw.virtual_size = (800, 600)
        draw.dpi_scale = 1.0
        draw.info = {"max_window_size": (1920, 1080)}

        with (
            patch.object(testexecution, "get_test_window_size", return_value=None),
            patch.object(renpy.game, "preferences") as preferences,
            patch.object(renpy.display, "interface"),
            patch.object(renpy.display.log, "write"),
            patch.object(renpy.pygame.display, "get_window") as get_window,
        ):
            preferences.fullscreen = True
            preferences.maximized = True
            preferences.physical_size = (1024, 768)
            draw.resize()

        get_window.return_value.resize.assert_called_once_with(
            (1024, 768), opengl=True, fullscreen=True, maximized=False
        )
