
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


label styles:

    show eileen happy at left

    e "Ren'Py has a powerful style system that lets you control what displayables look like. The GUI framework gives sensible default, but the style system allows total customization."

    e "If you're creating your own GUI from scratch, or creating your own screens, you'll want to learn about styles to make your visual novel look great."

    menu styles_menu:

        e "What would you like to know about styles?"

        "Style basics.":
            call style_basics


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

    example:
        screen style1:
            text _("This text is colored green."):
                at example
                color "#c0ffc0"

    show screen style1
    with dissolve

    e "The first is is as part of a screen. Each displayable defined in a screen takes style properties."

    example:
        image style2 = Text(_("This text is colored red."), color="#ffc0c0")


    hide screen style1
    show style2 at example

    e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."


    example:
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




