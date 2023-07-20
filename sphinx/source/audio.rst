.. _audio:

Audio
=====

Ren'Py supports playing music and sound effects in the background,
using the following audio file formats:

* Opus
* Ogg Vorbis
* MP3
* MP2
* FLAC
* WAV (uncompressed 16-bit signed PCM only)

On the web browser, Ren'Py will check a list of audio formats, and
enable a mode that is faster and less prone to skipping if the web
browser supports all modes on the list. If your game is using only
mp3s, and skips on Safari, then consider changing :var:`config.webaudio_required_types`.

Ren'Py supports an arbitrary number of audio channels. There are three
normal channels defined by default:

* ``music`` - A channel for music playback.
* ``sound`` - A channel for sound effects.
* ``voice`` - A channel for voice.

Normal channels support playing and queueing audio, but only play back
one audio file at a time. New normal channels can be registered with
:func:`renpy.music.register_channel`.

The Music Volume, Sound Volume, and Voice Volume settings
of the in-game preferences menu are used to set individual
volumes for these channels. See :ref:`volume` for more information.

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

.. _play-statement:

Play Statement
--------------

The ``play`` statement is used to play sound and music. If a file is
currently playing on a normal channel, it is interrupted and replaced with
the new file.

The name of a channel is expected following the keyword ``play``.
(Usually, this is either "sound", "music", "voice", or "audio"). This is
followed by audiofile(s), where audiofile(s) can be one file or list of files.
When the list is given, the item of it is played in order.


The ``fadein`` and ``fadeout`` clauses are optional. Fadeout gives the fadeout
time for currently playing music, in seconds, while fadein gives the time
it takes to fade in the new music. If fadeout is not given, :var:`config.fadeout_audio`
is used.

The ``loop`` and ``noloop`` clauses are also optional. The loop clause causes
the music to loop, while noloop causes it to play only once. If neither of them are
given, the default of the channel is used. ::

        play music "mozart.ogg"
        play sound "woof.mp3"
        play myChannel "punch.wav" # 'myChannel' needs to be defined with renpy.music.register_channel().

        "We can also play a list of sounds, or music."
        play music [ "a.ogg", "b.ogg" ] fadeout 1.0 fadein 1.0

When the ``if_changed`` clause is provided, and if the given track is currently playing
on the channel, the play instruction doesn't interrupt it. ::

        label market_side:
            play music market
            "We're entering the market."
            jump market_main

        label market_main:
            play music market if_changed
            "Maybe we just entered the market, maybe we were already there."
            "If we were already there, the music didn't stop and start over, it just continued."
            jump market_main

The ``volume`` clause is also optional, and specifies a relative volume for
the track, between 0.0 and 1.0. This makes it possible to adjust the volume a
track is played at, each time it's played. ::

        play sound "woof.mp3" volume 0.5


On the audio channel, multiple play statements play multiple sounds at the same
time::

        play audio "sfx1.opus"
        play audio "sfx2.opus"

A variable may be used instead of a string here. If a variable exists in the
:ref:`audio namespace <audio-namespace>`, it's used in preference to the default namespace::

        play music illurock

Files placed into the audio namespace may automatically define variables that can
be used like this.

Stop Statement
--------------

The ``stop`` statement begins with the keyword ``stop``, followed by the the name of a
channel to stop sound on. It may optionally have a ``fadeout`` clause. If the
fadeout clause is not given, :var:`config.fadeout_audio` is used. ::

        stop sound
        stop music fadeout 1.0


Queue Statement
---------------

The ``queue`` statement is used to queue up audio files. They will be played when
the channel finishes playing the currently playing file.

The queue statement begins with keyword ``queue``, followed by the the name of a
channel to play sound on. It optionally takes the ``fadein``, ``loop`` and ``noloop`` clauses. ::

        queue sound "woof.mp3"
        queue music [ "a.ogg", "b.ogg" ]

Queue also takes the ``volume`` clause. ::

        play sound "woof.mp3" volume 0.25
        queue sound "woof.mp3" volume 0.5
        queue sound "woof.mp3" volume 0.75
        queue sound "woof.mp3" volume 1.0

When multiple queue statements are given without an interaction between them,
all sound files are added to the queue. After an interaction has occurred, the
first queue statement clears the queue, unless it has already been cleared by
a play or stop statement.

A variable may be used instead of a string here. If a variable exists in the
:ref:`audio namespace <audio-namespace>`, it's used in preference to the default namespace::

    define audio.woof = "woof.mp3"

    # ...

    play sound woof

The advantage of using these statements is that your program will be checked for
missing sound and music files when lint is run. The functions below exist to allow
access to allow music and sound to be controlled from Python, and to expose
advanced (rarely used) features.


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

will play 10.5 seconds of waves.opus, starting at the 5 second mark. The statement::

        play music "<loop 6.333>song.opus"

will play song.opus all the way through once, then loop back to the 6.333
second mark before playing it again all the way through to the end.

.. _sync-start:

Sync Start Position
-------------------

The position in the file at which the clip begins playing can also be synced to
another channel with a currently-playing track using a filename like
"<sync channelname>track.opus", where channelname is the name of the channel,
which could be music, sound, or any other registered channels.

This can be used to sync multi-layered looping tracks together. For example::

        play music_2 [ "<sync music_1>layer_2.opus", "layer_2.opus" ]

Will play layer_2.opus with the start time synced to the current track in
channel music_1 in the first iteration, before playing the whole track in
subsequent iterations. (By default, the layer_2.opus start time will remain
modified even in subsequent iterations in the loop.)

.. _volume:

Volume
------

The volume at which a given track is going to be played depends on a number
of variables:

- the "main" mixer's volume
- the volume of the mixer which the channel relates to
- the volume of the channel
- the relative volume of the track itself

These four volumes are values between 0 and 1, and their multiplication results
in the volume the track will be played at.

For example, if the main volume is 80% (or 0.8), the mixer's volume is 100%,
the channel volume is 50% (0.5) and the track's relative volume is 25% (0.25),
the resulting volume is .8\*1.\*.5\*.25 = .1, so 10%.

The mixers' volumes can be set using :func:`preferences.set_mixer`, using the
:func:`SetMixer` action, or using the :func:`Preference` action with the
``"mixer <mixer> volume"`` key.
The "audio" and "sound" channels relate to the "sfx" mixer, the "music" channel
to the "music" mixer and the "voice" channel to the "voice" mixer.
Every channel additionally relates to the "main" mixer, as shown above.

A channel's volume can be set using :func:`renpy.music.set_volume`. It is only
useful when several channels use the same mixer. The ``mixer`` parameter of the
:func:`renpy.music.register_channel` function sets to which mixer the registered
channel relates, creating it in the process if it doesn't already exist.

A track's relative volume is set with the ``volume`` clause of the :ref:`play-statement`.


In addition to these volume values, there is the mute flag of the mixer which
the channel relates to. If enabled, it will reduce the played volume to 0.
They can be set using the :func:`SetMute` or :func:`ToggleMute` actions, or
using the :func:`Preference` action with the "mixer <mixer> mute" key, or using
the :func:`preferences.set_mute` function.

.. _silence:

Playing Silence
---------------

A specified duration of silence can played using a filename like
"<silence 3.0>", where 3.0 is the number of seconds of silence that is
desired. This can be used to delay the start of a sound file. For example::

        play audio [ "<silence .5>", "boom.opus" ]

Will play silence for half a second, and then an explosion sound.


.. _audio-namespace:

Audio Namespace and Directory
-----------------------------

The ``play`` and ``queue`` statements evaluate their arguments in the
audio namespace. This means it is possible to use the define statement
to provide an alias for an audio file.

For example, one can write::

    define audio.sunflower = "music/sun-flower-slow-jam.ogg"

and then use::

    play music sunflower

Ren'Py will also automatically place sound files in the audio namespace,
if found in the ``game/audio`` directory. Files in this directory with a
supported extension (currently, .wav, .mp2, .mp3, .ogg, and .opus) have the
extension stripped, the rest of the filename forced to lower case, and are
placed into the audio namespace.

Note that just because a file is placed into the audio namespace, that doesn't
mean it can be used. So while you could play a file named "opening_song.ogg"
by writing::

    play music opening_song

Some filenames can't be accessed this way, as their names are not expressable
as Python variables. For example, "my song.mp3", "8track.opus", and
"this-is-a-song.ogg" won't work.

When searching for an audio file, if the file is not found, Ren'Py will look
in the audio directory. For example::

    play music "opening.ogg"

Will first look for ``game/opening.ogg``. If not found, Ren'Py will look for
``game/audio/opening.ogg``.

Actions
-------

See :ref:`audio-actions`.


Functions
---------

.. include:: inc/audio


Sound Functions
---------------

Most ``renpy.music`` functions have aliases in ``renpy.sound``. These functions are similar,
except they default to the sound channel rather than the music channel, and default
to not looping.
