testsuite global:
    before testsuite:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 2.0

        if not screen main_menu:
            run MainMenu(confirm=False)

    teardown:
        exit
