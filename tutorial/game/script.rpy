# This file contains the script for the Ren'Py demo game. Execution starts at
# the start label.

# Here we define the backgrounds that are used.
image bg washington = "washington.jpg"
image bg whitehouse = "whitehouse.jpg"

# And this is the character art we use.
image eileen happy = "eileen_happy.png"
image eileen vhappy = "eileen_vhappy.png"
image eileen concerned = "eileen_concerned.png"

# Now, we declare the characters.
define e = Character('Eileen', color="#c8ffc8")

init python:

    tutorials = [
        ("tutorial_playing", "User Experience", "6.10.0"),
        ("tutorial_dialogue", "Writing Dialogue", "6.10.0"),
        ("tutorial_images", "Adding Images", "6.10.0"),
        ("tutorial_transitions", "Transitions", "6.10.0"),
        ("tutorial_music", "Music and Sound Effects", "6.10.0"),
        ("tutorial_menus", "In-Game Menus and Python", "6.10.0"),
        ("tutorial_positions", "Screen Positions", "6.10.0"),
        ("tutorial_atl", "Animation and Transformation", "6.10.0"),
        ("tutorial_video", "Video Playback", "6.10.0"),
        ("demo_transitions", "Transition Gallery", "6.11.1"),
        ("demo_imageops", "Image Operations", "6.5.0"),
        ("demo_ui", "User Interaction", "6.5.0"),
        ("demo_text", "Fonts and Text Tags", "6.13.0"),
        ("demo_character", "Character Objects", "6.2.0"), 
        ("demo_layers", "Layers & Advanced Show", "5.6.5"),
        ("demo_nvlmode", "NVL Mode", "6.4.0"),
        ("demo_dynamic", "Dynamic Displayables", "5.6.3"),
        ("demo_minigame", "Minigames", "6.3.2"),
        ("demo_persistent", "Persistent Data", "6.7.0"),
        ("demo_transform", "Transform", "6.9.0"),
        ("tutorial_sprite", "Sprites", "6.12.0"),
        ]

screen tutorials:

    side "c r":
        area (250, 40, 548, 400)
        
        viewport:
            yadjustment adj
            mousewheel True
            
            vbox:
                for label, name, ver in tutorials:
                    button:
                        action Return(label)
                        left_padding 20
                        xfill True
                        
                        hbox:
                            text name style "button_text" min_width 420
                            text ver style "button_text"
                            
                null height 20

                textbutton "That's enough for now.":
                    xfill True
                    action Return(False) 
                
        bar adjustment adj style "vscrollbar" 
        

# The game starts here.
#begin start
label start:

    #end start
    scene bg washington
    show eileen vhappy
    with dissolve

    # Start the background music playing.
    play music "happy_alley.ogg"

    window show

    e "Hi! My name is Eileen, and I'd like to welcome you to the Ren'Py tutorial. You've come at a very interesting time."

    show eileen happy
    
    e "We're hard at work making Ren'Py 7, and that means we'll be turning the old Ren'Py demo game into the new tutorial."
    
    e "What we have now is a bit of a mix of the two. But please check it out, to see what Ren'Py is capable of."

    $ tutorials_adjustment = ui.adjustment()
    $ tutorials_first_time = True
    
    while True:
        show eileen happy at left
        with move

        if tutorials_first_time:
            $ e("What would you like to see?", interact=False) 
        else:
            $ e("Is there anything else you'd like to see?", interact=False) 

        $ tutorials_first_time = False

        call screen tutorials(adj=tutorials_adjustment)
        
        show eileen happy at center
        with move

        if _return is False:
            jump end

        call expression _return
        
            
label end:

    e "Thank you for viewing this tutorial."

    e "If you'd like to see a full Ren'Py game, go to the launcher and choose \"Select Project\", then \"the_question\"."
    
    e "You can download new versions of Ren'Py from {a=http://www.renpy.org/}http://www.renpy.org/{/a}. For help and discussion, check out the {a=http://lemmasoft.renai.us/forums/}Lemma Soft Forums{/a}."

    e "We'd like to thank Piroshki for contributing my sprites, Mugenjohncel for Lucy and the band, and Jake for the magic circle."

    e "The background music is \"Happy Alley\" by Kevin MacLeod. The concert music is by Alessio."
    
    show eileen vhappy 
    
    e "We look forward to seeing what you can make with Ren'Py. Good luck!"

    window hide

    # Returning from the top level quits the game.
    return
