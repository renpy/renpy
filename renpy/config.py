# This is the config module, where game configuration settings are stored.
# This includes both simple settings (like the screen dimensions) and
# methods that perform standard tasks, like the say and menu methods.

import renpy.display

# The title of the game window.
window_title = "A Ren'Py Game"

# The width and height of the drawable area of the screen.
screen_width = 800
screen_height = 600

# Should the display be forced to be fullscreen?
fullscreen = None

# Turns recoverable errors into fatal ones, so that the user can know
# about and fix them.
debug = False

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
