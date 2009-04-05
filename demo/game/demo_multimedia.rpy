# This file contains demonstrations of Ren'Py's multimedia
# support. Right now, this is just showing off sound and music, but
# Ren'Py does support movies, and we'll add them sometime later.

image movie = Movie(size=(320, 240), xpos=475, ypos=50, xanchor=0, yanchor=0)

label demo_multimedia:

    e "Ren'Py supports a number of multimedia functions."

    e "You're probably hearing music playing in the background."

    # This stops the music, and fades it out.
    stop music fadeout 0.5

    e "We can stop it, with a fadeout..."

    # This plays music.
    play music "mozart.ogg"

    e "... and start it playing again."

    # This plays a sound effect.
    play sound "18005551212.ogg"

    e "We can play sound effects on top of the music."

    $ renpy.music.set_pan(-1, 0)
    $ renpy.music.set_pan( 1, 2)
    
    e "We can pan the music back and forth."

    $ renpy.music.set_pan(0, .5)
    
    e "Voice support is included as part of Ren'Py, although we don't yet have a demonstration."

    $ renpy.music.set_volume(0, .5)
    
    e "Finally, we support playing movie files."

    show movie behind eileen
    play movie "shuttle.ogv"
    
    e "We can put a movie on the screen with text and other images."

    stop movie
    hide movie
    
    e "We can also play the movie in fullscreen... but with this tiny movie we're using as an example, it's going to look bad."

    $ renpy.movie_cutscene("shuttle.ogv", stop_music=False)

    $ renpy.music.set_volume(1, 1.0)
        
    e "That's about it for multimedia."

    return
