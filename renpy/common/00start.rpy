# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

##############################################################################
# Code that originated in 00mainmenu.rpy

init -1600 python hide:

    # menus: Music to play at the main menu.
    config.main_menu_music = None

    # advanced: Callbacks to run at start.
    config.start_callbacks = [ ]

    # Transition that's used after the game is loaded.
    config.after_load_transition = None

    # menus: Transition that's used at the end of the splash screen, when
    # it is shown.
    config.end_splash_transition = None

    # Should we start the game with scene black or just scene?
    config.start_scene_black = False

    # A save to automatically load, if it exists.
    config.auto_load = None

    # The language we use when the game starts. None remembers the user's
    # choice of language, and defaults to the game's native language.
    config.language = None

init -1600 python:

    def _init_language():

        import os

        if "RENPY_LANGUAGE" in os.environ:
            language = os.environ["RENPY_LANGUAGE"]
        elif config.language is not None:
            language = config.language
        else:
            language = _preferences.language

        renpy.change_language(language)

# This fixes up the context, if necessary, then calls the real
# after_load.
label _after_load:
    $ renpy.context()._menu = False
    $ renpy.context()._main_menu = False
    $ main_menu = False
    $ _in_replay = None

    if config.after_load_transition:
        $ renpy.transition(config.after_load_transition, force=True)

    if renpy.has_label("after_load"):
        jump expression "after_load"
    else:
        return

# Common code for _start and _start_memory.
label _start_store:

    python hide:
        store.main_menu = False
        renpy.context()._menu = False
        renpy.context()._main_menu = False

        for i in config.start_callbacks:
            i()

    return


# Starts up a memory. This is called by renpy.game.call_memory, and
# is expected to be called with _in_memory set.
label _start_replay:

    call _start_store

    if config.start_scene_black:
        scene black
    else:
        scene

    $ renpy.block_rollback()

    jump expression _in_replay

# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    call _start_store

    $ _init_language()
    $ renpy.block_rollback()

    call _gl_test
    call _load_reload_game from _call__load_reload_game_1

    if not _restart and config.auto_load and renpy.can_load(config.auto_load):
        $ renpy.load(config.auto_load)

    if config.start_scene_black:
        scene black
    else:
        scene

    if not _restart:
        $ ui.pausebehavior(0)
        $ ui.interact(suppress_underlay=True, suppress_overlay=True)

    $ renpy.block_rollback()

    $ _old_game_menu_screen = _game_menu_screen
    $ _old_predict_screens = _predict_screens
    $ _game_menu_screen = None
    $ _predict_screens = [ 'main_menu' ]

    if renpy.has_label("splashscreen") and not _restart:
        call expression "splashscreen" from _call_splashscreen_1

    $ _game_menu_screen = _old_game_menu_screen
    $ del _old_game_menu_screen

    $ renpy.block_rollback()

    if config.main_menu_music:
        $ renpy.music.play(config.main_menu_music, if_changed=True)
    else:
        $ renpy.music.stop()

    $ renpy.music.stop(channel="movie")

    # Clean out any residual scene from the splashscreen.
    if config.start_scene_black:
        scene black
    else:
        scene


    # This has to be python, to deal with a case where _restart may
    # change across a shift-reload.
    python:
        if _restart is None:
            renpy.transition(config.end_splash_transition)
        else:
            renpy.transition(_restart[0])
            renpy.jump(_restart[1])

label _invoke_main_menu:

    # Again, this has to be python.
    python:
        if _restart:
            renpy.call_in_new_context(_restart[2])
        else:
            renpy.call_in_new_context("_main_menu")


    # If the main menu returns, then start the game.
    jump start

# At this point, we've been switched into a new context. So we
# initialize it.
label _main_menu(_main_menu_screen="_main_menu_screen"):

    $ _enter_menu()

    python:
        renpy.dynamic("_load_prompt")
        _load_prompt = False

        renpy.context()._main_menu = True
        store.main_menu = True

    jump expression _main_menu_screen

# This is called to show the main menu to the user.
label _main_menu_screen:

    # Let the user give code that runs in the main menu context before
    # the main menu runs.
    if renpy.has_label("before_main_menu"):
        call expression "before_main_menu"

    # Let the user completely override the main menu. (But please note
    # it still lives in the menu context, rather than the game context.)
    if renpy.has_label("main_menu"):
        jump expression "main_menu"

    # New name.
    elif renpy.has_label("main_menu_screen"):
        jump expression "main_menu_screen"

    # Compatibility name.
    elif renpy.has_label("_library_main_menu"):
        jump expression "_library_main_menu"

    return
