label screen_displayables:

    e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."

label screen_displayables_menu:

    $ reset_example()

    menu:

        e "What would you like to know about?"

        "Common properties all displayables share.":
            call screen_displayable_properties

        "Adding images and other displayables.":
            call add_displayable

        "Text.":
            call text_displayable

        "Boxes and other layouts.":
            call layout_displayables

        "Windows and frames.":
            call window_displayables

        "Buttons":
            call button_displayables

        "That's all for now.":
            return

    jump screen_displayables_menu



label screen_displayable_properties:

    e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."

    example large:
        screen pos_example():
            frame:
                xalign 0.5 ypos 50
                text _("This uses position properties.")

    e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."

    example:
        screen at_example():
            frame:
                xalign 0.5 ypos 50
                text _("And the world turned upside down..."):
                    at rotated

        transform rotated:
            rotate 180 rotate_pad False

    e "The at transform applies a transform to the displayable, the same way the at clause in the show statement does."

    e "The at clause can be used for all sorts of purposes. It can animate and transform the displayable. Here, we're rotating the text upside down."


#     example large:
#         screen event_example():
#             frame:
#                 at inout
#                 xalign 0.5 ypos 50
#                 text _("This is an event.") at textform
#
#
#         transform inout:
#             on show:
#                 zoom 1.5 alpha 0.0
#                 linear .5 zoom 1.0 alpha 1.0
#
#             on hide:
#                 linear .5 zoom 1.5 alpha 0.0

#
#     example:
#         screen default_example():
#             frame:
#                 xalign 0.5 ypos 50
#
#                 vbox:
#
#                     textbutton "Choice 1" action Return(1)
#                     textbutton "Choice 2" action Return(1) default True
#                     textbutton "Choice 3" action Return(1)


    hide screen at_example
    with dissolve

    show example say_screen

    e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."

    e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."

    example:
        screen style_example():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text _("Flight pressure in tanks.") style "green_text"
                    text _("On internal power.")
                    text _("Launch enabled.")
                    text _("Liftoff!")

    style green_text:
        color "#c8ffc8"

    e "The style property lets you specify the style of a single displayable."

    example:
        screen style_prefix_example():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    vbox:
                        style_prefix "green"
                        text _("Flight pressure in tanks.")
                        text _("On internal power.")

                    vbox:
                        style_prefix "yellow"
                        text _("Launch enabled.")
                        text _("Liftoff!")

    style yellow_text:
        color "#ffffc8"


    e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."

    e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."

    hide example

    e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."

    return

label add_displayable:

    e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."

    example large:

        screen add_image_example():
            frame:
                xalign 0.5 ypos 50
                add "logo base"

    e "This can be done using the add statement, which adds an image or other displayable to the screen."

    e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."

    example large:

        screen add_filename_example():
            frame:
                xalign 0.5 ypos 50
                add "images/logo base.png"

    e "An image can also be referred to by it's filename, relative to the game directory."

    example large:

        screen add_displayable_example():
            frame:
                xalign 0.5 ypos 50
                add Solid("#0000ff", xsize=234, ysize=360)

    e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."


    example large:

        screen add_transform_example():
            frame:
                xalign 0.5 ypos 50
                add "logo base" zoom 0.7 rotate 43.21

    e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."

    example:

        screen add_at_transform_example():
            frame:
                xalign 0.5 ypos 50
                add "logo base" at unrotate

        transform unrotate:
            zoom 0.7 rotate 43.21
            linear 1.0 rotate 0
    e "Of course, the add statement can also take the at property, letting you give it a more complex transform."

    hide example

    return

label text_displayable:

    example large:
        screen text_example():
            frame:
                xalign 0.5 ypos 50
                text _("This is a text displayable."):
                    size 30

    e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."

    e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."

    example large:
        screen text_interpolation_example():
            $ answer = 42

            frame:
                xalign 0.5 ypos 50
                text _("The answer is [answer].")

    e "The text displayable can also interpolate values enclosed in square brackets"

    e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it. Those variables may be parameters, defined with the default or python statements, or set using the SetScreenVariable action."

    example large:
        screen text_tax_example():
            frame:
                xalign 0.5 ypos 50
                text _("Text tags {color=#c8ffc8}work{/color} in screens.")


    e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."

    hide example
    return


label layout_displayables:

    e "The layout displayables take other displayables and lay them out on the screen."

    example large:
        screen hbox_example():
            frame:
                xalign 0.5 ypos 50
                hbox:
                    spacing 10
                    text "1"
                    text "2"
                    text "3"
                    text "4"
                    text "5"

    e "For example, the hbox displayable takes its children and lays them out horizontally."

    example:
        screen vbox_example():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    spacing 10
                    text "1"
                    text "2"
                    text "3"
                    text "4"
                    text "5"


    e "The vbox displayable is similar, except it takes its children and arranges them vertically."

    e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."

    example:
        screen grid_example():
            frame:
                xalign 0.5 ypos 50
                grid 3 2:
                    spacing 10
                    text "1"
                    text "2"
                    text "3"
                    text "4"
                    text "5"
                    null

    e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."

    e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."

    e "Like the boxes, grid uses the spacing property to specify the space between cells."

    example:
        screen grid_transpose_example():
            frame:
                xalign 0.5 ypos 50
                grid 3 2:
                    spacing 10
                    transpose True
                    text "1"
                    text "2"
                    text "3"
                    text "4"
                    text "5"
                    null

    e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."


    example:
        screen grid_bigger_example():
            frame:
                xalign 0.5 ypos 50
                grid 3 2:
                    spacing 10
                    transpose True
                    text "1"
                    text "2"
                    text "3"
                    text "4"
                    text "5"
                    text _("Bigger")

    e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."


    example:
        screen fixed_example():
            frame:
                xalign 0.5 ypos 50
                fixed:
                    xsize 400 ysize 300
                    text "1" xpos 41 ypos 184
                    text "2" xpos 135 ypos 177
                    text "3" xpos 92 ypos 3
                    text "4" xpos 359 ypos 184
                    text "5" xpos 151 ypos 25

    e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."

    e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."

    example:
        screen implicit_fixed_example():
            frame:
                xalign 0.5 ypos 50
                xsize 440 ysize 316

                text "1" xpos 41 ypos 184
                text "2" xpos 135 ypos 177
                text "3" xpos 92 ypos 3
                text "4" xpos 359 ypos 184
                text "5" xpos 151 ypos 25

    e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."

    example large:
        screen hbox_example():
            frame:
                xalign 0.5 ypos 50

                has hbox spacing 10

                text "1"
                text "2"
                text "3"
                text "4"
                text "5"

    e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."

    e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."

    hide example

    return


label window_displayables:

    e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."

    example large:
        screen noframe_example():
            vbox:
                xalign 0.5 ypos 50
                text "This is a screen."
                textbutton "Okay":
                    action Return(True)

    e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."

    example large:
        screen frame_example():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text "This is a screen."
                    textbutton "Okay":
                        action Return(True)


    e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."

    e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."

    show example say_screen

    e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."

    e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."

    hide example
    return


label button_displayables:

    e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."

    example large:
        screen button_example():
            frame:
                xalign 0.5 ypos 50
                button:
                    action Notify(_("You clicked the button."))
                    text _("Click me.") style "button_text"

    e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."

    e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."

    example large:
        screen button_hover_example():
            frame:
                xalign 0.5 ypos 50
                button:
                    action Notify(_("You clicked the button."))
                    hovered Notify(_("You hovered the button."))
                    unhovered Notify(_("You unhovered the button."))
                    text _("Click me.") style "button_text"


    e "It's also possible to run actions when a button gains and loses focus."

    example large:
        screen button_heal_example():
            default health = 42

            frame:
                xalign 0.5 ypos 50
                button:
                    action SetScreenVariable("health", 100)
                    hbox:
                        spacing 10
                        text _("Heal") style "button_text" yalign 0.5
                        bar value AnimatedValue(health, 100, 1.0) yalign 0.5 xsize 200

    e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."

    example large:
        screen textbutton_example():
            frame:
                xalign 0.5 ypos 50
                textbutton _("This is a textbutton."):
                    action Notify(_("You clicked the button."))


    e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."

    e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."


    example large:
        screen imagebutton_example():
            frame:
                xalign 0.5 ypos 50
                imagebutton:
                    idle "logo bw"
                    hover "logo base"

                    action Notify(_("You clicked the button."))

    e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."

    e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."


    example large:
        screen button_inline_style_example():
            frame:
                xalign 0.5 ypos 50
                textbutton _("Click me."):
                    idle_background Frame("button glossy idle", 12, 12)
                    hover_background Frame("button glossy hover", 12, 12)
                    xpadding 20
                    ypadding 10
                    xmargin 5
                    ymargin 5

                    hover_sound "pong_beep.opus"

                    text_idle_color "#c0c0c0"
                    text_hover_color "#ffffff"

                    action Notify(_("You clicked the button."))

    e "Buttons take Window window properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."

    e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."

    e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."

    example large:
        screen button_style_example():
            frame:
                xalign 0.5 ypos 50

                has vbox

                textbutton _("Click me."):
                    style "custom_button"
                    action Notify(_("You clicked the button."))

                textbutton _("Or me."):
                    style "custom_button"
                    action Notify(_("You clicked the other button."))

        style custom_button:
            idle_background Frame("button glossy idle", 12, 12)
            hover_background Frame("button glossy hover", 12, 12)
            xpadding 20
            ypadding 10
            xmargin 5
            ymargin 5
            size_group "custom_button"

            hover_sound "pong_beep.opus"

        style custom_button_text:
            idle_color "#c0c0c0"
            hover_color "#ffffff"

    e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."

    hide example
    return

    return

