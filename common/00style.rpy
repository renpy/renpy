# Copyright 2004-2008 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# This file is responsible for creating and defining the default styles
# used by the system.

# This file should be considered part of the Ren'Py library, and not
# something that needs to be modified by the user. Instead, just update
# the appropriate style property in an init: block in your script.
#
# For example, to change the default window backgrounds to a
# transparent dark red, add:
#
# init:
#     $ style.window.background = "#8008"
#
# to your script. No need to mess around here, it will just make your
# life harder when a new version of Ren'Py is released.

init -1200 python hide:

    # Style Declarations #################################################

    style.default = Style(None, help='The default style that all styles inherit from.')

    style.hbox = Style(style.default, help='Default for hboxes')
    style.vbox = Style(style.default, help='Default for vboxen')

    style.window = Style(style.default, help='Windows created by ui.window')

    style.image_placement = Style(style.default, help='The default placement of images on the screen.')
    style.image = Style(style.default, help="Default style of images.")

    style.animation = Style(style.default, help="Default style of animations.")

    style.say_label = Style(style.default, help='The speaker of dialogue.')
    style.say_dialogue = Style(style.default, help='Used for dialogue text.')
    style.say_thought = Style(style.default, help='Used for thoughts by the narrator.')
    style.say_window = Style(style.window, help='Windows containing dialogue and thoughts.')
    style.say_who_window = Style(style.window, help='Used for the window containing the label in two-window-say mode.')
    style.say_two_window_vbox = Style(style.vbox, help='The vbox containing the two windows in two-window-say mode.')
    style.say_vbox = Style(style.vbox, help='Containins the label (if present) and the body of dialogue and thoughts.')

    style.menu = Style(style.default, help='Used for the vbox containing a menu.')
    style.menu_caption = Style(style.default, help='Used for menu captions.')
    style.menu_choice = Style(style.default, help='Used to for the text of a menu choice.')
    style.menu_choice_button = Style(style.default, help='Used for buttons containing menu choices.')
    style.menu_choice_chosen = Style(style.menu_choice, help='Used for the text of a menu choice that has been chosen.')
    style.menu_choice_chosen_button = Style(style.menu_choice_button, help='Used for buttons containing chosen menu choices.')
    style.menu_window = Style(style.window, help='The style of a window containing a menu.')

    style.input_text = Style(style.default, help='Used for the text of an input box.')
    style.input_prompt = Style(style.default, help='Used for the prompt of an input box.')
    style.input_window = Style(style.window, help='Used for the window of an input box.')

    style.centered_window = Style(style.default, help='Used for a "window" containing centered text, displayed using centered.')
    style.centered_text = Style(style.default, help='Used for centered text displayed by centered or show text.')

    style.imagemap = Style(style.image_placement, help='Used for imagemaps.')
    style.imagemap_button = Style(style.default, help='Buttons inside imagemaps.')

    style.image_button = Style(style.default, help='Image buttons.')
    style.image_button_image = Style(style.default, help='Images inside image buttons.')

    style.hyperlink = Style(style.default, help='A hyperlink button.')
    style.hyperlink_text = Style(style.default, help='Hyperlink button text.')

    style.viewport = Style(style.default, help='Used for viewports.')

    # The base styles that can be customized by themes.

    style.frame = Style(style.default, help='Base style for frames.')
    
    style.button = Style(style.default, help='Base style for buttons.')
    style.button_text = Style(style.default, help='Base style for button text.')

    style.small_button = Style(style.button, help="Base style for small buttons.")
    style.small_button_text = Style(style.button_text, help="Base style for small button text.")
    style.radio_button = Style(style.button, help="Base style for radio buttons.")
    style.radio_button_text = Style(style.button_text, help="Base style for radio button text.")
    style.check_button = Style(style.button, help="Base style for check buttons.")
    style.check_button_text = Style(style.button_text, help="Base style for check button text.")
    style.large_button = Style(style.button, help="Base style for large buttons.")
    style.large_button_text = Style(style.button_text, help="Base style for large button text.")

    style.label = Style(style.default, help="Base style for windows surrounding labels.")
    style.label_text = Style(style.default, help="Base style for label text.")

    style.prompt = Style(style.default, help="Base style for windows surrounding prompts.")
    style.prompt_text = Style(style.default, help="Base style for prompt text.")
    
    style.bar = Style(style.default, help='Base style for horizontal bars.')
    style.vbar = Style(style.default, help='Base style for vertical bars.')
    style.scrollbar = Style(style.bar, help='Base style for horizontal scrollbars.')
    style.vscrollbar = Style(style.vbar, help='Used for vertical scollbars.')
    
    style.text = Style(style.default, help="Base style for interface text.")
    style.small_text = Style(style.text, help="Base style for small interface text.")


    
init -1090 python:
    
    # Colors #############################################################

    # The Default Style ###################################################

    # Text properties.
    style.default.font = "DejaVuSans.ttf"
    style.default.language = "western"
    style.default.antialias = True
    style.default.size = 22
    style.default.color = (255, 255, 255, 255)
    style.default.black_color = (0, 0, 0, 255)
    style.default.bold = False
    style.default.italic = False
    style.default.underline = False
    style.default.drop_shadow = None
    style.default.drop_shadow_color = (0, 0, 0, 255)
    style.default.minwidth = 0
    style.default.textalign = 0
    style.default.text_y_fudge = 0
    style.default.first_indent = 0
    style.default.rest_indent = 0
    style.default.line_spacing = 0
    style.default.layout = "greedy"
    style.default.subtitle_width = 0.9
    style.default.slow_cps = None
    style.default.slow_cps_multiplier = 1.0
    style.default.slow_abortable = False
    
    # Window properties.
    style.default.background = None
    style.default.xpadding = 0
    style.default.ypadding = 0
    style.default.xmargin = 0
    style.default.ymargin = 0
    style.default.xfill = False
    style.default.yfill = False
    style.default.xminimum = 0 # Includes margins and padding.
    style.default.yminimum = 0 # Includes margins and padding.

    # Placement properties.
    style.default.xpos = None # 0
    style.default.ypos = None # 0
    style.default.xanchor = None # 0
    style.default.yanchor = None # 0
    style.default.xmaximum = None
    style.default.ymaximum = None
    style.default.xoffset = 0
    style.default.yoffset = 0

    # Sound properties.
    style.default.sound = None

    # Box properties.
    style.default.spacing = 0
    style.default.first_spacing = None
    style.default.box_layout = None

    # Focus properties.
    style.default.focus_mask = None
    style.default.focus_rect = None

    # Bar properties.
    style.default.left_bar = None
    style.default.right_bar = None
    style.default.thumb = None
    style.default.thumb_shadow = None
    
    # Misc.
    style.default.activate_sound = None
    style.default.clipping = False

    # Boxes.
    style.hbox.box_layout = 'horizontal'
    style.vbox.box_layout = 'vertical'

    # Windows.
    style.window.background = Solid((0, 0, 128, 128))
    style.window.xpadding = 10
    style.window.ypadding = 5
    style.window.xmargin = 10
    style.window.ymargin = 5
    style.window.xfill = True
    style.window.yfill = False
    style.window.xminimum = 0 # Includes margins and padding.
    style.window.yminimum = 150 # Includes margins and padding.

    style.window.xalign = 0.5
    style.window.yalign = 1.0

    # Image placement.
    style.image_placement.xpos = 0.5
    style.image_placement.ypos = 1.0
    style.image_placement.xanchor = 0.5
    style.image_placement.yanchor = 1.0

    # Dialogue
    style.say_label.bold = True
    style.say_vbox.spacing = 8

    # Two window styles.
    style.say_who_window.xminimum = 200
    style.say_who_window.yminimum = 34
    style.say_who_window.xfill = False
    style.say_who_window.xalign = 0

    style.say_two_window_vbox.yalign = 1.0

    # Menus.
    style.menu_choice.idle_color = "#0ff"
    style.menu_choice.hover_color = "#ff0"
    style.input_text.color = "#ff0"

    # Styles used by centered.
    style.centered_window.xalign = 0.5
    style.centered_window.xfill = False                      
    style.centered_window.yalign = 0.5
    style.centered_window.yfill = False
    style.centered_window.xpadding = 10

    style.centered_text.textalign = 0.5
    style.centered_text.xalign = 0.5
    style.centered_text.yalign = 0.5
    style.centered_text.layout = "subtitle"

    # Hyperlinks.
    style.hyperlink_text.underline = True
    style.hyperlink_text.hover_color = "#0ff"
    style.hyperlink_text.idle_color = "#08f"
    
    # Bars.
    style.bar.bar_invert = False
    style.bar.bar_resizing = False
    style.bar.bar_vertical = False
    style.vbar.bar_vertical = True
    style.vbar.bar_invert = False
    style.vscrollbar.bar_invert = True

    # Viewport
    style.viewport.clipping = True

    ######################################################################

    # Error messages.
    style.error_root.background = Solid((220, 220, 255, 255))
    style.error_root.xfill = True
    style.error_root.yfill = True
    style.error_root.xpadding = 20
    style.error_root.ypadding = 20

    style.error_title.color = (255, 128, 128, 255)
    style.error_body.color = (128, 128, 255, 255)

