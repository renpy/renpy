testcase default:

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

    # Input

    call video
    call nvl_mode

    # Tools

#     call building




testcase player_experience:
    "Player Experience"
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
    "Creating a New Game"
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

testcase music:
    "Music and Sound Effects"
    click until label tutorials

testcase choices:
    "Choices and Python"
    click until "Yes, I do."
    click until "Yes."
    click until label tutorials

testcase positioning_images:
    click until label tutorials



testcase video:
    "Video Playback"
    click until label tutorials

testcase nvl_mode:
    "NVL Mode"
    click until "Yes."
    click until label tutorials

testcase building:
    "Building Distributions"
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
