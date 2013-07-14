# This file contains code for the menu that lets people select which demo
# they want to use. It uses quite a bit of the UI code, but it's probably
# a bit complex for the average user.

init:
    python:
        demos_main = [
            ("demo_basics", "Basic Scripting", "5.6.3"),
            ("demo_experience", "User Experience", "5.6.3"),
            ("demo_transitions", "Transitions", "5.6.6"),
            ("demo_movement", "Positions and Movement", "6.9.0"),
            ("demo_animation", "Animation", "6.2.0"),
            ("demo_multimedia", "Music, Sound, and Video", "6.9.1"),
            ("demo_imageops", "Image Operations", "6.5.0"),
            ("demo_ui", "User Interaction", "6.5.0"),
            ("demo_text", "Fonts and Text Tags", "6.8.0"),
            ("demo_character", "Character Objects", "6.2.0"),
            ("demo_advanced", "Advanced Features", "6.9.0"),
            ]

        # Update above with this!
        demos_advanced = [
            ("demo_layers", "Layers & Advanced Show", "5.6.5"),
            ("demo_nvlmode", "NVL Mode", "6.4.0"),
            ("demo_dynamic", "Dynamic Displayables", "5.6.3"),
            ("demo_minigame", "Minigames", "6.3.2"),
            ("demo_persistent", "Persistent Data", "6.7.0"),
            ("demo_transform", "Transform", "6.9.0"),
            ]

        def demos_show(demos_info, nevermind):

            renpy.choice_for_skipping()

            ui.vbox(xpos=250, ypos=225, yanchor=0.5)

            for label, name, ver in demos_info:
                ui.button(style='button',
                          clicked=ui.returns(label),
                          xminimum=530,
                          left_padding=20)
                ui.hbox()
                ui.text(name, style='button_text', size=22, minwidth=440)
                ui.text(ver, style='button_text', size=22)
                ui.close()

            ui.text(" ")

            ui.button(style='button',
                      clicked=ui.returns(False),
                      xminimum=530,
                      left_padding=20)

            ui.text(nevermind, style='button_text', size=22, minwidth=450)

            ui.close()

            rfd = renpy.roll_forward_info()
            store.result = ui.interact(roll_forward=rfd)
            renpy.checkpoint(store.result)


label demos:

    # Is this the first time through the demo?
    $ demo_first_time = True

    show eileen happy at left
    with move

label demo_repeat:

    python hide:

        if demo_first_time:
            e("What would you like demonstrated?", interact=False)
        else:
            e("Is there anything else you'd like demonstrated?", interact=False)

        store.demo_first_time = False

        demos_show(demos_main, "That's enough for now.")

    # If the result is False, then the user clicked the "Enough for
    # now" button, and we should return to the main script.
    if result == False:

        show eileen happy at center
        with move

        return

    # If the result is the advanced demo, just call it without
    # re-setting up the screen.
    elif result == "demo_advanced":

        call demo_advanced from _call_demo_advanced_1

        jump demo_repeat

    else:

        show eileen happy
        with move

        # Otherwise, we want to call the result.
        call expression result from _call_result_1

        show eileen happy at left
        with move

        # And then re-show this menu.
        jump demo_repeat


# Presented without commentary, as it's basically a repeat of the above.
label demo_advanced:

    # Hide the editor button.
    $ show_editor_button = False

    python hide:

        e("Which advanced feature would you like to learn about?", interact=False)

        demos_show(demos_advanced, "Nevermind.")

    # Move eileen back to the center of the screen, unless we're going for
    # an advanced demo.

    # Show the editor button.
    $ show_editor_button = True

    # If the result is False, then the user clicked the "Enough for
    # now" button, and we should return to the main script.
    if result == False:

        return

    else:

        show eileen happy
        with move

        # Otherwise, we want to call the result.
        call expression result from _call_result_2

        show eileen happy at left
        with move

        # And then re-show this menu.
        jump demo_advanced
