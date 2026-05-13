.. _movie:

Movie
=====

Ren'Py is capable of using FFmpeg (included) to play movies using the
video codecs:

* AV1
* VP9
* VP8
* Theora
* MPEG-4 part 2 (including Xvid and DivX)
* MPEG-2
* MPEG-1

and the following audio codecs:

* Opus
* Vorbis
* MP3
* MP2
* FLAC
* PCM

inside the following container formats:

* WebM
* Matroska
* Ogg
* AVI
* Various kinds of MPEG stream.

(Note that using some of these formats may require patent licenses.
When in doubt, and especially for commercial games, we recommend using
AV1, VP9, VP8, or Theora; Opus or Vorbis; and WebM, Matroska, or Ogg.)

Movies can be displayed fullscreen or in a displayable. Fullscreen movies
are more efficient. YUV444 movies are not hardware accelerated, use YUV420
or YUV422 instead.

Ren'Py's movie decoder does not support movies with alpha channels, but the
`side_mask` parameter of the :func:`Movie` displayable can be used for that
purpose. Here is an example of how to use ffmpeg to create a webm file with
a side-by-side mask from a mov file with an alpha channel. ::

    ffmpeg -i original.mov -filter:v alphaextract mask.mov
    ffmpeg -i original.mov -i mask.mov -filter_complex "hstack" -codec:v vp8 -crf 10 output.webm

Movies are supported on the Web platform, but the list of supported codecs differs
from browser to browser. For cross-browser compatibility (especially to support Safari),
the most efficient combination is H.264 with MP3 (or AAC) in a MP4 file. However, Ren'Py
does not support H.264 decoding (or AAC), so this combination can only work on the
Web platform.


Fullscreen Movies
-----------------

The easiest and most efficient way to display a movie fullscreen is
to use the :func:`renpy.movie_cutscene` function. This function displays the
movie fullscreen until it either ends, or the player clicks to dismiss
it. ::

    $ renpy.movie_cutscene("On_Your_Mark.webm")

Movie Displayables and Movie Sprites
------------------------------------

The Movie displayable can be used to display a movie anywhere Ren'Py can
show a displayable. For example, a movie can be displayed as the background
of a menu screen, or as a background.

The Movie displayable can also be used to define a movie sprite, which is
a sprite that is backed by two movies. The primary movie provides the
color of the sprite. A second movie, the mask movie, provides the alpha
channel, with white being full opacity and black being full transparency.

Movies played by the Movie displayable loop automatically.

Here's an example of defining a movie sprite::

    image eileen movie = Movie(play="eileen_movie.webm", side_mask=True)

The movie sprite can be shown using the show statement, which automatically starts the
movie playing. It will be automatically stopped when the displayable is hidden. ::

    show eileen movie

    e "I'm feeling quite animated today."

    hide eileen

    e "But there's no point on wasting energy when I'm not around."

A Movie displayable can also be used as part of a screen, provided it is created
during the init phase (for example, as part of an image statement.) ::


    image main_menu = Movie(play="main_menu.ogv")

    screen main_menu:
        add "main_menu"
        textbutton "Start" action Start() xalign 0.5 yalign 0.5

Multiple movie displayables or sprites can be displayed on the screen at once,
subject to system performance, and provided all share the same framerate. The
behavior of Ren'Py when displaying movies with different framerates is
undefined, but will likely include a significant amount of frame drop.


Python Functions
----------------

.. include:: inc/movie_cutscene
.. include:: inc/movie
