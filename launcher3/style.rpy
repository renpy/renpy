init python in styles:

    from store import Frame, Style, style, im

    # Frames
    full_frame = Frame("_theme_launcher/frame.png", 10, 10)
    bottom_frame = Frame(im.Crop("_theme_launcher/frame.png", (10, 10, 30, 40)), 0, 0, 0, 10)
    no_frame = Frame(im.Crop("_theme_launcher/frame.png", (10, 10, 30, 30)), 0, 0)

    full_hover_frame = Frame("_theme_launcher/hover_frame.png", 10, 10)
    bottom_hover_frame = Frame(im.Crop("_theme_launcher/hover_frame.png", (10, 10, 30, 40)), 0, 0, 0, 10)
    no_hover_frame = Frame(im.Crop("_theme_launcher/hover_frame.png", (10, 10, 30, 30)), 0, 0)

    # Take the default style from _default.
    style.default.take(style._default)

    # Lists of choices.

    style.choice_button.background = None 
    style.choice_button.hover_background = no_hover_frame
    style.choice_button.left_padding = 5
    
    style.choice_button_text.size = 14 
    style.choice_button_text.color = "#666"
    style.choice_button_text.selected_color = "#000"
    style.choice_button_text.insensitive_color = "#ddd"

    # Labels. 
    
    style._label.top_margin = 10
    style._label.bottom_margin = 7

    style._label_text.color = "#000"
    style._label_text.size = 14
    style._label_text.bold = True

    # The top navigation bar.

    style.topnav_frame = Style(style.default)
    style.topnav_frame.background = no_frame
    style.topnav_frame.xfill = True
    style.topnav_frame.xpadding = 0
    style.topnav_frame.top_padding = 0
    style.topnav_frame.bottom_padding = 0
    
    style.topnav_button = Style(style.launcher_button)
    style.topnav_button.xmargin = 5
    style.topnav_button.xpadding = 5    
    style.topnav_button.top_padding = 5

    style.topnav_button_text = Style(style.launcher_button_text)
    style.topnav_button.hover_background = no_hover_frame
    style.topnav_button_text.font = "DejaVuSans-ExtraLight.ttf"
    style.topnav_button_text.size = 28
    style.topnav_button_text.kerning = -2
    
    # The secondary navigation bar.

    style.secnav_frame = Style(style.default)
    style.secnav_frame.background = bottom_frame
    style.secnav_frame.ypos = 38
    style.secnav_frame.xfill = True
    style.secnav_frame.bottom_padding = 5
    
    style.secnav_button = Style(style.launcher_button)
    style.secnav_button.hover_background = no_hover_frame
    style.secnav_button.xmargin = 5
    style.secnav_button.left_padding = 8    
    style.secnav_button.right_padding = 5
    
    style.secnav_button_text = Style(style.launcher_button_text)
    style.secnav_button_text.size = 14
    
    # Page frame.
    style.page = Style(style._frame)
    style.page.top_margin = 55
    style.page.yfill = False
    style.page.xfill = False
    style.page.xalign = 0.6
    style.page.xminimum = 500

    # Link buttons.
    style.link = Style(style._default)
    style.link.hover_background = no_hover_frame
    style.link.left_margin = 5
    style.link_text = Style(style._default)
    style.link_text.color = "#44c"
    style.link_text.hover_underline = True

    # Checkbox buttons.
    style.checkbox = Style(style._default)
    style.checkbox.background = "_theme_launcher/bar.png"
    style.checkbox.hover_background = "_theme_launcher/hover_bar.png"
    style.checkbox.selected_background = "_theme_launcher/check.png"
    style.checkbox.selected_hover_background = "_theme_launcher/hover_check.png"
    style.checkbox.left_padding = 25
    style.checkbox.top_padding = 5
    
init 10:                   

    transform _notify_transform:
        # These control the position.
        xalign .5
        ypos 5
    
        # These control the actions on show and hide.
        on show:
            alpha 0
            linear .125 alpha 1.0
        on hide:
            linear .5 alpha 0.0

    screen notify:
        zorder 200
    
        frame:
            at _notify_transform
            style_group ""
            
            ypadding 13
            xpadding 20
            
            text "[message!q]":
                text_align 0.5
    
        timer 1.625 action Hide('notify')

