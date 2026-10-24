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

"""Tests for the cooperative generator tasks run by the interaction loop."""

import pytest

import renpy
import renpy.asynctask
from renpy.display.core import Interface
from renpy.display.im import Cache


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


class TestPreloadPass:
    """Tests for when the image preload pass yields to the event loop, which only happens on the web."""

    @pytest.fixture
    def cache(self) -> Cache:
        """Provide a Cache without running its constructor, with no preloads and no decode pool."""
        cache = Cache.__new__(Cache)
        cache.preloads = []
        cache.keep_preloading = False
        cache.get_decode_pool = lambda: None
        cache.cleanout = lambda: True
        return cache

    @pytest.fixture
    def pauses(self, mocker) -> list[bool]:
        """Replace the predict sleep with a generator that records each pause, and return the record list."""
        pauses: list[bool] = []

        def pause():
            pauses.append(True)
            yield

        mocker.patch.object(renpy.display.predict, "predict_sleep", pause)
        return pauses

    def test_preload_does_not_yield_off_web(self, cache, pauses, mocker) -> None:
        """Off the web, the preload pass runs to completion without pausing."""
        mocker.patch.object(renpy, "emscripten", False)
        renpy.asynctask.run_sync(cache.preload_thread_pass())

        assert not pauses

    def test_preload_yields_on_web(self, cache, pauses, mocker) -> None:
        """On the web, the preload pass pauses twice: once before its loop and once after cleanout."""
        mocker.patch.object(renpy, "emscripten", True)
        renpy.asynctask.run_sync(cache.preload_thread_pass())

        assert len(pauses) == 2
