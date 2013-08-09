# This file demonstrates some of the text-layout and handling
# capabilities of Ren'Py.

init:
    # Register an sfont.
    $ renpy.register_sfont('new_sfont', 22,
                           filename="new_sfont.png",
                           spacewidth=6)

    # Declare a character that uses the sfont.
    $ esfont = Character(_("Eileen"),
                         color="#c8ffc8",
                         what_font="new_sfont")

    # Slow text.
    $ eslow = Character(_("Eileen"),
                        color="#c8ffc8",
                        what_slow_cps=20)

    # Outlined text.
    $ eoutline = Character(_("Eileen"),
                           color="#c8ffc8",
                           what_outlines=[ (1, "#282") ])

    # Use it in subtitle mode.
    $ esubtitle = Character(None,
                            what_size=28,
                            what_outlines=[(3, "#0008", 2, 2), (3, "#282", 0, 0)],
                            what_layout="subtitle",
                            what_xalign=0.5,
                            what_text_align=0.5,
                            window_background=None,
                            window_yminimum=0,
                            window_xfill=False,
                            window_xalign=0.5)


    # This is used to show the defintion text, by the hyperlink demostration
    # code.
    $ definition = Character(None,
                             window_yfill=True,
                             window_xmargin=20,
                             window_ymargin=30)


    # The pink style, which we use as a custom text tag.
    $ style.pink = Style(style.default)
    $ style.pink.color = "#ffc0c0"

init python:
    style.ruby_style = Style(style.default)
    style.ruby_style.yoffset = -20
    style.ruby_style.size = 12

define eruby = Character(
    _("Eileen"),
    color="#c8ffc8",
    what_ruby_style=style.ruby_style,
    what_line_leading=10)



label demo_text:

    e "Ren'Py gives you quite a bit of control over how text appears."

    e "Text tags let us control the appearance of text that is shown to the user."

    e "Text tags can make text {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."

    e "They can make the font size {size=+12}bigger{/size} or {size=-8}smaller{/size}."

    e "They let you pause{w} the display of the text, optionally with{p}line breaks."

    e "They let you include images inside text{image=exclamation.png} Neat{image=exclamation.png}"

    e "We can pause the text for a short time, and have it auto-advance.{w=1} Just like that."

    eslow "We can even have the text auto-advance,{nw}"

    with flashbulb
    extend " when we reach the end of a block of text, in slow text mode."

    e "They can change the {color=#f00}color{/color} {color=#ff0}of{/color} {color=#0f0}the{/color} {color=#0ff}text{/color}."

    # e "There are also bold, italic, strikethrough, and underline style properties, which can be styled onto any text."

    e "The kerning tag lets you adjust the spacing between characters.\n{k=.5}The spacing between characters can be increased.{/k}\n{k=-.5}The spacing between characters can be decreased.{/k}"

    eruby "You are able to write ruby text, which can help clarify how to pronounce words, like {rb}Ren'Py{/rb}{rt}ren-pie{/rt}."

    e "{a=define_hyperlink}Hyperlinks{/a} let buttons be defined using text tags."

    e "The space and vspace tags add {space=30} horizontal and {vspace=20}vertical space, respectively."

    e "You can define your own text tags, {=pink}that use a style you define.{/=pink}"

    e "If you find yourself using text tags on every line, you should probably look at style properties instead."

    e "Used with care, text tags can enhance {b}your{/b} game."

    e "{u}Used{/u} with {i}abandon,{/i} they {b}can{/b} make {b}your{/b} game {color=#333}hard{/color} {color=#888}to{/color} {color=#ccc}read{/color}."

    e "With great power comes great responsibility, after all."

    e "And we want to give you all the power you need."

    e "There are a couple of text adjustments that don't correspond to text tags."

    eoutline "The outlines setting lets you put outlines around the text."

    eoutline "You can have more than one outline, and each has its own color and offset."

    window hide

    esubtitle "Here, we have two outlines around the white text."

    esubtitle "The bottom one is a translucent black that's offset a little, while the top one is green."

    esubtitle "By hiding the window and adjusting the layout method, we are able to create reasonable subtitles."

    esubtitle "This might be an interesting look for a game."

    window show

    esfont "For even more control, Ren'Py supports SFonts, image files containing font information."

    esfont "SFonts let you use fonts you otherwise couldn't, and apply special effects to fonts using your favorite image editor."

    e "Well, that's it for fonts and text tags."


    return


label define_hyperlink:

    definition "A hyperlink is a button that is defined inside text, using text tags. They're ideal for including definitions of words used in the script, but they shouldn't be used in place of menus."

    return
