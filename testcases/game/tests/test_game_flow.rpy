label branching:
label .basic:
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    "Aenean a tellus vitae dolor mattis dignissim."
    "Pellentesque blandit lectus et dolor lobortis consequat."
    "Fusce quis ante tempus, eleifend nibh quis, venenatis urna."

    menu:
        "Terminate":
            "Leaving label"
            return

        "Continue":
            pass

    menu:
        "Submenu test"
        "Option 1":
            menu:
                "Option 1.1":
                    pass
                "Option 1.2":
                    menu:
                        "Option 1.2.1":
                            "You chose option 1.2.1."

    "Cras tempor mauris nec tincidunt rutrum."
    "Suspendisse a mi eget orci molestie malesuada non ut neque."
    "Mauris at nisi eu mi vulputate varius."

    return

testcase menus_and_branching:
    $ _test.transition_timeout = 0.00

    run Start("branching")
    advance until screen choice
    click "Terminate"
    advance until screen main_menu

    run Start("branching")
    advance until screen choice
    click "Continue"
    click "Option 1"
    click "Option 1.1"
    advance until screen main_menu

    run Start("branching")
    advance until screen choice
    click "Continue"
    click "Option 1"
    click "Option 1.2"
    click "Option 1.2.1"
    advance until screen main_menu


################################

label .variable_test:
    $ menu_var = 0
label .variable_test2:
    menu:
        "Value: [menu_var]":
            pass

        "Increment":
            $ menu_var += 1

        "Decrement" if menu_var > 0:
            $ menu_var -= 1

        "Reset" if menu_var != 0:
            $ menu_var = 0

        "Done" if menu_var >= 3:
            return

    jump .variable_test2

testcase menus_and_branching_variables:
    run Start("branching.variable_test")

    pause until screen choice
    assert not "Decrement"
    assert not "Reset"
    assert not "Done"

    click "Increment"
    assert "Value: 1" timeout 2.0
    assert "Decrement"
    assert "Reset"
    assert not "Done"

    click "Reset"
    assert not "Decrement"
    assert not "Reset"

    click "Increment"
    click "Increment"
    click "Decrement"
    click "Increment"
    click "Increment"
    assert "Value: 3" timeout 2.0

    click "Done"


label global_label:
    "Under a global label.."
label .local_label:
    "..resides a local one."
    jump .another_local
label .another_local:
    "And another !"
    jump .local_label

label another_global:
    "Now lets jump inside a local label located somewhere else."
    jump global_label.local_name


##############################
## Test cases
##############################

testcase label_control_flow:
    $ _test.transition_timeout = 0.00
    run Start("global_label")
    pause 0.5
    click
    pause 0.5
