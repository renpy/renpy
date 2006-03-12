# This is the config module, where game configuration settings are stored.
# This includes both simple settings (like the screen dimensions) and
# methods that perform standard tasks, like the say and menu methods.

# This will be deleted by the end of this file.
import renpy

# The title of the game window.
window_title = "A Ren'Py Game"

# An image file containing the window icon image.
window_icon = None

# The width and height of the drawable area of the screen.
screen_width = 800
screen_height = 600

# The background color.
background = None # (0, 0, 0, 255)

# Turns recoverable errors into fatal ones, so that the user can know
# about and fix them.
debug = False

# Ditto, but for sound operations
debug_sound = False

# Is rollback enabled? (This only controls if the user-invoked
# rollback command does anything)
rollback_enabled = True

# If the rollback is longer than this, we may trim it.
rollback_length = 128

# The maximum number of steps the user can rollback the game,
# interactively.
hard_rollback_limit = 100

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

# The number of screens worth of images that are allowed to live in the image
# cache at once.
image_cache_size = 8

# The number of statements we will analyze when doing predictive
# loading. Please note that this is a total number of statements in a
# BFS along all paths, rather than the depth along any particular
# path. The current node is counted in this number.
predict_statements = 16

# Causes the contents of the image cache to be printed to stdout when
# it changes.
debug_image_cache = False

# Should we allow skipping at all?
allow_skipping = True

# Should we allow fast skipping?
fast_skipping = False

# Are we currently skipping? If so, how fast?
# May be "slow", "fast", or None.
skipping = None

# The delay while we are skipping say statements.
skip_delay = 75

# Archive files that are searched for images.
archives = [ ]

# Searchpath.
searchpath = [ ]

# If True, we will only try loading from archives.
# Only useful for debugging Ren'Py, don't document.
force_archives = False

# An image file containing the mouse cursor, if one is defined.
mouse = None

# The default sound playback sample rate.
sound_sample_rate = 44100

# The amount of time music is faded out between tracks.
fade_music = 0.0

# Should the at list be sticky?
sticky_positions = False

# A list of all of the layers that we know about.
layers = [ 'master', 'transient', 'overlay' ]

# A list of layers that should be cleared when we replace
# transients.
transient_layers = [ 'transient' ]

# A list of layers that should be cleared when we recompute
# overlays.
overlay_layers = [ 'overlay' ]

# A list of layers that are displayed above all other layers.
top_layers = [ ]

# True if we want to show overlays during wait statements, or
# false otherwise.
overlay_during_with = True

# True if we want to allow the fast dissolve.
enable_fast_dissolve = True

# When using the keyboard to navigate, how much we penalize
# distance out of the preferred direction.
focus_crossrange_penalty = 1024

# If True, then we force all loading to occur before transitions
# start.
load_before_transition = True

# The keymap that is used to change keypresses and mouse events.
keymap = dict(
    
    # Bindings present almost everywhere, unless explicitly
    # disabled.
    rollback = [ 'K_PAGEUP', 'mousedown_4', 'joy_rollback' ],
    screenshot = [ 's' ],
    toggle_fullscreen = [ 'f' ],
    toggle_music = [ 'm' ],
    game_menu = [ 'K_ESCAPE', 'mouseup_3', 'joy_menu' ],
    hide_windows = [ 'mouseup_2', 'h', 'joy_hide' ],
    launch_editor = [ 'E' ],

    # Say.
    rollforward = [ 'mousedown_5', 'K_PAGEDOWN' ],
    dismiss = [ 'mouseup_1', 'K_RETURN', 'K_SPACE', 'K_KP_ENTER', 'joy_dismiss' ],

    # Focus.
    focus_left = [ 'K_LEFT', 'K_KP_LEFT', 'joy_left' ],
    focus_right = [ 'K_RIGHT', 'K_KP_RIGHT', 'joy_right' ],
    focus_up = [ 'K_UP', 'K_KP_UP', 'joy_up' ],
    focus_down = [ 'K_DOWN', 'K_KP_DOWN', 'joy_down' ],
        
    # Button.
    button_select = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],

    # Input.
    input_backspace = [ 'K_BACKSPACE' ],
    input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],

    # These keys control skipping.
    skip = [ 'K_LCTRL', 'K_RCTRL', 'joy_holdskip' ],
    toggle_skip = [ 'K_TAB', 'joy_toggleskip' ],
    fast_skip = [ '>' ],

    # These control the bar.
    bar_activate = [ 'mousedown_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
    bar_deactivate = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
    bar_decrease = [ 'K_LEFT', 'joy_left' ],
    bar_increase = [ 'K_RIGHT', 'joy_right' ],
    )

# Should we try to support joysticks?
joystick = True

# A list of functions that are called when an interaction is started or
# restarted.
interact_callbacks = [ ]

# A list of functions that are called when an interaction is started.
start_interact_callbacks = [ ]

# A list of functions that are called when a say statement is sustained.
say_sustain_callbacks = [ ]

# A function that is called to tokenize text.
text_tokenizer = renpy.display.text.text_tokenizer

# The number of characters per AFM time period.
afm_characters = 250

# The number of bonus characters to add to a string for afm.
afm_bonus = 25

# A function that must return True for afm mode to forward.
afm_callback = None

# The amount of time we delay before making an automatic choice from a
# menu. This can be used for making a demo version of a game. It
# should be set to None in a deployed game.
auto_choice_delay = None

# A map from font, bold, italic to font, bold, italic. This is used
# to replace (say) the italic version of a regular font with the regular
# version of an italic font.
font_replacement_map = { }

# A callback that is called when a with statement (but not the with
# clause of a say or menu statement) executes. If not None, it's
# called with a single argument, the transition supplied to the with
# clause.
with_callback = None

# The framerate limit.
framerate = None

# The number of frames that Ren'Py has shown.
frames = 0

# A text editor that is launched at the location of the current
# statement.
editor = None

# Enable developer mode?
developer = False

# A logfile that logging messages are sent to.
log = None

del renpy

def backup():
    global _globals
    _globals = globals().copy()

    del _globals["backup"]
    del _globals["reload"]
    del _globals["__builtins__"]

def reload():
    import copy
    globals().update(_globals)

    for k, v in _globals.items():

        try:
            v = copy.deepcopy(v)
        except:
            pass

        globals()[k] = v
