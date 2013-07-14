# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python hide:

    layout.provides('yesno_prompt')

    # Define styles
    style.yesno_frame = Style(style.menu_frame, help="frame containing a yes/no prompt and yes/no buttons")
    style.yesno_frame_vbox = Style(style.vbox, help="box separating yes/no prompt from yes/no buttons")

    style.yesno_prompt = Style(style.prompt, help="a yes/no prompt")
    style.yesno_prompt_text = Style(style.prompt_text, help="a yes/no prompt (text)")

    style.yesno_button_hbox = Style(style.hbox, help="the box separating yes and no buttons")
    style.yesno_button = Style(style.button, help="a yes or no button")
    style.yesno_button_text = Style(style.button_text, help="a yes or no button (text)")

    # Alter styles.
    style.yesno_frame.xfill = True
    style.yesno_frame.xmargin = .05
    style.yesno_frame.ypos = .1
    style.yesno_frame.yanchor = 0
    style.yesno_frame.ypadding = .05

    style.yesno_frame_vbox.xalign = 0.5
    style.yesno_frame_vbox.yalign = 0.5
    style.yesno_frame_vbox.box_spacing = 30

    style.yesno_button_hbox.xalign = 0.5
    style.yesno_button_hbox.spacing = 100

    style.yesno_button.size_group = "yesno"

    def yesno_prompt(screen, message):
        renpy.transition(config.intra_transition)

        layout.navigation(screen)

        ui.window(style='yesno_frame')
        ui.vbox(style='yesno_frame_vbox')

        layout.prompt(message, "yesno")

        ui.hbox(style='yesno_button_hbox')

        # The extra nulls are because we want equal whitespace surrounding
        # the two buttons. It should work as long as we have xfill=True
        layout.button(u"Yes", 'yesno', clicked=ui.returns(True))
        layout.button(u"No", 'yesno', clicked=ui.returns(False))

        ui.close()
        ui.close()

        rv = ui.interact(mouse="gamemenu")
        renpy.transition(config.intra_transition)
        return rv

    layout.yesno_prompt = yesno_prompt

