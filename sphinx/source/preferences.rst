====================
Preference Variables
====================

Preference variables store the values of Ren'Py preferences. While the value
of a preference should be set at runtime using the :func:`Preference` action,
preference variables should be used in conjunction with the default statement
to set the default value of a preference.

For example::

    default preferences.text_cps = 40

sets the default text speed to 40 characters per second. The default statement
only sets the value of the preference if the default has changed since the
preference was set. For example, if the player changes the speed to 50,
it will remain at 50 over future runs of the game. If, in an upgrade, the
default is set to 42, the player's setting will be changed to 42. (The player
can then change it again.)

.. var:: preferences.afm_after_click = False

    If True, the auto-forward mode will be continued after a click. If False,
    a click will end auto-forward mode. The equivalent of the "auto-forward
    after click" preference.

.. var:: preferences.afm_enable = False

    If True, auto-forward move is enabled, otherwise False. The equivalent
    of the "auto-forward time" preference.

.. var:: preferences.afm_time = 15

    The amount of time to wait for auto-forward mode. Bigger numbers are
    slower, though the conversion to wall time is complicated, as the
    speed takes into account line length. The equivalent of the
    "auto-forward" preference.

.. var:: preferences.desktop_rollback_side = "disable"

    When on a desktop platform, touches or clicks to this side of the window
    cause rollback to occur. One of "left", "right", or "disable". This is
    the equivalent of the "rollback side" preference when on a desktop
    platform.

.. var:: preferences.mobile_rollback_side = "disable"

    When on a mobile platform, touches or clicks to this side of the window
    cause rollback to occur. One of "left", "right", or "disable". This is
    the equivalent of the "rollback side" preference when on a mobile
    platform.

.. var:: preferences.language = None

    The language that the player has selected to use when running the game.
    This is None for the default language or a string containing a language
    the game is translated to.

    This can be used to set the default language, and can be read to determine
    the current language. The :func:`Language` action can be used to change
    the language.

    See :doc:`translation` for more information.

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

.. var:: preferences.gl_powersave = True

    This determines how often Ren'Py will redraw an unchanging screen. If True,
    Ren'Py will only draw the screen 5 times a second. If False, it will always
    draw at the full framerate possible.

.. var:: preferences.gl_tearing = False

    This determines if tearing (True) or frameskip (False) is the preferred
    behavior when the game can't keep up with its intended framerate.

.. var:: preferences.mouse_move = True

    If True, the mouse will automatically move to a selected button. If False,
    it will not. The equivalent of the "automatic move" preference.

.. var:: preferences.show_empty_window = True

    If True, the window show and window auto statements will function. If
    False, those statements are disabled. The equivalent of the "show empty window"
    preference.

.. var:: preferences.skip_after_choices = False

    If True, skipping will resume after a choice. If False, a choice will
    prevent Ren'Py from skipping. The equivalent of the "after choices"
    preference.

.. var:: preferences.skip_unseen = False

    When True, Ren'Py will skip all text. When False, Ren'Py will
    only skip text that has been read by the player in any session.
    The equivalent of the "skip" preference.

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

.. var:: preferences.system_cursor = False

    If True, the system cursor is forced to be used, ignoring the value of
    :var:`config.mouse` and :var:`config.mouse_displayable`. If False, it
    will not. The equivalent of the "system cursor" preference.

.. var:: preferences.audio_when_minimized = True

    If False, audio channels are stopped when the window is minimized,
    and resumed when the window is restored. If True, window state will
    have no effect on audio.
    The equivalent of the "audio when minimized" preference.

.. var:: preferences.audio_when_unfocused = True

    If False, audio channels are stopped when the window loses keyboard focus,
    and resumed when the window regains keyboard focus. If True, keyboard focus
    will have no effect on audio.
    The equivalent of the "audio when unfocused" preference.

.. var:: preferences.web_cache_preload = False

    If True the game files will be loaded into the web browser's cache,
    allowing the game to be played offline. If False, the game files will
    not be loaded into the web browser's cache, and the game will require
    internet access to play.
    The equivalent of the "web cache preload" preference.

.. var:: preferences.voice_after_game_menu = False

    If True, voice will continue playing after the game menu is shown. If False,
    voice will be stopped when the game menu is shown. The equivalent of the
    "voice after menu" preference.

.. var:: preferences.restore_window_position = True

    If True, Ren'Py will attempt to restore the window position when the game
    is restarted. If False, Ren'Py will not attempt to restore the window
    position. The equivalent of the "restore window position" preference.

.. var:: preferences.force_mono = False

    If True, Ren'Py will mix stereo audio to mono before playing it. If False,
    stereo audio will be played normally.


.. _mixer-defaults:

Mixer Defaults
--------------

These variables may only be set with the ``default`` statement.

.. var:: preferences.volume.main = 1.0

    The default volume of the main mixer, which is applied to all channels in
    addition to the per-channel mixer.This should be a number between 0.0 and 1.0, with 1.0 being full volume.

.. var:: preferences.volume.music = 1.0

    The default volume of the music mixer, which is used for the music and
    movie channels. This should be a number between 0.0 and 1.0,
    with 1.0 being full volume.

.. var:: preferences.volume.sfx = 1.0

    The default volume of the sfx mixer, which is used for the sound and
    audio channels. This should be a number between 0.0 and 1.0,
    with 1.0 being full volume.

.. var:: preferences.volume.voice = 1.0

    The default volume of the voice mixer, which is used for the voice
    channel (and hence the voice statement, auto-voice, etc.).
    This should be a number between 0.0 and 1.0, with 1.0 being full volume.

If channels defined using :func:`renpy.music.register_channel` are used, the
default volume of those channels can be set using the preferences.volume.`mixer`
syntax, where `mixer` is the name of the mixer.

As an example, this will set the music mixer to 75% and the sfx mixer to 50%::

    default preferences.volume.music = 0.75
    default preferences.volume.sfx = 0.5


Mixer Functions
---------------

See :ref:`volume` for more details about mixers.

.. function:: preferences.set_mixer(mixer, volume)

    Sets `mixer` to `volume`.

    `mixer`
        A string giving the name of the mixer. By default, the mixers
        are "main", "music", "sfx", and "voice" ("main" being a special mixer).

    `volume`
        A number between 0.0 and 1.0, where 0.0 is -40 dB (power), and 1.0 is 0 dB
        (power).

.. function:: preferences.get_mixer(mixer)

    Gets the volume for `mixer`. If the mixer is muted, this returns
    0.0. The is returns a number between 0.0 and 1.0, where 0.0 is -40 dB
    (power) and 1.0 is 0 dB (power).

.. function:: preferences.set_mute(mixer, mute)

    Sets the mute setting for `mixer`. If `mute` is true, the mixer is muted.
    If `mute` is false, the mixer's volume is reverted to its value before
    it was muted.

.. function:: preferences.get_mute(mixer)

    Gets the mute setting for `mixer`.
