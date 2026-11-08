## This file tests the selector, drag, scroll, and expression-taking statements of the test language.

# ==============
# == Fixtures ==
# ==============

screen teleporting_button(x=0, y=0, remaining=20):
    textbutton "Teleporting Button":
        id "teleporting_button"
        xpos x
        ypos y
        if remaining > 0:
            action Show("teleporting_button", x=(x + 23) % 400, y=(y + 47) % 400, remaining=remaining - 1)
        else:
            action Hide("teleporting_button")

screen button_release_origin__screen():
    default clicked = None
    vbox:
        xpos 100
        ypos 100

        textbutton "First":
            id "button_release_first"
            action SetScreenVariable("clicked", "first")

        textbutton "Second":
            id "button_release_second"
            action SetScreenVariable("clicked", "second")

        textbutton "Reset":
            id "button_release_reset"
            action SetScreenVariable("clicked", None)

screen test_expressions__input__screen():
    default input_value = ""

    input:
        id "test_expressions__input"
        value ScreenVariableInputValue("input_value")


# The drag_and_drop screen is in script.rpy, as it is also an entry in the start menu.

screen scroll_screen:
    viewport:
        id "scroll_vp"
        draggable True
        mousewheel True

        vbox:
            spacing 10

            for i in range(50):
                text "This is line [i]."

            textbutton "Close" action Hide("scroll_screen") id "close_screen_button"


# ==============
# === Tests ====
# ==============

testsuite selectors:
    testcase button_release_origin:
        run Show("button_release_origin__screen")
        pause until screen "button_release_origin__screen"

        # These clicks should set the screen variable "clicked" to the button id,
        # and then reset it to None.
        for button_id in ["first", "second"]:
            click id f"button_release_{button_id}"

            python:
                result = renpy.exports.get_screen_variable("clicked", "button_release_origin__screen")
                assert result == button_id, f"Click, expected '{button_id}', got {result!r}"

            click id "button_release_reset"

        # The rest of these drags should not set the screen variable "clicked" to anything.
        drag id "button_release_first" to id "button_release_second"
        python:
            result = renpy.exports.get_screen_variable("clicked", "button_release_origin__screen")
            assert result is None, f"Drag from other button, expected None, got {result!r}"

        drag pos (0, 0) to id "button_release_second"
        python:
            result = renpy.exports.get_screen_variable("clicked", "button_release_origin__screen")
            assert result is None, f"Drag from empty space, expected None, got {result!r}"

        drag id "button_release_first" to pos (0, 0)
        python:
            result = renpy.exports.get_screen_variable("clicked", "button_release_origin__screen")
            assert result is None, f"Drag to empty space, expected None, got {result!r}"

        run Hide("button_release_origin__screen")

    testcase bounds_test:
        # Peg bounds: (100, 100) to (200, 200), size: (100, 100)
        # Hole bounds: (450, 140) to (600, 290), size: (150, 150)

        run Show("drag_and_drop")
        pause until screen "drag_and_drop"

        # Top left corner
        move id "peg" pos (0, 0)
        $ mpos = renpy.exports.get_mouse_pos()
        $ assert mpos == (100, 100), f"Peg position after move is {mpos}, expected (100, 100)"

        # Absolute offset
        move id "peg" pos (23, 45)
        $ mpos = renpy.exports.get_mouse_pos()
        $ assert mpos == (123, 145), f"Peg position after move is {mpos}, expected (123, 145)"

        # Relative offset
        move id "peg" pos (0.5, 1.0)
        $ mpos = renpy.exports.get_mouse_pos()
        $ assert 149 <= mpos[0] <= 151, f"Peg position after move is {mpos}, expected roughly (150, 200)"
        $ assert 199 <= mpos[1] <= 201, f"Peg position after move is {mpos}, expected roughly (150, 200)"

        # Position outside the bounds of the peg
        move id "peg" pos (-50, 2.0)
        $ mpos = renpy.exports.get_mouse_pos()
        $ assert mpos[0] == 50, f"Peg position after move is {mpos}, expected (50, 200)"
        $ assert 298 <= mpos[1] <= 302, f"Peg position after move is {mpos}, expected (50, 200)"

        # Hole
        move id "hole" pos (0, 0)
        $ mpos = renpy.exports.get_mouse_pos()
        $ assert mpos == (450, 140), f"Hole position after move is {mpos}, expected (450, 140)"

        # Relative offset
        move id "hole" pos (0.5, 0.5)
        $ mpos = renpy.exports.get_mouse_pos()
        $ assert 524 <= mpos[0] <= 526, f"Hole position after move is {mpos}, expected roughly (525, 215)"
        $ assert 214 <= mpos[1] <= 216, f"Hole position after move is {mpos}, expected roughly (525, 215)"

        run Hide("drag_and_drop")

    testcase drag_and_drop:
        run Show("drag_and_drop")
        pause until screen "drag_and_drop"

        assert screen "drag_and_drop"
        drag id "peg" pos (0, 0) to id "hole" pos (0, 0)
        assert id "success"

        # Back to the start
        drag id "peg" pos (0, 0) to pos (100, 100)
        assert not id "success"

        # Using the peg and hole ids
        drag id "peg" pos (0, 0) to id "hole" pos (0, 0)
        assert id "success"

        # Slightly out of bounds
        drag id "peg" pos (0, 0) to id "hole" pos (1.01, 0)
        assert not id "success"

        # Back in bounds
        drag id "peg" pos (0, 0) to id "hole" pos (1.0, 0)
        assert id "success"

        # Slightly out of bounds
        drag id "peg" pos (0, 0) to id "hole" pos (-101, 0)
        assert not id "success"

        # Back in bounds
        drag id "peg" pos (0, 0) to id "hole" pos (-99, -99)
        assert id "success"

        # -150 offset (50 pixels of distance to overlap)
        drag id "peg" pos (0, 0) to id "hole" pos (-1.0, 0)
        assert not id "success"

        # Back in bounds
        drag id "peg" pos (0, 0) to id "hole" pos (-0.5, 0)
        assert id "success"

        # We're not actually dragging the peg, so no change
        drag id "peg" pos (-0.1, 0) to id "hole" pos (1.01, 0)
        assert id "success"

        run Hide("drag_and_drop")


    testcase screen_and_id_selectors:
        assert screen "main_menu"
        assert id "quit_button"
        assert screen "main_menu" id "quit_button"

testsuite test_expressions:
    description "Tests that test statements accept Python expressions."

    after testcase:
        run Return()
        run Hide()
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase keysym:
        description "Keysym accepts a variable for the keysym name."

        run Show("test_expressions__input__screen")
        assert screen "test_expressions__input__screen"
        click id "test_expressions__input"

        $ keyval = "K_a"
        keysym keyval

        $ value = renpy.exports.get_screen("test_expressions__input__screen").scope.get("input_value", "NOT DEFINED")
        $ assert value == "a", f"Expected 'a', got '{value}'"

        run Hide("test_expressions__input__screen")

    testcase type:
        description "Type accepts a variable for the text to type."

        run Show("test_expressions__input__screen")
        assert screen "test_expressions__input__screen"
        click id "test_expressions__input"

        $ textval = "Hello"
        type textval

        $ value = renpy.exports.get_screen("test_expressions__input__screen").scope.get("input_value", "NOT DEFINED")
        $ assert value == "Hello", f"Expected 'Hello', got '{value}'"

        run Hide("test_expressions__input__screen")

    testcase drag_button_steps_before_to:
        description "Drag accepts expressions for button and steps."

        run Show("drag_and_drop")
        assert screen "drag_and_drop"

        $ btn = 1
        $ step_count = 10
        drag id "peg" pos (0, 0) button btn steps step_count to id "hole" pos (0, 0)
        assert id "success"

        run Hide("drag_and_drop")

    testcase drag_button_steps_after_to:
        description "Drag accepts expressions for button and steps (after to)."

        run Show("drag_and_drop")
        assert screen "drag_and_drop"

        $ btn = 1
        $ step_count = 10
        drag id "peg" pos (0, 0) to id "hole" pos (0, 0) button btn steps step_count
        assert id "success"

        run Hide("drag_and_drop")

    testcase click_button:
        description "Click button accepts a variable for the button number."

        run Show("teleporting_button")
        assert screen "teleporting_button"

        $ btn = 1
        $ element_id = "teleporting_button"
        $ screen_name = "teleporting_button"
        click button btn id element_id until not screen screen_name

    testcase click_after_pointer_leaves_window:
        description "The user's pointer leaving the window doesn't stop simulated clicks."

        run Show("teleporting_button")
        assert screen "teleporting_button"

        $ renpy.pygame.event.post(renpy.pygame.event.Event(renpy.pygame.WINDOWMOUSELEAVE))
        click id "teleporting_button" until not screen "teleporting_button"

    testcase scroll_amount:
        description "Scroll amount accepts a variable for the scroll amount."

        run Show("scroll_screen")
        assert screen "scroll_screen"

        assert eval (renpy.get_widget("scroll_screen", "scroll_vp").yadjustment.value == 0)

        $ scroll_amount = 50
        scroll amount scroll_amount id "scroll_vp"
        assert eval (renpy.get_widget("scroll_screen", "scroll_vp").yadjustment.value > 0)

        click id "close_screen_button"
        assert not screen "scroll_screen"

    testcase repeat:
        description "Repeat accepts an expression for the count."

        run Show("test_expressions__input__screen")
        assert screen "test_expressions__input__screen"
        click id "test_expressions__input"

        $ num = 4
        keysym "K_a" repeat num

        $ value = renpy.exports.get_screen("test_expressions__input__screen").scope.get("input_value", "NOT DEFINED")
        $ assert value == "aaaa", f"Expected 'aaaa', got '{value}'"

        run Hide("test_expressions__input__screen")

    testcase skip_fast:
        description "Skip fast works."

        run Start("three_messages")
        assert screen "say"

        skip fast
        $ assert renpy.config.skipping == "fast", f"Expected 'fast', got {renpy.config.skipping!r}"
        $ renpy.config.skipping = None


    testsuite label:
        description "Tests the label selector with quoted strings, naked names, and variables."

        testcase naked_name:
            description "Label selector matches a naked label name."

            run Start("three_messages")
            assert label three_messages timeout 0.2

        testcase quoted_string:
            description "Label selector matches a quoted string literal."

            run Start("three_messages")
            assert label "three_messages" timeout 0.2

        testcase variable:
            description "Label selector matches a variable."

            $ label_name = "three_messages"
            run Start("three_messages")
            assert label label_name timeout 0.2

        testcase negative:
            description "Label selector does not match an unreached label."

            run Start("three_messages")
            assert screen "say"
            assert not label "hard_pause"
