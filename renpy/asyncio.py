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
import threading
import time
from collections.abc import Coroutine
from typing import Any


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

    def create_task(self, coro: Coroutine[Any, Any, Any], name: str | None = None) -> asyncio.Task[Any]:
        """
        Adds a coroutine as a task to be executed by this runner.
        Returns the task object so status and results can be queried.
        """
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
