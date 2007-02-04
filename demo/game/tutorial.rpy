# This file contains the tutorial, which demonstrates the code found
# in the quickstart manual. Notably, we're trying here to demonstrate
# the effects of the code in the quickstart manual. We don't actually
# use the spot-on identical code, since we need to integrate this with
# the rest of the demo (while keeping the download to a minimal size).

init:
    image bg meadow = "meadow.jpg"
    image bg uni = "uni.jpg"
    
    image sylvie smile = "sylvie_smile.png"
    image sylvie surprised = "sylvie_surprised.png"    

    $ s = Character('Sylvie', color="#c8ffc8")
    $ m = Character('Me', color="#c8c8ff")

    $ config.searchpath.append('../the_question/game')

label tutorial:

    e "Okay, I'll give you a quick tutorial on how to use Ren'Py."

    e "We put the source code for these examples into the quickstart manual, so you can follow along as I show you each example."

    menu:

        e "Would you like me to open the quickstart manual for you?"

        "Yes.":
            
            python hide:

                try:
                    import os
                    os.startfile(config.renpy_base + "/doc/tutorials/Quickstart.html")
                except:
                    try:
                        import webbrowser
                        url = 'file://' + config.renpy_base + "/doc/tutorials/Quickstart.html"
                        webbrowser.open(url, new=True)
                    except:
                        pass
                        
            e "Okay, here goes."
                
        "No.":

            e "No problem."

    e "If you want to read the quickstart manual yourself, you can find it in doc/tutorials/Quickstart.html."


    
    e "I'll skip over the details of how to operate the launcher, and show you some examples of Ren'Py in action."

    e "These are all taken from the game {i}The Question,{/i} which ships with Ren'Py."

    e "Example 1 shows the simplest use of Ren'Py, just showing text and dialogue."

    e "This is an example of the say statement in action."
    
    scene black
    with dissolve

    "I'll ask her..."

    "Me" "Um... will you..."
    "Me" "Will you be my artist for a visual novel?"

    "Silence."
    "She is shocked, and then..."

    "Sylvie" "Sure, but what is a \"visual novel?\""

    scene bg washington
    show eileen happy
    with dissolve

    e "If you take a look at the quickstart, you'll see how simple this script is. There's a start label to tell Ren'Py where to start, and lines of dialogue and narration."

    e "Unfortunately, with a script this simple, there isn't a way to customize the look of the characters' names."

    e "If you take a look at Example 2, you'll see how we can define characters, and then use them in dialogue."

    e "Let's run that example."

    scene black
    with dissolve

    "I'll ask her..."

    m "Um... will you..."
    m "Will you be my artist for a visual novel?"

    "Silence."
    "She is shocked, and then..."

    s "Sure, but what is a \"visual novel?\""
    
    scene bg washington
    show eileen happy
    with dissolve
    
    e "It's still not much to look at, but hopefully you noticed that the characters' names were colored in."

    e "If you looked at the script, you'll also notice that instead of having to write out \"Me\" and \"Sylvie\" each time, we used short names like m and s."

    e "That'll save typing in the long run."

    e "To make our example into a visual novel, we need to add some pictures."

    e "Example 3 shows how we define images, and then use the scene and show statements to display them to the player."

    
    scene bg meadow
    show sylvie smile
    with dissolve 
    
    "I'll ask her..."

    m "Um... will you..."
    m "Will you be my artist for a visual novel?"

    show sylvie surprised

    "Silence."
    "She is shocked, and then..."

    show sylvie smile

    s "Sure, but what is a \"visual novel?\""
    
    scene bg washington
    show eileen happy
    with dissolve
    
    e "To make Ren'Py use the pictures, you need to put them in the game directory, which you can get to from the launcher."

    e "Just showing the pictures might be a bit boring, so Ren'Py lets you give a transition between the old and new screens."

    e "Transitions are written using the with statement."

    e "Example 4 shows how they're used."

    scene bg uni
    show sylvie smile
    with dissolve
    
    s "Oh, hi, do we walk home together?"
    m "Yes..."
    "I said and my voice was already shaking."

    scene bg meadow
    with fade
    
    "We reached the meadows just outside our hometown."
    "Autumn was so beautiful here."
    "When we were children, we often played here."
    m "Hey... ummm..."

    show sylvie smile
    with dissolve
    
    "She turned to me and smiled."
    "I'll ask her..."
    m "Ummm... will you..."
    m "Will you be my artist for a visual novel?"

    scene bg washington
    show eileen happy
    with dissolve

    e "One thing users have come to expect is music."

    e "Music can be played with the play music statement, and stopped with the stop music statement."

    play music "illurock.ogg" fadeout 1

    e "Let's start playing the music from {i}The Question{/i}."

    e "If you're making a kinetic novel— a game with no choices— then what we have here is enough."
    
    e "Otherwise, you'll probably want to use in-game menus to let the user decide what to do."

    e "Example 5 shows how to make an in-game menu."

    e "It also shows how we use the jump and label statements to transfer control around the program."


    scene bg meadow
    show sylvie smile
    with dissolve
    
    s "Sure, but what's a \"visual novel?\""

menu:
    "It's a story with pictures.":
         jump tut_vn

    "It's a hentai game.":
         jump tut_hentai

label tut_vn:    
    m "It's a story with pictures and music."
    jump tut_marry

label tut_hentai:
    m "Why it's a game with lots of sex."
    jump tut_marry

label tut_marry:
    scene black
    with dissolve

    "--- years later ---"
    
    scene bg washington
    show eileen happy
    with dissolve

    e "And that's it, for now. To see what happens years later, you'll have to play {i}The Question.{/i}"

    e "You can use the launcher to run it, and it serves as an example of a complete, if short, Ren'Py game."

    play music "mozart.ogg" fadeout 1.0
    
    e "To learn more about Ren'Py, you can visit http://renpy.org/, and take a look at the web tutorial we have there."

    e "In this tutorial, I've tried to show you the most commonly-used parts of Ren'Py, things you'll see in almost every game."

    e "If you'd like to see more of what Ren'Py can do, I can show you a demonstration of its features."
        
    return
