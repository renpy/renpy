# This file contains the script for the Ren'Py demo game. Execution starts at
# the start label.

# Declare the characters.
define e = Character(_('Eileen'), color="#c8ffc8")

init python:

    tutorials = [

        (None, _("Quickstart"), False),


        ("tutorial_playing", _("Player Experience"), True),
        ("tutorial_create", _("Creating a new Game"), True),
        ("tutorial_dialogue", _("Writing Dialogue"), True),
        ("tutorial_images", _("Adding Images"), True),
        ("tutorial_transitions", _("Transitions"), True),
        ("tutorial_music", _("Music and Sound Effects"), True),
        ("tutorial_menus", _("Choices and Python"), True),
        ("tutorial_video", _("Video Playback"), True),
        ("tutorial_nvlmode", _("NVL Mode"), False),

        (None, _("In Depth"), False),

        ("tutorial_screens", _("Screens"), True),
        ("tutorial_positions", _("Screen Positions"), True),
        ("tutorial_atl", _("Transforms and Animation"), True),

        ("transform_properties", _("Transform Properties"), True),

        ("demo_transitions", _("Transition Gallery"), True),
        ("demo_imageops", _("Image Operations"), True),
        ("demo_ui", _("User Interaction"), True),
        ("demo_text", _("Fonts and Text Tags"), True),
        ("demo_character", _("Character Objects"), True),
        ("demo_layers", _("Layers & Advanced Show"), True),
        ("demo_dynamic", _("Dynamic Displayables"), True),
        ("demo_minigame", _("Minigames"), True),
        ("demo_persistent", _("Persistent Data"), True),
        ("demo_transform", _("Transform"), True),
        ("tutorial_sprite", _("Sprites"), True),

        ]

screen tutorials(adj):

    frame:
        xsize 640
        xalign .5
        ysize 495
        ypos 20

        has side "c r b"

        viewport:
            yadjustment adj
            mousewheel True

            vbox:
                for label, name, should_move in tutorials:

                    if label is not None:

                        textbutton name:
                            action Return((label, should_move))
                            left_padding 20
                            xfill True

                    else:

                        null height 10
                        text name
                        null height 5




        bar adjustment adj style "vscrollbar"

        textbutton _("That's enough for now."):
            xfill True
            action Return((False, True))
            top_margin 10


# This is used to preserve the state of the scrollbar on the selection
# screen.
default tutorials_adjustment = ui.adjustment()

# True if this is the first time through the tutorials.
default tutorials_first_time = True

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

label tutorials:

    show eileen happy at left
    with move

    if tutorials_first_time:
        $ e(_("What would you like to see?"), interact=False)
    else:
        $ e(_("Is there anything else you'd like to see?"), interact=False)

    $ tutorials_first_time = False

    call screen tutorials(adj=tutorials_adjustment)

    $ target, should_move = _return

    if should_move:
        show eileen happy at center
        with move

    if target is False:
        jump end

    call expression target from _call_expression

    jump tutorials

label end:

    e "Thank you for viewing this tutorial."

    e "If you'd like to see a full Ren'Py game, select \"The Question\" in the launcher."

    e "You can download new versions of Ren'Py from {a=https://www.renpy.org/}https://www.renpy.org/{/a}. For help and discussion, check out the {a=https://lemmasoft.renai.us/forums/}Lemma Soft Forums{/a}."

    e "We'd like to thank Piroshki for contributing my sprites, Mugenjohncel for Lucy and the band, and Jake for the magic circle."

    e "The background music is \"Sunflower Slow Drag\", by Scott Joplin and Scott Hayden, performed by the United States Marine Band. The concert music is by Alessio."

    show eileen vhappy

    e "We look forward to seeing what you can make with Ren'Py. Have fun!"

    window hide

    # Returning from the top level quits the game.
    return
