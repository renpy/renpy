# This file contains some of the basics of Ren'Py. This is stuff you'll use in
# just about every game.

# First, we have an init block that contains many of the definitions we
# use in the game
init:

    # Here we define the backgrounds that are used by the demo.
    image bg washington = "washington.jpg"
    image bg whitehouse = "whitehouse.jpg"

    # And this is the character art we use in the demo.
    image eileen happy = "eileen_happy.png"
    image eileen vhappy = "eileen_vhappy.png"
    image eileen concerned = "eileen_concerned.png"
    
    # Now, we declare the characters.
    $ e = Character('Eileen', color="#c8ffc8")


# In a real game, we would have:
#
# label start:
#
# here. But since we are inside the demo game, we have to use a different
# label.

label demo_basics:

    e "This is our demonstration of the basics of using Ren'Py. You may want to click the button at the upper-right of the screen, to follow along."

    "Somehow, I realize that Ren'Py supports narration."

    e "Ren'Py supports dialogue, as long as you declare a character first. If it didn't I wouldn't be able to talk to you."

    e "Ren'Py also supports menus, which let you make decisions based on user input."


    menu:

        e "Do you think you'd ever use menus in a game?"

        "Yes.":
            
            jump about_menus_yes

        "No.":

            jump about_menus_no

        "I'm not ready to make that decision yet.":

            jump about_menus_unsure

label about_menus_yes:
    
    $ about_menus_choice = "yes"
    
    e "Menus are the most important way of providing interactivity to a game."

    jump about_menus_done
    
label about_menus_no:

    $ about_menus_choice = "no"
    
    e "That's okay, Ren'Py has been used to make a number of linear games, which we call kinetic novels."

    jump about_menus_done

label about_menus_unsure:

    $ about_menus_choice = "unsure"
    
    e "Well, it doesn't really matter. Whatever you decide, Ren'Py is ready for you."

    jump about_menus_done


label about_menus_done:

    e "Ren'Py wouldn't be much of a visual novel engine if it didn't support images."

    scene bg whitehouse
    with dissolve
    
    e "The scene statement clears the screen, and optionally lets you place a single new image on the screen."

    show eileen happy
    with dissolve
    
    e "The show statement shows images to the user."

    show eileen vhappy
    with dissolve
    
    e "Showing an image with the same tag, the same first part of the name, as an already-show image replaces that image."

    show eileen happy at right
    with dissolve
    
    e "Images can be shown at different locations on the screen, and you can show as many images on the screen as you want."

    hide eileen happy
    with dissolve
 
    e "The hide statement hides images, although with scene statement clearing the screen and the show statement replacing images, it's rarely necessary to do so."

    scene bg washington
    show eileen happy
    with dissolve

    e "Finally, the with statement is what we use to perform a transition from one screen to the next."

    e "That's all you need to make a simple game, like a kinetic novel."

    e "But I would be remiss if I didn't mention that Ren'Py can store data, and make decisions based on it."

    if about_menus_choice == "yes":

        e "For example, I remember you wanted to use menus in your game."

    elif about_menus_choice == "no":

        e "For example, I remember you didn't want to use menus."

    else:

        e "For example, I remember you weren't sure about menus."

    e "Ren'Py embeds the Python programming language, which lets you do some very sophisticated things."

    e "But you don't need learn Python if you don't want to."

    return
