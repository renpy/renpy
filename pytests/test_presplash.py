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
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
from unittest.mock import Mock, call, patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display import core, presplash


class TestPresplashEnd(unittest.TestCase):
    def test_web_overlay_remains_during_display_initialization(self) -> None:
        browser = Mock()

        with (
            patch.object(renpy, "emscripten", True),
            patch.object(presplash, "emscripten", browser, create=True),
            patch.object(presplash, "window", None),
            patch.object(presplash, "done", False),
        ):
            presplash.end()

            self.assertTrue(presplash.done)
            browser.run_script.assert_not_called()

    def test_desktop_window_and_images_are_released(self) -> None:
        window = Mock()

        with (
            patch.object(renpy, "emscripten", False),
            patch.object(presplash, "window", window),
            patch.object(presplash, "progress_bar", Mock()),
            patch.object(presplash, "done", False),
            patch.object(presplash.pygame.display, "quit") as quit_display,
        ):
            presplash.end()

            window.destroy.assert_called_once_with()
            quit_display.assert_called_once_with()
            self.assertIsNone(presplash.window)
            self.assertIsNone(presplash.progress_bar)
            self.assertTrue(presplash.done)


class TestFirstFramePresplash(unittest.TestCase):
    def setUp(self) -> None:
        self.interface: core.Interface = object.__new__(core.Interface)
        self.interface.first_frame = True
        self.interface.frame_times = []
        self.browser: Mock = Mock()
        self.renderer: Mock = Mock()
        self.events: Mock = Mock()
        self.events.attach_mock(self.renderer.draw_screen, "draw")
        self.events.attach_mock(self.browser.run_script, "script")

        self.enterContext(patch.object(renpy, "emscripten", True))
        self.enterContext(patch.object(renpy, "android", False))
        self.enterContext(patch.object(core, "emscripten", self.browser))
        self.enterContext(patch.object(renpy.display, "draw", self.renderer))
        self.enterContext(patch.object(renpy.display.screen, "per_frame"))
        self.enterContext(patch.object(renpy.display.render, "per_frame", False))
        self.enterContext(patch.object(renpy.display.render, "render_screen", return_value="frame"))
        self.enterContext(patch.object(renpy.display.render, "mark_sweep"))
        self.enterContext(patch.object(renpy.display.focus, "take_focuses"))

    def test_web_overlay_is_removed_after_drawing_and_only_once(self) -> None:
        self.interface.draw_screen(None, False, True)
        self.interface.draw_screen(None, False, True)

        self.assertEqual(
            self.events.mock_calls,
            [call.draw("frame"), call.script("presplashEnd();"), call.draw("frame")],
        )
        self.assertFalse(self.interface.first_frame)

    def test_failed_render_does_not_remove_overlay(self) -> None:
        self.renderer.draw_screen.side_effect = RuntimeError("Rendering failed")

        with self.assertRaisesRegex(RuntimeError, "Rendering failed"):
            self.interface.draw_screen(None, False, True)

        self.browser.run_script.assert_not_called()
        self.assertTrue(self.interface.first_frame)

    def test_desktop_first_frame_does_not_call_browser(self) -> None:
        with patch.object(renpy, "emscripten", False):
            self.interface.draw_screen(None, False, True)

        self.browser.run_script.assert_not_called()

    def test_android_presplash_is_still_removed_after_first_frame(self) -> None:
        jnius = Mock()

        with (
            patch.object(renpy, "emscripten", False),
            patch.object(renpy, "android", True),
            patch.dict("sys.modules", {"jnius": jnius}),
            patch("builtins.print"),
        ):
            self.interface.draw_screen(None, False, True)
            self.interface.draw_screen(None, False, True)

        jnius.autoclass.assert_called_once_with("org.renpy.android.PythonSDLActivity")
        jnius.autoclass.return_value.mActivity.hidePresplash.assert_called_once_with()
        self.browser.run_script.assert_not_called()


if __name__ == "__main__":
    unittest.main()
