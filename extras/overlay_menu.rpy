# This file replaces most of the game menu navigation with overlay
# buttons that jump directly to various parts of the game menu.
# Right clicking hides and shows the buttons, rather than calling
# up the game menu directly.

init:
    python hide:

        # overlay_menu is an object storing information about the
        # overlay menu state.        
        store.overlay_menu = object()
        overlay_menu.shown = False

        # overlay_menu is also a new layer, containing the overlay
        # menu.
        config.layers.append("overlay_menu")
        config.overlay_layers.append("overlay_menu")


        # This function actually draws the overlay menu.
        def overlay_menu_func():
            if overlay_menu.shown:

                ui.layer("overlay_menu")

                ui.vbox(xpos=1.0, xanchor="right", ypos=0.75, yanchor="bottom")

                def button(label, target):
                    ui.textbutton(label, clicked=renpy.curried_call_in_new_context(target))

                button("Load Game", "_game_menu_load")
                button("Save Game", "_game_menu_save")
                button("Preferences", "_game_menu_preferences")

                ui.close()
                ui.close()
        

        config.overlay_functions.append(overlay_menu_func)


        # This function toggles the visibility of the overlay menu.
        def overlay_menu_toggle():
            shown = not overlay_menu.shown
            overlay_menu.shown = shown

            # How long should the transitions take?
            trans_delay = 0.5

            # These transitions assume that the menu is placed on the
            # right side of the screen. This indicator gives the
            # fraction of the screen that participates in transitions.

            trans_frac = 0.75

            if shown:
                
                trans = CropMove(trans_delay,
                                 "custom",
                                 startcrop=(trans_frac, 0.0, 0.0, 1.0),
                                 startpos=(1.0, 0.0),
                                 endcrop=(trans_frac, 0.0, 1.0-trans_frac, 1.0),
                                 endpos=(trans_frac, 0.0),
                                 topnew=True)
                
                renpy.transition(trans, 'overlay_menu')

            else:

                trans = CropMove(trans_delay,
                                 "custom",
                                 endcrop=(trans_frac, 0.0, 0.0, 1.0),
                                 endpos=(1.0, 0.0),
                                 startcrop=(trans_frac, 0.0, 1.0-trans_frac, 1.0),
                                 startpos=(trans_frac, 0.0),
                                 topnew=False)
                
                renpy.transition(trans, 'overlay_menu')
                

            renpy.restart_interaction()


        # Add a new underlay that handles the overlay menu toggle.
        config.underlay.append(renpy.Keymap(game_menu = overlay_menu_toggle))
            
        
