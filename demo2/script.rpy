# This script, but not the artwork associated with it, is in the
# public domain. Feel free to use it as the basis for your own
# game.

# If you're trying to understand this script, I recommend skipping
# down to the line beginning with 'label start:', at least on your
# first read-through.

# This init block runs first, and sets up all sorts of things that
# are used by the rest of the game. Variables that are set in init
# blocks are _not_ saved, unless they are changed later on in the
# program.

init:

    # Set up the size of the screen, and the window title.
    $ config.screen_width = 800
    $ config.screen_height = 600
    $ config.window_title = "The Ren'Py Demo Game"

    # Change some styles, to add images in the background of
    # the menus and windows.
    $ style.mm_root_window.background = Image("mainmenu.jpg")
    $ style.gm_root_window.background = Image("gamemenu.jpg")
    $ style.window.background = Frame("frame.png", 125, 25)

    # Interface sounds, just for the heck of it.
    $ style.button.activate_sound = 'click.wav'
    $ style.imagemap.activate_sound = 'click.wav'
    $ library.enter_sound = 'click.wav'
    $ library.exit_sound = 'click.wav'

    # These are positions that can be used inside at clauses. We set
    # them up here so that they can be used throughout the program.
    $ left = Position(xpos=0.0, xanchor='left')
    $ right = Position(xpos=1.0, xanchor='right')
    $ center = Position()

    # Likewise, we set up some transitions that we can use in with
    # clauses and statements.
    $ fade = Fade(.5, 0, .5) # Fade to black and back.
    $ dissolve = Dissolve(0.5)
    
    $ wiperight = CropMove(1.0, "wiperight")
    $ wipeleft = CropMove(1.0, "wipeleft")
    $ wipeup = CropMove(1.0, "wipeup")
    $ wipedown = CropMove(1.0, "wipedown")

    $ slideright = CropMove(1.0, "slideright")
    $ slideleft = CropMove(1.0, "slideleft")
    $ slideup = CropMove(1.0, "slideup")
    $ slidedown = CropMove(1.0, "slidedown")

    $ slideawayright = CropMove(1.0, "slideawayright")
    $ slideawayleft = CropMove(1.0, "slideawayleft")
    $ slideawayup = CropMove(1.0, "slideawayup")
    $ slideawaydown = CropMove(1.0, "slideawaydown")

    $ irisout = CropMove(1.0, "irisout")
    $ irisin = CropMove(1.0, "irisin")

    # Select the transitions that are used when entering and exiting
    # the game menu.
    $ library.enter_transition = dissolve
    $ library.exit_transition = dissolve

    # Now, we declare the images that are used in the program.

    # Backgrounds.
    image carillon = Image("carillon.jpg")
    image whitehouse = Image("whitehouse.jpg")
    image washington = Image("washington.jpg")
    image black = Solid((0, 0, 0, 255))

    # Character pictures.
    image eileen happy = Image("9a_happy.png")
    image eileen vhappy = Image("9a_vhappy.png")
    image eileen concerned = Image("9a_concerned.png")

    # Finally, the character object. This object lets us have the
    # character say dialogue without us having to repeatedly type
    # her name. It also lets us change the color of her name.
    
    # Character objects.
    $ e = Character('Eileen', color=(200, 255, 200, 255))

# The splashscreen is called, if it exists, before the main menu is
# shown the first time. It is not called if the game has restarted.

# We'll comment it out for now.
#
# label splashscreen:
#     scene black
#     show text "American Bishoujo Presents..." with fade
#     $ renpy.pause(1.0)
#     hide text with fade
#
#     return

# The start label marks the place where the main menu jumps to to
# begin the actual game.

label start:

    # The save_name variable sets the name of the save game. Like all
    # variables declared outside of init blocks, this variable is
    # saved and restored with a save file.
    $ save_name = "Introduction"

    # This variable is only used by our game. If it's true, it means
    # that we won the date.
    $ date = False

    # Clear the game runtime timer, so it doesn't reflect time spent
    # sitting at the main menu.
    $ renpy.clear_game_runtime()

    # Start some music playing in the background.
    $ renpy.music_start('sun-flower-slow-drag.mid')

    # Now, set up the first scene. We first fade in our washington
    # background, and then we dissolve in the image of Eileen on top
    # of it.
    scene washington with fade
    show eileen vhappy with dissolve

    # Display a line of dialogue. In this case, we manually specify
    # who's saying the line of dialoge.    
    "Girl" "Hi, and welcome to the Ren'Py 4 demo program."

    # This instantly replaces the very happy picture of Eileen with
    # one showing her merely happy. It demonstrates how the show
    # statement lets characters change emotions.
    show eileen happy

    # Another line of dialogue.
    "Girl" "My name is Eileen, and while I plan to one day star in a
            real game, for now I'm here to tell you about Ren'Py."

    # This line used the e character object, which displays Eileen's
    # name in green. The use of a short name for a character object
    # lets us save typing when writing the bulk of the dialogue.
    e "Ren'Py is a language and engine for writing and playing visual
       novel games."

    e "Our goal is to allow people to be able to write the script for
       a game, and with very little effort, turn that script into
       a working game."

    e "I can tell you about the features of Ren'Py games, or how to write
       your own game. What do you want to know about?"

    # This variable is used to save the choices that have been made in
    # the main menu.
    $ seen_set = [ ]

label choices:

    # We change the save name here.
    $ save_name = "Question Menu"

    # This is the main menu, that lets the user decide what he wants
    # to hear about.
    menu:

        # The set menu clause ensures that each menu choice can only
        # be chosen once.
        set seen_set

        # This is a menu choice. When chosen, the statements in its
        # block are executed.
        "What are some features of Ren'Py games?":

            # We call the features label. The from clause needs to be
            # here to ensure that save games work, even after we
            # change the script. It was added automatically.
            call features from _call_features_1

            # When we're done talking about features, jump back up
            # to choices.
            jump choices

        # Another choice. 
        "How do I write my own games with it?":
            call writing from _call_writing_1
            jump choices

        "What's new with Ren'Py?":
            call whatsnew from _call_whatsnew_1
            jump choices

        # This choice has a condition associated with it. It is only
        # displayed if the condition is true (in this case, if we have
        # selected at least one other choice has been chosen.) 
        "Where can I find out more?" if seen_set:
            call find_out_more from _call_find_out_more_1
            jump choices

        "Why are we in Washington, DC?":
            call washington from _call_washington_1
            jump choices

        "I think I've heard enough." if seen_set:
            jump ending


# This is the section on writing games.
label writing:

    # Change the title of the save games.
    $ save_name = "Writing Games"

    # We start off with a bunch of dialogue.
    e "If you want to write a game, I recommend that you read the
       Ren'Py tutorial, which you can get from our web page,
       http://www.bishoujo.us/renpy/."

    e "But here, we'll go over some of the basics of writing Ren'Py
       scripts. It might make sense if you open the source for this
       game."

    e "The source for this game can be found in the file
       game/script.rpy."

    e "The goal of Ren'Py is to make writing the game similar to
       typing up the script on the computer."

    e "For example, a line of dialogue is expressed by putting the
       character's name next to the dialogue string."

    # A string by itself like this displays without a name associated
    # with it. So it's useful for dialogue and narration.
    "I somehow remember that strings by themselves are displayed as
     thoughts or narration."
    
    e "The menu statement makes it easy to create menus."

    e "A number of statements let you control what is shown on the
       screen."

    # This scene statement has a with clause associated with it. In
    # this case (based on what is defined in the init clause at the
    # top of this script), it causes a fade to black, and then back
    # to the new scene.
    scene whitehouse with fade

    e "The scene statement clears the scene list, which is the list of
       things that are shown on the screen."

    # This shows an image, and dissolves it in.
    show eileen happy with dissolve

    e "The show statement shows another image on the screen."

    # The at clause here, displays the character on the left side of
    # the screen.
    show eileen happy at left with dissolve

    e "Images can take at clauses that specify where on the screen
       they are shown."

    show eileen vhappy at left

    e "Showing a new image with the same first part of the name
       replaces the image in the scene list."

    hide eileen with dissolve

    e "Finally, the hide statement hides an image, which is useful
       when a character leaves the scene."

    show eileen happy with dissolve

    e "Don't worry, I'm not going anywhere."

    e "The with statement is used to cause transitions to
       happen. Transitions like fade..."

    # This statement hides the transient stuff from being included
    # in the next fade.
    with None

    # This with statement causes things to fade without changing the
    # scene.
    with fade

    e "... or dissolve ..."

    # In this block, the scene statement clears the scene list. So we
    # have to reshow the eileen happy image, so that it appears that
    # just the background is dissolving. Sneaky.
    with None
    scene washington
    show eileen happy
    with dissolve

    e "... are easily invoked."

    e "As of version 4.2, Ren'Py supports image maps, which are like
       another form of menu. Let's try one."

    # This is an imagemap. It consists of two images, and a list of
    # hotspots. For each hotspot we give the coordinates of the left,
    # top, right, and bottom sides, and the value to return if it is
    # picked.

    $ result = renpy.imagemap("ground.png", "selected.png", [
        (100, 100, 300, 400, "eileen"),
        (500, 100, 700, 400, "lucy")
        ])

    # We've assigned the chosen result from the imagemap to the
    # result variable. We can use an if statement to vary what
    # happens based on the user's choice.

    if result == "eileen":
        show eileen vhappy
        e "You picked me!"

    elif result == "lucy":
        show eileen concerned
        e "It looks like you picked Lucy."

        # Eileen is being a bit possesive here. :-P
        if date:
            e "You can forget about Saturday."
            $ date = False

    show eileen happy

    e "Ren'Py supports music, such as what's playing in the
       background..."

    # This plays a sound effect.
    $ renpy.play("18005551212.wav")
    
    e "... and sound effects, like the one that just played."

    e "We now provide a series of user-interface functions, that allow
       the programmer to create fairly complex interfaces."

    e "For example, try the following scheduling and stats screen,
       which could be used by a stat-based dating simulation."

    $ day_planner()
    
    e "Ren'Py also includes a number of control statements, and even
       lets you include python code."

    e "Rather than go into this here, you can read all about it in the
       tutorial."

    e "If you want to make changes, you can edit the script for this
       game by editing game/script.rpy"

    e "When you've made a change, just re-run the game to see your
       change in action."

    e "Would you like to know about something else?"

    # We return back up to the menu that lets the user pick a topic.
    return

# This ends the well-commented portion of this script.

label features:

    $ save_name = "Features"

    e "By providing a range of useful features, we let game authors
       focus on writing their games."

    e "What are some of these features? Well, first of all, we take
       care of displaying the screen, as well as dialogue and menus."

    e "You can navigate through the game using the keyboard or the
       mouse. If you've gotten this far, you've probably figured that
       out already."

    e "If you press 'f', you can toggle fullscreen mode. Pressing 'm'
       will toggle music on and off."

    e "Right-clicking or pressing escape will bring you to the game
       menu."

    e "The game menu lets you save or load the game. Ren'Py doesn't
       limit the number of save slots available. You can create as
       many slots as you can stand."

    e "The game menu also lets you restart or quit the game. But you
       wouldn't want to do that, would you?"

    e "Finally, the game menu lets you set up the game
       preferences. These preferences are saved between games."

    show eileen vhappy

    e "The next feature is really neat."

    show eileen happy

    menu rollback_menu:
        "Would you like to hear about rollback?"
        
        "Yes.":
            pass

        "No.":
            jump after_rollback


    e "Rollback is a feature that only Ren'Py has. It lets you go back
       in time in a game."

    e "For example, you can go back to a menu and save or make a
       different choice."

    e "You can access it by pressing page up or scrolling up on your
       mouse wheel."

    e "Why don't you try it by going back to the last menu and
       choosing 'No.' instead of 'Yes.'"

    e "Press page up or scroll up the mouse wheel."

    show eileen concerned

    e "Well, are you going to try it?"

    e "Your loss."

    e "Moving on."

label after_rollback:

    show eileen happy
    
    e "Ren'Py gives you a few ways of skipping dialogue. Pressing
       control quickly skips dialogue you've seen at least once."

    e "Pressing Tab toggles the skipping of dialogue you've seen at
       least once."

    e "Pressing page down or scrolling the mouse wheel down will let
       you skip dialogue you've seen this session. This is useful
       after a rollback."

    e "If you want to try these, you might want to rollback a bit
       first, so you can skip over something you've seen already."

    e "Finally, Ren'Py has predictive image loading, so you rarely
       have to wait for a new image to load."

    e "Remember, all these features are built into the engine or
       standard library. So every game written with Ren'Py has them."

    e "Is there anything else you'd like to know about?"
    
    return


label find_out_more:

    $ save_name = "Find Out More"

    e "There are a few places you can go to find out more about
       Ren'Py."

    e "The Ren'Py homepage, http://www.bishoujo.us/renpy/, is probably
       the best place to start."

    e "There, you can download new versions of Ren'Py, and read the
       tutorial online."

    e "If you have questions, the best place to ask them is the Ren'Py
       forum of the Lemmasoft forums."

    e "Just go to http://www.lemmasoft.net/forums/, and click on
       Ren'Py."

    e "We thank Blue Lemma for hosting our forum."

    e "Finally, feel free to email or IM us if you need help. You can
       get the addresses to use from http://www.bishoujo.us/renpy/."

    e "We really want people to make their own games with Ren'Py, and
       if there's anything we can do to help, just tell us."

    e "Is there anything I can help you with now?"

    return

label washington:

    $ save_name = "Washington, DC"

    e "We're in Washington, DC because over Summer 2004 American
       Bishoujo's home base was just outside of DC."

    scene whitehouse
    show eileen happy at left
    with fade

    e "Even though we've moved back to New York, we took a bunch of
       pictures, and decided to use them."

    show eileen concerned at left

    e "It was easier than drawing new pictures for this demo."

    show eileen happy at left
    
    e "Do you have a favorite landmark in or around DC?"

    menu:

        "The White House.":

            e "I was supposed to go on a tour of the West Wing, once."

            show eileen concerned

            e "They wouldn't let us in."

            e "The secret service guy who was supposed to show us
               around was out of town that day."

            e "Too bad."

        "The National Mall.":

            e "It's always fun to go down to the national mall."

            e "You can visit the monuments, or see one of the
               museums."

            e "I guess you could run out of things to do after a while
               but I didn't over the course of a summer."
            
        "The Netherlands Carillon.":
            jump netherlands
            
    jump post_netherlands

label netherlands:

    show eileen vhappy at left

    e "You've been to the Netherlands Carillon?"

    scene carillon
    show eileen vhappy at left
    with dissolve

    e "It may not be much to look at but the sound of the bells is
       really neat."

    e "I love going there. Saturdays during the summer, they have
       these recitals in the park where a guy comes and plays the 
       bells live."

    e "You can climb to the top and talk to him, if you're not afraid
       of heights."

    e "Once, I saw a little girl there, maybe three or four years old.
       The guy played the bumblebee song for here, and he even let her play the last
       note. It was so cute!"

    e "I haven't been there for so long."

    menu:
        "Would you like to go there sometime?":

            e "You mean, together?"

            e "Sure, why not. How does next Saturday sound?"
            
            e "It's a date."

            $ date = True

        "That sounds nice.":

            show eileen happy at left

            e "Well, it is."
        
label post_netherlands:

    scene washington
    show eileen happy
    with fade

    e "Anyway, is there anything else you want to know about Ren'Py?"

    return

label ending:

    $ save_name = "Ending"

    e "Well, that's okay."

    e "I hope you'll consider using Ren'Py for your next game
       project."

    show eileen vhappy

    e "Thanks for viewing this demo!"

    if date:
        e "And I'll see you on Saturday."
    
    scene black with fade

    "Ren'Py and the Ren'Py demo were written by PyTom."

    'The background music is "Sun Flower Slow Drag" by S. Joplin
     (1868-1917). Thanks to the Mutopia project for making it
       available.'

    'The author would like to thank everyone who makes original
     English-language bishoujo games, and the people on the Lemmasoft forums
     who encouraged him.'

    "We can't wait to see what you do with this. Good luck!"

    $ minutes, seconds = divmod(int(renpy.get_game_runtime()), 60)
    "It took you %(minutes)d minutes and %(seconds)d seconds to
     finish this demo."
       
    $ renpy.full_restart()

init:

    # This is just some example code to show the ui functions in
    # action. You probably want to delete this (and the call to
    # day_planner above) from your game. This code isn't really all
    # that useful except as an example.
    
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
                style = 'button'
                style_text = 'button_text'

                if selected:
                    style='selected_button'
                    style_text='selected_button_text'

                ui.button(clicked=ui.returns(returns),
                          style=style, **properties)
                ui.text(text, style=style_text)


            while True:

                # Stats Window
                ui.window(xpos=0,
                          ypos=0,
                          xanchor='left',
                          yanchor='top',
                          xfill=True,
                          yminimum=200,
                          )

                ui.vbox()

                ui.text('Statistics')
                ui.null(height=20)


                for name, range, value in stats:

                    ui.hbox()
                    ui.text(name, minwidth=150)
                    ui.bar(600, 20, range, value, ypos=0.5, yanchor=center)
                    ui.close()

                ui.close()
                
                

            
                # Period Selection Window.
                ui.window(xpos=0,
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
                    button(face, editing == i, ("edit", i))

                ui.null(height=20)
                ui.textbutton("Continue", clicked=ui.returns(("done", True)))
                ui.null(height=20)
                ui.close()


                # Choice window.
                if editing:
                    ui.window(xpos=300,
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

init:
    image movie = Movie()

    python:
        style.create('odd_window', 'say_window')
        style.odd_window.left_margin = 50
        style.odd_window.right_margin = 150
        style.odd_window.bottom_margin = 25

        eodd = Character('Eileen', color=(200, 255, 200, 255), window_style='odd_window')
    

label whatsnew:

    show washington
    show eileen happy

    e "I can give you a demonstration of some of the new features in
       Ren'Py, but you'll have to tell me what version you want to
       start with."

    menu:
        "I'd like to start with 4.5.":
            jump whatsnew45

        "I'd like to start with 4.6.":
            jump whatsnew46

label whatsnew45:

    show washington
    show eileen happy

    e "While most of the improvements in Ren'Py 4.5 were behind the scenes,
       we can give you a demonstration of one of the new features."

    e "There is now a new transition, CropMove, that can be used to
       provide a whole range of transition effects."

    hide eileen with dissolve

    e "I'll stand offscreen, so you can see some of its modes. I'll read
       out the mode name after each transiton."

    scene whitehouse with wiperight

    e "We first have wiperight..."

    scene washington with wipeleft

    e "...followed by wipeleft... "    

    scene whitehouse with wipeup

    e "...wipeup..."

    scene washington with wipedown

    e "...and wipedown."

    e "Next, the slides."

    scene whitehouse with slideright

    e "Slideright..."

    scene washington with slideleft

    e "...slideleft..."

    scene whitehouse with slideup

    e "...slideup..."

    scene washington with slidedown

    e "and slidedown."

    e "We also have a couple of transitions that use a rectangular iris."

    scene whitehouse with irisout

    e "There's irisout..."

    with None
    scene washington
    show eileen happy
    with irisin

    e "... and irisin."

    e "There are other transitions, such as various forms of
       slideaway. And if you can't find the transition for you, you
       can write a custom one."
    
    e "It's enough to make you feel a bit dizzy."

    e "Ren'Py 4.5 also includes the ability to show MPEG-1 movies as
       cutscenes or even backgrounds."

label ike:

    if renpy.exists('Eisenhow1952.mpg'):

        e "Since you downloaded the Eisenhower commercial, I can show
           it to you as a cutscene."

        e "You can click to continue if it gets on your nerves too
           much."

        $ renpy.movie_cutscene('Eisenhow1952.mpg', 63.0)
        
        hide eileen
        show movie at Position(xpos=420, ypos=25, xanchor='left', yanchor='top')
        show eileen happy

        $ renpy.movie_start_displayable('Eisenhow1952.mpg', (352, 240))

        e "Ren'Py can even overlay rendered images on top of a movie,
           although that's more taxing for your CPU."

        e "It's like I'm some sort of newscaster or something."
           
        $ renpy.movie_stop()
        hide movie

    else:

        e "You haven't download the Eisenhower commercial, so we
           can't demonstrate it."

label whatsnew46:

    eodd "As of 4.6, we now support separate padding and margin for the
          left, right, top, and bottom sides of a window."

    eodd "This means that a game can have oddly shaped windows without
          having to go beyond the style system."

    e "We also introduced a new layer system, and the ability to have
       transitions affect only one layer."

    e "Because of this we can do things like slide away a window..."

    $ renpy.transition(slideawayup, 'transient')
    $ renpy.pause(1.5)
    $ renpy.transition(slidedown, 'transient')
    
    e "... and slide it back in again."

    e "Also new in this release is the ability to specify transitions
       that occur when you enter and exit the game menu."

    e "Right click to see them, if you want."

    e "A few more obscure features involving things like overlays and
       activated widgets round out the 4.6 release."

label whatsnewend:

    e "Anyway, now that you've heard about some of the new features, is there anything
       else I can help you with?"

    return

    

    
