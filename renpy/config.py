# This is the config module, where game configuration settings are stored.
# This includes both simple settings (like the screen dimensions) and
# methods that perform standard tasks, like the say and menu methods.

import renpy.display

# Setting that may only be changed in init blocks are marked with an
# (init) tag.

# The width and height of the drawable area of the screen. (init)
screen_width = 800
screen_height = 600

# Should the display be forced to be fullscreen?
fullscreen = None


# The default font for text.
text_font = "FreeSans.ttf"

# The defaut size for text.
text_size = 22

# The default color for text (RGBA)
text_color = ( 255, 255, 255, 255 )

# The drop-shadow offset. None means no drop shadow.
text_dropshadow_offset = ( 2, 2 )

# The color of the drop-shadow (RGBA)
text_dropshadow_color = (0, 0, 0, 128)

# The color of unselected choices in a menu.
menu_unselected_color = (128, 255, 255, 255)

# The color of selected choices in a menu.
menu_selected_color = (255, 255, 128, 255)




# The maximum number of statements of rollback that will be kept before
# the log is pruned.
rollback_maximum = 110

# The amount that the rollback log is pruned by.
rollback_prune = 10

# Is rollback enabled? (This only controls if the user-invoked
# rollback command does anything)
rollback_enabled = True

# A list of Displayables that should always be added to the end
# of the scene list.
overlay = [ ]

# A list of Displayables that should always be added to the start
# of the scene list. (Mostly used for keymaps and the like.)
underlay = [ ]

# True to enable profiling.
profile = False


def finish():
    """
    Called when we're finished initializing, in order to prevent
    circular dependencies.
    """

    import renpy.display.image

    global say_window_properties

    # A set of window properties that will be use for the background of
    # the say window.
    say_window_properties = dict(
        background = renpy.display.image.Solid((0, 0, 128, 128)),
        xpadding = 10,
        ypadding = 5,
        xmargin = 10,
        ymargin = 5,
        xfill = True,
        yfill = False,
        yminimum = 150
        )

    global menu_window_properties

    # A set of window properties that will be use for the background of
    # the menu window.
    menu_window_properties = dict(
        background = renpy.display.image.Solid((0, 0, 128, 128)),
        xpadding = 10,
        ypadding = 5,
        xmargin = 10,
        ymargin = 5,
        xfill = True,
        yfill = False,
        yminimum = 150
        )
    
    
