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

from sdl2 cimport *
from renpy.pygame.display cimport Window, main_window
import threading
import renpy.pygame
import sys

if sys.version_info[0] >= 3:
    unichr = chr

include "event_names.pxi"

# Add events to emulate SDL 1.2. These also need to be added in locals.
ACTIVEEVENT = SDL_LASTEVENT - 1
VIDEORESIZE = SDL_LASTEVENT - 2
VIDEOEXPOSE = SDL_LASTEVENT - 3
WINDOWMOVED = SDL_LASTEVENT - 4
# (Do not add events here.)

event_names[ACTIVEEVENT] = "ACTIVEEVENT"
event_names[VIDEORESIZE] = "VIDEORESIZE"
event_names[VIDEOEXPOSE] = "VIDEOEXPOSE"
event_names[WINDOWMOVED] = "WINDOWMOVED"

# This is used for events posted to the event queue. This won't be returned
# to the user - it's just used internally, with the event object itself
# giving the type.
cdef unsigned int POSTEDEVENT
POSTEDEVENT = SDL_LASTEVENT - 5

# The maximum number of a user-defined event.
USEREVENT_MAX = SDL_LASTEVENT - 6

# If true, the mousewheel is mapped to buttons 4 and 5. Otherwise, a
# MOUSEWHEEL event is created.
cdef bint mousewheel_buttons = 1

cdef unsigned int SDL_TOUCH_MOUSEID
SDL_TOUCH_MOUSEID = <unsigned int> -1

class EventType(object):

    def __init__(self, type, dict=None, **kwargs):
        self._type = type

        if dict:
            self.__dict__.update(dict)

        self.__dict__.update(kwargs)

    def __repr__(self):
        if SDL_USEREVENT <= self.type < WINDOWMOVED:
            ename = "UserEvent%d" % (self.type - SDL_USEREVENT)
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

    if SDL_PeepEvents(&evt, 1, SDL_GETEVENT, SDL_TEXTINPUT, SDL_TEXTINPUT) > 0:
        return evt.text.text.decode('utf-8')
    return u''

cdef make_keyboard_event(SDL_KeyboardEvent *e):
    dargs = { 'scancode' : e.keysym.scancode,
              'key' : e.keysym.sym,
              'mod' : e.keysym.mod,
              'unicode' : '',
              'repeat' : e.repeat,
               }

    if not renpy.pygame.key.text_input:

        if e.type == SDL_KEYDOWN:
            # Be careful to only check for a TEXTINPUT event when you know that
            # there will be one associated with this KEYDOWN event.
            if e.keysym.sym < 0x20:
                dargs['unicode'] = unichr(e.keysym.sym)
            elif e.keysym.sym <= 0xFFFF:
                dargs['unicode'] = get_textinput()

    else:
        if e.type == SDL_KEYDOWN and not(e.keysym.mod & KMOD_NUM):
            if SDLK_KP_1 <= e.keysym.sym <= SDLK_KP_0:
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

    cdef int x, y

    # SDL2-style, if the user has opted-in.
    if not mousewheel_buttons:
        return EventType(e.type, which=e.which, x=e.x, y=e.y, touch=(SDL_TOUCH_MOUSEID == e.which))

    # Otherwise, follow the SDL1 approach.

    y = e.y

# TODO: Implement when 2.0.4 becomes widespread.
#     if e.direction == SDL_MOUSEWHEEL_FLIPPED:
#         y = -y

    if y > 0:
        btn = 4
    elif y < 0:
        btn = 5
    else:
        return EventType(0) # x axis scrolling produces no event in pygame

    # This is not the mouse position at the time of the event
    SDL_GetMouseState(&x, &y)

    # MOUSEBUTTONUP event should follow immediately after
    event_queue.insert(0, EventType(SDL_MOUSEBUTTONUP, which=e.which, button=btn, pos=(x,y), touch=(SDL_TOUCH_MOUSEID == e.which)))
    return EventType(SDL_MOUSEBUTTONDOWN, which=e.which, button=btn, pos=(x,y), touch=(SDL_TOUCH_MOUSEID == e.which))


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
    if e.file:
        file = e.file.decode("utf-8")
        SDL_free(e.file)
    else:
        file = None

    return EventType(e.type, file=file, window_id=e.windowID)

cdef make_window_event(SDL_WindowEvent *e):
    # SDL_APPMOUSEFOCUS
    if e.event == SDL_WINDOWEVENT_ENTER:
        return EventType(ACTIVEEVENT, state=1, gain=1)
    elif e.event == SDL_WINDOWEVENT_LEAVE:
        return EventType(ACTIVEEVENT, state=1, gain=0)

    # SDL_APPINPUTFOCUS
    elif e.event == SDL_WINDOWEVENT_FOCUS_GAINED:
        return EventType(ACTIVEEVENT, state=2, gain=1)
    elif e.event == SDL_WINDOWEVENT_FOCUS_LOST:
        return EventType(ACTIVEEVENT, state=2, gain=0)

    # SDL_APPACTIVE
    elif e.event == SDL_WINDOWEVENT_RESTORED:
        return EventType(ACTIVEEVENT, state=4, gain=1)
    elif e.event == SDL_WINDOWEVENT_MINIMIZED:
        return EventType(ACTIVEEVENT, state=4, gain=0)

    elif e.event == SDL_WINDOWEVENT_RESIZED:
        return EventType(VIDEORESIZE, size=(e.data1, e.data2), w=e.data1, h=e.data2)

    elif e.event == SDL_WINDOWEVENT_EXPOSED:
        return EventType(VIDEOEXPOSE)

    elif e.event == SDL_WINDOWEVENT_MOVED:
        return EventType(WINDOWMOVED, pos=(e.data1, e.data2), x=e.data1, y=e.data2)

    return EventType(SDL_WINDOWEVENT, event=e.event, data1=e.data1, data2=e.data2)

cdef make_event(SDL_Event *e):
    cdef object o

    if e.type == SDL_MOUSEMOTION:
        return make_mousemotion_event(<SDL_MouseMotionEvent*>e)
    elif e.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
        return make_mousebtn_event(<SDL_MouseButtonEvent*>e)

    elif e.type == SDL_MOUSEWHEEL:
        return make_mousewheel_event(<SDL_MouseWheelEvent*>e)
    elif e.type in (SDL_KEYDOWN, SDL_KEYUP):
        return make_keyboard_event(<SDL_KeyboardEvent*>e)
    elif e.type == SDL_JOYAXISMOTION:
        return make_joyaxis_event(<SDL_JoyAxisEvent*>e)
    elif e.type == SDL_JOYBALLMOTION:
        return make_joyball_event(<SDL_JoyBallEvent*>e)
    elif e.type == SDL_JOYHATMOTION:
        return make_joyhat_event(<SDL_JoyHatEvent*>e)
    elif e.type in (SDL_JOYBUTTONDOWN, SDL_JOYBUTTONUP):
        return make_joybtn_event(<SDL_JoyButtonEvent*>e)
    elif e.type in (SDL_JOYDEVICEADDED, SDL_JOYDEVICEREMOVED):
        return EventType(e.type, which=e.jdevice.which)
    elif e.type == SDL_WINDOWEVENT:
        return make_window_event(<SDL_WindowEvent*>e)
    elif e.type == SDL_TEXTINPUT:
        return make_textinput_event(<SDL_TextInputEvent *> e)
    elif e.type == SDL_TEXTEDITING:
        return make_textediting_event(<SDL_TextEditingEvent *> e)
    elif e.type == SDL_CONTROLLERAXISMOTION:
        return EventType(e.type, which=e.caxis.which, axis=e.caxis.axis, value=e.caxis.value)
    elif e.type in (SDL_CONTROLLERBUTTONDOWN, SDL_CONTROLLERBUTTONUP):
        return EventType(e.type, which=e.cbutton.which, button=e.cbutton.button, state=e.cbutton.state)
    elif e.type in (SDL_CONTROLLERDEVICEADDED, SDL_CONTROLLERDEVICEREMOVED, SDL_CONTROLLERDEVICEREMAPPED):
        return EventType(e.type, which=e.cdevice.which)
    elif e.type in (SDL_FINGERMOTION, SDL_FINGERDOWN, SDL_FINGERUP):
        return EventType(e.type, touchId=e.tfinger.touchId, fingerId=e.tfinger.fingerId, touch_id=e.tfinger.touchId, finger_id=e.tfinger.fingerId, x=e.tfinger.x, y=e.tfinger.y, dx=e.tfinger.dx, dy=e.tfinger.dy, pressure=e.tfinger.pressure)
    elif e.type == SDL_MULTIGESTURE:
        return EventType(e.type, touchId=e.mgesture.touchId, dTheta=e.mgesture.dTheta, dDist=e.mgesture.dDist, x=e.mgesture.x, y=e.mgesture.y, numFingers=e.mgesture.numFingers, touch_id=e.mgesture.touchId, rotated=e.mgesture.dTheta, pinched=e.mgesture.dDist, num_fingers=e.mgesture.numFingers)
    elif e.type in (SDL_DROPFILE, SDL_DROPTEXT, SDL_DROPBEGIN, SDL_DROPCOMPLETE):
        return make_drop_event(<SDL_DropEvent*> e)
    elif e.type == POSTEDEVENT:
        o = <object> e.user.data1
        Py_DECREF(o)
        return o
    elif e.type >= SDL_USEREVENT:
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
            if evt.type == SDL_MOUSEMOTION:

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

    return [ i for i in event_names.keys() if (i < SDL_USEREVENT) or (i > USEREVENT_MAX) ]

def event_name(t):
    try:
        return event_names[t]
    except KeyError:
        return "UNKNOWN"

def set_blocked(t=None):
    if t == None:
        for et in event_names.keys():
            SDL_EventState(et, SDL_ENABLE)
    elif isinstance(t, int):
        SDL_EventState(t, SDL_IGNORE)
    else:
        for et in t:
            SDL_EventState(et, SDL_IGNORE)

def set_allowed(t=None):
    if t == None:
        for et in event_names.keys():
            SDL_EventState(et, SDL_IGNORE)
    elif isinstance(t, int):
        SDL_EventState(t, SDL_ENABLE)
    else:
        for et in t:
            SDL_EventState(et, SDL_ENABLE)

def get_blocked(t):
    return SDL_EventState(t, SDL_QUERY) == SDL_IGNORE

def set_grab(on):
    SDL_SetWindowGrab(main_window.window, on)

    if SDL_ShowCursor(SDL_QUERY) == SDL_DISABLE:
        SDL_SetRelativeMouseMode(on)

def get_grab():
    return SDL_GetWindowGrab(main_window.window)

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
        raise renpy.pygame.error("event.post must be called with an Event.")

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

        renpy.pygame.display.sdl_main_init()

        if SDL_InitSubSystem(SDL_INIT_EVENTS):
            raise renpy.pygame.error.error()
