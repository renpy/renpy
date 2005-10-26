# This file gives an example of how the various entries on the main
# and game menus can be repositioned on the screen. Unlike the other
# extras, we don't intend this to be used as-is, but instead to be
# copied and changed to change the positions of buttons on the screen.

# Buttons should not overlap, and certain configurations may make
# buttons inaccessible with keyboard navigation.

init:

    python hide:

        library.main_menu_positions = {
            'Start Game' : dict(xpos=400, ypos=400, xanchor='left', yanchor='top'),
            'Continue Game' : dict(xpos=450, ypos=430, xanchor='left', yanchor='top'),
            'Preferences' : dict(xpos=500, ypos=460, xanchor='left', yanchor='top'),
            'Quit Game' : dict(xpos=550, ypos=490, xanchor='left', yanchor='top'),
            }

        library.game_menu_positions = {
            'Return' : dict(xpos=400, ypos=400, xanchor='left', yanchor='top'),
            'Preferences' : dict(xpos=450, ypos=430, xanchor='left', yanchor='top'),
            'Save Game' : dict(xpos=500, ypos=460, xanchor='left', yanchor='top'),
            'Load Game' : dict(xpos=550, ypos=490, xanchor='left', yanchor='top'),
            'Main Menu' : dict(xpos=600, ypos=520, xanchor='left', yanchor='top'),
            'Quit' : dict(xpos=650, ypos=550, xanchor='left', yanchor='top'),
            }
