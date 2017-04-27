# This file contains demonstrations of Ren'Py's multimedia
# support. Right now, this is just showing off sound and music, but
# Ren'Py does support movies, and we'll add them sometime later.

#begin movie_image
image launch = Movie(play="oa4_launch.webm", pos=(10, 10), anchor=(0, 0))
#end movie_image

label tutorial_video:

    e "Ren'Py supports playing movies. There are two ways of doing this."

    e "The first way allows you to show a movie as an image, along with every other image that's displayed on the screen."

    show screen example('movie_image')

    e "To do this, we first have to define an image to be a Movie displayable. Movie displayables take a movie to play, and can be given position properties."

    stop music fadeout .25
    show screen example('movie_play')
    pause .25

    #begin movie_play
    show launch behind eileen
    #end movie_play

    e "Then, we can show the movie displayable, which starts the movie playing."

    #begin movie_stop
    hide launch
    #end movie_stop

    show screen example('movie_stop')

    e "When we no longer want to play the movie, we can hide it."

    show screen example('movie_cutscene')

    e "The other way to show a movie is with the renpy.movie_cutscene python function. This shows the movie fullscreen, either until it ends or until the user clicks."

    hide screen example

    #begin movie_cutscene
    $ renpy.movie_cutscene("oa4_launch.webm")
    #end movie_cutscene

    e "A Movie displayable can also take a mask with an alpha channel, which lets you make movie sprites. But that's more complicated, so I'll stop here for now."

    play music "sunflower-slow-drag.ogg"

    return
