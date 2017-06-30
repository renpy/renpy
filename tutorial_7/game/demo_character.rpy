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

        e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brakets around them."

        e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."

    example:

        define e6 = Character("Eileen", what_outlines=[( 0, "#808080", 2, 2 )] )

        e6 "When the outline size is 0 and the offsets are given, ``what_outlines`` can also act as a drop-shadow behind the text."


    example:
        define e7 = Character("Eileen", what_xalign=0.5, what_textalign=0.5, what_layout='subtitle')


        e7 "Something here."


    hide example

    return

