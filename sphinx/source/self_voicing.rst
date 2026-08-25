.. _self-voicing:

============
Self-Voicing
============

Ren'Py supports a self-voicing mode in which a speech synthesizer is used
to read out text and other interface elements. This is intended to make
Ren'Py games accessible to the vision impaired.

The Self-voicing mode can be toggled by pressing the ``v`` key. Self-voicing
modes can be selected through the accessibility menu, which can be accessed
by pressing ``Shift+A``.

When in the ``Shift+A`` accessibility menu, the ``R`` key resets the self-voicing settings
to the default values, then enables self-voicing. This can be used to reset the self-voicing
settings if the user has changed them to a state that makes self-voicing unusable.

When in self-voicing mode, keyboard navigation is changed so that the
up and down arrow keys with iterate through all focusable displayables
on the screen.

When a displayable is focused, Ren'Py will read the text associated with that
displayable out loud. If no displayable is focused, Ren'Py will read on-screen
text that cannot be focused. This will generally include dialogue and other
text that comprises the game.

Speech Synthesis
----------------

Ren'Py generally uses speech synthesizers provided by the operating system and web browser.
Linux is the exception - the ``espeak-ng`` command must be installed for self-voicing
to work on Linux.

The voice may be selected through the accessibility menu, which uses the :func:`renpy.get_tts_voices` function to
list available voices and :func:`Preference` to set the voice. The precise list of available voices is platform
and computer dependent.

On most platforms, Ren'Py relies on the operating system to provide speech synthesis
services. To adjust the speed of speech synthesis and the voice used,
adjust your platform's speech settings.

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

Text Tags
    There are two text tags that are useful for self-voicing. The :tt:`alt` tag is to provide alternative text that is heard
    but not seen, and the :tt:`noalt` tag lets you provide text that is seen but not heard. For example::

        p "My name is {noalt}Cholmondeley{/noalt}{alt}Chumley{/alt}."

The :var:`config.tts_substitutions` variable can be used to substitute
words in the text being spoken, to better control pronunciation. The
voice can be selected through the accessibility menu (Shift+A), as can its speed. The voice is stored
in :var:`preferences.tts_voice`. Te speed of self-voicing is stored in :var:`preferences.tts_speed`.

A self-voicing debug mode can be enabled by typing Shift+Alt+V. This will
display the text that would be voiced on the screen for development
purposes.


Python
------

The following functions are provided by the self-voicing system:

.. include:: inc/self_voicing

.. _text-events:

Text Events
-----------

Ren'Py can stream the text it shows on the screen to other programs, so that
a text-to-speech engine, a live translator, or a streaming overlay can react
to what the game is showing without having to read the screen. This is
separate from self-voicing, and works whether or not self-voicing is on.

The stream is off by default. It's turned on by setting
:var:`config.text_events_port`, or by running the game with the
``RENPY_TEXT_EVENTS_PORT`` environment variable set to a port number. Ren'Py
then listens on that port on 127.0.0.1, and any number of programs can
connect to it. Ren'Py only writes to the connection; it never reads from it,
and a program that stops reading is disconnected rather than allowed to stall
the game.

Each line Ren'Py writes is one JSON object. When the text on the screen
changes, Ren'Py writes an ``interaction`` record, followed by one ``text``
record for each piece of text on the screen, in the order self-voicing would
read them (front to back). When the focus changes, it writes a ``focus``
record for the focused displayable. ::

    {"kind": "interaction", "image_tag": "eileen", "id": 12, "interaction": 4}
    {"kind": "text", "role": "who", "style": "say_label", "text": "Eileen", "id": 13, "interaction": 4}
    {"kind": "text", "role": "what", "style": "say_dialogue", "text": "Hi! My name is Eileen.", "id": 14, "interaction": 4}
    {"kind": "text", "role": "quick_menu", "style": "quick_button", "text": "Back", "id": 15, "interaction": 4}
    {"kind": "focus", "role": "choice", "style": "choice_button", "text": "To ask her right away.", "id": 16, "interaction": 4}

``id`` goes up with every record. ``interaction`` goes up each time the set
of text on the screen changes, so a tool can tell which records belong
together. ``image_tag`` is the image tag of the speaking character, if there
is one.

``role`` comes from :var:`config.text_events_roles`, which maps style names
to roles; the default covers the styles the default screens use, giving
``who``, ``what``, ``choice``, ``quick_menu``, ``navigation``, ``input``,
and ``notify``. When no style in the chain is in the map, the role is the name
of the style itself. ``style`` is always the name of the displayable's own
style, for tools that need more detail than the role gives.

The text is given as self-voicing would speak it: text tags are removed,
``{alt}`` text is used where it's present, and a displayable with the
:propref:`alt` style property contributes that text instead of its children.
