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

    e "In addition ot the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."

    example:

        screen add_at_transform_example():
            frame:
                xalign 0.5 ypos 50
                add "logo base" at unrotate

        transform unrotate:
            zoom 0.7 rotate 43.21
            linear 1.0 rotate 0
    e "Of course, the add statment can also take the at property, letting you give it a more complex transform."

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
