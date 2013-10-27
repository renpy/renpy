Environment Variables
=====================

The following environment variables control the behavior of Ren'Py:

``RENPY_SCALE_FACTOR``
    If set, this is parsed as a floating point number, and the display screen
    is scaled by that amount. For example, if RENPY_SCALE_FACTOR is set to "0.5",
    everything is half normal size.

``RENPY_SCALE_FAST``
    If set and Ren'Py starts scaling the display screen, the display screen
    will use nearest-neighbor filtering rather than slower but higher-quality
    bilinear filtering. It should generally be unnecessary to set this.

``RENPY_DISABLE_JOYSTICK``
    If set, joystick detection is disabled. Use this if a faulty joystick is
    causing Ren'Py to advance when not desired.

``RENPY_DISABLE_FULLSCREEN``
    If set, Ren'Py will refuse to go into fullscreen mode.

``RENPY_DISABLE_SOUND``
    This prevents sound playback from occuring. If this variable contains
    "pss", sound playback will be disabled. If it contains "mixer", volume control
    will be disabled. A value of "pss,mixer" will disable both.

``RENPY_SOUND_BUFSIZE``
    This controls the sound buffer size. Values larger than the default (2048)
    can prevent sound from skipping, at the cost of a larger delay from when a
    sound is invoked to when it is played.

``RENPY_NOMIXER``
    If set, prevents Ren'Py from trying to control the system audio mixer.

``RENPY_EDITOR``
    The default value of :var:`config.editor`.

``RENPY_EDITOR_FILE_SEPARATOR``
    The default value of :var:`config.editor_file_separator`.

``RENPY_EDITOR_TRANSIENT``
    The default value of :var:`config.editor_transient`.

``RENPY_SCREENSHOT_PATTERN``
    A pattern used to create screenshot filenames. It should contain a single
    %d substitution in it. For example, setting this to "screenshot%04d.jpg" will
    cause Ren'Py to write out jpeg screenshots rather than the usual pngs.

``RENPY_LESS_MEMORY``
    This causes Ren'Py to reduce its memory usage, in exchange for reductions
    in speed.

``RENPY_LESS_UPDATES``
    This causes Ren'Py to reduce the number of screen updates that occur.

``RENPY_LESS_MOUSE``
    This causes Ren'Py to disable the mouse at all times.

``RENPY_BASE``
    This environment variable is exported by Ren'Py to processes run by it. It
    contains the full path to the directory containing renpy.exe, renpy.sh, or
    renpy.app.


As Ren'Py uses SDL, its behavior can also be controlled by the SDL environment
variables.

At startup, Ren'Py will look in the Ren'Py directory (the one containing
renpy.exe or renpy.py) for the file "environment.txt". If it exists, it will be
evaluated as a python file, and the values defined in that file will be used as
the default values of environment variables.
