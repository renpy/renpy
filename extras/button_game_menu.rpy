# This file adds a number of buttons to the lower-right hand corner of
# the screen. Three of these buttons jump to the game menu, which
# giving quick access to Load, Save, and Prefs. The fourth button
# toggles skipping, to make that more convenient.

init:

    # Give us some space on the right side of the screen.
    $ style.window.right_margin = 100

    python:

        def toggle_skipping():
            config.skipping = not config.skipping

        def button_game_menu():

            # to save typing
            ccinc = renpy.curried_call_in_new_context

            ui.vbox(xpos=0.98, ypos=0.98, xanchor='right', yanchor='bottom')
            ui.textbutton("Skip", clicked=toggle_skipping)
            ui.textbutton("Save", clicked=ccinc("_game_menu_save"))
            ui.textbutton("Load", clicked=ccinc("_game_menu_load"))
            ui.textbutton("Prefs", clicked=ccinc("_game_menu_preferences"))
            ui.close()


        config.overlay_functions.append(button_game_menu)

        

            
    
    
