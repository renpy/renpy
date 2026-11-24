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

    clock[0] += 0.5
    run_check()


def test_raises_after_grace_period(reset_loop_state):
    """
    If the game is still looping when the one-second grace period ends, the exception is raised, and the
    first deadline is pushed out, so the same loop is not reported again until that deadline has passed.
    """

    clock = reset_loop_state

    run_check()

    clock[0] += 1.5

    with pytest.raises(Exception, match="Possible infinite loop"):
        run_check()

    # Without the pushed-out deadline, this would begin a new grace period that ends, and raises, 1.5 seconds on.
    run_check()

    clock[0] += 1.5
    run_check()


@pytest.mark.parametrize("checked_in_window", [True, False], ids=["checked-in-window", "unchecked-in-window"])
def test_progress_cancels_pending_detection(reset_loop_state, checked_in_window):
    """
    If not_infinite_loop is called during the grace period, no exception is raised afterwards, and the
    cancelled grace period does not carry over to the next detection.

    When no check runs before the new first deadline passes (fewer than 100 statements before the next
    suspend), check_infinite_loop never gets to clear the pending second deadline itself, so
    not_infinite_loop has to. If it did not, the next detection would raise at once instead of getting its
    own grace period.
    """

    clock = reset_loop_state

    run_check()

    clock[0] += 0.5
    renpy.execution.not_infinite_loop(10)

    if checked_in_window:
        run_check()

        clock[0] += 5
        run_check()

    # The new first deadline has passed, and the earlier grace period would have ended long ago.
    clock[0] += 100
    run_check()

    clock[0] += 0.5
    run_check()

    clock[0] += 1.5

    with pytest.raises(Exception, match="Possible infinite loop"):
        run_check()


@pytest.fixture
def unhandled_reporting(mocker):
    """
    Sets up handle_exception so that no handler handles an exception: there is no creator-defined handler, and
    Ren'Py's default handler reports it unhandled, as it does for lint, compile, and RENPY_SIMPLE_EXCEPTIONS. The
    traceback formatter is patched because the real one prints and writes traceback.txt.
    """

    mocker.patch.object(renpy.exports, "is_in_test", return_value=False)
    mocker.patch.object(renpy.config, "exception_handler", None)
    te = renpy.error.TracebackException(ValueError())
    mocker.patch.object(renpy.error, "report_exception", return_value=te)
    mocker.patch.object(renpy.display.error, "report_exception", return_value=True)


class StubContext:
    """
    A context with no handler of its own, using Context's exception handling methods without the rest of a
    context's state.
    """

    exception_handler = None

    handle_exception = renpy.execution.Context.handle_exception
    run_exception_handlers = renpy.execution.Context.run_exception_handlers


def run_handle_exception(exception: Exception) -> None:
    """
    Calls handle_exception on a new context while `exception` is being handled, as the statement loop does.
    """

    try:
        raise exception
    except Exception:
        StubContext().handle_exception()


def test_handle_exception_reraises_original_when_handler_fails(mocker, unhandled_reporting, capsys):
    """
    If config.exception_handler itself raises, the original exception is re-raised, as before Ren'Py 8.4, and the
    handler's error is printed rather than hidden.
    """

    mocker.patch.object(renpy.config, "exception_handler", mocker.Mock(side_effect=KeyError("handler bug")))

    with pytest.raises(ValueError, match="original"):
        run_handle_exception(ValueError("original"))

    assert "handler bug" in capsys.readouterr().err
