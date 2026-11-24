# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

cimport cython
from cpython.ref cimport Py_INCREF, Py_DECREF
from cpython.mem cimport PyMem_Malloc, PyMem_Free

from libc.string cimport memcpy, memset

from .sdl cimport *
from .display cimport Window, main_window
from .time cimport suspend_timers
from .error import error
import threading
import sys


# sphinx/source/pygame_events.rst documents every event type's names (including the aliases in locals.pyx),
# whether Ren'Py enables it by default (enabled_events in renpy/display/core.py), the attributes it carries, and how
# it differs from pygame-ce. Update that page with any change to event_names, the event constants, or the attributes
# the make_*_event functions below produce. test_pygame_event.py checks that the page names every event.

# The name of each event type, as given by event_name() and repr(). SDL's range markers (SDL_EVENT_DISPLAY_FIRST,
# SDL_EVENT_WINDOW_LAST, and so on) share values with real events, so they are left out, and the real event's name is
# the one reported.
event_names = {
    SDL_EVENT_FIRST: "NOEVENT",
    SDL_EVENT_QUIT: "QUIT",
    SDL_EVENT_TERMINATING: "TERMINATING",
    SDL_EVENT_LOW_MEMORY: "LOWMEMORY",
    SDL_EVENT_WILL_ENTER_BACKGROUND: "WILLENTERBACKGROUND",
    SDL_EVENT_DID_ENTER_BACKGROUND: "DIDENTERBACKGROUND",
    SDL_EVENT_WILL_ENTER_FOREGROUND: "WILLENTERFOREGROUND",
    SDL_EVENT_DID_ENTER_FOREGROUND: "DIDENTERFOREGROUND",
    SDL_EVENT_LOCALE_CHANGED: "LOCALECHANGED",
    SDL_EVENT_SYSTEM_THEME_CHANGED: "SYSTEMTHEMECHANGED",
    SDL_EVENT_DISPLAY_ORIENTATION: "DISPLAYORIENTATION",
    SDL_EVENT_DISPLAY_ADDED: "DISPLAYADDED",
    SDL_EVENT_DISPLAY_REMOVED: "DISPLAYREMOVED",
    SDL_EVENT_DISPLAY_MOVED: "DISPLAYMOVED",
    SDL_EVENT_DISPLAY_DESKTOP_MODE_CHANGED: "DISPLAYDESKTOPMODECHANGED",
    SDL_EVENT_DISPLAY_CURRENT_MODE_CHANGED: "DISPLAYCURRENTMODECHANGED",
    SDL_EVENT_DISPLAY_CONTENT_SCALE_CHANGED: "DISPLAYCONTENTSCALECHANGED",
    SDL_EVENT_DISPLAY_USABLE_BOUNDS_CHANGED: "DISPLAYUSABLEBOUNDSCHANGED",
    SDL_EVENT_WINDOW_SHOWN: "WINDOWSHOWN",
    SDL_EVENT_WINDOW_HIDDEN: "WINDOWHIDDEN",
    SDL_EVENT_WINDOW_EXPOSED: "WINDOWEXPOSED",
    SDL_EVENT_WINDOW_MOVED: "WINDOWMOVED",
    SDL_EVENT_WINDOW_RESIZED: "WINDOWRESIZED",
    SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED: "WINDOWPIXELSIZECHANGED",
    SDL_EVENT_WINDOW_METAL_VIEW_RESIZED: "WINDOWMETALVIEWRESIZED",
    SDL_EVENT_WINDOW_MINIMIZED: "WINDOWMINIMIZED",
    SDL_EVENT_WINDOW_MAXIMIZED: "WINDOWMAXIMIZED",
    SDL_EVENT_WINDOW_RESTORED: "WINDOWRESTORED",
    SDL_EVENT_WINDOW_MOUSE_ENTER: "WINDOWMOUSEENTER",
    SDL_EVENT_WINDOW_MOUSE_LEAVE: "WINDOWMOUSELEAVE",
    SDL_EVENT_WINDOW_FOCUS_GAINED: "WINDOWFOCUSGAINED",
    SDL_EVENT_WINDOW_FOCUS_LOST: "WINDOWFOCUSLOST",
    SDL_EVENT_WINDOW_CLOSE_REQUESTED: "WINDOWCLOSEREQUESTED",
    SDL_EVENT_WINDOW_HIT_TEST: "WINDOWHITTEST",
    SDL_EVENT_WINDOW_ICCPROF_CHANGED: "WINDOWICCPROFCHANGED",
    SDL_EVENT_WINDOW_DISPLAY_CHANGED: "WINDOWDISPLAYCHANGED",
    SDL_EVENT_WINDOW_DISPLAY_SCALE_CHANGED: "WINDOWDISPLAYSCALECHANGED",
    SDL_EVENT_WINDOW_SAFE_AREA_CHANGED: "WINDOWSAFEAREACHANGED",
    SDL_EVENT_WINDOW_OCCLUDED: "WINDOWOCCLUDED",
    SDL_EVENT_WINDOW_ENTER_FULLSCREEN: "WINDOWENTERFULLSCREEN",
    SDL_EVENT_WINDOW_LEAVE_FULLSCREEN: "WINDOWLEAVEFULLSCREEN",
    SDL_EVENT_WINDOW_DESTROYED: "WINDOWDESTROYED",
    SDL_EVENT_WINDOW_HDR_STATE_CHANGED: "WINDOWHDRSTATECHANGED",
    SDL_EVENT_KEY_DOWN: "KEYDOWN",
    SDL_EVENT_KEY_UP: "KEYUP",
    SDL_EVENT_TEXT_EDITING: "TEXTEDITING",
    SDL_EVENT_TEXT_INPUT: "TEXTINPUT",
    SDL_EVENT_KEYMAP_CHANGED: "KEYMAPCHANGED",
    SDL_EVENT_KEYBOARD_ADDED: "KEYBOARDADDED",
    SDL_EVENT_KEYBOARD_REMOVED: "KEYBOARDREMOVED",
    SDL_EVENT_TEXT_EDITING_CANDIDATES: "TEXTEDITINGCANDIDATES",
    SDL_EVENT_SCREEN_KEYBOARD_SHOWN: "SCREENKEYBOARDSHOWN",
    SDL_EVENT_SCREEN_KEYBOARD_HIDDEN: "SCREENKEYBOARDHIDDEN",
    SDL_EVENT_MOUSE_MOTION: "MOUSEMOTION",
    SDL_EVENT_MOUSE_BUTTON_DOWN: "MOUSEBUTTONDOWN",
    SDL_EVENT_MOUSE_BUTTON_UP: "MOUSEBUTTONUP",
    SDL_EVENT_MOUSE_WHEEL: "MOUSEWHEEL",
    SDL_EVENT_MOUSE_ADDED: "MOUSEADDED",
    SDL_EVENT_MOUSE_REMOVED: "MOUSEREMOVED",
    SDL_EVENT_JOYSTICK_AXIS_MOTION: "JOYSTICKAXISMOTION",
    SDL_EVENT_JOYSTICK_BALL_MOTION: "JOYSTICKBALLMOTION",
    SDL_EVENT_JOYSTICK_HAT_MOTION: "JOYSTICKHATMOTION",
    SDL_EVENT_JOYSTICK_BUTTON_DOWN: "JOYSTICKBUTTONDOWN",
    SDL_EVENT_JOYSTICK_BUTTON_UP: "JOYSTICKBUTTONUP",
    SDL_EVENT_JOYSTICK_ADDED: "JOYSTICKADDED",
    SDL_EVENT_JOYSTICK_REMOVED: "JOYSTICKREMOVED",
    SDL_EVENT_JOYSTICK_BATTERY_UPDATED: "JOYSTICKBATTERYUPDATED",
    SDL_EVENT_JOYSTICK_UPDATE_COMPLETE: "JOYSTICKUPDATECOMPLETE",
    SDL_EVENT_GAMEPAD_AXIS_MOTION: "GAMEPADAXISMOTION",
    SDL_EVENT_GAMEPAD_BUTTON_DOWN: "GAMEPADBUTTONDOWN",
    SDL_EVENT_GAMEPAD_BUTTON_UP: "GAMEPADBUTTONUP",
    SDL_EVENT_GAMEPAD_ADDED: "GAMEPADADDED",
    SDL_EVENT_GAMEPAD_REMOVED: "GAMEPADREMOVED",
    SDL_EVENT_GAMEPAD_REMAPPED: "GAMEPADREMAPPED",
    SDL_EVENT_GAMEPAD_TOUCHPAD_DOWN: "GAMEPADTOUCHPADDOWN",
    SDL_EVENT_GAMEPAD_TOUCHPAD_MOTION: "GAMEPADTOUCHPADMOTION",
    SDL_EVENT_GAMEPAD_TOUCHPAD_UP: "GAMEPADTOUCHPADUP",
    SDL_EVENT_GAMEPAD_SENSOR_UPDATE: "GAMEPADSENSORUPDATE",
    SDL_EVENT_GAMEPAD_UPDATE_COMPLETE: "GAMEPADUPDATECOMPLETE",
    SDL_EVENT_GAMEPAD_STEAM_HANDLE_UPDATED: "GAMEPADSTEAMHANDLEUPDATED",
    SDL_EVENT_FINGER_DOWN: "FINGERDOWN",
    SDL_EVENT_FINGER_UP: "FINGERUP",
    SDL_EVENT_FINGER_MOTION: "FINGERMOTION",
    SDL_EVENT_FINGER_CANCELED: "FINGERCANCELED",
    SDL_EVENT_PINCH_BEGIN: "PINCHBEGIN",
    SDL_EVENT_PINCH_UPDATE: "PINCHUPDATE",
    SDL_EVENT_PINCH_END: "PINCHEND",
    SDL_EVENT_CLIPBOARD_UPDATE: "CLIPBOARDUPDATE",
    SDL_EVENT_DROP_FILE: "DROPFILE",
    SDL_EVENT_DROP_TEXT: "DROPTEXT",
    SDL_EVENT_DROP_BEGIN: "DROPBEGIN",
    SDL_EVENT_DROP_COMPLETE: "DROPCOMPLETE",
    SDL_EVENT_DROP_POSITION: "DROPPOSITION",
    SDL_EVENT_AUDIO_DEVICE_ADDED: "AUDIODEVICEADDED",
    SDL_EVENT_AUDIO_DEVICE_REMOVED: "AUDIODEVICEREMOVED",
    SDL_EVENT_AUDIO_DEVICE_FORMAT_CHANGED: "AUDIODEVICEFORMATCHANGED",
    SDL_EVENT_SENSOR_UPDATE: "SENSORUPDATE",
    SDL_EVENT_PEN_PROXIMITY_IN: "PENPROXIMITYIN",
    SDL_EVENT_PEN_PROXIMITY_OUT: "PENPROXIMITYOUT",
    SDL_EVENT_PEN_DOWN: "PENDOWN",
    SDL_EVENT_PEN_UP: "PENUP",
    SDL_EVENT_PEN_BUTTON_DOWN: "PENBUTTONDOWN",
    SDL_EVENT_PEN_BUTTON_UP: "PENBUTTONUP",
    SDL_EVENT_PEN_MOTION: "PENMOTION",
    SDL_EVENT_PEN_AXIS: "PENAXIS",
    SDL_EVENT_CAMERA_DEVICE_ADDED: "CAMERADEVICEADDED",
    SDL_EVENT_CAMERA_DEVICE_REMOVED: "CAMERADEVICEREMOVED",
    SDL_EVENT_CAMERA_DEVICE_APPROVED: "CAMERADEVICEAPPROVED",
    SDL_EVENT_CAMERA_DEVICE_DENIED: "CAMERADEVICEDENIED",
    SDL_EVENT_RENDER_TARGETS_RESET: "RENDERTARGETSRESET",
    SDL_EVENT_RENDER_DEVICE_RESET: "RENDERDEVICERESET",
    SDL_EVENT_RENDER_DEVICE_LOST: "RENDERDEVICELOST",
    SDL_EVENT_PRIVATE0: "PRIVATE0",
    SDL_EVENT_PRIVATE1: "PRIVATE1",
    SDL_EVENT_PRIVATE2: "PRIVATE2",
    SDL_EVENT_PRIVATE3: "PRIVATE3",
    SDL_EVENT_POLL_SENTINEL: "POLLSENTINEL",
    SDL_EVENT_USER: "USER",
    SDL_EVENT_LAST: "LAST",
    SDL_EVENT_ENUM_PADDING: "ENUMPADDING",
}

# This is used for events posted to the event queue. This won't be returned
# to the user - it's just used internally, with the event object itself
# giving the type.
cdef unsigned int POSTEDEVENT
POSTEDEVENT = SDL_EVENT_LAST - 1

# The maximum number of a user-defined event.
USEREVENT_MAX = SDL_EVENT_LAST - 2

# If true, the mousewheel generates presses and releases of mouse buttons 4
# and 5 instead of MOUSEWHEEL events, and buttons 4 and higher are mapped to 6
# and higher.
cdef bint mousewheel_buttons = 1

cdef unsigned int SDL_TOUCH_MOUSEID
SDL_TOUCH_MOUSEID = <unsigned int> -1 # type: ignore

# EventType pickles itself, in a format that older versions, which had no C fields, can also load.
@cython.auto_pickle(False)
cdef class EventBase:
    """
    The base of EventType, holding the fields stored in C.
    """

    # The time SDL queued the event, in seconds since SDL was initialized, or 0.0 for an event that has not been
    # through the queue. Stored outside __dict__, so it does not take part in equality or appear in `dict`.
    cdef public double timestamp


class EventType(EventBase):
    """
    An event, as returned by the event queue or created by the program to be
    posted. The event's attributes are stored in its __dict__, along with its
    type as `_type`.
    """

    def __init__(self, type, dict=None, **kwargs):
        self._type = type

        if dict:
            self.__dict__.update(dict)

        self.__dict__.update(kwargs)

        if "timestamp" in self.__dict__:
            self.timestamp = self.__dict__.pop("timestamp")

    def __getstate__(self):
        return (dict(self.__dict__), self.timestamp)

    def __setstate__(self, state):
        if isinstance(state, tuple):
            attributes, self.timestamp = state
        else:
            # Older versions pickled only the attribute dictionary, with the timestamp in it in SDL's units, so the
            # timestamp is dropped.
            attributes = dict(state)
            attributes.pop("timestamp", None)

        self.__dict__.update(attributes)

    def __repr__(self):
        if SDL_EVENT_USER <= self.type <= USEREVENT_MAX:
            ename = "UserEvent%d" % (self.type - SDL_EVENT_USER)
        else:
            try:
                ename = event_names[self.type]
            except KeyError:
                ename = "UNKNOWN"

        rest = [ ]

        for k, v in sorted(self.__dict__.items()):
            if k == "_type":
                continue

            rest.append("%s=%r" % (k, v))

        return '<Event(%d-%s %s)>' % (self.type, ename, ", ".join(rest))

    @property
    def dict(self):
        return self.__dict__

    @property
    def type(self):
        return self._type

    def __eq__(self, other):
        if not isinstance(other, EventType):
            return NotImplemented

        return self.__dict__ == other.__dict__

    def __bool__(self):
        return self.type != 0

Event = EventType


cdef bint text_input_active():
    """
    Returns true if text input is active on the main window, in which case
    typed text arrives as TEXTINPUT events.
    """

    return main_window is not None and SDL_TextInputActive(main_window.window)


cdef object get_event_window(SDL_WindowID window_id):
    """
    Returns the value of the `window` attribute of an event that SDL associates
    with `window_id`: the main window if `window_id` is its id, or None
    otherwise, as for an event with no window or one from a window this module
    did not create.
    """

    if window_id == 0 or main_window is None or main_window.window == NULL:
        return None

    if SDL_GetWindowID(main_window.window) == window_id:
        return main_window

    return None


cpdef tuple convert_hat_value(int state):
    """
    Converts an SDL joystick hat bitmask into pygame's (x, y) tuple, where x is
    -1 for left and 1 for right, and y is 1 for up and -1 for down, and each is
    0 when the hat is centered on that axis.
    """

    cdef int hx = 0
    cdef int hy = 0

    if state & SDL_HAT_LEFT:
        hx = -1
    elif state & SDL_HAT_RIGHT:
        hx = 1

    if state & SDL_HAT_UP:
        hy = 1
    elif state & SDL_HAT_DOWN:
        hy = -1

    return (hx, hy)


cdef str get_joystick_guid(SDL_JoystickID instance_id):
    """
    Returns the GUID of the joystick with `instance_id` as a 32-character hex
    string, as pygame gives it. The string is all zeros if SDL no longer knows
    the joystick.
    """

    cdef char buf[33]

    SDL_GUIDToString(SDL_GetJoystickGUIDForID(instance_id), buf, sizeof(buf))
    return buf.decode("utf-8")


cdef make_keyboard_event(SDL_KeyboardEvent *e, bint text_input):
    """
    Converts an SDL keyboard event. `text_input` is true if text input is
    active, in which case typed text is delivered by separate TEXTINPUT events,
    and KEYDOWN only gives control characters a unicode value.
    """

    dargs = { 'scancode' : e.scancode,
              'key' : e.key,
              'mod' : e.mod,
              'unicode' : '',
              'repeat' : e.repeat,
              'window' : get_event_window(e.windowID),
               }

    if text_input:

        if e.type == SDL_EVENT_KEY_DOWN:
            # Control keys produce no TEXTINPUT event.
            if e.key < 0x20:
                dargs['unicode'] = chr(e.key)

    else:
        if e.type == SDL_EVENT_KEY_DOWN:
            # Without text input, there is no TEXTINPUT event, so take the
            # character from the keyboard layout, with shift, caps lock, and
            # AltGr applied. Keycodes of keys that do not produce a character
            # have bits above the Unicode range set.
            keycode = SDL_GetKeyFromScancode(e.scancode, e.mod, False)

            if 0x20 <= keycode <= 0x10FFFF and keycode != 0x7F:
                dargs['unicode'] = chr(keycode)

    return EventType(e.type, dict=dargs, repeat=e.repeat)


def _make_keyboard_event(type, scancode, key, mod, repeat=False, text_input=False):
    """
    Converts the fields of an SDL keyboard event into an event object, as
    the event queue does when text input is active if `text_input` is true,
    or inactive otherwise. This exists so tests can exercise the conversion
    without a keyboard or window.
    """

    cdef SDL_KeyboardEvent e

    memset(&e, 0, sizeof(e))
    e.type = type
    e.scancode = scancode
    e.key = key
    e.mod = mod
    e.down = (type == SDL_EVENT_KEY_DOWN)
    e.repeat = repeat

    return make_keyboard_event(&e, text_input)


def _make_finger_event(type, touch_id, finger_id, x, y, dx=0.0, dy=0.0, pressure=0.0):
    """
    Converts the fields of an SDL touch finger event into an event object,
    as the event queue does. This exists so tests can exercise the
    conversion without a touchscreen.
    """

    cdef SDL_Event e

    memset(&e, 0, sizeof(e))
    e.type = type
    e.tfinger.touchID = touch_id
    e.tfinger.fingerID = finger_id
    e.tfinger.x = x
    e.tfinger.y = y
    e.tfinger.dx = dx
    e.tfinger.dy = dy
    e.tfinger.pressure = pressure

    return make_event(&e)


cdef const char *get_cstring(object value):
    """
    Returns a pointer to the contents of bytes object `value`, or NULL if
    `value` is None. The caller must keep `value` alive while it uses the
    pointer.
    """

    if value is None:
        return NULL

    return <const char *> value


def _make_event(type, **fields):
    """
    Converts an SDL event of `type` into the list of event objects the event
    queue would produce for it. This exists so tests can exercise the
    conversion of every event type without the devices that produce them.

    The keyword arguments give the fields of the SDL structure for `type`,
    using SDL's field names, and fields not given are zero. String fields take
    bytes or None, `candidates` takes a list of bytes or None entries, and the
    sensor `data` fields take a sequence of floats.
    """

    cdef SDL_Event e
    cdef const char **candidates = NULL
    cdef int i

    # Keeps the bytes objects whose buffers the event points to alive.
    keep = [ ]

    def get(name):
        return fields.get(name, 0)

    def get_string(name):
        value = fields.get(name, None)

        if value is not None:
            keep.append(bytes(value))
            return keep[-1]

        return None

    def get_data(limit):
        data = tuple(fields.get("data", ()))

        if len(data) > limit:
            raise ValueError("The data field takes at most %d values." % limit)

        return data

    # The text events are converted by decoding their text, which can't be NULL.
    if type in (SDL_EVENT_TEXT_INPUT, SDL_EVENT_TEXT_EDITING) and fields.get("text", None) is None:
        fields["text"] = b""

    # A posted event carries a reference to an event object, which this can't supply.
    if type == POSTEDEVENT:
        raise ValueError("Posted events can't be made from fields.")

    memset(&e, 0, sizeof(e))
    e.type = type

    try:
        if type in (SDL_EVENT_KEY_DOWN, SDL_EVENT_KEY_UP):
            e.key.windowID = get("windowID")
            e.key.which = get("which")
            e.key.scancode = get("scancode")
            e.key.key = get("key")
            e.key.mod = get("mod")
            e.key.down = get("down")
            e.key.repeat = get("repeat")

        elif type in (SDL_EVENT_KEYBOARD_ADDED, SDL_EVENT_KEYBOARD_REMOVED):
            e.kdevice.which = get("which")

        elif type == SDL_EVENT_MOUSE_MOTION:
            e.motion.windowID = get("windowID")
            e.motion.which = get("which")
            e.motion.state = get("state")
            e.motion.x = get("x")
            e.motion.y = get("y")
            e.motion.xrel = get("xrel")
            e.motion.yrel = get("yrel")

        elif type in (SDL_EVENT_MOUSE_BUTTON_DOWN, SDL_EVENT_MOUSE_BUTTON_UP):
            e.button.windowID = get("windowID")
            e.button.which = get("which")
            e.button.button = get("button")
            e.button.down = get("down")
            e.button.clicks = get("clicks")
            e.button.x = get("x")
            e.button.y = get("y")

        elif type == SDL_EVENT_MOUSE_WHEEL:
            e.wheel.windowID = get("windowID")
            e.wheel.which = get("which")
            e.wheel.x = get("x")
            e.wheel.y = get("y")
            e.wheel.direction = get("direction")
            e.wheel.mouse_x = get("mouse_x")
            e.wheel.mouse_y = get("mouse_y")
            e.wheel.integer_x = get("integer_x")
            e.wheel.integer_y = get("integer_y")

        elif type in (SDL_EVENT_MOUSE_ADDED, SDL_EVENT_MOUSE_REMOVED):
            e.mdevice.which = get("which")

        elif type == SDL_EVENT_JOYSTICK_AXIS_MOTION:
            e.jaxis.which = get("which")
            e.jaxis.axis = get("axis")
            e.jaxis.value = get("value")

        elif type == SDL_EVENT_JOYSTICK_BALL_MOTION:
            e.jball.which = get("which")
            e.jball.ball = get("ball")
            e.jball.xrel = get("xrel")
            e.jball.yrel = get("yrel")

        elif type == SDL_EVENT_JOYSTICK_HAT_MOTION:
            e.jhat.which = get("which")
            e.jhat.hat = get("hat")
            e.jhat.value = get("value")

        elif type in (SDL_EVENT_JOYSTICK_BUTTON_DOWN, SDL_EVENT_JOYSTICK_BUTTON_UP):
            e.jbutton.which = get("which")
            e.jbutton.button = get("button")
            e.jbutton.down = get("down")

        elif type in (SDL_EVENT_JOYSTICK_ADDED, SDL_EVENT_JOYSTICK_REMOVED, SDL_EVENT_JOYSTICK_UPDATE_COMPLETE):
            e.jdevice.which = get("which")

        elif type == SDL_EVENT_JOYSTICK_BATTERY_UPDATED:
            e.jbattery.which = get("which")
            e.jbattery.state = get("state")
            e.jbattery.percent = get("percent")

        elif type == SDL_EVENT_GAMEPAD_AXIS_MOTION:
            e.gaxis.which = get("which")
            e.gaxis.axis = get("axis")
            e.gaxis.value = get("value")

        elif type in (SDL_EVENT_GAMEPAD_BUTTON_DOWN, SDL_EVENT_GAMEPAD_BUTTON_UP):
            e.gbutton.which = get("which")
            e.gbutton.button = get("button")
            e.gbutton.down = get("down")

        elif type in (
                SDL_EVENT_GAMEPAD_ADDED, SDL_EVENT_GAMEPAD_REMOVED, SDL_EVENT_GAMEPAD_REMAPPED,
                SDL_EVENT_GAMEPAD_UPDATE_COMPLETE, SDL_EVENT_GAMEPAD_STEAM_HANDLE_UPDATED):
            e.gdevice.which = get("which")

        elif type in (SDL_EVENT_GAMEPAD_TOUCHPAD_DOWN, SDL_EVENT_GAMEPAD_TOUCHPAD_MOTION, SDL_EVENT_GAMEPAD_TOUCHPAD_UP):
            e.gtouchpad.which = get("which")
            e.gtouchpad.touchpad = get("touchpad")
            e.gtouchpad.finger = get("finger")
            e.gtouchpad.x = get("x")
            e.gtouchpad.y = get("y")
            e.gtouchpad.pressure = get("pressure")

        elif type == SDL_EVENT_GAMEPAD_SENSOR_UPDATE:
            e.gsensor.which = get("which")
            e.gsensor.sensor = get("sensor")

            for i, value in enumerate(get_data(3)):
                e.gsensor.data[i] = value

        elif type == SDL_EVENT_SENSOR_UPDATE:
            e.sensor.which = get("which")

            for i, value in enumerate(get_data(6)):
                e.sensor.data[i] = value

        elif SDL_EVENT_WINDOW_FIRST <= type <= SDL_EVENT_WINDOW_LAST:
            e.window.windowID = get("windowID")
            e.window.data1 = get("data1")
            e.window.data2 = get("data2")

        elif SDL_EVENT_DISPLAY_FIRST <= type <= SDL_EVENT_DISPLAY_LAST:
            e.display.displayID = get("displayID")
            e.display.data1 = get("data1")
            e.display.data2 = get("data2")

        elif type == SDL_EVENT_TEXT_INPUT:
            e.text.windowID = get("windowID")
            e.text.text = get_cstring(get_string("text"))

        elif type == SDL_EVENT_TEXT_EDITING:
            e.edit.windowID = get("windowID")
            e.edit.text = get_cstring(get_string("text"))
            e.edit.start = get("start")
            e.edit.length = get("length")

        elif type == SDL_EVENT_TEXT_EDITING_CANDIDATES:
            e.edit_candidates.windowID = get("windowID")
            e.edit_candidates.selected_candidate = get("selected_candidate")
            e.edit_candidates.horizontal = get("horizontal")

            if fields.get("candidates", None) is not None:
                entries = fields["candidates"]
                keep.extend(entries)

                candidates = <const char **> PyMem_Malloc(sizeof(char *) * max(len(entries), 1))
                if candidates == NULL:
                    raise MemoryError()

                for i, value in enumerate(entries):
                    candidates[i] = get_cstring(value)

                e.edit_candidates.candidates = candidates
                e.edit_candidates.num_candidates = len(entries)

        elif type in (SDL_EVENT_FINGER_DOWN, SDL_EVENT_FINGER_UP, SDL_EVENT_FINGER_MOTION, SDL_EVENT_FINGER_CANCELED):
            e.tfinger.touchID = get("touchID")
            e.tfinger.fingerID = get("fingerID")
            e.tfinger.x = get("x")
            e.tfinger.y = get("y")
            e.tfinger.dx = get("dx")
            e.tfinger.dy = get("dy")
            e.tfinger.pressure = get("pressure")
            e.tfinger.windowID = get("windowID")

        elif type in (SDL_EVENT_PINCH_BEGIN, SDL_EVENT_PINCH_UPDATE, SDL_EVENT_PINCH_END):
            e.pinch.scale = get("scale")
            e.pinch.windowID = get("windowID")

        elif type in (
                SDL_EVENT_DROP_FILE, SDL_EVENT_DROP_TEXT, SDL_EVENT_DROP_BEGIN, SDL_EVENT_DROP_COMPLETE,
                SDL_EVENT_DROP_POSITION):
            e.drop.windowID = get("windowID")
            e.drop.x = get("x")
            e.drop.y = get("y")
            e.drop.source = get_cstring(get_string("source"))
            e.drop.data = get_cstring(get_string("data"))

        elif type in (SDL_EVENT_AUDIO_DEVICE_ADDED, SDL_EVENT_AUDIO_DEVICE_REMOVED, SDL_EVENT_AUDIO_DEVICE_FORMAT_CHANGED):
            e.adevice.which = get("which")
            e.adevice.recording = get("recording")

        elif type in (
                SDL_EVENT_CAMERA_DEVICE_ADDED, SDL_EVENT_CAMERA_DEVICE_REMOVED,
                SDL_EVENT_CAMERA_DEVICE_APPROVED, SDL_EVENT_CAMERA_DEVICE_DENIED):
            e.cdevice.which = get("which")

        elif type in (SDL_EVENT_PEN_PROXIMITY_IN, SDL_EVENT_PEN_PROXIMITY_OUT):
            e.pproximity.windowID = get("windowID")
            e.pproximity.which = get("which")

        elif type == SDL_EVENT_PEN_MOTION:
            e.pmotion.windowID = get("windowID")
            e.pmotion.which = get("which")
            e.pmotion.pen_state = get("pen_state")
            e.pmotion.x = get("x")
            e.pmotion.y = get("y")

        elif type in (SDL_EVENT_PEN_DOWN, SDL_EVENT_PEN_UP):
            e.ptouch.windowID = get("windowID")
            e.ptouch.which = get("which")
            e.ptouch.pen_state = get("pen_state")
            e.ptouch.x = get("x")
            e.ptouch.y = get("y")
            e.ptouch.eraser = get("eraser")
            e.ptouch.down = get("down")

        elif type in (SDL_EVENT_PEN_BUTTON_DOWN, SDL_EVENT_PEN_BUTTON_UP):
            e.pbutton.windowID = get("windowID")
            e.pbutton.which = get("which")
            e.pbutton.pen_state = get("pen_state")
            e.pbutton.x = get("x")
            e.pbutton.y = get("y")
            e.pbutton.button = get("button")
            e.pbutton.down = get("down")

        elif type == SDL_EVENT_PEN_AXIS:
            e.paxis.windowID = get("windowID")
            e.paxis.which = get("which")
            e.paxis.pen_state = get("pen_state")
            e.paxis.x = get("x")
            e.paxis.y = get("y")
            e.paxis.axis = get("axis")
            e.paxis.value = get("value")

        elif type in (SDL_EVENT_RENDER_TARGETS_RESET, SDL_EVENT_RENDER_DEVICE_RESET, SDL_EVENT_RENDER_DEVICE_LOST):
            e.render.windowID = get("windowID")

        elif type >= SDL_EVENT_USER and type != POSTEDEVENT:
            e.user.windowID = get("windowID")
            e.user.code = get("code")

        return make_events(&e)

    finally:
        PyMem_Free(candidates)


def _get_main_window_id():
    """
    Returns SDL's id for the main window, or 0 if there is none. This exists
    so tests can give an event the main window's id.
    """

    if main_window is None or main_window.window == NULL:
        return 0

    return SDL_GetWindowID(main_window.window)


def _push_mousewheel_event(x, y, integer_y, mouse_x, mouse_y, which=0, timestamp=0):
    """
    Pushes an SDL mouse wheel event onto SDL's queue, as a mouse would. This
    exists so tests can exercise the queue without a mouse. A `timestamp` of 0
    makes SDL use the current time.
    """

    cdef SDL_Event e

    memset(&e, 0, sizeof(e))
    e.type = SDL_EVENT_MOUSE_WHEEL
    e.common.timestamp = timestamp
    e.wheel.which = which
    e.wheel.x = x
    e.wheel.y = y
    e.wheel.integer_x = int(x)
    e.wheel.integer_y = integer_y
    e.wheel.mouse_x = mouse_x
    e.wheel.mouse_y = mouse_y

    if not SDL_PushEvent(&e):
        raise error()


def _push_mousemotion_event(x, y, xrel, yrel, state=0, which=0, timestamp=0):
    """
    Pushes an SDL mouse motion event onto SDL's queue, as a mouse would. This
    exists so tests can exercise the queue without a mouse. A `timestamp` of 0
    makes SDL use the current time.
    """

    cdef SDL_Event e

    memset(&e, 0, sizeof(e))
    e.type = SDL_EVENT_MOUSE_MOTION
    e.common.timestamp = timestamp
    e.motion.which = which
    e.motion.state = state
    e.motion.x = x
    e.motion.y = y
    e.motion.xrel = xrel
    e.motion.yrel = yrel

    if not SDL_PushEvent(&e):
        raise error()


def _push_user_event(type, code=0, timestamp=0):
    """
    Pushes an SDL user event of `type` onto SDL's queue. This exists so tests
    can put a non-motion event with a known timestamp on the queue. A
    `timestamp` of 0 makes SDL use the current time.
    """

    cdef SDL_Event e

    memset(&e, 0, sizeof(e))
    e.type = type
    e.common.timestamp = timestamp
    e.user.code = code

    if not SDL_PushEvent(&e):
        raise error()

cdef cbool reject_posted_events_filter(void *userdata, SDL_Event *event) noexcept nogil:
    return event.type != POSTEDEVENT


def _reject_posted_events(flag):
    """
    If `flag` is true, installs an SDL event filter that rejects the events
    post() pushes, so SDL_PushEvent fails. If false, removes the filter. This
    exists so tests can exercise a failed post(). Changing the filter discards
    the events pending in SDL's queue.
    """

    if flag:
        SDL_SetEventFilter(reject_posted_events_filter, NULL)
    else:
        SDL_SetEventFilter(NULL, NULL)

cdef make_mousemotion_event(SDL_MouseMotionEvent *e):
    buttons = (1 if e.state & SDL_BUTTON_LMASK else 0,
               1 if e.state & SDL_BUTTON_MMASK else 0,
               1 if e.state & SDL_BUTTON_RMASK else 0)
    return EventType(
        e.type,
        pos=(e.x, e.y),
        rel=(e.xrel, e.yrel),
        which=e.which,
        buttons=buttons,
        touch=(SDL_TOUCH_MOUSEID == e.which),
        window=get_event_window(e.windowID))

cdef make_mousebtn_event(SDL_MouseButtonEvent *e):
    btn = e.button

    # SDL 1.x maps wheel to buttons 4/5
    if mousewheel_buttons and btn >= 4:
        btn += 2

    return EventType(
        e.type,
        button=btn,
        pos=(e.x, e.y),
        which=e.which,
        touch=(SDL_TOUCH_MOUSEID == e.which),
        clicks=e.clicks,
        window=get_event_window(e.windowID))

cdef make_mousewheel_event(SDL_MouseWheelEvent *e):
    """
    Converts an SDL mouse wheel event into a MOUSEWHEEL event.
    """

    return EventType(
        e.type,
        which=e.which,
        x=e.x,
        y=e.y,
        touch=(SDL_TOUCH_MOUSEID == e.which),
        flipped=(e.direction == SDL_MOUSEWHEEL_FLIPPED),
        precise_x=e.x,
        precise_y=e.y,
        pos=(e.mouse_x, e.mouse_y),
        window=get_event_window(e.windowID))

cdef list make_mousewheel_events(SDL_MouseWheelEvent *e):
    """
    Converts an SDL mouse wheel event into a list of events.

    If mousewheel_buttons is false, this is a single MOUSEWHEEL event.

    Otherwise, as in SDL 1, no MOUSEWHEEL event is generated. If SDL has
    accumulated at least one whole step of vertical scrolling, the result is a
    single press and release of button 4 (up) or 5 (down), however many steps
    the event carries, so a fast flick doesn't scroll in a jump. Otherwise, the
    result is empty.
    """

    if not mousewheel_buttons:
        return [ make_mousewheel_event(e) ]

    if e.integer_y == 0:
        return [ ]

    if e.integer_y > 0:
        btn = 4
    else:
        btn = 5

    touch = (SDL_TOUCH_MOUSEID == e.which)
    pos = (e.mouse_x, e.mouse_y)
    window = get_event_window(e.windowID)

    return [
        EventType(SDL_EVENT_MOUSE_BUTTON_DOWN, which=e.which, button=btn, pos=pos, touch=touch, clicks=1, window=window),
        EventType(SDL_EVENT_MOUSE_BUTTON_UP, which=e.which, button=btn, pos=pos, touch=touch, clicks=1, window=window),
    ]

cdef make_joyaxis_event(SDL_JoyAxisEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, axis=e.axis, value=e.value/32768.0)

cdef make_joyball_event(SDL_JoyBallEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, ball=e.ball, rel=(e.xrel, e.yrel))

cdef make_joyhat_event(SDL_JoyHatEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, hat=e.hat, value=convert_hat_value(e.value))

cdef make_joybtn_event(SDL_JoyButtonEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, button=e.button)

cdef make_joydevice_event(SDL_JoyDeviceEvent *e):
    """
    Converts an SDL joystick added or removed event. The device index of an
    added joystick is its instance id, which is what Joystick() takes.
    """

    if e.type == SDL_EVENT_JOYSTICK_ADDED:
        return EventType(
            e.type,
            which=e.which,
            device_index=e.which,
            instance_id=e.which,
            guid=get_joystick_guid(e.which))

    return EventType(e.type, which=e.which, instance_id=e.which)

cdef make_joybattery_event(SDL_JoyBatteryEvent *e):
    return EventType(e.type, which=e.which, instance_id=e.which, state=e.state, percent=e.percent)

cdef make_gamepaddevice_event(SDL_GamepadDeviceEvent *e):
    """
    Converts an SDL gamepad added, removed, or remapped event. The device index
    of an added gamepad is its instance id, which is what Controller() takes.
    """

    if e.type == SDL_EVENT_GAMEPAD_ADDED:
        return EventType(
            e.type,
            which=e.which,
            device_index=e.which,
            instance_id=e.which,
            guid=get_joystick_guid(e.which))

    return EventType(e.type, which=e.which, instance_id=e.which)

cdef make_gamepadtouchpad_event(SDL_GamepadTouchpadEvent *e):
    return EventType(
        e.type,
        which=e.which,
        instance_id=e.which,
        touch_id=e.touchpad,
        finger_id=e.finger,
        x=e.x,
        y=e.y,
        pressure=e.pressure)

cdef make_gamepadsensor_event(SDL_GamepadSensorEvent *e):
    return EventType(
        e.type,
        which=e.which,
        instance_id=e.which,
        sensor=e.sensor,
        data=(e.data[0], e.data[1], e.data[2]))

cdef make_sensor_event(SDL_SensorEvent *e):
    return EventType(
        e.type,
        which=e.which,
        instance_id=e.which,
        data=tuple(e.data[i] for i in range(6)))

cdef make_textinput_event(SDL_TextInputEvent *e):
    window = get_event_window(e.windowID)

    try:
        return EventType(e.type, text=e.text.decode("utf-8"), window=window)
    except UnicodeDecodeError:
        return EventType(e.type, text='', window=window)

cdef make_textediting_event(SDL_TextEditingEvent *e):
    window = get_event_window(e.windowID)

    try:
        return EventType(e.type, text=e.text.decode("utf-8"), start=e.start, length=e.length, window=window)
    except UnicodeDecodeError:
        return EventType(e.type, text='', start=e.start, length=e.length, window=window)

cdef make_textediting_candidates_event(SDL_TextEditingCandidatesEvent *e):
    candidates = [ ]

    if e.candidates:
        for i in range(e.num_candidates):
            if e.candidates[i]:
                candidates.append(e.candidates[i].decode("utf-8", "replace"))
            else:
                candidates.append('')

    return EventType(
        e.type,
        candidates=candidates,
        selected=e.selected_candidate,
        horizontal=bool(e.horizontal),
        window_id=e.windowID,
        window=get_event_window(e.windowID))

cdef make_drop_event(SDL_DropEvent *e):
    if e.data:
        file = e.data.decode("utf-8")
    else:
        file = None

    rv = EventType(e.type, file=file, window_id=e.windowID, window=get_event_window(e.windowID), x=e.x, y=e.y)

    if e.type == SDL_EVENT_DROP_TEXT:
        rv.text = file

    return rv

cdef make_window_event(SDL_WindowEvent *e):
    rv = EventType(e.type, data1=e.data1, data2=e.data2, window=get_event_window(e.windowID))

    if e.type in (SDL_EVENT_WINDOW_MOVED, SDL_EVENT_WINDOW_RESIZED, SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED):
        rv.x = e.data1
        rv.y = e.data2
    elif e.type == SDL_EVENT_WINDOW_DISPLAY_CHANGED:
        rv.display_index = e.data1

    return rv

cdef make_display_event(SDL_DisplayEvent *e):
    return EventType(e.type, display_index=e.displayID, data1=e.data1, data2=e.data2)

cdef make_pen_event(SDL_Event *e):
    """
    Converts an SDL pen event. Every pen event has `which` and `window`. All but
    the proximity events also give the pen's state and position, and the touch,
    button, and axis events add the fields of their SDL structure.
    """

    if e.type in (SDL_EVENT_PEN_PROXIMITY_IN, SDL_EVENT_PEN_PROXIMITY_OUT):
        return EventType(e.type, which=e.pproximity.which, window=get_event_window(e.pproximity.windowID))

    # The motion event's fields begin every other pen structure.
    rv = EventType(
        e.type,
        which=e.pmotion.which,
        window=get_event_window(e.pmotion.windowID),
        pen_state=e.pmotion.pen_state,
        x=e.pmotion.x,
        y=e.pmotion.y)

    if e.type in (SDL_EVENT_PEN_DOWN, SDL_EVENT_PEN_UP):
        rv.eraser = e.ptouch.eraser
        rv.down = e.ptouch.down
    elif e.type in (SDL_EVENT_PEN_BUTTON_DOWN, SDL_EVENT_PEN_BUTTON_UP):
        rv.button = e.pbutton.button
        rv.down = e.pbutton.down
    elif e.type == SDL_EVENT_PEN_AXIS:
        rv.axis = e.paxis.axis
        rv.value = e.paxis.value

    return rv

cdef make_event(SDL_Event *e):
    cdef object o

    if e.type == SDL_EVENT_MOUSE_MOTION:
        return make_mousemotion_event(<SDL_MouseMotionEvent*>e)
    elif e.type in (SDL_EVENT_MOUSE_BUTTON_DOWN, SDL_EVENT_MOUSE_BUTTON_UP):
        return make_mousebtn_event(<SDL_MouseButtonEvent*>e)

    elif e.type == SDL_EVENT_MOUSE_WHEEL:
        return make_mousewheel_event(<SDL_MouseWheelEvent*>e)
    elif e.type in (SDL_EVENT_KEY_DOWN, SDL_EVENT_KEY_UP):
        return make_keyboard_event(<SDL_KeyboardEvent*>e, text_input_active())
    elif e.type == SDL_EVENT_JOYSTICK_AXIS_MOTION:
        return make_joyaxis_event(<SDL_JoyAxisEvent*>e)
    elif e.type == SDL_EVENT_JOYSTICK_BALL_MOTION:
        return make_joyball_event(<SDL_JoyBallEvent*>e)
    elif e.type == SDL_EVENT_JOYSTICK_HAT_MOTION:
        return make_joyhat_event(<SDL_JoyHatEvent*>e)
    elif e.type in (SDL_EVENT_JOYSTICK_BUTTON_DOWN, SDL_EVENT_JOYSTICK_BUTTON_UP):
        return make_joybtn_event(<SDL_JoyButtonEvent*>e)
    elif e.type in (SDL_EVENT_JOYSTICK_ADDED, SDL_EVENT_JOYSTICK_REMOVED):
        return make_joydevice_event(<SDL_JoyDeviceEvent*>e)
    elif e.type == SDL_EVENT_JOYSTICK_BATTERY_UPDATED:
        return make_joybattery_event(<SDL_JoyBatteryEvent*>e)
    elif SDL_EVENT_WINDOW_FIRST <= e.type <= SDL_EVENT_WINDOW_LAST:
        return make_window_event(<SDL_WindowEvent*>e)
    elif SDL_EVENT_DISPLAY_FIRST <= e.type <= SDL_EVENT_DISPLAY_LAST:
        return make_display_event(<SDL_DisplayEvent*>e)
    elif e.type == SDL_EVENT_TEXT_INPUT:
        return make_textinput_event(<SDL_TextInputEvent *> e)
    elif e.type == SDL_EVENT_TEXT_EDITING:
        return make_textediting_event(<SDL_TextEditingEvent *> e)
    elif e.type == SDL_EVENT_TEXT_EDITING_CANDIDATES:
        return make_textediting_candidates_event(<SDL_TextEditingCandidatesEvent *> e)
    elif e.type == SDL_EVENT_GAMEPAD_AXIS_MOTION:
        return EventType(e.type, which=e.gaxis.which, instance_id=e.gaxis.which, axis=e.gaxis.axis, value=e.gaxis.value)
    elif e.type in (SDL_EVENT_GAMEPAD_BUTTON_DOWN, SDL_EVENT_GAMEPAD_BUTTON_UP):
        return EventType(
            e.type, which=e.gbutton.which, instance_id=e.gbutton.which, button=e.gbutton.button, state=e.gbutton.down)
    elif e.type in (SDL_EVENT_GAMEPAD_ADDED, SDL_EVENT_GAMEPAD_REMOVED, SDL_EVENT_GAMEPAD_REMAPPED):
        return make_gamepaddevice_event(<SDL_GamepadDeviceEvent*>e)
    elif e.type in (SDL_EVENT_GAMEPAD_TOUCHPAD_DOWN, SDL_EVENT_GAMEPAD_TOUCHPAD_MOTION, SDL_EVENT_GAMEPAD_TOUCHPAD_UP):
        return make_gamepadtouchpad_event(<SDL_GamepadTouchpadEvent*>e)
    elif e.type == SDL_EVENT_GAMEPAD_SENSOR_UPDATE:
        return make_gamepadsensor_event(<SDL_GamepadSensorEvent*>e)
    elif e.type == SDL_EVENT_SENSOR_UPDATE:
        return make_sensor_event(<SDL_SensorEvent*>e)
    elif e.type in (SDL_EVENT_FINGER_MOTION, SDL_EVENT_FINGER_DOWN, SDL_EVENT_FINGER_UP, SDL_EVENT_FINGER_CANCELED):
        return EventType(e.type, touchId=e.tfinger.touchID, fingerId=e.tfinger.fingerID, touch_id=e.tfinger.touchID, finger_id=e.tfinger.fingerID, x=e.tfinger.x, y=e.tfinger.y, dx=e.tfinger.dx, dy=e.tfinger.dy, pressure=e.tfinger.pressure, window=get_event_window(e.tfinger.windowID))
    elif e.type in (SDL_EVENT_PINCH_BEGIN, SDL_EVENT_PINCH_UPDATE, SDL_EVENT_PINCH_END):
        return EventType(e.type, scale=e.pinch.scale, window=get_event_window(e.pinch.windowID))
    elif e.type in (
            SDL_EVENT_DROP_FILE, SDL_EVENT_DROP_TEXT, SDL_EVENT_DROP_BEGIN, SDL_EVENT_DROP_COMPLETE, SDL_EVENT_DROP_POSITION):
        return make_drop_event(<SDL_DropEvent*> e)
    elif e.type in (SDL_EVENT_AUDIO_DEVICE_ADDED, SDL_EVENT_AUDIO_DEVICE_REMOVED, SDL_EVENT_AUDIO_DEVICE_FORMAT_CHANGED):
        return EventType(e.type, which=e.adevice.which, iscapture=e.adevice.recording)
    elif e.type in (SDL_EVENT_KEYBOARD_ADDED, SDL_EVENT_KEYBOARD_REMOVED):
        return EventType(e.type, which=e.kdevice.which)
    elif e.type in (SDL_EVENT_MOUSE_ADDED, SDL_EVENT_MOUSE_REMOVED):
        return EventType(e.type, which=e.mdevice.which)
    elif e.type in (
            SDL_EVENT_CAMERA_DEVICE_ADDED, SDL_EVENT_CAMERA_DEVICE_REMOVED,
            SDL_EVENT_CAMERA_DEVICE_APPROVED, SDL_EVENT_CAMERA_DEVICE_DENIED):
        return EventType(e.type, which=e.cdevice.which)
    elif SDL_EVENT_PEN_PROXIMITY_IN <= e.type <= SDL_EVENT_PEN_AXIS:
        return make_pen_event(e)
    elif e.type == POSTEDEVENT:
        o = <object> e.user.data1
        Py_DECREF(o)
        return o
    elif e.type >= SDL_EVENT_USER:
        # Can't do anything useful with data1 and data2 here.
        return EventType(e.type, code=e.user.code)

    return EventType(e.type)


cdef list make_events(SDL_Event *e):
    """
    Converts an SDL event into the list of events it produces, which can be
    empty.
    """

    if e.type == SDL_EVENT_MOUSE_WHEEL:
        return make_mousewheel_events(<SDL_MouseWheelEvent*>e)

    return [ make_event(e) ]


cdef void stamp_event(EventBase e, Uint64 timestamp):
    """
    Sets the timestamp of `e` from an SDL timestamp in nanoseconds.
    """

    e.timestamp = <double> timestamp / 1e9


# The event queue - a list of pending events from oldest to newest.
cdef public event_queue = list()

# The lock that protects the event queue.
lock = threading.RLock()

# This is the object that is returned when no event exists.
NOEVENT_EVENT = EventType(0)


cdef bint has_event(kinds):
    """
    Returns true if at least one event in the queue has a type in `kinds`,
    which must support the in operator.

    The lock must be held when calling this function
    """

    for i in event_queue:
        if i._type in kinds:
            return True


cdef object get_events(kinds):
    """
    Returns a list containing all events in the event queue with type `kinds`.
    Removes those events from the event queue.

    The lock must be held when calling this function.
    """

    if isinstance(kinds, int):
        kinds = [ kinds ]

    global event_queue

    cdef list rv = [ ]
    cdef list new_queue = [ ]

    for i in event_queue:
        if i._type in kinds:
            rv.append(i)
        else:
            new_queue.append(i)

    event_queue = new_queue

    return rv


cdef int poll_sdl() except 1:
    """
    Polls SDL for pending events, and places those events onto the event q
    queue.
    """

    # This also merges MOUSEMOTION events.

    cdef bint last_mousemotion = False

    cdef SDL_Event evt
    cdef SDL_Event old_evt

    cdef SDL_MouseMotionEvent *mm_evt = <SDL_MouseMotionEvent *> &evt
    cdef SDL_MouseMotionEvent *old_mm_evt = <SDL_MouseMotionEvent *> &old_evt

    with lock:
        while SDL_PollEvent(&evt):
            if evt.type == SDL_EVENT_MOUSE_MOTION:

                # We can merge the event.
                if last_mousemotion and mm_evt.state == old_mm_evt.state and mm_evt.which == old_mm_evt.which:
                    old_mm_evt.timestamp = mm_evt.timestamp
                    old_mm_evt.x = mm_evt.x
                    old_mm_evt.y = mm_evt.y
                    old_mm_evt.xrel += mm_evt.xrel
                    old_mm_evt.yrel += mm_evt.yrel
                    continue

                # We can't merge the event.
                if last_mousemotion:
                    e = make_mousemotion_event(old_mm_evt)
                    stamp_event(e, old_evt.common.timestamp)
                    event_queue.append(e)

                memcpy(&old_evt, &evt, sizeof(SDL_Event))
                last_mousemotion = True

            else:
                if last_mousemotion:
                    e = make_mousemotion_event(old_mm_evt)
                    stamp_event(e, old_evt.common.timestamp)
                    event_queue.append(e)
                    last_mousemotion = False

                for e in make_events(&evt):
                    stamp_event(e, evt.common.timestamp)
                    event_queue.append(e)

        if last_mousemotion:
            e = make_mousemotion_event(old_mm_evt)
            stamp_event(e, old_evt.common.timestamp)
            event_queue.append(e)
            last_mousemotion = False

    return 0


def pump():
    with lock:
        poll_sdl()


def get(t=None):

    global event_queue

    with lock:
        poll_sdl()

        if t is None:
            rv = event_queue
            event_queue = [ ]

        elif isinstance(t, int):
            rv = get_events(( t, ))

        else:
            rv = get_events(t)

    return rv


def poll():

    with lock:
        poll_sdl()

        if event_queue:
            return event_queue.pop(0)

        return NOEVENT_EVENT


def wait():

    cdef bint result

    while True:
        with lock:
            poll_sdl()

            if event_queue:
                return event_queue.pop(0)

        # Wait for an event without removing it, so the next poll_sdl converts,
        # merges, and timestamps it like any other event.
        with nogil:
            result = SDL_WaitEvent(NULL)

        if not result:
            return NOEVENT_EVENT


def peek(t=None):

    with lock:
        poll_sdl()

        if t is None:
            return len(event_queue) != 0
        elif isinstance(t, int):
            return has_event(( t, ))
        else:
            return has_event(t)


def clear(t=None):

    # Clear is implemented in terms of get.
    get(t)

def get_standard_events():
    """
    Returns a list of standard events that renpy.pygame knows about.
    """

    return [ i for i in event_names.keys() if (i < SDL_EVENT_USER) or (i > USEREVENT_MAX) ]

def event_name(t):
    try:
        return event_names[t]
    except KeyError:
        return "UNKNOWN"


cdef inline bint is_sdl_lifecycle_event(Uint32 event_type) noexcept nogil:
    return (
        event_type == SDL_EVENT_TERMINATING or
        event_type == SDL_EVENT_LOW_MEMORY or
        event_type == SDL_EVENT_WILL_ENTER_BACKGROUND or
        event_type == SDL_EVENT_DID_ENTER_BACKGROUND or
        event_type == SDL_EVENT_WILL_ENTER_FOREGROUND or
        event_type == SDL_EVENT_DID_ENTER_FOREGROUND)


cdef void queue_sdl_lifecycle_event(SDL_Event *event) noexcept nogil:
    cdef SDL_Event queued_event

    memcpy(&queued_event, event, sizeof(SDL_Event))
    SDL_PeepEvents(&queued_event, 1, SDL_ADDEVENT, 0, 0)


cdef cbool lifecycle_event_watch(void *userdata, SDL_Event *event) noexcept nogil:

    # SDL calls this while it is pumping events. On Android, the pump that pauses the app only returns once
    # other threads stop posting events, so the timers have to be suspended here, rather than by the code that
    # handles the queued event.
    if event.type == SDL_EVENT_WILL_ENTER_BACKGROUND:
        suspend_timers(True)
    elif event.type == SDL_EVENT_DID_ENTER_FOREGROUND:
        suspend_timers(False)

    if is_sdl_lifecycle_event(event.type):
        queue_sdl_lifecycle_event(event)

    return True

def set_blocked(t=None):
    if t is None:
        for et in event_names.keys():
            SDL_SetEventEnabled(et, False)
    elif isinstance(t, int):
        SDL_SetEventEnabled(t, False)
    else:
        for et in t:
            SDL_SetEventEnabled(et, False)

def set_allowed(t=None):
    if t is None:
        for et in event_names.keys():
            SDL_SetEventEnabled(et, True)
    elif isinstance(t, int):
        SDL_SetEventEnabled(t, True)
    else:
        for et in t:
            SDL_SetEventEnabled(et, True)

def get_blocked(t):
    """
    Returns true if event type `t` is blocked. If `t` is a sequence of event
    types, returns true if any of them is blocked.
    """

    if isinstance(t, int):
        return not SDL_EventEnabled(t)

    return any(not SDL_EventEnabled(et) for et in t)

def set_grab(on):
    if main_window is None:
        raise error("No window has been created.")

    SDL_SetWindowMouseGrab(main_window.window, on)

    if not SDL_CursorVisible():
        SDL_SetWindowRelativeMouseMode(main_window.window, on)

def get_grab():
    if main_window is None:
        raise error("No window has been created.")

    return SDL_GetWindowMouseGrab(main_window.window)

def set_mousewheel_buttons(flag):
    """
    If true (the default), the mouse wheel generates presses and releases of
    mouse buttons 4 (up) and 5 (down) instead of MOUSEWHEEL events: one press
    and release for each wheel event that completes at least one whole step of
    vertical scrolling. Mouse buttons 4 and higher are mapped to 6 and higher.

    If false, the mouse wheel generates MOUSEWHEEL events, and the mouse
    buttons are not remapped.
    """

    global mousewheel_buttons
    mousewheel_buttons = flag

def get_mousewheel_buttons():
    """
    Returns the value set by mousehweel buttons,.
    """

    return mousewheel_buttons

def post(e):
    """
    Posts event object `e` to the event queue.
    """

    cdef SDL_Event event

    if not isinstance(e, EventType):
        raise error("event.post must be called with an Event.")

    if get_blocked(e.type):
        return

    Py_INCREF(e)

    # A zero timestamp makes SDL stamp the event with the current time.
    memset(&event, 0, sizeof(event))
    event.type = POSTEDEVENT
    event.user.data1 = <void *> e

    # The reference is released when the event is taken off the queue, or here
    # if SDL rejected it.
    if not SDL_PushEvent(&event):
        Py_DECREF(e)

def register(name):
    """
    Registers a unique event number and returns that number.

    `name`
        A string name for the event. This is used when calling `repr` on
        the event.
    """

    rv = SDL_RegisterEvents(1)

    event_names[rv] = name
    return rv

def copy_event_queue():
    """
    Returns a copy of the event queue. The copy cannot be used for modifying
    the event queue.
    """

    return event_queue[:]

# Usually called by display.init.
def init():
    if not SDL_WasInit(SDL_INIT_EVENTS):

        from . import display

        display.sdl_main_init()

        if not SDL_InitSubSystem(SDL_INIT_EVENTS):
            raise error()

    SDL_AddEventWatch(lifecycle_event_watch, NULL)
