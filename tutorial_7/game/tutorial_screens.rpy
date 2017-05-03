#begin simple_screen
screen simple_screen():
    frame:
        vbox:
            text "This is a screen."
            textbutton "Okay":
                action Return(True)
#end simple_screen



label screens:

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



    return
