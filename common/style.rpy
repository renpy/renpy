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

init -250:
    python hide:

        style.create('default', None,
                     'The default style that all styles inherit from.')

        # Text properties.
        style.default.font = "Vera.ttf"
        style.default.size = 22
        style.default.color = (255, 255, 255, 255)
        style.default.drop_shadow = (2, 2)
        style.default.drop_shadow_color = (0, 0, 0, 128)
        style.default.minwidth = 0
        style.default.textalign = 0

        # Change this if you're not using Vera 22.
        if renpy.windows():
            style.default.line_height_fudge = -4
        else:
            style.default.line_height_fudge = 0
            
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

        # Sound properties.
        style.default.hover_sound = None
        style.default.activate_sound = None

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

        style.create('menu_caption', 'default',
                     """(text) The style that is used to render a menu
                     caption.""")

        style.create('menu_choice', 'default',
                     """(text, hover, sound) The style that is used to render a menu choice.""")

        style.menu_choice.hover_color = (255, 255, 0, 255) # yellow
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
                     '(sound, position) The style that is used for imagemaps.')

        # Style that is used by imagebutttons.
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
        style.button_text.color = (0, 255, 255, 255)
        style.button_text.hover_color = (128, 255, 255, 255)
        
        # Selected button.
        style.create('selected_button', 'button',
                     '(window, hover) The style that is used for a selected button (for example, the active screen or a chosen preference).')

        style.create('selected_button_text', 'button_text',
                     '(text, hover) The style that is used for the label of a selected button.')
                     
        style.selected_button_text.color = (255, 255, 0, 255)
        
        # Disabled button.

        style.create('disabled_button', 'button',
                     '(window, hover) The style that is used for a disabled button.')

        style.disabled_button.hover_sound = None
        style.disabled_button.activate_sound = None

        style.create('disabled_button_text', 'button_text',
                     '(text, hover) The style that is used for the label of a disabled button.')
                     
        style.disabled_button_text.color = (128, 128, 128, 255)

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


        style.create('file_picker_window', 'default',
                     '(window, position) A window containing the file picker that is used to choose slots for loading and saving.')

        style.file_picker_window.xpos = 10
        style.file_picker_window.xanchor = 'left'
        style.file_picker_window.ypos = 10
        style.file_picker_window.yanchor = 'top'


        style.create('file_picker_image', 'default')

        style.file_picker_image.xminimum = 280

        style.create('file_picker_entry', 'button',
                     '(window, hover) The style that is used for each of the slots in the file picker.')

        style.file_picker_entry.xpadding = 3
        style.file_picker_entry.xminimum = 500
        style.file_picker_entry.ymargin = 2
        
        style.file_picker_entry.idle_background = Solid((255, 255, 255, 255))
        style.file_picker_entry.hover_background = Solid((255, 255, 192, 255))

        style.create('file_picker_text', 'default',
                     '(text) A base style for all text that is displayed in the file picker.')
        
        style.file_picker_text.size = 18

        style.create('file_picker_new', 'file_picker_text',
                     '(text) The style that is applied to the new indicator in the file picker.')

        style.create('file_picker_old', 'file_picker_text',
                     '(text) The style that is applied to the old indicator in the file pciker.')

        style.file_picker_new.color = (255, 192, 192, 255)
        style.file_picker_old.color = (192, 192, 255, 255)
        style.file_picker_new.minwidth = 30
        style.file_picker_old.minwidth = 30

        style.create('file_picker_extra_info', 'file_picker_text',
                     '(text) The style that is applied to extra info in the file picker. The extra info is the save time, and the save_name if one exists.')

        style.file_picker_extra_info.color = (192, 192, 255, 255)

        style.create('file_picker_new_slot', 'file_picker_text',
                     '(text) The style that is used for the new slot indicator in the file picker.')


        style.create('yesno_prompt', 'default',
                     '(text, position) The style used for the prompt in a yes/no dialog.')

        style.yesno_prompt.xpos = 0.5
        style.yesno_prompt.xanchor = 'center'

        style.yesno_prompt.ypos = 0.25
        style.yesno_prompt.yanchor = 'center'

        style.create('yesno_yes', 'button',
                     '(position) The position of the yes button on the screen.')

        style.yesno_yes.xpos = 0.33
        style.yesno_yes.xanchor = 'center'
        style.yesno_yes.ypos = 0.33
        style.yesno_yes.yanchor = 'center'

        style.create('yesno_no', 'button',
                     '(position) The position of the no button on the screen.')

        style.yesno_no.xpos = 0.66
        style.yesno_no.xanchor = 'center'
        style.yesno_no.ypos = 0.33
        style.yesno_no.yanchor = 'center'
        

        # Preferences
        style.create('prefs_label', 'default',
                     '(text, position) The style that is applied to the label of a block of preferences.')

        style.prefs_label.xpos = 0.5
        style.prefs_label.xanchor = "center"

        style.create('prefs_pref', 'default',
                     '(position) The position of the box containing an individual preference.')

        style.prefs_pref.xpos = 0.5
        style.prefs_pref.xanchor = 'center'

        style.create('prefs_left', 'default',
                     '(position) The position of the left column of preferences.')

        style.prefs_left.xpos = 0.25
        style.prefs_left.xanchor = "center"
        style.prefs_left.ypos = 0.05
        style.prefs_left.yalign = "top"

        style.create('prefs_right', 'default',
                     '(position) The position of the right column of preferences.')

        style.prefs_right.xpos = 0.75
        style.prefs_right.xanchor = "center"
        style.prefs_right.ypos = 0.05
        style.prefs_right.yalign = "top"
        
