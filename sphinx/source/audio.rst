Audio
=======

Ren'Py supports playing music and sound effects in the background,
using the following audio file formats

* OGG Vorbis
* MP3
* WAV (uncompressed PCM only)

Ren'Py supports an arbitrary number of audio channels.
Three are defined by default:

* music - A channel for music playback.
* sound - A channel for sound effects.
* voice - A channel for voice.

New channels can be registeres with :func:`renpy.register_channel`.

The 'Music Volume', 'Sound Volume', and 'Voice Volume' settings
of the in-game preferences menu are used to set individual
volumes for these channels.

Sounds can also be set to play when buttons, menu choices, or
imagemaps enter their hovered or activated states. See
:ref:`Button Style Properties <button-style-properties>`. Two configuration
variables, :var:`config.main_menu_music` and :var:`config.game_menu_music` allow
for the given music files to be played as the main and game menu music,
respectively.

In-game, the usual way to play music and sound in Ren'Py is using
the three music/sound statements.

The Play Statement
------------------

The play statement is used to play sound and music. If a file is
currently playing, it is interrupted and replaced with the new file.

The name of a channel is expected following keyword ``play``,
(Usually, this is either "sound", "music", or "voice"). This is
followed by audiofile(s), where audiofile(s) can be one file or list of files.

The ``fadein`` and ``fadeout`` clauses are optional. Fadeout gives the fadeout
time for currently playing music, in seconds, while fadein gives the time
it takes to fade in the new music. If fadeout is not given, config.fade_music
is used.

The ``loop`` and ``noloop`` clauses are also optional. The loop clause causes
the music to loop, while noloop causes it to play only once. If both of them isn't
given the default of the channel is used. ::

        play music "mozart.ogg"
        play sound "woof.mp3"
        play myChannel "punch.wav" # 'myChannel' needs to be defined with renpy.music.register_channel().

        "We can also play a list of sounds, or music."
        play music [ "a.ogg", "b.ogg" ] fadeout 1.0 fadein 1.0

Stop Statement
--------------

The stop statement begin with keyword ``stop``, followed by the the name of a
channel to stop sound on. It may optionally have a ``fadeout``
clause. ::

        stop sound
        stop music fadeout 1.0

Queue Statement
---------------

The queue statement begin with keyword ``queue``, followed by the the name of a
channel to stop sound on. It optionally takes the ``loop`` and ``noloop`` clauses. ::

        queue sound "woof.ogg"
        queue music [ "a.ogg", "b.ogg" ]

The advantage of using these statements is that your program will be checked for
missing sound and music files when lint is run. The functions below exist to allow
access to allow music and sound to be controlled from python, and to expose
advanced (rarely-used) features.


Functions
---------

.. include:: inc/audio

Sound Functions
---------------

Most renpy.music functions have aliases in renpy.sound. These functions are similar,
except they default to the sound channel rather than the music channel, and default to not looping.
