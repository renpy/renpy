testcase default:
    # Bad end
    "start"
    click until screen choice
    "ask her later"
    click until screen main_menu


    # Good end
    $ _test.transition_timeout = 0.0

    "start"
    click until "ask her right away"
    click until ("an interactive book" or "video game")
    click until eval (not renpy.has_default_focus())
    "quit"
