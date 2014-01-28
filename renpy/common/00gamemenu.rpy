# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains functions relevant to the game menu.

init -1700 python:

    ######################################################################
    # First up, we define a bunch of configuration variables, which the
    # user can change.

    # menus: Music to play when entering the game menu.
    config.game_menu_music = None

    # menus: Sound played when entering the library without clicking a
    # button.
    config.enter_sound = None

    # menus: Sound played when leaving the library without clicking a
    # button.
    config.exit_sound = None

    # menus: Transition that occurs when entering the game menu.
    config.enter_transition = None

    # menus: Transition that occurs when leaving the game menu.
    config.exit_transition = None

    # menus: Transition that's used when going from one screen to another.
    config.intra_transition = None

    # menus: Transition that's used when going from the main to the game
    # menu.
    config.main_game_transition = None

    # menus: Transition that's used when going from the game to the main
    # menu.
    config.game_main_transition = None

    # menus: Transition that's used at the end of the game, when returning
    # to the main menu.
    config.end_game_transition = None

    # basics: True if autosave should be used.
    config.has_autosave = True

    # basics: True if quicksave has been enabled.
    config.has_quicksave = True

    # A list of layers to clear when entering the main and game menus.
    config.clear_layers = [ ]

    # The _window_subtitle used inside menus.
    config.menu_window_subtitle = ''

    # Layers to clear when entering the menus.
    config.menu_clear_layers = [ ]

    # What we do on a quit, by default.
    config.quit_action = ui.gamemenus("_quit_prompt")

    # What we do on a game menu invokcation.
    config.game_menu_action = None

    # The screen that we go to when entering the game menu.
    _game_menu_screen = None

    def _enter_menu():
        config.skipping = None

        renpy.movie_stop(only_fullscreen=True)
        if not renpy.context()._menu:
            renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))

        for i in config.menu_clear_layers:
            renpy.scene(layer=i)

        renpy.context()._menu = True
        renpy.context()._main_menu = main_menu

        renpy.context_dynamic("main_menu")
        renpy.context_dynamic("_window_subtitle")
        renpy.context_dynamic("_window")

        store._window_subtitle = config.menu_window_subtitle
        store._window = False

        store.mouse_visible = True
        store.suppress_overlay = True
        ui.clear()

        for i in config.clear_layers:
            renpy.scene(layer=i)

    def _invoke_game_menu():
        if renpy.context()._menu:
            if renpy.context()._main_menu:
                return
            else:
                renpy.jump("_noisy_return")
        else:
            if config.game_menu_action:
                renpy.display.behavior.run(config.game_menu_action)
            else:
                renpy.call_in_new_context('_game_menu')


# Run at the end of init, to set up autosaving based on the user's
# choices.
init 1700 python:

    if config.has_autosave:
        config.autosave_slots = 10
    else:
        config.autosave_frequency = None

# Factored this all into one place, to make our lives a bit easier.
label _enter_game_menu:
    $ _enter_menu()

    $ renpy.transition(config.enter_transition)

    if renpy.has_label("enter_game_menu"):
        call expression "enter_game_menu" from _call_enter_game_menu_1

    if config.game_menu_music:
        $ renpy.music.play(config.game_menu_music, if_changed=True)

    return

# Entry points from the game into menu-space.
label _game_menu(_game_menu_screen=_game_menu_screen, *args, **kwargs):
    if not _game_menu_screen:
        return

    $ renpy.play(config.enter_sound)

    call _enter_game_menu from _call__enter_game_menu_0

    if renpy.has_label("game_menu"):
        jump expression "game_menu"

    if renpy.has_screen(_game_menu_screen):
        $ renpy.show_screen(_game_menu_screen, *args, **kwargs)
        $ ui.interact()
        jump _noisy_return

    jump expression _game_menu_screen

label _game_menu_save:
    call _enter_game_menu from _call__enter_game_menu_1

    if renpy.has_label("_save_screen"):
        jump expression "_save_screen"
    else:
        jump expression "save_screen"

label _game_menu_load:
    call _enter_game_menu from _call__enter_game_menu_2

    if renpy.has_label("_load_screen"):
        jump expression "_load_screen"
    else:
        jump expression "load_screen"

label _game_menu_preferences:
    call _enter_game_menu from _call__enter_game_menu_3

    if renpy.has_label("_prefs_screen"):
        jump expression "_prefs_screen"
    else:
        jump expression "preferences_screen"

label _quit:
    if renpy.has_label("quit"):
        call expression "quit"
    $ renpy.quit()

label _return_fast_skipping:
    $ config.skipping = "fast"
    jump _return

label _return_skipping:
    $ config.skipping = "slow"
    jump _return

# Make some noise, then return.
label _noisy_return:
    $ renpy.play(config.exit_sound)

# Return to the game.
label _return:

    if renpy.context()._main_menu:
        $ renpy.transition(config.game_main_transition)
        jump _main_menu_screen

    $ renpy.transition(config.exit_transition)

    return

label _confirm_quit:

    if renpy.has_label("confirm_quit"):
        jump expression "confirm_quit"
    elif renpy.has_label("_compat_confirm_quit"):
        jump expression "_compat_confirm_quit"
    else:
        jump expression "_quit_prompt"
