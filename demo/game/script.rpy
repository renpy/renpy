# This file contains the script for the Ren'Py demo game. Execution starts at
# the start label.
#
# Declarations of characters and images used throughout the game can be found
# in demo_basics.rpy. Options can be set in options.rpy.

# The game starts here.
label start:

    scene bg washington
    show eileen vhappy
    with dissolve

    # Start the background music playing.
    $ renpy.music.play("mozart.ogg")

    e "Hi, and welcome to the Ren'Py demo game."

    show eileen happy
    
    e "My name is Eileen, and I'm here to demonstrate some of the features of the Ren'Py visual novel engine."

    # Show the editor button, which is defined in editor.rpy.
    $ show_editor_button = True

    e "See that button in the upper-right corner of the screen?"

    e "It shows where we are in the script. You can click it, and we'll try to open the file in a text editor."

    e "It's an easy way to see how you can use the features I'm showing off."

    e "We'll only show it for code that's intended to be easy to understand."

    call demos from _call_demos_1

    e "Thank you for viewing the Ren'Py demo script."

    e "For Ren'Py help and discussion on visual novel development, check out the Lemma Soft Forums, at http://lemmasoft.renai.us."

    e "We'd like to thank Piroshki for contributing character art... I've never looked better."

    e "Thanks to Jake for the magic circle."
    
    e "The background music was generating using a Musikalisches Würfelspiel attributed to Mozart... even though that's probably wrong."

    show eileen vhappy 
    
    e "We look forward to seeing what you can make with this! Good luck!"

    # Returning from the top level quits the game.
    return

    
    
