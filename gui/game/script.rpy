# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    call screen test

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return


screen test():

    frame:
        xpadding 10
        ypadding 10


        has vbox:
            spacing 10

        hbox:
            text "Test 1"
            bar value StaticValue(33, 100) xsize 300
        hbox:
            text "Test 2"
            bar value StaticValue(66, 100) xsize 300

