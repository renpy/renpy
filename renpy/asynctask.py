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
Immediate cooperative tasks driven by generators.

Each yield (including a yield inside a ``yield from`` chain) gives another
ready task one turn. There are no timers, futures, or event loop: a generator
that needs to wait for an external condition must yield until it is ready.
"""

from __future__ import annotations

import inspect
import os
import sys
import threading
import time
from collections import deque
from collections.abc import Generator
from typing import Any


class CancelledError(Exception):
    """Raised when querying the result of a cancelled task."""


class Task[T]:
    """The status and eventual result of a scheduled generator."""

    def __init__(self, runner: Runner, generator: Generator[Any, None, T], name: str | None = None) -> None:
        self._runner = runner
        self._generator = generator
        self._name = name if name is not None else getattr(generator, "__qualname__", repr(generator))
        self._done = False
        self._cancelled = False
        self._cancel_requested = False
        self._running = False
        self._result: T | None = None
        self._exception: BaseException | None = None

    def get_name(self) -> str:
        return self._name

    def done(self) -> bool:
        return self._done

    def cancelled(self) -> bool:
        return self._cancelled

    def result(self) -> T:
        if not self._done:
            raise RuntimeError("Task is not done")
        if self._cancelled:
            raise CancelledError()
        if self._exception is not None:
            raise self._exception
        return self._result  # type: ignore[return-value]

    def exception(self) -> BaseException | None:
        if not self._done:
            raise RuntimeError("Task is not done")
        if self._cancelled:
            raise CancelledError()
        return self._exception

    def cancel(self) -> bool:
        """Close a pending generator; its finally blocks run, but cannot yield."""
        if self._done:
            return False
        if self._running:
            self._cancel_requested = True
            return True
        self._runner._cancel(self)
        return True


def _suspension_info(generator: Generator[Any, None, Any], done: bool) -> str:
    frames: list[tuple[str, int, str]] = []
    current: Any = generator
    while inspect.isgenerator(current):
        frame = current.gi_frame
        if frame is not None and current.gi_running is False:
            frames.append((frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name))
        current = current.gi_yieldfrom

    if frames:
        return "suspended at " + " -> ".join(
            f"{fn}:{line} in {name}" for fn, line, name in frames
        )
    return "completed" if done else ""


def _report_slow_task(task: Task[Any], dt_ns: int, threshold_ns: int) -> None:
    generator = task._generator
    code = generator.gi_code
    location = f" at {code.co_filename}:{code.co_firstlineno}"
    suspension = _suspension_info(generator, task.done())
    status = f", {suspension}" if suspension else ""
    sys.stdout.write(
        f"Slow generator task {task.get_name()!r} ({generator.__qualname__}{location}{status}) "
        f"took {dt_ns / 1_000_000:.2f} ms (threshold: {threshold_ns / 1_000_000:.2f} ms)\n"
    )
    sys.stdout.flush()


class Runner:
    """Run ready generators in round-robin order, one yield per turn."""

    def __init__(self) -> None:
        self.tasks: set[Task[Any]] = set()
        self._ready: deque[Task[Any]] = deque()
        self._debug_threshold_ns: int | None = None
        self._check_slow_task_threshold()

    def _check_slow_task_threshold(self) -> None:
        value = os.environ.get("RENPY_DEBUG_SLOW_ASYNC")
        try:
            self._debug_threshold_ns = None if value is None else max(0, int(float(value) * 1_000_000))
        except (ValueError, OverflowError):
            self._debug_threshold_ns = None

    def create_task[T](self, generator: Generator[Any, None, T], name: str | None = None) -> Task[T]:
        """Queue a generator without executing it."""
        if not inspect.isgenerator(generator):
            raise TypeError("create_task requires a generator")
        task = Task(self, generator, name)
        self.tasks.add(task)
        self._ready.append(task)
        return task

    def _cancel(self, task: Task[Any]) -> None:
        # Generator.close() injects GeneratorExit, not a catchable cancellation.
        # In particular, closing an unstarted generator must not enter its body.
        try:
            task._generator.close()
        except BaseException as exc:
            task._exception = exc
            raise
        else:
            task._cancelled = True
        finally:
            task._done = True
            self.tasks.discard(task)
            if task in self._ready:
                self._ready.remove(task)

    def run_for_ns(self, ns: int) -> bool:
        """
        Run at least one ready step, then check the elapsed-time budget after
        each step. Return whether tasks remain. Task exceptions propagate.
        """
        self._check_slow_task_threshold()
        if not self.tasks:
            return False
        deadline = time.perf_counter_ns() + ns
        while self.tasks:
            task = self._ready.popleft()
            if task.done():
                continue
            threshold = self._debug_threshold_ns
            start = time.perf_counter_ns() if threshold is not None else 0
            task._running = True
            failure: BaseException | None = None
            try:
                next(task._generator)
            except StopIteration as stop:
                task._result = stop.value
                task._done = True
                self.tasks.discard(task)
            except BaseException as exc:
                task._exception = exc
                task._done = True
                self.tasks.discard(task)
                failure = exc
            finally:
                task._running = False
                if not task.done() and task._cancel_requested:
                    try:
                        self._cancel(task)
                    except BaseException as exc:
                        failure = exc
                elif not task.done():
                    self._ready.append(task)
                if threshold is not None:
                    dt = time.perf_counter_ns() - start
                    if dt >= threshold:
                        _report_slow_task(task, dt, threshold)
            if failure is not None:
                raise failure
            if not self.tasks:
                return False
            if time.perf_counter_ns() >= deadline:
                return True
        return False

    def reset(self) -> None:
        """Close every pending task, running finally blocks without yielding."""
        first_error: BaseException | None = None
        while True:
            task = next((task for task in self.tasks if not task._running), None)
            if task is None:
                break
            try:
                task.cancel()
            except BaseException as exc:
                if first_error is None:
                    first_error = exc
        # A reset from inside a running task cannot close its generator until
        # the current next() returns. Its own cancellation is deferred.
        for task in tuple(self.tasks):
            task._cancel_requested = True
        self._ready.clear()
        if first_error is not None:
            raise first_error

    def close(self) -> None:
        self.reset()


default_runner = Runner()


def create_task[T](generator: Generator[Any, None, T], name: str | None = None) -> Task[T]:
    """Queue a task on the default runner."""
    return default_runner.create_task(generator, name)


def run_for_ns(ns: int) -> bool:
    """Run the default runner for at least one step, up to the time budget."""
    return default_runner.run_for_ns(ns)


def reset() -> None:
    """Close all pending tasks on the default runner."""
    default_runner.reset()


def has_tasks() -> bool:
    """Return whether the default runner has pending work."""
    return bool(default_runner.tasks)


_sync_state = threading.local()


def run_sync[T](generator: Generator[Any, None, T]) -> T:
    """Drain a generator immediately, ignoring yields, and return its value."""
    if getattr(_sync_state, "running", False):
        generator.close()
        raise RuntimeError("run_sync cannot be called recursively")
    _sync_state.running = True
    try:
        while True:
            try:
                next(generator)
            except StopIteration as stop:
                return stop.value
    finally:
        try:
            generator.close()
        finally:
            _sync_state.running = False
