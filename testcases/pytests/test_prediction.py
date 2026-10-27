from types import SimpleNamespace

import pytest

import renpy
from renpy.display import predict
from renpy.sl2 import slast


@pytest.fixture
def predicting(mocker):
    """Puts prediction in the predicting state with its pause deadline already reached; restored afterwards."""

    mocker.patch.object(predict, "predicting", True)
    mocker.patch.object(predict, "next_predict_pause_ns", 0)


def test_cancelled_prediction_pause_restores_ui_state(predicting):
    """
    Closing a predict_sleep generator while it is paused restores the prediction and UI state it saved.

    While paused, predict_sleep turns prediction off and resets the ui and screen stacks so other code
    can run. If the prediction task is cancelled at the pause, its finally block must still put back the
    exact same objects; the identity checks catch restoring an equal but different stack.
    """

    old_screen = renpy.ui.screen
    old_stack = renpy.ui.stack
    old_at_stack = renpy.ui.at_stack
    old_imagemap_stack = renpy.ui.imagemap_stack
    old_add_tag = renpy.ui.add_tag
    old_screen_stack = renpy.display.screen.current_screen_stack
    old_current_screen = renpy.display.screen._current_screen

    pause = predict.predict_sleep()
    assert next(pause) is None
    assert not predict.predicting
    pause.close()

    assert predict.predicting
    assert renpy.ui.screen is old_screen
    assert renpy.ui.stack is old_stack
    assert renpy.ui.at_stack is old_at_stack
    assert renpy.ui.imagemap_stack is old_imagemap_stack
    assert renpy.ui.add_tag is old_add_tag
    assert renpy.display.screen.current_screen_stack is old_screen_stack
    assert renpy.display.screen._current_screen is old_current_screen


def test_screen_pause_does_not_postpone_prediction_yield(mocker, predicting):
    """
    A screen-language predict_pause only reports that a pause is due. It leaves the deadline alone, so
    it can't postpone the pause that predict_sleep then takes.

    predict_sleep moves the deadline 100 µs past the (patched) current time when it actually pauses,
    after which predict_pause stops asking for pauses. predict_pause also never yields when prediction
    is off. Patching slast.time.perf_counter_ns patches the shared time module, so predict_sleep sees
    the same clock.
    """

    context = SimpleNamespace(yield_prediction=True)
    mocker.patch.object(slast.time, "perf_counter_ns", return_value=1_000_000)

    assert list(slast.predict_pause(context)) == [None]
    assert predict.next_predict_pause_ns == 0

    pause = predict.predict_sleep()
    assert next(pause) is None
    with pytest.raises(StopIteration):
        next(pause)

    assert predict.next_predict_pause_ns == 1_100_000
    assert list(slast.predict_pause(context)) == []

    predict.predicting = False
    predict.next_predict_pause_ns = 0
    assert list(slast.predict_pause(context)) == []
