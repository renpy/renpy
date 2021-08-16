# This file demonstrates some of the text-layout and handling
# capabilities of Ren'Py.


init 1:
    define eslow = Character(kind=e, what_slow_cps=20)

# init python:
#     style.ruby_style = Style(style.default)
#     style.ruby_style.yoffset = -20
#     style.ruby_style.size = 12
#
# define eruby = Character(
#     _("Eileen"),
#     color="#c8ffc8",
#     what_ruby_style=style.ruby_style,
#     what_line_leading=10)


label a_label:

    e "You just clicked to jump to a label."

    jump after_a_label

label text:

    e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."

    example tags1 hide:
        e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."

    e "That's what text tags are for."

    show example tags1

    e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."

    e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."

    example:

        e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."

label after_a_label:

    example:

        e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."

    example:

        e "The color text tag changes the {color=#0080c0}color{/color} of the text."

    example:

        e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."

        e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."


    example:

        e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."

        e "Sometimes, changing to a bold font looks better than using the {{b} tag."


    example:

        e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."


    example:

        e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."


    example:

        e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."

    hide example

    e "There are a few text tags that only makes sense in dialogue."

    example:

        e "The p tag breaks a paragraph,{p}and waits for the player to click."

        e "If it is given a number as an argument,{p=1.5}it waits that many seconds."

    example:

        e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."


    example:

        eslow "The nw tag causes Ren'Py to continue past slow text,{nw}"
        with flashbulb
        extend " to the next statement."


    example:
        e "To break a line without pausing,\none can write \\n. \\' and \\\" include quotes in the text."


    hide example

    e "The interpolation feature takes a variable name in square brackets, and inserts it into text."


    example:
        $ variable = _("{i}variable value{/i}")

        e "For example, this displays the [variable!t]."


    example:
        e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."

    example showtrans:
        $ translatable = _("translatable text")

        e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."

    example:
        e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."

    hide example
    pause .5

    return




# label demo_text:
#
#     e "Ren'Py gives you quite a bit of control over how text appears."
#
#     e "Text tags let us control the appearance of text that is shown to the user."
#
#     e "Text tags can make text {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
#
#     e "They can make the font size {size=+12}bigger{/size} or {size=-8}smaller{/size}."
#
#     e "They let you pause{w} the display of the text, optionally with{p}line breaks."
#
#     e "They let you include images inside text{image=exclamation.png} Neat{image=exclamation.png}"
#
#     e "We can pause the text for a short time, and have it auto-advance.{w=1} Just like that."
#
#     eslow "We can even have the text auto-advance,{nw}"
#
#     with flashbulb
#     extend " when we reach the end of a block of text, in slow text mode."
#
#     e "They can change the {color=#f00}color{/color} {color=#ff0}of{/color} {color=#0f0}the{/color} {color=#0ff}text{/color}."
#
#     # e "There are also bold, italic, strikethrough, and underline style properties, which can be styled onto any text."
#
#     e "The kerning tag lets you adjust the spacing between characters.\n{k=.5}The spacing between characters can be increased.{/k}\n{k=-.5}The spacing between characters can be decreased.{/k}"
#
#     eruby "You are able to write ruby text, which can help clarify how to pronounce words, like {rb}Ren'Py{/rb}{rt}ren-pie{/rt}."
#
#     e "{a=define_hyperlink}Hyperlinks{/a} let buttons be defined using text tags."
#
#     e "The space and vspace tags add {space=30} horizontal and {vspace=20}vertical space, respectively."
#
#     e "You can define your own text tags, {=pink}that use a style you define.{/=pink}"
#
#     e "If you find yourself using text tags on every line, you should probably look at style properties instead."
#
#     e "Used with care, text tags can enhance {b}your{/b} game."
#
#     e "{u}Used{/u} with {i}abandon,{/i} they {b}can{/b} make {b}your{/b} game {color=#333}hard{/color} {color=#888}to{/color} {color=#ccc}read{/color}."
#
#     e "With great power comes great responsibility, after all."
#
#     e "And we want to give you all the power you need."
#
#     e "There are a couple of text adjustments that don't correspond to text tags."
#
#     eoutline "The outlines setting lets you put outlines around the text."
#
#     eoutline "You can have more than one outline, and each has its own color and offset."
#
#     window hide
#
#     esubtitle "Here, we have two outlines around the white text."
#
#     esubtitle "The bottom one is a translucent black that's offset a little, while the top one is green."
#
#     esubtitle "By hiding the window and adjusting the layout method, we are able to create reasonable subtitles."
#
#     esubtitle "This might be an interesting look for a game."
#
#     window show
#
#     e "Well, that's it for fonts and text tags."
#
#
#     return
#
#
# label define_hyperlink:
#
#     definition "A hyperlink is a button that is defined inside text, using text tags. They're ideal for including definitions of words used in the script, but they shouldn't be used in place of menus."
#
#     return
