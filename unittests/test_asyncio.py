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
import threading
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

    def test_reset_preserves_event_loop(self):
        # Reset should preserve the event loop instead of creating a new one.
        loop_before = rasynco.default_runner.loop
        rasynco.reset()
        self.assertIs(rasynco.default_runner.loop, loop_before)
        self.assertFalse(rasynco.default_runner.loop.is_closed())

    def test_reset_cancels_and_cleans_up_ongoing_tasks(self):
        # Ongoing tasks should be cancelled and cleaned up on reset.
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

        loop_before = rasynco.default_runner.loop
        rasynco.reset()

        # Event loop preserved and not closed.
        self.assertIs(rasynco.default_runner.loop, loop_before)
        self.assertFalse(rasynco.default_runner.loop.is_closed())

        # Task cancelled and cleaned up.
        self.assertTrue(task.done())
        self.assertTrue(task.cancelled())
        self.assertTrue(cancelled_cleaned_up)
        self.assertEqual(len(rasynco.default_runner.tasks), 0)
        self.assertFalse(rasynco.has_tasks())

    def test_reset_cleans_up_nested_tasks(self):
        # Nested tasks spawned before reset should also be cancelled and cleaned up.
        child_cancelled = False

        async def child():
            nonlocal child_cancelled
            try:
                await asyncio.sleep(10.0)
            except asyncio.CancelledError:
                child_cancelled = True
                raise

        async def parent():
            asyncio.create_task(child())
            await asyncio.sleep(10.0)

        p_task = rasynco.create_task(parent())
        rasynco.run_for_ns(100_000)
        rasynco.reset()

        self.assertTrue(p_task.done())
        self.assertTrue(child_cancelled)
        self.assertFalse(rasynco.has_tasks())

    def test_runner_usable_after_reset(self):
        # Runner should be fully functional on the same loop after reset.
        async def work1():
            await asyncio.sleep(10.0)

        rasynco.create_task(work1())
        rasynco.run_for_ns(100_000)
        loop_before = rasynco.default_runner.loop
        rasynco.reset()

        self.assertIs(rasynco.default_runner.loop, loop_before)

        async def work2():
            return 999

        t2 = rasynco.create_task(work2())
        rasynco.run_for_ns(10_000_000)
        self.assertTrue(t2.done())
        self.assertEqual(t2.result(), 999)
        self.assertFalse(rasynco.has_tasks())

    def test_run_sync_simple(self):
        # run_sync runs a coroutine to completion and returns the result.
        async def work():
            return 42

        self.assertEqual(rasynco.run_sync(work()), 42)

    def test_run_sync_shared_loop(self):
        # Multiple calls to run_sync in one thread should share the same event loop.
        loops = []

        async def capture_loop():
            loops.append(asyncio.get_running_loop())
            return True

        rasynco.run_sync(capture_loop())
        rasynco.run_sync(capture_loop())

        self.assertEqual(len(loops), 2)
        self.assertIs(loops[0], loops[1])
        self.assertIsNot(loops[0], rasynco.default_runner.loop)

    def test_run_sync_uses_thread_local_loops(self):
        loops = []

        async def capture_loop():
            loops.append(asyncio.get_running_loop())

        thread = threading.Thread(target=lambda: rasynco.run_sync(capture_loop()))
        thread.start()
        thread.join()
        rasynco.run_sync(capture_loop())

        self.assertEqual(len(loops), 2)
        self.assertIsNot(loops[0], loops[1])

    def test_run_sync_with_sleep(self):
        # run_sync correctly advances time/timers to run async operations.
        progress = []

        async def timed_work():
            progress.append("a")
            await asyncio.sleep(0.005)
            progress.append("b")
            return "done"

        result = rasynco.run_sync(timed_work())
        self.assertEqual(result, "done")
        self.assertEqual(progress, ["a", "b"])

    def test_run_sync_propagates_exception(self):
        # Exceptions inside coroutine are propagated and the loop remains usable.
        async def failing():
            await asyncio.sleep(0.001)
            raise ValueError("sync failure")

        with self.assertRaises(ValueError) as ctx:
            rasynco.run_sync(failing())
        self.assertIn("sync failure", str(ctx.exception))

        # Subsequent call works on the shared loop
        async def succeeding():
            return "ok"

        self.assertEqual(rasynco.run_sync(succeeding()), "ok")

    def test_run_sync_with_other_running_loop_active(self):
        # Calling run_sync when another loop is set as current running loop works and restores it.
        asyncio._set_running_loop(rasynco.default_runner.loop)
        try:
            async def work():
                return 123

            self.assertEqual(rasynco.run_sync(work()), 123)
            self.assertIs(asyncio.get_running_loop(), rasynco.default_runner.loop)
        finally:
            asyncio._set_running_loop(None)

    def test_run_sync_nested_call_raises(self):
        # Calling run_sync from inside a coroutine running on the thread's sync loop raises RuntimeError.
        async def inner():
            return 1

        async def outer():
            return rasynco.run_sync(inner())

        with self.assertRaises(RuntimeError):
            rasynco.run_sync(outer())


if __name__ == "__main__":
    unittest.main()
