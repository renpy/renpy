
transform examplepos:
    xalign 0.5
    ypos 50


screen style0():

    frame:
        at examplepos

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

label styles_menu:

    $ reset_example()

    menu:

        e "What would you like to know about styles?"

        "Style basics.":
            call style_basics

        "General style properties.":
            call style_general

        "Text style properties.":
            call style_text

        "Window and Button style properties.":
            call style_button

        "Bar style properties.":
            call style_bar

        "Box, Grid, and Fixed style properties.":
            call style_box

        "The Displayable Inspector.":
            call style_inspector

        "That's all I want to know.":
            return

    jump styles_menu

label style_basics:

    e "Styles let a displayable look different from game to game, or even inside the same game."

    show screen style0
    with dissolve

    e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."

    hide screen style0
    with dissolve

    e "Styles are a combination of information from four different places."

    example:
        screen style1():
            text _("This text is colored green."):
                style "my_text"
                color "#c0ffc0"

                at examplepos

    show screen style1
    with dissolve

    e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."

    example:
        screen textstyle():
            frame:
                textbutton _("Danger"):
                    text_color "#c04040"
                    text_hover_color "#ff0000"
                    action Return(True)

                at examplepos


    hide screen style1
    show screen textstyle
    with dissolve

    e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."


    example:
        image style2 = Text(_("This text is colored red."), color="#ffc0c0")


    show style2 at examplepos
    with dissolve
    hide screen textstyle
    with dissolve


    e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."

    hide style2
    with dissolve

    example:
        define egreen = Character("Eileen", who_color="#c8ffc8", who_bold=True, what_color="#c8ffc8")


    egreen "Style properties can also be given as arguments when defining a character."

    egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."

    egreen "Style properties that don't have a prefix are also applied to the character's name."

    example:
        style blue_text:
            color "#c0c0ff"

        image style3 = Text(_("This text is colored blue."), style="blue_text")

    show style3 at examplepos

    e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."

    hide style3
    hide example
    with dissolve

    e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."

    e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."

    e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."

    example:
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

    example:
        style styled_button_text:
            idle_color "#c0c0c0"
            hover_color "#ffffff"
            insensitive_color "#303030"
            selected_idle_color "#e0e080"
            selected_hover_color "#ffffc0"

        screen style4():

            default result = 1

            frame:
                style_prefix "styled"
                xpadding 20
                ypadding 20

                at examplepos

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

    e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."

    return


screen general(style):
    frame:
        style style
        text _("Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin")


label style_general:

    e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."

    example:

        style general is frame:
            xalign 0.5
            yalign 0.2

    show screen general("general")
    with dissolve

    e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."


    example:
        style minmax_general:
            xmaximum 400
            yminimum 200

    show screen general("minmax_general")
    with dissolve

    e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."

    e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."

    e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."


    example:
        style xysize_general:
            xsize 400
            ysize 200

    show screen general("xysize_general")

    e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."

    e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."

    example:
        style area_general:
            area (600, 20, 400, 200)

    show screen general("area_general")

    e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."

    example:
        style alt_general:
            alt _("\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin.")

    show screen general("alt_general")


    e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."

    hide screen general
    hide example
    with dissolve

    return

screen text(style, vertical=False):
    frame:
        xalign 0.5
        ypos 50

        if vertical:
            left_padding 20
            right_padding 35
            bottom_padding 35

            text _("Vertical") style style
        else:
            xsize 400
            text _("Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"):
                style style


label style_text:

    e "The text style properties apply to text and input displayables."

    e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."

    e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."

    example:
        style bold_text:
            bold True

    show screen text("bold_text")

    e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."

    example:
        style color_text:
            color "#c0ffc0"

    show screen text("color_text")

    e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."

    example:
        style first_indent_text:
            first_indent 40

    show screen text("first_indent_text")

    e "The first_indent style property determines how far the first line is indented."

    example:
        style font_text:
            font "DejaVuSans-Bold.ttf"

    show screen text("font_text")

    e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."

    example:
        style size_text:
            size 14

    show screen text("size_text")

    e "The size property changes the size of the text."


    example:
        style italic_text:
            italic True

    show screen text("italic_text")

    e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."


    example:
        style justify_text:
            justify True

    show screen text("justify_text")

    e "The justify property makes the text justified, lining all but the last line up on the left and the right side."

    example:
        style kerning_text:
            kerning -0.5

    show screen text("kerning_text")

    e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."


    example:
        style leading_spacing_text:
            line_leading 5
            line_spacing 7

    show screen text("leading_spacing_text")

    e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."


    example:
        style outlines_text:
            outlines [ (1, "#408040", 0, 0) ]

    show screen text("outlines_text")

    e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."

    e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."

    example:
        style rest_indent_text:
            rest_indent 40

    show screen text("rest_indent_text")

    e "The rest_indent property controls the indentation of lines after the first one."


    example:
        style center_text:
            text_align 0.5

    show screen text("center_text")

    e "The text_align property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."

    e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the text_align and xalign to the same value."


    example:
        style right_text:
            text_align 1.0
            yalign 1.0

    show screen text("right_text")

    e "When both text_align and xalign are set to 1.0, the text is properly right-justified."


    example:
        style underline_text:
            underline True

    show screen text("underline_text")

    e "The underline property underlines the text."


    hide screen text
    hide example
    with dissolve

    e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."

    example:
        style antialias_text:
            antialias False

    show screen text("antialias_text")

    e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."

    example:
        style adjust_true_text:
            adjust_spacing True

    show screen text("adjust_true_text")

    e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."


    example:
        style adjust_true_text:
            adjust_spacing False

    show screen text("adjust_false_text")

    e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."


    example:
        style layout_nobreak_text:
            layout "nobreak"

    show screen text("layout_nobreak_text")

    e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."


    example:
        style layout_subtitle_text:
            layout "subtitle"
            xalign 0.5
            text_align 0.5

    show screen text("layout_subtitle_text")

    e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."

    example:
        style strikethrough_text:
            strikethrough True

    show screen text("strikethrough_text")

    e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."


    example:
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




screen button(style):

    default selected = "top"

    frame:
        xalign 0.5
        ypos 50
        background "#0004"
        xsize 350

        has vbox:
            xalign 0.5

        textbutton _("Top Choice"):
            style style
            action SetScreenVariable("selected", "top")
            text_style "example_button_text"

        textbutton _("Bottom Choice"):
            style style
            action SetScreenVariable("selected", "bottom")
            text_style "example_button_text"


example example_button_text:
    style example_button_text:
        xalign 0.5
        color "#404040"
        hover_color "#4040c0"

label style_button:

    e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."

    e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."

    example example_button large:
        style example_button is default:
            idle_background Frame("idle_background.png", 10, 10, tile=True)
            hover_background Frame("hover_background.png", 10, 10, tile=True)
            xalign 0.5

    show screen button('example_button')
    with dissolve

    e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."

    e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."

    e "We also center the two buttons, using the xalign position property."

    show example example_button_text

    e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."

    example:
        style oddly_padded_button is example_button:
            left_padding 10
            right_padding 40
            top_padding 10
            bottom_padding 5

    show screen button('oddly_padded_button')

    e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."

    example:
        style padded_button is example_button:
            xpadding 40
            ypadding 10

    show screen button('padded_button')

    e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."

    example:
        style margin_button is padded_button:
            ymargin 10

    show screen button('margin_button')

    e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."


    example:
        style sized_button is margin_button:
            size_group "example"

    show screen button('sized_button')

    e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."


    example:
        style xfill_button is margin_button:
            xfill True

    show screen button('xfill_button')

    e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."


    example:
        style foreground_button is xfill_button:
            foreground "check_foreground.png"
            selected_foreground "check_selected_foreground.png"

    show screen button('foreground_button')

    e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."

    e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."

    example:
        style beep_button is foreground_button:
            hover_sound "pong_beep.opus"
            activate_sound "pong_boop.opus"

    show screen button('beep_button')

    e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."


    example:
        style focus_mask_button is beep_button:
            focus_mask True

    show screen button('focus_mask_button')

    e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."

    hide example
    hide screen button
    with dissolve

    return

screen bar(style):

    default measure = 42.0

    frame:
        xalign 0.5
        ypos 50
        ypadding 20

        has vbox:
            spacing 20

        bar:
            value ScreenVariableValue("measure", range=100.0)
            style style
            xsize 400


        text "[measure:.0f]/100":
            xalign 0.5


screen vbar(style):

    default measure = 42.0

    frame:
        xalign 0.5
        ypos 20
        ypadding 20
        xsize 140

        has vbox:
            spacing 20
            xfill True

        bar:
            value ScreenVariableValue("measure", range=100.0)
            style style
            ysize 250
            xalign 0.5

        text "[measure:.0f]/100":
            xalign 0.5
            text_align 0.5
            min_width 100


image bar empty idle vertical = Transform("bar empty idle", rotate=90, rotate_pad=False)
image bar empty hover vertical  = Transform("bar empty hover", rotate=90, rotate_pad=False)
image bar full idle vertical = Transform("bar full idle", rotate=90, rotate_pad=False)
image bar full hover vertical = Transform("bar full hover", rotate=90, rotate_pad=False)

style empty_only is default:
    left_bar Frame("bar empty idle.png", 4, 0)
    hover_left_bar Frame("bar empty hover.png", 4, 0)
    right_bar Frame("bar empty idle.png", 4, 0)
    hover_right_bar Frame("bar empty hover.png", 4, 0)
    ysize 30

style full_only is default:
    left_bar Frame("bar full idle.png", 4, 0)
    hover_left_bar Frame("bar full hover.png", 4, 0)
    right_bar Frame("bar full idle.png", 4, 0)
    hover_right_bar Frame("bar full hover.png", 4, 0)
    ysize 30

label style_bar:

    show screen bar("empty_only")
    with dissolve

    e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."

    show screen bar("full_only")

    e "And here's what we use for parts of the bar that are full."

    example large:
        style example_bar is default:
            left_bar Frame("bar full idle.png", 4, 0)
            hover_left_bar Frame("bar full hover.png", 4, 0)
            right_bar Frame("bar empty idle.png", 4, 0)
            hover_right_bar Frame("bar empty hover.png", 4, 0)
            ysize 30

    show screen bar('example_bar')

    e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."

    e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."

    e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."

    example:
        style invert_bar is default:
            bar_invert True
            left_bar Frame("bar empty idle.png", 4, 0)
            hover_left_bar Frame("bar empty hover.png", 4, 0)
            right_bar Frame("bar full idle.png", 4, 0)
            hover_right_bar Frame("bar full hover.png", 4, 0)
            ysize 30

    show screen bar('invert_bar')

    e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."

    example:
        style resizing_bar is default:
            bar_resizing True
            left_bar Frame("bar full idle.png", 4, 0)
            hover_left_bar Frame("bar full hover.png", 4, 0)
            right_bar Frame("bar empty idle.png", 4, 0)
            hover_right_bar Frame("bar empty hover.png", 4, 0)
            ysize 30


    show screen bar('resizing_bar')

    e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."

    example:

        style thumb_bar is default:
            thumb "bar thumb idle.png"
            hover_thumb "bar thumb hover.png"
            base_bar Frame("bar empty idle.png", 4, 0)
            hover_base_bar Frame("bar empty hover.png", 4, 0)
            ysize 30

    show screen bar('thumb_bar')

    e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."

    e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."

    example:

        style gutter_bar is default:
            left_gutter 4
            right_gutter 4
            thumb "bar thumb idle.png"
            hover_thumb "bar thumb hover.png"
            base_bar Frame("bar empty idle.png", 4, 0)
            hover_base_bar Frame("bar empty hover.png", 4, 0)
            ysize 30

    show screen bar('gutter_bar')

    e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."

    example:
        style vertical_bar is default:
            bar_vertical True
            top_bar Frame("bar empty idle vertical", 4, 0)
            hover_top_bar Frame("bar empty hover vertical", 4, 0)
            bottom_bar Frame("bar full idle vertical", 4, 0)
            hover_bottom_bar Frame("bar full hover vertical", 4, 0)
            xsize 30

    hide screen bar
    show screen vbar('vertical_bar')
    with dissolve

    e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."

    hide screen vbar
    with dissolve

    e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."

    e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."

    hide example

    e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."

    return

screen hbox(style, wide, highlight="#fff2"):
    frame:
        xalign 0.5
        ypos 50
        ypadding 20
        xsize 500

        frame:
            style "empty"
            background highlight

            hbox:
                style style
                text _("First Child") color "#ffe0e0"
                text _("Second Child") color "#e0ffe0"
                text _("Third Child") color "#e0e0ff"

                if wide:
                    text _("Fourth Child") color "#ffffe0"
                    text _("Fifth Child") color "#e0ffff"
                    text _("Sixth Child") color "#ffe0ff"


screen vbox(style, highlight="#fff2"):

    frame:
        xalign 0.5
        ypos 50
        ypadding 20
        xsize 500

        frame:
            style "empty"
            background highlight

            vbox:
                style style
                text _("First Child") xalign 0.5 color "#ffe0e0"
                text _("Second Child") xalign 0.5 color "#e0ffe0"
                text _("Third Child") xalign 0.5 color "#e0e0ff"


screen grid(style):

    frame:
        xalign 0.5
        ypos 50
        ypadding 20

        grid 3 2:
            style style

            text _("First Child") color "#ffe0e0"
            text _("Second Child") color "#e0ffe0"
            text _("Third Child") color "#e0e0ff"

            text _("Fourth Child") color "#ffffe0"
            text _("Fifth Child") color "#e0ffff"
            text _("Sixth Child") color "#ffe0ff"


screen fixed(style):

    frame:
        xalign 0.5
        ypos 50
        ypadding 20
        xsize 500
        ysize 400

        frame:
            style "empty"
            background "#fff2"

            fixed:
                style style

                add Transform("logo base", zoom=.9):
                    xpos 10
                    ypos 10

                text "Ren'Py":
                    font "DejaVuSans.ttf"
                    xpos 150
                    ypos 220
                    size 80
                    outlines [ (2, "#333", 0, 0) ]



label style_box:

    show screen hbox('hbox', False, None)
    with dissolve

    e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."

    hide screen hbox
    show screen vbox('vbox', None)
    with dissolve

    e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."

    show screen vbox('vbox')
    with dissolve

    e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."

    example:
        style fill_vbox:
            xfill True

    show screen vbox('fill_vbox')

    e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."


    example:
        style spacing_vbox:
            spacing 10
            xfill True

    show screen vbox('spacing_vbox')

    e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."


    example:
        style first_spacing_vbox is vbox:
            first_spacing 10
            xfill True

    show screen vbox('first_spacing_vbox')

    e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."


    example:
        style reverse_vbox:
            box_reverse True
            xfill True

    show screen vbox('reverse_vbox')

    e "The box_reverse style property reverses the order of entries in the box."



    example:
        style spacing_hbox:
            spacing 20
            xfill True

    hide screen vbox
    show screen hbox("spacing_hbox", False)
    with dissolve

    e "We'll switch back to a horizontal box for our next example."

    example:
        style wrap_hbox:
            box_wrap True
            spacing 5
            xfill True

    show screen hbox("wrap_hbox", True)

    e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."

    hide screen hbox
    show screen grid('spacing_grid')
    with dissolve


    example:
        style spacing_grid:
            xspacing 20
            yspacing 50


    e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."

    hide example
    hide screen grid
    show screen fixed('fixed')
    with dissolve

    e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."

    e "But of course, we have some style properties that can change that."

    example:
        style fit_fixed:
            xfit True
            yfit True

    show screen fixed('fit_fixed')

    e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."

    example:
        style reverse_fixed:
            order_reverse True

    show screen fixed('reverse_fixed')

    e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."


    hide screen fixed
    hide example
    with dissolve

    return


label style_inspector:

    e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."

    e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."

    e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."

    e "You can click on the name of the style to see where it gets its properties from."

    e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."

    e "You can try the inspector right now, by hovering this text and hitting shift+I."

    return


