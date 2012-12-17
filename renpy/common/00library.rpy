# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file consists of renpy functions that aren't expected to be
# touched by the user too much. We reserve the _ prefix for names
# defined in the library.

init -1700 python:

    # These are settings that the user can tweak to control the
    # look of the main menu and the load/save/escape screens.

    # basics: The version of Ren'Py this script is intended for, or
    # None if it's intended for the current version.
    config.script_version = None

    # basics: True if the skip indicator should be shown.
    config.skip_indicator = True

    # basics: The width of a thumbnail.
    config.thumbnail_width = 66

    # basics: The height of a thumbnail.
    config.thumbnail_height = 50
    
    # Layers to clear when entering the menus.
    config.menu_clear_layers = [ ]

    # Should we start the game with scene black or just scene?
    config.start_scene_black = False

    # This is updated to give the user an idea of where a save is
    # taking place.
    save_name = ''

    # A save to automatically load, if it exists.
    config.auto_load = None

    def _default_empty_window():
        
        who = _last_say_who

        if who is not None:
            who = eval(who)

        if who is None:
            who = narrator

        if isinstance(who, NVLCharacter):
            nvl_show_core()
        else:
            store.narrator("", interact=False)
                
    config.empty_window = _default_empty_window
        
    style.skip_indicator = Style(style.default, heavy=True, help='The skip indicator.')
    style.skip_indicator.xpos = 10
    style.skip_indicator.ypos = 10

    config.extend_interjection = "{fast}"

    def extend(what, interact=True):
        who = _last_say_who

        if who is not None:
            who = eval(who)

        if who is None:
            who = narrator 
            
        if isinstance(who, basestring):
            who = unknown.copy(who)

        # This ensures extend works even with NVL mode.
        who.do_extend()
            
        what = _last_say_what + config.extend_interjection + what
            
        renpy.exports.say(who, what, interact=interact)
        store._last_say_what = what
        
    extend.record_say = False

        
    _predict_screens = [ ]
        

    def skip_indicator():

        ### skip_indicator default
        # (text) The style and placement of the skip indicator.            

        if config.skip_indicator is True:

            if config.skipping == "slow" and config.skip_indicator:
                ui.text(_(u"Skip Mode"), style='skip_indicator')

            if config.skipping == "fast" and config.skip_indicator:
                ui.text(_(u"Fast Skip Mode"), style='skip_indicator')

            return

        if not config.skip_indicator:
            return

        if not config.skipping:
            return

        ui.add(renpy.easy.displayable(config.skip_indicator))

    config.overlay_functions.append(skip_indicator)

    # Prediction of screens.    
    def predict():

        for s in _predict_screens:
            if renpy.has_screen(s):
                renpy.predict_screen(s)

        s = _game_menu_screen

        if s is None:
            return

        if renpy.has_screen(s):
            renpy.predict_screen(s)
            return

        if s.endswith("_screen"):
            s = s[:-7]
            if renpy.has_screen(s):
                renpy.predict_screen(s)
                return

            
    config.predict_callbacks.append(predict)
            


    


init -1000:
    # Lock the library object.
    $ config.locked = True



        
##############################################################################
# Code that originated in 00gamemenu.rpy
init -1700 python:

    ######################################################################
    # First up, we define a bunch of configuration variable, which the
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

    # menus: Transition that's used at the end of the splash screen, when
    # it is shown.
    config.end_splash_transition = None

    # basics: True if autosave should be used.
    config.has_autosave = True

    # basics: True if quicksave has been enabled.
    config.has_quicksave = False

    # A list of layers to clear when entering the main and game menus.
    config.clear_layers = [ ]

    # The _window_subtitle used inside menus.
    config.menu_window_subtitle = ''
    
    # The screen that we go to when entering the game menu.
    _game_menu_screen = None
    
    # The language we use when the game starts. None remembers the user's
    # choice of language, and defaults to the game's native language.
    config.language = None
    
    def _enter_menu():
        config.skipping = None
        
        renpy.movie_stop(only_fullscreen=True)
        renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))

        for i in config.menu_clear_layers:
            renpy.scene(layer=i)
        
        renpy.context()._menu = True        
        renpy.context()._main_menu = False
        renpy.context_dynamic("main_menu")
        renpy.context_dynamic("_window_subtitle")
        renpy.context_dynamic("_window")
        
        store.main_menu = False
        store._window_subtitle = config.menu_window_subtitle
        store._window = False
        
        store.mouse_visible = True
        store.suppress_overlay = True
        ui.clear()

        for i in config.clear_layers:
            renpy.scene(layer=i)
        
    def _init_language():
        
        if "RENPY_LANGUAGE" in os.environ:
            language = os.environ["RENPY_LANGUAGE"]
        elif config.language is not None:
            language = config.language
        else:
            language = _preferences.language
        
        renpy.change_language(language)

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
init 1180 python:

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
label _game_menu(_game_menu_screen=_game_menu_screen):
    if not _game_menu_screen:
        return

    $ renpy.play(config.enter_sound)
    
    call _enter_game_menu from _call__enter_game_menu_0
    
    if renpy.has_label("game_menu"):
        jump expression "game_menu"

    if renpy.has_screen(_game_menu_screen):
        $ renpy.show_screen(_game_menu_screen)
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
    $ renpy.quit()

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


# After init, make some changes based on if config.developer is True.
init 1700 python hide:

    if config.developer:

        if config.debug_sound is None:
            config.debug_sound = True
        
        renpy.load_module("_developer")

# Entry point for the developer screen. The rest of it is loaded from
# _developer.rpym
label _developer:

    if not config.developer:
        return

    $ _enter_menu()

    jump expression "_developer_screen"


