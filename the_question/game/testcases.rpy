testcase default:
    "start"
    click until "ask her right away"
    click until ("an interactive book" or "video game")
    click until eval (not renpy.has_default_focus())
    "quit"
