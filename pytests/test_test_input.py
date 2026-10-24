import pytest

from renpy import pygame
from renpy.test import testkey


@pytest.mark.parametrize("active", [False, True], ids=["text-input-inactive", "text-input-active"])
def test_printable_key_does_not_require_native_text_input(mocker, active):
    """
    A synthetic printable key press carries its text on the KEYDOWN event whether or not native text
    input is active.

    In a headless test window there may be no active IME, so no TEXTINPUT event would arrive; the test
    runner must not depend on one. Both posted events are marked as test events so they can be told apart
    from real input.
    """

    mocker.patch.object(pygame.key, "text_input_active", return_value=active)
    post = mocker.patch.object(pygame.event, "post")

    testkey.down("a")
    testkey.up("a")

    events = [call.args[0] for call in post.call_args_list]
    assert [event.type for event in events] == [pygame.KEYDOWN, pygame.KEYUP]
    assert events[0].unicode == "a"
    assert events[0].key == pygame.K_a
    assert all(event.test for event in events)


@pytest.mark.parametrize(
    ("keysym", "text", "mods"),
    [
        ("H", "H", pygame.KMOD_LSHIFT),
        ("shift_K_a", "a", pygame.KMOD_LSHIFT),
        ("ctrl_K_a", "a", pygame.KMOD_LCTRL),
        ("alt_K_a", "a", pygame.KMOD_LALT),
    ],
)
def test_uppercase_and_modifiers(mocker, keysym, text, mods):
    """
    Keysyms set the modifiers and text of the single KEYDOWN event they post.

    An uppercase letter implies left shift and keeps its uppercase text. Explicit modifier prefixes set
    the matching left-hand modifier. "shift_K_a" keeps the lowercase "a" because the keysym names the
    key, not the shifted character.
    """

    post = mocker.patch.object(pygame.event, "post")

    testkey.down(keysym)

    event = post.call_args.args[0]
    assert event.unicode == text
    assert event.mod == mods
    post.assert_called_once()


@pytest.mark.parametrize("keysym", ["K_LEFT", "K_BACKSPACE", "K_RETURN"])
def test_navigation_keys_do_not_insert_text(mocker, keysym):
    """
    Navigation and editing keys post a KEYDOWN/KEYUP pair with empty text.

    Backspace and Return have control-character codes (below 32), which must not be inserted into an
    input as text.
    """

    post = mocker.patch.object(pygame.event, "post")

    testkey.queue_keysym(keysym)

    events = [call.args[0] for call in post.call_args_list]
    assert [event.type for event in events] == [pygame.KEYDOWN, pygame.KEYUP]
    assert events[0].unicode == ""


def test_keymap_event_uses_existing_queue(mocker):
    """
    A name found in config.keymap is queued as that keymap event through renpy.queue_event, rather than
    being treated as a key name and posted as key presses.
    """

    mocker.patch.dict(testkey.renpy.config.keymap, {"dismiss": ["K_RETURN"]})
    queue = mocker.patch.object(testkey.renpy.exports, "queue_event")

    testkey.queue_keysym("dismiss")

    queue.assert_called_once_with("dismiss")
