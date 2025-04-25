Environment Variables
=====================

Ren'Py accepts a number of environment variables that influence its behavior.
These environment variables may disappear or change between Ren'Py releases.

The following environment variables control the behavior of Ren'Py:

``RENPY_DEBUG_SOUND``
    If set, Ren'Py will generate exceptions when audio errors occur.

``RENPY_DISABLE_JOYSTICK``
    If set, joystick detection is disabled. Use this if a faulty joystick is
    causing Ren'Py to advance when not desired.

``RENPY_DISABLE_FULLSCREEN``
    If set, Ren'Py will refuse to go into fullscreen mode.

``RENPY_DISABLE_SOUND``
    This prevents sound playback from occurring. If this variable contains
    "pss", sound playback will be disabled.

``RENPY_DRAWABLE_RESOLUTION_TEXT``
    If set to 0, Ren'Py will not use draw text at the screen's resolution.

``RENPY_EDIT_PY``
    The path to an .edit.py file telling Ren'Py how to invoke a text editor.
    See :doc:`editor` for more information.

``RENPY_GL_ENVIRON``
    Sets the OpenGL texture environment.

``RENPY_GL_RTT``
    Sets the OpenGL render-to-texture method.

``RENPY_GL_VSYNC``
    This determines if Ren'Py will attempt to synchronize with the display's
    vertical refresh. (This prevents tearing, at the cost of potentially
    lowering framerate.) Set this to "0" to disable synchronization, or
    "1" to sync to every vertical refresh.

``RENPY_LANGUAGE``
    If set, gives the translation language Ren'Py will use.

``RENPY_LESS_MEMORY``
    This causes Ren'Py to reduce its memory usage, in exchange for reductions
    in speed.

``RENPY_LESS_MOUSE``
    This causes Ren'Py to disable the mouse at all times.

``RENPY_LESS_PAUSES``
    This causes Ren'Py to disable the pauses created by the {p} and {w}
    text tags.

``RENPY_LESS_UPDATES``
    This causes Ren'Py to reduce the number of screen updates that occur.

``RENPY_LOG_EVENTS``
    If set, Ren'Py will log pygame-style events to the log.txt file. This will hurt performance, but might be
    useful for debugging certain problems.

``RENPY_MULTIPERSISTENT``
    The path to a directory where Ren'Py stores multipersistent data.

``RENPY_NO_STEAM``
    If present in the environment, Ren'Py will not initialize Steamworks.

``RENPY_OPEN_FILE_ENCODING``
    Sets the default encoding for :func:`renpy.open_file`. This is mostly
    used to help Python 2 games run on Python 3 based versions of Ren'Py
    try "utf-8" and "latin-1" to see if it helps a those games run. (But
    remember to set this back for newer games.)

``RENPY_PATH_TO_SAVES``
    The path to a directory where Ren'Py stores it's saves. The actual saves
    for a game are stored in a game-specific path underneath this directory.

``RENPY_SCREENSHOT_PATTERN``
    A pattern used to create screenshot filenames. It should contain a single
    %d substitution in it. For example, setting this to "screenshot%04d.jpg" will
    cause Ren'Py to write out jpeg screenshots rather than the usual pngs.

``RENPY_SEARCHPATH``
    If set, a double-colon (\:\:) separated list of additional paths that
    are added to :var:`config.searchpath`.

``RENPY_SIMPLE_EXCEPTIONS``
    When set, this disables Ren'Py's graphical exception handling.

``RENPY_SKIP_MAIN_MENU``
    When set, skips the main menu.

``RENPY_SKIP_SPLASHSCREEN``
    When set, skips the splashscreen.

``RENPY_SOUND_BUFSIZE``
    This controls the sound buffer size. Values larger than the default (2048)
    can prevent sound from skipping, at the cost of a larger delay from when a
    sound is invoked to when it is played.

``RENPY_TIMEWARP``
    This can be set to make time run faster or slower. For example, setting
    a timewarp of 0.5 makes things run at half-speed, while a timewarp of
    2.0 makes everything run at twice normal speed.

``RENPY_USE_DRAWABLE_RESOLUTION``
    If set to 0, Ren'Py will perform certain operations (including dissolve
    transforms and text rendering) at the game's virtual resolution rather
    than the screen's native resolution.

``RENPY_VARIANT``
    This should be set to a space-separated list of screen variants that
    Ren'Py is expected to use.

As Ren'Py uses SDL, its behavior can also be controlled by the SDL environment
variables.

At startup, Ren'Py will look in the Ren'Py directory (the one containing
renpy.exe or renpy.py) for the file :file:`environment.txt`. If it exists, it will be
evaluated as a Python file, and the values defined in that file will be used as
the default values of environment variables.
