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
    advance until screen "choice"
    click "Terminate"
    advance until screen "main_menu"

    run Start("branching")
    advance until screen "choice"
    click "Continue"
    click "Option 1"
    click "Option 1.1"
    advance until screen "main_menu"

    run Start("branching")
    advance until screen "choice"
    click "Continue"
    click "Option 1"
    click "Option 1.2"
    click "Option 1.2.1"
    advance until screen "main_menu"


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

    pause until screen "choice"
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

    # for_loops.menu_choices and while_loops.real_choices in test_test_testast_flow.rpy click through the full
    # Increment/Decrement sequence, so this only needs to get to the value where "Done" appears.
    click "Increment"
    click "Increment"
    click "Increment"
    assert "Value: 3" timeout 2.0
    assert "Done"

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
    assert "Under a global label.." timeout 2.0

    # A global label falls through into the local label that follows it.
    advance until "..resides a local one."

    # The local labels then jump to each other, and the last one jumps back to the first.
    advance until "And another !"
    advance until "..resides a local one."

    run MainMenu(confirm=False, save=False)


##############################
## Translated say statements and scry
##############################

define ast_scry_nvl = Character(None, kind=nvl, ctc=Text("LINE CTC"), page_ctc=Text("PAGE CTC"))

label translate_say_scry:
    nvl clear
    ast_scry_nvl "One." id ast_scry_one
    ast_scry_nvl "Two." id ast_scry_two
    nvl clear
    ast_scry_nvl "Three." id ast_scry_three
    "Done."
    return

# nvl clear is translatable, so it is part of the block for the first and third lines.
translate ast_scry ast_scry_one:
    nvl clear
    ast_scry_nvl "Un."

translate ast_scry ast_scry_two:
    ast_scry_nvl "Deux."

translate ast_scry ast_scry_three:
    nvl clear
    ast_scry_nvl "Trois."

init python:
    def ast_scry_line():
        """
        Returns the text of the current NVL line and the text of its click-to-continue indicator, or None in place
        of either that is missing.

        The test uses this instead of text selectors, which never match the indicator.
        """

        what = renpy.get_widget("nvl", "what", config.nvl_layer)

        if what is None:
            return (None, None)

        # The indicator is wrapped, for example in a CTCPauseHolder, so search inside it for its Text.
        pending = [ getattr(what, "ctc", None) ]
        ctc = None

        while pending:
            d = pending.pop()

            if isinstance(d, Text):
                ctc = "".join(str(i) for i in d.text)
                break

            if d is not None:
                pending.extend(d.visit())

        return ("".join(str(i) for i in what.text), ctc)

testsuite translate_say_scry:
    teardown:
        run Language(None)

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    # Only a line followed by nvl clear shows the page CTC, in the default language and in a translation, which
    # used to show it after every line (#7537). Each assertion waits for the line's text to finish, so the advance
    # that follows goes to the next line.
    testcase nvl_page_ctc:
        parameter (language, first, second, third) = [(None, "One.", "Two.", "Three."), ("ast_scry", "Un.", "Deux.", "Trois.")]

        $ _test.transition_timeout = 0.00
        run Language(language)
        run Start("translate_say_scry")

        assert eval (ast_scry_line() == (first, "LINE CTC")) timeout 2.0
        advance
        assert eval (ast_scry_line() == (second, "PAGE CTC")) timeout 2.0
        advance
        assert eval (ast_scry_line() == (third, "LINE CTC")) timeout 2.0
