.. _preference-variables:

====================
Preference Variables
====================

Preference variables store the values of Ren'Py preferences. While the value
of a preference should be set at runtime using the :func:`Preference` action,
preference variables should be used in conjuction with the default statement
to set the default value of a preference.

For example::

    default preferences.text_cps = 142

sets the default text speed to 40 characters per second. The default statement
only sets the value of the preference if the default has changed since the
preference was set. For example, if the player changes the speed to 50,
it will remain at 50 over future runs of the game. If, in an upgrade, the
default is set to 42, the player's setting will be changed to 42. (The player
can then change it again.)

.. var:: preferences.afm_after_click = False

    If True, auto-forward move will be continue after a click. If False,
    a click will end auto-forward mode. The equivalent of the
    "auto-forward after click" preference.

.. var:: preferences.afm_time = 15

    The amount of time to wait for auto-forward mode. Bigger numbers are
    slower, though the conversion to wall time is complicated, as the
    speed takes into account line length. The equivalent of the
    "auto-forward" preference.

.. var:: preferences.desktop_rollback_side = "disable"

    When on a desktop platform, touches or clicks to this side of the window
    cause rollback to occur. One of "left", "right", or "disable". This is
    the equivalend of the "rollback side" preference when on a desktop
    platform.

.. var:: preferences.desktop_rollback_side = "disable"

    When on a desktop platform, touches or clicks to this side of the window
    cause rollback to occur. One of "left", "right", or "disable". This is
    the equivalend of the "rollback side" preference when on a desktop
    platform.

.. var:: preferences.emphasize_audio = False

    If True, Ren'Py will emphasize the audio channels found in :var:`config.emphasize_audio_channels`
    by reducing the volume of other channels. (For example, reducing the music volume when voice
    is playing.) If False, this doesn't happen.

.. var:: preferences.fullscreen = False

    This is True when Ren'Py is in fullscreen mode, and False when it
    is running in a window. The equivalent of the "display" preference.

.. var:: preferences.gl_framerate = None

    This is either an integer, or None. If not None, it's a target framerate
    that Ren'Py will attempt to achieve. If this is set low (for example, to
    30), on a monitor with a high framerate (say, 60 frames per second),
    Ren'Py will only draw on every other frame.

    If None, Ren'Py will attempt to draw at the monitor's full framerate.

.. var:: preferences.gl_powersave = "auto"

    This determines how often Ren'Py will redraw an unchanging screen. If True,
    Ren'Py will only draw the screen 5 times a second. If False, it will always
    draw at the full framerate possible. If "auto", it will draw at full speed
    when the device is powered, and 5hz when it is running on battery.

.. var:: preferences.gl_tearing = False

    This determines if tearing (True) or frameskip (False) is the preferred
    behavior when the game can't keep up with its intended framerate.

.. var:: preferences.mouse_move = False

    If True, the mouse will automatically move to a selected button. If False,
    it will not. The equivalent of the "automatic mouse move" preference.

.. var:: preferences.show_empty_window = True

    If True, the window show and window auto statements will function. If
    False, those statements are disabled. The equivalent of the "show empty window"
    preference.

.. var:: preferences.skip_after_choices = False

    If True, skipping will resume after a choice. If False, a choice will
    prevent Ren'Py from skipping. The equivalent of the "after choices"
    preference.

.. var:: preferences.skip_unseen = False

    When True, Ren'Py will only skip unseen text. When False, Ren'Py will
    skip all text. The equivalent of the "skip" preference.

.. var:: preferences.text_cps = 0

    The speed of text display. 0 is infinite, otherwise this is the number
    of characters per second to show. The equivalent of the "text speed"
    preference.

.. var:: preferences.transitions = 2

    Determines which transitions should be shown. 2 shows all transitions,
    0 shows no transitions. (1 is reserved.) The equivalent of the
    "transitions" preference.

.. var:: preferences.video_image_fallback = False

    If True, images are displayed instead of videosprites. If False,
    video sprites are displayed normally. The equivalent (inverted) of the
    "video sprites" preference.

.. var:: preferences.voice_sustain = False

    If True, voice keeps playing until finished, or another voice line
    replaces it. If False, the voice line ends when the line of dialogue
    advances. The equivalent of the "voice sustain" preference.

.. var:: preferences.wait_voice = True

    If True, auto-forward mode will wait for voice files and self-voicing to
    finish before advancing. If False, it will not. The equivalent of the
    "wait for voice" preference.



Audio Channel Defaults
-----------------------

These config variables set the default volumes on various audio mixers.

.. var:: config.default_music_volume = 1.0

    The default volume of the music mixer, which is used for the music and
    movie audio channels. This should be a number between 0.0 and 1.0,
    with 1.0 being full volume.

.. var:: config.default_sfx_volume = 1.0

    The default volume of the sfx mixer, which is used for the sound
    audio channel. This should be a number between 0.0 and 1.0,
    with 1.0 being full volume.

.. var:: config.default_voice_volume = 1.0

    The default volume of the voice mixer, which is used for the voice
    audio channel (And hence the voice statement, auto-voice, etc.).
    This should be a number between 0.0 and 1.0, with 1.0 being full volume.
