Audio
=======

Ren'Py supports playing music and sound effects in the background,
using the following audio file formats

* OPUS
* OGG Vorbis
* MP3
* WAV (uncompressed PCM only)

Ren'Py supports an arbitrary number of audio channels. There are three
normal channels defined by default:

* music - A channel for music playback.
* sound - A channel for sound effects.
* voice - A channel for voice.

Normal channels support playing and queueing audio, but only play back
one audio file at a time. New normal channels can be registered with
:func:`renpy.music.register_channel`.

The 'Music Volume', 'Sound Volume', and 'Voice Volume' settings
of the in-game preferences menu are used to set individual
volumes for these channels.

In addition to the normal channel, there is one special channel, ``audio``.
The audio channel supports playing back multiple audio files at one time,
but does not support queueing sound or stopping playback.

Sounds can also be set to play when buttons, menu choices, or
imagemaps enter their hovered or activated states. See
:ref:`Button Style Properties <button-style-properties>`. Two configuration
variables, :var:`config.main_menu_music` and :var:`config.game_menu_music` allow
for the given music files to be played as the main and game menu music,
respectively.

In-game, the usual way to play music and sound in Ren'Py is using
the three music/sound statements.


Play Statement
------------------

The play statement is used to play sound and music. If a file is
currently playing on a normal channel, it is interrupted and replaced with
the new file.

The name of a channel is expected following keyword ``play``,
(Usually, this is either "sound", "music", "voice", or "audio"). This is
followed by audiofile(s), where audiofile(s) can be one file or list of files.
When the list is given, the item of it is played in order.


The ``fadein`` and ``fadeout`` clauses are optional. Fadeout gives the fadeout
time for currently playing music, in seconds, while fadein gives the time
it takes to fade in the new music. If fadeout is not given, config.fade_music
is used.

The ``loop`` and ``noloop`` clauses are also optional. The loop clause causes
the music to loop, while noloop causes it to play only once. If both of them isn't
given, the default of the channel is used. ::

        play music "mozart.ogg"
        play sound "woof.mp3"
        play myChannel "punch.wav" # 'myChannel' needs to be defined with renpy.music.register_channel().

        "We can also play a list of sounds, or music."
        play music [ "a.ogg", "b.ogg" ] fadeout 1.0 fadein 1.0

On the audio channel, multiple play statements play multiple sounds at the same
time::

        play audio "sfx1.opus"
        play audio "sfx2.opus"


Stop Statement
--------------

The stop statement begin with keyword ``stop``, followed by the the name of a
channel to stop sound on. It may optionally have a ``fadeout``
clause. ::

        stop sound
        stop music fadeout 1.0


Queue Statement
---------------

The queue statement is used to queue up audio files. They will be played when
the channel finishes playing the currently playing file.

The queue statement begin with keyword ``queue``, followed by the the name of a
channel to play sound on. It optionally takes the ``loop`` and ``noloop`` clauses. ::

        queue sound "woof.ogg"
        queue music [ "a.ogg", "b.ogg" ]

The advantage of using these statements is that your program will be checked for
missing sound and music files when lint is run. The functions below exist to allow
access to allow music and sound to be controlled from python, and to expose
advanced (rarely-used) features.


.. _partial-playback:

Partial Playback
----------------

Ren'Py supports partial of audio files. This is done by putting a playback
specification, enclosed in angle brackets, at the start of the file.
The partial playback specification should consist of alternating
property name and value pairs, with every thing separated by spaces.

The values are always interpreted as seconds from the start of the file.
The three properties are:

``from``
    Specifies the position in the file at which the first play-through
    begins playing. (This defaults to 0.0 seconds.)

``to``
    Specifies the position in the file at which the file ends playing.
    (This defaults to the full duration of the file.)

``loop``
    Specifies the position in the file at which the second and later
    play-throughs begin playing. (This defaults to the start time
    given by ``from`` if specified, or to the start of the file.)

For example::

        play music "<from 5 to 15.5>waves.opus"

Will play 10.5 seconds of waves.opus, starting at the 5 second mark. The statement::

        play music "<loop 6.333>song.opus"

Will play song.opus all the way through once, then loop back to the 6.333
second mark before playing it again all the way through to the end.

.. _silence:

Playing Silence
---------------

A specified duration of silence can played using a filename like
"<silence 3.0>", where 3.0 is the number of seconds of silence that is
desired. This can be used to delay the start of a sound file. For example::

        play audio [ "<silence .5>", "boom.opus" ]

Will play silence for half a second, and then an explosion sound.


.. _audio-namespace:

Audio Namespace
---------------

The ``play`` and ``queue`` statements evaluate their arguments in the
audio namespace. This means it is possible to use the define statement
to provide an alias for an audio file.

For example, one can write::

    define audio.sunflower = "music/sun-flower-slow-jam.ogg"

and then use::

    play music sunflower


Functions
---------

.. include:: inc/audio


Sound Functions
---------------

Most renpy.music functions have aliases in renpy.sound. These functions are similar,
except they default to the sound channel rather than the music channel, and default
to not looping.
