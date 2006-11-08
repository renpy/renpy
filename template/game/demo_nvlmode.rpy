# This demonstrates nvl_mode.rpy.

init:

    # Declare an nvl-version of eileen.
    $ nvle = NVLCharacter("Eileen",
                          color="#c8ffc8")

    # Setup the nvl styles.

    $ style.nvl_label.minwidth = 150
    $ style.nvl_label.text_align = 1.0
    
    $ style.nvl_window.background = "#0008"
    $ style.nvl_window.yfill = True
    $ style.nvl_window.xfill = True
    $ style.nvl_window.xpadding = 20
    $ style.nvl_window.ypadding = 30

    $ style.nvl_vbox.box_spacing = 10
    
    $ style.nvl_menu_choice.idle_color = "#0ff"
    $ style.nvl_menu_choice.hover_color = "#ff0"
    $ style.nvl_menu_choice_button.left_margin = 160
    $ style.nvl_menu_choice_button.right_margin = 20
    $ style.nvl_menu_choice_button.xfill = True
    $ style.nvl_menu_choice_button.hover_background = "#F0F2"


label demo_nvlmode:

    $ nvl_clear()
    
    nvle "NVL-style games are games that cover the full screen with text, rather then placing it in a file at the bottom of the screen."

    nvle "Ren'Py ships with a file, nvl_mode.rpy, that implements NVL-style games. You're seeing an example of NVL-mode at work."

    $ nvl_clear()

    nvle "To use NVL-mode, you need to define NVLCharacters instead of regular old Characters."

    nvle "You should also use nvl_clear() to clear the screen when that becomes necessary."

    # Doing this during the game isn't recommended, it's better to do
    # it in an init block.
    $ menu = nvl_menu
    
    menu:

        nvle "The nvl_mode also supports showing menus to the user, provided they are the last thing on the screen. Understand?"

        "Yes.":

            $ nvl_clear()

            nvle "Good!"

        "No.":

            $ nvl_clear()

            nvle "Well, it might help if you take a look at the demo code."

    $ menu = renpy.display_menu

    return
        
    
