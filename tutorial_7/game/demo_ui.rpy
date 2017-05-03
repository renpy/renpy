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

screen demo_imagemap:
    imagemap:
        auto "imagemap %s"

        hotspot (44, 238, 93, 93) action Return("swimming") alt "Swimming"
        hotspot (360, 62, 93, 93) action Return("science") alt "Science"
        hotspot (726, 106, 93, 93) action Return("art") alt "Art"
        hotspot (934, 461, 93, 93) action Return("go home") alt "Go Home"

default povname = "Player"
define pov = Character("[povname]", color="#c44")


define day_periods = [ _('Morning'), _('Afternoon'), _('Evening') ]
define day_choices = [ _('Study'), _('Exercise'), _('Eat'), _('Drink'), _('Be Merry') ]

default day_plan = { _('Morning') : _('Eat'),
                     _('Afternoon') : _('Drink'),
                     _('Evening') : _('Be Merry') }
default day = _('March 25th')

default stat_strength = 10
default stat_intelligence = 25
default stat_moxie = 100
default stat_chutzpah = 75


style stat_text is default:
    min_width 150
    text_align 1.0
    yalign 0.5


style stat_hbox is hbox:
    spacing 10

style stat_vbox:
    spacing 5

screen day_planner():

    # This displays the stats at the top of the screen.

    vbox:

        spacing 5

        frame:
            style_prefix "stat"

            xpadding 150


            xfill True

            has vbox

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



init python:

    def stats_frame(name, level, hp, maxhp, **properties):

        ui.frame(xfill=False, yminimum=None, **properties)

        ui.hbox() # (name, "HP", bar) from (level, hp, maxhp)
        ui.vbox() # name from ("HP", bar)

        ui.text(name, size=20)

        ui.hbox() # "HP" from bar
        ui.text("HP", size=20)
        ui.bar(maxhp, hp,
               xmaximum=150)

        ui.close()
        ui.close()

        ui.vbox() # Level from (hp/maxhp)

        ui.text("Lv. %d" % level, xalign=0.5, size=20)
        ui.text("%d/%d" % (hp, maxhp), xalign=0.5, size=20)

        ui.close()
        ui.close()

label fight(ename, elevel, ehp, pname="Zanthier", plevel=4, php=40):
    $ stats_frame(pname, plevel, int(php * .73), php, xalign=.02, yalign=.05)
    $ stats_frame(ename, elevel, ehp, ehp, xalign=.98, yalign=.05)

    return

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
