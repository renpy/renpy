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

    call building


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

testcase building:
    scroll "Bar" until "Building Distributions"
    click until label tutorials


testcase transition_gallery:
    scroll "Bar" until "Transition Gallery"
    click until "Simple"
    click until "ImageDissolve"
    click until "MoveTransition"
    click until "CropMove"
    click until "PushMove"
    click until "AlphaDissolve"
    click until "something else"
    click until label tutorials
