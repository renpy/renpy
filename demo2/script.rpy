# This script, but not the artwork associated with it, is in the
# public domain. Feel free to use it as the basis for your own
# game.

init:
    # Set up the size of the screen.
    $ config.screen_width = 800
    $ config.screen_height = 600
    $ config.window_title = "The Ren'Py Demo Game"

    # Set up the library.
    $ library.file_page_length = 3

    # Styles.
    $ style.mm_root_window.background = Image("mainmenu.jpg")
    $ style.gm_root_window.background = Image("gamemenu.jpg")
    $ style.window.background = Frame("frame.png", 125, 25)

    # Positions of things on the screen.
    $ left = Position(xpos=0.0, xanchor='left')
    $ right = Position(xpos=1.0, xanchor='right')
    $ center = Position()

    # Transitions between scenes.
    $ fade = Fade(.5, 0, .5) # Fade to black and back.
    $ dissolve = Dissolve(0.5)  # Dissolve.

    # Backgrounds.
    image carillon = Image("carillon.jpg")
    image whitehouse = Image("whitehouse.jpg")
    image washington = Image("washington.jpg")
    image black = Solid((0, 0, 0, 255))

    # Character pictures.
    image eileen happy = Image("9a_happy.png")
    image eileen vhappy = Image("9a_vhappy.png")
    image eileen concerned = Image("9a_concerned.png")

    # Character objects.
    $ e = Character('Eileen', color=(200, 255, 200, 255))


# The actual game starts here.
label start:

    $ save_name = "Introduction"

    # Did we win the date?
    $ date = False

    # scene black
    # centered "American Bishoujo\npresents..." with fade
    # centered "The Ren'Py Demo Game" with fade
    
    $ renpy.music_start('sun-flower-slow-drag.mid')

    scene washington with fade
    show eileen vhappy with dissolve

    "Girl" "Hi, and welcome to the Ren'Py 4 demo program."

    show eileen happy

    "Girl" "My name is Eileen, and while I plan to one day star in a
            real game, for now I'm here to tell you about Ren'Py."

    e "Ren'Py is a language and engine for writing and playing visual
       novel games."

    e "Our goal is to allow people to be able to write the script for
       a game, and with very little effort, turn that script into
       a working game."

    e "I can tell you about the features of Ren'Py games, or how to write
       your own game. What do you want to know about?"

    $ seen_set = [ ]

    label choices:

    $ save_name = "Question Menu"

    menu:
        set seen_set

        "What are some features of Ren'Py games?":
            call features from _call_features_1
            jump choices

        "How do I write my own games with it?":
            call writing from _call_writing_1
            jump choices

        "Where can I find out more?" if seen_set:
            call find_out_more from _call_find_out_more_1
            jump choices

        "Why are we in Washington, DC?":
            call washington from _call_washington_1
            jump choices

        "I think I've heard enough." if seen_set:
            jump ending

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
       control quickly skips dialogue you've seen at least once, ever."

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

label writing:

    $ save_name = "Writing Games"

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

    "I somehow remember that strings by themselves are displayed as
     thoughts or narration."
    

    e "The menu statement makes it easy to create menus."

    e "A number of statements let you control what is shown on the
       screen."

    scene whitehouse with fade

    e "The scene statement clears the scene list, which is the list of
       things that are shown on the screen."

    show eileen happy with dissolve

    e "The show statement shows another image on the screen."

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

    with fade

    e "... or dissolve ..."

    with None
    scene washington
    show eileen happy
    with dissolve

    e "... are easily invoked."

    e "As of version 4.2, Ren'Py supports image maps, which are like
       another form of menu. Let's try one."

    $ result = renpy.imagemap("ground.png", "selected.png", [
        (100, 100, 300, 400, "eileen"),
        (500, 100, 700, 400, "lucy")
        ])


    if result == "eileen":
        show eileen vhappy
        e "You picked me!"

    elif result == "lucy":
        show eileen concerned
        e "It looks like you picked Lucy."

        if date:
            e "You can forget about Saturday."
            $ date = False

    show eileen happy
    
    e "Ren'Py also includes a number of control statements, and even
       lets you include python code."

    e "Rather than go into this here, you can read all about it in the
       tutorial."

    e "If you want to make changes, you can edit the script for this
       game by editing game/script.rpy"

    e "When you've made a change, just re-run the game to see your
       change in action."

    e "Would you like to know about something else?"

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
       
    $ renpy.full_restart()
