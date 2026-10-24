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

import contextlib
import io
import os
import time
import unittest
from unittest.mock import patch

import renpy.asynctask as tasks


class TestAsyncTask(unittest.TestCase):
    def setUp(self):
        self.runner = tasks.Runner()

    def tearDown(self):
        self.runner.reset()

    def test_empty_and_result(self):
        self.assertFalse(self.runner.run_for_ns(0))

        def work():
            yield
            return 42

        task = self.runner.create_task(work())
        with self.assertRaises(RuntimeError):
            task.result()
        self.assertTrue(self.runner.run_for_ns(0))
        self.assertFalse(self.runner.run_for_ns(1_000_000))
        self.assertTrue(task.done())
        self.assertFalse(task.cancelled())
        self.assertIsNone(task.exception())
        self.assertEqual(task.result(), 42)
        self.assertFalse(task.cancel())
        self.assertFalse(self.runner.tasks)

    def test_round_robin_and_budget(self):
        order = []

        def work(label):
            for i in range(3):
                order.append((label, i))
                yield

        a = self.runner.create_task(work("a"))
        b = self.runner.create_task(work("b"))
        # A zero budget still performs exactly one step per call.
        for expected in [("a", 0), ("b", 0), ("a", 1), ("b", 1)]:
            self.assertTrue(self.runner.run_for_ns(0))
            self.assertEqual(order[-1], expected)
        while self.runner.run_for_ns(1_000_000):
            pass
        self.assertEqual(order, [("a", 0), ("b", 0), ("a", 1), ("b", 1), ("a", 2), ("b", 2)])
        self.assertTrue(a.done())
        self.assertTrue(b.done())

    def test_budget_checks_clock_after_each_step(self):
        ticks = iter([0, 1, 10])
        order = []

        def work():
            order.append(1)
            yield
            order.append(2)
            yield

        self.runner.create_task(work())
        with patch.object(tasks.time, "perf_counter_ns", side_effect=lambda: next(ticks)):
            self.assertTrue(self.runner.run_for_ns(5))
        self.assertEqual(order, [1, 2])

    def test_cancel_before_start(self):
        events = []

        def work():
            try:
                events.append("started")
                yield
            finally:
                events.append("cleanup")

        task = self.runner.create_task(work())
        self.assertTrue(task.cancel())
        self.assertTrue(task.done())
        self.assertTrue(task.cancelled())
        self.assertEqual(events, [])
        with self.assertRaises(tasks.CancelledError):
            task.result()
        with self.assertRaises(tasks.CancelledError):
            task.exception()
        self.assertEqual(len(self.runner._ready), 0)
        self.assertFalse(task.cancel())
        self.assertFalse(self.runner.run_for_ns(10))

    def test_cancel_only_started_task_clears_ready_queue(self):
        def work():
            yield

        task = self.runner.create_task(work())
        self.assertTrue(self.runner.run_for_ns(0))
        self.assertEqual(list(self.runner._ready), [task])
        self.assertTrue(task.cancel())
        self.assertFalse(task.cancel())
        self.assertTrue(task.cancelled())
        self.assertFalse(self.runner.tasks)
        self.assertFalse(self.runner._ready)

        for _ in range(20):
            task = self.runner.create_task(work())
            self.assertTrue(task.cancel())
            self.assertFalse(task.cancel())
            self.assertFalse(self.runner._ready)

    def test_cancel_different_queued_task_from_running_task(self):
        order = []

        def canceller():
            self.assertTrue(victim.cancel())
            order.append("cancelled")
            yield
            order.append("resumed")

        def work():
            order.append("victim ran")
            yield

        def healthy():
            order.append("healthy ran")
            yield

        own = self.runner.create_task(canceller())
        victim = self.runner.create_task(work())
        remaining = self.runner.create_task(healthy())
        self.assertTrue(self.runner.run_for_ns(0))
        self.assertEqual(list(self.runner._ready), [remaining, own])
        self.assertTrue(victim.cancelled())
        while self.runner.run_for_ns(1_000_000):
            pass
        self.assertEqual(order, ["cancelled", "healthy ran", "resumed"])

    def test_cancel_closes_nested_yield_from(self):
        events = []

        def child():
            try:
                yield
                events.append("unexpected")
            finally:
                events.append("child cleaned")

        def parent():
            try:
                yield from child()
            finally:
                events.append("parent cleaned")

        task = self.runner.create_task(parent())
        self.assertTrue(self.runner.run_for_ns(0))
        task.cancel()
        self.assertEqual(events, ["child cleaned", "parent cleaned"])
        self.assertTrue(task.cancelled())
        self.assertFalse(self.runner.run_for_ns(10))

    def test_reset_closes_all_pending_and_reusable(self):
        events = []

        def work(i):
            try:
                yield
            finally:
                events.append(i)

        a = self.runner.create_task(work("a"))
        b = self.runner.create_task(work("b"))
        self.runner.run_for_ns(0)
        self.runner.run_for_ns(0)
        self.runner.reset()
        self.assertCountEqual(events, ["a", "b"])
        self.assertTrue(a.cancelled())
        self.assertTrue(b.cancelled())
        self.assertFalse(self.runner.tasks)
        self.assertFalse(self.runner.run_for_ns(1))
        self.assertFalse(self.runner.create_task(work("c")).done())

    def test_reset_from_running_task_defers_its_close(self):
        events = []

        def sibling():
            try:
                yield
            finally:
                events.append("sibling closed")

        def calling_reset():
            try:
                self.runner.reset()
                events.append("reset returned")
                yield
            finally:
                events.append("caller closed")

        caller = self.runner.create_task(calling_reset())
        other = self.runner.create_task(sibling())
        self.assertFalse(self.runner.run_for_ns(10_000_000))
        self.assertEqual(events, ["reset returned", "caller closed"])
        self.assertTrue(caller.cancelled())
        self.assertTrue(other.cancelled())

    def test_cleanup_that_yields_is_error_but_other_tasks_are_closed(self):
        events = []

        def bad():
            try:
                yield
            finally:
                events.append("bad")
                yield

        def good():
            try:
                yield
            finally:
                events.append("good")

        bad_task = self.runner.create_task(bad())
        good_task = self.runner.create_task(good())
        self.runner.run_for_ns(0)
        self.runner.run_for_ns(0)
        with self.assertRaisesRegex(RuntimeError, "ignored GeneratorExit"):
            self.runner.reset()
        self.assertCountEqual(events, ["bad", "good"])
        self.assertTrue(bad_task.done())
        self.assertIsInstance(bad_task.exception(), RuntimeError)
        self.assertTrue(good_task.cancelled())
        self.assertFalse(self.runner.tasks)

    def test_exception_propagates_without_discarding_other_work(self):
        events = []

        def bad():
            yield
            raise ValueError("failure")

        def good():
            yield
            events.append("done")

        failed = self.runner.create_task(bad())
        healthy = self.runner.create_task(good())
        self.runner.run_for_ns(0)
        self.runner.run_for_ns(0)
        with self.assertRaisesRegex(ValueError, "failure"):
            self.runner.run_for_ns(0)
        self.assertIsInstance(failed.exception(), ValueError)
        self.assertNotIn(failed, self.runner.tasks)
        self.assertFalse(self.runner.run_for_ns(10_000_000))
        self.assertEqual(events, ["done"])
        self.assertIsNone(healthy.result())

    def test_nested_yield_from_result(self):
        def child():
            yield
            return 17

        def parent():
            return (yield from child()) + 1

        task = self.runner.create_task(parent())
        self.assertTrue(self.runner.run_for_ns(0))
        self.assertFalse(self.runner.run_for_ns(100_000))
        self.assertEqual(task.result(), 18)

    def test_run_sync_and_guard(self):
        def child():
            yield
            return 3

        def parent():
            return (yield from child()) + 2

        self.assertEqual(tasks.run_sync(parent()), 5)

        def outer():
            return tasks.run_sync(child())
            yield  # pragma: no cover

        with self.assertRaisesRegex(RuntimeError, "recursively"):
            tasks.run_sync(outer())
        self.assertEqual(tasks.run_sync(parent()), 5)

    def test_run_sync_closes_on_exception(self):
        events = []

        def work():
            try:
                yield
                raise ValueError("sync failure")
            finally:
                events.append("closed")

        with self.assertRaisesRegex(ValueError, "sync failure"):
            tasks.run_sync(work())
        self.assertEqual(events, ["closed"])

    def test_slow_step_logs_nested_location_and_completed(self):
        def leaf():
            time.sleep(0.003)
            yield

        def root():
            yield from leaf()
            time.sleep(0.003)

        with patch.dict(os.environ, {"RENPY_DEBUG_SLOW_ASYNC": "0.5"}):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                task = self.runner.create_task(root(), name="slow_name")
                while self.runner.run_for_ns(100_000_000):
                    pass
        text = output.getvalue()
        self.assertTrue(task.done())
        self.assertIn("Slow generator task 'slow_name'", text)
        self.assertIn("in root", text)
        self.assertIn("in leaf", text)
        self.assertIn("suspended at", text)
        self.assertIn("completed", text)
        self.assertIn("threshold: 0.50 ms", text)

    def test_slow_step_logs_single_frame_location(self):
        def work():
            time.sleep(0.003)
            yield

        with patch.dict(os.environ, {"RENPY_DEBUG_SLOW_ASYNC": "0.5"}):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                task = self.runner.create_task(work(), name="single_task")
                self.runner.run_for_ns(0)
        text = output.getvalue()
        self.assertFalse(task.done())
        self.assertIn("Slow generator task 'single_task'", text)
        self.assertIn("suspended at", text)
        self.assertIn("in work", text)

    def test_slow_step_disabled_and_invalid_setting(self):
        def work():
            time.sleep(0.001)
            yield

        with patch.dict(os.environ, {"RENPY_DEBUG_SLOW_ASYNC": "invalid"}):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                task = self.runner.create_task(work())
                while self.runner.run_for_ns(10_000_000):
                    pass
            self.assertEqual(output.getvalue(), "")
            self.assertTrue(task.done())
            self.assertIsNone(self.runner._debug_threshold_ns)


if __name__ == "__main__":
    unittest.main()
