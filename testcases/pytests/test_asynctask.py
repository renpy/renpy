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

import os
import time

import pytest

import renpy.asynctask as tasks


@pytest.fixture
def runner():
    """
    Provide a fresh Runner and reset it after the test so pending tasks never leak into the next test.

    reset() closes every task still queued, so a test may leave work behind without affecting others.
    """

    runner = tasks.Runner()
    yield runner
    runner.reset()


def test_empty_and_result(runner):
    """
    An empty runner reports no work, and a task's result is unavailable until it finishes.

    The first run_for_ns(0) advances the task to its yield and reports work remaining. A later call with
    a 1 ms budget finishes it, after which the result, exception, and cancel state describe a completed task.
    """

    assert not runner.run_for_ns(0)

    def work():
        yield
        return 42

    task = runner.create_task(work())
    with pytest.raises(RuntimeError):
        task.result()
    assert runner.run_for_ns(0)
    assert not runner.run_for_ns(1_000_000)
    assert task.done()
    assert not task.cancelled()
    assert task.exception() is None
    assert task.result() == 42
    assert not task.cancel()
    assert not runner.tasks


def test_round_robin_and_budget(runner):
    """
    Tasks take turns one step at a time, and a zero time budget still allows exactly one step per call.

    Two tasks each yield three times. The first four single-step calls interleave them as a0, b0, a1, b1,
    and draining the rest with a 1 ms budget completes the full sequence.
    """

    order = []

    def work(label):
        for i in range(3):
            order.append((label, i))
            yield

    a = runner.create_task(work("a"))
    b = runner.create_task(work("b"))
    for expected in [("a", 0), ("b", 0), ("a", 1), ("b", 1)]:
        assert runner.run_for_ns(0)
        assert order[-1] == expected
    while runner.run_for_ns(1_000_000):
        pass
    assert order == [("a", 0), ("b", 0), ("a", 1), ("b", 1), ("a", 2), ("b", 2)]
    assert a.done()
    assert b.done()


def test_budget_checks_clock_after_each_step(runner, mocker):
    """
    run_for_ns reads the clock after each step, so a step that overruns the budget ends the call.

    The patched clock returns 0, 1, then 10 ns against a 5 ns budget. The first step runs while under
    budget, and the clock reading after the second step ends the call while the task is still pending,
    so run_for_ns reports work remaining. The patch is stopped immediately afterward because it replaces
    the global time.perf_counter_ns.
    """

    ticks = iter([0, 1, 10])
    order = []

    def work():
        order.append(1)
        yield
        order.append(2)
        yield

    runner.create_task(work())
    clock = mocker.patch.object(tasks.time, "perf_counter_ns", side_effect=lambda: next(ticks))
    assert runner.run_for_ns(5)
    mocker.stop(clock)
    assert order == [1, 2]


def test_cancel_before_start(runner):
    """
    Cancelling a task before its first step closes it without ever running its body.

    The generator has never started, so its finally block does not run and "started" never appears. The
    task reports cancelled, result() and exception() both raise CancelledError, and a second cancel
    returns False.
    """

    events = []

    def work():
        try:
            events.append("started")
            yield
        finally:
            events.append("cleanup")

    task = runner.create_task(work())
    assert task.cancel()
    assert task.done()
    assert task.cancelled()
    assert events == []
    with pytest.raises(tasks.CancelledError):
        task.result()
    with pytest.raises(tasks.CancelledError):
        task.exception()
    assert len(runner._ready) == 0
    assert not task.cancel()
    assert not runner.run_for_ns(10)


def test_cancel_only_started_task_clears_ready_queue(runner):
    """
    Cancelling a started task removes it from the ready queue, and repeated cancels are no-ops.

    After one step the task sits in the ready queue. Cancelling it empties both the task list and the queue.
    The loop repeats create-and-cancel 20 times to confirm the queue never keeps a cancelled task.
    """

    def work():
        yield

    task = runner.create_task(work())
    assert runner.run_for_ns(0)
    assert list(runner._ready) == [task]
    assert task.cancel()
    assert not task.cancel()
    assert task.cancelled()
    assert not runner.tasks
    assert not runner._ready

    for _ in range(20):
        task = runner.create_task(work())
        assert task.cancel()
        assert not task.cancel()
        assert not runner._ready


def test_cancel_different_queued_task_from_running_task(runner):
    """
    A running task can cancel another task that is still queued, and the cancelled task never runs.

    The canceller cancels "victim" from inside its first step, then yields and resumes. The expected order
    is cancelled, healthy ran, resumed, and "victim ran" never appears.
    """

    order = []

    def canceller():
        assert victim.cancel()
        order.append("cancelled")
        yield
        order.append("resumed")

    def work():
        order.append("victim ran")
        yield

    def healthy():
        order.append("healthy ran")
        yield

    own = runner.create_task(canceller())
    victim = runner.create_task(work())
    remaining = runner.create_task(healthy())
    assert runner.run_for_ns(0)
    assert list(runner._ready) == [remaining, own]
    assert victim.cancelled()
    while runner.run_for_ns(1_000_000):
        pass
    assert order == ["cancelled", "healthy ran", "resumed"]


def test_cancel_closes_nested_yield_from(runner):
    """
    Cancelling a task closes the whole `yield from` chain, with the innermost generator cleaned up first.

    The parent is suspended inside the child when cancelled. The child's finally block runs before the
    parent's, and "unexpected" never appears because the child is never resumed.
    """

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

    task = runner.create_task(parent())
    assert runner.run_for_ns(0)
    task.cancel()
    assert events == ["child cleaned", "parent cleaned"]
    assert task.cancelled()
    assert not runner.run_for_ns(10)


def test_reset_closes_all_pending_and_reusable(runner):
    """
    reset() closes every pending task, and the runner accepts new tasks afterward.

    Both tasks are suspended at a yield when reset() runs, so both finally blocks execute. Their order is not
    specified, so the recorded events are compared without regard to order. A task created after the reset
    is queued and not yet done.
    """

    events = []

    def work(i):
        try:
            yield
        finally:
            events.append(i)

    a = runner.create_task(work("a"))
    b = runner.create_task(work("b"))
    runner.run_for_ns(0)
    runner.run_for_ns(0)
    runner.reset()
    assert sorted(events) == ["a", "b"]
    assert a.cancelled()
    assert b.cancelled()
    assert not runner.tasks
    assert not runner.run_for_ns(1)
    assert not runner.create_task(work("c")).done()


def test_reset_from_running_task_defers_its_close(runner):
    """
    A task that calls reset() from inside its own step is not closed until that step finishes.

    reset() returns normally to the caller, which records "reset returned" before its own finally block runs
    at the end. The sibling never started, so its body and finally block never run; it is only cancelled.
    """

    events = []

    def sibling():
        try:
            yield
        finally:
            events.append("sibling closed")

    def calling_reset():
        try:
            runner.reset()
            events.append("reset returned")
            yield
        finally:
            events.append("caller closed")

    caller = runner.create_task(calling_reset())
    other = runner.create_task(sibling())
    assert not runner.run_for_ns(10_000_000)
    assert events == ["reset returned", "caller closed"]
    assert caller.cancelled()
    assert other.cancelled()


def test_cleanup_that_yields_is_error_but_other_tasks_are_closed(runner):
    """
    A cleanup block that yields makes reset() raise RuntimeError, but every other task is still closed.

    The bad task yields inside its finally block, which Python reports as "ignored GeneratorExit". reset()
    still closes the good task, and the bad task finishes with that RuntimeError as its exception.
    """

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

    bad_task = runner.create_task(bad())
    good_task = runner.create_task(good())
    runner.run_for_ns(0)
    runner.run_for_ns(0)
    with pytest.raises(RuntimeError, match="ignored GeneratorExit"):
        runner.reset()
    assert sorted(events) == ["bad", "good"]
    assert bad_task.done()
    assert isinstance(bad_task.exception(), RuntimeError)
    assert good_task.cancelled()
    assert not runner.tasks


def test_exception_propagates_without_discarding_other_work(runner):
    """
    An exception raised by one task propagates out of run_for_ns, and unrelated ready work is kept.

    The failing task is removed from the runner with its ValueError stored on the task. The healthy task
    still runs to completion in later calls, and its result is None.
    """

    events = []

    def bad():
        yield
        raise ValueError("failure")

    def good():
        yield
        events.append("done")

    failed = runner.create_task(bad())
    healthy = runner.create_task(good())
    runner.run_for_ns(0)
    runner.run_for_ns(0)
    with pytest.raises(ValueError, match="failure"):
        runner.run_for_ns(0)
    assert isinstance(failed.exception(), ValueError)
    assert failed not in runner.tasks
    assert not runner.run_for_ns(10_000_000)
    assert events == ["done"]
    assert healthy.result() is None


def test_nested_yield_from_result(runner):
    """
    A `yield from` child's return value flows back to the parent, which can transform it before returning.

    The child yields once and returns 17, and the parent returns that value plus one. The task finishes
    within the second call, and its result is 18.
    """

    def child():
        yield
        return 17

    def parent():
        return (yield from child()) + 1

    task = runner.create_task(parent())
    assert runner.run_for_ns(0)
    assert not runner.run_for_ns(100_000)
    assert task.result() == 18


def test_run_sync_and_guard():
    """
    run_sync drives a generator to completion and returns its value, and it refuses to run inside itself.

    Calling run_sync from a generator that is already being driven by run_sync raises RuntimeError
    with "recursively" in the message. The guard must not leave the module unusable, so a later normal
    run_sync still succeeds.
    """

    def child():
        yield
        return 3

    def parent():
        return (yield from child()) + 2

    assert tasks.run_sync(parent()) == 5

    def outer():
        return tasks.run_sync(child())
        yield  # pragma: no cover

    with pytest.raises(RuntimeError, match="recursively"):
        tasks.run_sync(outer())
    assert tasks.run_sync(parent()) == 5


def test_run_sync_closes_on_exception():
    """
    An exception raised inside a generator run by run_sync still runs the generator's finally block.

    The ValueError propagates out of run_sync unchanged, and "closed" is recorded exactly once.
    """

    events = []

    def work():
        try:
            yield
            raise ValueError("sync failure")
        finally:
            events.append("closed")

    with pytest.raises(ValueError, match="sync failure"):
        tasks.run_sync(work())
    assert events == ["closed"]


def test_slow_step_logs_nested_location_and_completed(runner, capsys, mocker):
    """
    A step that exceeds RENPY_DEBUG_SLOW_ASYNC is logged with the nested frame locations and a completion note.

    Both the outer task and the `yield from` child sleep past the 0.5 ms threshold. The report must name the
    task, show the outer and inner frames, mark the suspension point, and note the completion and threshold.
    """

    def leaf():
        time.sleep(0.003)
        yield

    def root():
        yield from leaf()
        time.sleep(0.003)

    mocker.patch.dict(os.environ, {"RENPY_DEBUG_SLOW_ASYNC": "0.5"})
    task = runner.create_task(root(), name="slow_name")
    while runner.run_for_ns(100_000_000):
        pass
    text = capsys.readouterr().out
    assert task.done()
    assert "Slow generator task 'slow_name'" in text
    assert "in root" in text
    assert "in leaf" in text
    assert "suspended at" in text
    assert "completed" in text
    assert "threshold: 0.50 ms" in text


def test_slow_step_logs_single_frame_location(runner, capsys, mocker):
    """
    A slow step that suspends at a single frame logs that frame and names the task, without a completion note.

    The task sleeps past the threshold, yields, and is still pending after one step. The report must name the
    task and the function it is suspended in.
    """

    def work():
        time.sleep(0.003)
        yield

    mocker.patch.dict(os.environ, {"RENPY_DEBUG_SLOW_ASYNC": "0.5"})
    task = runner.create_task(work(), name="single_task")
    runner.run_for_ns(0)
    text = capsys.readouterr().out
    assert not task.done()
    assert "Slow generator task 'single_task'" in text
    assert "suspended at" in text
    assert "in work" in text


def test_slow_step_disabled_and_invalid_setting(runner, capsys, mocker):
    """
    An unparseable RENPY_DEBUG_SLOW_ASYNC value disables slow-step logging and leaves the threshold unset.

    Output must be empty even though the task sleeps, the task still completes normally, and the runner's
    internal threshold stays None.
    """

    def work():
        time.sleep(0.001)
        yield

    mocker.patch.dict(os.environ, {"RENPY_DEBUG_SLOW_ASYNC": "invalid"})
    task = runner.create_task(work())
    while runner.run_for_ns(10_000_000):
        pass
    assert capsys.readouterr().out == ""
    assert task.done()
    assert runner._debug_threshold_ns is None
