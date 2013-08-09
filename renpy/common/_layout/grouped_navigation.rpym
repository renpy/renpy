# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('navigation')

    style.gm_nav_frame = Style(style.menu_frame, help="game menu navigation frame")
    style.gm_nav_inner_box = Style(style.hbox, help="inner box containing game menu navigation buttons")
    style.gm_nav_outer_box = Style(style.vbox, help="outer box containing game menu navigation buttons")

    style.gm_nav_button = Style(style.button, help="game menu navigation button")
    style.gm_nav_button_text = Style(style.button_text, help="game menu navigation button (text)")

    style.gm_nav_button.size_group = "gm_nav_button"

    style.gm_nav_frame.xalign = 0.5
    style.gm_nav_frame.ypos = 0.98
    style.gm_nav_frame.yanchor = 1.0

    style.gm_nav_inner_box.xalign = 0.5

    config.navigation_per_group = 4

    def navigation(screen=None):

        # Display the game menu background
        ui.window(style=style.gm_root[screen])
        ui.null()

        if screen is None:
            return

        # Display the navigation frame.
        ui.frame(style='gm_nav_frame')
        ui.vbox(focus='gm_nav', style='gm_nav_outer_box')

        box_open = False

        for i, e in enumerate(config.game_menu):

            if len(e) == 4:
                 key, label, clicked, enabled = e
                 shown = "True"
            else:
                 key, label, clicked, enabled, shown = e

            if not eval(shown):
                continue

            if i % config.navigation_per_group == 0:
                if box_open:
                    ui.close()

                ui.hbox(style='gm_nav_inner_box')
                box_open = True

            layout.button(label,
                          "gm_nav",
                          selected=(screen==key),
                          enabled=eval(enabled),
                          clicked=clicked)

        if box_open:
            ui.close() # inner box.

        ui.close() # outer box.

    layout.navigation = navigation
