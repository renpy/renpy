# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This is the config module, where game configuration settings are stored.
# This includes both simple settings (like the screen dimensions) and
# methods that perform standard tasks, like the say and menu methods.

# This will be deleted by the end of this file.
import renpy
import sets
import os

# Can we add more config variables?
locked = False

# Contains help for config variables.
help = [ ]

# basics: The title of the game window.
window_title = "A Ren'Py Game"

# basics: An image file containing the window icon image.
window_icon = None

# basics: The width and height of the drawable area of the screen.
screen_width = 800
screen_height = 600

# advanced: Should sound be enabled?
sound = True

# advanced: Turns recoverable errors into fatal ones, so that the user can know
# about and fix them.
debug = False

# advanced: Ditto, but for sound operations
debug_sound = False

# advanced: Is rollback enabled? (This only controls if the user-invoked
# rollback command does anything)
rollback_enabled = True

# advanced: If the rollback is longer than this, we may trim it.
rollback_length = 128

# advanced: The maximum number of steps the user can rollback the game,
# interactively.
hard_rollback_limit = 100

# advanced: A list of functions returning lists of displayables that will be
# added to the end of the display list.
overlay_functions = [ ]

# advanced: A list of Displayables that should always be added to the start
# of the scene list. (Mostly used for keymaps and the like.)
underlay = [ ]

# advanced: True to enable profiling.
profile = False

# advanced: The directory save files will be saved to.
savedir = None

# advanced: The number of screens worth of images that are allowed to
# live in the image cache at once.
image_cache_size = 8

# advanced: The number of statements we will analyze when doing predictive
# loading. Please note that this is a total number of statements in a
# BFS along all paths, rather than the depth along any particular
# path. The current node is counted in this number.
predict_statements = 16

# advanced: Causes the contents of the image cache to be printed to stdout when
# it changes.
debug_image_cache = False

# advanced: Should we allow skipping at all?
allow_skipping = True

# advanced: Should we allow fast skipping?
fast_skipping = False

# advanced: Are we currently skipping? If so, how fast?
# May be "slow", "fast", or None.
skipping = None

# advanced: The delay while we are skipping say statements.
skip_delay = 75

# basic: Archive files that are searched for images.
archives = [ ]

# advanced: Searchpath.
searchpath = [ ]

# advanced: If True, we will only try loading from archives.
# Only useful for debugging Ren'Py, don't document.
force_archives = False

# advanced: Used to control the software mouse cursor.
mouse = None

# advanced: The default sound playback sample rate.
sound_sample_rate = 44100

# advanced: The amount of time music is faded out between tracks.
fade_music = 0.0

# advanced: Should the at list be sticky?
sticky_positions = False

# advanced: A list of all of the layers that we know about.
layers = [ 'master', 'transient', 'overlay' ]

# advanced: A list of layers that should be cleared when we replace
# transients.
transient_layers = [ 'transient' ]

# advanced: A list of layers that should be cleared when we recompute
# overlays.
overlay_layers = [ 'overlay' ]

# advanced: A list of layers that are displayed atop all other layers, and do
# not participate in transitions.
top_layers = [ ]

# advanced: True if we want to show overlays during wait statements, or
# false otherwise.
overlay_during_with = True

# True if we want to allow the fast dissolve.
enable_fast_dissolve = True

# advanced: When using the keyboard to navigate, how much we penalize
# distance out of the preferred direction.
focus_crossrange_penalty = 1024

# advanced: If True, then we force all loading to occur before transitions
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
    dump_styles = [ 'Y' ],
    reload_game = [ 'R' ],
    inspector = [ 'I' ],
    developer = [ 'D' ],
    
    # Say.
    rollforward = [ 'mousedown_5', 'K_PAGEDOWN' ],
    dismiss = [ 'mouseup_1', 'K_RETURN', 'K_SPACE', 'K_KP_ENTER', 'joy_dismiss' ],

    # Pause.
    dismiss_hard_pause = [ ],
    
    # Focus.
    focus_left = [ 'K_LEFT', 'joy_left' ],
    focus_right = [ 'K_RIGHT', 'joy_right' ],
    focus_up = [ 'K_UP', 'joy_up' ],
    focus_down = [ 'K_DOWN', 'joy_down' ],
        
    # Button.
    button_select = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],

    # Input.
    input_backspace = [ 'K_BACKSPACE' ],
    input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],

    # Viewport.
    viewport_up = [ 'mousedown_4' ],
    viewport_down = [ 'mousedown_5' ],
    viewport_drag_start = [ 'mousedown_1' ],
    viewport_drag_end = [ 'mouseup_1' ],
    
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

# advanced: Should we try to support joysticks?
joystick = True

# advanced: A list of functions that are called when an interaction is
# started or restarted.
interact_callbacks = [ ]

# advanced: A list of functions that are called when an interaction is started.
start_interact_callbacks = [ ]

# advanced: A list of functions that are called when a say statement
# is sustained.
say_sustain_callbacks = [ ]

# advanced: A function that is called to see if say should allow
# itself to be dismissed.
say_allow_dismiss = None

# advanced: A function that is called to tokenize text.
text_tokenizer = renpy.display.text.text_tokenizer

# advanced: The number of characters per AFM time period.
afm_characters = 250

# advanced: The number of bonus characters to add to a string for afm.
afm_bonus = 25

# advanced: A function that must return True for afm mode to forward.
afm_callback = None

# advanced: The amount of time we delay before making an automatic
# choice from a menu. This can be used for making a demo version of a
# game. It should be set to None in a deployed game.
auto_choice_delay = None

# advanced: A map from font, bold, italic to font, bold, italic. This is used
# to replace (say) the italic version of a regular font with the regular
# version of an italic font.
font_replacement_map = { }

# advanced: A callback that is called when a with statement (but not
# the with clause of a say or menu statement) executes. If not None,
# it's called with a single argument, the transition supplied to the
# with clause.
with_callback = None

# advanced: The framerate limit, in frames per second.
framerate = None

# The number of frames that Ren'Py has shown.
frames = 0

# A text editor that is launched at the location of the current
# statement.
editor = os.environ.get('RENPY_EDITOR', None)

# basics: Enable developer mode?
developer = False

# advanced: A logfile that logging messages are sent to.
log = None

# advanced: Lint hooks.
lint_hooks = [ ]

# advanced: Hyperlink callback.
hyperlink_callback = None

# advanced: Hyperlink focus.
hyperlink_focus = None

# Should SFonts be recolored? internal.
recolor_sfonts = True

# advanced: Function that is called to layout text.
text_layout = renpy.display.text.text_layout

# advanced: A callback that is called 20 times a second.
periodic_callback = None

# A dictionary, mapping from style property to functions (which map
# arguments to values) or to None to indicate no such function is
# necessary.
style_properties = None

# Should we check that all style properties are in style_properties? (Internal)
check_properties = True

# advanced: If True, then we implicily do a with None after every interaction.
implicit_with_none = True

# advanced: A map from a layer to (x, y, w, h) tuples that the layer is clipped to.
layer_clipping = { }

# Should we disable the fullscreen optimization?
disable_fullscreen_opt = False

# Should we reject midi files?
reject_midi = True

# advanced: Default character callback.
character_callback = None

# advanced: Character callback list.
all_character_callbacks = [ ]

# basics: The number of autosave slots we have.
autosave_slots = 10

# basics: How often do we autosave. (Number of interactions, sort of.)
autosave_frequency = 200

# The callback that is used by the scene statement.
scene = renpy.exports.scene

# The callback that is used by the show statement.
show = renpy.exports.show

# The callback that is used by the hide statement.
hide = renpy.exports.hide

# Should we use cPickle or pickle for load/save?
use_cpickle = True

# The function to call as the inspector.
inspector = None

# Should we reject backslashes in filenames?
reject_backslash = True

# basics: Hide the mouse.
mouse_hide_time = 30

# advanced: Called when we can't load an image.
missing_image_callback = None

# advanced: Called to filter text in the say and menu statements.
say_menu_text_filter = None

# advanced: Used to replace one label with another.
label_overrides = { }

del renpy
del sets

def init():
    import renpy
    global properties
    style_properties = renpy.style.style_properties
