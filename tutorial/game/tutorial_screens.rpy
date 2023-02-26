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
                text "[name!t]" min_width 220
                text _(" Lv. [lv]")

            hbox:
                text _("HP"):
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
    min_width 200
    textalign 1.0
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
                textbutton _("Done"):
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

        "What screens can do.":
            call screens_demo

        "How to show screens.":
            call screens_showing

        "Passing parameters to screens.":
            call screens_parameters

        "Screen properties.":
            call screens_properties

        "Special screen statements.":
            call screens_control

        "Using other screens.":
            call screen_use

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

    example large noshow:
        screen simple_screen():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text _("This is a screen.")
                    textbutton _("Okay"):
                        action Return(True)


    e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and its name is simple_screen." id screens_showing_1b51e9a4

    e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."

    show screen simple_screen
    with dissolve

    e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."

    e "The text statement is used to display the text provided."

    e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."

    e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."

    e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."

    hide screen simple_screen
    hide example
    with dissolve

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

    example large noshow:
        screen parameter_screen(message, okay=Return(True), cancel=Return(False)):
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "[message!t]"
                    textbutton _("Okay"):
                        action okay
                    textbutton _("Cancel"):
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


    e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."

    show screen b_tag_screen

    e "When I show b_tag_screen, it replaces a_tag_screen."

    e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."

    show eileen concerned

    e "For some reason, tag takes a name, and not an expression. It's too late to change it."

    show eileen happy
    with None

    hide screen b_tag_screen

    example noshow:
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



    hide screen zorder_100_screen
    hide screen zorder_0_screen

    example nohide:

        screen variant_screen():
            variant "small"
            frame:
                xalign 0.5 ypos 50
                text _("You're on a small device.")

        screen variant_screen():
            frame:
                xalign 0.5 ypos 50
                text _("You're not on a small device.")

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


    e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."

    e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."

    e "This can save a lot of typing when styling screens with many displayables in them."

    hide example

    return

label warp_screen_displayables:
    $ renpy.pop_call()
    jump screen_displayables

label screens_control:

    e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."

    example large:
        screen single_python_screen():

            $ message = _("Hello, World.")

            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "[message!t]"

    e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."

    example large:
        screen block_python_screen():

            python:
                message1 = _("Hello, World.")
                message2 = _("It's good to meet you.")

            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "[message1!t]"
                    text "[message2!t]"

    e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."

    e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."

    e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."

    example large:

        screen default_screen():

            default n = 0

            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "n = [n]"
                    textbutton _("Increase") action SetScreenVariable("n", n + 1)

    e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."

    e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."


    example large:

        screen if_screen():

            default n = 0

            frame:
                xalign 0.5 ypos 50
                vbox:
                    if n > 2:
                        text "n = [n]" color "#cfc"
                    else:
                        text "n = [n]" color "#fcc"

                    textbutton _("Increase") action SetScreenVariable("n", n + 1)

    e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."

    example large:

        screen for_screen():

            $ landings = [ _("Earth"), _("Moon"), _("Mars") ]

            frame:
                xalign 0.5 ypos 50

                vbox:
                    for i in landings:
                        textbutton "[i!t]" action Return(i)

    e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."

    example large:

        screen on_key_screen():

            frame:
                xalign 0.5 ypos 50

                text _("Now press 'a'.")

            on "show" action Notify(_("The screen was just shown."))

            key "a" action Notify(_("You pressed the 'a' key."))


    e "The on and key statements probably only make sense at the top level of the screen."

    e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."

    e "The key event runs an event when a key is pressed."

    hide example

    return

label screen_use:

    e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."

    example large:

        screen duplicate_stats():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text _("Health") xalign 0.5
                    bar value StaticValue(90, 100) xalign 0.5 xsize 250

                    null height 15

                    text _("Magic") xalign 0.5
                    bar value StaticValue(42, 100) xalign 0.5 xsize 250

    e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."

    example large:

        screen using_stats():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    use stat(_("Health"), 90)
                    null height 15
                    use stat(_("Magic"), 42)

        screen stat(name, amount):

            text name xalign 0.5
            bar value StaticValue(amount, 100) xalign 0.5 xsize 250

    e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."

    e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."

    e "By doing it this way, we control the amount of duplication, and can change the stat in one place."

    example large:

        screen transclusion_example():

            use boilerplate():
                text _("There's not much left to see.")

        screen boilerplate():
            frame:
                xalign 0.5 ypos 50

                vbox:
                    transclude

    e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."

    e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."

    e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."

    e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."

    hide example
    return
