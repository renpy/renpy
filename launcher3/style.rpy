init python:

    # Common styles.
    style.common_frame.background = "#bbccccf5"
    style.common_frame.xfill = True

    # Launcher (main frame) styles.
    style.launcher_frame = Style(style.common_frame)
    style.launcher_frame.yfill = True
    style.launcher_frame.xpadding = 5
    style.launcher_frame.ypadding = 5
    style.launcher_frame.xmargin = 5
    style.launcher_frame.top_margin = 29 + 17 + 5
    style.launcher_frame.bottom_margin = 5

    style.launcher_text.font = "DejaVuSans.ttf"
    style.launcher_text.size = 14
    style.launcher_text.color = "#000"
    
    style.launcher_button_text.font = "DejaVuSans.ttf"
    style.launcher_button_text.size = 14
    style.launcher_button_text.color = "#008"
    style.launcher_button_text.hover_color = "#04c"
    style.launcher_button_text.insensitive_color = "#888"


    # The top navigation bar.

    style.topnav_frame = Style(style.common_frame)
    
    style.topnav_button = Style(style.launcher_button)
    style.topnav_button.xpadding = 10    

    style.topnav_button_text = Style(style.launcher_button_text)
    style.topnav_button_text.xalign = 1.0
    style.topnav_button_text.size = 24
    style.topnav_button_text.kerning = -1.5
    
    # The secondary navigation bar.

    style.secnav_frame = Style(style.common_frame)
    style.secnav_frame.ypos = 29
    
    style.secnav_button = Style(style.launcher_button)
    style.secnav_button.xpadding = 10    

    style.secnav_button_text = Style(style.launcher_button_text)
