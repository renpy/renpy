## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't
## uncomment them. Lines beginning with a single '#' mark are commented-out
## code, and you may want to uncomment them when appropriate.


## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("Old School High School")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "oshs"


## The version of the game.

define config.version = "1.0"


## Text that is placed on the game's about screen. To insert a blank line
## between paragraphs, write \n\n.

define gui.about = _("""\
Created by PyTom.

Backgrounds by Mugenjohncel.""")


###############################################################################
## Sounds and music


## These three variables control which mixers are shown to the player by
## default. Setting one of these to False will hide the appropriate mixer.

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
define config.sample_voice = "sample_voice.opus"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

# define config.main_menu_music = "main-menu-theme.ogg"


###############################################################################
## Transitions
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## A transition that is used after a game has been loaded.

define config.after_load_transition = None


## Used when entering the main menu after the game has ended.

define config.end_game_transition = None


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


###############################################################################
## Window management.

## This controls when the dialogue window is displayed. If "show", it is
## always displayed. If "hide", it is only displayed when dialogue is present.
## If "auto", the window is hidden before scene statements and shown again
## once dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "auto"


## Transitions used to show and hide the dialogue window

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


###############################################################################
## Preference defaults

## Controls the default text speed. The default, 0, is infinite, while any
## other number is the number of characters per second to type out.

default preferences.text_cps = 0


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


###############################################################################
## Save directory

## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "oshs-1466351223"



define gui.accent_color = '#000060'
define gui.idle_color = '#606060'
define gui.idle_small_color = '#404040'
define gui.hover_color = '#3284d6'
define gui.button_text_hover_color = '#3284d6'
define gui.selected_color = '#000060'
define gui.button_text_selected_color = '#000060'
define gui.insensitive_color = '#8888887f'
define gui.muted_color = '#6080d0'
define gui.hover_muted_color = '#8080f0'
define gui.text_color = '#402000'
define gui.interface_text_color = '#404040'
define gui.choice_idle_color = "#cccccc"
define gui.choice_hover_color = "#0066cc"

define gui.text_font = "ArchitectsDaughter.ttf"
define gui.name_text_font = "ArchitectsDaughter.ttf"
define gui.interface_text_font = "ArchitectsDaughter.ttf"
define gui.button_text_font = "ArchitectsDaughter.ttf"
define gui.slot_font = "ArchitectsDaughter.ttf"
define gui.glyph_font = "DejaVuSans.ttf"

define gui.button_height = 64
define gui.slider_size = 64

define gui.navigation_button_width = 290
define gui.radio_button_width = 300
define gui.check_button_width = 300

define gui.button_tile = True

define gui.button_borders = Borders(10, 10, 10, 10)
define gui.radio_button_borders = Borders(40, 10, 10, 10)
define gui.check_button_borders = Borders(40, 10, 10, 10)

define gui.page_button_width = 50
define gui.page_button_text_xalign = 0.5

define gui.confirm_button_width = 100



define gui.choice_button_tile = True
define gui.choice_button_borders = Borders(150, 7, 150, 10)
define gui.choice_button_text_font = gui.text_font

define gui.choice_button_text_idle_color = "#606060"
define gui.choice_button_text_hover_color = "#0066CC"

define gui.scrollbar_size = 24
define gui.scrollbar_tile = True

define gui.vscrollbar_borders = Borders(7, 10, 7, 10)

define gui.frame_borders = Borders(20, 20, 20, 20)
define gui.frame_tile = True

define gui.name_xalign = 0.5
define gui.name_xpos = 0.5
define gui.namebox_width = 300
define gui.name_ypos = -22
define gui.namebox_borders = Borders(15, 7, 15, 7)
define gui.namebox_tile = True

define gui.dialogue_ypos = 60
define gui.dialogue_xpos = 0.5
define gui.dialogue_text_xalign = 0.5


define gui.history_name_xpos = 0.5
define gui.history_name_xalign = 0.5

define gui.history_text_xpos = 0.5
define gui.history_text_ypos = 50
define gui.history_text_xalign = 0.5
