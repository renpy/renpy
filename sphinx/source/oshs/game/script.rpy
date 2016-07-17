# You can place the script of your game in this file.

define e = Character("Eileen", kind=nvl)

define narrator = nvl_narrator
define menu = nvl_menu

define gui.nvl_name_xpos = 0.5
define gui.nvl_name_xalign = 0.5

define gui.nvl_text_xpos = 0.5
define gui.nvl_text_ypos = 50
define gui.nvl_text_xalign = 0.5
define gui.nvl_text_width = 1120

define gui.nvl_thought_xpos = 0.5
define gui.nvl_thought_xalign = 0.5
define gui.nvl_thought_width = 1120

define gui.nvl_button_xpos = 0.5
define gui.nvl_button_xalign = 0.5
define gui.nvl_button_width = 1000
define gui.nvl_button_text_xalign = 0.5

label start:

    scene expression "gui/main_menu.png"

    show eileen happy

    "Quidquid latine dictum sit, altum videtur."

    e "Hello!"

    e "Is there some reason why school-based games always seem to use handwriting fonts and paper textures?"

    menu:

        e "What do you think?"

        "It seems appropriate for the location of the game.":
            pass

        "Sometimes the old ways are the best ways.":
            pass

