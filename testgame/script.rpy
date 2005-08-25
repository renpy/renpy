init:
    $ config.window_title = "Test Game"
    $ config.profile = False

    $ config.debug_sound = True

    # Set up the size of the screen.
    $ config.screen_width = 800
    $ config.screen_height = 600
    $ config.fade_music = 0.5

    # Positions of things on the screen.
    $ left = Position(xpos=0.0, xanchor='left')
    $ right = Position(xpos=1.0, xanchor='right')
    $ center = Position()
    $ top = Position(ypos=0.0, yanchor='top')

    # Transitions
    $ fade = Fade(0.5, 0.5, 0.5)
    $ dissolve = Dissolve(.5)

    # Styles.
    $ style.window.background = Frame("frame.png", 120, 25)

    $ style.menu_choice_button.hover_sound = "chev1.wav"
    $ style.menu_choice_button.activate_sound = "chev2.wav"

    $ style.imagemap_button.hover_sound = "chev3.wav"
    $ style.imagemap_button.activate_sound = "chev4.wav"

    $ style.button.hover_sound = "chev6.wav"
    $ style.button.activate_sound = "chev7.wav"

    # $ style.mm_root_window.background = Solid((128, 128, 128, 255))
    # $ style.gm_root_window.background = Solid((128, 128, 128, 255))

    # Backgrounds.
    image whitehouse = Image("whitehouse.jpg")
    image black = Solid((0, 0, 0, 255))

    # Character pictures.
    image eileen happy = Image("9a_happy.png")
    image eileen happy beret = Image(("9a_happy.png", "beret.png"))
    image eileen vhappy = Image("9a_vhappy.png")
    image eileen concerned = Image("9a_concerned.png")

    image eileen anim = Animation("9a_happy.png", 0.25,
                                  "9a_vhappy.png", 0.25,
                                  "9a_concerned.png", 0.5)

    image movie = Movie()

    # Character objects.
    $ e = Character('Eileen', color=(200, 255, 200, 255))
    $ w = Character('Walter')
    $ pov = DynamicCharacter('pov_name', color=(255, 0, 0, 255))
    $ pov_name = '????'

    # $ style._write_docs('/tmp/style.xml')

# init:

#     python hide:        
#         def menu_button_overlay():
#             ui.imagebutton("menu_button.png",
#                            "menu_button_hover.png",
#                            clicked=renpy.curried_call_in_new_context("_game_menu"))

#         config.overlay_functions.append(menu_button_overlay)
        
    

init:
    python:
        def p(what):
            renpy.display_say(player_name, what, color=(255, 255, 0, 255))

        p.say = p

    $ player_name = "Foo Bar"

label main_menu:

    # Stuff that happens before the real main menu.

    scene black

    show eileen anim

    $ renpy.pause()
        

    show text "American Bishoujo\nPresents" \
         at Move((0.5, 0.0), (0.5, 0.5), 4.0,
                 xanchor='center', yanchor='bottom')

    if renpy.pause(8):
        jump _library_main_menu

    show text "A PyTom Game" at Position(xpos=0.5, ypos=0.5,
                                         xanchor="center", yanchor="bottom")

    if renpy.with(fade) or renpy.pause(4):
        jump _library_main_menu

    $ renpy.transition(fade)
    jump _library_main_menu
    

# The actual game starts here.
label start:

    jump foobar

    scene whitehouse
    show eileen happy beret

    $ renpy.context().foo = 1
    $ renpy.watch('str(renpy.context().foo)')

    e "Okay, let's play stargate."

    voice "chev1.wav"
    w "Chevron one encoded!"

    $ renpy.context().foo = 2

    voice "chev2.wav"
    w "Chevron two encoded!"

    voice "chev3.wav"
    w "Chevron three encoded!"

    voice "chev4.wav"
    w "Chevron four encoded!"

    voice "chev5.wav"
    w "Chevron five encoded!"

    voice "chev6.wav"
    w "Chevron six encoded!"

    voice "chev7.wav"
    w "Chevron seven..."

    voice_sustain ""
    w "... locked!"


    python:
        ui.sizer(200, None)
        ui.text("Now is      the     time for all good men to come to the aid of their party. Whatsoever, things are true.", first_indent=50)

        ui.saybehavior()
        ui.interact()


        
    "Hey, let's make sure that the
     multi-line text\ \ \ still
     works right."

    $ renpy.movie_cutscene("On_Your_Mark.mpg", 450.0)
    $ the_value = 10

    label foo:
        
    python hide:

        def bar_clicked(value):
            print "Value is:", value
            return value

        ui.vbox()
        ui.bar(300, 30, 10, store.the_value, clicked=bar_clicked)
        ui.textbutton("Continue", clicked = lambda : False)
        ui.close()

        rv = ui.interact()

        if rv is not False:
            store.the_value = rv
            renpy.jump('foo')
            

        

    $ renpy.movie_start_displayable('On_Your_Mark.mpg', (400, 300))
    show movie

    p "I'm now showing a movie."

    p "It's using alpha blending and all that."

    p "Bully!"

    $ renpy.movie_stop()
    hide movie
    
                                    
    

    p "This is a test."

    $ overtext = 'This is overtext.'

    python hide:
        renpy.watch("overtext", xpos=0.0, ypos=0.0, xanchor="left", yanchor="top")



    menu:
        "Yes?":
            pass
        "No.":
            pass

    $ result = renpy.imagemap("ground.png", "selected.png", [
        (100, 100, 300, 400, "eileen"),
        (500, 100, 700, 400, "lucy")
        ])

    if result == "eileen":
        e "You picked me!"

    elif result == "lucy":
        e "It looks like you picked Lucy."   

    $ renpy.music_start('2f-final.mp3')

#     centered "American Bishoujo presents..."

#     $ renpy.pause(5, 5)

#     centered "A PyTom Game...."

#     $ renpy.pause(500, 10)

label foobar:
        
    scene whitehouse with dissolve
    show eileen happy with dissolve

    $ save_name = 'Early.'

    e "Welcome to tests of loading and saving."

    $ pov_name = renpy.input('What is your name?', 'Joe User', length=20)

    e "You claim your name is %(pov_name)s."

    pov "Yes, I do."

    with fade

    $ renpy.play('chev5.wav')

    e "Save when I tell you to."

label recover:

    $ save_name = 'Post-Recover.'

    hide eileen with dissolve

    e "If the script is changed, then this is the line that will be
       rolled-back to."

    e "Wait for it..."

    $ overtext = 'Wind - A Breath of Heart'
    $ renpy.music_start("wind.ogg")

    $ save_name = 'Proper-Line.'

    e "This is the line you should save at. It also will be the line
       that is displayed after a load, when the script is not changed."

    $ save_name = 'Late.'

    e "This is past the save point."

    $ overtext = 'Final Fantasy 7 - World'
    $ renpy.music_start("FF7world.mid")

    e "This is way past the save point."


e "This is past 10k lines. Let's see how big the log is. Save here."

return
