testsuite global:
    teardown:
        exit

testcase default:
    $ _test.transition_timeout = 0.05
    click "Start"
    pause .6

    # Test rollback
    click "You've created a new"
    click "Back"
    advance

    # Test history.
    click "History"

    # Test Help.
    click "Help"
    click "Keyboard"

    # Test About
    click "About"

    # Test Preferences
    click "Preferences"

    # click "Left"
    # click "Right"
    # click "Disable"

    click "Unseen Text"
    click "Unseen Text"

    click "After Choices"
    click "After Choices"

    click "Transitions"
    click "Transitions"

    click "Mute All"
    click "Mute All"

    click "Save"
    click "Load"

    click "Return"
    pause .6

    run Jump("test")

    click "In testcase code."

    # menu_1
    advance until screen "choice"
    click "Choice A"

    # input
    type "Test User\n"
    click "Name: Test User"

    # Nvl
    advance
    advance
    advance

    advance
    advance

    # NVL Menu.
    advance until eval ("nvl_menu" in renpy.game.context().modes)
    click "Choice B"

    $ renpy.unlink_save("1-1")
    click "Save"

    pause .6

    click "Save slot 1"

    pause .6

    click "Save slot 1"
    click "Yes"

    click "Main Menu"
    click "Yes"

    click "Load"
    click "Load slot 1"

    pause .5

    click "Save"

    pause .5


    click "Load"
    click "Load slot 1"
    click "No"

    click "Return"

    # Done.
    pause .5

    click "Done."
    exit


define nvle = Character("Eileen", kind=nvl)


label test:

    "In testcase code."


menu menu_1:
    "This is a menu."

    "Choice A":
        pass

    "Choice B":
        pass

label after_menu_1:


    $ name = renpy.input("What is your name?")
    "Name: [name]"

    nvle "NVL 1"
    nvle "NVL 2"
    nvle "NVL 3"

    nvl clear

    nvle "NVL 4"
    nvle "NVL 5"
    nvle "NVL 6"


    $ menu = nvl_menu


menu menu_2:
    "This is a menu."

    "Choice A":
        pass

    "Choice B":
        pass

label after_menu_2:

    "Done."

    return
