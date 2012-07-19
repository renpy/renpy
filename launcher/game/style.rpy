# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:
    INDENT = 20
    HALF_INDENT = 10

    SCROLLBAR_SIZE = 16

    SEPARATOR = Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=1.0)
    SEPARATOR2 = Frame("pattern.png", 0, 0, tile=True, ymaximum=10, yalign=1.0)

    SPACER_HEIGHT = 12
    SPACER = Null(height=SPACER_HEIGHT)

    HALF_SPACER_HEIGHT = 6
    HALF_SPACER = Null(height=HALF_SPACER_HEIGHT)

    # Colors.
    TEXT = "#545454"
    IDLE = "#42637b"
    LIGHT_IDLE = "#78a5c5"
    SCROLLBAR_IDLE = "#dfdfdf"
    HOVER = "#d86b45"
    WHITE = "#ffffff"
    DISABLED = "#808080"
    DANGER = "#d15353"
    
    # FONTS/WEIGHTS
    LIGHT = "Roboto-Light.ttf"
    REGULAR = "Roboto-Regular.ttf"
    DARK = "Roboto-Medium.ttf"
    
    # DIVIDING THE SCREEN
    ONETHIRD = 258
    TWOTHIRDS = 496
    ONEHALF = 377

    
    # Default style.
    style.l_default = Style(style.default)
    style.l_default.font = LIGHT
    style.l_default.color = TEXT
    style.l_default.idle_color = IDLE
    style.l_default.hover_color = HOVER
    style.l_default.size = 18
    
    style.l_text = Style(style.l_default)

    style.l_button = Style(style.l_default)
    style.l_button_text = Style(style.l_default)
    style.l_button_text.insensitive_color = DISABLED
    style.l_button_text.selected_font = REGULAR

    # A small button, used at the bottom of the screen.
    style.l_link = Style(style.l_default)
    style.l_link_text = Style(style.l_default)
    style.l_link_text.size = 14
    style.l_link_text.font = LIGHT

    # Action buttons on the bottom of the screen.
    style.l_right_button = Style(style.l_default)
    style.l_right_button.xalign = 1.0
    style.l_right_button.ypos = 600 - 128 + 12
    style.l_right_button.left_margin = 8 + INDENT
    style.l_right_button.right_margin = 10 + INDENT
    style.l_right_button_text = Style(style.l_default)
    style.l_right_button_text.size = 30

    style.l_left_button = Style(style.l_right_button)
    style.l_left_button.xalign = 0.0
    style.l_left_button_text = Style(style.l_right_button_text)
    
    
    # The root frame. This contains everything but the bottom navigation, back
    # button, and tooltip button.
    style.l_root = Style(style.l_default)
    style.l_root.background = "background.png"
    style.l_root.xpadding = 10
    style.l_root.top_padding = 64
    style.l_root.bottom_padding = 128
    
    # An inner window.
    style.l_window = Style(style.l_default)
    style.l_window.background = Frame("window.png", 0, 0, tile=True)
    style.l_window.left_padding = 6
    style.l_window.xfill = True
    style.l_window.yfill = True
    
    # Normal-sized labels.
    style.l_label = Style(style.l_default)
    style.l_label.xfill = True
    style.l_label.top_padding = 10
    style.l_label.bottom_padding = 8
    style.l_label.bottom_margin = 12
    style.l_label.background = SEPARATOR    
    style.l_label_text = Style(style.l_default)
    style.l_label_text.size = 24
    style.l_label_text.xpos = INDENT
    style.l_label_text.yoffset = 6

    # Small labels.
    style.l_label_small = Style(style.l_default)
    style.l_label_small.xfill = True
    style.l_label_small.bottom_padding = 8
    style.l_label_small.bottom_margin = HALF_SPACER_HEIGHT
    style.l_label_small.background = SEPARATOR    
    style.l_label_small_text = Style(style.l_default)
    style.l_label_small_text.xpos = INDENT
    style.l_label_small_text.yoffset = 6
    style.l_label_small_text.size = 20
    
    # Alternate labels. This nests inside an l_label, and gives a button
    # or label that's nested inside another label.
    style.l_alternate = Style(style.l_default)
    style.l_alternate.xalign = 1.0
    style.l_alternate.yalign = 1.0
    style.l_alternate.yoffset = 4
    style.l_alternate.right_margin = INDENT
    style.l_alternate_text = Style(style.l_default)
    style.l_alternate_text.size = 14
    style.l_alternate_text.font = LIGHT
    style.l_alternate_text.text_align = 1.0
    
    style.l_small_button = Style(style.l_button)
    style.l_small_button_text = Style(style.l_button_text)
    style.l_small_button_text.size = 14
    style.l_small_text = Style(style.l_text)
    style.l_small_text.size = 14
    
    
    # Indents its contents.
    style.l_indent = Style(style.l_default)
    style.l_indent.left_margin = INDENT
    
    # Indents its contents and pads them vertically.
    style.l_indent_margin = Style(style.l_indent)
    style.l_indent_margin.ymargin = 6 
    
    # List button.
    style.l_list = Style(style.l_default)
    style.l_list.left_padding = HALF_INDENT
    style.l_list.xfill = True
    style.l_list.selected_background = LIGHT_IDLE
    style.l_list.selected_hover_background = HOVER
    style.l_list_text = Style(style.l_default)
    style.l_list_text.idle_color = IDLE
    style.l_list_text.hover_color = HOVER
    style.l_list_text.selected_idle_color = WHITE
    style.l_list_text.selected_hover_color = WHITE
    style.l_list_text.insensitive_color = DISABLED

    style.l_list2 = Style(style.l_list)
    style.l_list2.left_padding = HALF_INDENT + INDENT
    style.l_list2_text = Style(style.l_list_text)


    # Scrollbar.
    style.l_vscrollbar = Style(style.l_default)
    style.l_vscrollbar.thumb = Fixed(
        Solid(SCROLLBAR_IDLE, xmaximum=8, xalign=0.5),
        Image("vscrollbar_center.png", xalign=0.5, yalign=0.5),
        xmaximum = SCROLLBAR_SIZE)
    style.l_vscrollbar.hover_thumb = Fixed(
        Solid(HOVER, xmaximum=8, xalign=0.5),
        Image("vscrollbar_center.png", xalign=0.5, yalign=0.5),
        xmaximum = SCROLLBAR_SIZE)
    style.l_vscrollbar.xmaximum = SCROLLBAR_SIZE
    style.l_vscrollbar.bar_vertical = True
    style.l_vscrollbar.bar_invert = True
    style.l_vscrollbar.unscrollable = "hide"
    
    
    # Information window.
    style.l_info_vbox = Style(style.vbox)
    style.l_info_vbox.yalign = 0.5
    style.l_info_vbox.xalign = 0.5
    style.l_info_vbox.xfill = True
    
    style.l_info_frame = Style(style.l_default)
    style.l_info_frame.ypadding = 21
    style.l_info_frame.xfill = True
    style.l_info_frame.background = Fixed(
        "#f9f9f9",
        Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=0.0, yoffset=8),
        Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=1.0, yoffset=-8),
        )    
    style.l_info_frame.yminimum = 180
    style.l_info_frame.ypos = 100
    
    style.l_info_label = Style(style.l_default)
    style.l_info_label.xalign = 0.5
    style.l_info_label.ypos = 100
    style.l_info_label.yanchor = 1.0
    style.l_info_label.yoffset = 12
    style.l_info_label_text = Style(style.l_default)
    style.l_info_label_text.size = 36
    
    style.l_info_text = Style(style.l_default)
    style.l_info_text.xalign = 0.5
        
    style.l_info_button = Style(style.l_button)
    style.l_info_button.xalign = 0.5
    style.l_info_button_text = Style(style.l_button_text)

    # Code navigation
    style.l_navigation_button = Style(style.l_button)
    style.l_navigation_button.size_group = "navigation"
    style.l_navigation_button.right_margin = INDENT
    style.l_navigation_button.top_margin = 3
    style.l_navigation_button_text = Style(style.l_button_text)
    style.l_navigation_button_text.size = 14
    style.l_navigation_button_text.font = REGULAR

    style.l_navigation_text = Style(style.l_text)
    style.l_navigation_text.size = 12
    style.l_navigation_text.font = LIGHT
    style.l_navigation_text.color = TEXT

    # Check boxes
    style.l_checkbox = Style(style.l_button)
    style.l_checkbox.left_padding = INDENT
    style.l_checkbox.background = Image("checkbox_idle.png", yalign=0.5)
    style.l_checkbox.hover_background = Image("checkbox_hover.png", yalign=0.5)
    style.l_checkbox.selected_idle_background = Image("checkbox_selected_idle.png", yalign=0.5)
    style.l_checkbox.selected_hover_background = Image("checkbox_selected_hover.png", yalign=0.5)
    style.l_checkbox.insensitive_background = Image("checkbox_insensitive.png", yalign=0.5)

    style.l_checkbox_text = Style(style.l_button_text)
    style.l_checkbox_text.selected_font = LIGHT
    
    # A normal button that lines up with checkboxes.
    style.l_nonbox = Style(style.l_button)
    style.l_nonbox.xpadding = INDENT
    style.l_nonbox_text = Style(style.l_button_text)
    style.l_nonbox_text.selected_font = LIGHT
        
    # A progress bar and its frame.
    style.l_progress_frame = Style(style.l_default)
    style.l_progress_frame.background = Frame("pattern.png", 0, 0, tile=True)
    style.l_progress_frame.ypadding = 5
    
    style.l_progress_bar = Style(style.l_default)
    style.l_progress_bar.left_bar = LIGHT_IDLE
    style.l_progress_bar.right_bar = Null()
    style.l_progress_bar.ymaximum = 24


