# Hi there! This is the Ren'Py tutorial game. It's actually a fairly bad
# example of Ren'Py programming style - the examples we present in the game
# itself are good, but to make them easy to present we wind up doing
# some non-standard high-level things.
#
# So feel free to poke around, but if you're really looking for an example
# of good Ren'Py programming style, consider checking out The Question
# instead.

# Declare the characters.
define e = Character(_('Eileen'), color="#c8ffc8")

init python:

    # A list of section and tutorial objects.
    tutorials = [ ]

    class Section(object):
        """
        Represents a section of the tutorial menu.

        `title`
            The title of the section. This should be a translatable string.
        """

        def __init__(self, title):
            self.kind = "section"
            self.title = title

            tutorials.append(self)


    class Tutorial(object):
        """
        Represents a label that we can jump to.
        """

        def __init__(self, label, title, move=True):
            self.kind = "tutorial"
            self.label = label
            self.title = title

            if move and (move != "after"):
                self.move_before = True
            else:
                self.move_before = False

            if move and (move != "before"):
                self.move_after = True
            else:
                self.move_after = False

            tutorials.append(self)


    Section(_("Quickstart"))

    Tutorial("tutorial_playing", _("Player Experience"))
    Tutorial("tutorial_create", _("Creating a New Game"))
    Tutorial("tutorial_dialogue", _("Writing Dialogue"))
    Tutorial("tutorial_images", _("Adding Images"))
    Tutorial("tutorial_simple_positions", _("Positioning Images"))
    Tutorial("tutorial_transitions", _("Transitions"))
    Tutorial("tutorial_music", _("Music and Sound Effects"))
    Tutorial("tutorial_menus", _("Choices and Python"))
    Tutorial("tutorial_input", _("Input and Interpolation"))
    Tutorial("tutorial_video", _("Video Playback"))
    Tutorial("tutorial_nvlmode", _("NVL Mode"), move=None)
    Tutorial("director", _("Tools and the Interactive Director"))
    Tutorial("distribute", _("Building Distributions"))

    Section(_("In Depth"))

    Tutorial("text", _("Text Tags, Escapes, and Interpolation"))
    Tutorial("demo_character", _("Character Objects"))
    Tutorial("simple_displayables", _("Simple Displayables"), move=None)
    Tutorial("demo_transitions", _("Transition Gallery"))

    # Positions and Transforms?
    Tutorial("tutorial_positions", _("Position Properties"))

    # Advanced Transforms?
    Tutorial("tutorial_atl", _("Transforms and Animation"))
    Tutorial("transform_properties", _("Transform Properties"))

    Tutorial("new_gui", _("GUI Customization"))
    Tutorial("styles", _("Styles and Style Properties"), move=None)
    Tutorial("tutorial_screens", _("Screen Basics"), move=None)
    Tutorial("screen_displayables", _("Screen Displayables"), move=None)

    Tutorial("demo_minigame", _("Minigames and CDDs"))
    Tutorial("translations", _("Translations"))

screen tutorials(adj):

    frame:
        xsize 640
        xalign .5
        ysize 485
        ypos 30

        has side "c r b"

        viewport:
            yadjustment adj
            mousewheel True

            vbox:
                for i in tutorials:

                    if i.kind == "tutorial":

                        textbutton i.title:
                            action Return(i)
                            left_padding 20
                            xfill True

                    else:

                        null height 10
                        text i.title alt ""
                        null height 5




        bar adjustment adj style "vscrollbar"

        textbutton _("That's enough for now."):
            xfill True
            action Return(False)
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
    $ renpy.choice_for_skipping()

    call screen tutorials(adj=tutorials_adjustment)

    $ tutorial = _return

    if not tutorial:
        jump end

    if tutorial.move_before:
        show eileen happy at center
        with move

    $ reset_example()

    call expression tutorial.label from _call_expression

    if tutorial.move_after:
        hide example
        show eileen happy at left
        with move

    jump tutorials

label end:

    show eileen happy at center
    with move

    show _finale behind eileen


    e "Thank you for viewing this tutorial."

    e "If you'd like to see a full Ren'Py game, select \"The Question\" in the launcher."

    e "You can download new versions of Ren'Py from {a=https://www.renpy.org/}https://www.renpy.org/{/a}. For help and discussion, check out the {a=https://lemmasoft.renai.us/forums/}Lemma Soft Forums{/a}."

    e "We'd like to thank Piroshki for contributing my sprites; Mugenjohncel for Lucy, the band, and drawn backgrounds; and Jake for the magic circle."

    e "The background music is \"Sunflower Slow Drag\", by Scott Joplin and Scott Hayden, performed by the United States Marine Band. The concert music is by Alessio."

    show eileen vhappy

    e "We look forward to seeing what you create with Ren'Py. Have fun!"

    window hide

    # Returning from the top level quits the game.
    return
