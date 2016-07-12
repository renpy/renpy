# You can place the script of your game in this file.

define e = Character("Eileen")

screen bar_test:
    frame:
        xalign 0.5
        yalign 0.5

        xsize 800

        hbox:
            spacing 10
            text "Progress"
            bar value StaticValue(60, 100)

label start:

    scene expression "gui/main_menu.png"

    show eileen happy

    e "Hello!"

    $ renpy.input("What's your name?", "Hiro Protagonist")

    e "Is there some reason why school-based games always seem to use handwriting fonts and paper textures?"

    menu:

        e "What do you think?"

        "It seems appropriate for the location of the game.":
            pass

        "Sometimes the old ways are the best ways.":
            pass


    call screen borders


