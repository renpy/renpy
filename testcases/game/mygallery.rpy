image b0 red = "#f00"
image b0 green = "#0f0"
image b0 blue = "#00f"
image b1 red = "#f00"
image b1 green = "#0f0"
image b1 blue = "#00f"
image b2 red = "#f00"
image b2 green = "#0f0"
image b2 blue = "#00f"


init python:
    g = Gallery()

    g.button("b0")
    g.unlock_image("b0 red")
    g.unlock_image("b0 green")
    g.unlock_image("b0 blue")

    g.button("b1")
    g.unlock_image("b1 red")
    g.unlock_image("b1 green")
    g.unlock_image("b1 blue")

    g.button("b2")
    g.unlock_image("b2 red")
    g.unlock_image("b2 green")
    g.unlock_image("b2 blue")


screen gallery:
    vbox:
        textbutton "b0" action g.Action("b0")
        textbutton "b1" action g.Action("b1")
        textbutton "b2" action g.Action("b2")

label gallery:
    show b0 green
    show b0 blue
    hide b0

    show b1 green
    hide b1

    call screen gallery

    return

