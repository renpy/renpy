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

"""
Tests for renpy/display/core.py: the cooperative tasks the Interface runs while idle, and how it removes the
presplash after drawing the first frame.
"""

from types import SimpleNamespace

import pytest

import renpy
import renpy.asynctask
from renpy.display import core
from renpy.display.core import Interface

################################################################################
# Interface.run_tasks: the texture task
################################################################################


class FakeDraw:
    """A draw object with a fixed number of textures waiting to be uploaded."""

    def __init__(self, pending: int) -> None:
        self.pending: int = pending
        self.processed: int = 0

    def ready_one_texture(self) -> bool:
        if not self.pending:
            return False

        self.pending -= 1
        self.processed += 1
        return True


def run_until_texture_task_done(interface: Interface) -> None:
    """Run idle passes until the interface's texture task finishes, giving up after 10 passes."""
    for _ in range(10):
        interface.run_tasks(False)
        if interface.texture_task.done():
            break


class TestTextureTask:
    """Tests for the texture-upload task that the interface advances once per idle pass."""

    @pytest.fixture
    def runner(self):
        """Provide a Runner that is closed at teardown."""
        runner = renpy.asynctask.Runner()
        yield runner
        runner.close()

    @pytest.fixture
    def draw(self) -> FakeDraw:
        """Provide a draw object with two textures waiting to be uploaded."""
        return FakeDraw(2)

    @pytest.fixture
    def interface(self) -> Interface:
        """Provide an Interface without running its constructor, with no texture task and no forced prediction."""
        interface = Interface.__new__(Interface)
        interface.texture_task = None
        interface.force_prediction = False
        return interface

    @pytest.fixture(autouse=True)
    def texture_environment(self, mocker, runner, draw) -> None:
        """Route drawing and the default runner to the fakes, and remove the prediction time floor."""
        mocker.patch.object(renpy.display, "draw", draw)
        mocker.patch.object(renpy.asynctask, "default_runner", runner)
        mocker.patch.object(renpy.config, "minimum_prediction_time_ns", 0)

    def test_texture_work_each_idle_pass(self, interface, draw, runner) -> None:
        """Each idle pass uploads one texture, the task is reused until it finishes, and a new task starts for new work."""
        interface.run_tasks(False)
        first_task = interface.texture_task
        assert not first_task.done()
        assert draw.processed == 1

        interface.run_tasks(False)
        assert interface.texture_task is first_task
        assert draw.processed == 2

        run_until_texture_task_done(interface)
        assert draw.processed == 2
        assert interface.texture_task.done()
        assert not runner.tasks

        draw.pending = 1
        run_until_texture_task_done(interface)
        assert interface.texture_task is not first_task
        assert interface.texture_task.done()
        assert draw.processed == 3
        assert not runner.tasks


################################################################################
# Interface.draw_screen: removing the presplash after the first frame
################################################################################


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
