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

init -100:
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

        # The base style for the large windows.
        style.create('window', 'default',
                     '(window, placement) The base style for the windows that contain dialogue, thoughts, and menus.')
                     
        style.window.background = renpy.Solid((0, 0, 128, 128))
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

        style.create('image_placement', None,
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

        style.create('menu_selected', 'default',
                     """(text) The style that is used to render a
                     selected menu choice.""")

        style.menu_selected.color = (255, 255, 0, 255) # yellow

        style.create('menu_unselected', 'default',
                     """(text) The style that is used to render an
                     unselected menu choice.""")

        style.menu_unselected.color = (0, 255, 255, 255) # cyan

        style.create('menu_window', 'window',
                     '(window, position) The default style for windows containing a menu.') 

        # Styles that are used for windows that contain dialogue or
        # menus.


        # Styles that are used by all Buttons.
        style.create('button', 'default',
                     '(window, hover) The default style used for buttons in the main and game menus.')

        style.create('button_text', 'default',
                     '(text, hover) The default style used for the label of a button.')

        style.button_text.xpos = 0.0
        style.button_text.xanchor = 'left'
        style.button_text.size = 24
        style.button_text.color = (0, 255, 255, 255)
        
        # Selected button.
        style.create('selected_button', 'button',
                     '(window, hover) The style that is used for a selected button (for example, the active screen or a chosen preference).')

        style.create('selected_button_text', 'button_text',
                     '(text, hover) The style that is used for the label of a selected button.')
                     
        style.selected_button_text.color = (255, 255, 0, 255)
        
        # Disabled button.

        style.create('disabled_button', 'button',
                     '(window, hover) The style that is used for a disabled button.')

        style.create('disabled_button_text', 'button_text',
                     '(text, hover) The style that is used for the label of a disabled button.')
                     
        style.disabled_button_text.color = (128, 128, 128, 255)
        


        # Styles that are used when laying out the main menu.
        style.create('mm_root_window', 'default',
                     '(window) The style used for the root window of the main menu. This is primarily used to set a background for the main menu.')

        style.mm_root_window.background = renpy.Image("mainmenu.jpg")

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

        style.gm_root_window.background = renpy.Image("escapemenu.jpg")
    
        style.create('gm_nav_window', 'default',
                     '(window, placement) The style used by a window containing buttons that allow the user to navigate through the different screens of the game menu.')

        style.gm_nav_window.xpos = 0.95
        style.gm_nav_window.xanchor = 'right'
        style.gm_nav_window.ypos = 0.95
        style.gm_nav_window.yanchor = 'bottom'


        style.create('file_picker_window', 'default',
                     '(window, placement) A window containing the file picker that is used to choose slots for loading and saving.')

        style.file_picker_window.xpos = 10
        style.file_picker_window.xanchor = 'left'
        style.file_picker_window.ypos = 10
        style.file_picker_window.yanchor = 'top'


        style.create('file_picker_entry', 'button',
                     '(window, hover) The style that is used for each of the slots in the file picker.')

        style.file_picker_entry.xpadding = 3
        style.file_picker_entry.xminimum = 780
        style.file_picker_entry.ymargin = 5
        
        style.file_picker_entry.idle_background = renpy.Solid((255, 255, 255, 255))
        style.file_picker_entry.hover_background = renpy.Solid((255, 255, 192, 255))

        style.create('file_picker_text', 'default',
                     '(text) A base style for all text that is displayed in the file picker.')
        
        style.create('file_picker_new', 'file_picker_text',
                     '(text) The style that is applied to the new indicator in the file picker.')

        style.create('file_picker_old', 'file_picker_text',
                     '(text) The style that is applied to the old indicator in the file pciker.')

        style.file_picker_new.color = (255, 192, 192, 255)
        style.file_picker_old.color = (192, 192, 255, 255)
        style.file_picker_new.minwidth = 50
        style.file_picker_old.minwidth = 50

        style.create('file_picker_extra_info', 'file_picker_text',
                     '(text) The style that is applied to extra info in the file picker. The extra info is the save time, and the save_name if one exists.')

        style.file_picker_extra_info.color = (192, 192, 255, 255)

        style.create('file_picker_new_slot', 'file_picker_text',
                     '(text) The style that is used for the new slot indicator in the file picker.')

        style._write_docs("/tmp/style_docs.xml")
