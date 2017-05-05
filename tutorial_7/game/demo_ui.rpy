# This file contains a demonstration of the user interaction
# functions.

screen viewport_screen():

    viewport:
        scrollbars "both"
        xmaximum 711
        ymaximum 400

        side_xpos 100
        side_ypos 100
        side_spacing 5

        draggable True
        mousewheel True
        arrowkeys True

        add "bg band"

    textbutton _("Dismiss"):
        xpos 455
        xanchor 0.5
        ypos 550
        yanchor 0.5

        action Return(True)

screen edgescroll_screen():

    viewport:
        edgescroll (150, 500)
        add "concert2"


default povname = "Player"
define pov = Character("[povname]", color="#c44")


label demo_ui:

    e "Ren'Py gives a number of ways of interacting with the user."

    e "You've already seen say statements and menus."

    menu:

        e "But were you aware that you can have dialogue and menus onscreen at the same time?"

        "Yes.":

            show eileen vhappy

            e "Good!"

            show eileen happy

        "No.":

            e "Well, now you know."

    if not renpy.variant('touch'):

        e "We can also prompt the user to enter some text."

        $ povname = renpy.input(_("What is your name?")) or _("Guy Shy")

        pov "My name is [povname!t]."


    e "Imagemaps let the user click on an image to make a choice. For example, the following screen lets you pick what to do after school:"

    # Show an imagemap.
    window hide None
    call screen demo_imagemap
    window show None

    # Call screen assignes the chosen result from the imagemap to the
    # _return variable. We can use an if statement to vary what
    # happens based on the user's choice.

    if _return == "swimming":

        e "You chose swimming."

        e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."

    elif _return == "science":

        e "You chose science."

        e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."

    elif _return == "art":

        e "You chose art."

        e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."

    elif _return == "go home":

        e "You chose to go home."

    e "Anyway..."

    e "We also support viewports, that allow us to display things that are bigger than the screen."

    e "This viewport can be adjusted by dragging, by the mouse wheel, and by the scrollbars."

    window hide

    show eileen happy at right
    with move

    call screen viewport_screen

    show screen edgescroll_screen
    with dissolve


    e "Viewports also support edge scrolling, which is automatic scrolling when the mouse reaches their edge."

    hide screen edgescroll_screen
    show eileen happy at center
    with dissolve

    window show

    e "While these constructs are probably enough for most visual novels, dating simulations may be more complicated."

    e "The ui functions allow you to create quite complicated interfaces."

    e "For example, try the following scheduling and stats screen, which could be used by a stat-based dating simulation."

    hide eileen
    with dissolve

    call screen day_planner

    show eileen happy
    with dissolve

    e "For a better implementation of this, take a look at the dating sim engine (DSE) that ships with Ren'Py."

    call fight("Eileen", 10, 99, pname=povname) from _call_fight_1

    e "The ui functions can be also be used to show the sorts of stats you'd need if your game involves combat."

    call fight("Eileen", 10, 99, pname=povname) from _call_fight_2

    e "Hopefully, the ui functions will let you write whatever visual novel or dating sim you want."

    return
