
transform example:
    xalign 0.5
    yalign 0.25


screen style0():

    frame:
        at example

        xpadding 20
        ypadding 20

        vbox:

            spacing 10

            textbutton _("Button 1") action Return(True)

            textbutton _("Button 2"):
                style "empty"
                text_style "empty"

                xminimum 240
                ypadding 2

                background RoundRect("#003c78")
                hover_background RoundRect("#0050a0")

                text_color "#c8ffff"
                text_xalign 0.5

                action Return(True)



label new_gui:

    e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."

    e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."

    e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."

    e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."

    e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."

    e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."

    return

label styles:

    show eileen happy at left

    e "Ren'Py has a powerful style system that controls what displayables look like."

    e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."

    menu styles_menu:

        e "What would you like to know about styles?"

        "Style basics.":
            call style_basics

        "General style properties.":
            call style_general

        "Text style properties.":
            call style_text

        "That's all I want to know.":
            return

    jump styles_menu

label style_basics:

    e "Styles let a displayable look different from game to game, or even inside the same game."

    show screen style0
    with dissolve

    e "For example, both of these are Buttons that use the style displayable. And yet, they look quite different from each other."

    hide screen style0
    with dissolve

    e "Styles are a combination of information from three different places."

    example small:
        screen style1:
            text _("This text is colored green."):
                at example
                color "#c0ffc0"

    show screen style1
    with dissolve

    e "The first is is as part of a screen. Each displayable defined in a screen takes style properties."

    example small:
        image style2 = Text(_("This text is colored red."), color="#ffc0c0")


    hide screen style1
    show style2 at example

    e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."


    example small:
        style blue_text:
            color "#c0c0ff"

        image style3 = Text(_("This text is colored blue."), style="blue_text")

    hide style2
    show style3 at example

    e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."

    hide style3
    hide example
    with dissolve

    e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."

    e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."

    e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."

    example small:
        style blue_text is text:
            color "#c0c0ff"

    e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."

    hide example

    e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."

    e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."

    e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."

    e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."

    e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."

    e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."

    example small:
        style example_button_text:
            idle_color "#c0c0c0"
            hover_color "#ffffff"
            insensitive_color "#303030"
            selected_idle_color "#e0e080"
            selected_hover_color "#ffffc0"

        screen style4():

            default result = 1

            frame:
                style_prefix "example"
                xpadding 20
                ypadding 20

                at example
                vbox:
                    textbutton "Button 1" action SetScreenVariable("result", 1)
                    textbutton "Button 2" action SetScreenVariable("result", 2)
                    textbutton "Button 3" action None

    show screen style4
    with dissolve

    e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."

    hide screen style4
    with dissolve

    hide example

    e "If you ever need to know what style a displayable uses, you can hover the mouse over it and hit shift+I, as in India."

    e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."

    return


screen general(style):
    frame:
        style style
        text _("The road to the stars is steep and dangerous. But we are not afraid.\n–Yuri Gagarin")


label style_general:

    e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."

    example small:

        style general is frame:
            xalign 0.5
            yalign 0.2

    show screen general("general")
    with dissolve

    e "Every displayable takes the positon properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."


    example small:
        style minmax_general:
            xmaximum 400
            yminimum 200

    show screen general("minmax_general")
    with dissolve

    e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."

    e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."

    e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."


    example small:
        style xysize_general:
            xsize 400
            ysize 200

    show screen general("xysize_general")

    e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."

    e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."

    example small:
        style area_general:
            area (600, 20, 400, 200)

    show screen general("area_general")

    e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."

    example small:
        style fill_general:
            xfill True

    show screen general("fill_general")

    e "The xfill and yfill properties make a displayable expand to fill available space in the horizontal and vertical directions."


    example small:
        style alt_general:
            alt _("\"The road to the stars is steep and dangerous. But we are not afraid.\" Said by Yuri Gagarin.")

    show screen general("alt_general")


    e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."

    hide screen general
    hide example
    with dissolve

    return

screen text(style, vertical=False):
    frame:
        xalign 0.5
        yalign 0.2

        if vertical:
            right_padding 30
            bottom_padding 30
            text _("Vertical") style style
        else:
            xsize 400
            text _("The road to the stars is steep and dangerous. But we are not afraid.\n\nYuri Gagarin"):
                style style



label style_text:

    e "The text style properties apply to text and input displayables."

    e "Text displayables can be create implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."

    e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."

    example small:
        style bold_text:
            bold True

    show screen text("bold_text")

    e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."

    example small:
        style color_text:
            color "#c0ffc0"

    show screen text("color_text")

    e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."

    example small:
        style first_indent_text:
            first_indent 40

    show screen text("first_indent_text")

    e "The first_indent style property determines how far the first line is indented."

    example small:
        style font_text:
            font "DejaVuSans-Bold.ttf"

    show screen text("font_text")

    e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."

    example small:
        style size_text:
            size 28

    show screen text("size_text")

    e "The size property changes the size of the text."


    example small:
        style italic_text:
            italic True

    show screen text("italic_text")

    e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."


    example small:
        style justify_text:
            justify True

    show screen text("justify_text")

    e "The justify property makes the text justified, lining all but the last line up on the left and the right side."

    example small:
        style kerning_text:
            kerning -0.5

    show screen text("kerning_text")

    e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."


    example small:
        style leading_spacing_text:
            line_leading 5
            line_spacing 7

    show screen text("leading_spacing_text")

    e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."


    example small:
        style outlines_text:
            outlines [ (1, "#408040", 0, 0) ]

    show screen text("outlines_text")

    e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."

    e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."

    example small:
        style rest_indent_text:
            rest_indent 40

    show screen text("rest_indent_text")

    e "The rest_indent property controls the indentation of lines after the first one."


    example small:
        style center_text:
            text_align 0.5

    show screen text("center_text")

    e "The text align property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."

    e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the text_align and xalign to the same value."


    example small:
        style right_text:
            text_align 1.0
            yalign 1.0

    show screen text("right_text")

    e "When both text_align and xalign are set to 1.0, the text is properly right-justified."


    example small:
        style underline_text:
            underline True

    show screen text("underline_text")

    e "The underline property underlines the text."


    hide screen text
    hide example
    with dissolve

    e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."

    example small:
        style antialias_text:
            antialias False

    show screen text("antialias_text")

    e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."

    example small:
        style adjust_true_text:
            adjust_spacing True

    show screen text("adjust_true_text")

    e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When true, characters will be shifted a bit so the Text has the same relative spacing."


    example small:
        style adjust_true_text:
            adjust_spacing False

    show screen text("adjust_false_text")

    e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."


    example small:
        style layout_nobreak_text:
            layout "nobreak"

    show screen text("layout_nobreak_text")

    e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."


    example small:
        style layout_subtitle_text:
            layout "subtitle"
            xalign 0.5
            text_align 0.5

    show screen text("layout_subtitle_text")

    e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."

    example small:
        style strikethrough_text:
            strikethrough True

    show screen text("strikethrough_text")

    e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."


    example small:
        style vertical_text:
            vertical True
            size 18

    show screen text("vertical_text", True)

    e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."

    hide screen text
    hide example
    with dissolve

    e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."


    return








