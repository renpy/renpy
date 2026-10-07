testsuite global:
    setup:
        $ _test.screenshot_directory = "tests/screenshots/testcases"
        if eval not renpy.mobile:
            assert eval renpy.get_physical_size() == (config.screen_width, config.screen_height)
            assert eval renpy.pygame.display.get_drawable_size() == (config.screen_width, config.screen_height)

    before testsuite:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 2.0

        if eval not renpy.context()._main_menu: #screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit
