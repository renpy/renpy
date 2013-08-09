# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('main_menu')

    style.mm_menu_frame = Style(style.menu_frame, help="frame containing main menu")
    style.mm_menu_frame_box = Style(style.vbox, help="box containing main menu buttons")

    style.mm_button = Style(style.button, help="main menu button")
    style.mm_button_text = Style(style.button_text, help="main menu button (text)")

    style.mm_button.size_group = "mm"

    style.mm_menu_frame.xpos = 5.0/6.0
    style.mm_menu_frame.xanchor = 0.5
    style.mm_menu_frame.ypos = 0.9
    style.mm_menu_frame.yanchor = 1.0

label main_menu_screen:

    python hide:

        # Ignore right-click while at the main menu.
        ui.keymap(game_menu=ui.returns(None))

        # Show the background.
        ui.window(style='mm_root')
        ui.null()

        ui.frame(style='mm_menu_frame')
        ui.vbox(style='mm_menu_frame_box')

        for e in config.main_menu:

            if len(e) == 3:
                label, clicked, enabled = e
                shown = "True"
            else:
                label, clicked, enabled, shown = e

            if not eval(shown):
                continue

            # This checks to see if clicked is a string. If so, we want clicked
            # to jump us out of the current context.
            if isinstance(clicked, basestring):
                clicked=ui.jumpsoutofcontext(clicked)

            # Create each button.
            layout.button(label, "mm", enabled=eval(enabled), clicked=clicked)

        ui.close()

        ui.interact(mouse="mainmenu")

    return
