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
        ("demo_transitions", "Transition Gallery", "5.6.6"),
        ("demo_imageops", "Image Operations", "6.5.0"),
        ("demo_ui", "User Interaction", "6.5.0"),
        ("demo_text", "Fonts and Text Tags", "6.8.0"),
        ("demo_character", "Character Objects", "6.2.0"), 
        ("demo_layers", "Layers & Advanced Show", "5.6.5"),
        ("demo_nvlmode", "NVL Mode", "6.4.0"),
        ("demo_dynamic", "Dynamic Displayables", "5.6.3"),
        ("demo_minigame", "Minigames", "6.3.2"),
        ("demo_persistent", "Persistent Data", "6.7.0"),
        ("demo_transform", "Transform", "6.9.0"),
        ]
    
    def tutorials_show(adjustment):

        renpy.choice_for_skipping()

        with ui.side(['c', 'r'], xpos=250, ypos=40):

            ui.viewport(xmaximum=530, ymaximum=400, yadjustment=adjustment, mousewheel=True)
            with ui.vbox():
        
                for label, name, ver in tutorials:
                    ui.button(style='button',
                              clicked=ui.returns(label),
                              xminimum=530,
                              left_padding=20)
                    ui.hbox()
                    ui.text(name, style='button_text', size=22, minwidth=420)
                    ui.text(ver, style='button_text', size=22)
                    ui.close()

                ui.text(" ")

                ui.button(style='button',
                          clicked=ui.returns(False),
                          xminimum=530,
                          left_padding=20)

                ui.text("That's enough for now.", style='button_text', size=22, minwidth=450)

            ui.bar(adjustment=adjustment, style='vscrollbar')
        
        
        rfd = renpy.roll_forward_info()        
        result = ui.interact(roll_forward=rfd)
        renpy.checkpoint(result)

        return result
        


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
        
        $ result = tutorials_show(tutorials_adjustment)
            
        show eileen happy at center
        with move

        if result is False:
            jump end

        call expression result
        
            
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
