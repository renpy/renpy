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
Tests for the attributes of every event type renpy.pygame.event converts from SDL.

Each test fills an SDL event structure with known values through the `_make_event` hook, which runs the same
conversion the event queue uses, and compares the complete attribute dictionary of the result, so that a missing,
extra, renamed, or retyped attribute fails. The type lists below drive the parametrizations, and the completeness test
checks that together they name every standard event type.

The tests run without a window, so `window` is None and text input is inactive.
"""

import pytest

from renpy import pygame

# The id SDL gives mouse events synthesized from touches, as the unsigned 32-bit value SDL_MouseID holds.
TOUCH_MOUSEID: int = 2**32 - 1

# An SDL window id that no window in the test process has.
UNKNOWN_WINDOW_ID: int = 12345

# The SDL scancode of the I key, which renpy.pygame does not expose.
SCANCODE_I: int = 12


def convert(event_type: int, **fields) -> list:
    """
    Returns the events the event queue would produce for an SDL event of `event_type` with these SDL fields.
    """

    return pygame.event._make_event(event_type, **fields)


def convert_one(event_type: int, **fields):
    """
    Returns the single event the event queue would produce for an SDL event of `event_type` with these SDL fields,
    checking that it has that type.
    """

    events = convert(event_type, **fields)

    assert len(events) == 1
    assert events[0].type == event_type

    return events[0]


def attributes(ev) -> dict:
    """
    Returns the attributes a game can read from `ev`, without the internal type entry.
    """

    return {k: v for k, v in ev.dict.items() if k != "_type"}


def types(*names: str) -> list[int]:
    """
    Returns the event types with the given constant names.
    """

    return [getattr(pygame, name) for name in names]


@pytest.fixture
def wheel_buttons():
    """
    Lets a test set the mouse wheel mode, and restores the default mode afterwards.
    """

    yield pygame.event.set_mousewheel_buttons
    pygame.event.set_mousewheel_buttons(True)


# ===========================
# Keyboard and text events.
# ===========================

KEYBOARD_TYPES = types("KEYDOWN", "KEYUP")
TEXT_TYPES = types("TEXTINPUT", "TEXTEDITING", "TEXTEDITINGCANDIDATES")
KEYBOARD_DEVICE_TYPES = types("KEYBOARDADDED", "KEYBOARDREMOVED")


@pytest.mark.parametrize("event_type, unicode", [(pygame.KEYDOWN, "i"), (pygame.KEYUP, "")])
@pytest.mark.parametrize("repeat", [False, True])
def test_keyboard_attributes(event_type, unicode, repeat):
    """
    Key events carry the scancode, keycode, modifiers, repeat flag, and window, and a key press without text input
    gets its character from the keyboard layout.
    """

    ev = convert_one(event_type, scancode=SCANCODE_I, key=pygame.K_i, mod=pygame.KMOD_NUM, repeat=repeat)

    assert attributes(ev) == {
        "scancode": SCANCODE_I,
        "key": pygame.K_i,
        "mod": pygame.KMOD_NUM,
        "unicode": unicode,
        "repeat": repeat,
        "window": None,
    }


@pytest.mark.parametrize("text, expected", [("héllo".encode(), "héllo"), (b"\xff\xfe", "")])
def test_textinput_attributes(text, expected):
    """
    TEXTINPUT carries the typed text and the window, and text that is not valid UTF-8 becomes an empty string
    rather than an error when the event is taken from the queue.
    """

    ev = convert_one(pygame.TEXTINPUT, text=text)

    assert attributes(ev) == {"text": expected, "window": None}


@pytest.mark.parametrize("text, expected", [("日本".encode(), "日本"), (b"\xff", "")])
def test_textediting_attributes(text, expected):
    """
    TEXTEDITING carries the composition text, cursor start and length, and the window. Invalid UTF-8 gives an empty
    string.
    """

    ev = convert_one(pygame.TEXTEDITING, text=text, start=1, length=2)

    assert attributes(ev) == {"text": expected, "start": 1, "length": 2, "window": None}


@pytest.mark.parametrize(
    "candidates, expected",
    [
        (["你".encode(), None, b"b\xff"], ["你", "", "b�"]),
        (None, []),
    ],
)
@pytest.mark.parametrize("horizontal", [False, True])
def test_texteditingcandidates_attributes(candidates, expected, horizontal):
    """
    TEXTEDITINGCANDIDATES carries the candidate list, the selected index, the layout direction, and the window, under
    both `window_id` and `window`. A NULL candidate becomes an empty string, invalid UTF-8 is replaced rather than
    dropped, and a NULL list gives no candidates.
    """

    ev = convert_one(
        pygame.TEXTEDITINGCANDIDATES,
        candidates=candidates,
        selected_candidate=1,
        horizontal=horizontal,
        windowID=UNKNOWN_WINDOW_ID,
    )

    assert attributes(ev) == {
        "candidates": expected,
        "selected": 1,
        "horizontal": horizontal,
        "window_id": UNKNOWN_WINDOW_ID,
        "window": None,
    }


@pytest.mark.parametrize("event_type", KEYBOARD_DEVICE_TYPES)
def test_keyboard_device_attributes(event_type):
    """
    Keyboard added and removed events carry the keyboard's id.
    """

    assert attributes(convert_one(event_type, which=7)) == {"which": 7}


# ===============
# Mouse events.
# ===============

MOUSE_TYPES = types("MOUSEMOTION", "MOUSEBUTTONDOWN", "MOUSEBUTTONUP", "MOUSEWHEEL")
MOUSE_DEVICE_TYPES = types("MOUSEADDED", "MOUSEREMOVED")


@pytest.mark.parametrize(
    "state, buttons",
    [
        (0, (0, 0, 0)),
        (pygame.BUTTON_LMASK, (1, 0, 0)),
        (pygame.BUTTON_MMASK, (0, 1, 0)),
        (pygame.BUTTON_RMASK, (0, 0, 1)),
        (pygame.BUTTON_LMASK | pygame.BUTTON_MMASK | pygame.BUTTON_RMASK, (1, 1, 1)),
    ],
)
@pytest.mark.parametrize("which, touch", [(3, False), (TOUCH_MOUSEID, True)])
def test_mousemotion_attributes(state, buttons, which, touch):
    """
    MOUSEMOTION carries the position, relative motion, the state of the left, middle, and right buttons, the mouse id,
    whether the motion came from a touch, and the window.
    """

    ev = convert_one(pygame.MOUSEMOTION, x=1.5, y=2.5, xrel=-1.0, yrel=3.0, state=state, which=which)

    assert attributes(ev) == {
        "pos": (1.5, 2.5),
        "rel": (-1.0, 3.0),
        "which": which,
        "buttons": buttons,
        "touch": touch,
        "window": None,
    }


@pytest.mark.parametrize("event_type", types("MOUSEBUTTONDOWN", "MOUSEBUTTONUP"))
@pytest.mark.parametrize(
    "mode, button, expected",
    [
        (True, 1, 1),
        (True, 3, 3),
        (True, 4, 6),
        (True, 5, 7),
        (False, 1, 1),
        (False, 4, 4),
        (False, 5, 5),
    ],
)
def test_mousebutton_attributes(wheel_buttons, event_type, mode, button, expected):
    """
    Mouse button events carry the button, position, mouse id, touch flag, click count, and window. While the wheel is
    reported as buttons 4 and 5, buttons 4 and above are moved up by two to make room; otherwise they are unchanged.
    """

    wheel_buttons(mode)

    ev = convert_one(event_type, button=button, x=4.0, y=5.0, which=TOUCH_MOUSEID, clicks=2)

    assert attributes(ev) == {
        "button": expected,
        "pos": (4.0, 5.0),
        "which": TOUCH_MOUSEID,
        "touch": True,
        "clicks": 2,
        "window": None,
    }


@pytest.mark.parametrize("integer_y, button", [(2, 4), (-1, 5)])
def test_mousewheel_as_buttons_attributes(wheel_buttons, integer_y, button):
    """
    In the default mode, a wheel step gives a press and release of button 4 or 5, with the same attributes as a real
    button event: the mouse position from the wheel event, a click count of one, and the window.
    """

    wheel_buttons(True)

    events = convert(pygame.MOUSEWHEEL, y=float(integer_y), integer_y=integer_y, mouse_x=7.0, mouse_y=8.0, which=2)

    assert [ev.type for ev in events] == [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]

    for ev in events:
        assert attributes(ev) == {
            "which": 2,
            "button": button,
            "pos": (7.0, 8.0),
            "touch": False,
            "clicks": 1,
            "window": None,
        }


@pytest.mark.parametrize("direction, flipped", [(0, False), (1, True)])
def test_mousewheel_attributes(wheel_buttons, direction, flipped):
    """
    With wheel buttons off, MOUSEWHEEL carries the scroll amounts as floats, under both `x`/`y` and pygame-ce's
    `precise_x`/`precise_y`, whether the direction is flipped (SDL's direction 1), the mouse position, the mouse id,
    the touch flag, and the window.
    """

    wheel_buttons(False)

    ev = convert_one(
        pygame.MOUSEWHEEL, x=0.5, y=-1.25, integer_y=-1, direction=direction, mouse_x=9.0, mouse_y=10.0, which=4
    )

    assert attributes(ev) == {
        "which": 4,
        "x": 0.5,
        "y": -1.25,
        "touch": False,
        "flipped": flipped,
        "precise_x": 0.5,
        "precise_y": -1.25,
        "pos": (9.0, 10.0),
        "window": None,
    }


@pytest.mark.parametrize("event_type", MOUSE_DEVICE_TYPES)
def test_mouse_device_attributes(event_type):
    """
    Mouse added and removed events carry the mouse's id.
    """

    assert attributes(convert_one(event_type, which=9)) == {"which": 9}


# ==================
# Joystick events.
# ==================

JOYSTICK_TYPES = types(
    "JOYSTICKAXISMOTION",
    "JOYSTICKBALLMOTION",
    "JOYSTICKHATMOTION",
    "JOYSTICKBUTTONDOWN",
    "JOYSTICKBUTTONUP",
    "JOYSTICKADDED",
    "JOYSTICKREMOVED",
    "JOYSTICKBATTERYUPDATED",
)


@pytest.mark.parametrize("value, expected", [(0, 0.0), (16384, 0.5), (-32768, -1.0), (32767, 32767 / 32768.0)])
def test_joyaxis_attributes(value, expected):
    """
    JOYAXISMOTION carries the joystick, axis, and value scaled to a float from -1.0 to just under 1.0.
    """

    ev = convert_one(pygame.JOYAXISMOTION, which=5, axis=2, value=value)

    assert attributes(ev) == {"joy": 5, "instance_id": 5, "axis": 2, "value": expected}


def test_joyball_attributes():
    """
    JOYBALLMOTION carries the joystick, ball, and relative motion.
    """

    ev = convert_one(pygame.JOYBALLMOTION, which=5, ball=1, xrel=-3, yrel=4)

    assert attributes(ev) == {"joy": 5, "instance_id": 5, "ball": 1, "rel": (-3, 4)}


# SDL hat masks: up 1, right 2, down 4, left 8.
HAT_POSITIONS = [
    (0, (0, 0)),
    (1, (0, 1)),
    (2, (1, 0)),
    (4, (0, -1)),
    (8, (-1, 0)),
    (3, (1, 1)),
    (6, (1, -1)),
    (12, (-1, -1)),
    (9, (-1, 1)),
]


@pytest.mark.parametrize("mask, value", HAT_POSITIONS)
def test_joyhat_attributes(mask, value):
    """
    JOYHATMOTION carries the joystick, hat, and position as pygame's (x, y) tuple, with x -1 for left and 1 for right,
    and y 1 for up and -1 for down, for each of the nine hat positions.
    """

    ev = convert_one(pygame.JOYHATMOTION, which=5, hat=1, value=mask)

    assert attributes(ev) == {"joy": 5, "instance_id": 5, "hat": 1, "value": value}


@pytest.mark.parametrize("mask, value", HAT_POSITIONS)
def test_convert_hat_value(mask, value):
    """
    The conversion that Joystick.get_hat shares with JOYHATMOTION gives the same tuple as the event.
    """

    assert pygame.event.convert_hat_value(mask) == value


@pytest.mark.parametrize("event_type", types("JOYSTICKBUTTONDOWN", "JOYSTICKBUTTONUP"))
def test_joybutton_attributes(event_type):
    """
    Joystick button events carry the joystick and button.
    """

    ev = convert_one(event_type, which=5, button=3, down=event_type == pygame.JOYBUTTONDOWN)

    assert attributes(ev) == {"joy": 5, "instance_id": 5, "button": 3}


def test_joystick_added_attributes():
    """
    JOYSTICKADDED carries the joystick's instance id under `which`, `device_index`, and `instance_id`, and its GUID
    as a hex string. SDL has no joystick with this id, so the GUID is all zeros.
    """

    ev = convert_one(pygame.JOYSTICKADDED, which=1234)

    assert attributes(ev) == {"which": 1234, "device_index": 1234, "instance_id": 1234, "guid": "0" * 32}


def test_joystick_removed_attributes():
    """
    JOYSTICKREMOVED carries the joystick's instance id under `which` and `instance_id`.
    """

    assert attributes(convert_one(pygame.JOYSTICKREMOVED, which=6)) == {"which": 6, "instance_id": 6}


def test_joystick_battery_attributes():
    """
    JOYSTICKBATTERYUPDATED carries the joystick, its power state, and its charge percentage.
    """

    ev = convert_one(pygame.JOYSTICKBATTERYUPDATED, which=6, state=pygame.POWERSTATE_ON_BATTERY, percent=42)

    assert attributes(ev) == {"which": 6, "instance_id": 6, "state": pygame.POWERSTATE_ON_BATTERY, "percent": 42}


# =================
# Gamepad events.
# =================

GAMEPAD_TYPES = types(
    "GAMEPADAXISMOTION",
    "GAMEPADBUTTONDOWN",
    "GAMEPADBUTTONUP",
    "GAMEPADADDED",
    "GAMEPADREMOVED",
    "GAMEPADREMAPPED",
    "GAMEPADTOUCHPADDOWN",
    "GAMEPADTOUCHPADMOTION",
    "GAMEPADTOUCHPADUP",
    "GAMEPADSENSORUPDATE",
)


@pytest.mark.parametrize("value", [-32768, 0, 12345, 32767])
def test_gamepad_axis_attributes(value):
    """
    GAMEPADAXISMOTION carries the gamepad, axis, and raw, unscaled integer value.
    """

    ev = convert_one(pygame.GAMEPADAXISMOTION, which=8, axis=pygame.GAMEPAD_AXIS_RIGHTY, value=value)

    assert attributes(ev) == {"which": 8, "instance_id": 8, "axis": pygame.GAMEPAD_AXIS_RIGHTY, "value": value}


@pytest.mark.parametrize("event_type, down", [(pygame.GAMEPADBUTTONDOWN, True), (pygame.GAMEPADBUTTONUP, False)])
def test_gamepad_button_attributes(event_type, down):
    """
    Gamepad button events carry the gamepad, the button, and whether it is pressed, as `state`.
    """

    ev = convert_one(event_type, which=8, button=pygame.GAMEPAD_BUTTON_SOUTH, down=down)

    assert attributes(ev) == {"which": 8, "instance_id": 8, "button": pygame.GAMEPAD_BUTTON_SOUTH, "state": down}


def test_gamepad_added_attributes():
    """
    GAMEPADADDED carries the gamepad's instance id under `which`, `device_index`, and `instance_id`, and its GUID. SDL
    has no gamepad with this id, so the GUID is all zeros.
    """

    ev = convert_one(pygame.GAMEPADADDED, which=4321)

    assert attributes(ev) == {"which": 4321, "device_index": 4321, "instance_id": 4321, "guid": "0" * 32}


@pytest.mark.parametrize("event_type", types("GAMEPADREMOVED", "GAMEPADREMAPPED"))
def test_gamepad_device_attributes(event_type):
    """
    Gamepad removed and remapped events carry the gamepad's instance id under `which` and `instance_id`.
    """

    assert attributes(convert_one(event_type, which=8)) == {"which": 8, "instance_id": 8}


@pytest.mark.parametrize("event_type", types("GAMEPADTOUCHPADDOWN", "GAMEPADTOUCHPADMOTION", "GAMEPADTOUCHPADUP"))
def test_gamepad_touchpad_attributes(event_type):
    """
    Gamepad touchpad events carry the gamepad, the touchpad and finger as pygame-ce's `touch_id` and `finger_id`, and
    the normalized position and pressure.
    """

    ev = convert_one(event_type, which=8, touchpad=1, finger=2, x=0.25, y=0.5, pressure=0.75)

    assert attributes(ev) == {
        "which": 8,
        "instance_id": 8,
        "touch_id": 1,
        "finger_id": 2,
        "x": 0.25,
        "y": 0.5,
        "pressure": 0.75,
    }


def test_gamepad_sensor_attributes():
    """
    GAMEPADSENSORUPDATE carries the gamepad, the sensor type, and the three sensor readings as a tuple.
    """

    ev = convert_one(pygame.GAMEPADSENSORUPDATE, which=8, sensor=2, data=[0.5, -1.0, 2.0])

    assert attributes(ev) == {"which": 8, "instance_id": 8, "sensor": 2, "data": (0.5, -1.0, 2.0)}


# =========================
# Touch and drop events.
# =========================

FINGER_TYPES = types("FINGERDOWN", "FINGERUP", "FINGERMOTION", "FINGERCANCELED")
PINCH_TYPES = types("PINCHBEGIN", "PINCHUPDATE", "PINCHEND")
DROP_TYPES = types("DROPFILE", "DROPTEXT", "DROPBEGIN", "DROPCOMPLETE", "DROPPOSITION")


@pytest.mark.parametrize("event_type", FINGER_TYPES)
def test_finger_attributes(event_type):
    """
    Finger events carry the touch and finger ids under both naming styles, the position, motion, pressure, and
    window. The touch id is above 2**32 to check that 64-bit ids are kept.
    """

    touch_id = 2**40 + 12

    ev = convert_one(event_type, touchID=touch_id, fingerID=34, x=0.25, y=0.75, dx=0.125, dy=-0.5, pressure=0.5)

    assert attributes(ev) == {
        "touchId": touch_id,
        "fingerId": 34,
        "touch_id": touch_id,
        "finger_id": 34,
        "x": 0.25,
        "y": 0.75,
        "dx": 0.125,
        "dy": -0.5,
        "pressure": 0.5,
        "window": None,
    }


@pytest.mark.parametrize("event_type", PINCH_TYPES)
def test_pinch_attributes(event_type):
    """
    Pinch events carry the scale factor and window.
    """

    assert attributes(convert_one(event_type, scale=1.5)) == {"scale": 1.5, "window": None}


@pytest.mark.parametrize("event_type", DROP_TYPES)
@pytest.mark.parametrize("data, file", [(b"/tmp/dropped.txt", "/tmp/dropped.txt"), (None, None)])
def test_drop_attributes(event_type, data, file):
    """
    Drop events carry the dropped file name or text as `file` (None when SDL gives none), the window under both
    `window_id` and `window`, and the drop position. DROPTEXT also gives the text as pygame-ce's `text`.
    """

    ev = convert_one(event_type, data=data, x=3.0, y=4.0, windowID=UNKNOWN_WINDOW_ID)

    expected = {"file": file, "window_id": UNKNOWN_WINDOW_ID, "window": None, "x": 3.0, "y": 4.0}

    if event_type == pygame.DROPTEXT:
        expected["text"] = file

    assert attributes(ev) == expected


# ===================================
# Window, display, and app events.
# ===================================

# Every type in the window range, so a window event SDL adds later is covered as soon as it is named.
WINDOW_TYPES = [t for t in pygame.event.get_standard_events() if pygame.WINDOWFIRST <= t <= pygame.WINDOWLAST]
DISPLAY_TYPES = [t for t in pygame.event.get_standard_events() if pygame.DISPLAYFIRST <= t <= pygame.DISPLAYLAST]

# Types whose events have no attributes.
NO_ATTRIBUTE_TYPES = types(
    "QUIT",
    "TERMINATING",
    "LOWMEMORY",
    "WILLENTERBACKGROUND",
    "DIDENTERBACKGROUND",
    "WILLENTERFOREGROUND",
    "DIDENTERFOREGROUND",
    "LOCALECHANGED",
    "SYSTEMTHEMECHANGED",
    "KEYMAPCHANGED",
    "SCREENKEYBOARDSHOWN",
    "SCREENKEYBOARDHIDDEN",
    "CLIPBOARDUPDATE",
    "RENDERTARGETSRESET",
    "RENDERDEVICERESET",
    "RENDERDEVICELOST",
    "JOYSTICKUPDATECOMPLETE",
    "GAMEPADUPDATECOMPLETE",
    "GAMEPADSTEAMHANDLEUPDATED",
)


@pytest.mark.parametrize("event_type", WINDOW_TYPES, ids=pygame.event.event_name)
def test_window_attributes(event_type):
    """
    Every window event carries `data1`, `data2`, and the window. Moved, resized, and pixel-size-changed events also
    give the data as pygame-ce's `x` and `y`, and display-changed events give the display as `display_index`.
    """

    ev = convert_one(event_type, data1=640, data2=-480, windowID=UNKNOWN_WINDOW_ID)

    expected = {"data1": 640, "data2": -480, "window": None}

    if event_type in (pygame.WINDOWMOVED, pygame.WINDOWRESIZED, pygame.WINDOWPIXELSIZECHANGED):
        expected.update(x=640, y=-480)
    elif event_type == pygame.WINDOWDISPLAYCHANGED:
        expected.update(display_index=640)

    assert attributes(ev) == expected


@pytest.mark.parametrize("event_type", DISPLAY_TYPES, ids=pygame.event.event_name)
def test_display_attributes(event_type):
    """
    Every display event carries the display's id as `display_index`, and SDL's `data1` and `data2`.
    """

    ev = convert_one(event_type, displayID=3, data1=1, data2=2)

    assert attributes(ev) == {"display_index": 3, "data1": 1, "data2": 2}


@pytest.mark.parametrize("event_type", NO_ATTRIBUTE_TYPES, ids=pygame.event.event_name)
def test_no_attribute_events(event_type):
    """
    Lifecycle, locale, theme, keymap, screen keyboard, clipboard, render, and update-complete events convert to an
    event of their type with no attributes.
    """

    assert attributes(convert_one(event_type)) == {}


# ======================================
# Audio, camera, sensor, and pen events.
# ======================================

AUDIO_TYPES = types("AUDIODEVICEADDED", "AUDIODEVICEREMOVED", "AUDIODEVICEFORMATCHANGED")
CAMERA_TYPES = types("CAMERADEVICEADDED", "CAMERADEVICEREMOVED", "CAMERADEVICEAPPROVED", "CAMERADEVICEDENIED")
SENSOR_TYPES = types("SENSORUPDATE")
PEN_TYPES = types(
    "PENPROXIMITYIN", "PENPROXIMITYOUT", "PENDOWN", "PENUP", "PENBUTTONDOWN", "PENBUTTONUP", "PENMOTION", "PENAXIS"
)


@pytest.mark.parametrize("event_type", AUDIO_TYPES)
@pytest.mark.parametrize("recording", [False, True])
def test_audio_device_attributes(event_type, recording):
    """
    Audio device events carry the device id and whether it is a recording device, as pygame-ce's `iscapture`.
    """

    ev = convert_one(event_type, which=11, recording=recording)

    assert attributes(ev) == {"which": 11, "iscapture": recording}


@pytest.mark.parametrize("event_type", CAMERA_TYPES)
def test_camera_device_attributes(event_type):
    """
    Camera device events carry the camera's id.
    """

    assert attributes(convert_one(event_type, which=12)) == {"which": 12}


def test_sensor_attributes():
    """
    SENSORUPDATE carries the sensor's id under `which` and `instance_id`, and its six readings as a tuple.
    """

    ev = convert_one(pygame.SENSORUPDATE, which=13, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.5])

    assert attributes(ev) == {"which": 13, "instance_id": 13, "data": (1.0, 2.0, 3.0, 4.0, 5.0, 6.5)}


@pytest.mark.parametrize("event_type", PEN_TYPES, ids=pygame.event.event_name)
def test_pen_attributes(event_type):
    """
    Every pen event carries the pen's id and the window. All but the proximity events add the pen's state flags and
    position, and the touch, button, and axis events add the fields that describe what changed.
    """

    ev = convert_one(
        event_type, which=14, pen_state=5, x=1.5, y=2.5, eraser=True, down=True, button=2, axis=1, value=0.75
    )

    expected = {"which": 14, "window": None}

    if event_type not in (pygame.PENPROXIMITYIN, pygame.PENPROXIMITYOUT):
        expected.update(pen_state=5, x=1.5, y=2.5)

    if event_type in (pygame.PENDOWN, pygame.PENUP):
        expected.update(eraser=True, down=True)
    elif event_type in (pygame.PENBUTTONDOWN, pygame.PENBUTTONUP):
        expected.update(button=2, down=True)
    elif event_type == pygame.PENAXIS:
        expected.update(axis=1, value=0.75)

    assert attributes(ev) == expected


# =============================
# User events and completeness.
# =============================


@pytest.mark.parametrize("offset", [0, 7])
def test_user_event_attributes(offset):
    """
    An event of a user type carries the SDL user event's code.
    """

    ev = convert_one(pygame.USEREVENT + offset, code=99)

    assert attributes(ev) == {"code": 99}


# Names of event types that SDL uses as range markers or reserves, and which never reach a game.
SENTINEL_NAMES = {"FIRST", "PRIVATE0", "PRIVATE1", "PRIVATE2", "PRIVATE3", "POLLSENTINEL", "LAST", "ENUMPADDING"}

# Every type the parametrizations above cover.
COVERED_TYPES = set(
    KEYBOARD_TYPES
    + TEXT_TYPES
    + KEYBOARD_DEVICE_TYPES
    + MOUSE_TYPES
    + MOUSE_DEVICE_TYPES
    + JOYSTICK_TYPES
    + GAMEPAD_TYPES
    + FINGER_TYPES
    + PINCH_TYPES
    + DROP_TYPES
    + WINDOW_TYPES
    + DISPLAY_TYPES
    + NO_ATTRIBUTE_TYPES
    + AUDIO_TYPES
    + CAMERA_TYPES
    + SENSOR_TYPES
    + PEN_TYPES
)


def test_every_standard_event_is_covered():
    """
    Every standard event type, apart from SDL's markers and reserved types, is covered by one of the conversion
    tests above, so a type added to the event names fails here until a test gives it its expected attributes.
    """

    standard = {t for t in pygame.event.get_standard_events() if pygame.event.event_name(t) not in SENTINEL_NAMES}

    missing = sorted(pygame.event.event_name(t) for t in standard - COVERED_TYPES)

    assert missing == []
