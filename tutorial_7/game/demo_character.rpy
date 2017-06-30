# This file demonstrates how Character objects can be used to customize the
# display of text.

init python:
    config.searchpath.append("../launcher/game/fonts")

label demo_character:

    "There are quite a few properties that apply. Here, ill'll show you some of the most useful."

    example:
        define e1 = Character("Eileen", window_background="gui/startextbox.png")

        e1 "The window_background property sets the image thay's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."

    example:

        define e1a = Character("Eileen", window_background=None)

        e1a "If it's set to None, the textbox has no background window."

    example:
        define e2 = Character("Eileen", who_color="#c8ffc8", what_color="#ffc8c8")

        e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."

        e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."

    example:

        define e3 = Character("Eileen", who_font="Roboto-Regular.ttf", what_font="Roboto-Light.ttf")

        e3 "Similarly, the ``who_font`` and ``what_font`` properties set the font used by the different kinds of text."


    example:

        define e4 = Character("Eileen", who_bold=True, what_italic=True, what_size=20)

        e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."

        e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."


    example:

        define e5 = Character("Eileen", what_outlines=[( 1, "#008000", 0, 0 )] )

        e5 "The ``what_outlines`` property puts an outline around the text."

        e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."

        e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."

    example:

        define e6 = Character("Eileen", what_outlines=[( 0, "#808080", 2, 2 )] )

        e6 "When the outline size is 0 and the offsets are given, ``what_outlines`` can also act as a drop-shadow behind the text."


    example:
        define e7 = Character("Eileen", what_xalign=0.5, what_textalign=0.5, what_layout='subtitle')

        e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."

        e7 "The what_xalign property controls where all the text text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."

        e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."

        e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."

    example large:

        define e8 = Character(
            None,
            window_background = None,

            what_size=28,
            what_outlines=[( 1, "#008000", 0, 0 )],
            what_xalign=0.5,
            what_textalign=0.5,
            what_layout='subtitle')

    e8 "These properties can be combined to achieve many different effects."

    e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."


    hide example

    return

