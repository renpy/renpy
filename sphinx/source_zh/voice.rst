=====
Voice
=====

Ren'Py includes support for playing back voice in conjunction with
dialogue. This is done through the voice statement, which gives the
voice filename to play::

  voice "line0001.ogg"
  "Welcome to Ren'Py"

Normally, a playing voice is stopped at the start of the next
interaction. The voice sustain statement can sustain voice playback
through an interaction. ::

  voice "line0001.ogg"
  "Welcome to Ren'Py..."

  voice sustain
  "... your digital storytelling engine."

The :var:`config.voice_filename_format` variable allows you to customize
the voice filename, making it possible to omit directories and extensions.

Voice Tags
----------

Ren'Py includes a voice tag system that makes it possible to selectively
mute or unmute a character's voice. To take advantage of this system,
supply a voice_tag argument to each :func:`Character`, and use the
:func:`SetVoiceMute` or :func:`ToggleVoiceMute` actions to allow the
player to toggle the voice.

For example::

  define e = Character("Eileen", voice_tag="eileen")
  define l = Character("Lucy", voice_tag="lucy")

  screen voice_toggle:
      vbox:
          textbutton "Mute Eileen" action ToggleVoiceMute("eileen")
          textbutton "Mute Lucy" action ToggleVoiceMute("lucy")

  label start:
      show screen voice_toggle

      voice "e01.ogg"
      e "You can turn a character's voice on and off."

      voice "l01.ogg"
      l "Yeah! Now I can finally shut you up!"

      voice "l02.ogg"
      l "Wait... that means they can mute me as well! Really?"

.. _automatic-voice:

Automatic Voice
---------------

Ren'Py includes support for automatically determining the voice file to play,
making it possible to play back voice without having to put voice statements
before each line of dialogue.

This is done by creating voice files that match the identifier for each line
of dialogue. To determine the identifiers to use , first export the dialogue
to a spreadsheet by choosing from the launcher "Extract Dialogue", "Tab-delimited
Spreadsheet (dialogue.tab)", and "Continue". This will produce a file, dialogue.tab,
that can be loaded in a spreadsheet program.

The first column of the spreadsheet is the identifier to use, with other
columns giving more information about the dialogue.

To make Ren'Py automatically play voices, set :var:`config.auto_voice` to
a string containing `{id}`. When dialogue occurs, `{id}` is replaced with
the dialogue identifier, forming a filename. If the filename exists, it is
played.

For example, if we have::

    config.auto_voice = "voice/{id}.ogg"

And the dialogue identifier is ``demo_minigame_03fc91ef``, then when
the corresponding line is shown, Ren'Py will look for the file
``voice/demo_minigame_03fc91ef.ogg``. If the file exists, Ren'Py will
play it.


Voice Functions
---------------

.. include:: inc/voice

Voice Actions
-------------

.. include:: inc/voice_action

