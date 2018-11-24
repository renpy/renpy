# This file demonstrates how Character objects can be used to customize the
# display of text.

init python:
    config.searchpath.append("../launcher/game/fonts")

label demo_character:

    show example characters

    e "We've already seen how to define a Character in Ren'Py. But I want to go into a bit more detail as to what a Character is."

    example:
        define e_shout = Character("Eileen", who_color="#c8ffc8", what_size=34)
        define e_whisper = Character("Eileen", who_color="#c8ffc8", what_size=18)

    e "Here are couple of additional characters."

    e "Each statement creates a Character object, and gives it a single argument, a name. If the name is None, no name is displayed."

    e "This can be followed by named arguments that set properties of the character. A named argument is a property name, an equals sign, and a value."

    e "Multiple arguments should be separated with commas, like they are here. Let's see those characters in action."

    example:

        e_shout "I can shout!"

        e_whisper "And I can speak in a whisper."

    e "This example shows how the name Character is a bit of a misnomer. Here, we have multiple Characters in use, but you see it as me speaking."

    e "It's best to think of a Character as repesenting a name and style, rather than a single person."

    hide example

    e "There are a lot of properties that can be given to Characters, most of them prefixed styles."

    e "Properties beginning with window apply to the textbox, those with what apply to the the dialogue, and those with who to the name of Character speaking."

    e "If you leave a prefix out, the style customizes the name of the speaker."

    e "There are quite a few different properties that can be set this way. Here are some of the most useful."

    example:
        define e1 = Character("Eileen", window_background="gui/startextbox.png")

        e1 "The window_background property sets the image that's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."

    example:

        define e1a = Character("Eileen", window_background=None)

        e1a "If it's set to None, the textbox has no background window."

    example:
        define e2 = Character("Eileen", who_color="#c8ffc8", what_color="#ffc8c8")

        e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."

        e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."

    example:

        define e3 = Character("Eileen", who_font="Roboto-Regular.ttf", what_font="Roboto-Light.ttf")

        e3 "Similarly, the who_font and what_font properties set the font used by the different kinds of text."


    example:

        define e4 = Character("Eileen", who_bold=True, what_italic=True, what_size=20)

        e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."

        e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."


    example:

        define e5 = Character("Eileen", what_outlines=[( 1, "#008000", 0, 0 )] )

        e5 "The what_outlines property puts an outline around the text."

        e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."

        e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."

    example:

        define e6 = Character("Eileen", what_outlines=[( 0, "#808080", 2, 2 )] )

        e6 "When the outline size is 0 and the offsets are given, what_outlines can also act as a drop-shadow behind the text."


    example:
        define e7 = Character("Eileen", what_xalign=0.5, what_textalign=0.5, what_layout='subtitle')

        e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."

        e7 "The what_xalign property controls where all the text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."

        e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."

        e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."

    hide example


    e8 "These properties can be combined to achieve many different effects."

    example large:

        define e8 = Character(
            None,
            window_background = None,

            what_size=28,
            what_outlines=[( 1, "#008000", 0, 0 )],
            what_xalign=0.5,
            what_textalign=0.5,
            what_layout='subtitle')

    e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."

    hide example
    with dissolve

    example small:

        define e9 = Character("Eileen", what_prefix='"', what_suffix='"')

        e9 "There are two interesting non-style properties, what_prefix and what_suffix. These can put text at the start and end of a line of dialogue."

    example:

        define l8 = Character(kind=e8, what_outlines=[( 1, "#c00000", 0, 0 )] )

    e "By using kind, you can copy properties from one character to another, changing only what you need to."

    hide example
    with dissolve

    scene bg cave
    show lucy happy
    with slideleft

    l8 "Like this! Finally I get some more dialogue around here."

    scene bg washington
    show eileen happy
    with slideawayleft

    example:
        define narrator = Character(what_italic=True)

    e "The last thing you have to know is that there's a special character, narrator, that speaks narration. Got it?"

    "I think I do."

    hide example

    return
