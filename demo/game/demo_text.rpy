# This file demonstrates some of the text-layout and handling
# capabilities of Ren'Py.

init:
    python:

        # This imports in the asfont22 module, which contains a list of
        # kerning pairs.
        import asfont22

        # Register the sfont contained in asfont22 as "subfont".
        renpy.register_sfont('subfont', 22,
                             filename="asfont22.png",
                             kerns=asfont22.kerns,
                             spacewidth=4)

    # Declare some characters that speak in the subfont.

    # Just use the subfont.
    $ esub = Character("Eileen",
                       color="#c8ffc8",
                       what_font="subfont",
                       what_black_color="#282")

    # Use it in subtitle mode.
    $ esubtitle = Character(None,
                            what_font="subfont",
                            what_black_color="#282",
                            what_layout="subtitle",
                            what_xalign=0.5,
                            what_text_align=0.5,
                            window_background=None,
                            window_yminimum=0,
                            show_say_vbox_properties=dict(xalign=0.5))

    $ definition = Character(None,
                             window_yfill=True,
                             window_xmargin=20,
                             window_ymargin=30)
    
label demo_text:

    e "Ren'Py gives you quite a bit of control over how text appears."

    e "Text tags let us control the appearance of text that is shown to the user."

    e "Text tags can make text {b}bold{/b}, {i}italic{/i}, or {u}underlined{/u}."

    e "They can make the font size {size=+12}bigger{/size} or {size=-8}smaller{/size}."

    e "They let you pause{w} the display of the text, optionally with{p}line breaks."

    e "They let you include images inside text{image=exclamation.png} Neat {image=exclamation.png}"

    e "They can even change the {color=#f00}color{/color} {color=#ff0}of{/color} {color=#0f0}the{/color} {color=#0ff}text{/color}."

    e "There are also bold, italic, and underline style properties, which can be styled onto any text."

    e "{a=define_hyperlink}Hyperlinks{/a} let buttons be defined using text tags."

    e "If you find yourself using text tags on every line, you should probably look at style properties instead."

    e "Used with care, text tags can enhance {b}your{/b} game."

    e "{u}Used{/u} with {i}abandon,{/i} they {b}can{/b} make {b}your{/b} game {color=#333}hard{/color} {color=#888}to{/color} {color=#ccc}read{/color}."

    e "With great power comes great responsibility, after all."

    e "And we want to give you all the power you need."

    esub "For even more control, Ren'Py supports SFonts, image files containing font information."
    
    esub "SFonts let you use fonts you otherwise couldn't, and apply special effects to fonts... like I'm doing now, applying an outline to the font."

    esubtitle "Finally, you can adjust the line breaking algorithm. The subtitle line-breaking algorithm tries to make lines even in length."

    esubtitle "Along with sfonts and the ability to change the text window, this lets us render reasonable subtitles."

    e "Well, that's it for fonts and text tags."


    return

        
label define_hyperlink:

    definition "A hyperlink is a button that is defined inside text, using text tags. They're ideal for including definitions of words used in the script, but they shouldn't be used in place of menus."

    return
