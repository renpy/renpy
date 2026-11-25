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
Tests for renpy/display/core.py: the cooperative tasks the Interface runs while idle, how it removes the
presplash after drawing the first frame, how the window geometry is held back until it is stable, and how long the
mobile reload save is kept after the app returns to the foreground.
"""

from types import SimpleNamespace

import pytest

import renpy
import renpy.asynctask
from renpy.display import core
from renpy.display.core import WINDOW_GEOMETRY_STABLE_TIME, Interface, WindowGeometryDebouncer

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


################################################################################
# WindowGeometryDebouncer: saving the window geometry once it stops changing
################################################################################

WINDOWED = ((640, 400), (100, 100))
ANIMATING = ((2560, 1305), (0, 25))


def run_geometry_steps(steps: list[tuple[float, object]]) -> list[object]:
    """Pass each (time, geometry) step to a new WindowGeometryDebouncer, returning the geometries it reported."""
    debouncer = WindowGeometryDebouncer()
    rv = []

    for now, geometry in steps:
        reported = debouncer.check(geometry, now)

        if reported is not None:
            rv.append(reported)

    return rv


@pytest.mark.parametrize(
    ("steps", "expected"),
    [
        pytest.param(
            [(0.0, WINDOWED), (WINDOW_GEOMETRY_STABLE_TIME - 0.01, WINDOWED)],
            [],
            id="not-yet-stable",
        ),
        pytest.param(
            [(0.0, WINDOWED), (WINDOW_GEOMETRY_STABLE_TIME, WINDOWED)],
            [WINDOWED],
            id="stable",
        ),
        pytest.param(
            [(0.0, WINDOWED), (1.5, ANIMATING), (2.5, ANIMATING), (1.5 + WINDOW_GEOMETRY_STABLE_TIME, ANIMATING)],
            [ANIMATING],
            id="change-restarts-timer",
        ),
        pytest.param(
            [(0.0, ANIMATING), (0.5, ANIMATING), (1.0, None), (5.0, None)],
            [],
            id="fullscreen-before-stable",
        ),
        pytest.param(
            [(0.0, WINDOWED), (1.0, None), (2.5, WINDOWED), (3.0, WINDOWED)],
            [],
            id="ineligible-clears-pending",
        ),
        pytest.param(
            [(0.0, WINDOWED), (2.0, WINDOWED), (3.0, WINDOWED), (10.0, WINDOWED)],
            [WINDOWED],
            id="reported-once",
        ),
        pytest.param(
            [(0.0, WINDOWED), (2.0, WINDOWED), (3.0, ANIMATING), (5.0, ANIMATING), (6.0, WINDOWED), (8.0, WINDOWED)],
            [WINDOWED, ANIMATING, WINDOWED],
            id="reported-again-after-change",
        ),
        pytest.param(
            [(0.0, WINDOWED), (2.0, WINDOWED), (3.0, None), (4.0, WINDOWED), (6.0, WINDOWED)],
            [WINDOWED, WINDOWED],
            id="reported-again-after-fullscreen",
        ),
    ],
)
def test_stable_window_geometry(steps: list[tuple[float, object]], expected: list[object]) -> None:
    """
    The window geometry is reported only after it has stayed the same for WINDOW_GEOMETRY_STABLE_TIME while
    eligible (None marks a fullscreen, maximized, minimized, or hidden window). This keeps the desktop-sized
    geometry seen during macOS's asynchronous fullscreen animation from being saved as the windowed size (#7549),
    and keeps the preferences from being rewritten every frame once the geometry is stable.
    """
    assert run_geometry_steps(steps) == expected


################################################################################
# Interface.check_suspend / check_mobile_unlink: keeping the mobile reload save after a resume
################################################################################


@pytest.fixture
def resumed(mocker) -> SimpleNamespace:
    """
    Provide an Interface that has gone to the background on a mobile platform and returned to the foreground at
    time 100, by running check_suspend with stubbed audio, timers, and saving. Android is off so check_suspend
    doesn't need jnius or the activity. ``unlink`` records deletions of save slots, and ``clock`` sets the time
    check_mobile_unlink sees.
    """
    interface = Interface.__new__(Interface)
    interface.display_reset = False
    interface.restart_interaction = False
    interface.mobile_unlink_pending = False

    clock = SimpleNamespace(now=100.0)

    mocker.patch.object(renpy, "mobile", True)
    mocker.patch.object(renpy, "android", False)
    mocker.patch.object(renpy.config, "quit_on_mobile_background", False)
    mocker.patch.object(renpy.audio.audio, "pause_all")
    mocker.patch.object(renpy.audio.audio, "unpause_all")
    mocker.patch.object(renpy.exports, "free_memory")
    mocker.patch.object(core.pygame.time, "set_timer")
    mocker.patch.object(core.pygame.event, "wait", return_value=SimpleNamespace(type=core.pygame.DIDENTERFOREGROUND))
    mocker.patch.object(Interface, "mobile_save")
    mocker.patch.object(core, "get_time", side_effect=lambda: clock.now)
    mocker.patch("builtins.print")
    unlink = mocker.patch.object(renpy.loadsave, "unlink_save")

    assert interface.check_suspend(SimpleNamespace(type=core.pygame.WILLENTERBACKGROUND))

    return SimpleNamespace(interface=interface, unlink=unlink, clock=clock)


def test_resume_keeps_reload_save_until_display_reset(resumed) -> None:
    """
    Returning to the foreground requests a display reset but doesn't delete the reload save, and frames drawn while
    that reset is still pending don't count, since the reset (which recreates the GL context on Android) can still
    fail or be interrupted by the activity being destroyed.
    """
    assert resumed.interface.display_reset

    resumed.clock.now = 200.0

    for _ in range(core.MOBILE_UNLINK_FRAMES * 2):
        resumed.interface.check_mobile_unlink()

    resumed.unlink.assert_not_called()


@pytest.mark.parametrize(
    ("frames", "elapsed", "deleted"),
    [
        (core.MOBILE_UNLINK_FRAMES - 1, 10.0, False),
        (core.MOBILE_UNLINK_FRAMES, core.MOBILE_UNLINK_DELAY / 2, False),
        (core.MOBILE_UNLINK_FRAMES, core.MOBILE_UNLINK_DELAY, True),
        (core.MOBILE_UNLINK_FRAMES * 3, 10.0, True),
    ],
)
def test_reload_save_deleted_once_stable(resumed, frames: int, elapsed: float, deleted: bool) -> None:
    """
    After the display reset has run, the reload save is deleted only once enough frames have been drawn and enough
    time has passed since the resume, and only once. Either condition alone keeps it, so a fast device drawing many
    frames quickly and a slow device that takes a while to draw both keep the save while the game settles.
    """
    resumed.interface.display_reset = False
    resumed.clock.now = 100.0 + elapsed

    for _ in range(frames):
        resumed.interface.check_mobile_unlink()

    if deleted:
        resumed.unlink.assert_called_once_with("_reload-1")
    else:
        resumed.unlink.assert_not_called()


def test_new_display_reset_restarts_frame_count(resumed) -> None:
    """
    A display reset requested during the countdown, such as after a failed buffer swap, means the display isn't
    stable yet. Frames drawn before it no longer count, so a single good frame after it can't delete the save.
    """
    resumed.interface.display_reset = False
    resumed.clock.now = 200.0

    for _ in range(core.MOBILE_UNLINK_FRAMES - 1):
        resumed.interface.check_mobile_unlink()

    resumed.interface.display_reset = True
    resumed.interface.check_mobile_unlink()
    resumed.interface.display_reset = False

    resumed.interface.check_mobile_unlink()
    resumed.unlink.assert_not_called()

    for _ in range(core.MOBILE_UNLINK_FRAMES - 1):
        resumed.interface.check_mobile_unlink()

    resumed.unlink.assert_called_once_with("_reload-1")
