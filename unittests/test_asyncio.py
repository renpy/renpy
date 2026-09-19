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

import asyncio
import time
import unittest

import renpy.asyncio as rasynco


class TestAsyncioRunner(unittest.TestCase):
    def setUp(self):
        rasynco.reset()

    def tearDown(self):
        rasynco.reset()

    def test_empty_runner(self):
        # When no tasks exist, run_for_ns should return False immediately.
        self.assertFalse(rasynco.run_for_ns(1_000_000))

    def test_simple_task_execution(self):
        # Task runs to completion and result can be queried.
        async def work():
            return 1234

        task = rasynco.create_task(work())
        self.assertFalse(task.done())

        # Run until completion.
        has_more = rasynco.run_for_ns(50_000_000)
        self.assertFalse(has_more)
        self.assertTrue(task.done())
        self.assertEqual(task.result(), 1234)

        # Finished task should be removed; subsequent run_for_ns returns False.
        self.assertEqual(len(rasynco.default_runner.tasks), 0)
        self.assertFalse(rasynco.run_for_ns(1_000_000))

    def test_multi_step_time_budget(self):
        # Coroutine yields across frames using sleep; run_for_ns returns True
        # while work remains and False when all done.
        progress = []

        async def multi_step():
            progress.append(1)
            await asyncio.sleep(0.005)  # 5 ms
            progress.append(2)
            await asyncio.sleep(0.005)  # 5 ms
            progress.append(3)
            return "finished"

        task = rasynco.create_task(multi_step())

        # Small budget (100 us): should make partial progress or be pending.
        has_more = rasynco.run_for_ns(100_000)
        self.assertTrue(has_more)
        self.assertFalse(task.done())

        # Loop with small frame budgets until finished.
        start = time.perf_counter_ns()
        while rasynco.run_for_ns(1_000_000):  # 1 ms per frame
            # Protect against infinite loop in test
            if time.perf_counter_ns() - start > 1_000_000_000:
                self.fail("Timed out waiting for task to complete")

        self.assertTrue(task.done())
        self.assertEqual(task.result(), "finished")
        self.assertEqual(progress, [1, 2, 3])
        self.assertEqual(len(rasynco.default_runner.tasks), 0)

    def test_task_cancellation(self):
        # Cancelled tasks should not throw exceptions out of run_for_ns
        # and should be removed from the runner.
        cancelled_cleaned_up = False

        async def long_running():
            nonlocal cancelled_cleaned_up
            try:
                await asyncio.sleep(10.0)
            except asyncio.CancelledError:
                cancelled_cleaned_up = True
                raise

        task = rasynco.create_task(long_running())
        self.assertFalse(task.done())

        # Step once so coroutine starts.
        rasynco.run_for_ns(100_000)
        self.assertFalse(task.done())

        # Cancel the task.
        task.cancel()

        # Stepping should process the cancellation without raising CancelledError.
        has_more = rasynco.run_for_ns(10_000_000)
        self.assertFalse(has_more)
        self.assertTrue(task.done())
        self.assertTrue(task.cancelled())
        self.assertTrue(cancelled_cleaned_up)
        self.assertEqual(len(rasynco.default_runner.tasks), 0)

    def test_task_exception_propagation(self):
        # If a task throws an exception, run_for_ns should propagate it
        # and remove the failing task.
        async def failing():
            await asyncio.sleep(0.001)
            raise ValueError("Something went wrong")

        task = rasynco.create_task(failing())

        with self.assertRaises(ValueError) as ctx:
            while rasynco.run_for_ns(10_000_000):
                pass

        self.assertIn("Something went wrong", str(ctx.exception))
        self.assertTrue(task.done())
        self.assertIsInstance(task.exception(), ValueError)
        # Failing task must be removed from the runner.
        self.assertEqual(len(rasynco.default_runner.tasks), 0)

    def test_exception_removes_failing_task_and_retains_healthy(self):
        # If one task fails, it is removed, but remaining tasks can continue.
        async def fail_soon():
            await asyncio.sleep(0.001)
            raise RuntimeError("Task 1 error")

        async def succeed_later():
            await asyncio.sleep(0.005)
            return "healthy"

        t_fail = rasynco.create_task(fail_soon())
        t_ok = rasynco.create_task(succeed_later())

        with self.assertRaises(RuntimeError):
            while rasynco.run_for_ns(10_000_000):
                pass

        # t_fail is done and removed.
        self.assertTrue(t_fail.done())
        self.assertNotIn(t_fail, rasynco.default_runner.tasks)

        # t_ok might still be running or done. If still running, run until completion.
        while rasynco.run_for_ns(10_000_000):
            pass

        self.assertTrue(t_ok.done())
        self.assertEqual(t_ok.result(), "healthy")
        self.assertEqual(len(rasynco.default_runner.tasks), 0)

    def test_nested_create_task(self):
        # Tasks created with asyncio.create_task within running coroutine
        # should also be tracked and executed.
        child_ran = False

        async def child():
            nonlocal child_ran
            await asyncio.sleep(0.001)
            child_ran = True
            return "child_result"

        async def parent():
            return asyncio.create_task(child())

        parent_task = rasynco.create_task(parent())

        while rasynco.run_for_ns(10_000_000):
            pass

        self.assertTrue(parent_task.done())
        child_task = parent_task.result()
        self.assertTrue(child_task.done())
        self.assertEqual(child_task.result(), "child_result")
        self.assertTrue(child_ran)
        self.assertEqual(len(rasynco.default_runner.tasks), 0)

    def test_custom_runner_instance(self):
        # A custom Runner instance can be used independently.
        runner = rasynco.Runner()
        try:
            self.assertFalse(runner.run_for_ns(1_000_000))

            async def custom_work():
                await asyncio.sleep(0.001)
                return "custom"

            task = runner.create_task(custom_work())
            while runner.run_for_ns(10_000_000):
                pass

            self.assertTrue(task.done())
            self.assertEqual(task.result(), "custom")
            self.assertEqual(len(runner.tasks), 0)
        finally:
            runner.close()


if __name__ == "__main__":
    unittest.main()
