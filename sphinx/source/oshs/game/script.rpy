# You can place the script of your game in this file.

define e = Character("Eileen")

define b = Borders(40, 40, 40, 40, tile=True)


screen borders():
    add "black"

    textbutton "Child":
        background Frame("borders.png", b)
        padding b.padding
        text_size 125
        text_color "#484"

        xalign 0.5
        yalign 0.5


label start:

    scene expression "gui/main_menu.png"

    show eileen happy

    e "Is there some reason why school-based games always seem to use handwriting fonts and paper textures?"

    menu:

        e "What do you think?"

        "It seems appropriate for the location of the game.":
            pass

        "Sometimes the old ways are the best ways.":
            pass


    call screen borders

