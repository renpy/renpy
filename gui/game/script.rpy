# You can place the script of your game in this file.

define e = Character("Eileen")

label start:

    scene expression "#ff0000"

    e "Hello, and welcome to the game."

    scene expression "#000080"
    with dissolve

    e "It's good to see you."

    menu:
        "This is a choice."

        "The first choice.":
            pass
        "The second choice.":
            pass
        "The third choice.":
            pass

    return
