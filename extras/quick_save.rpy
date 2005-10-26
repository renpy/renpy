# This file implements quick save and load functionality. The
# quicksave functionality adds a button to the overlay that is
# displayed over the game. When the button is clicked, the game is
# saved in a special quicksave slot. It also adds a quick load button
# to the main menu. When that button is clicked, the quicksave game is
# loaded.

# This is called when the quick save button is clicked.
label _quick_save:
    call _enter_menu_without_scene from __call__enter_menu_4

    # Save the game.
    $ renpy.save('quicksave', _('Quick Save'))

    # Tell the user that we saved the game.
    $ ui.add(Solid((0, 0, 0, 128)))
    $ ui.text(_('The game has been saved using quick save.'),
              xpos=0.5, xanchor='center', ypos=0.5, yanchor='center')

    $ ui.saybehavior()
    $ ui.interact(suppress_overlay=True, suppress_underlay=True)

    return

# This is called when the quick load button is clicked, to load the
# game.
label _quick_load:
    $ renpy.load('quicksave')
    return

init -1:

    python hide:
        
        # Add the quick save button in as an overlay function.
        def quick_save_button():
            ui.textbutton(_("Quick Save"),
                          xpos=0.98, ypos=0.02,
                          xanchor='right', yanchor='top',
                          clicked=renpy.curried_call_in_new_context('_quick_save'))

        config.overlay_functions.append(quick_save_button)

        # Add the quick load function to the main menu.
        library.main_menu.insert(1, ('Quick Load',
                                     ui.jumps("_quick_load"),
                                     'renpy.can_load("quicksave")'))
