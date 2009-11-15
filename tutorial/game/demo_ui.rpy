# This file contains a demonstration of the user interaction
# functions.

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

            periods = [ 'Morning', 'Afternoon', 'Evening' ]
            choices = [ 'Study', 'Exercise',
                        'Eat', 'Drink', 'Be Merry' ]

            plan = { 'Morning' : 'Eat',
                     'Afternoon' : 'Drink',
                     'Evening' : 'Be Merry' }

            day = 'March 25th'

            stats = [
                ('Strength', 100, 10),
                ('Intelligence', 100, 25),
                ('Moxie', 100, 100),
                ('Chutzpah', 100, 75),
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

                ui.text('Statistics')
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
                    face = i + ": " + plan[i]
                    button(face, editing == i, ("edit", i), xminimum=250)

                ui.null(height=20)
                ui.textbutton("Continue",
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
                    ui.text("What will you do in the %s?" % editing.lower())
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
                e("To get to the next screen, click the 'Continue' button.", interact=False)

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

    e "We can also prompt the user to enter some text."

    $ povname = renpy.input("What is your name?") or "Guy Shy"

    pov "My name is %(povname)s."

    
    e "Imagemaps let the user click on an image to make a choice. For example, the following screen lets you pick what to do after school:"

    window hide None
    
    # This is an imagemap. It consists of two images, and a list of
    # hotspots. For each hotspot we give the coordinates of the left,
    # top, right, and bottom sides, and the value to return if it is
    # picked.

    $ result = renpy.imagemap("ground.jpg", "hover.jpg", [
        (8, 200, 86, 278, "swimming"),
        (204, 50, 282, 128, "science"), 
        (452, 79, 530, 157, "art"),
        (602, 316, 680, 394, "go home"),
        ], focus="imagemap")

    # We've assigned the chosen result from the imagemap to the
    # result variable. We can use an if statement to vary what
    # happens based on the user's choice.

    window show None
    
    if result == "swimming":

        e "You chose swimming."
        
        e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."

    elif result == "science":

        e "You chose science."
        
        e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
        
    elif result == "art":

        e "You chose art."
        
        e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."

    elif result == "go home":

        e "You chose to go home."

    e "Anyway..."

    e "We also support viewports, that allow us to display things that are bigger then the screen."

    e "This viewport can be adjusted by dragging, by the mouse wheel, and by the scrollbars."

    window hide
    
    show eileen happy at right
    with move
    
    python hide:

        ui.side(('c', 'b', 'r'), xpos=100, ypos=50, spacing=5)
        
        vp = ui.viewport(draggable=True, mousewheel=True, xmaximum=400, ymaximum=400)
        ui.image("concert2.jpg")
        ui.bar(adjustment=vp.xadjustment, style='scrollbar')
        ui.bar(adjustment=vp.yadjustment, style='vscrollbar')

        ui.close()
        
        ui.textbutton("Dismiss", xpos=300, xanchor=0.5, ypos=550, yanchor=0.5, clicked=ui.returns(True))
        ui.interact()

    show eileen happy at center
    with move

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
