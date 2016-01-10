testcase default:
    "Start Game"
    click until label tutorials
    call user_experience
    call dialogue
    call images
    call transitions


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
