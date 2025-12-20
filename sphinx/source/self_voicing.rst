.. _self-voicing:

============
Self-Voicing
============

Ren'Py supports a self-voicing mode in which a speech synthesizer is used
to read out text and other interface elements. This is intended to make
Ren'Py games accessible to the vision impaired.

The Self-voicing mode can be toggled by pressing the ``v`` key. Self-voicing
modes can be selected through the accessibility menu, which can be accessed
by pressing `Shift+A.

When in self-voicing mode, keyboard navigation is changed so that the
up and down arrow keys with iterate through all focusable displayables
on the screen.

When a displayable is focused, Ren'Py will read the text associated with that
displayable out loud. If no displayable is focused, Ren'Py will read on-screen
text that cannot be focused. This will generally include dialogue and other
text that comprises the game.

Speech Synthesis
----------------

Ren'Py relies on the operating system to provide speech synthesis
services. To adjust the speed of speech synthesis and the voice used,
adjust your platform's speech settings.

Windows
    On Windows, Ren'Py uses the Microsoft Speech API. Speech synthesis
    settings can be changed on the "Text to Speech" tab of the "Speech
    Recognition" control panel.

Mac OS X
    On Mac OS X, Ren'Py uses the ``say`` command. Speech synthesis settings
    can be changed on the "Text to Speech" tab of the "Dictation & Speech"
    control panel.

Linux
    On Linux, Ren'Py uses the ``espeak`` command. Espeak may need to be
    installed using your package manager before self-voicing mode will
    work.

Android, iOS, Chrome OS
    These use the platform's built-in text-to-speech services.

Web
    This uses the Web Speech API, which is supported by modern browsers.


The default voice can be selected on a per-platform basis, using the
:var:`config.tts_voice` variable. For example::

    init python:

        if renpy.windows:
            config.tts_voice = "Mark"
        elif renpy.macintosh:
            config.tts_voice = "Alex"
        elif renpy.linux:
            config.tts_voice = "english_rp"

The available voice vary based on the platform.

Other Modes
-----------

There are two other modes related to self-voicing.

Clipboard
    Clipboard mode can be toggled by pressing Shift+C. In clipboard
    mode, the text is copied to the clipboard instead of being played
    through TTS. This can be with screen readers or other assistive
    technologies that will present the clipboard contents to the user.

    It may also be useful for translation software that can read from the
    clipboard.

Debug
    Debug mode can be toggled by pressing Shift+Alt+V. In debug mode,
    the text that would be spoken is displayed on the screen, to help
    with development.


Creator Concerns
----------------

Ren'Py's self-voicing works by extracting text from displayables and
reading it to the player. Ren'Py extracts this text from multiple places.

Text displayables
    Ren'Py will extract text from a Text displayable, and make it
    available to be read to the player.

Alternative text
    Alternative text is supplied by a displayable's :propref:`alt` style
    property. It can also be supplied by instances of the :class:`Action`
    and :class:`BarValue` classes.
    Explicitly supplied alternative text takes precedence over text
    supplied by Actions or BarValues, and both take precedence over
    text extracted from Text displayables.

    Alternative text is translated using Ren'Py's string translation
    mechanism. Alternative text takes precedence over text extracted
    from a displayable and its children, but such child text is made
    available as the "[text]" string substitution. No other string
    substitutions are allowed.

    For example::

        screen information(message, planet, badness):
            text message:
                color color_from_badness(badness)
                alt "Information for you : [text]. Badness is " + str(badness)

            text "ORIGIN_OF_MESSAGE_{color=#f00}[planet!u]{/color}":
                alt "Origin of message is " + planet

    In the above example, the ``badness`` and ``planet`` variables
    cannot be substituted directly using "[badness]". Concatenating
    it manually is a solution.

    Supplying the `who_alt` and `what_alt` parameters to Character
    sets the alt style property for the character name and body text,
    respectively. As an example, we define a Character that uses italics
    to indicate thoughts normally, but explicitly indicates thoughts
    via self voicing::

        define thought = Character(None, what_italic=True, what_alt="I think, [text]")

    In screens, displayables may be given the :scpref:`group_alt` property,
    which is used to give a group prefix that is spoken the first time a displayable
    with the same group prefix is focused, but will not be spoken again until a
    displayable with a different group prefix is focused.

    Displayables may also be given the :scpref:`extra_alt` property, which is spoken
    when the '?' key is pressed while the displayable is focused. This is intended
    for more detail information about how a group of controls works.

Descriptive Text
    Descriptive text is text that is displayed (and spoken) by the narrator if
    self-voicing is enabled. The text is not displayed if self-voicing is
    disabled. Self-voicing text uses the :var:`alt` variable, which is defined to
    be similar to a character.

    .. var:: alt = ...

        A character-like object that uses the narrator to speak text if
        self-voicing is enabled.

    For example::

        e "Hang on, this is gonna be a bumpy ride!"

        alt "And then the sun exploded..."

        # A complex and exciting cut scene.
        show event sun_exploding
        pause 10

    There is a variable that controls descriptive text:

    .. var:: config.descriptive_text_character = None

        If not None, this should be a character object that is used to
        display the descriptive text, instead of the narrator.

The :var:`config.tts_substitutions` variable can be used to substitute
words in the text being spoken, to better control pronunciation. The
:var:`config.tts_voice` variable can be used to select the voice used
to speak text from the voices on a platform.

A self-voicing debug mode can be enabled by typing Shift+Alt+V. This will
display the text that would be voiced on the screen for development
purposes.


Python
------

The following functions are provided by the self-voicing system:

.. include:: inc/self_voicing
