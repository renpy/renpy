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

The 'Music Volume', 'Sound Volume', and 'Voice Volume' settings
of the in-game preferences menu are used to set individual
volumes for these channels.

Sounds can also be set to play when buttons, menu choices, or
imagemaps enter their hovered or activated states.
See Sound Properties.

The usual way to play music and sound in Ren'Py is using
the three music/sound statements

The Play Statement
------------------

The play statement is used to play sound and music. If a file is
currently playing, it is interrupted and replaced with the new file.

The name of a channel is expected following Keyword `play`,
(Usually, this is either "sound", "music", or "voice".) and audiofile(s)
follow it.

audiofile(s) can be one file or list of files.

fadein and fadeout clauses are all optional. Fadeout gives the fadeout
time for currently playing music, in seconds, while fadein gives the time
it takes to fade in the new music. If fadeout is not given, config.fade_music
is used.

loop and noloop clauses are also all optional.

A loop clause causes the queued music to loop, while noloop causes it to play
only once. If both of them isn't given The default of the channel is used. ::

        play music "mozart.ogg"
        play sound "woof.mp3"
        play myChannel "punch.wav" # 'myChannel' needs to be defined with renpy.music.register_channel().

        "We can also play a list of sounds, or music."
        play music [ "a.ogg", "b.ogg" ] fadeout 1.0 fadein 1.0

The Stop Statement
------------------

The stop statement begin with keyword `stop`, the name of a channel to stop
sound on is expected following it. It also optionally have a fadeout clause. ::

        stop sound
        stop music fadeout 1.0

The Queue Statement
-------------------

The queue statement begin with keyword `queue`, the name of a channel to play
sound on is expected following it. it also optionally have loop and noloop clauses. ::

        queue sound "woof.ogg"
        queue music [ "a.ogg", "b.ogg" ]

The advantage of using these statements is that your program will be checked for
missing sound and music files when lint is run. The functions below exist to allow
access to allow music and sound to be controlled from python, and to expose
advanced (rarely-used) features.

Two configuration variables, config.main_menu_music and config.game_menu_music allow
for the given music files to be played as the main and game menu music, respectively. 

Functions
---------

.. include:: inc/audio

Sound Functions
---------------

Most renpy.music functions have aliases in renpy.sound. These functions are similar,
except they default to the sound channel rather than the music channel, and default to not looping. 
