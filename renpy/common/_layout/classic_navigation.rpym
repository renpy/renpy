# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('navigation')

    style.gm_nav_frame = Style(style.menu_frame, help="game menu navigation frame")
    style.gm_nav_box = Style(style.vbox, help="box containing game menu navigation buttons")

    style.gm_nav_button = Style(style.button, help="game menu navigation button")
    style.gm_nav_button_text = Style(style.button_text, help="game menu navigation button (text)")

    style.gm_nav_button.size_group = "gm_nav_button"

    style.gm_nav_frame.xpos = 5.0/6.0
    style.gm_nav_frame.xanchor = 0.5
    style.gm_nav_frame.ypos = 0.95
    style.gm_nav_frame.yanchor = 1.0

    def _navigation(screen=None):

        # Display the game menu background
        ui.window(style=style.gm_root[screen])
        ui.null()

        if screen is None:
            return

        # Display the navigation frame.
        ui.frame(style='gm_nav_frame')
        ui.vbox(focus='gm_nav', style='gm_nav_box')

        for e in config.game_menu:

            if len(e) == 4:
                 key, label, clicked, enabled = e
                 shown = "True"
            else:
                 key, label, clicked, enabled, shown = e

            if not eval(shown):
                continue

            layout.button(label,
                          "gm_nav",
                          selected=(screen==key),
                          enabled=eval(enabled),
                          clicked=clicked)

        ui.close()

    layout.navigation = _navigation
