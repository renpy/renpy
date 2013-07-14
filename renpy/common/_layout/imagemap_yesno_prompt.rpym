# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python hide:

    layout.provides('yesno_prompt')

    renpy.load_module("_layout/imagemap_common")

    # Define styles
    style.yesno_prompt = Style(style.prompt, help="a yes/no prompt")
    style.yesno_prompt_text = Style(style.prompt_text, help="a yes/no prompt (text)")

    # Define config variables.
    config.yesno_prompt_ground = None
    config.yesno_prompt_idle = None
    config.yesno_prompt_hover = None
    config.yesno_prompt_hotspots = None

    config.yesno_prompt_message_images = { }


    def yesno_prompt(screen, message):
        renpy.transition(config.intra_transition)

        ime = _ImageMapper(
            screen,
            config.yesno_prompt_ground,
            config.yesno_prompt_idle,
            config.yesno_prompt_hover,
            config.yesno_prompt_idle,
            config.yesno_prompt_hover,
            config.yesno_prompt_hotspots)

        ime.button("Yes", ui.returns(True), False)
        ime.button("No", ui.returns(False), False)

        ime.close()

        default = config.yesno_prompt_message_images.get(layout.ARE_YOU_SURE, None)
        message_image = config.yesno_prompt_message_images.get(message, default)

        if message_image:
            ui.add(message_image)
        else:
            layout.prompt(message, "yesno")

        rv = ui.interact(mouse="gamemenu")
        renpy.transition(config.intra_transition)
        return rv

    layout.yesno_prompt = yesno_prompt

