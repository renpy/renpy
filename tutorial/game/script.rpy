# This file contains the script for the Ren'Py demo game. Execution starts at
# the start label.

# Declare the characters.
define e = Character(_('Eileen'), color="#c8ffc8")

init python:

    tutorials = [
        ("tutorial_playing", _("User Experience"), "6.10.0"),
        ("tutorial_dialogue", _("Writing Dialogue"), "6.10.0"),
        ("tutorial_images", _("Adding Images"), "6.10.0"),
        ("tutorial_transitions", _("Transitions"), "6.10.0"),
        ("tutorial_music", _("Music and Sound Effects"), "6.10.0"),
        ("tutorial_menus", _("In-Game Menus and Python"), "6.10.0"),
        ("tutorial_positions", _("Screen Positions"), "6.10.0"),
        ("tutorial_atl", _("Animation and Transformation"), "6.10.0"),
        ("tutorial_video", _("Video Playback"), "6.10.0"),
        ("demo_transitions", _("Transition Gallery"), "6.11.1"),
        ("demo_imageops", _("Image Operations"), "6.5.0"),
        ("demo_ui", _("User Interaction"), "6.15.0"),
        ("demo_text", _("Fonts and Text Tags"), "6.13.0"),
        ("demo_character", _("Character Objects"), "6.2.0"),
        ("demo_layers", _("Layers & Advanced Show"), "6.17.0"),
        ("demo_nvlmode", _("NVL Mode"), "6.4.0"),
        ("demo_dynamic", _("Dynamic Displayables"), "5.6.3"),
        ("demo_minigame", _("Minigames"), "6.3.2"),
        ("demo_persistent", _("Persistent Data"), "6.7.0"),
        ("demo_transform", _("Transform"), "6.9.0"),
        ("tutorial_sprite", _("Sprites"), "6.12.0"),
        ]

screen tutorials:

    side "c r":
        area (250, 40, 548, 400)

        viewport:
            yadjustment adj
            mousewheel True

            vbox:
                for label, name, ver in tutorials:
                    button:
                        action Return(label)
                        left_padding 20
                        xfill True

                        hbox:
                            text name style "button_text" min_width 420
                            text ver style "button_text"

                null height 20

                textbutton _("That's enough for now."):
                    xfill True
                    action Return(False)

        bar adjustment adj style "vscrollbar"


# The game starts here.
#begin start
label start:

    #end start
    scene bg washington
    show eileen vhappy
    with dissolve

    # Start the background music playing.
    play music "sunflower-slow-drag.ogg"

    window show

    e "Hi! My name is Eileen, and I'd like to welcome you to the Ren'Py tutorial."

    show eileen happy

    e "In this tutorial, we'll teach you the basics of Ren'Py, so you can make games of your own. We'll also demonstrate many features, so you can see what Ren'Py is capable of."

    $ tutorials_adjustment = ui.adjustment()
    $ tutorials_first_time = True

    while True:
        show eileen happy at left
        with move

        if tutorials_first_time:
            $ e(_("What would you like to see?"), interact=False)
        else:
            $ e(_("Is there anything else you'd like to see?"), interact=False)

        $ tutorials_first_time = False

        call screen tutorials(adj=tutorials_adjustment)

        show eileen happy at center
        with move

        if _return is False:
            jump end

        call expression _return


label end:

    e "Thank you for viewing this tutorial."

    e "If you'd like to see a full Ren'Py game, select \"The Question\" in the launcher."

    e "You can download new versions of Ren'Py from {a=http://www.renpy.org/}http://www.renpy.org/{/a}. For help and discussion, check out the {a=http://lemmasoft.renai.us/forums/}Lemma Soft Forums{/a}."

    e "We'd like to thank Piroshki for contributing my sprites, Mugenjohncel for Lucy and the band, and Jake for the magic circle."

    e "The background music is \"Sunflower Slow Drag\", by Scott Joplin and Scott Hayden, performed by the United States Marine Band. The concert music is by Alessio."

    show eileen vhappy

    e "We look forward to seeing what you can make with Ren'Py. Have fun!"

    window hide

    # Returning from the top level quits the game.
    return
