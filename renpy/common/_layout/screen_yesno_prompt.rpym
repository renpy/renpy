# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python hide:

    layout.provides('yesno_prompt')

    def yesno_prompt(screen, message):
        try:
            renpy.show_screen('yesno_prompt', message=message, yes_action=Return(True), no_action=Return(False))
            return ui.interact()
        finally:
            renpy.hide_screen('yesno_prompt')

    layout.yesno_prompt = yesno_prompt
