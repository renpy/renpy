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

Voice Functions
---------------

.. include:: inc/voice

Voice Actions
-------------

.. include:: inc/voice_action

