init python hide:
    # Default style.
    style.l_default = Style(style.default)
    style.l_default.font = "DejaVuSans.ttf"
    style.l_default.color = "#222"
    style.l_default.idle_color = "#3183a3"
    style.l_default.selected_idle_color = "#eeaaaa"
    style.l_default.hover_color = "#6090c0"
    style.l_default.selected_hover_color = "#c06060"
    style.l_default.size = 20
    
    # The main frame. (This should be the only frame on the screen.)
    style.l_frame = Style(style.l_default)
    style.l_frame.background = "background.png"
    style.l_frame.xfill = True
    style.l_frame.yfill = True
    style.l_frame.xpadding = 30
    style.l_frame.top_padding = 30
    style.l_frame.bottom_padding = 60
    
    # Normal text.
    style.l_text = Style(style.l_default)
    style.l_text.color = "#000"
    
    # Labels: The base style for information, error, and prompt text.
    style.l_label = Style(style.l_default)
    style.l_label.xfill = True
    
    style.l_label_text = Style(style.l_default)
    style.l_label_text.size = 22
    style.l_label_text.xalign = 0.5
    style.l_label_text.text_align = 0.5
    style.l_label_text.layout = "subtitle"

    # Prompt text.
    style.l_prompt = Style(style.l_label)
    style.l_prompt_text = Style(style.l_label_text)    
    style.l_prompt.background = Image("divider.png", yalign=1.0, yoffset=-8, xalign=0.5)
    style.l_prompt.bottom_padding = 22
    
    # Error text.
    style.l_error = Style(style.l_label)
    style.l_error_text = Style(style.l_label_text)    
    style.l_error_text.color = "#800"
    
    # Info text.
    style.l_info = Style(style.l_label)
    style.l_info_text = Style(style.l_label_text)    

    # Small label text.
    style.l_small = Style(style.l_label)
    style.l_small_text = Style(style.l_label_text)    
    style.l_small_text.size = 14
    
    # Normal buttons. (These look like hyperlinked text.)
    style.l_button = Style(style.l_default)
    style.l_button_text = Style(style.l_default)
    
    # Bottom buttons.
    style.l_bottom_button = Style(style.l_default)
    style.l_bottom_button.background = "button.png"
    style.l_bottom_button.xminimum = 180
    style.l_bottom_button.yminimum = 45
    style.l_bottom_button_text = Style(style.l_default)
    style.l_bottom_button_text.xalign = 0.5
    style.l_bottom_button_text.yalign = 0.5

    # List buttons.
    style.l_list = Style(style.l_button)
    style.l_list.xmargin = 5
    style.l_list.xpadding = 5
    style.l_list_text = Style(style.l_button_text)
    style.l_list_text.size = 14

    # Alternate buttons.
    style.l_alternate = Style(style.l_button)
    style.l_alternate.xalign = 1.0
    style.l_alternate_text = Style(style.l_button_text)
    style.l_alternate_text.size = 14
    
    
    
##############################################################################
# Elements that are used by multiple screens.

# Buttons at the bottom of the screen.
#
# parameters:
# left_label - the label for the left button.
# left_action - the action for the left_button.
# right_label - the label for the right button.
# 
    # label - the label of the button.
# action - the action to run when the button is clicked.
screen bottom_buttons:

    default left_label = None
    default right_label = None
    
    if left_label is not None:
    
        textbutton left_label style "l_bottom_button":
            xanchor 0.5
            xpos (1.1 / 6.0)
            yalign 0.98
            action left_action
        
    if right_label is not None:
    
        textbutton right_label style "l_bottom_button":
            xanchor 0.5
            xpos (4.9 / 6.0)
            yalign 0.98
            action right_action

# Spacers that are used to space elements out vertically.
screen small_spacer:
    null height 12
    
screen spacer:
    null height 24
    

##############################################################################
# Standard screens.
# 
# These are displayed by the interface.<screen> functions, 
screen interface_info:
    
    frame:
        style_group "l"
        
        has vbox
        
        label info style "l_info"
    
        use small_spacer
        
        label _("(please click to continue)") style "l_small"
        
    use bottom_buttons

    
screen interface_error:
    
    frame:
        style_group "l"
        
        has vbox
        
        label info style "l_error"
    
        use small_spacer
        
        label _("(please click to continue)") style "l_small"
        
    use bottom_buttons
        
        
screen interface_progress:
    frame:
        style_group "l"
        
        has vbox
        
        label info style "l_info"
    
    # The progress screen can't have bottom buttons.
        
    
init python in interface:

    def info(info, right_label=None, right_action=None, left_label=None, left_action=None):
        
        ui.saybehavior()
        rv = renpy.call_screen("interface_info", info=info, 
            right_label=right_label, right_action=right_action,
            left_label=left_label, left_action=left_action)
            
        return rv
                
    def error(info, right_label=None, right_action=None, left_label=None, left_action=None):
        
        ui.saybehavior()
        rv = renpy.call_screen("interface_error", info=info, 
            right_label=right_label, right_action=right_action,
            left_label=left_label, left_action=left_action)
            
        return rv
        
    def progress(info):
        renpy.show_screen("interface_progress", info=info, _transient=True)
        renpy.pause(0)
        