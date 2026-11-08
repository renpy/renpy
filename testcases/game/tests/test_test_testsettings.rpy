## This file tests the timeout and screenshot settings of the test language.

# ==============
# == Fixtures ==
# ==============

label hard_pause:
    "Before hard pause."
    $ renpy.pause(0.5, hard=True)
    "End"

# ==============
# === Tests ====
# ==============

testsuite screenshot:
    setup:
        run Preference("display", 1.0)

        # Other tests change these, so reset them to their defaults to keep the preferences screen fixed.
        run Preference("text speed", 0)
        run Preference("auto-forward time", 0)

        # Earlier tests leave the mouse at a random position, which could hover over a button. No
        # screen in this suite has anything here.
        move pos (300, 500)

    testcase main_menu:
        screenshot "main_menu.png" #crop (0, 0, 400, 300)

    testsuite menus:
        parameter screen_name = ["preferences", "load"]

        setup:
            run ShowMenu(screen_name)

        teardown:
            run Return()

        testcase menu_screen:
            screenshot f"screens/{screen_name}.png"

testsuite timeout:
    setup:
        run Start("hard_pause")
        assert screen "say"

    # The testcases below change the timeout, and leave the game showing the last line of the hard_pause
    # label, so this dismisses it, which ends the game and returns to the main menu.
    teardown:
        $ _test.timeout = 2.0
        advance until screen "main_menu"

    testcase hard_pause_fail_timeout:
        xfail True

        $ _test.timeout = 0.2
        advance until "End"

    testcase hard_pause_pass_timeout:
        $ _test.timeout = 1.0
        advance until "End"
