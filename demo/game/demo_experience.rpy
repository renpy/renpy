# This file demonstrates the Ren'Py User Experience... the features you get
# for free by choosing to use Ren'Py as a visual novel engine.

init:
    image popup prefs = "prefs.png"
    image popup save = "save.png"

label demo_experience:

    e "One of the goals of Ren'Py is to provide visual novel players with a good user experience."

    e "To ensure this, there are a number of features that are included as part of every Ren'Py game. Here, we'll show off some of these features."

    e "Skipping can be turned on from the game menu, or when the user presses the Tab key. It is also enabled while the user holds down either Ctrl key."

    e "By default it only skips read text, so if it's your first time reading this, it won't do anything. That can be changed from the game menu."

    e "On the second and later times reading a screen of text, it will skip right through it."

    e "Rollback is a feature that lets you go back in time to previous screens, letting you re-read text."

    menu:

        e "Would you like to hear more about rollback?"

        "Yes.":

            jump demo_rollback

        "No.":

            jump demo_rollback_done


label demo_rollback:

    e "You can invoke a rollback by scrolling the mouse wheel up, or by pushing the page up key. That'll bring you back to the previous screen."

    e "While at a previous screen, you can roll forward by scrolling the mouse wheel down, or pushing the page down key."

    e "Rolling forward through a menu will make the same choice you did last time. You can also make a different choice, if you change your mind."

    e "You can try it by rolling back through the last menu, and saying 'No'."

    e "Press page up, or scroll up the mouse wheel."

    show eileen concerned

    e "Well, are you going to try it?"

    e "Your loss."

    e "Moving on."

    show eileen happy
        
label demo_rollback_done:
    
    e "Now, let me show off the game menu. You can access the game menu by right clicking, or by hitting escape. You can get back by doing the same thing, or by clicking \"Return\"."

    e "The game menu lets you do many things."

    show popup save at Position(ypos=.1, yanchor=0, xpos=0, xanchor=1.0)
    with None
    
    show popup save at Position(xpos=.1, ypos=.1, xanchor=0, yanchor=0)
    show eileen happy at right
    with move
    
    e "The save screen lets you save a game, while the load screen lets you load the game back in."

    e "Unlike many game engines, Ren'Py supports an unlimited number of save slots."

    show popup prefs at Position(xpos=.1, ypos=.1, xanchor=0, yanchor=0)
    with dissolve

    e "The preferences screen lets the end-user change some aspects of the behavior of Ren'Py."

    e "The user can choose if the game runs in a window, or fullscreen."

    e "By setting transitions to None, a user can eliminate transitions entirely."

    e "A user can choose if the skipping feature skips all messages, or only seen messages, and if it stops when an in-game menu is selected."

    e "When the text speed setting isn't the maximum, text will be drawn onto the screen one character at a time."

    e "The auto-forward time setting controls how long we will wait before automatically advancing through text."

    e "The auto-forward time is adjusted by the length of the text being shown."

    e "Finally, we allow the user to choose the volume for music, voice, and sound effects."

    e "From the game menu, the user can return to the game, begin skipping, return to the main menu, or quit entirely."

    show popup save at Position(ypos=.1, yanchor=0, xpos=0, xanchor=1.0)
    show eileen happy at center
    with move

    hide popup save

    e "And that's part of how Ren'Py gives end-users the experience they expect."
    
    return
