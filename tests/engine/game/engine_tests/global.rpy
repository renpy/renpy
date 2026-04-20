testsuite global:
    setup:
        $ _test.screenshot_directory = "screenshots"

    before testsuite:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 2.0

        if eval not renpy.context()._main_menu: #screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit
