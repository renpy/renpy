# This file is responsible for creating and defining the default styles
# used by the system.

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

        style.create('say_label', 'default',
                     'The style that the label text of a two-argument say statement is in.')

        style.create('say_dialogue', 'default',
                     'The style that the dialogue text of a two-argument say statement is in.')

        style.create('say_thought', 'default',
                     'The style that that the text of a one-argument say statement is in.')


        style.create('menu_caption', 'default',
                     'The style that menu captions are styled in.')

        style.create('menu_choice_selected', 'default',
                     'The style that selected menu choices are rendered in.')

        style.menu_choice_selected.color = (255, 255, 0, 255) # yellow

        style.create('menu_choice_unselected', 'default',
                     'The style that unselected menu choices are rendered in.')

        style.menu_choice_unselected.color = (0, 255, 255, 255) # cyan

        style.create('window', 'default',
                     'The base style for large windows that have content in them.')

        style.window.background = renpy.Solid((0, 0, 128, 128))
        style.window.xpadding = 10
        style.window.ypadding = 5
        style.window.xmargin = 10
        style.window.ymargin = 5
        style.window.xpos = 0
        style.window.ypos = 0
        style.window.xfill = True
        style.window.yfill = False
        style.window.xminimum = 0 # Includes margins and padding.
        style.window.yminimum = 150 # Includes margins and padding.

        style.create('window_say', 'window',
                     'The default style for windows containing dialogue.')

        style.create('window_menu', 'window',
                     'The default style for windows containing a menu.') 
                   
        print "Finished loading styles."
