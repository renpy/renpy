# Copyright 2004-2006 PyTom
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
#     $ style.window.background = renpy.Solid((128, 0, 0, 128)
#
# to your script. No need to mess around here, it will just make your
# life harder when a new version of Ren'Py is released.

init -1200 python hide:

    # Style Declarations #################################################

    style.default = Style(None, heavy=True, help='The default style that all styles inherit from.')

    style.hbox = Style(style.default, heavy=True, help='Default for hboxes')
    style.vbox = Style(style.default, heavy=True, help='Default for vboxen')

    style.window = Style(style.default, heavy=True, help='Windows created by ui.window')
    style.frame = Style(style.default, heavy=True, help='Frames created by ui.frame')

    style.image_placement = Style(style.default, heavy=True, help='The default placement of images on the screen.')
    style.image = Style(style.default, heavy=True, help="Default style of images.")

    style.animation = Style(style.default, heavy=True, help="Default style of animations.")

    style.say_label = Style(style.default, heavy=True, help='The speaker of dialogue.')
    style.say_dialogue = Style(style.default, heavy=True, help='Used for dialogue text.')
    style.say_thought = Style(style.default, heavy=True, help='Used for thoughts by the narrator.')
    style.say_window = Style(style.window, heavy=True, help='Windows containing dialogue and thoughts.')
    style.say_who_window = Style(style.window, heavy=True, help='Used for the window containing the label in two-window-say mode.')
    style.say_two_window_vbox = Style(style.vbox, heavy=True, help='The vbox containing the two windows in two-window-say mode.')
    style.say_vbox = Style(style.vbox, heavy=True, help='Containins the label (if present) and the body of dialogue and thoughts.')

    style.menu = Style(style.default, heavy=True, help='Used for the vbox containing a menu.')
    style.menu_caption = Style(style.default, heavy=True, help='Used for menu captions.')
    style.menu_choice = Style(style.default, heavy=True, help='Used to for the text of a menu choice.')
    style.menu_choice_button = Style(style.default, heavy=True, help='Used for buttons containing menu choices.')
    style.menu_choice_chosen = Style(style.menu_choice, help='Used for the text of a menu choice that has been chosen.')
    style.menu_choice_chosen_button = Style(style.menu_choice_button, help='Used for buttons containing chosen menu choices.')
    style.menu_window = Style(style.window, heavy=True, help='The style of a window containing a menu.')

    style.input_text = Style(style.default, heavy=True, help='Used for the text of an input box.')
    style.input_prompt = Style(style.default, heavy=True, help='Used for the prompt of an input box.')
    style.input_window = Style(style.window, heavy=True, help='Used for the window of an input box.')

    style.centered_window = Style(style.default, heavy=True, help='Used for a "window" containing centered text, displayed using centered.')
    style.centered_text = Style(style.default, heavy=True, help='Used for centered text displayed by centered or show text.')

    style.imagemap = Style(style.image_placement, heavy=True, help='Used for imagemaps.')
    style.imagemap_button = Style(style.default, heavy=True, help='Buttons inside imagemaps.')

    style.image_button = Style(style.default, heavy=True, help='Image buttons.')
    style.image_button_image = Style(style.default, heavy=True, help='Images inside image buttons.')

    style.button = Style(style.default, heavy=True, help='Buttons created using ui.button.')
    style.button_text = Style(style.default, heavy=True, help='The text of buttons created using ui.textbutton ')

    style.menu_button = Style(style.button, heavy=True, help='Buttons that are part of the main or game menus.')
    style.menu_button_text = Style(style.button_text, heavy=True, help='The label of buttons that are part of the main or game menus.')

    style.bar = Style(style.default, heavy=True, help='Used for bars.')
    style.vbar = Style(style.default, heavy=True, help='Used for vertical bars.')
    style.scrollbar = Style(style.bar, heavy=True, help='Used for scrollbars.')
    style.vscrollbar = Style(style.vbar, heavy=True, help='Used for vertical scollbars.')

    style.thin_hbox = Style(style.hbox, heavy=True, help='A hbox with a small amount of spacing.')
    style.thick_hbox = Style(style.hbox, heavy=True, help='A hbox with a large amount of spacing.')
    style.thin_vbox = Style(style.vbox, heavy=True, help='A vbox with a small amount of spacing.')
    style.thick_vbox = Style(style.vbox, heavy=True, help='A vbox with a large amount of spacing.')

    style.hyperlink = Style(style.default, heavy=True, help='A hyperlink button.')
    style.hyperlink_text = Style(style.default, heavy=True, help='Hyperlink button text.')

    style.viewport = Style(style.default, heavy=True, help='Used for viewports.')
        

init -1090 python:
    
    # Colors #############################################################

    dark_cyan = (0, 192, 255, 255)
    bright_cyan = (0, 255, 255, 255)

    dark_red = (255, 128, 128, 255)
    bright_red = (255, 64, 64, 255)

    green = (0, 128, 0, 255)

    # The Default Style ###################################################

    # Text properties.
    style.default.font = "DejaVuSans.ttf"
    style.default.antialias = True
    style.default.size = 22
    style.default.color = (255, 255, 255, 255)
    style.default.black_color = (0, 0, 0, 255)
    style.default.bold = False
    style.default.italic = False
    style.default.underline = False
    style.default.drop_shadow = (1, 1)
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
    style.default.box_spacing = 0
    style.default.box_first_spacing = None
    style.default.box_layout = None

    # Focus properties.
    style.default.focus_mask = None
    style.default.focus_rect = None

    # Misc.
    style.default.activate_sound = None
    style.default.clipping = False

    ######################################################################
    # The style of various boxes.

    style.hbox.box_layout = 'horizontal'
    style.vbox.box_layout = 'vertical'

    style.thin_hbox.box_spacing = 3
    style.thick_hbox.box_spacing = 30
    style.thin_vbox.box_spacing = 0
    style.thick_vbox.box_spacing = 30

    ######################################################################
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

    style.window.xpos = 0.5
    style.window.ypos = 1.0
    style.window.xanchor = 0.5
    style.window.yanchor = 1.0

    # Frames.
    style.frame.background = Solid((0, 0, 128, 128))
    style.frame.xpadding = 10
    style.frame.ypadding = 5
    style.frame.xmargin = 10
    style.frame.ymargin = 5

    ######################################################################
    # Image placement.

    style.image_placement.xpos = 0.5
    style.image_placement.ypos = 1.0
    style.image_placement.xanchor = 0.5
    style.image_placement.yanchor = 1.0


    ######################################################################
    # Dialogue

    style.say_label.bold = True
    style.say_vbox.box_spacing = 8

    # Two window styles.
    style.say_who_window.xminimum = 200
    style.say_who_window.yminimum = 34
    style.say_who_window.xfill = False
    style.say_who_window.xalign = 0

    style.say_two_window_vbox.yalign = 1.0

    # Menus.
    style.menu_choice.hover_color = (255, 255, 0, 255) # yellow
    style.menu_choice.idle_color = (0, 255, 255, 255) # cyan

    style.input_text.color = (255, 255, 0, 255)

    # Styles used by centered.
    style.centered_window.xpos = 0.5
    style.centered_window.xanchor = 0.5
    style.centered_window.xfill = False                      
    style.centered_window.ypos = 0.5
    style.centered_window.yanchor = 0.5
    style.centered_window.yfill = False
    style.centered_window.xpadding = 10

    style.centered_text.textalign = 0.5
    style.centered_text.xpos = 0.5
    style.centered_text.ypos = 0.5
    style.centered_text.xanchor = 0.5
    style.centered_text.yanchor = 0.5
    style.centered_text.layout = "subtitle"


    ######################################################################
    # Buttons.

    style.button_text.color = dark_cyan
    style.button_text.hover_color = bright_cyan
    style.button_text.insensitive_color = (192, 192, 192, 255)
    style.button_text.size = 24
    style.button_text.drop_shadow = (2, 2)        

    style.button_text.selected_color = dark_red
    style.button_text.selected_hover_color = bright_red

    style.button_text.xpos = 0.5
    style.button_text.xanchor = 0.5

    style.menu_button.xpos = 0.5
    style.menu_button.xanchor = 0.5

    ######################################################################
    # Hyperlinks
    style.hyperlink_text.underline = True
    style.hyperlink_text.hover_color = bright_cyan
    style.hyperlink_text.idle_color = dark_cyan


    ######################################################################
    # Bar.

    style.bar.bar_vertical = False
    style.bar.bar_invert = False
    style.bar.ymaximum = 22

    style.bar.left_bar = Solid(bright_cyan)
    style.bar.right_bar = Solid((0, 0, 0, 128))
    style.bar.bottom_bar = Solid(bright_cyan)
    style.bar.top_bar = Solid((0, 0, 0, 128))
    style.bar.left_gutter = 0
    style.bar.right_gutter = 0
    style.bar.bottom_gutter = 0
    style.bar.top_gutter = 0
    style.bar.thumb = None
    style.bar.thumb_offset = 0
    style.bar.thumb_shadow = None

    style.vbar.bar_vertical = True
    style.vbar.bar_invert = False
    style.vbar.xmaximum = 22

    style.vbar.left_bar = Solid(bright_cyan)
    style.vbar.right_bar = Solid((0, 0, 0, 128))
    style.vbar.bottom_bar = Solid(bright_cyan)
    style.vbar.top_bar = Solid((0, 0, 0, 128))
    style.vbar.left_gutter = 0
    style.vbar.right_gutter = 0
    style.vbar.bottom_gutter = 0
    style.vbar.top_gutter = 0
    style.vbar.thumb = None
    style.vbar.thumb_offset = 0
    style.vbar.thumb_shadow = None

    style.vscrollbar.bottom_bar = Solid((0, 0, 0, 128))        
    style.vscrollbar.top_bar = Solid(bright_cyan) 
    style.vscrollbar.bar_invert = True

    ######################################################################
    # Viewport
    style.viewport.clipping = True

    ######################################################################
    # Main menu.

    style.mm_root.background = Solid((0, 0, 0, 255))
    style.mm_root.xfill = True
    style.mm_root.yfill = True

    style.mm_menu_frame.xpos = 0.9
    style.mm_menu_frame.xanchor = 1.0
    style.mm_menu_frame.ypos = 0.9
    style.mm_menu_frame.yanchor = 1.0


    ######################################################################
    # Game menu common.

    style.gm_root.background = Solid((0, 0, 0, 255))
    style.gm_root.xfill = True
    style.gm_root.yfill = True

    style.gm_nav_frame.xpos = 0.95
    style.gm_nav_frame.xanchor = 1.0
    style.gm_nav_frame.ypos = 0.95
    style.gm_nav_frame.yanchor = 1.0


    ##############################################################################
    # File picker.

    style.file_picker_frame.xpos = 0
    style.file_picker_frame.xanchor = 0.0
    style.file_picker_frame.ypos = 0
    style.file_picker_frame.yanchor = 0.0
    style.file_picker_frame.xpadding = 5

    style.file_picker_navbox.xpos = 10

    style.file_picker_grid.xfill = True

    style.file_picker_entry.xpadding = 5
    style.file_picker_entry.ypadding = 2
    style.file_picker_entry.xmargin = 5
    style.file_picker_entry.xfill = True
    style.file_picker_entry.ymargin = 2        
    style.file_picker_entry.background = Solid((255, 255, 255, 255))
    style.file_picker_entry.hover_background = Solid((255, 255, 192, 255))

    style.file_picker_text.size = 16
    style.file_picker_text.color = dark_cyan
    style.file_picker_text.hover_color = bright_cyan

    style.file_picker_new.hover_color = bright_red
    style.file_picker_new.idle_color = dark_red

    style.file_picker_new.minwidth = 40
    style.file_picker_old.minwidth = 40

    style.file_picker_new.text_align = 1.0
    style.file_picker_old.text_align = 1.0


    ######################################################################
    # Yes/No Dialog

    style.yesno_label.color = green
    style.yesno_label.textalign = 0.5
    style.yesno_label.xpos = 0.5
    style.yesno_label.xanchor = 0.5

    style.yesno_frame.xfill = True
    style.yesno_frame.yminimum = 0.5
    style.yesno_frame.xmargin = .1

    style.yesno_frame_vbox.xpos = 0.5
    style.yesno_frame_vbox.xanchor = 0.5
    style.yesno_frame_vbox.ypos = 0.5
    style.yesno_frame_vbox.yanchor = 0.5

    style.yesno_button_hbox.xalign = 0.5
    style.yesno_button_hbox.box_spacing = 100
    
    ##############################################################################
    # Preferences.


    style.prefs_pref_frame.xpos = 0.5
    style.prefs_pref_frame.xanchor = 0.5
    style.prefs_pref_frame.bottom_margin = 10

    style.prefs_label.xpos = 0.5
    style.prefs_label.xanchor = 0.5
    style.prefs_label.color = green

    style.prefs_slider.xmaximum=200
    style.prefs_slider.ymaximum=22
    style.prefs_slider.xpos = 0.5
    style.prefs_slider.xanchor = 0.5

    style.prefs_hbox.xpos = 0.5
    style.prefs_hbox.xanchor = 0.5

    style.prefs_button.xpos = 0.5
    style.prefs_button.xanchor = 0.5

    style.prefs_button.selected_xpos = 0.5
    style.prefs_button.selected_xanchor = 0.5

    style.prefs_frame.xfill=True
    style.prefs_frame.ypadding = 0.05

    style.prefs_column.box_spacing = 6

    style.prefs_left.xanchor = 0.5
    style.prefs_left.xpos = 1.0 / 6.0

    style.prefs_center.xanchor = 0.5
    style.prefs_center.xpos = 3.0 / 6.0

    style.prefs_right.xanchor = 0.5
    style.prefs_right.xpos = 5.0 / 6.0

    style.prefs_spinner.xpos = 0.5
    style.prefs_spinner.xanchor = 0.5

    style.prefs_spinner_label.minwidth = 100
    style.prefs_spinner_label.textalign = 0.5

    style.prefs_js_button_text.size = 18
    style.prefs_js_button_text.drop_shadow = (1, 1)

    style.js_function_label.textalign = 0.5
    style.js_prompt_label.textalign = 0.5

    style.js_frame.xfill = True
    style.js_frame.yminimum = 0.5
    style.js_frame.xmargin = .1

    style.js_frame_vbox.xpos = 0.5
    style.js_frame_vbox.xanchor = 0.5
    style.js_frame_vbox.ypos = 0.5
    style.js_frame_vbox.yanchor = 0.5

    style.soundtest_button.activate_sound = None

    ######################################################################
    # Skip indicator.

    style.skip_indicator.xpos = 10
    style.skip_indicator.ypos = 10

    ######################################################################
    # Error messages.

    style.error_root.background = Solid((220, 220, 255, 255))
    style.error_root.xfill = True
    style.error_root.yfill = True
    style.error_root.xpadding = 20
    style.error_root.ypadding = 20

    style.error_title.color = (255, 128, 128, 255)

    style.error_body.color = (128, 128, 255, 255)


    ######################################################################
    # Compatibility names for renamed styles.
    style.file_picker_window_vbox = style.file_picker_frame_vbox
    style.prefs_window = style.prefs_frame
    style.mm_root_window = style.mm_root
    style.file_picker_window = style.file_picker_frame
    style.prefs_pref = style.prefs_pref_frame
    style.gm_root_window = style.gm_root
    style.yesno_window_vbox = style.yesno_frame_vbox
    style.joyprompt_label = style.js_prompt_label
    style.gm_nav_window = style.gm_nav_frame
    style.joy_window = style.js_frame
    style.mm_menu_window = style.mm_menu_frame
    style.error_window = style.error_root
    style.joyfunc_label = style.js_function_label
    style.joy_vbox = style.js_frame_vbox
    style.yesno_window = style.yesno_frame
    style.mm_menu_window_vbox = style.mm_menu_frame_vbox
