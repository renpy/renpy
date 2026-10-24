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

import unittest
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

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


class TestTextureTask(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = renpy.asynctask.Runner()
        self.addCleanup(self.runner.close)

        self.draw = FakeDraw(2)

        self.interface = Interface.__new__(Interface)
        self.interface.texture_task = None
        self.interface.force_prediction = False

        for patcher in (
            patch.object(renpy.display, "draw", self.draw),
            patch.object(renpy.asynctask, "default_runner", self.runner),
            patch.object(renpy.config, "minimum_prediction_time_ns", 0),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_until_texture_task_done(self) -> None:
        for _ in range(10):
            self.interface.run_tasks(False)
            if self.interface.texture_task.done():
                break

    def test_texture_work_each_idle_pass(self) -> None:
        interface = self.interface

        interface.run_tasks(False)
        first_task = interface.texture_task
        self.assertFalse(first_task.done())
        self.assertEqual(self.draw.processed, 1)

        interface.run_tasks(False)
        self.assertIs(interface.texture_task, first_task)
        self.assertEqual(self.draw.processed, 2)

        self.run_until_texture_task_done()
        self.assertEqual(self.draw.processed, 2)
        self.assertTrue(interface.texture_task.done())
        self.assertFalse(self.runner.tasks)

        self.draw.pending = 1
        self.run_until_texture_task_done()
        self.assertIsNot(interface.texture_task, first_task)
        self.assertTrue(interface.texture_task.done())
        self.assertEqual(self.draw.processed, 3)
        self.assertFalse(self.runner.tasks)


class TestPreloadPass(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = Cache.__new__(Cache)
        self.cache.preloads = []
        self.cache.keep_preloading = False
        self.cache.get_decode_pool = lambda: None
        self.cache.cleanout = lambda: True

        self.pauses: list[bool] = []

        def pause():
            self.pauses.append(True)
            yield

        patcher = patch.object(renpy.display.predict, "predict_sleep", pause)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_preload_does_not_yield_off_web(self) -> None:
        with patch.object(renpy, "emscripten", False):
            renpy.asynctask.run_sync(self.cache.preload_thread_pass())

        self.assertFalse(self.pauses)

    def test_preload_yields_on_web(self) -> None:
        with patch.object(renpy, "emscripten", True):
            renpy.asynctask.run_sync(self.cache.preload_thread_pass())

        self.assertEqual(len(self.pauses), 2)


if __name__ == "__main__":
    unittest.main()
