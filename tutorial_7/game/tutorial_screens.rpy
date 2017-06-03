################################################################################
# Stats screen.
#
# This displays RPG-like statistics.
################################################################################

default player_hp = 15
default player_hp_max = 42
default eileen_hp = 100
default eileen_hp_max = 100

default player_lv = 4
default eileen_lv = 99

# This screen displays a single stat.
screen single_stat(name, hp, hp_max, lv, xalign):

    frame:
        xalign xalign

        vbox:
            spacing 5

            hbox:
                text "[name]" min_width 220
                text _(" Lv. [lv]")

            hbox:
                text "HP":
                    min_width 40
                    yalign 0.5

                bar:
                    value AnimatedValue(hp, hp_max, 1.0)
                    xmaximum 180
                    ysize 26


                text " [hp]/[hp_max]":
                    yalign 0.5


# This screen uses single_stat to display two stats at once.
screen stats():
    use single_stat(_("Player"), player_hp, player_hp_max, player_lv, 0.0)
    use single_stat(_("Eileen"), eileen_hp, eileen_hp_max, eileen_lv, 1.0)


################################################################################
# Day picker
#
# This code displays a day picker, including statistics and a way of choosing
# an action for each period of the day.
################################################################################


# This constant defines the periods in the day.
define day_periods = [ _('Morning'), _('Afternoon'), _('Evening') ]

# This constant defines what to do in each period.
define day_choices = [ _('Study'), _('Exercise'), _('Eat'), _('Drink'), _('Be Merry') ]

# This is a dictionary mapping a period to a
default day_plan = {
    'Morning' : 'Eat',
    'Afternoon' : 'Drink',
    'Evening' : 'Be Merry'
    }

# These variables display statistics to the player.
default stat_strength = 10
default stat_intelligence = 25
default stat_moxie = 100
default stat_chutzpah = 75

# These styles are used to style the various stats.
style stat_text is default:
    min_width 150
    text_align 1.0
    yalign 0.5

style stat_hbox is hbox:
    spacing 10

style stat_vbox:
    spacing 5


# This is the day planner screen. It displays the

screen day_planner():

    # This vbox organizes everything.
    vbox:

        spacing 5

        # A frame containing all the stats.
        frame:
            style_prefix "stat"
            xpadding 150
            xfill True

            vbox:

                hbox:
                    text _("Strength")
                    bar value StaticValue(stat_strength, 100)

                hbox:
                    text _("Intelligence")
                    bar value StaticValue(stat_strength, 100)

                hbox:
                    text _("Moxie")
                    bar value StaticValue(stat_strength, 100)

                hbox:
                    text _("Chutzpah")
                    bar value StaticValue(stat_strength, 100)


        # A grid of three frames, one for each of the periods in the day.
        grid 3 1:

            spacing 5
            xfill True

            for p in day_periods:

                frame:
                    xfill True

                    vbox:
                        label p

                        null height 5

                        for i in day_choices:
                            textbutton i action SetDict(day_plan, p, i)

        # This is a grid containing two empty space and the done button,
        # so everything lines up.
        grid 3 1:
            xfill True
            spacing 5

            null

            frame:
                textbutton "Done":
                    action Return(True)
                    xfill True

                    text_xalign 0.5

            null





label tutorial_screens:

    e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."

label screens_menu:

    $ reset_example()

    menu:

        e "What would you like to know about screens?"

        "What can screens do?":
            call screens_demo

        "How to show screens.":
            call screens_showing

        "Passing parameters to screens.":
            call screens_parameters

        "Screen properties.":
            call screens_properties

        "That's it.":
            return

    jump screens_menu


label screens_demo:

    e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."

    e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."

    menu:

        e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?"

        "Yes.":
            pass

        "I do.":
            pass

    e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."

    e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."

    e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."

    e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."

    e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."

    $ player_hp = 15

    show screen stats
    with dissolve

    e "For example, in an RPG like visual novel, a screen can display the player's statistics."

    $ player_hp = 42

    e "Which reminds me, I should probably heal you."

    hide screen stats
    show screen day_planner

    with dissolve

    e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."

    hide screen day_planner
    with dissolve

    e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."

    return




label screens_showing:

    example large:
        screen simple_screen():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "This is a screen."
                    textbutton "Okay":
                        action Return(True)


    e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."

    e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."

    show screen simple_screen

    e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."

    e "The text statement is used to display the text provided."

    e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."

    e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."

    e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."

    hide screen simple_screen
    hide screen example

    e "There are a trio of statements that are used to display screens."

    example:
        show screen simple_screen

        e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."

        e "The screen will stay shown until it is hidden."

        hide screen simple_screen

        e "Hiding a screen is done with the hide screen statement."

    show example call_screen

    e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."

    e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."

    hide example

    example call_screen hide:
        call screen simple_screen

    e "When a call screen statement ends, the screen is automatically hidden."

    e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."

    return


label screens_parameters:

    example large:
        screen parameter_screen(message, okay=Return(True), cancel=Return(False)):
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "[message]"
                    textbutton "Okay":
                        action okay
                    textbutton "Cancel":
                        action cancel

    example hide show_parameter_screen:
        show screen parameter_screen(_("Hello, world."), cancel=Notify(_("You can't cancel this.")))

    with dissolve

    e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."

    e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."

    e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."

    show example show_parameter_screen

    e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."

    example:
        show screen parameter_screen(_("Shiro was here."))

    with dissolve

    e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."

    hide screen parameter_screen
    with dissolve

    show example call_parameter_screen

    e "The call screen statement can also take arguments, much like show screen does."

    hide example

    example hide call_parameter_screen:
        call screen parameter_screen(_("Click either button to continue."))

    return


label screens_properties:

    e "There are a few properties that can be applied to a screen itself."

    example large:
        screen modal_example():
            modal True

            frame:
                xalign 0.5 ypos 50
                textbutton _("Close This Screen"):
                     action Hide("modal_example")

    show screen modal_example
    with dissolve

    e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."

    example:
        screen a_tag_screen():
            tag tag_screen

            frame:
                xalign 0.33 ypos 50
                text _("A Tag Screen")

        screen b_tag_screen():
            tag tag_screen

            frame:
                xalign 0.66 ypos 50
                text _("B Tag Screen")


    show screen a_tag_screen
    with dissolve

    e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."

    show screen b_tag_screen

    e "When I show b_tag_screen, it replaces a_tag_screen."

    e "This is useful in the game and menus, where you'd want the load screen to replace the preferences screen. All those screens have tag menu."

    show eileen concerned

    e "For some reason, tag takes a name, and not an expression. It's too late to change it."

    show eileen happy
    with None

    hide screen b_tag_screen

    example:
        screen zorder_100_screen():
            zorder 100
            frame:
                xalign 0.5 xoffset 50 ypos 70
                text "Zorder 100"

        screen zorder_0_screen():
            frame:
                xalign 0.5 ypos 50
                text "Zorder 0"

        show screen zorder_100_screen
        show screen zorder_0_screen

    with dissolve

    e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."

    e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."

    example:

        screen variant_screen():
            variant "small"
            frame:
                xalign 0.5 ypos 50
                text _("You're on a small device.")

        screen variant_screen():
            frame:
                xalign 0.5 ypos 50
                text _("You're not on a small device.")

    hide screen zorder_100_screen
    hide screen zorder_0_screen
    show screen variant_screen
    with dissolve

    e "The variant property selects a screen based on the properties of the device it's running on."

    e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."


    example:

        screen style_prefix_screen():
            style_prefix "red"

            frame:
                xalign 0.5 ypos 50
                text _("This text is red.")

        style red_frame:
            background "#440000d9"

        style red_text:
            color "#ffc0c0"

    hide screen variant_screen
    show screen style_prefix_screen
    with dissolve

    e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."

    e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."

    e "This can save a lot of typing when styling screens with many displayables in them."

    hide example
    hide screen style_prefix_screen
    with dissolve

    return







label imagemap_tutorial:

    show example imagemap

    e "Another type of screen is an imagemap. An imagemap uses images that display hotspots that act as buttons."

    e "This imagemap uses two images - one when a button is idle, and one when a button is hovered. The idle image also doubles as a background."

    e "When a player clicks on a hotspot, this imagemap runs a Jump action to take them to a label. Each hotspots also has alt text, for vision-impared players."

    hide example

    e "Let's take a look at an imagemap screen in action."

    jump imagemap_example

example imagemap hide:
    screen imagemap_example:

        imagemap:
            ground "imagemap ground"
            hover "imagemap hover"

            hotspot (44, 238, 93, 93) action Jump("swimming") alt "Swimming"
            hotspot (360, 62, 93, 93) action Jump("science") alt "Science"
            hotspot (726, 106, 93, 93) action Jump("art") alt "Art"
            hotspot (934, 461, 93, 93) action Jump("go home") alt "Go Home"

    label imagemap_example:

        # Call the imagemap_example screen.
        call screen imagemap_example

    label swimming:

        e "You chose swimming."

        e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."

        jump imagemap_done

    label science:

        e "You chose science."

        e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."

        jump imagemap_done

    label art:
        e "You chose art."

        e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."

        jump imagemap_done

    label home:

        e "You chose to go home."

        jump imagemap_done

    label imagemap_done:

        e "Anyway..."

label after_imagemap_example:

    show screen stats
    with dissolve

    e "Screens can do a lot. For example, if a game is an RPG - or even RPG-themed - we can display statistics to the player."

    hide screen stats
    with dissolve

    window show

    $ e("For a dating sim or life simulation game, we can display scheduling interfaces like this one.", interact=False)
    call screen day_planner

    e "Screens can also be used to customize all parts of the Ren'Py interface - for example, the say screen is what shows dialogue to the player."

    e "Screens might look complicated, and more complex ones can have a lot of code in them. But every screen is made out of lots of small parts."

    return
