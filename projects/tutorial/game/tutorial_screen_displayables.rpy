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

        "Buttons.":
            call button_displayables

        "Bars.":
            call bar_displayables

        "Viewports.":
            call viewport_displayables

        "Imagemaps.":
            call imagemap_displayables

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

    e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."


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

    e "The text displayable can also interpolate values enclosed in square brackets."

    e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."

    e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."

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
                text _("This is a screen.")
                textbutton _("Okay"):
                    action Return(True)

    e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."

    example large:
        screen frame_example():
            frame:
                xalign 0.5 ypos 50
                vbox:
                    text _("This is a screen.")
                    textbutton _("Okay"):
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

    e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."

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


label bar_displayables:

    example large:
        screen bar_example():
            frame:
                xalign 0.5 ypos 50
                xsize 500
                bar:
                    value StaticValue(66, 100)


    e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."

    e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."

    e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."

    e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."

    example large:
        screen bars_example():
            default n = 66

            frame:
                xalign 0.5 ypos 50
                xsize 500

                vbox:
                    spacing 10

                    bar value AnimatedValue(n, 100, 0.5) style "bar"
                    bar value ScreenVariableValue("n", 100) style "slider"
                    bar value ScreenVariableValue("n", 100) style "scrollbar"

    e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."

    e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."

    e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."

    e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."

    example large:
        screen vbars_example():
            default n = 66

            frame:
                xalign 0.5 ypos 50
                ysize 300

                hbox:
                    spacing 10

                    vbar value AnimatedValue(n, 100, 0.5)
                    vbar value ScreenVariableValue("n", 100) style "vslider"
                    vbar value ScreenVariableValue("n", 100) style "vscrollbar"

    e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."


    e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."

    hide example
    return



label imagemap_displayables:

    e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."

    window hide None

    example imagemap hide noshow:
        screen imagemap_example():
            imagemap:
                idle "imagemap ground"
                hover "imagemap hover"

                hotspot (44, 238, 93, 93) action Jump("swimming") alt "Swimming"
                hotspot (360, 62, 93, 93) action Jump("science") alt "Science"
                hotspot (726, 106, 93, 93) action Jump("art") alt "Art"
                hotspot (934, 461, 93, 93) action Jump("home") alt "Home"

        label imagemap_example:

            # Call the imagemap_example screen.
            call screen imagemap_example

        label swimming:

            e "You chose swimming."

            e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."

            jump imagemap_done

        label science:

            e "You chose science."

            e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."

            jump imagemap_done

        label art:
            e "You chose art."

            e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."

            jump imagemap_done

        label home:

            e "You chose to go home."

            jump imagemap_done

        label imagemap_done:

            e "Anyway..."

    window show None
    window auto

    e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."

    show imagemap volume idle:
        xalign 0.5 ypos 50
    with dissolve

    e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."

    show imagemap volume hover:
        xalign 0.5 ypos 50
    with dissolve

    e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."

    e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."

    show imagemap volume selected_idle:
        xalign 0.5 ypos 50
    with dissolve

    e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."

    show imagemap volume selected_hover:
        xalign 0.5 ypos 50
    with dissolve

    e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."

    show imagemap volume insensitive:
        xalign 0.5 ypos 50
    with dissolve

    e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."

    hide imagemap
    with dissolve

    e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."

    example large:
        screen volume_imagemap_example():
            imagemap:
                xalign 0.5 ypos 50
                idle "imagemap volume idle"
                hover "imagemap volume hover"
                selected_idle "imagemap volume selected_idle"
                selected_hover "imagemap volume selected_hover"
                insensitive "imagemap volume insensitive"

                hotspot (237, 171, 126, 50) action Return(True)
                hotbar (51, 96, 498, 52) value Preference("music volume")

    e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."

    example large:
        screen volume_imagemap_auto_example():
            imagemap:
                xalign 0.5 ypos 50
                auto "imagemap volume %s"

                hotspot (237, 171, 126, 50) action Return(True)
                hotbar (51, 96, 498, 52) value Preference("music volume")


    e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."

    e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."

    e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."

    e "Both take the coordinates of the area, in (x, y, width, height) format."

    e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."

    e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."


    hide screen volume_imagemap_auto_example
    show example imagemap
    with dissolve

    e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."

    e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."

    hide example

    e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."

    e "It's up to you and your team to decide if imagemaps are right for your project."

    return


label viewport_displayables:

    e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."

    example large:
        screen viewport_screen():

            viewport:
                xalign 0.5 ypos 50 xysize (700, 300)

                draggable True
                mousewheel True
                arrowkeys True

                add "bg band"

    with dissolve

    e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."

    e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."

    example large:
        screen edgescroll_viewport_screen():

            viewport:
                xalign 0.5 ypos 50 xysize (700, 300)

                edgescroll (150, 500)
                mousewheel True
                arrowkeys True

                add "bg band"


    e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."

    example large:
        screen scrollbar_viewport_screen():

            viewport:
                xalign 0.5 ypos 50 xysize (700, 300)

                scrollbars "both"
                spacing 5

                draggable True
                mousewheel True
                arrowkeys True

                add "bg band"

    with dissolve

    e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."

    e "The spacing property controls the space between the viewport and its scrollbars, in pixels."


    example large:
        screen initial_viewport_screen():

            viewport:
                xalign 0.5 ypos 50 xysize (700, 300)

                xinitial 0.5
                yinitial 1.0

                scrollbars "both"
                spacing 5

                draggable True
                mousewheel True
                arrowkeys True

                add "bg band"

    with dissolve

    e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."

    example large:
        screen nochild_size_viewport_screen():

            viewport:
                xalign 0.5 ypos 50 xysize (700, 300)

                scrollbars "horizontal"
                spacing 5

                draggable True
                mousewheel True
                arrowkeys True

                add "#000c"
                text _("This text is wider than the viewport.") size 40


    with dissolve

    e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."

    e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."

    example large:
        screen child_size_viewport_screen():

            viewport:
                xalign 0.5 ypos 50 xysize (700, 300)

                child_size (1000, None)

                scrollbars "horizontal"
                spacing 5

                draggable True
                mousewheel True
                arrowkeys True

                add "#000c"
                text _("This text is wider than the viewport.") size 40

    with dissolve

    e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."


    example large:
        screen vpgrid_screen():

            vpgrid:
                cols 6
                rows 4

                xalign 0.5 ypos 50 xysize (700, 300)

                child_size (1000, None)

                scrollbars "both"
                side_spacing 5

                draggable True
                mousewheel True
                arrowkeys True

                for i in range(6 * 4):
                    add "logo base"


    with dissolve

    e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."

    e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."


    hide example

    return
