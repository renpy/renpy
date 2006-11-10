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
                style='selected_button'
                style_text='selected_button_text'
                    
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
                ui.textbutton("Continue", clicked=ui.returns(("done", True)), xminimum=250)
                ui.null(height=20)
                ui.close()


                # Choice window.
                if editing:
                    ui.frame(xpos=300,
                              ypos=200,
                              xanchor='left',
                              yanchor='top',
                              xfill=False,
                              xminimum=500
                              )
                
                    ui.vbox()
                    ui.text("What will you do in the %s?" % editing.lower())
                    ui.null(height=20)

                    for i in choices:
                        button(i, plan[editing] == i, ("set", i),
                               xpos=0, xanchor='left')

                    ui.close()

                # Window at the bottom.
                ui.window()
                ui.vbox()
                ui.text("To get to the next screen, click the 'Continue' button.")
                ui.close()

                type, value = ui.interact()

                if type == "done":
                    break

                if type == "edit":
                    editing = value

                if type == "set":
                    plan[editing] = value
                    editing = None

            return plan

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

    $ povname = renpy.input("What is your name?")

    pov "My name is %(povname)s."

    
    e "Imagemaps let the user click on an image to make a choice. For example, the following screen lets you pick what to do after school:"

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

    if result == "swimming":

        e "You chose swimming."
        
        e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."

    elif result == "science":

        e "You chose science."
        
        e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
        
    elif result == "art":

        e "You chose art."
        
        e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can chage that."

    elif result == "go home":

        e "You chose to go home."

    e "Anyway..."
                
    e "While these constructs are probably enough for most visual novels, dating simulations may be more complicated."

    e "The ui functions allow you to create quite complicated interfaces."

    e "For example, try the following scheduling and stats screen, which could be used by a stat-based dating simulation."

    $ day_planner()

    e "For a better implementation of this, take a look at the dating sim engine (DSE) that ships with Ren'Py."
    
    e "The ui functions can be used to rewrite many parts of the interface."

    e "Hopefully, the ui functions will let you write whatever visual novel or dating sim you want."

    return
