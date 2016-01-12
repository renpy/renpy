testcase default:
    "Start Game"
    click until label tutorials
    call user_experience
    call dialogue
    call images
    call transitions
    call music_and_sound
    call menus
    call positions
    call atl
    call video
    call transition_gallery
    call image_operations
    call fonts
    run Quit(confirm=False)

testcase quick:
    "Start Game"
    click until label tutorials

    # Won't work until we can scroll the bar.

    call character_objects
    call layers
    call nvl_mode
    call dynamic

testcase user_experience:
    "User Experience"
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

testcase dialogue:
    "Writing Dialogue"
    click until label tutorials

testcase images:
    "Adding Images"
    click until label tutorials

testcase transitions:
    "Transitions"
    click until label tutorials

testcase music_and_sound:
    "Music and Sound Effects"
    click until label tutorials

testcase menus:
    "In-Game Menus and Python"
    click until "Yes, I do."
    click until label tutorials

testcase positions:
    "Screen Positions"
    click until "xpos .75 ypos .25"
    click until label tutorials

testcase atl:
    "Animation and Transformation"
    click until label tutorials

testcase video:
    "Video Playback"
    click until label tutorials

testcase transition_gallery:
    "Transition Gallery"
    click until "Simple"
    click until "ImageDissolve"
    click until "MoveTransition"
    click until "CropMove"
    click until "PushMove"
    click until "AlphaDissolve"
    click until "something else"
    click until label tutorials

testcase image_operations:
    "Image Operations"
    click until label tutorials

# User Interaction

testcase fonts:
    "Fonts and Text Tags"
    click until label tutorials

testcase character_objects:
    "Character Objects"
    click until label tutorials

testcase layers:
    "Layers & Advanced Show"
    click until label tutorials

testcase nvl_mode:
    "NVL Mode"
    click until "Yes."
    click until label tutorials

testcase dynamic:
    "Dynamic Displayables"
    click until label tutorials
