# You can place the script of your game in this file.

define e = Character("Eileen")

define b = Borders(40, 5, 40, 5, tile=True)

define gui.frame_borders = Borders(20, 20, 20, 20, tile=True)


screen buttons():

    frame:
        has vbox



        spacing 10

        textbutton "Large Button":
            action Return(None)
            background Frame("btb.png", b)
            padding b.padding

        textbutton "1":
            action Return(None)
            background Frame("btb.png", b)
            padding b.padding



label start:

    call screen buttons

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


