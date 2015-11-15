# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file is responsible for creating and defining the default styles
# used by the system.

init -1800 python:

    # The style hierarchy root has to be initialized through python
    # code.
    style.default = Style(None)

    # Fix up some styles originally defined in _errorhandling.rpym.
    style.image = Style(style.default)
    style.fixed = Style(style.default)

init -1800:

    # Declare styles and inheritance.

    style text is default
    style fixed is default
    style hbox is default
    style vbox is default
    style grid is default
    style side is default
    style window is default
    style image_placement is default
    style image is default
    style animation is default

    style say_label is default
    style say_dialogue is default
    style say_thought is default
    style say_window is window
    style say_who_window is window
    style say_two_window_vbox is vbox
    style say_vbox is vbox

    style menu is default
    style menu_caption is default
    style menu_choice is default
    style menu_choice_button is default
    style menu_choice_chosen is menu_choice
    style menu_choice_chosen_button is menu_choice_button
    style menu_window is window

    style input is default
    style input_text is input
    style input_prompt is default
    style input_window is window

    style centered_window is default
    style centered_text is default
    style centered_vtext is default

    style imagemap is image_placement
    style hotspot is default
    style imagemap_button is hotspot
    style hotbar is default

    style image_button is default
    style image_button_image is default

    style hyperlink is default
    style hyperlink_text is default
    style ruby_text is default

    style viewport is default
    style drag is default

    style motion is default
    style transform is motion

    style tile is default

    # Not used - kept for compatibility.
    style error_root is default

    style frame is default
    style menu_frame is frame

    style button is default
    style button_text is default

    style small_button is button
    style small_button_text is button_text

    style radio_button is button
    style radio_button_text is button_text

    style check_button is button
    style check_button_text is button_text

    style large_button is default
    style large_button_text is default

    style label is default
    style label_text is default

    style prompt is default
    style prompt_text is default

    style bar is default
    style vbar is default
    style slider is default
    style vslider is default
    style scrollbar is default
    style vscrollbar is default

    style mm_root is default
    style gm_root is default

    # Default style.

    style default:

        # Text properties
        font "DejaVuSans.ttf"
        language "unicode"
        antialias True
        size 22
        color (255, 255, 255, 255)
        black_color (0, 0, 0, 255)
        bold False
        italic False
        underline False
        strikethrough False
        kerning 0.0
        drop_shadow None
        drop_shadow_color (0, 0, 0, 255)
        outlines [ ]
        minwidth 0
        text_align 0
        justify False
        text_y_fudge 0
        first_indent 0
        rest_indent 0
        line_spacing 0
        line_leading 0
        line_overlap_split 0
        layout "tex"
        subtitle_width 0.9
        slow_cps None
        slow_cps_multiplier 1.0
        slow_abortable False
        ruby_style style.ruby_text
        # hyperlink_functions is set in 00defaults.rpy
        hinting "auto"
        adjust_spacing True

        # Window properties
        background None
        xpadding 0
        ypadding 0
        xmargin 0
        ymargin 0
        xfill False
        yfill False

        # Size properties
        xminimum 0
        yminimum 0
        xmaximum None
        ymaximum None

        # Position properties
        xpos None
        ypos None
        xanchor None
        yanchor None
        xoffset 0
        yoffset 0
        subpixel False

        # Sound properties
        activate_sound None
        hover_sound None

        # Box properties
        spacing 0
        first_spacing None
        box_layout None
        box_wrap False
        box_reverse False
        order_reverse False

        # Button properties
        focus_mask None
        focus_rect None
        keyboard_focus True

        # Bar properties
        fore_bar Null()
        aft_bar Null()
        thumb None
        thumb_shadow None
        left_gutter 0
        right_gutter 0
        thumb_offset 0
        unscrollable None
        bar_invert False
        bar_resizing False
        bar_vertical False

        # Viewport properties
        clipping False

    # Boxes

    style hbox:
        box_layout 'horizontal'

    style vbox:
        box_layout 'vertical'

    # Motions, zooms, rotozooms, and transforms

    style motion:
        xanchor 0
        yanchor 0
        xpos 0
        ypos 0

    style transform:
        subpixel True

    # Windows

    style window:
        background Solid((0, 0, 0, 192))
        xpadding 6
        ypadding 6
        xmargin 0
        ymargin 0
        xfill True
        yfill False
        yminimum 150
        xalign 0.5
        yalign 1.0

    # Dialogue
    style say_label:
        bold True

    style say_vbox:
        spacing 8

    style say_who_window:
        xminimum 200
        yminimum 34
        xfill False
        xalign 0

    style say_two_window_vbox:
        yalign 1.0

    # Menus

    style menu_choice:
        idle_color "#0ff"
        hover_color "#ff0"

    # Input

    style input:
        color "#ff0"
        adjust_spacing False

    # Centered text and dialogue

    style centered_window:
        xalign 0.5
        xfill False
        yalign 0.5
        yfill False
        xpadding 10

    style centered_text:
        textalign 0.5
        xalign 0.5
        yalign 0.5
        layout "subtitle"

    style centered_vtext:
        textalign 0.5
        xalign 0.5
        yalign 0.5
        vertical True

    # Hyperlinks

    style hyperlink_text:
        underline True
        hover_color "#0ff"
        idle_color "#08f"

    # Ruby text (Furigana)

    style ruby_text:
        size 22
        xoffset 0

    # Bars

    style vbar:
        bar_vertical True

    style vslider:
        bar_vertical True

    style vscrollbar:
        bar_vertical True
        bar_invert True

    style viewport:
        clipping True
        xfill True
        yfill True

    style drag:
        focus_mask True

    # Out-of-game menu root windows

    style mm_root:
        background "#000"
        xfill True
        yfill True

    style gm_root:
        background "#000"
        xfill True
        yfill True

    # Tiles

    style tile:
        clipping True

    # Labels
    style pref_label:
        alt "" # We expect the labelled buttons/bars to read themselves out.
