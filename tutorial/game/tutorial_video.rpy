# This file contains demonstrations of Ren'Py's multimedia
# support. Right now, this is just showing off sound and music, but
# Ren'Py does support movies, and we'll add them sometime later.

#begin movie_image
image shuttle = Movie(channel="shuttle", play="shuttle.ogv", pos=(475, 50), anchor=(0, 0))
#end movie_image

label tutorial_video:

    e "Ren'Py supports playing movies. There are two ways of doing this."

    e "The first way allows you to show a movie as an image, along with every other image that's displayed on the screen."

    show example movie_image

    e "To do this, we first have to define an image to be a Movie displayable. Movie displayables require a size argument, and also use properties to position themselves on the screen."

    stop music fadeout .25
    show example movie_play
    pause .25

    #begin movie_play
    show shuttle behind eileen
    #end movie_play

    e "Then, we can show the movie displayable, which starts the movie playing."

    #begin movie_stop
    hide shuttle
    #end movie_stop

    show example movie_stop

    e "When we no longer want to play the movie, we can hide it."

    show example movie_cutscene

    e "The other way to show a movie is with the renpy.movie_cutscene python function. This shows the movie fullscreen, either until it ends or until the user clicks."

    hide example

    #begin movie_cutscene
    $ renpy.movie_cutscene("shuttle.ogv")
    #end movie_cutscene

    e "And that's all there is when it comes to movie playback in Ren'Py."

    play music "sunflower-slow-drag.ogg"

    return
