# This is the config module, where game configuration settings are stored.
# This includes both simple settings (like the screen dimensions) and
# methods that perform standard tasks, like the say and menu methods.

import renpy.display

# The title of the game window.
window_title = "A Ren'Py Game"

# The width and height of the drawable area of the screen.
screen_width = 800
screen_height = 600

# The background color.
background = None # (0, 0, 0, 255)

# Turns recoverable errors into fatal ones, so that the user can know
# about and fix them.
debug = False

# Is rollback enabled? (This only controls if the user-invoked
# rollback command does anything)
rollback_enabled = True

# If the rollback is longer than this, we may trim it.
rollback_length = 128

# The maximum number of steps the user can rollback the game,
# interactively.
hard_rollback_limit = 10

# A list of functions returning lists of displayables that will be
# added to the end of the display list.
overlay_functions = [ ]

# A list of Displayables that should always be added to the start
# of the scene list. (Mostly used for keymaps and the like.)
underlay = [ ]

# True to enable profiling.
profile = False

# The directory save files will be saved to.
savedir = None

# The number of images that are allowed to live in the image cache
# at once.
image_cache_size = 10

# The number of statements we will analyze when doing predictive
# loading. Please note that this is a total number of statements in a
# BFS along all paths, rather than the depth along any particular
# path. The current node is counted in this number.
predict_statements = 10

# Causes the contents of the image cache to be printed to stdout when
# it changes.
debug_image_cache = False

# The delay while we are skipping say statements.
skip_delay = 100

# Archive files that are searched for images.
archives = [ ]

# If True, we will only try loading from archives.
# Only useful for debugging Ren'Py, don't document.
force_archives = False

# An image file containing the mouse cursor, if one is defined.
mouse = None

# The distance the keyboard moves the mouse, per 50 ms tick, in pixels.
keymouse_distance = 5

# The default sound playback sample rate.
sound_sample_rate = 44100

# How fast text is displayed on the screen, by default.
annoying_text_cps = None

# The amount of time music is faded out between tracks.
fade_music = 0.0

_globals = globals().copy()

def reload():
    globals().update(_globals)
