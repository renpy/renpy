init python:
    INDENT = 20
    HALF_INDENT = 10
    SCROLLBAR_SIZE = 16
    SEPARATOR = Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=1.0)
    SPACER = Null(height=12)
    HALF_SPACER = Null(height=6)
    
    # Colors.
    TEXT = "#545454"
    IDLE = "#42637b"
    LIGHT_IDLE = "#78a5c5"
    SCROLLBAR_IDLE = "#dfdfdf"
    HOVER = "#d86b45"
    WHITE = "#ffffff"
    
    # Default style.
    style.l_default = Style(style.default)
    style.l_default.font = "Roboto-Light.ttf"
    style.l_default.color = TEXT
    style.l_default.idle_color = IDLE
    style.l_default.hover_color = HOVER
    style.l_default.size = 18
    
    style.l_text = Style(style.l_default)
    style.l_button = Style(style.l_default)
    style.l_button_text = Style(style.l_default)
    
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
    style.l_window.right_margin = 0
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
    
    # Alternate labels. This nests inside an l_label, and gives a button
    # or label that's nested inside another label.
    style.l_alternate = Style(style.l_default)
    style.l_alternate.xalign = 1.0
    style.l_alternate.yalign = 1.0
    style.l_alternate.right_margin = INDENT
    style.l_alternate_text = Style(style.l_default)
    style.l_alternate_text.yoffset = 4
    style.l_alternate_text.size = 14
    style.l_alternate_text.text_align = 1.0
    
    # Indents its contents by 16 pixels.
    style.l_indent = Style(style.l_default)
    style.l_indent.left_margin = INDENT
    
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
    