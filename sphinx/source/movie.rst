Movie
=====

Ren'Py is capable of using libav (included) to play movies using the
video codecs:

* Theora
* MPEG 4 part 2 (including Xvid and DivX)
* MPEG 2
* MPEG 1 

and the following audio codecs:

* Vorbis
* MP3
* MP2
* PCM 

inside the following container formats:

* Matroska
* Ogg
* Avi
* Various kinds of MPEG stream. 

(Note that using some of these formats may require patent licenses.
When in doubt, and especially for commercial games, we recommend using
Theora, Vorbis, and Matroska or Ogg.)

Ren'Py expects that every movie will have an audio track associated with it,
even if that audio track consists of nothing but silence. This is because
the audio track is used for synchronization purposes.

Movies can be displayed fullscreen, or in a displayable. Fullscreen movies
are the more efficient. 


Fullscreen Movies
-----------------

The easiest way to display a movie fullscreen is to display it using
the renpy.movie_cutscene function. This function displays a movie for a specified
length of time. When that time has elapsed, or when the user clicks to dismiss
the movie, the movie ends and the function returns. ::

        $ renpy.movie_cutscene("On_Your_Mark.mpg")

.. include:: inc/movie_cutscene

Movies Inside Displayables
--------------------------

A movie can also be displayed inside a displayable, allowing it to be combined with
other things on the screen. To do this, one must first show a Movie displayable, and
then play the movie on an audio channel. (We recommend using the movie channel
for this purpose.) ::

        init:
            image movie = Movie(size=(400, 300), xalign=0.5, yalign=0.5)

        label movie_sign:
            scene black
            show movie

            play movie "incubus.mkv"

            "Wow, this movie is really terrible."

            "I mean, it stars William Shatner..."

            "... speaking Esperanto."

            "MAKE IT STOP!"

            stop movie
            hide movie

            "Thats... better."

.. include:: inc/movie
