# This file demonstrates how Character objects can be used to customize the
# display of text.

init:
    # With a nestled click-to-continue indicator.
    $ ectc = Character(_('Eileen'),
                       color="#c8ffc8",
                       ctc=anim.Blink("arrow.png"))


    # With a fixed-position ctc indicator.
    $ ectcf = Character(_('Eileen'),
                        color="#c8ffc8",
                        ctc=anim.Filmstrip("sakura.png", (20, 20), (2, 1), .30, xpos=760, ypos=560, xanchor=0, yanchor=0),
                        ctc_position="fixed")

    # With quotes around text.
    $ equote = Character(_('Eileen'),
                         color="#c8ffc8",
                         who_suffix = ':',
                         what_prefix='"',
                         what_suffix='"')

    # Weird-looking.
    $ eweird = Character(_('Eileen'),
                         color="#c8ffc8",
                         what_underline=True,
                         window_left_margin=200,
                         window_yminimum=300)

    # Two-window mode.
    $ etwo = Character(_('Eileen'),
                       color="#c8ffc8",
                       show_two_window=True)

    # Image on the side.
    $ eside = Character(_('Eileen'),
                        color="#c8ffc8",
                        window_left_padding=160,
                        show_side_image=Image("eileen_side.png", xalign=0.0, yalign=1.0))

label demo_character:


    e "The Character object is used to declare characters, and it can also be used to customize the way in which a character speaks."

    e "By supplying it with the appropriate arguments, we can really change around the feel of the game."

    e "In this section, we'll demonstrate some of what can be accomplished by customizing character objects."

    equote "By supplying what_prefix and what_suffix arguments to a Character object, we can automatically add things before each line of text."

    equote "This is a lot easier than having to put those quotes in by hand."

    equote "We can also use who_prefix and who_suffix to add text to the name of the speaker."

    e "We can also supply arguments to the Character object that customize the look of the character name, the text that is being said, and the window itself."

    eweird "These can really change the look of the game."

    eside "A more practical use of that is in conjunction with show_side_image, which lets us position an image next to the text."

    etwo "There's also show_two_window, which puts the character's name in its own window."

    ectc "Finally, we demonstrate a click to continue indicator. In this example, it's nestled in with the text."

    ectcf "A click to continue image can also be placed at a fixed location on the screen."

    e "There's a lot more you can do with Character, as it lets you set style properties on all of the displayed text."

    e "Finally, let me point out a couple of special characters we pre-define."

    show black
    with dissolve

    centered "The \"centered\" character shows text at the center of the screen, without a window."

    centered "It's just a highly customized normal character, that's useful for dates and titles."

    hide black
    with dissolve

    e "The \"extend\" character is very special."

    e "It lets you"

    show eileen vhappy

    extend " extend the previous dialogue"

    show eileen happy

    extend " with additional text."

    e "That lets you have things happen in the middle of text. If you didn't notice, I was changing my expression."

    e "Hopefully, these characters, along with the ones you define, will lead to a very expressive game."

    return
