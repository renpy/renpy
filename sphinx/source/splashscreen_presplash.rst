Splashscreen and Presplash
==========================

Adding a Splashscreen
---------------------
A splash screen is an image or movie that appears when the game is starting up
and before it goes to the menu. Usually these are logos or intro videos. The
"splashscreen" label automatically plays before the main menu. However, same
code applies to a splashscreen located anywhere in your game under a different
label.

To add a text splashscreen to your game, insert code like this into anywhere in
your script file (as long as it is not itself in a block): ::

    label splashscreen:
        scene black
        with Pause(1)

        show text "American Bishoujo Presents..." with dissolve
        with Pause(2)

        hide text with dissolve
        with Pause(1)

        return

Here's another example of a splashscreen, this time using an image and
sound: ::

    image splash = "splash.png"

    label splashscreen:
        scene black 
        with Pause(1)
        
        play sound "ping.ogg"

        show splash with dissolve
        with Pause(2)
        
        scene black with dissolve
        with Pause(1)

        return

And finally, with a movie file: ::

    label splashscreen:

        $ renpy.movie_cutscene('movie.ogv')

        return

Adding a Presplash
------------------

A presplash is an image shown while Ren'py is reading the scripts and
launching the game. Make an image named `presplash.png` (or `presplash.jpg`),
and put that image into the game directory.
