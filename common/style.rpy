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

init -1000:
    python hide:

        # Style Declarations #################################################

        style.create('default', None,
                     'The default style that all styles inherit from.')

        style.create('hbox', 'default', '(box) The base style for hboxen.')
        style.create('vbox', 'default', '(box) The base style for vboxen.')
        
        style.create('window', 'default', '(window) The base style for the windows that contain dialogue, thoughts, and menus.')
        style.create('frame', 'default', '(window) The base style for frames.')
        
        style.create('image_placement', 'default', 'This style is used to control the default placement of images on the screen.')

        style.create('image', 'default', 'This is the style of images themselves. Don\'t change this, change image_placement instead.')
        style.create('animation', 'default', 'This is the default style of animations. Don\'t change this, change image_placement instead.')

        # say
        style.create('say_label', 'default', '(text) The style that is used by default for the label of dialogue. The label is used to indicate who is saying something.')
        style.create('say_dialogue', 'default', "(text) The style that is used by default for the text of dialogue.")
        style.create('say_thought', 'default', "(text) The label that is used by default for the text of thoughts or narration, when no speaker is given.""")
        style.create('say_window', 'window', '(window) The default style for windows containing dialogue and thoughts.')
        style.create('say_who_window', 'window', '(window) The style used for the window containing the label, of a character with show_two_window set.')
        style.create('say_two_window_vbox', 'vbox', '(window) The style used for the containing vbox in dialogue for a character with two_window set.')
        style.create('say_vbox', 'vbox', '(box) The vbox containing the label (if present) and the body of dialogue and thoughts.')

        # menu
        style.create('menu', 'default', "(position) The style that is used for the vbox containing a menu.")
        style.create('menu_caption', 'default', "(text) The style that is used to render a menu caption.")
        style.create('menu_choice', 'default', "(text, hover) The style that is used to render the text of a menu choice.""")
        style.create('menu_choice_button', 'default', "(window, hover, sound) The style that is used to render the button containing a menu choice.")
        style.create('menu_choice_chosen', 'menu_choice', "(text, hover) The style that is used to render the text of a menu choice that has been chosen by the user sometime in the past.""")
        style.create('menu_choice_chosen_button', 'menu_choice_button', "(window, hover, sound) The style that is used to render the button containing a menu choice that has been chosen by the user sometime in the past.")
        style.create('menu_window', 'window', '(window) The default style for windows containing a menu.') 

        # input
        style.create('input_text', 'default', '(text) The style used for the text of an input box.')
        style.create('input_prompt', 'default', '(text) The style used for the prompt of an input box.')
        style.create('input_window', 'window', '(window) The style used for the window of an input box.')

        # centered
        style.create('centered_window', 'default', '(window) The style that is used for a "window" containing centered text.')
        style.create('centered_text', 'default', '(text) The style used for centered text.')

        # imagemap
        style.create('imagemap', 'image_placement', 'The style that is used for imagemaps.')
        style.create('imagemap_button', 'default', '(window, sound, hover) The style that is used for buttons inside imagemaps.')

        # imagebutton
        style.create('image_button', 'default', '(window, sound, hover) The default style used for image buttons.')
        style.create('image_button_image', 'default', 'The default style used for images inside image buttons.')

        # button
        style.create('button', 'default', '(window, sound, hover) The default style used for buttons in the main and game menus.')
        style.create('button_text', 'default', '(text, hover) The default style used for the label of a button.')
        style.create('menu_button', 'button', 'The base style for buttons that are part of the main or game menus.')
        style.create('menu_button_text', 'button_text', 'The base style for the label of buttons that are part of the main or game menus.')

        # bar
        style.create('bar', 'default', '(bar) The style that is used by default for bars.')
        
        # boxen used by the various menus.
        style.create('thin_hbox', 'hbox', '(box) A hbox with a small amount of spacing.')
        style.create('thick_hbox', 'hbox', '(box) A hbox with a large amount of spacing.')
        style.create('thin_vbox', 'vbox', '(box) A vbox with a small amount of spacing.')
        style.create('thick_vbox', 'vbox', '(box) A vbox with a large amount of spacing.')

        # Hyperlinks.
        style.create('hyperlink', 'default', 'The style of a hyperlink button.')
        style.create('hyperlink_text', 'default', 'The stype of hyperlink button text.')

# AUTOMATICALLY GENERATED
        style.create("gm_root", "default", "(window) The style used for the root window of the game menu. This is primarily used to change the background of the game menu.")
        style.create("gm_nav_frame", "default", "(window) The style used by a window containing buttons that allow the user to navigate through the different screens of the game menu.")
        style.create("gm_nav_vbox", "thin_vbox", "(box) The style that is used by the box inside the gm_nav_frame")
        style.create("gm_nav_button", "menu_button", "(window, hover) The style of a game menu navigation button.")
        style.create("gm_nav_button_text", "menu_button_text", "(text, hover) The style of the text of a  game menu navigation button.")
        style.create("file_picker_entry", "menu_button", "(window, hover) The style that is used for each of the slots in the file picker.")
        style.create("file_picker_entry_box", "thin_hbox", "(box) The style that is used for the hbox inside of a file picker entry.")
        style.create("file_picker_text", "default", "(text) A base style for all text that is displayed in the file picker.")
        style.create("file_picker_new", "file_picker_text", "(text) The style that is applied to the number of the new slot in the file picker.")
        style.create("file_picker_old", "file_picker_text", "(text) The style that is applied to the number of the old slot in the file picker.")
        style.create("file_picker_extra_info", "file_picker_text", "(text) The style that is applied to extra info in the file picker. The extra info is the save time, and the save_name if one exists.")
        style.create("file_picker_empty_slot", "file_picker_text", "(text) The style that is used for the empty slot indicator in the file picker.")
        style.create("file_picker_frame", "default", "(window) A window containing the file picker that is used to choose slots for loading and saving.")
        style.create("file_picker_frame_vbox", "thin_vbox", "(box) The vbox containing both the nav and the grid in the file picker.")
        style.create("file_picker_navbox", "thick_hbox", "(box) The box containing the naviation (next/previous) buttons in the file picker.")
        style.create("file_picker_nav_button", "menu_button", "(window, hover) The style that is used for enabled file picker navigation buttons.")
        style.create("file_picker_nav_button_text", "menu_button_text", "(text) The style that is used for the label of enabled file picker navigation buttons.")
        style.create("file_picker_grid", "default", "The style of the grid containing the file picker entries.")
        style.create("yesno_frame", "default", "(window) The style of a window containing a yes/no prompt.")
        style.create("yesno_frame_vbox", "thick_vbox", "(box) The style of a box containing the widgets in a yes/no prompt.")
        style.create("yesno_label", "default", "(text) The style used for the prompt in a yes/no dialog.")
        style.create("yesno_button", "menu_button", "(window, hover) The style of yes/no buttons.")
        style.create("yesno_button_text", "menu_button_text", "(window, hover) The style of yes/no button text.")
        style.create("error_root", "default", "(window) The style of the window containing internal error messages.")
        style.create("error_title", "default", "(text) The style of the text containing the title of an error message.")
        style.create("error_body", "default", "(text) The style of the body of an error message.")
        style.create("skip_indicator", "default", "(text) The style and placement of the skip indicator.")
        style.create("mm_root", "default", "(window) The style used for the root window of the main menu. This is primarily used to set a background for the main menu.")
        style.create("mm_menu_frame", "default", "(window) A window that contains the choices in the main menu. Change this to change the placement of these choices on the main menu screen.")
        style.create("mm_menu_frame_vbox", "thin_vbox", "(box) The vbox containing the main menu choices.")
        style.create("mm_button", "menu_button", "(window, hover) The style that is used on buttons that are part of the main menu.")
        style.create("mm_button_text", "menu_button_text", "(text, hover) The style that is used for the labels of buttons that are part of the main menu.")
        style.create("prefs_frame", "default", "(window) A window containing all preferences.")
        style.create("prefs_pref_frame", "default", "(window) A window containing an individual preference.")
        style.create("prefs_pref_vbox", "thin_vbox", "(box) The style of the vbox containing a preference.")
        style.create("prefs_label", "default", "(text) The style that is applied to the label of a block of preferences.")
        style.create("prefs_hbox", "default", "If config.hbox_pref_choices is True, the style of the hbox containing the choices.")
        style.create("prefs_button", "menu_button", "(window, hover) The style of an unselected preferences button.")
        style.create("prefs_button_text", "menu_button_text", "(text, hover) The style of the text of an unselected preferences button.")
        style.create("prefs_volume_slider", "prefs_slider", "(bar) The style that is applied to volume sliders.")
        style.create("soundtest_button", "prefs_button", "(window, hover) The style of a sound test button.")
        style.create("soundtest_button_text", "prefs_button_text", "(text, hover) The style of the text of a sound test  button.")
        style.create("prefs_slider", "bar", "(bar) The style that is applied to preference sliders.")
        style.create("prefs_spinner", "default", "The position of the prefs spinner.")
        style.create("prefs_spinner_label", "prefs_label", "(text) This is the style that displays the value of a preference spinner.")
        style.create("prefs_spinner_button", "prefs_button", "(window, hover) The style of the + or - buttons in a preference spinner.")
        style.create("prefs_spinner_button_text", "prefs_button_text", "(text, hover) The style of the text of the + and - buttons in a preference spinner.")
        style.create("prefs_js_frame", "prefs_pref_frame", "(window) The window containing a joystick mapping preference.")
        style.create("prefs_js_vbox", "prefs_pref_vbox", "(box) A vbox containing a joystick mapping preference.")
        style.create("prefs_js_button", "prefs_button", "(window, hover) The style of buttons giving a joystick mapping.")
        style.create("prefs_js_button_text", "prefs_button_text", "(text, hover) The style of the text in buttons giving a joystick mapping.")
        style.create("js_frame", "prefs_frame", "(window) The window containing the joystick message.")
        style.create("js_frame_vbox", "thick_vbox", "(window) The vbox containing the joistick mapping message.")
        style.create("js_function_label", "prefs_label", "(text, position) The style of the joystick mapping function name.")
        style.create("js_prompt_label", "prefs_label", "(text, position) The style of the joystick mapping prompt message.")
        style.create("prefs_jump", "prefs_pref_frame", "(window) The style of a window containing a jump preference.")
        style.create("prefs_jump_button", "prefs_button", "(window, hover) The style of a jump preference button.")
        style.create("prefs_jump_button_text", "prefs_button_text", "(text, hover) The style of jump preference button text.")
        style.create("prefs_column", "default", "The style of a vbox containing a column of preferences.")
        style.create("prefs_left", "prefs_column", "The position of the left column of preferences.")
        style.create("prefs_center", "prefs_column", "The position of the center column of preferences.")
        style.create("prefs_right", "prefs_column", "The position of the right column of preferences.")
        style.create("prefs_joystick", "prefs_center", "The position of the column of joystick preferences.")
# END AUTOMATICALLY GENERATED

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

        # Sound properties.
        style.default.sound = None

        # Box properties.
        style.default.box_spacing = 0
        style.default.box_first_spacing = None
        style.default.box_layout = None

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
        style.say_vbox.box_spacing = 10

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

        style.file_picker_text.size = 18
        style.file_picker_text.color = dark_cyan
        style.file_picker_text.hover_color = bright_cyan

        style.file_picker_new.hover_color = bright_red
        style.file_picker_new.idle_color = dark_red
        style.file_picker_new.minwidth = 30

        style.file_picker_old.minwidth = 30


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
