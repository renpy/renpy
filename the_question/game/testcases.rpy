testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 2.0

        if not screen "main_menu":
            run MainMenu(confirm=False)


    teardown:
        exit

testcase bad_end:
    click "start"
    advance until screen "choice"
    click "ask her later"
    advance until screen "main_menu"

testcase good_end:
    click "start"
    advance until "ask her right away"
    click "ask her right away"
    advance until ("an interactive book" or "video game")
    assert not "video game" ## Last condition fails since it's "videogame" in script
    assert "videogame"
    click "an interactive book"
    advance until screen "main_menu"

testcase history_screen_from_quick_menu:
    click "Start"

    # Open and close history using mouse
    click "History"
    pause 0.5
    click "Return"

    # Open and close history using keysyms
    keysym "K_RETURN" "History"
    pause 0.5
    keysym "game_menu"

    assert not screen "history"
