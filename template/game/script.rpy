# You can place the script of your game in this file.

init:

    # Declare images used by this game.
    image gray = "#c0c0c0"

    # Declare characters used by this game.
    $ e = Character('Eileen', color="#c8ffc8")


# The game starts here.
label start:

    scene gray

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it
       to the world!"
