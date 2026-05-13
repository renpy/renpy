init python:
    import time

testsuite global:
    before testsuite:
        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit


testsuite default:
    description "Default project testsuite"
    parameter language = ["french", None]

    setup:
        $ _test.timeout = 4.0
        $ _test.transition_timeout = 0.05

        if eval _preferences.language != language:
            run Language(language)

    before testcase:
        ## Go to the test screen, even if we've crashed in a prior test
        if not screen "tutorials":
            if not screen "main_menu":
                run MainMenu(confirm=False)

            if screen "main_menu":
                run Start()
                advance until screen "tutorials"

    teardown:
        click "That's enough for now." raw
        advance until screen "main_menu"
        # click "Quit" raw


    testsuite blank:
        testcase do_nothing:
            pass

    testsuite blank2:
        testcase do_nothing2:
            pass


    ## Run the testcases
    testcase player_experience:
        $ preferences.text_cps = 0

        scroll "Bar" until "Player Experience" raw
        click "Player Experience" raw
        advance until screen "choice"
        click "Yes." raw

        # Dialogue after menu.
        advance
        advance
        advance

        # Rollback to the menu.
        click button 4
        click button 4
        click button 4
        click button 4

        # Roll forward.
        click button 5
        click button 5

        # Back again to the menu.
        click button 4
        click button 4

        # Roll forward.
        keysym "K_PAGEDOWN"
        keysym "K_PAGEDOWN"

        # Back again.
        keysym "K_PAGEUP"
        keysym "K_PAGEUP"

        click "No." raw
        advance until screen "tutorials"

    testcase new_game:
        scroll "Bar" until "Creating a New Game" raw
        click "Creating a New Game" raw
        advance until screen "tutorials"

    testcase dialogue:
        scroll "Bar" until "Writing Dialogue" raw
        click "Writing Dialogue" raw
        advance until screen "tutorials"

    testcase images:
        scroll "Bar" until "Adding Images" raw
        click "Adding Images" raw
        advance until screen "tutorials"

    testcase transitions:
        scroll "Bar" until "Transitions" raw
        click "Transitions" raw
        advance until screen "tutorials"

    testcase music:
        scroll "Bar" until "Music and Sound Effects" raw
        click "Music and Sound Effects" raw
        advance until screen "tutorials"

    testcase choices:
        scroll "Bar" until "Choices and Python" raw
        click "Choices and Python" raw
        advance until screen "choice"
        click "Yes, I do." raw
        advance until screen "choice"
        click "Yes." raw
        advance until screen "tutorials"

    testcase input:
        scroll "Bar" until "Input and Interpolation" raw
        click "Input and Interpolation" raw
        advance until screen "input"
        type "Tom"
        keysym "K_BACKSPACE"
        type "m"
        keysym "K_LEFT"
        keysym "K_RIGHT"
        keysym "K_RETURN"
        advance until screen "tutorials"

    testcase positioning_images:
        scroll "Bar" until "Positioning Images" raw
        click "Positioning Images" raw
        advance until screen "tutorials"

    testcase video:
        scroll "Bar" until "Video Playback" raw
        click "Video Playback" raw
        advance until screen "tutorials"


    testcase nvl_mode:
        scroll "Bar" until "NVL Mode" raw
        click "NVL Mode" raw
        advance until eval ("nvl_menu" in renpy.game.context().modes) # screen "nvl_choice"
        click "Yes." raw
        advance until screen "tutorials"

    testcase tools:
        scroll "Bar" until "Tools and the Interactive Director" raw
        click "Tools and the Interactive Director" raw
        advance until screen "tutorials"

        # Not actually testing the various tools yet.

    testcase building:
        scroll "Bar" until "Building Distributions" raw
        click "Building Distributions" raw
        advance until screen "tutorials"

    testcase text_tags:
        scroll "Bar" until "Text Tags, Escapes, and Interpolation" raw
        click "Text Tags, Escapes, and Interpolation" raw
        advance until screen "tutorials"

    testcase character_objects:
        scroll "Bar" until "Character Objects" raw
        click "Character Objects" raw
        advance until screen "tutorials"

    testcase simple_displayables:
        scroll "Bar" until "Simple Displayables" raw
        click "Simple Displayables" raw
        advance until screen "tutorials"

    testcase transition_gallery:
        $ _test.transition_timeout = 60.0

        scroll "Bar" until "Transition Gallery" raw
        click "Transition Gallery" raw
        advance until screen "choice"
        click "Simple" raw
        advance until screen "choice"
        click "ImageDissolve" raw
        advance until screen "choice"
        click "MoveTransition" raw
        advance until screen "choice"
        click "CropMove" raw
        advance until screen "choice"
        click "PushMove" raw
        advance until screen "choice"
        click "AlphaDissolve" raw
        advance until screen "choice"
        click "something else" raw
        advance until screen "tutorials"

    testcase position_properties:
        scroll "Bar" until "Position Properties" raw
        click "Position Properties" raw
        advance until screen "choice"
        click "xpos .75 ypos .25" raw
        advance until screen "tutorials"

    testcase transforms:
        scroll "Bar" until "Transforms and Animation" raw
        click "Transforms and Animation" raw
        advance until screen "tutorials"

        scroll "Bar" until "Transform Properties" raw
        click "Transform Properties" raw
        advance until screen "tutorials"

    testcase gui_customization:
        scroll "Bar" until "GUI Customization" raw
        click "GUI Customization" raw
        advance until screen "tutorials"

    testcase styles:
        scroll "Bar" until "Styles and Style Properties" raw
        click "Styles and Style Properties" raw
        advance until screen "choice"
        click "Style basics." raw
        advance until screen "choice"
        click "General style properties." raw
        advance until screen "choice"
        click "Text style properties." raw
        advance until screen "choice"
        click "Window and Button style properties." raw
        advance until screen "choice"
        click "Bar style properties." raw
        advance until screen "choice"
        click "Box, Grid, and Fixed style properties." raw
        advance until screen "choice"
        click "The Displayable Inspector." raw
        advance until screen "choice"
        click "That's all I want to know." raw
        advance until screen "tutorials"

    testcase screens:
        scroll "Bar" until "Screen Basics" raw
        click "Screen Basics" raw
        advance until screen "choice"

        click "What screens can do." raw
        advance until screen "choice"
        click "Yes." raw
        advance until screen "choice"

        click "How to show screens." raw
        advance until "Since we can't display dialogue at the same time" raw
        advance until screen "simple_screen"
        click "Okay" raw
        advance until screen "choice"

        click "Passing parameters to screens." raw
        advance until screen "parameter_screen"
        ## We need to insist on closing the screen. May have to do with transitions
        click "Okay" raw until not screen "parameter_screen"
        advance until "The call screen statement can also take arguments" raw
        advance until screen "parameter_screen"
        click "Okay" raw
        advance until screen "choice"

        click "Screen properties." raw
        advance until screen "modal_example"
        ## We need to insist on closing the screen. May have to do with transitions
        click "Close This Screen" raw until not screen "modal_example"
        advance until screen "choice"

        click "Special screen statements." raw
        advance until screen "choice"

        click "Using other screens." raw
        advance until screen "choice"

        click "That's it." raw


    testcase screen_displayables:
        scroll "Bar" until "Screen Displayables" raw
        click "Screen Displayables" raw
        advance until screen "choice"
        click "Common properties" raw
        advance until screen "choice"
        click "Adding images" raw
        advance until screen "choice"
        click "Text" raw
        advance until screen "choice"
        click "Buttons" raw
        advance until screen "choice"
        click "Bars" raw
        advance until screen "choice"
        click "Viewports" raw
        advance until screen "choice"
        click "Imagemaps" raw
        advance until screen "imagemap_example"
        click "Science" raw
        advance until screen "choice"
        click "That's all" raw

        advance until screen "tutorials"

    testcase translations:
        scroll "Bar" until "Translations" raw
        click "Translations" raw
        advance until screen "tutorials"


    testcase out_of_game:
        click "Back" raw
        click "Back" raw

        click "Skip" raw

        click "Back" raw

        $ _preferences.self_voicing = False
        $ _preferences.afm_time = 1

        click "Auto" raw
        scroll "Bar" until "Player Experience" raw
        click "Player Experience" raw
        click "Auto" raw
        click "History" raw

        pause .5

        click "Save" raw
        pause .5

        click id "save_slot_1"
        pause 0.2
        if screen "confirm":
            click id "confirm_yes_button" until not screen "confirm"

        click "Load" raw
        pause .5

        click id "save_slot_1"
        click id "confirm_yes_button" until not screen "confirm"

        click "Prefs" raw
        pause .5

        click "About" raw
        pause .5

        click "Help" raw
        pause .5

        click "Main Menu" raw
        click id "confirm_yes_button" until not screen "confirm"

        click "Load" raw
        pause .5

        click id "save_slot_1"

        advance until screen "choice"
        click "Yes." raw
        advance until screen "tutorials"
