=============
pygame Events
=============

This page lists the events that :doc:`renpy.pygame <pygame>` produces, the
attributes each one carries, and how they differ from the events of
`pygame-ce <https://pyga.me/docs/ref/event.html>`_.

Events reach a game through the ``event`` method of a
:doc:`creator-defined displayable <cdd>`. Ren'Py blocks the event types it
does not use, so they are never delivered; the Default column below says
which types reach displayables without any configuration. To receive another
type, add it to :var:`config.pygame_events`.

Every event is an instance of ``pygame.Event`` (also available as
``pygame.event.Event``), and can be compared with the constants in the
Event column, such as ``ev.type == pygame.KEYDOWN``. An event's attributes
are also available as the dictionary ``ev.dict``, and
``pygame.event.event_name(ev.type)`` gives the first name in the Event
column.

Every event has a ``timestamp`` attribute: the time SDL queued the event,
as a float number of seconds since SDL started, or 0.0 for an event the game
created itself. It is not part of ``ev.dict``.

The ``window`` attribute is the main window, as returned by
``pygame.display.get_window()``, when SDL associates the event with it, and
None otherwise.

The Event column gives the Ren'Py name of each type first, then other names
for the same type, such as the pygame-ce names, and finally the name SDL
uses. Positions and sizes are in the units SDL reports them in, and Ren'Py
gives the event's position in virtual pixels separately, as the ``x`` and
``y`` arguments to the ``event`` method.

The event types that are available, and the attributes each event has, come
from the version of SDL that Ren'Py uses, and may change in major versions of
Ren'Py.


Application Events
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``QUIT`` (``SDL_EVENT_QUIT``)
     - Yes
     - None
     - None
   * - ``TERMINATING``, ``APP_TERMINATING`` (``SDL_EVENT_TERMINATING``)
     - Yes
     - None
     - None
   * - ``LOWMEMORY``, ``APP_LOWMEMORY`` (``SDL_EVENT_LOW_MEMORY``)
     - Yes
     - None
     - None
   * - ``WILLENTERBACKGROUND``, ``APP_WILLENTERBACKGROUND``
       (``SDL_EVENT_WILL_ENTER_BACKGROUND``)
     - Yes
     - None
     - None
   * - ``DIDENTERBACKGROUND``, ``APP_DIDENTERBACKGROUND``
       (``SDL_EVENT_DID_ENTER_BACKGROUND``)
     - Yes
     - None
     - None
   * - ``WILLENTERFOREGROUND``, ``APP_WILLENTERFOREGROUND``
       (``SDL_EVENT_WILL_ENTER_FOREGROUND``)
     - Yes
     - None
     - None
   * - ``DIDENTERFOREGROUND``, ``APP_DIDENTERFOREGROUND``
       (``SDL_EVENT_DID_ENTER_FOREGROUND``)
     - Yes
     - None
     - None
   * - ``LOCALECHANGED`` (``SDL_EVENT_LOCALE_CHANGED``)
     - No
     - None
     - None
   * - ``SYSTEMTHEMECHANGED`` (``SDL_EVENT_SYSTEM_THEME_CHANGED``)
     - No
     - None
     - Not in pygame-ce.
   * - ``CLIPBOARDUPDATE`` (``SDL_EVENT_CLIPBOARD_UPDATE``)
     - No
     - None
     - None


Display Events
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``DISPLAYORIENTATION`` (``SDL_EVENT_DISPLAY_ORIENTATION``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYADDED`` (``SDL_EVENT_DISPLAY_ADDED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYREMOVED`` (``SDL_EVENT_DISPLAY_REMOVED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYMOVED`` (``SDL_EVENT_DISPLAY_MOVED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYDESKTOPMODECHANGED``
       (``SDL_EVENT_DISPLAY_DESKTOP_MODE_CHANGED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYCURRENTMODECHANGED``
       (``SDL_EVENT_DISPLAY_CURRENT_MODE_CHANGED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYCONTENTSCALECHANGED``
       (``SDL_EVENT_DISPLAY_CONTENT_SCALE_CHANGED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.
   * - ``DISPLAYUSABLEBOUNDSCHANGED``
       (``SDL_EVENT_DISPLAY_USABLE_BOUNDS_CHANGED``)
     - No
     - ``display_index: int``, ``data1: int``, ``data2: int``
     - Not in pygame-ce.

``display_index`` is SDL's id for the display, which is not necessarily its
position in the list of displays.


Window Events
-------------

Every window event has the fields ``data1: int``, ``data2: int``, and
``window: Window | None``. The meaning of ``data1`` and ``data2`` depends
on the event, as described by SDL; the Fields column lists other fields.

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``WINDOWSHOWN`` (``SDL_EVENT_WINDOW_SHOWN``)
     - Yes
     - None
     - None
   * - ``WINDOWHIDDEN`` (``SDL_EVENT_WINDOW_HIDDEN``)
     - Yes
     - None
     - None
   * - ``WINDOWEXPOSED`` (``SDL_EVENT_WINDOW_EXPOSED``)
     - Yes
     - None
     - None
   * - ``WINDOWMOVED`` (``SDL_EVENT_WINDOW_MOVED``)
     - Yes
     - ``x: int``, ``y: int`` (the window's new position)
     - None
   * - ``WINDOWRESIZED``, ``WINDOWSIZECHANGED``
       (``SDL_EVENT_WINDOW_RESIZED``)
     - Yes
     - ``x: int``, ``y: int`` (the window's new size)
     - ``WINDOWSIZECHANGED`` is a pygame-ce name. pygame-ce has two events
       for a change in the window's size, and here both names give this one.
   * - ``WINDOWPIXELSIZECHANGED`` (``SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED``)
     - Yes
     - ``x: int``, ``y: int`` (the window's new size in pixels)
     - Not in pygame-ce. The size in pixels can differ from the size
       ``WINDOWRESIZED`` gives on high-DPI displays.
   * - ``WINDOWMETALVIEWRESIZED`` (``SDL_EVENT_WINDOW_METAL_VIEW_RESIZED``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWMINIMIZED`` (``SDL_EVENT_WINDOW_MINIMIZED``)
     - Yes
     - None
     - None
   * - ``WINDOWMAXIMIZED`` (``SDL_EVENT_WINDOW_MAXIMIZED``)
     - Yes
     - None
     - None
   * - ``WINDOWRESTORED`` (``SDL_EVENT_WINDOW_RESTORED``)
     - Yes
     - None
     - None
   * - ``WINDOWMOUSEENTER``, ``WINDOWENTER`` (``SDL_EVENT_WINDOW_MOUSE_ENTER``)
     - Yes
     - None
     - ``WINDOWENTER`` is the pygame-ce name.
   * - ``WINDOWMOUSELEAVE``, ``WINDOWLEAVE`` (``SDL_EVENT_WINDOW_MOUSE_LEAVE``)
     - Yes
     - None
     - ``WINDOWLEAVE`` is the pygame-ce name.
   * - ``WINDOWFOCUSGAINED`` (``SDL_EVENT_WINDOW_FOCUS_GAINED``)
     - Yes
     - None
     - None
   * - ``WINDOWFOCUSLOST`` (``SDL_EVENT_WINDOW_FOCUS_LOST``)
     - Yes
     - None
     - None
   * - ``WINDOWCLOSEREQUESTED``, ``WINDOWCLOSE``
       (``SDL_EVENT_WINDOW_CLOSE_REQUESTED``)
     - Yes
     - None
     - ``WINDOWCLOSE`` is the pygame-ce name.
   * - ``WINDOWHITTEST`` (``SDL_EVENT_WINDOW_HIT_TEST``)
     - Yes
     - None
     - None
   * - ``WINDOWICCPROFCHANGED`` (``SDL_EVENT_WINDOW_ICCPROF_CHANGED``)
     - Yes
     - None
     - None
   * - ``WINDOWDISPLAYCHANGED`` (``SDL_EVENT_WINDOW_DISPLAY_CHANGED``)
     - Yes
     - ``display_index: int``
     - ``display_index`` is SDL's id for the display, rather than its
       position in the list of displays. pygame-ce also gives ``x`` and ``y``.
   * - ``WINDOWDISPLAYSCALECHANGED``
       (``SDL_EVENT_WINDOW_DISPLAY_SCALE_CHANGED``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWSAFEAREACHANGED`` (``SDL_EVENT_WINDOW_SAFE_AREA_CHANGED``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWOCCLUDED`` (``SDL_EVENT_WINDOW_OCCLUDED``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWENTERFULLSCREEN`` (``SDL_EVENT_WINDOW_ENTER_FULLSCREEN``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWLEAVEFULLSCREEN`` (``SDL_EVENT_WINDOW_LEAVE_FULLSCREEN``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWDESTROYED`` (``SDL_EVENT_WINDOW_DESTROYED``)
     - Yes
     - None
     - Not in pygame-ce.
   * - ``WINDOWHDRSTATECHANGED`` (``SDL_EVENT_WINDOW_HDR_STATE_CHANGED``)
     - Yes
     - None
     - Not in pygame-ce.

pygame-ce's ``WINDOWTAKEFOCUS`` has no SDL 3 equivalent, and is not
available. pygame-ce's window events have only the fields listed in the
pygame-ce documentation, not ``data1`` and ``data2``.


Keyboard and Text Events
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``KEYDOWN`` (``SDL_EVENT_KEY_DOWN``)
     - Yes
     - ``key: int``, ``mod: int``, ``scancode: int``, ``unicode: str``,
       ``repeat: bool``, ``window: Window | None``
     - While text input is active, ``unicode`` is empty for keys that type
       text, which arrives as TEXTINPUT events instead, and holds the
       character only for control keys such as Return and Backspace.
       ``repeat`` is not in pygame-ce.
   * - ``KEYUP`` (``SDL_EVENT_KEY_UP``)
     - Yes
     - ``key: int``, ``mod: int``, ``scancode: int``, ``unicode: str``,
       ``repeat: bool``, ``window: Window | None``
     - ``unicode`` is always empty. ``repeat`` is not in pygame-ce.
   * - ``TEXTEDITING`` (``SDL_EVENT_TEXT_EDITING``)
     - Yes
     - ``text: str``, ``start: int``, ``length: int``,
       ``window: Window | None``
     - ``text`` is empty if SDL gives text that is not valid UTF-8.
   * - ``TEXTINPUT`` (``SDL_EVENT_TEXT_INPUT``)
     - Yes
     - ``text: str``, ``window: Window | None``
     - ``text`` is empty if SDL gives text that is not valid UTF-8.
   * - ``TEXTEDITINGCANDIDATES`` (``SDL_EVENT_TEXT_EDITING_CANDIDATES``)
     - Yes
     - ``candidates: list[str]``, ``selected: int``, ``horizontal: bool``,
       ``window_id: int``, ``window: Window | None``
     - Not in pygame-ce.
   * - ``KEYMAPCHANGED`` (``SDL_EVENT_KEYMAP_CHANGED``)
     - Yes
     - None
     - None
   * - ``KEYBOARDADDED`` (``SDL_EVENT_KEYBOARD_ADDED``)
     - No
     - ``which: int``
     - Not in pygame-ce.
   * - ``KEYBOARDREMOVED`` (``SDL_EVENT_KEYBOARD_REMOVED``)
     - No
     - ``which: int``
     - Not in pygame-ce.
   * - ``SCREENKEYBOARDSHOWN`` (``SDL_EVENT_SCREEN_KEYBOARD_SHOWN``)
     - No
     - None
     - Not in pygame-ce.
   * - ``SCREENKEYBOARDHIDDEN`` (``SDL_EVENT_SCREEN_KEYBOARD_HIDDEN``)
     - No
     - None
     - Not in pygame-ce.


Mouse Events
------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``MOUSEMOTION`` (``SDL_EVENT_MOUSE_MOTION``)
     - Yes
     - ``pos: (float, float)``, ``rel: (float, float)``,
       ``buttons: (int, int, int)``, ``which: int``, ``touch: bool``,
       ``window: Window | None``
     - ``pos`` and ``rel`` are floats. ``which`` is not in pygame-ce.
   * - ``MOUSEBUTTONDOWN`` (``SDL_EVENT_MOUSE_BUTTON_DOWN``)
     - Yes
     - ``button: int``, ``pos: (float, float)``, ``which: int``,
       ``touch: bool``, ``clicks: int``, ``window: Window | None``
     - ``pos`` is floats. ``which`` is not in pygame-ce. By default, a mouse
       wheel event that completes at least one step of vertical scrolling
       produces one press and release of button 4 (up) or 5 (down), with
       ``clicks`` 1, however many steps it scrolls, and the mouse buttons
       numbered 4 and above by SDL are numbered from 6.
   * - ``MOUSEBUTTONUP`` (``SDL_EVENT_MOUSE_BUTTON_UP``)
     - Yes
     - ``button: int``, ``pos: (float, float)``, ``which: int``,
       ``touch: bool``, ``clicks: int``, ``window: Window | None``
     - As for ``MOUSEBUTTONDOWN``.
   * - ``MOUSEWHEEL`` (``SDL_EVENT_MOUSE_WHEEL``)
     - Yes [#wheel]_
     - ``which: int``, ``x: float``, ``y: float``, ``precise_x: float``,
       ``precise_y: float``, ``flipped: bool``, ``pos: (float, float)``,
       ``touch: bool``, ``window: Window | None``
     - ``x`` and ``y`` are floats, the same as ``precise_x`` and
       ``precise_y``. ``pos`` is floats.
   * - ``MOUSEADDED`` (``SDL_EVENT_MOUSE_ADDED``)
     - No
     - ``which: int``
     - Not in pygame-ce.
   * - ``MOUSEREMOVED`` (``SDL_EVENT_MOUSE_REMOVED``)
     - No
     - ``which: int``
     - Not in pygame-ce.

``touch`` is True when SDL synthesized a mouse event from a touch, as in
pygame-ce.

.. [#wheel] Ren'Py reports the mouse wheel as presses and releases of buttons
   4 and 5, so MOUSEWHEEL events are only produced after a call to
   ``pygame.event.set_mousewheel_buttons(False)``.


Joystick Events
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``JOYSTICKAXISMOTION``, ``JOYAXISMOTION``
       (``SDL_EVENT_JOYSTICK_AXIS_MOTION``)
     - Yes [#joystick]_
     - ``joy: int``, ``instance_id: int``, ``axis: int``, ``value: float``
     - ``joy`` is the same as ``instance_id``.
   * - ``JOYSTICKBALLMOTION``, ``JOYBALLMOTION``
       (``SDL_EVENT_JOYSTICK_BALL_MOTION``)
     - Yes [#joystick]_
     - ``joy: int``, ``instance_id: int``, ``ball: int``,
       ``rel: (int, int)``
     - ``joy`` is the same as ``instance_id``.
   * - ``JOYSTICKHATMOTION``, ``JOYHATMOTION``
       (``SDL_EVENT_JOYSTICK_HAT_MOTION``)
     - Yes [#joystick]_
     - ``joy: int``, ``instance_id: int``, ``hat: int``,
       ``value: (int, int)``
     - ``joy`` is the same as ``instance_id``.
   * - ``JOYSTICKBUTTONDOWN``, ``JOYBUTTONDOWN``
       (``SDL_EVENT_JOYSTICK_BUTTON_DOWN``)
     - Yes [#joystick]_
     - ``joy: int``, ``instance_id: int``, ``button: int``
     - ``joy`` is the same as ``instance_id``.
   * - ``JOYSTICKBUTTONUP``, ``JOYBUTTONUP`` (``SDL_EVENT_JOYSTICK_BUTTON_UP``)
     - Yes [#joystick]_
     - ``joy: int``, ``instance_id: int``, ``button: int``
     - ``joy`` is the same as ``instance_id``.
   * - ``JOYSTICKADDED``, ``JOYDEVICEADDED`` (``SDL_EVENT_JOYSTICK_ADDED``)
     - Yes [#joystick]_
     - ``which: int``, ``device_index: int``, ``instance_id: int``,
       ``guid: str``
     - ``device_index`` is the same as ``instance_id``, which is what
       ``pygame.joystick.Joystick`` takes. ``which`` and ``instance_id`` are
       not in pygame-ce.
   * - ``JOYSTICKREMOVED``, ``JOYDEVICEREMOVED`` (``SDL_EVENT_JOYSTICK_REMOVED``)
     - Yes [#joystick]_
     - ``which: int``, ``instance_id: int``
     - ``which`` is not in pygame-ce.
   * - ``JOYSTICKBATTERYUPDATED`` (``SDL_EVENT_JOYSTICK_BATTERY_UPDATED``)
     - No
     - ``which: int``, ``instance_id: int``, ``state: int``,
       ``percent: int``
     - Not in pygame-ce.
   * - ``JOYSTICKUPDATECOMPLETE`` (``SDL_EVENT_JOYSTICK_UPDATE_COMPLETE``)
     - No
     - None
     - Not in pygame-ce.

The ``value`` of a hat event is an ``(x, y)`` tuple, where ``x`` is -1 when
the hat is pushed left and 1 when it is pushed right, and ``y`` is 1 when it
is pushed up and -1 when it is pushed down. Each is 0 when the hat is
centered in that direction.

.. [#joystick] Ren'Py consumes these events itself unless
   :var:`config.pass_joystick_events` is True.


Gamepad Events
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``GAMEPADAXISMOTION``, ``CONTROLLERAXISMOTION``
       (``SDL_EVENT_GAMEPAD_AXIS_MOTION``)
     - Yes [#gamepad]_
     - ``which: int``, ``instance_id: int``, ``axis: int``, ``value: int``
     - ``value`` is the raw integer from -32768 to 32767, as in pygame-ce.
       ``which`` is not in pygame-ce.
   * - ``GAMEPADBUTTONDOWN``, ``CONTROLLERBUTTONDOWN``
       (``SDL_EVENT_GAMEPAD_BUTTON_DOWN``)
     - Yes [#gamepad]_
     - ``which: int``, ``instance_id: int``, ``button: int``,
       ``state: bool``
     - ``which`` and ``state`` are not in pygame-ce.
   * - ``GAMEPADBUTTONUP``, ``CONTROLLERBUTTONUP``
       (``SDL_EVENT_GAMEPAD_BUTTON_UP``)
     - Yes [#gamepad]_
     - ``which: int``, ``instance_id: int``, ``button: int``,
       ``state: bool``
     - ``which`` and ``state`` are not in pygame-ce.
   * - ``GAMEPADADDED``, ``CONTROLLERDEVICEADDED`` (``SDL_EVENT_GAMEPAD_ADDED``)
     - Yes [#gamepad]_
     - ``which: int``, ``device_index: int``, ``instance_id: int``,
       ``guid: str``
     - ``device_index`` is the same as ``instance_id``, which is what
       ``pygame.controller.Controller`` takes. ``which`` and ``instance_id``
       are not in pygame-ce.
   * - ``GAMEPADREMOVED``, ``CONTROLLERDEVICEREMOVED``
       (``SDL_EVENT_GAMEPAD_REMOVED``)
     - Yes [#gamepad]_
     - ``which: int``, ``instance_id: int``
     - ``which`` is not in pygame-ce.
   * - ``GAMEPADREMAPPED``, ``CONTROLLERDEVICEREMAPPED``
       (``SDL_EVENT_GAMEPAD_REMAPPED``)
     - No
     - ``which: int``, ``instance_id: int``
     - ``which`` is not in pygame-ce.
   * - ``GAMEPADTOUCHPADDOWN`` (``SDL_EVENT_GAMEPAD_TOUCHPAD_DOWN``)
     - No
     - ``which: int``, ``instance_id: int``, ``touch_id: int``,
       ``finger_id: int``, ``x: float``, ``y: float``, ``pressure: float``
     - Called ``CONTROLLERTOUCHPADDOWN`` in pygame-ce. ``which`` is not in
       pygame-ce.
   * - ``GAMEPADTOUCHPADMOTION`` (``SDL_EVENT_GAMEPAD_TOUCHPAD_MOTION``)
     - No
     - ``which: int``, ``instance_id: int``, ``touch_id: int``,
       ``finger_id: int``, ``x: float``, ``y: float``, ``pressure: float``
     - Called ``CONTROLLERTOUCHPADMOTION`` in pygame-ce. ``which`` is not in
       pygame-ce.
   * - ``GAMEPADTOUCHPADUP`` (``SDL_EVENT_GAMEPAD_TOUCHPAD_UP``)
     - No
     - ``which: int``, ``instance_id: int``, ``touch_id: int``,
       ``finger_id: int``, ``x: float``, ``y: float``, ``pressure: float``
     - Called ``CONTROLLERTOUCHPADUP`` in pygame-ce. ``which`` is not in
       pygame-ce.
   * - ``GAMEPADSENSORUPDATE`` (``SDL_EVENT_GAMEPAD_SENSOR_UPDATE``)
     - No
     - ``which: int``, ``instance_id: int``, ``sensor: int``,
       ``data: (float, float, float)``
     - Called ``CONTROLLERSENSORUPDATE`` in pygame-ce, where it has no
       fields.
   * - ``GAMEPADUPDATECOMPLETE`` (``SDL_EVENT_GAMEPAD_UPDATE_COMPLETE``)
     - No
     - None
     - Not in pygame-ce.
   * - ``GAMEPADSTEAMHANDLEUPDATED``
       (``SDL_EVENT_GAMEPAD_STEAM_HANDLE_UPDATED``)
     - No
     - None
     - Not in pygame-ce.

.. [#gamepad] Ren'Py consumes these events itself, to drive its own gamepad
   support, unless :var:`config.pass_controller_events` is True.


Touch Events
------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``FINGERDOWN`` (``SDL_EVENT_FINGER_DOWN``)
     - No
     - ``touch_id: int``, ``finger_id: int``, ``x: float``, ``y: float``,
       ``dx: float``, ``dy: float``, ``pressure: float``,
       ``window: Window | None``
     - ``touchId`` and ``fingerId`` are also available, as older names for
       ``touch_id`` and ``finger_id``.
   * - ``FINGERUP`` (``SDL_EVENT_FINGER_UP``)
     - No
     - As for ``FINGERDOWN``.
     - As for ``FINGERDOWN``.
   * - ``FINGERMOTION`` (``SDL_EVENT_FINGER_MOTION``)
     - No
     - As for ``FINGERDOWN``.
     - As for ``FINGERDOWN``.
   * - ``FINGERCANCELED`` (``SDL_EVENT_FINGER_CANCELED``)
     - No
     - As for ``FINGERDOWN``.
     - Not in pygame-ce.
   * - ``PINCHBEGIN`` (``SDL_EVENT_PINCH_BEGIN``)
     - No
     - ``scale: float``, ``window: Window | None``
     - Not in pygame-ce.
   * - ``PINCHUPDATE`` (``SDL_EVENT_PINCH_UPDATE``)
     - No
     - ``scale: float``, ``window: Window | None``
     - Not in pygame-ce.
   * - ``PINCHEND`` (``SDL_EVENT_PINCH_END``)
     - No
     - ``scale: float``, ``window: Window | None``
     - Not in pygame-ce.

Touch positions are normalized, from 0.0 to 1.0 across the window.


Drop Events
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``DROPFILE`` (``SDL_EVENT_DROP_FILE``)
     - No
     - ``file: str | None``, ``x: float``, ``y: float``, ``window_id: int``,
       ``window: Window | None``
     - ``x``, ``y``, and ``window_id`` are not in pygame-ce.
   * - ``DROPTEXT`` (``SDL_EVENT_DROP_TEXT``)
     - No
     - ``text: str | None``, ``file: str | None``, ``x: float``, ``y: float``,
       ``window_id: int``, ``window: Window | None``
     - ``file`` (the same as ``text``), ``x``, ``y``, and ``window_id`` are
       not in pygame-ce.
   * - ``DROPBEGIN`` (``SDL_EVENT_DROP_BEGIN``)
     - No
     - ``file: str | None``, ``x: float``, ``y: float``, ``window_id: int``,
       ``window: Window | None``
     - pygame-ce gives only ``window``.
   * - ``DROPCOMPLETE`` (``SDL_EVENT_DROP_COMPLETE``)
     - No
     - ``file: str | None``, ``x: float``, ``y: float``, ``window_id: int``,
       ``window: Window | None``
     - pygame-ce gives only ``window``.
   * - ``DROPPOSITION`` (``SDL_EVENT_DROP_POSITION``)
     - No
     - ``file: str | None``, ``x: float``, ``y: float``, ``window_id: int``,
       ``window: Window | None``
     - Not in pygame-ce.

``file`` is None when SDL gives no file name or text for the event.


Device, Pen, Camera, and Sensor Events
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``AUDIODEVICEADDED`` (``SDL_EVENT_AUDIO_DEVICE_ADDED``)
     - No
     - ``which: int``, ``iscapture: bool``
     - None
   * - ``AUDIODEVICEREMOVED`` (``SDL_EVENT_AUDIO_DEVICE_REMOVED``)
     - No
     - ``which: int``, ``iscapture: bool``
     - None
   * - ``AUDIODEVICEFORMATCHANGED`` (``SDL_EVENT_AUDIO_DEVICE_FORMAT_CHANGED``)
     - No
     - ``which: int``, ``iscapture: bool``
     - Not in pygame-ce.
   * - ``SENSORUPDATE`` (``SDL_EVENT_SENSOR_UPDATE``)
     - No
     - ``which: int``, ``instance_id: int``,
       ``data: (float, float, float, float, float, float)``
     - Not in pygame-ce.
   * - ``PENPROXIMITYIN`` (``SDL_EVENT_PEN_PROXIMITY_IN``)
     - No
     - ``which: int``, ``window: Window | None``
     - Not in pygame-ce.
   * - ``PENPROXIMITYOUT`` (``SDL_EVENT_PEN_PROXIMITY_OUT``)
     - No
     - ``which: int``, ``window: Window | None``
     - Not in pygame-ce.
   * - ``PENDOWN`` (``SDL_EVENT_PEN_DOWN``)
     - No
     - ``which: int``, ``window: Window | None``, ``pen_state: int``,
       ``x: float``, ``y: float``, ``eraser: bool``, ``down: bool``
     - Not in pygame-ce.
   * - ``PENUP`` (``SDL_EVENT_PEN_UP``)
     - No
     - ``which: int``, ``window: Window | None``, ``pen_state: int``,
       ``x: float``, ``y: float``, ``eraser: bool``, ``down: bool``
     - Not in pygame-ce.
   * - ``PENBUTTONDOWN`` (``SDL_EVENT_PEN_BUTTON_DOWN``)
     - No
     - ``which: int``, ``window: Window | None``, ``pen_state: int``,
       ``x: float``, ``y: float``, ``button: int``, ``down: bool``
     - Not in pygame-ce.
   * - ``PENBUTTONUP`` (``SDL_EVENT_PEN_BUTTON_UP``)
     - No
     - ``which: int``, ``window: Window | None``, ``pen_state: int``,
       ``x: float``, ``y: float``, ``button: int``, ``down: bool``
     - Not in pygame-ce.
   * - ``PENMOTION`` (``SDL_EVENT_PEN_MOTION``)
     - No
     - ``which: int``, ``window: Window | None``, ``pen_state: int``,
       ``x: float``, ``y: float``
     - Not in pygame-ce.
   * - ``PENAXIS`` (``SDL_EVENT_PEN_AXIS``)
     - No
     - ``which: int``, ``window: Window | None``, ``pen_state: int``,
       ``x: float``, ``y: float``, ``axis: int``, ``value: float``
     - Not in pygame-ce.
   * - ``CAMERADEVICEADDED`` (``SDL_EVENT_CAMERA_DEVICE_ADDED``)
     - No
     - ``which: int``
     - Not in pygame-ce.
   * - ``CAMERADEVICEREMOVED`` (``SDL_EVENT_CAMERA_DEVICE_REMOVED``)
     - No
     - ``which: int``
     - Not in pygame-ce.
   * - ``CAMERADEVICEAPPROVED`` (``SDL_EVENT_CAMERA_DEVICE_APPROVED``)
     - No
     - ``which: int``
     - Not in pygame-ce.
   * - ``CAMERADEVICEDENIED`` (``SDL_EVENT_CAMERA_DEVICE_DENIED``)
     - No
     - ``which: int``
     - Not in pygame-ce.


Render Events
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``RENDERTARGETSRESET``, ``RENDER_TARGETS_RESET``
       (``SDL_EVENT_RENDER_TARGETS_RESET``)
     - Yes
     - None
     - None
   * - ``RENDERDEVICERESET``, ``RENDER_DEVICE_RESET``
       (``SDL_EVENT_RENDER_DEVICE_RESET``)
     - Yes
     - None
     - None
   * - ``RENDERDEVICELOST``, ``RENDER_DEVICE_LOST``
       (``SDL_EVENT_RENDER_DEVICE_LOST``)
     - No
     - None
     - Not in pygame-ce.


User and Ren'Py Events
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``USEREVENT``, ``USER`` (``SDL_EVENT_USER``)
     - Yes
     - ``code: int``, or the attributes of a posted event
     - None
   * - ``TIMEEVENT``
     - Yes
     - Internal to Ren'Py.
     - Not in pygame-ce.
   * - ``PERIODIC``
     - Yes
     - Internal to Ren'Py.
     - Not in pygame-ce.
   * - ``REDRAW``
     - Yes
     - Internal to Ren'Py.
     - Not in pygame-ce.
   * - ``EVENTNAME``
     - Yes
     - Internal to Ren'Py.
     - Not in pygame-ce.

Types from ``USEREVENT`` up are never blocked. An event posted with
``pygame.event.post`` is delivered as the same object, with the attributes
it was created with. ``pygame.event.register`` returns a new type, and gives
it the name that ``event_name()`` returns. Ren'Py registers ``TIMEEVENT``,
``PERIODIC``, ``REDRAW``, and ``EVENTNAME`` for its own use, so the events it
posts with these types should not be relied on.


Markers and Obsolete Names
--------------------------

These names never identify an event a game receives.

.. list-table::
   :header-rows: 1
   :widths: 30 10 25 35

   * - Event
     - Default
     - Fields
     - pygame(-ce) differences
   * - ``NOEVENT`` (``SDL_EVENT_FIRST``)
     - n/a
     - None
     - The type of the event ``pygame.event.poll()`` returns when the queue
       is empty.
   * - ``DISPLAYFIRST``, ``DISPLAYLAST``, ``WINDOWFIRST``, ``WINDOWLAST``
     - n/a
     - None
     - The first and last display and window event types. Not in pygame-ce.
   * - ``PRIVATE0``, ``PRIVATE1``, ``PRIVATE2``, ``PRIVATE3``,
       ``POLLSENTINEL``, ``LAST``, ``ENUMPADDING``
     - n/a
     - None
     - Reserved by SDL. Not in pygame-ce.
   * - ``DISPLAYEVENT``, ``WINDOWEVENT``, ``SYSWMEVENT``, ``DOLLARGESTURE``,
       ``DOLLARRECORD``, ``MULTIGESTURE``
     - n/a
     - None
     - SDL 2 event types that SDL 3 removed. These names exist so that code
       using them still loads, but no event has them as its type.
