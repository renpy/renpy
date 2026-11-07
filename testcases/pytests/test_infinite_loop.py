import pytest

import renpy
import renpy.execution


@pytest.fixture(autouse=True)
def reset_loop_state(mocker):
    """
    Resets the infinite loop detector's module state before and after each test, and controls the clock
    through the returned list so tests are deterministic.
    """

    mocker.patch.object(renpy.execution, "il_statements", 0)
    mocker.patch.object(renpy.execution, "il_first_deadline", 0.0)
    mocker.patch.object(renpy.execution, "il_second_deadline", 0.0)
    mocker.patch.object(renpy.config, "developer", False)

    clock = [1000.0]
    mocker.patch.object(renpy.execution.time, "time", lambda: clock[0])

    return clock


def run_check() -> None:
    """
    Runs enough statements to make check_infinite_loop do a real time check.
    """

    for _ in range(101):
        renpy.execution.check_infinite_loop()


def test_first_detection_gives_grace_period(reset_loop_state):
    """
    When the first deadline has passed, the first check must not raise (the app may have just been
    suspended), and neither must a check within the one-second grace period.
    """

    clock = reset_loop_state

    run_check()
    assert renpy.execution.il_second_deadline == 1001.0

    clock[0] += 0.5
    run_check()


def test_raises_after_grace_period(reset_loop_state):
    """
    If the game is still looping when the one-second grace period ends, the exception is raised and
    the first deadline is pushed out so it is not raised again immediately.
    """

    clock = reset_loop_state

    run_check()

    clock[0] += 1.5

    with pytest.raises(Exception, match="Possible infinite loop"):
        run_check()

    assert renpy.execution.il_first_deadline == clock[0] + 60
    assert renpy.execution.il_second_deadline == 0


def test_progress_cancels_pending_detection(reset_loop_state):
    """
    If not_infinite_loop is called during the grace period, the pending second deadline is dropped
    and no exception is raised afterwards.
    """

    clock = reset_loop_state

    run_check()

    clock[0] += 0.5
    renpy.execution.not_infinite_loop(10)
    run_check()

    assert renpy.execution.il_second_deadline == 0

    clock[0] += 5
    run_check()


def test_stale_second_deadline_is_cleared_by_not_infinite_loop(reset_loop_state):
    """
    A pending second deadline must not survive not_infinite_loop. Fewer than 100 statements run before
    the next suspend, so check_infinite_loop never gets to clear it, and without this the next detection
    would raise at once instead of getting its grace period.
    """

    clock = reset_loop_state

    run_check()

    clock[0] += 0.5
    renpy.execution.not_infinite_loop(10)

    clock[0] += 100
    run_check()

    assert renpy.execution.il_second_deadline == clock[0] + 1
