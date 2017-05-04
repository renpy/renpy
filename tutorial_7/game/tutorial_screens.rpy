#begin simple_screen
screen simple_screen():
    frame:
        vbox:
            text "This is a screen."
            textbutton "Okay":
                action Return(True)
#end simple_screen



label screens:

    jump imagemap_done

    e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."

    show screen example('simple_screen')

    e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen."

    e "Inside the screen statement, every statement either introduces a displayable like frame, vbox, text, and textbutton; or a property like action."

    show screen simple_screen

    e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."

    e "The text statement is used to display the text provided."

    e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."

    e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."

    e "And that is inside a frame that provides the background and borders."

    hide screen simple_screen
    hide screen example


    e "There are a trio of statements that are used to display screens."

    show screen example('show_screen')

#begin show_screen
    show screen simple_screen

    e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."

    e "The screen will stay shown until it is hidden."

    hide screen simple_screen

    e "Hiding a screen is done with the hide screen statement."
#end show_screen

    show screen example('call_screen')

    e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."

    e "Since we can't display dialogue at the same time, you'll have to click 'Return' to continue."

    hide screen example

#begin call_screen
    call screen simple_screen
#end call_screen

    e "When a call screen statement ends, the screen is automatically hidden."

    e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."

label imagemap_tutorial:

    show screen example('imagemap')

    e "Another type of screen is an imagemap. An imagemap uses images that display hotspots that act as buttons."

    e "This imagemap uses two images - one when a button is idle, and one when a button is hovered. The idle image also doubles as a background."

    e "When a player clicks on a hotspot, this imagemap runs a Jump action to take them to a label. Each hotspots also has alt text, for vision-impared players."

    hide screen example

    e "Let's take a look at an imagemap screen in action."

    jump imagemap_example

#begin imagemap
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
#end imagemap

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
