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
Tests for converting SDL events into Ren'Py event objects in renpy.pygame.event.

The keyboard tests run without a window, so text input is never active. That is the case of a game with no focused input,
where KEYDOWN events get their unicode character from the keyboard layout. With no video subsystem, SDL uses its
default US keymap, so the expected characters are those of a US layout.
"""

import pathlib
import pickle
import re
import sys

import pytest

import renpy.display.behavior
import renpy.display.core
from renpy import pygame

# SDL scancodes (USB HID usage IDs), which renpy.pygame does not expose.
SCANCODE_I: int = 12
SCANCODE_RETURN: int = 40
SCANCODE_BACKSPACE: int = 42
SCANCODE_1: int = 30
SCANCODE_F1: int = 58
SCANCODE_KP_1: int = 89


def make_keydown(scancode: int, key: int, mod: int = 0):
    """
    Returns the event object the event queue would produce for an SDL KEYDOWN with these fields.
    """

    return pygame.event._make_keyboard_event(pygame.KEYDOWN, scancode, key, mod)


@pytest.mark.parametrize(
    "scancode, key, mod, expected",
    [
        (SCANCODE_I, pygame.K_i, 0, "i"),
        (SCANCODE_I, pygame.K_i, pygame.KMOD_LSHIFT, "I"),
        (SCANCODE_I, pygame.K_i, pygame.KMOD_CAPS, "I"),
        (SCANCODE_I, pygame.K_i, pygame.KMOD_LCTRL, "i"),
        (SCANCODE_1, pygame.K_1, 0, "1"),
        (SCANCODE_1, pygame.K_1, pygame.KMOD_RSHIFT, "!"),
        (SCANCODE_F1, pygame.K_F1, 0, ""),
        (SCANCODE_KP_1, pygame.K_KP_1, pygame.KMOD_NUM, ""),
    ],
)
def test_keydown_unicode_without_text_input(scancode, key, mod, expected):
    """
    Without text input, a KEYDOWN gets the character the key types in the layout, with shift and caps lock
    applied, and keys that do not type a character get an empty string.

    Ctrl does not change the character; keymap matching checks it separately. Keypad keycodes are outside
    the Unicode range, even with num lock on, so keypad digits get no character.
    """

    assert make_keydown(scancode, key, mod).unicode == expected


def test_keyup_has_no_unicode():
    """
    A KEYUP never carries a character, so single-character keysyms only match key presses.
    """

    ev = pygame.event._make_keyboard_event(pygame.KEYUP, SCANCODE_I, pygame.K_i, 0)
    assert ev.unicode == ""


def test_single_character_keysym_matches_without_text_input():
    """
    A screen's `key "i"` matches pressing I when no input is focused, and `key "I"` matches shift+I but not I.

    This is the regression in issue #7530: under SDL3, KEYDOWN events had no unicode unless text input was
    active, so single-character keysyms only matched while the player typed in an input.
    """

    plain = make_keydown(SCANCODE_I, pygame.K_i)
    shifted = make_keydown(SCANCODE_I, pygame.K_i, pygame.KMOD_LSHIFT)

    assert renpy.display.behavior.map_event(plain, "i")
    assert not renpy.display.behavior.map_event(plain, "I")
    assert renpy.display.behavior.map_event(shifted, "I")
    assert not renpy.display.behavior.map_event(shifted, "i")


@pytest.mark.parametrize("kind", ["FINGERDOWN", "FINGERUP", "FINGERMOTION", "FINGERCANCELED"])
def test_finger_event_fields(kind):
    """
    Touch finger events carry their touch and finger IDs, position, motion, and pressure, under both the
    pygame 2 names (touch_id, finger_id) and the older camelCase names (touchId, fingerId).

    This is the regression in issue #7541: the conversion read misspelled SDL3 field names, so these events
    raised AttributeError when taken from the queue, and FINGERCANCELED events carried no fields at all.
    The touch ID is above 2**32 to check that 64-bit IDs are not truncated.
    """

    event_type = getattr(pygame, kind)
    touch_id = 2**40 + 12

    ev = pygame.event._make_finger_event(event_type, touch_id, 34, 0.25, 0.75, 0.125, -0.5, 0.5)

    assert ev.type == event_type
    assert ev.touch_id == touch_id
    assert ev.touchId == touch_id
    assert ev.finger_id == 34
    assert ev.fingerId == 34
    assert (ev.x, ev.y) == (0.25, 0.75)
    assert (ev.dx, ev.dy) == (0.125, -0.5)
    assert ev.pressure == 0.5


def test_keydown_with_text_input_leaves_text_to_textinput():
    """
    While text input is active, a printable KEYDOWN gets no unicode, because its text arrives as a separate TEXTINPUT
    event, which Input inserts. Control keys produce no TEXTINPUT, so they keep their control character.
    """

    def keydown(scancode, key, mod=0):
        return pygame.event._make_keyboard_event(pygame.KEYDOWN, scancode, key, mod, text_input=True)

    assert keydown(SCANCODE_I, pygame.K_i).unicode == ""
    assert keydown(SCANCODE_I, pygame.K_i, pygame.KMOD_LSHIFT).unicode == ""
    assert keydown(SCANCODE_RETURN, pygame.K_RETURN).unicode == "\r"
    assert keydown(SCANCODE_BACKSPACE, pygame.K_BACKSPACE).unicode == "\x08"


# Event objects.


def test_event_truthiness():
    """
    NOEVENT is falsy and other events are truthy, as in pygame.
    """

    assert not pygame.event.Event(pygame.NOEVENT)
    assert pygame.event.Event(pygame.KEYDOWN)


def test_event_equality():
    """
    Events are equal when their type and attributes are equal, whatever their timestamps. Comparing an event with a
    non-event is False rather than an error.
    """

    a = pygame.event.Event(pygame.USEREVENT, code=1, timestamp=1.0)
    b = pygame.event.Event(pygame.USEREVENT, {"code": 1}, timestamp=2.0)

    assert a == b
    assert (a != b) is False
    assert a != pygame.event.Event(pygame.USEREVENT, code=2)
    assert a != pygame.event.Event(pygame.USEREVENT + 1, code=1)
    assert (a == 3) is False
    assert a != 3


def test_event_timestamp_field():
    """
    The timestamp defaults to 0.0, can be given to the constructor, and is a float kept out of the attribute
    dictionary, so it neither shows up in `dict` nor affects equality.
    """

    assert pygame.event.Event(pygame.USEREVENT).timestamp == 0.0

    ev = pygame.event.Event(pygame.USEREVENT, code=3, timestamp=1.5)
    assert ev.timestamp == 1.5
    assert "timestamp" not in ev.dict

    ev.timestamp = 2
    assert isinstance(ev.timestamp, float)


def test_event_pickle_round_trip():
    """
    Events survive pickling with their type, attributes, and timestamp. Reload pickles module globals that hold
    events, such as the event queue. An attribute named like internal state must not collide with the timestamp.
    """

    ev = pygame.event.Event(pygame.USEREVENT, code=4, timestamp=1.25)
    ev.extra = "x"
    ev._timestamp = "kept"

    copy = pickle.loads(pickle.dumps(ev, pickle.HIGHEST_PROTOCOL))

    assert type(copy) is type(ev)
    assert copy == ev
    assert copy.type == pygame.USEREVENT
    assert copy.extra == "x"
    assert copy._timestamp == "kept"
    assert copy.timestamp == 1.25


# The event queue.


@pytest.fixture(scope="module")
def sdl_events():
    """
    Initializes SDL's event subsystem, which the tests that push events onto SDL's queue need.
    """

    pygame.event.init()


@pytest.fixture
def event_queue(sdl_events):
    """
    Provides an empty event queue in the default mouse wheel mode, and empties it and restores the mode afterwards.
    """

    pygame.event.get()
    pygame.event.set_mousewheel_buttons(True)

    yield

    pygame.event.get()
    pygame.event.set_mousewheel_buttons(True)


def describe(events):
    """
    Returns (type, button) pairs for `events`, with button None for events without one, for comparing event order.
    """

    return [(ev.type, getattr(ev, "button", None)) for ev in events]


@pytest.mark.parametrize("integer_y, button", [(1, 4), (3, 4), (-1, 5), (-2, 5)])
def test_mousewheel_with_buttons(event_queue, integer_y, button):
    """
    In the default mode, a wheel event gives a single press and release of button 4 (up) or 5 (down), in order, at
    the position carried by the wheel event, and no MOUSEWHEEL. An event carrying several whole steps, as a fast
    flick can on macOS or the web, still gives only one pair.
    """

    pygame.event._push_mousewheel_event(0.0, float(integer_y), integer_y, 12.0, 34.0)

    events = pygame.event.get()

    assert describe(events) == [(pygame.MOUSEBUTTONDOWN, button), (pygame.MOUSEBUTTONUP, button)]

    for ev in events:
        assert ev.pos == (12.0, 34.0)


@pytest.mark.parametrize("x, y", [(1.0, 0.0), (0.0, 0.25)])
def test_mousewheel_without_whole_step(event_queue, x, y):
    """
    In the default mode, horizontal scrolling, and vertical scrolling of less than a step, give no events. In
    particular, they never put a NOEVENT on the queue.
    """

    pygame.event._push_mousewheel_event(x, y, 0, 0.0, 0.0)

    assert pygame.event.get() == []


def test_mousewheel_without_buttons(event_queue):
    """
    With mouse wheel buttons turned off, every wheel event, including one of less than a step, gives a MOUSEWHEEL
    carrying the scroll amounts, and no button events.
    """

    pygame.event.set_mousewheel_buttons(False)
    pygame.event._push_mousewheel_event(0.5, 1.0, 1, 0.0, 0.0)
    pygame.event._push_mousewheel_event(0.0, 0.25, 0, 0.0, 0.0)

    events = pygame.event.get()

    assert describe(events) == [(pygame.MOUSEWHEEL, None), (pygame.MOUSEWHEEL, None)]
    assert [(ev.x, ev.y) for ev in events] == [(0.5, 1.0), (0.0, 0.25)]


def test_merged_motion_keeps_its_timestamp(event_queue):
    """
    Consecutive motion events are merged, and the merged event keeps the timestamp of its last motion, in seconds,
    rather than taking the timestamp of the event that ended the run of motion.

    Timestamps are given explicitly, in nanoseconds, so SDL keeps them rather than using the current time.
    """

    pygame.event._push_mousemotion_event(1.0, 1.0, 1.0, 1.0, timestamp=3_000_000)
    pygame.event._push_mousemotion_event(2.0, 3.0, 1.0, 2.0, timestamp=5_000_000)
    pygame.event._push_user_event(pygame.USEREVENT, timestamp=9_000_000)

    events = pygame.event.get()

    assert [ev.type for ev in events] == [pygame.MOUSEMOTION, pygame.USEREVENT]
    assert events[0].pos == (2.0, 3.0)
    assert events[0].rel == (2.0, 3.0)
    assert events[0].timestamp == pytest.approx(0.005)
    assert events[1].timestamp == pytest.approx(0.009)


def test_merge_motion_keeps_newest_in_place(event_queue):
    """
    merge_motion() leaves one MOUSEMOTION, the newest, in its place in the queue, carrying the position of the newest
    motion and the total movement of all of them. Other events keep their order around it.
    """

    pygame.event._push_mousemotion_event(1.0, 1.0, 1.0, 1.0)
    pygame.event._push_user_event(pygame.USEREVENT)
    pygame.event._push_mousemotion_event(10.0, 20.0, 3.0, 4.0)
    pygame.event._push_user_event(pygame.USEREVENT + 1)

    assert pygame.event.merge_motion()

    events = pygame.event.get()

    assert [ev.type for ev in events] == [pygame.USEREVENT, pygame.MOUSEMOTION, pygame.USEREVENT + 1]
    assert events[1].pos == (10.0, 20.0)
    assert events[1].rel == (4.0, 5.0)


def test_merge_motion_includes_posted_motion(event_queue):
    """
    Motion posted to the queue, as the test runner and the touch emulator do, is merged with motion from SDL.
    """

    pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=(1, 2), rel=(1, 2), buttons=(0, 0, 0)))
    pygame.event._push_user_event(pygame.USEREVENT)
    pygame.event._push_mousemotion_event(30.0, 40.0, 2.0, 1.0)

    assert pygame.event.merge_motion()

    events = pygame.event.get()

    assert [ev.type for ev in events] == [pygame.USEREVENT, pygame.MOUSEMOTION]
    assert events[1].pos == (30.0, 40.0)
    assert events[1].rel == (3.0, 3.0)


def test_merge_motion_with_event_posted_twice(event_queue):
    """
    When the same motion event object is posted twice, only one queue entry is left, so its movement isn't counted
    twice when the queue is read.
    """

    ev = pygame.event.Event(pygame.MOUSEMOTION, pos=(5, 6), rel=(1, 2), buttons=(0, 0, 0))
    pygame.event.post(ev)
    pygame.event._push_user_event(pygame.USEREVENT)
    pygame.event.post(ev)

    assert pygame.event.merge_motion()

    events = pygame.event.get()

    assert [ev.type for ev in events] == [pygame.USEREVENT, pygame.MOUSEMOTION]
    assert events[1].rel == (2, 4)


def test_merge_motion_without_motion(event_queue):
    """
    With no MOUSEMOTION on the queue, merge_motion() returns false and leaves the queue as it was.
    """

    pygame.event._push_user_event(pygame.USEREVENT)

    assert not pygame.event.merge_motion()
    assert [ev.type for ev in pygame.event.get()] == [pygame.USEREVENT]


def test_wait_uses_the_queue(event_queue):
    """
    wait() returns events converted like those from get(): a wheel event comes back as a timestamped button press,
    with its release following it on the queue.
    """

    pygame.event._push_mousewheel_event(0.0, 1.0, 1, 5.0, 6.0, timestamp=7_000_000)

    ev = pygame.event.wait()

    assert (ev.type, ev.button) == (pygame.MOUSEBUTTONDOWN, 4)
    assert ev.timestamp == pytest.approx(0.007)
    assert describe(pygame.event.get()) == [(pygame.MOUSEBUTTONUP, 4)]


def test_posted_event_is_timestamped(event_queue):
    """
    A posted event comes back from the queue as the same object, stamped with the time it was queued.
    """

    ev = pygame.event.Event(pygame.USEREVENT, code=5)
    pygame.event.post(ev)

    events = pygame.event.get()

    assert events == [ev]
    assert events[0] is ev
    assert ev.timestamp > 0.0


def test_failed_post_releases_event(event_queue):
    """
    When SDL refuses a posted event, post() releases the reference it took for the queue, so the event is not leaked.

    SDL refuses the event because a test-only SDL event filter rejects posted events. Blocking the event type would
    not do: SDL still queues pushed events of disabled types.
    """

    ev = pygame.event.Event(pygame.USEREVENT, code=6)

    before = sys.getrefcount(ev)

    pygame.event._reject_posted_events(True)

    try:
        pygame.event.post(ev)
    finally:
        pygame.event._reject_posted_events(False)

    assert sys.getrefcount(ev) == before
    assert pygame.event.get() == []


def test_get_blocked_sequence(event_queue):
    """
    get_blocked accepts a sequence of types, and is true if any of them is blocked.
    """

    pygame.event.set_blocked(pygame.USEREVENT + 2)

    try:
        assert pygame.event.get_blocked([pygame.USEREVENT + 1, pygame.USEREVENT + 2])
        assert not pygame.event.get_blocked([pygame.USEREVENT + 1, pygame.USEREVENT + 3])
        assert pygame.event.get_blocked(pygame.USEREVENT + 2)
    finally:
        pygame.event.set_allowed(pygame.USEREVENT + 2)


def test_event_unpickles_old_format():
    """
    An event pickled by an older version, whose timestamp, in SDL's units, was in the attribute dictionary, loads
    with its type and attributes, and with the old timestamp dropped rather than left in the dictionary.

    The pickle is written out by hand, as older versions produced it: the class, then its attribute dictionary.
    """

    data = (
        b"\x80\x02crenpy.pygame.event\nEventType\n)\x81"
        b"}(X\x05\x00\x00\x00_typeK\x05X\x01\x00\x00\x00aK\x01X\t\x00\x00\x00timestampK{ub."
    )

    ev = pickle.loads(data)

    assert ev.type == 5
    assert ev.dict == {"_type": 5, "a": 1}
    assert ev.timestamp == 0.0
    assert ev == pygame.event.Event(5, a=1)


# Names, aliases, and representation.

# The pygame-ce names that renpy.pygame provides for its own event types.
PYGAME_CE_ALIASES = {
    "WINDOWENTER": "WINDOWMOUSEENTER",
    "WINDOWLEAVE": "WINDOWMOUSELEAVE",
    "WINDOWCLOSE": "WINDOWCLOSEREQUESTED",
    "WINDOWSIZECHANGED": "WINDOWRESIZED",
    "APP_TERMINATING": "TERMINATING",
    "APP_LOWMEMORY": "LOWMEMORY",
    "APP_WILLENTERBACKGROUND": "WILLENTERBACKGROUND",
    "APP_DIDENTERBACKGROUND": "DIDENTERBACKGROUND",
    "APP_WILLENTERFOREGROUND": "WILLENTERFOREGROUND",
    "APP_DIDENTERFOREGROUND": "DIDENTERFOREGROUND",
    "RENDER_TARGETS_RESET": "RENDERTARGETSRESET",
    "RENDER_DEVICE_RESET": "RENDERDEVICERESET",
    "RENDER_DEVICE_LOST": "RENDERDEVICELOST",
}

# The source of renpy.pygame.locals, and the event reference page, which distributions may leave out.
LOCALS_SOURCE = pathlib.Path(renpy.__file__).parent / "pygame" / "locals.pyx"
EVENTS_PAGE = pathlib.Path(renpy.__file__).parent.parent / "sphinx" / "source" / "pygame_events.rst"


def read_event_constants() -> list[str]:
    """
    Returns the name of every event type constant defined in renpy.pygame.locals, skipping the test if the source is
    not available.
    """

    if not LOCALS_SOURCE.exists():
        pytest.skip(f"{LOCALS_SOURCE} is not available")

    return re.findall(r"^([A-Z][A-Z0-9_]*) = SDL_EVENT_", LOCALS_SOURCE.read_text(), re.MULTILINE)


def test_event_class_is_exported():
    """
    pygame.Event is the event class, as in pygame-ce, so code that creates events with it gets the class the queue
    returns.
    """

    assert pygame.Event is pygame.event.Event
    assert isinstance(pygame.Event(pygame.USEREVENT), pygame.event.EventType)


@pytest.mark.parametrize("alias, name", sorted(PYGAME_CE_ALIASES.items()))
def test_pygame_ce_alias(alias, name):
    """
    Each pygame-ce name is the same type as the Ren'Py name, and event_name() still gives the Ren'Py name.
    """

    assert getattr(pygame, alias) == getattr(pygame, name)
    assert getattr(pygame.locals, alias) == getattr(pygame, name)
    assert pygame.event.event_name(getattr(pygame, alias)) == name


def test_every_event_constant_has_a_name():
    """
    Every event constant in renpy.pygame.locals is exported from renpy.pygame, and its type has a name, so events of
    that type have a useful repr().
    """

    names = read_event_constants()

    assert "SCREENKEYBOARDSHOWN" in names

    for name in names:
        assert getattr(pygame, name) == getattr(pygame.locals, name), name
        assert pygame.event.event_name(getattr(pygame, name)) != "UNKNOWN", name


def test_unknown_window_is_none():
    """
    An event from a window id that is not the main window's has None as its window, rather than an error or an id.
    """

    (ev,) = pygame.event._make_event(pygame.WINDOWMOVED, windowID=12345, data1=1, data2=2)

    assert ev.window is None


@pytest.mark.parametrize(
    "ev, expected",
    [
        (pygame.event.Event(pygame.KEYDOWN, key=97, unicode="a"), "<Event(768-KEYDOWN key=97, unicode='a')>"),
        (pygame.event.Event(pygame.USEREVENT + 2, code=1), "<Event(32770-UserEvent2 code=1)>"),
        (pygame.event.Event(0x7FFF), "<Event(32767-UNKNOWN )>"),
        (pygame.event.Event(pygame.WINDOWSIZECHANGED), "<Event(518-WINDOWRESIZED )>"),
    ],
)
def test_event_repr(ev, expected):
    """
    repr() gives the type number and name, then the attributes in name order. User types are numbered from USEREVENT,
    a type with no name is UNKNOWN, and an aliased type uses the Ren'Py name.
    """

    assert repr(ev) == expected


# The event reference page.


def read_event_rows() -> list[list[str]]:
    """
    Returns the cells of each row of the list tables on the event reference page, without the header rows, skipping the
    test if the page is not available.
    """

    if not EVENTS_PAGE.exists():
        pytest.skip(f"{EVENTS_PAGE} is not available")

    rows = []
    cell = None

    for line in EVENTS_PAGE.read_text().splitlines():
        if m := re.match(r"^   \* - (.*)$", line):
            rows.append([m.group(1)])
            cell = rows[-1]
        elif cell is not None and (m := re.match(r"^     - (.*)$", line)):
            cell.append(m.group(1))
        elif cell is not None and (m := re.match(r"^       (\S.*)$", line)):
            cell[-1] += " " + m.group(1)
        else:
            cell = None

    return [row for row in rows if row[0] != "Event"]


def get_row_names(row: list[str]) -> list[str]:
    """
    Returns the event names in the Event cell of `row`, without the SDL names.
    """

    return [name for name in re.findall(r"``([A-Z][A-Z0-9_]*)``", row[0]) if not name.startswith("SDL_")]


def test_events_page_names_every_event():
    """
    The event reference page has a row naming every event type and every event constant, including the pygame-ce and
    older aliases, so a new type or alias fails here until it is documented.
    """

    documented = set()

    for row in read_event_rows():
        assert len(row) == 4, row
        documented.update(get_row_names(row))

    expected = set(pygame.event.event_names.values()) | set(read_event_constants())

    assert sorted(expected - documented) == []


def test_events_page_default_matches_enabled_events():
    """
    The Default column says Yes for exactly the standard event types Ren'Py enables by default, and for user and
    registered types, which are never blocked. Markers and obsolete names say n/a.
    """

    standard = set(pygame.event.get_standard_events())
    types_by_name = {name: t for t, name in pygame.event.event_names.items()}
    obsolete = {"DISPLAYEVENT", "WINDOWEVENT", "SYSWMEVENT", "DOLLARGESTURE", "DOLLARRECORD", "MULTIGESTURE"}
    markers = {"NOEVENT", "DISPLAYFIRST", "PRIVATE0"} | obsolete

    rows = read_event_rows()
    assert len(rows) > 100

    for row in rows:
        name = get_row_names(row)[0]
        default = row[1].split()[0]

        if name in markers:
            assert default == "n/a", name
            continue

        event_type = getattr(pygame, name, None)
        if event_type is None:
            event_type = types_by_name[name]

        if event_type in standard:
            expected = "Yes" if event_type in renpy.display.core.enabled_events else "No"
        else:
            expected = "Yes"

        assert default == expected, name
