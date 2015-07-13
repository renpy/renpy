# This file contains a demonstration of the user interaction
# functions.

screen viewport_screen:

    viewport:
        scrollbars "both"
        xmaximum 400
        ymaximum 400

        side_xpos 100
        side_ypos 100
        side_spacing 5

        draggable True
        mousewheel True

        add "concert2"

    textbutton _("Dismiss"):
        xpos 300
        xanchor 0.5
        ypos 550
        yanchor 0.5

        action Return(True)

screen edgescroll_screen:

    viewport:
        edgescroll (150, 500)
        add "concert2"

screen demo_imagemap:
    imagemap:
        auto "imagemap_%s.jpg"

        hotspot (8, 200, 78, 78) action Return("swimming") alt "Swimming"
        hotspot (204, 50, 78, 78) action Return("science") alt "Science"
        hotspot (452, 79, 78, 78) action Return("art") alt "Art"
        hotspot (602, 316, 78, 78) action Return("go home") alt "Go Home"

init:

    # The variable we store the entered name of the character in.
    $ povname = ""

    # And this is a DynamicCharacter that has the same stored in
    # povname.
    $ pov = DynamicCharacter("povname", color=(192, 64, 64, 255))


    # This is code for a day planner, or at least sort of. To be
    # honest, the code in the dse game is a bit better. Take this
    # as more of an example of what Ren'Py can do.
    python:
        def day_planner():

            periods = [ _('Morning'), _('Afternoon'), _('Evening') ]
            periods_small = {'Morning': _('morning'), 'Afternoon': _('afternoon'), 'Evening': _('evening') }
            choices = [ _('Study'), _('Exercise'),
                        _('Eat'), _('Drink'), _('Be Merry') ]

            plan = { _('Morning') : _('Eat'),
                     _('Afternoon') : _('Drink'),
                     _('Evening') : _('Be Merry') }

            day = _('March 25th')

            stats = [
                (_('Strength'), 100, 10),
                (_('Intelligence'), 100, 25),
                (_('Moxie'), 100, 100),
                (_('Chutzpah'), 100, 75),
                ]

            editing = None

            def button(text, selected, returns, **properties):

                if selected:
                    role='selected_'
                else:
                    role=''

                ui.button(clicked=ui.returns(returns),
                          style='button', role=role, **properties)
                ui.text(text, style='button_text')


            while True:

                # Stats Window
                ui.frame(xpos=0,
                         ypos=0,
                         xanchor='left',
                         yanchor='top',
                         xfill=True,
                         )

                ui.vbox()

                ui.text(_('Statistics'))
                ui.null(height=20)

                for name, range, value in stats:

                    ui.hbox()
                    ui.text(name, minwidth=150)
                    ui.bar(range, value, ypos=0.5, yanchor='center')
                    ui.close()

                ui.close()

                # Period Selection Window.
                ui.frame(xpos=0,
                         ypos=200,
                         xanchor='left',
                         yanchor='top',
                         xfill=False,
                         xminimum=300
                         )

                ui.vbox(xpos=0.5, xanchor='center')
                ui.text(day, xpos=0.5, xanchor='center', textalign=0.5)
                ui.null(height=20)

                for i in periods:
                    renpy.store.period_tmp = i
                    renpy.store.plan_tmp = plan[i]
                    button("[period_tmp!t]: [plan_tmp!t]", editing == i, ("edit", i), xminimum=250)

                ui.null(height=20)
                ui.textbutton(_("Continue"),
                              clicked=ui.returns(("done", True)),
                              xminimum=250)
                ui.null(height=20)
                ui.close()


                # Choice window.
                if editing:
                    ui.frame(xpos=300,
                             ypos=200,
                             xanchor='left',
                             yanchor='top',
                             xfill=False,
                             xminimum=500,
                             xmargin = 10
                             )

                    ui.vbox()
                    renpy.store.periods_small_selected = periods_small[editing]
                    ui.text(_("What will you do in the [periods_small_selected!t]?"))
                    ui.null(height=20)

                    for i in choices:
                        button(i,
                               plan[editing] == i,
                               ("set", i),
                               xpos=0,
                               xanchor='left',
                               xminimum=250)

                    ui.close()

                # Window at the bottom.
                e(_("To get to the next screen, click the 'Continue' button."), interact=False)

                type, value = ui.interact()

                if type == "done":
                    break

                if type == "edit":
                    editing = value

                if type == "set":
                    plan[editing] = value
                    editing = None

            return plan

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

    $ day_planner()

    show eileen happy
    with dissolve

    e "For a better implementation of this, take a look at the dating sim engine (DSE) that ships with Ren'Py."

    call fight("Eileen", 10, 99, pname=povname) from _call_fight_1

    e "The ui functions can be also be used to show the sorts of stats you'd need if your game involves combat."

    call fight("Eileen", 10, 99, pname=povname) from _call_fight_2

    e "Hopefully, the ui functions will let you write whatever visual novel or dating sim you want."

    return
