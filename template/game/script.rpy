## You can place the script of your game in this file.

init:
    ## Declare images.

    image bg black = "#000000"
    image bg gray = "#c0c0c0"
    # image bg outside = "outside.jpg"
    # image eileen happy = "eileen_happy.png"

    ## Declare characters used by this game.

    $ e = Character('Eileen', color="#c8ffc8")


## The game starts here.
label start:

    scene bg gray

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"
