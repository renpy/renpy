# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

    # Should we attempt to return to the menu we were on after a reload?
    config.reload_menu = True

    # Callbacks to run after load.
    config.after_load_callbacks = [ ]

    # Should we suppress overlay during the splashscreen?
    config.splashscreen_suppress_overlay = True

    # Should we profile reloading?
    config.profile_reload = False

    # When should start_store happen?
    config.early_start_store = False

init -1600 python:

    def _init_language():
        """
        Changes the default language. This is called automatically by
        Ren'Py as it starts up.
        """

        import os

        language = os.environ.get("RENPY_LANGUAGE") or config.language or _preferences.language

        renpy.change_language(language)

# This fixes up the context, if necessary, then calls the real
# after_load.
label _after_load:

    python:
        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None

        renpy.execute_default_statement(False)
        _init_language()

    python hide:

        for i in config.after_load_callbacks:
            i()

        if config.after_load_transition:
            renpy.transition(config.after_load_transition, force=True)

        if "_reload_time" in renpy.session:
            start = renpy.session.pop("_reload_time")
            import time

            if config.profile_reload:
                print("Reloading took:", time.time() - start, "seconds" )

        menu = renpy.session.pop("_reload_screen", None)

        if config.reload_menu and (menu is not None):
            renpy.run(ShowMenu(menu,
                *renpy.session.pop("_reload_screen_args", tuple()),
                **renpy.session.pop("_reload_screen_kwargs", { })
                ))

    if renpy.has_label("after_load"):
        jump expression "after_load"
    else:
        return

# Ditto, for warp.
label _after_warp:

    python:
        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None

    if renpy.has_label("after_warp"):
        jump expression "after_warp"
    else:
        return



# Common code for _start and _start_replay.
label _start_store:

    python hide:
        store.main_menu = False
        renpy.context()._menu = False
        renpy.context()._main_menu = False

        for i in config.start_callbacks:
            i()

    return


# Starts up a replay. This is called by renpy.game.call_replay, and
# is expected to be called with _in_replay True and
# renpy.execute_default_statement already called.
label _start_replay:

    call _start_store

    scene black

    $ _init_language()
    $ renpy.block_rollback(purge=True)

    jump expression _in_replay


label _splashscreen:

    python:

        if config.splashscreen_suppress_overlay:
            renpy.dynamic("suppress_overlay", "_confirm_quit")
            suppress_overlay = True
            _confirm_quit = False

        renpy.dynamic("_autosave")
        _autosave = False

    jump expression "splashscreen"


# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    if config.early_start_store:
        call _start_store

    python:
        renpy.execute_default_statement(True)

    if not config.early_start_store:
        call _start_store

    python:

        # Predict the main menu. When a load occurs, the loaded data will
        # overwrite the prediction requests.
        if renpy.has_screen("main_menu"):
            renpy.start_predict_screen("main_menu")

        renpy.block_rollback()

    scene black

    if not _restart:
        call _gl_test

    python hide:
        renpy.warp.warp()

    call _load_reload_game from _call__load_reload_game_1

    python hide:
        auto_load = renpy.os.environ.get("RENPY_AUTO_LOAD", config.auto_load)
        if not _restart and auto_load and renpy.can_load(auto_load):
            renpy.load(auto_load)

    if config.start_scene_black:
        scene black

    if not _restart:
        $ renpy.display.interface.with_none(overlay=False)

    $ renpy.block_rollback()

    $ _old_game_menu_screen = _game_menu_screen
    $ _game_menu_screen = None
    $ _old_history = _history
    $ _history = False

    if renpy.has_label("splashscreen") and (not _restart) and (not renpy.os.environ.get("RENPY_SKIP_SPLASHSCREEN", None)):
        call _splashscreen from _call_splashscreen_1

    $ _game_menu_screen = _old_game_menu_screen
    $ del _old_game_menu_screen
    $ _history = _old_history
    $ del _old_history

    $ renpy.block_rollback()

    if config.main_menu_music:
        $ renpy.music.play(config.main_menu_music, if_changed=True)
    else:
        $ renpy.music.stop()

    $ renpy.music.stop(channel="movie")

    scene black

    python:
        # Stop predicting the main menu, now that we're ready to show it.
        if renpy.has_screen("main_menu"):
            renpy.stop_predict_screen("main_menu")

        # Implement config.window
        _init_window()

    # This has to be Python, to deal with a case where _restart may
    # change across a shift-reload.
    python:
        if _restart is None:
            renpy.transition(config.end_splash_transition)
        else:
            renpy.transition(_restart[0])

            renpy.game.context().force_checkpoint = True
            renpy.jump(_restart[1])

label _invoke_main_menu:

    # Again, this has to be Python.
    python:
        if _restart:
            renpy.call_in_new_context(_restart[2])
        elif not renpy.os.environ.get("RENPY_SKIP_MAIN_MENU", False):
            renpy.call_in_new_context("_main_menu")


    # If the main menu returns, then start the game.

    python:
        renpy.game.context().force_checkpoint = True
        renpy.jump("start")

# At this point, we've been switched into a new context. So we
# initialize it.
label _main_menu(_main_menu_screen="_main_menu_screen"):

    python:
        renpy.block_rollback(purge=True)

        _enter_menu()

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
