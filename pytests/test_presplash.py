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

from types import SimpleNamespace

import pytest

import renpy
from renpy.display import core, presplash


def test_web_overlay_remains_during_display_initialization(mocker) -> None:
    """On the web, ending presplash marks it done without asking the browser to remove the overlay."""
    browser = mocker.Mock()

    mocker.patch.object(renpy, "emscripten", True)
    mocker.patch.object(presplash, "emscripten", browser, create=True)
    mocker.patch.object(presplash, "window", None)
    mocker.patch.object(presplash, "done", False)

    presplash.end()

    assert presplash.done
    browser.run_script.assert_not_called()


def test_desktop_window_and_images_are_released(mocker) -> None:
    """On desktop, ending presplash destroys the window, quits pygame's display, and clears the window and progress bar."""
    window = mocker.Mock()

    mocker.patch.object(renpy, "emscripten", False)
    mocker.patch.object(presplash, "window", window)
    mocker.patch.object(presplash, "progress_bar", mocker.Mock())
    mocker.patch.object(presplash, "done", False)
    quit_display = mocker.patch.object(presplash.pygame.display, "quit")

    presplash.end()

    window.destroy.assert_called_once_with()
    quit_display.assert_called_once_with()
    assert presplash.window is None
    assert presplash.progress_bar is None
    assert presplash.done


class TestFirstFramePresplash:
    """Tests for the web overlay removal that the interface performs after its first drawn frame."""

    @pytest.fixture
    def frame(self, mocker) -> SimpleNamespace:
        """
        Provide an Interface on its first frame with rendering, browser, and focus stubbed out. ``events``
        records draws and browser scripts in order, so tests can assert their relative ordering.
        """
        interface = object.__new__(core.Interface)
        interface.first_frame = True
        interface.frame_times = []
        browser = mocker.Mock()
        renderer = mocker.Mock()
        events = mocker.Mock()
        events.attach_mock(renderer.draw_screen, "draw")
        events.attach_mock(browser.run_script, "script")

        mocker.patch.object(renpy, "emscripten", True)
        mocker.patch.object(renpy, "android", False)
        mocker.patch.object(core, "emscripten", browser)
        mocker.patch.object(renpy.display, "draw", renderer)
        mocker.patch.object(renpy.display.screen, "per_frame")
        mocker.patch.object(renpy.display.render, "per_frame", False)
        mocker.patch.object(renpy.display.render, "render_screen", return_value="frame")
        mocker.patch.object(renpy.display.render, "mark_sweep")
        mocker.patch.object(renpy.display.focus, "take_focuses")

        return SimpleNamespace(interface=interface, browser=browser, renderer=renderer, events=events)

    def test_web_overlay_is_removed_after_drawing_and_only_once(self, frame, mocker) -> None:
        """The web overlay is removed right after the first frame is drawn, and not again on later frames."""
        frame.interface.draw_screen(None, False, True)
        frame.interface.draw_screen(None, False, True)

        assert frame.events.mock_calls == [
            mocker.call.draw("frame"),
            mocker.call.script("presplashEnd();"),
            mocker.call.draw("frame"),
        ]
        assert not frame.interface.first_frame

    def test_failed_render_does_not_remove_overlay(self, frame) -> None:
        """If the first frame fails to render, the overlay stays and the interface remains on its first frame."""
        frame.renderer.draw_screen.side_effect = RuntimeError("Rendering failed")

        with pytest.raises(RuntimeError, match="Rendering failed"):
            frame.interface.draw_screen(None, False, True)

        frame.browser.run_script.assert_not_called()
        assert frame.interface.first_frame

    def test_desktop_first_frame_does_not_call_browser(self, frame, mocker) -> None:
        """Off the web, drawing the first frame never calls the browser."""
        mocker.patch.object(renpy, "emscripten", False)
        frame.interface.draw_screen(None, False, True)

        frame.browser.run_script.assert_not_called()

    def test_android_presplash_is_still_removed_after_first_frame(self, frame, mocker) -> None:
        """On Android, the presplash is hidden through the activity once, and the browser is never called."""
        jnius = mocker.Mock()

        mocker.patch.object(renpy, "emscripten", False)
        mocker.patch.object(renpy, "android", True)
        mocker.patch.dict("sys.modules", {"jnius": jnius})
        mocker.patch("builtins.print")

        frame.interface.draw_screen(None, False, True)
        frame.interface.draw_screen(None, False, True)

        jnius.autoclass.assert_called_once_with("org.renpy.android.PythonSDLActivity")
        jnius.autoclass.return_value.mActivity.hidePresplash.assert_called_once_with()
        frame.browser.run_script.assert_not_called()
