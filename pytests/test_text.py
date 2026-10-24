from types import SimpleNamespace

import pytest

import renpy
from renpy.display.core import IgnoreEvent
from renpy.text import text


@pytest.fixture
def slow_text():
    """A stand-in for a Text displayable that is still showing slow text and allows it to be aborted."""

    return SimpleNamespace(
        slow=True,
        slow_done=None,
        style=SimpleNamespace(slow_abortable=True),
        get_layout=lambda: None,
    )


@pytest.fixture
def event():
    """An opaque event; map_event is patched, so its contents do not matter."""

    return SimpleNamespace()


def test_slow_abort_does_not_consume_event_while_grabbed(mocker, slow_text, event):
    """
    A dismiss event does not abort slow text while another displayable holds the focus grab.

    The event has to be left for the grabbing displayable (for example, a drag in progress), so
    Text.event returns None instead of raising IgnoreEvent, and the text keeps displaying slowly.
    """

    mocker.patch.object(renpy.display.behavior, "map_event", return_value=True)
    mocker.patch.object(renpy.display.focus, "get_grab", return_value=object())

    result = text.Text.event(slow_text, event, 0, 0, 0)

    assert result is None
    assert slow_text.slow


def test_slow_abort_consumes_dismiss_event_without_grab(mocker, slow_text, event):
    """
    Without a focus grab, a dismiss event finishes every abortable slow text and is consumed.

    The displayable is registered in the module-level slow_text list, which is what Text.event walks
    to finish all slow text at once. IgnoreEvent means the click doesn't also advance the dialogue.
    """

    mocker.patch.object(renpy.display.behavior, "map_event", return_value=True)
    mocker.patch.object(renpy.display.focus, "get_grab", return_value=None)
    mocker.patch.object(text, "slow_text", [slow_text])

    with pytest.raises(IgnoreEvent):
        text.Text.event(slow_text, event, 0, 0, 0)

    assert not slow_text.slow
