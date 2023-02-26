
testcase player_experience:
    scroll "Bar" until "Player Experience"
    click until "Yes."

    # Dialogue after menu.
    click
    click
    click

    # Rollback to the menu.
    click button 4
    click button 4
    click button 4
    click button 4

    # Roll forward.
    click button 5
    click button 5

    # Back again.
    click button 4
    click button 4

    # Roll forward.
    type PAGEDOWN
    type PAGEDOWN

    # Back again.
    type PAGEUP
    type PAGEUP

    "No."

    click until label tutorials

testcase new_game:
    scroll "Bar" until "Creating a New Game"
    click until label tutorials

testcase dialogue:
    scroll "Bar" until "Writing Dialogue"
    click until label tutorials

testcase images:
    scroll "Bar" until "Adding Images"
    click until label tutorials

testcase transitions:
    scroll "Bar" until "Transitions"
    click until label tutorials

testcase music:
    scroll "Bar" until "Music and Sound Effects"
    click until label tutorials

testcase choices:
    scroll "Bar" until "Choices and Python"
    click until "Yes, I do."
    click until "Yes."
    click until label tutorials


testcase input:
    scroll "Bar" until "Input and Interpolation"
    click until "Some games might prompt the player for input."
    type "Tom"
    type BACKSPACE
    type "m"
    type LEFT
    type RIGHT
    type "\n"
    click until label tutorials

testcase positioning_images:
    scroll "Bar" until "Positioning Images"
    click until label tutorials

testcase video:
    scroll "Bar" until "Video Playback"
    click until label tutorials

testcase nvl_mode:
    scroll "Bar" until "NVL Mode"
    click until "Yes."
    click until label tutorials

testcase tools:
    scroll "Bar" until "Tools and the Interactive Director"

    # Not actually testing the various tools yet.

    click until label tutorials

testcase building:
    scroll "Bar" until "Building Distributions"
    click until label tutorials


testcase text_tags:
    scroll "Bar" until "Text Tags, Escapes, and Interpolation"
    click until label tutorials

testcase character_objects:
    scroll "Bar" until "Character Objects"
    click until label tutorials

testcase simple_displayables:
    scroll "Bar" until "Simple Displayables"
    click until label tutorials



testcase transition_gallery:
    $ _test.transition_timeout = 60.0

    scroll "Bar" until "Transition Gallery"
    click until "Simple"
    click until "ImageDissolve"
    click until "MoveTransition"
    click until "CropMove"
    click until "PushMove"
    click until "AlphaDissolve"
    click until "something else"
    click until label tutorials

    $ _test.transition_timeout = 0.05

testcase position_properties:
    scroll "Bar" until "Position Properties"
    click until "xpos .75 ypos .25"
    click until label tutorials

testcase transforms:

    scroll "Bar" until "Transforms and Animation"
    click until label tutorials

    scroll "Bar" until "Transform Properties"
    click until label tutorials

testcase gui_customization:

    scroll "Bar" until "GUI Customization"
    click until label tutorials


testcase styles:

    scroll "Bar" until "Styles and Style Properties"
    click until "Style basics."
    click until "General style properties."
    click until "Text style properties."
    click until "Window and Button style properties."
    click until "Bar style properties."
    click until "Box, Grid, and Fixed style properties."
    click until "The Displayable Inspector."
    click until "That's all I want to know."
    click until label tutorials


testcase screens:

    scroll "Bar" until "Screen Basics"
    click until "What screens can do."
    click until "Yes."
    click until "How to show screens."
    click until "you'll have to click"
    "Okay"
    click until "Passing parameters to screens."
    click until "the call screen statement"
    "Okay"
    click until "Screen properties."
    click until "Close This Screen"
    pause .5
    "Close This Screen"
    click until "Special screen statements."
    click until "Using other screens."
    click until "That's it."

    scroll "Bar" until "Screen Displayables"
    click until "Common properties"
    click until "Adding images"
    click until "Text"
    click until "Buttons"
    click until "Bars"
    click until "Viewports"
    click until "Imagemaps"
    click until "Science"
    click until "That's all"

    click until label tutorials


testcase translations:

    scroll "Bar" until "Translations"
    click until label tutorials


testcase out_of_game:
    "Back"
    "Back"

    "Skip"

    "Back"

    $ _preferences.self_voicing = False
    $ _preferences.afm_time = 1


    "Auto"
    scroll "Bar" until "Player Experience"
    "Auto"
    "History"

    pause .5

    "Save"
    "Save Slot 1"
    "Yes"

    "Load"
    pause .5

    "Load Slot 1"
    "Yes"

    "Prefs"
    pause .5

    "About"
    pause .5

    "Help"
    pause .5

    "Main Menu"
    "Yes"

    "Load"
    pause .5

    "Load Slot 1"

    click until "Yes."
    click until label tutorials



testcase template:

    scroll "Bar" until "-"
    click until label tutorials


testcase default:

    $ _test.transition_timeout = 0.05

    "Start"
    click until label tutorials

    call player_experience
    call new_game
    call dialogue
    call images
    call positioning_images
    call transitions
    call music
    call choices
    call input
    call video
    call nvl_mode
    call tools
    call building

    call text_tags
    call character_objects
    call simple_displayables
    call transition_gallery
    call position_properties
    call transforms
    call gui_customization
    call styles
    call screens

    # Skip Minigames and CDDs.

    call translations
    call out_of_game

    "That's enough for now."
    click until "Quit"
    pause .5



