init python in styles:

    from store import Frame, Style, style, im

    # Frames
    full_frame = Frame("frame.png", 10, 10)
    bottom_frame = Frame(im.Crop("frame.png", (10, 10, 30, 40)), 0, 0, 0, 10)
    no_frame = Frame(im.Crop("frame.png", (10, 10, 30, 30)), 0, 0)

    full_hover_frame = Frame("hover_frame.png", 10, 10)
    bottom_hover_frame = Frame(im.Crop("hover_frame.png", (10, 10, 30, 40)), 0, 0, 0, 10)
    no_hover_frame = Frame(im.Crop("hover_frame.png", (10, 10, 30, 30)), 0, 0)


    # Launcher (main frame) styles.
    style.launcher_frame = Style(style.default)
    style.launcher_frame.background = full_frame
    style.launcher_frame.xfill = True
    style.launcher_frame.yfill = True
    style.launcher_frame.xpadding = 10
    style.launcher_frame.ypadding = 10
    style.launcher_frame.xmargin = 0
    style.launcher_frame.top_margin = 55
    style.launcher_frame.bottom_margin = 0

    style.launcher_text.font = "DejaVuSans.ttf"
    style.launcher_text.size = 13
    style.launcher_text.color = "#000"
    
    style.launcher_button.background = None
    style.launcher_button.hover_background = no_hover_frame


    # The top navigation bar.

    style.topnav_frame = Style(style.default)
    style.topnav_frame.background = no_frame
    style.topnav_frame.xfill = True
    style.topnav_frame.xpadding = 0
    style.topnav_frame.top_padding = 0
    style.topnav_frame.bottom_padding = 0
    
    style.topnav_button = Style(style.launcher_button)
    style.topnav_button.xpadding = 10    

    style.topnav_button_text = Style(style.launcher_button_text)
    style.topnav_button_text.font = "DejaVuSans-ExtraLight.ttf"
    style.topnav_button_text.size = 28
    style.topnav_button_text.kerning = -2
    style.topnav_button_text.color = "#666"
    style.topnav_button_text.selected_color = "#000"
    style.topnav_button_text.insensitive_color = "#ddd"
    
    # The secondary navigation bar.

    style.secnav_frame = Style(style.default)
    style.secnav_frame.background = bottom_frame
    style.secnav_frame.ypos = 33
    style.secnav_frame.xfill = True
    style.secnav_frame.bottom_padding = 5
    
    style.secnav_button = Style(style.launcher_button)
    style.secnav_button.xpadding = 10    

    style.secnav_button_text = Style(style.launcher_button_text)
    style.secnav_button_text.color = "#666"
    style.secnav_button_text.size = 13
    style.secnav_button_text.selected_color = "#000"
    style.secnav_button_text.insensitive_color = "#ddd"
    
    # Command Button
    style.command_button.background = full_frame
    style.command_button.hover_background = full_hover_frame
    style.command_button.xpadding = 10
    style.command_button.ypadding = 10
    
    style.command_button_text.size = 13
    style.command_button_text.color = "#666"
    