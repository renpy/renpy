# Copyright 2014 Patrick Dawson <pat@dw.is>
# Copyright 2014 Tom Rothamel <tom@rothamel.us>
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

from cpython.ref cimport Py_INCREF, Py_DECREF

from libc.string cimport memcpy

from .sdl cimport *
from .display cimport Window, main_window
from .error import error
from . import key
import threading
import sys


event_names = {
    SDL_EVENT_FIRST: "FIRST",
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
    SDL_EVENT_DISPLAY_FIRST: "DISPLAYFIRST",
    SDL_EVENT_DISPLAY_LAST: "DISPLAYLAST",
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
    SDL_EVENT_WINDOW_FIRST: "WINDOWFIRST",
    SDL_EVENT_WINDOW_LAST: "WINDOWLAST",
    SDL_EVENT_KEY_DOWN: "KEYDOWN",
    SDL_EVENT_KEY_UP: "KEYUP",
    SDL_EVENT_TEXT_EDITING: "TEXTEDITING",
    SDL_EVENT_TEXT_INPUT: "TEXTINPUT",
    SDL_EVENT_KEYMAP_CHANGED: "KEYMAPCHANGED",
    SDL_EVENT_KEYBOARD_ADDED: "KEYBOARDADDED",
    SDL_EVENT_KEYBOARD_REMOVED: "KEYBOARDREMOVED",
    SDL_EVENT_TEXT_EDITING_CANDIDATES: "TEXTEDITINGCANDIDATES",
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


# Add events to emulate SDL 1 and 2. These also need to be added in locals.
ACTIVEEVENT = SDL_EVENT_LAST - 1
VIDEORESIZE = SDL_EVENT_LAST - 2
VIDEOEXPOSE = SDL_EVENT_LAST - 3
WINDOWMOVED = SDL_EVENT_LAST - 4
# (Do not add events here.)

event_names[ACTIVEEVENT] = "ACTIVEEVENT"
event_names[VIDEORESIZE] = "VIDEORESIZE"
event_names[VIDEOEXPOSE] = "VIDEOEXPOSE"
event_names[WINDOWMOVED] = "WINDOWMOVED"

# This is used for events posted to the event queue. This won't be returned
# to the user - it's just used internally, with the event object itself
# giving the type.
cdef unsigned int POSTEDEVENT
POSTEDEVENT = SDL_EVENT_LAST - 5

# The maximum number of a user-defined event.
USEREVENT_MAX = SDL_EVENT_LAST - 6

# If true, the mousewheel is mapped to buttons 4 and 5. Otherwise, a
# MOUSEWHEEL event is created.
cdef bint mousewheel_buttons = 1

cdef unsigned int SDL_TOUCH_MOUSEID
SDL_TOUCH_MOUSEID = <unsigned int> -1 # type: ignore

class EventType(object):

    def __init__(self, type, dict=None, **kwargs):
        self._type = type

        if dict:
            self.__dict__.update(dict)

        self.__dict__.update(kwargs)

    def __repr__(self):
        if SDL_EVENT_USER <= self.type < WINDOWMOVED:
            ename = "UserEvent%d" % (self.type - SDL_EVENT_USER)
        else:
            try:
                ename = event_names[self.type]
            except KeyError:
                ename = "UNKNOWN"

        rest = [ ]

        for k, v in sorted(self.__dict__.items()):
            if k == "_type" or k == "timestamp":
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
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

    def __nonzero__(self):
        return self.type != 0

Event = EventType

cdef get_textinput():
    cdef SDL_Event evt

    SDL_PumpEvents()

    if SDL_PeepEvents(&evt, 1, SDL_GETEVENT, SDL_EVENT_TEXT_INPUT, SDL_EVENT_TEXT_INPUT) > 0:
        return evt.text.text.decode('utf-8')
    return u''

cdef make_keyboard_event(SDL_KeyboardEvent *e):
    dargs = { 'scancode' : e.scancode,
              'key' : e.key,
              'mod' : e.mod,
              'unicode' : '',
              'repeat' : e.repeat,
               }

    if key.text_input:

        if e.type == SDL_EVENT_KEY_DOWN:
            # Be careful to only check for a TEXTINPUT event when you know that
            # there will be one associated with this KEYDOWN event.
            if e.key < 0x20:
                dargs['unicode'] = chr(e.key)
            elif e.key <= 0xFFFF:
                dargs['unicode'] = get_textinput()

    else:
        if e.type == SDL_EVENT_KEY_DOWN and not(e.key & SDL_KMOD_NUM):
            if SDLK_KP_1 <= e.key <= SDLK_KP_0:
                get_textinput()
                dargs['unicode'] = ''

    return EventType(e.type, dict=dargs, repeat=e.repeat)

cdef make_mousemotion_event(SDL_MouseMotionEvent *e):
    buttons = (1 if e.state & SDL_BUTTON_LMASK else 0,
               1 if e.state & SDL_BUTTON_MMASK else 0,
               1 if e.state & SDL_BUTTON_RMASK else 0)
    return EventType(e.type, pos=(e.x, e.y), rel=(e.xrel, e.yrel), which=e.which, buttons=buttons, touch=(SDL_TOUCH_MOUSEID == e.which))

cdef make_mousebtn_event(SDL_MouseButtonEvent *e):
    btn = e.button

    # SDL 1.x maps wheel to buttons 4/5
    if mousewheel_buttons and btn >= 4:
        btn += 2

    return EventType(e.type, button=btn, pos=(e.x, e.y), which=e.which, touch=(SDL_TOUCH_MOUSEID == e.which))

cdef make_mousewheel_event(SDL_MouseWheelEvent *e):

    cdef float mx, my

    # SDL2-style, if the user has opted-in.
    if not mousewheel_buttons:
        return EventType(e.type, which=e.which, x=e.x, y=e.y, touch=(SDL_TOUCH_MOUSEID == e.which))

    # Otherwise, follow the SDL1 approach.

    cdef float y = e.y

    if e.direction == SDL_MOUSEWHEEL_FLIPPED:
        y = -y

    if y > 0:
        btn = 4
    elif y < 0:
        btn = 5
    else:
        return EventType(0) # x axis scrolling produces no event in pygame

    # This is not the mouse position at the time of the event
    SDL_GetMouseState(&mx, &my)

    # MOUSEBUTTONUP event should follow immediately after
    event_queue.insert(0, EventType(SDL_EVENT_MOUSE_BUTTON_UP, which=e.which, button=btn, pos=(mx, my), touch=(SDL_TOUCH_MOUSEID == e.which)))
    return EventType(SDL_EVENT_MOUSE_BUTTON_DOWN, which=e.which, button=btn, pos=(mx, my), touch=(SDL_TOUCH_MOUSEID == e.which))

cdef make_joyaxis_event(SDL_JoyAxisEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, axis=e.axis, value=e.value/32768.0)

cdef make_joyball_event(SDL_JoyBallEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, ball=e.ball, rel=(e.xrel, e.yrel))

cdef make_joyhat_event(SDL_JoyHatEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, hat=e.hat, value=e.value)

cdef make_joybtn_event(SDL_JoyButtonEvent *e):
    return EventType(e.type, joy=e.which, instance_id=e.which, button=e.button)

cdef make_textinput_event(SDL_TextInputEvent *e):
    try:
        return EventType(e.type, text=e.text.decode("utf-8"))
    except UnicodeDecodeError:
        return EventType(e.type, text='')

cdef make_textediting_event(SDL_TextEditingEvent *e):
    try:
        return EventType(e.type, text=e.text.decode("utf-8"), start=e.start, length=e.length)
    except UnicodeDecodeError:
        return EventType(e.type, text='', start=e.start, length=e.length)

cdef make_drop_event(SDL_DropEvent *e):
    if e.data:
        file = e.data.decode("utf-8")
    else:
        file = None

    return EventType(e.type, file=file, window_id=e.windowID)

cdef make_window_event(SDL_WindowEvent *e):
    if e.type == SDL_EVENT_WINDOW_MOUSE_ENTER:
        return EventType(ACTIVEEVENT, state=1, gain=1)
    elif e.type == SDL_EVENT_WINDOW_MOUSE_LEAVE:
        return EventType(ACTIVEEVENT, state=1, gain=0)

    elif e.type == SDL_EVENT_WINDOW_FOCUS_GAINED:
        return EventType(ACTIVEEVENT, state=2, gain=1)
    elif e.type == SDL_EVENT_WINDOW_FOCUS_LOST:
        return EventType(ACTIVEEVENT, state=2, gain=0)

    elif e.type == SDL_EVENT_WINDOW_RESTORED:
        return EventType(ACTIVEEVENT, state=4, gain=1)
    elif e.type == SDL_EVENT_WINDOW_MINIMIZED:
        return EventType(ACTIVEEVENT, state=4, gain=0)

    elif e.type == SDL_EVENT_WINDOW_RESIZED:
        return EventType(VIDEORESIZE, size=(e.data1, e.data2), w=e.data1, h=e.data2)

    elif e.type == SDL_EVENT_WINDOW_EXPOSED:
        return EventType(VIDEOEXPOSE)

    elif e.type == SDL_EVENT_WINDOW_MOVED:
        return EventType(WINDOWMOVED, pos=(e.data1, e.data2), x=e.data1, y=e.data2)

    return EventType(e.type, data1=e.data1, data2=e.data2)

cdef make_event(SDL_Event *e):
    cdef object o

    if e.type == SDL_EVENT_MOUSE_MOTION:
        return make_mousemotion_event(<SDL_MouseMotionEvent*>e)
    elif e.type in (SDL_EVENT_MOUSE_BUTTON_DOWN, SDL_EVENT_MOUSE_BUTTON_UP):
        return make_mousebtn_event(<SDL_MouseButtonEvent*>e)

    elif e.type == SDL_EVENT_MOUSE_WHEEL:
        return make_mousewheel_event(<SDL_MouseWheelEvent*>e)
    elif e.type in (SDL_EVENT_KEY_DOWN, SDL_EVENT_KEY_UP):
        return make_keyboard_event(<SDL_KeyboardEvent*>e)
    elif e.type == SDL_EVENT_JOYSTICK_AXIS_MOTION:
        return make_joyaxis_event(<SDL_JoyAxisEvent*>e)
    elif e.type == SDL_EVENT_JOYSTICK_BALL_MOTION:
        return make_joyball_event(<SDL_JoyBallEvent*>e)
    elif e.type == SDL_EVENT_JOYSTICK_HAT_MOTION:
        return make_joyhat_event(<SDL_JoyHatEvent*>e)
    elif e.type in (SDL_EVENT_JOYSTICK_BUTTON_DOWN, SDL_EVENT_JOYSTICK_BUTTON_UP):
        return make_joybtn_event(<SDL_JoyButtonEvent*>e)
    elif e.type in (SDL_EVENT_JOYSTICK_ADDED, SDL_EVENT_JOYSTICK_REMOVED):
        return EventType(e.type, which=e.jdevice.which)
    elif SDL_EVENT_WINDOW_FIRST <= e.type <= SDL_EVENT_WINDOW_LAST:
        return make_window_event(<SDL_WindowEvent*>e)
    elif e.type == SDL_EVENT_TEXT_INPUT:
        return make_textinput_event(<SDL_TextInputEvent *> e)
    elif e.type == SDL_EVENT_TEXT_EDITING:
        return make_textediting_event(<SDL_TextEditingEvent *> e)
    elif e.type == SDL_EVENT_GAMEPAD_AXIS_MOTION:
        return EventType(e.type, which=e.gaxis.which, axis=e.gaxis.axis, value=e.gaxis.value)
    elif e.type in (SDL_EVENT_GAMEPAD_BUTTON_DOWN, SDL_EVENT_GAMEPAD_BUTTON_UP):
        return EventType(e.type, which=e.gbutton.which, button=e.gbutton.button, state=e.gbutton.down)
    elif e.type in (SDL_EVENT_GAMEPAD_ADDED, SDL_EVENT_GAMEPAD_REMOVED, SDL_EVENT_GAMEPAD_REMAPPED):
        return EventType(e.type, which=e.gdevice.which)
    elif e.type in (SDL_EVENT_FINGER_MOTION, SDL_EVENT_FINGER_DOWN, SDL_EVENT_FINGER_UP):
        return EventType(e.type, touchId=e.tfinger.touchId, fingerId=e.tfinger.fingerId, touch_id=e.tfinger.touchId, finger_id=e.tfinger.fingerId, x=e.tfinger.x, y=e.tfinger.y, dx=e.tfinger.dx, dy=e.tfinger.dy, pressure=e.tfinger.pressure)
    elif e.type in (SDL_EVENT_DROP_FILE, SDL_EVENT_DROP_TEXT, SDL_EVENT_DROP_BEGIN, SDL_EVENT_DROP_COMPLETE):
        return make_drop_event(<SDL_DropEvent*> e)
    elif e.type == POSTEDEVENT:
        o = <object> e.user.data1
        Py_DECREF(o)
        return o
    elif e.type >= SDL_EVENT_USER:
        # Can't do anything useful with data1 and data2 here.
        return EventType(e.type, code=e.user.code)

    return EventType(e.type)


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
                    e.timestamp = evt.common.timestamp
                    event_queue.append(e)

                memcpy(&old_evt, &evt, sizeof(SDL_Event))
                last_mousemotion = True

            else:
                if last_mousemotion:
                    e = make_mousemotion_event(old_mm_evt)
                    e.timestamp = evt.common.timestamp
                    event_queue.append(e)
                    last_mousemotion = False

                e = make_event(&evt)
                e.timestamp = evt.common.timestamp
                event_queue.append(e)
                last_mousemotion = False

        if last_mousemotion:
            e = make_mousemotion_event(old_mm_evt)
            e.timestamp = old_evt.common.timestamp
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

    cdef SDL_Event evt
    cdef int result

    with lock:
        poll_sdl()

        if event_queue:
            return event_queue.pop(0)

    with nogil:
        result = SDL_WaitEvent(&evt)

    if result:
        return make_event(&evt)
    else:
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

def set_blocked(t=None):
    if t == None:
        for et in event_names.keys():
            SDL_SetEventEnabled(et, False)
    elif isinstance(t, int):
        SDL_SetEventEnabled(t, False)
    else:
        for et in t:
            SDL_SetEventEnabled(et, False)

def set_allowed(t=None):
    if t == None:
        for et in event_names.keys():
            SDL_SetEventEnabled(et, True)
    elif isinstance(t, int):
        SDL_SetEventEnabled(t, True)
    else:
        for et in t:
            SDL_SetEventEnabled(et, True)

def get_blocked(t):
    return not SDL_EventEnabled(t)

def set_grab(on):
    SDL_SetWindowMouseGrab(main_window.window, on)

    if not SDL_CursorVisible():
        SDL_SetWindowRelativeMouseMode(main_window.window, on)

def get_grab():
    return SDL_GetWindowMouseGrab(main_window.window)

def set_mousewheel_buttons(flag):
    """
    If true (the default), the mousewheel will generate events involving
    mouse buttons 4 and 5, and mousebuttons 4 and higher will be mapped to 6 and higher.

    If false, MOUSEWHEEL events are generated, and the mousebuttons are
    not remapped.
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

    cdef SDL_Event event;

    if not isinstance(e, EventType):
        raise error("event.post must be called with an Event.")

    if get_blocked(e.type):
        return

    Py_INCREF(e)

    event.type = POSTEDEVENT
    event.user.data1 = <void *> e

    SDL_PushEvent(&event)

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

        if SDL_InitSubSystem(SDL_INIT_EVENTS):
            raise error()
