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

        style.create('default', None,
                     'The default style that all styles inherit from.')

        dark_cyan = (0, 192, 255, 255)
        bright_cyan = (0, 255, 255, 255)

        dark_red = (255, 128, 128, 255)
        bright_red = (255, 64, 64, 255)

        green = (0, 128, 0, 255)

        # Magic.
        style.default.enable_hover = True

        # Text properties.
        style.default.font = "Vera.ttf"
        style.default.antialias = True
        style.default.size = 22
        style.default.color = (255, 255, 255, 255)
        style.default.bold = False
        style.default.italic = False
        style.default.underline = False
        style.default.drop_shadow = (1, 1)
        style.default.drop_shadow_color = (0, 0, 0, 128)
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
        style.default.xpos = 0
        style.default.ypos = 0
        style.default.xanchor = 'left'
        style.default.yanchor = 'top'
        style.default.xmaximum = None
        style.default.ymaximum = None

        # Sound properties.
        style.default.sound = None

        # The base style for the large windows.
        style.create('window', 'default',
                     '(window, placement) The base style for the windows that contain dialogue, thoughts, and menus.')
                     
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
        style.window.xanchor = 'center'
        style.window.yanchor = 'bottom'

        # This style controls the default placement of images on the screen.

        style.create('image_placement', 'default',
                     'This style is used to control the default placement of images on the screen.')

        style.image_placement.xpos = 0.5
        style.image_placement.ypos = 1.0
        style.image_placement.xanchor = 'center'
        style.image_placement.yanchor = 'bottom'

        # Styles that are used for dialogue.

        style.create('say_label', 'default',
                     """(text) The style that is used by default for
                     the label of dialogue. The label is used to
                     indicate who is saying something.""")

        style.say_label.bold = True

        style.create('say_dialogue', 'default',
                     """(text) The style that is used by default for
                     the text of dialogue.""")

        style.create('say_thought', 'default',
                     """(text) The label that is used by default for
                     the text of thoughts or narration, when no
                     speaker is given.""")
                     
        style.create('say_window', 'window',
                     '(window, position) The default style for windows containing dialogue and thoughts.')


        # Styles that are used for menus.

        style.create('menu', 'default',
                     "(position) The style that is used for the vbox containing a menu.")

        style.create('menu_caption', 'default',
                     "(text) The style that is used to render a menu caption.")

        style.create('menu_choice', 'default',
                     """(text, hover) The style that is used to render
                        the text of a menu choice.""")

        style.create('menu_choice_button', 'default',
                     """(window, hover, sound) The style that is used
                        to render the button containing a menu choice.""")

        style.menu_choice.hover_color = (255, 255, 0, 255) # yellow
        style.menu_choice.activate_color = (255, 255, 0, 255) # yellow
        style.menu_choice.idle_color = (0, 255, 255, 255) # cyan

        style.create('menu_window', 'window',
                     '(window, position) The default style for windows containing a menu.') 

        # Styles that are used by input widgets.
        style.create('input_text', 'default',
                     '(text) The style used for the text of an input box.')

        style.input_text.color = (255, 255, 0, 255)

        style.create('input_prompt', 'default',
                     '(text) The style used for the prompt of an input box.')

        style.create('input_window', 'window',
                     '(window, position) The style used for the window of an input box.')

        # Styles used by centered.
        style.create('centered_window', 'default',
                     '(window) The style that is used for a "window" containing centered text.')

        style.create('centered_text', 'default',
                     '(text) The style used for centered text.')

        style.centered_window.xpos = 0.5
        style.centered_window.xanchor = 'center'
        style.centered_window.xfill = False
                      
        style.centered_window.ypos = 0.5
        style.centered_window.yanchor = 'center'
        style.centered_window.yfill = False

        style.centered_window.xpadding = 10

        style.centered_text.textalign = 0.5
        style.centered_text.xpos = 0.5
        style.centered_text.ypos = 0.5
        style.centered_text.xanchor = 'center'
        style.centered_text.yanchor = 'center'
           
        # Styles that are used by imagemaps
        style.create('imagemap', 'image_placement',
                     '(position) The style that is used for imagemaps.')

        style.create('imagemap_button', 'default',
                     '(window, sound, hover) The style that is used for buttons inside imagemaps.')

        # Styles that are used by imagebutttons.
        style.create('image_button', 'default',
                     '(window, sound, hover) The default style used for image buttons.')

        style.create('image_button_image', 'default',
                     'The default style used for images inside image buttons.')


        # Styles that are used by all other Buttons.
        style.create('button', 'default',
                     '(window, sound, hover) The default style used for buttons in the main and game menus.')

        style.button.xpos = 0.5
        style.button.xanchor = 'center'

        style.create('button_text', 'default',
                     '(text, hover) The default style used for the label of a button.')

        style.button_text.xpos = 0.5
        style.button_text.xanchor = 'center'
        style.button_text.size = 24
        style.button_text.color = dark_cyan
        style.button_text.hover_color = bright_cyan
        style.button_text.activate_color = bright_cyan
        style.button_text.insensitive_color = (192, 192, 192, 255)
        style.button_text.drop_shadow = (2, 2)
        
        # Selected button.
        style.create('selected_button', 'button',
                     '(window, hover) The style that is used for a selected button (for example, the active screen or a chosen preference).')

        style.create('selected_button_text', 'button_text',
                     '(text, hover) The style that is used for the label of a selected button.')
                     
        style.selected_button_text.color = dark_red
        style.selected_button_text.hover_color = bright_red
        style.selected_button_text.activate_color = bright_red
        
        # Bar.
        style.create('bar', 'default',
                     '(bar) The style that is used by default for bars.')

        style.bar.left_bar = Solid(bright_cyan)
        style.bar.right_bar = Solid((0, 0, 0, 128))

        # Styles that are used when laying out the main menu.
        style.create('mm_root_window', 'default',
                     '(window) The style used for the root window of the main menu. This is primarily used to set a background for the main menu.')

        style.mm_root_window.background = Solid((0, 0, 0, 255))

        style.create('mm_menu_window', 'default',
                     '(window, position) A window that contains the choices in the main menu. Change this to change the placement of these choices on the main menu screen.')

        style.mm_menu_window.xpos = 0.9
        style.mm_menu_window.xanchor = 'right'
        style.mm_menu_window.ypos = 0.9
        style.mm_menu_window.yanchor = 'bottom'

        style.create('mm_button', 'button',
                     '(window, hover) The style that is used on buttons that are part of the main menu.')

        style.create('mm_button_text', 'button_text',
                     '(text, hover) The style that is used for the labels of buttons that are part of the main menu.')

        # Styles that are used to lay out the game menu.

        style.create('gm_root_window', 'default',
                     '(window) The style used for the root window of the game menu. This is primarily used to change the background of the game menu.')

        style.gm_root_window.background = Solid((0, 0, 0, 255))
    
        style.create('gm_nav_window', 'default',
                     '(window, position) The style used by a window containing buttons that allow the user to navigate through the different screens of the game menu.')

        style.gm_nav_window.xpos = 0.9
        style.gm_nav_window.xanchor = 'right'
        style.gm_nav_window.ypos = 0.95
        style.gm_nav_window.yanchor = 'bottom'

        
        style.create('gm_nav_button', 'button',
                     '(window, hover) The style of an unselected game menu navigation button.')

        style.create('gm_nav_button_text', 'button_text',
                     '(text, hover) The style of the text of an unselected game menu navigation button.')

        style.create('gm_nav_selected_button', 'selected_button',
                     '(window, hover) The style of a selected game menu navigation button.')

        style.create('gm_nav_selected_button_text', 'selected_button_text',
                     '(text, hover) The style of the text of a selected game menu navigation button.')

        style.create('file_picker_window', 'default',
                     '(window, position) A window containing the file picker that is used to choose slots for loading and saving.')

        style.file_picker_window.xpos = 0
        style.file_picker_window.xanchor = 'left'
        style.file_picker_window.ypos = 0
        style.file_picker_window.yanchor = 'top'
        style.file_picker_window.xpadding = 5


        style.create('file_picker_navbox', 'default',
                     '(position) The position of the naviation (next/previous) buttons in the file picker.')

        style.file_picker_navbox.xmargin = 10

        style.create('file_picker_nav_button', 'button',
                     '(window, hover) The style that is used for enabled file picker navigation buttons.')

        style.create('file_picker_nav_button_text', 'button_text',
                     '(text) The style that is used for the label of enabled file picker navigation buttons.')        


        style.create('file_picker_grid', 'default',
                     '(position) The style of the grid containing the file picker entries.')

        style.file_picker_grid.xfill = True
                
        style.create('file_picker_entry', 'button',
                     '(window, hover) The style that is used for each of the slots in the file picker.')

        style.file_picker_entry.xpadding = 5
        style.file_picker_entry.ypadding = 2
        style.file_picker_entry.xmargin = 5
        style.file_picker_entry.xfill = True
        style.file_picker_entry.ymargin = 2
        
        style.file_picker_entry.background = Solid((255, 255, 255, 255))
        style.file_picker_entry.hover_background = Solid((255, 255, 192, 255))
        style.file_picker_entry.activate_background = Solid((255, 255, 192, 255))

        style.create('file_picker_text', 'default',
                     '(text) A base style for all text that is displayed in the file picker.')
        
        style.file_picker_text.size = 18
        style.file_picker_text.color = dark_cyan
        style.file_picker_text.hover_color = bright_cyan

        style.create('file_picker_new', 'file_picker_text',
                     '(text) The style that is applied to the new indicator in the file picker.')

        style.create('file_picker_old', 'file_picker_text',
                     '(text) The style that is applied to the old indicator in the file pciker.')

        style.file_picker_new.hover_color = bright_red
        style.file_picker_new.activate_color = bright_red
        style.file_picker_new.idle_color = dark_red
        style.file_picker_new.minwidth = 30
        style.file_picker_old.minwidth = 30

        style.create('file_picker_extra_info', 'file_picker_text',
                     '(text) The style that is applied to extra info in the file picker. The extra info is the save time, and the save_name if one exists.')

        style.create('file_picker_empty_slot', 'file_picker_text',
                     '(text) The style that is used for the empty slot indicator in the file picker.')

        style.create('yesno_label', 'default',
                     '(text, position) The style used for the prompt in a yes/no dialog.')

        style.yesno_label.color = green

        style.create('yesno_button', 'button',
                     '(window, hover) The style of yes/no buttons.')

        style.create('yesno_button_text', 'button_text',
                     '(window, hover) The style of yes/no button text.')
        
        style.create('yesno_window', 'default',
                     '(window) The style of a window containing a yes/no dialogue.')

        style.yesno_window.xfill = True
        style.yesno_window.yminimum = 0.5

        # Preferences


        style.create('prefs_pref', 'default',
                     '(window, position) The position of the box containing an individual preference.')

        style.prefs_pref.xpos = 0.5
        style.prefs_pref.xanchor = 'center'

        style.create('prefs_label', 'default',
                     '(text, position) The style that is applied to the label of a block of preferences.')

        style.prefs_label.xpos = 0.5
        style.prefs_label.xanchor = "center"
        style.prefs_label.color = green
        
        style.create('prefs_button', 'button',
                     '(window, hover) The style of an unselected preferences button.')

        style.prefs_button.xpos = 0.5
        style.prefs_button.xanchor = 'center'

        style.create('prefs_button_text', 'button_text',
                     '(text, hover) The style of the text of an unselected preferences button.')

        style.create('prefs_selected_button', 'selected_button',
                     '(window, hover) The style of a selected preferences button.')

        style.prefs_selected_button.xpos = 0.5
        style.prefs_selected_button.xanchor = 'center'

        style.create('prefs_selected_button_text', 'selected_button_text',
                     '(text, hover) The style of the text of a selected preferences button.')

        style.create('prefs_window', 'default',
                     '(window, position) A window containing all preferences.')

        style.prefs_window.xfill=True
        style.prefs_window.ypadding = 0.05
        
        style.create('skip_indicator', 'default',
                     '(text, position) The style of the text that is used to indicate that skipping is in progress.')

        style.skip_indicator.xpos = 10
        style.skip_indicator.ypos = 10

