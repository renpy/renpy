# This file demonstrates how Character objects can be used to customize the
# display of text.

label demo_character:

    e "We saw before how a Character object can be used to assign a name to a character. But there are a lot of other ways character objects can customize dialogue and thoughts."

    e "The main way is by setting style properties on a character-by-character basis."

    example:
        define ebluewhat = Character(_("Eileen"), what_color="#ccccff")

        ebluewhat "When a style property is prefixed with 'what_', it's given to the text that's being spoken."


    example:

        define eredwho = Character(_("Eileen"), who_color="#cc8888")
        define ered = Character(_("Eileen"), color="#cc8888")

        eredwho "A style property that is prefixed with 'who_' is applied to the name of the speaking character."
        ered "Style properties that have no prefix are also given to the name of the speaking character."


    example:
        define eblackwindow = Character(_("Eileen"), window_background="#000000f0")

        eblackwindow "Finally, style properties prefixed with 'window_' apply to the dialogue window."


    example:
        define eoutline = Character(
            None,
            window_background="#0000",
            what_outlines=[ (3, "#008000", 0, 0) ],
            what_size=28,
            what_text_align=0.5,
            what_xalign=0.5,
            what_layout="subtitle"
            )


        eoutline "While each single style property makes only a small change, multiple properties can massively change the look of the game."


    example:
        define equoted = Character(_("Eileen"), what_prefix='"', what_suffix='"')

        equoted "There are other arguments that can be given to Character. I'll show you a few of the most common ones here."

        equoted "The what_prefix and what_suffix can be used to add text to the start and end of dialogue, respectively."

    example:

        define eside = Character(_("Eileen"), image="eileen")
        image side eileen happy = Transform("eileen happy", crop=(0, 0, 320, 400), zoom=.6)
        image side eileen vhappy = Transform("eileen vhappy", crop=(0, 0, 320, 400), zoom=.6)

        eside "The image argument associates an image with a character."
        eside vhappy "It lets dialogue take attributes, which can be used to change the image associated with the character."
        eside happy "When the character speaks, Ren'Py will look for a side image assoicated with the character. It will apply image attributes, then show the side image."


    example:
        define big = Character(None, what_size=26)
        define ebig = Character(_("Eileen"), kind=big)
        define lbig = Character(_("Lucy"), kind=big)

        ebig "The kind argument takes a Character to use as a template. This makes it possible to customize a single Charater, then copy it."


    example:
        e "Finally, there are a couple of special characters we want to mention."
        extend " The extend character appends text to the last thing spoken."

    example:
        e "The narrator character is used to customize narration. Understand?"

        narrator "I get it."
        "I get that this line and the last line are both narration."





    hide example
    pause .5

    return

