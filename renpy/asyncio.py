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

from __future__ import annotations

import asyncio
import os
import sys
import threading
import time
from collections.abc import Coroutine
from typing import Any


def _report_slow_task(task: asyncio.Task[Any], dt_ns: int, threshold_ns: int) -> None:
    task_name = task.get_name()
    try:
        coro = task.get_coro()
    except AttributeError:
        coro = None

    if coro is not None:
        coro_name = getattr(coro, "__qualname__", getattr(coro, "__name__", str(coro)))
        code = getattr(coro, "cr_code", None)
        if code is not None:
            location = f" at {code.co_filename}:{code.co_firstlineno}"
        else:
            location = ""
    else:
        coro_name = "coroutine"
        location = ""

    dt_ms = dt_ns / 1_000_000.0
    threshold_ms = threshold_ns / 1_000_000.0
    sys.stdout.write(
        f"Slow async task {task_name!r} ({coro_name}{location}) took {dt_ms:.2f} ms "
        f"(threshold: {threshold_ms:.2f} ms)\n"
    )
    sys.stdout.flush()


class Runner:
    """
    An asyncio runner that can execute coroutines within a synchronous frame loop.
    """

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.tasks: set[asyncio.Task[Any]] = set()

        def _task_factory(loop: asyncio.AbstractEventLoop, coro: Any, **kwargs: Any) -> asyncio.Task[Any]:
            task: asyncio.Task[Any] = asyncio.Task(coro, loop=loop, **kwargs)
            self.tasks.add(task)
            return task

        self.loop.set_task_factory(_task_factory)
        # Setting _stopping = True ensures _run_once uses a zero select timeout.
        self.loop._stopping = True  # type: ignore

        self._orig_call_soon = self.loop._call_soon  # type: ignore
        self._debug_threshold_ns: int | None = None
        self._check_debug_slow_async()

    def _wrap_task_callback(self, callback: Any, task: asyncio.Task[Any], threshold_ns: int) -> Any:
        orig_cb = callback

        def timed_callback(*cb_args: Any) -> Any:
            if self._debug_threshold_ns is None:
                return orig_cb(*cb_args)
            t0 = time.perf_counter_ns()
            try:
                return orig_cb(*cb_args)
            finally:
                dt = time.perf_counter_ns() - t0
                threshold = self._debug_threshold_ns
                if threshold is not None and dt >= threshold:
                    _report_slow_task(task, dt, threshold)

        timed_callback._is_timed_task_cb = True  # type: ignore
        timed_callback._orig_task_cb = orig_cb  # type: ignore
        return timed_callback

    def _make_debug_call_soon(self, threshold_ns: int) -> Any:
        orig_call_soon = self._orig_call_soon

        def debug_call_soon(callback: Any, args: Any, context: Any) -> Any:
            if not getattr(callback, "_is_timed_task_cb", False):
                task = getattr(callback, "__self__", None)
                if isinstance(task, asyncio.Task):
                    callback = self._wrap_task_callback(callback, task, threshold_ns)
            return orig_call_soon(callback, args, context)

        return debug_call_soon

    def _check_debug_slow_async(self) -> None:
        env_val = os.environ.get("RENPY_DEBUG_SLOW_ASYNC")
        if env_val is None:
            if self._debug_threshold_ns is not None:
                self._debug_threshold_ns = None
                self.loop.__dict__.pop("_call_soon", None)
            return

        try:
            threshold_ms = float(env_val)
            threshold_ns = max(0, int(threshold_ms * 1_000_000))
        except ValueError:
            threshold_ns = None

        if threshold_ns != self._debug_threshold_ns:
            self._debug_threshold_ns = threshold_ns
            if threshold_ns is not None:
                self.loop._call_soon = self._make_debug_call_soon(threshold_ns)  # type: ignore
                ready = getattr(self.loop, "_ready", None)
                if ready:
                    for handle in ready:
                        cb = handle._callback
                        if not getattr(cb, "_is_timed_task_cb", False):
                            task = getattr(cb, "__self__", None)
                            if isinstance(task, asyncio.Task):
                                handle._callback = self._wrap_task_callback(cb, task, threshold_ns)
            else:
                self.loop.__dict__.pop("_call_soon", None)

    def create_task(self, coro: Coroutine[Any, Any, Any], name: str | None = None) -> asyncio.Task[Any]:
        """
        Adds a coroutine as a task to be executed by this runner.
        Returns the task object so status and results can be queried.
        """
        self._check_debug_slow_async()
        task = self.loop.create_task(coro, name=name)
        self.tasks.add(task)
        return task

    def run_for_ns(self, ns: int) -> bool:
        """
        Runs tasks until `ns` nanoseconds have elapsed (measured with
        time.perf_counter_ns) or all tasks are done.

        Returns True if at least one task is not done, and False if all tasks
        are done.
        """
        self._check_debug_slow_async()

        if not self.tasks:
            return False

        start = time.perf_counter_ns()
        deadline = start + ns

        try:
            prev_loop = asyncio.get_running_loop()
        except RuntimeError:
            prev_loop = None

        asyncio._set_running_loop(self.loop)
        try:
            self.loop._stopping = True  # type: ignore
            while self.tasks:
                self.loop._run_once()  # type: ignore

                done_tasks = [t for t in self.tasks if t.done()]
                if done_tasks:
                    for t in done_tasks:
                        self.tasks.discard(t)

                    exceptions: list[BaseException] = []
                    for t in done_tasks:
                        if t.cancelled():
                            continue
                        exc = t.exception()
                        if exc is not None:
                            exceptions.append(exc)

                    if exceptions:
                        raise exceptions[0]

                if not self.tasks:
                    return False

                if time.perf_counter_ns() >= deadline:
                    return True
        finally:
            asyncio._set_running_loop(prev_loop)

        return bool(self.tasks)

    def close(self) -> None:
        """
        Cancels all pending tasks and closes the event loop.
        """
        self.reset()
        if self._debug_threshold_ns is not None:
            self._debug_threshold_ns = None
            if not self.loop.is_closed():
                self.loop.__dict__.pop("_call_soon", None)
        if not self.loop.is_closed():
            self.loop.close()

    def reset(self) -> None:
        """
        Cancels and cleans up ongoing tasks without ending the event loop.
        """
        to_cancel = {t for t in self.tasks if not t.done()}
        if not self.loop.is_closed():
            to_cancel.update(t for t in asyncio.all_tasks(self.loop) if not t.done())

        for t in to_cancel:
            t.cancel()

        if not self.loop.is_closed() and (to_cancel or getattr(self.loop, "_ready", None)):
            try:
                prev_loop = asyncio.get_running_loop()
            except RuntimeError:
                prev_loop = None

            asyncio._set_running_loop(self.loop)
            try:
                self.loop._stopping = True  # type: ignore
                steps = 0
                while (to_cancel and any(not t.done() for t in to_cancel)) or getattr(self.loop, "_ready", None):
                    if not getattr(self.loop, "_ready", None):
                        break
                    self.loop._run_once()  # type: ignore
                    for t in self.tasks:
                        if not t.done() and t not in to_cancel:
                            t.cancel()
                            to_cancel.add(t)
                    steps += 1
                    if steps >= 1000:
                        break
            finally:
                asyncio._set_running_loop(prev_loop)

            for t in to_cancel:
                if t.done() and not t.cancelled():
                    t.exception()

        for t in list(self.tasks):
            if t.done() and not t.cancelled():
                t.exception()
        self.tasks.clear()


default_runner = Runner()


def create_task(coro: Coroutine[Any, Any, Any], name: str | None = None) -> asyncio.Task[Any]:
    """
    Adds a coroutine as a task to the default runner.
    """
    return default_runner.create_task(coro, name=name)


def run_for_ns(ns: int) -> bool:
    """
    Runs tasks on the default runner for up to `ns` nanoseconds.
    """
    return default_runner.run_for_ns(ns)


def reset() -> None:
    """
    Resets the default runner by cancelling and cleaning up ongoing tasks without ending the event loop.
    """
    default_runner.reset()


def has_tasks() -> bool:
    """
    Returns True if the default runner has pending tasks.
    """
    return bool(default_runner.tasks)


_sync_loop_state = threading.local()


def run_sync[T](coro: Coroutine[Any, Any, T]) -> T:
    """
    Runs a coroutine task to completion on an event loop dedicated to the
    current thread and shared between calls to run_sync on that thread.
    """
    sync_loop = getattr(_sync_loop_state, "loop", None)
    if sync_loop is None or sync_loop.is_closed():
        sync_loop = asyncio.new_event_loop()
        _sync_loop_state.loop = sync_loop

    try:
        prev_loop = asyncio.get_running_loop()
    except RuntimeError:
        prev_loop = None

    if prev_loop is sync_loop:
        if hasattr(coro, "close"):
            coro.close()
        raise RuntimeError("run_sync cannot be called from within a coroutine running on the sync loop")

    if prev_loop is not None:
        asyncio._set_running_loop(None)
    try:
        return sync_loop.run_until_complete(coro)
    finally:
        if prev_loop is not None:
            asyncio._set_running_loop(prev_loop)
