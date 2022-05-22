image logo blink:
    "logo base"
    pause 0.5
    linear .5 alpha 0.0
    pause 0.5
    linear .5 alpha 1.0
    repeat

transform logopos:
    xalign .5
    ypos 50

label simple_displayables:

    e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."

    example:
        image logo base = "logo base.png"

    show logo base at logopos

    e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."

    example:
        image logo alias = "logo base"

    show logo alias at logopos

    e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."

    hide logo with dissolve

    example:
        image bg red = "#c00"
        image bg blue = "#0000cc"
        image overlay red = "#c008"
        image overlay blue = "#0000cc88"

    show bg blue with dissolve

    e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."

    e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."

    show bg washington with dissolve

    example:
        image logo rotated = Transform("logo base", rotate=45)

    show logo rotated at logopos
    with dissolve

    e "The Transform displayable takes a displayable and can apply transform properties to it."

    e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."

    example:
        image logo solidexample = Solid("#0000cc", xysize=(200, 200))

    show logo solidexample at logopos
    with dissolve

    e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."


    example:
        image logo text = Text(_("This is a text displayable."), size=30)

    show logo text at logopos
    with dissolve

    e "The Text displayable lets Ren'Py treat text as if it was an image."

    example:
        image logo text rotate = Transform(Text(_("This is a text displayable."), size=30), rotate=45)

    show logo text rotate at logopos
    with dissolve

    e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."

    example:
        image logo composite = Composite((240, 460),
            (0, 0), "logo blink",
            (0, 50), "logo base.png",
            (0, 100), "logo base.png")

    show logo composite at logopos
    with dissolve

    e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."

    hide logo

    example:
        image ninepatch frame = Frame("ninepatch", 40, 40, 40, 40)

    show ninepatch frame at logopos:
        size (120, 120)

    e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."

    show ninepatch frame at logopos:
        size (120, 120)
        linear 3.0 size (360, 360)
        pause 1.0
        linear 3.0 size (120, 120)
        pause 1.0
        repeat

    e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."

    example:
        image ninepatch frame tiled = Frame("ninepatch", 40, 40, 40, 40, tile=True)

    show ninepatch frame tiled

    e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."

    example:
        image ninepatch paper tiled = Frame("ninepatch paper", 40, 40, 40, 40, tile=True)

    show ninepatch paper tiled
    with dissolve

    e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."

    hide ninepatch
    hide example
    with dissolve

    e "These are just the simplest displayables, the ones you'll use directly the most often."

    e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."

    return
