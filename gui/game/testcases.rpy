testcase default:

    "Start"
    pause .6

    # Test rollback
    "Hello, World."
    "Back"

    # Test history.
    click
    click
    "History"
    pause .6

    # Test Help.
    "Help"
    "Keyboard"

    # Test About
    "About"

    # Test Preferences
    "Preferences"

    "Left"
    "Right"
    "Disable"

    "Unseen Text"
    "Unseen Text"

    "After Choices"
    "After Choices"

    "Transitions"
    "Transitions"

    "Mute All"
    "Mute All"

    "Save"
    "Load"

    "Return"
    pause .6

    run Jump("test")

    "In testcase code."

    # menu_1
    click until "Choice A"


    # input
    type "Test User\n"
    "Name: Test User"

    # Nvl
    click
    click
    click

    click
    click
    click until "NVL 6"

    # NVL Menu.
    "Choice B"

    $ renpy.unlink_save("1-1")
    "Save"

    pause .6

    "Save slot 1"

    pause .6

    "Save slot 1"
    "Yes"

    "Main Menu"
    "Yes"

    "Load"
    "Load slot 1"

    pause .5

    "Save"

    pause .5


    "Load"
    "Load slot 1"
    "No"

    "Return"

    # Done.
    pause .5

    "Done."
    "Quit"


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
