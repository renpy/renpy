# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file consists of renpy functions that aren't expected to be
# touched by the user too much. We reserve the _ prefix for names
# defined in the library.

init -1180 python:

    # These are settings that the user can tweak to control the
    # look of the main menu and the load/save/escape screens.

    # basics: The version of Ren'Py this script is intended for, or
    # None if it's intended for the current version.
    config.script_version = None
    
    # The minimum version of the module we work with. Don't change
    # this unless you know what you're doing.
    config.module_version = 6007001

    # Should we warn the user if the module is missing or has a bad
    # version?
    config.module_warning = False

    # basics: A map from a string that's displayed by the interface to
    # a translated value of that string.
    config.translations = { }

    # Used internally to maintain compatiblity with old
    # translations of strings.
    config.old_names = { }

    # basics: True if the skip indicator should be shown.
    config.skip_indicator = True

    # basics: The width of a thumbnail.
    config.thumbnail_width = 66

    # basics: The height of a thumbnail.
    config.thumbnail_height = 50

    # basics: If not None, the default value of the fullscreen
    # preference when the game is first run.
    config.default_fullscreen = None

    # basics: If not None, the default value of the text_cps
    # preference when the game is first run.
    config.default_text_cps = None        

    # If not None, the default value of afm_time
    config.default_afm_time = None

    # If not None, the default value of afm_enable
    config.default_afm_enable = None
    
    # Should we automatically define images?
    config.automatic_images = None

    # Prefixes to strip from automatic images.
    config.automatic_images_strip = [ ]
    
    # A save to automatically load, if it exists.
    config.auto_load = None

    # Layers to clear when entering the menus.
    config.menu_clear_layers = [ ]

    # Should we start the game with scene black or just scene?
    config.start_scene_black = False

    # Voice and Sound samples.
    config.sample_sound = None
    config.sample_voice = None
    
    # This is updated to give the user an idea of where a save is
    # taking place.
    save_name = ''

    # Should the window be shown during transitions?
    _window_during_transitions = False

    def _default_with_callback(trans, paired=None):
        if (_window_during_transitions and not
            renpy.context_nesting_level() and
            not renpy.count_displayables_in_layer('transient')):

            # narrator("", interact=False)
            ui.window(style=style.say_window["empty"])
            ui.null()
            
        return trans

    config.with_callback = _default_with_callback


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

    # This is used to jump to a label with a transition.
    def _intra_jumps_core(label, transition):
        renpy.transition(getattr(config, transition))
        renpy.jump(label)

    _intra_jumps = renpy.curry(_intra_jumps_core)

    # The function that's used to translate strings in the game menu.
    def _(s):
        """
        Translates s into another language or something.
        """

        if s in config.translations:
            return config.translations[s]

        if s in config.old_names and config.old_names[s] in config.translations:
            return config.translations[config.old_names[s]]

        return s

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

    # Are the windows currently hidden?
    _windows_hidden = False

    def toggle_skipping():

        if not config.skipping:
            config.skipping = "slow"
        else:
            config.skipping = None

        if renpy.context()._menu:
            renpy.jump("_noisy_return")
        else:            
            renpy.restart_interaction()

    config.help = None
            
    def _help(help=None):

        if help is None:
            help = config.help

        if help is None:
            return

        if renpy.has_label(help):
            renpy.call_in_new_context(help)
            return

        _preferences.fullscreen = False

        try:
            import webbrowser
            webbrowser.open_new("file:///" + config.basedir + "/" + help)
        except:
            pass

        
    # Called to make a screenshot happen.
    def _screenshot():
        import os.path
        import os
        import __main__
        
        pattern = os.environ.get("RENPY_SCREENSHOT_PATTERN", "screenshot%04d.png")

        # Pick the directory to save into.
        dest = config.renpy_base.rstrip("/")
        
        # Guess if we're an OSX App.
        if dest.endswith("/Contents/Resources/autorun"):
            # Go up 4 directories.
            dest = os.path.dirname(dest)
            dest = os.path.dirname(dest)
            dest = os.path.dirname(dest)
            dest = os.path.dirname(dest)

        # Try to pick a filename.
        i = 1
        while True:
            fn = dest + "/" + pattern % i
            if not os.path.exists(fn):
                break
            i += 1

        try:
            renpy.screenshot(fn)
        except:
            import traceback
            traceback.print_exc()

        if config.screenshot_callback is not None:
            config.screenshot_callback(fn)

    def _screenshot_callback(fn):
        renpy.notify(_("Saved screenshot as %s.") % fn)

    config.screenshot_callback = _screenshot_callback
        
    _predict_screens = [ ]
        
init -1180 python hide:

    def dump_styles():
        if config.developer:
            renpy.style.write_text("styles.txt")

    # This is run when entering the game menu.
    config.game_menu_action = None
            
    def invoke_game_menu():
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

    def keymap_toggle_skipping():
        if renpy.context()._menu:
            return

        toggle_skipping()
            
    def fast_skip():
        if config.fast_skipping or config.developer:
            config.skipping = "fast"

        if renpy.context()._menu:
            renpy.jump("_noisy_return")

    def reload_game():
        if not config.developer:
            return

        renpy.call_in_new_context("_save_reload_game")

    def launch_editor():
        if not config.developer:
            return

        filename, line = renpy.get_filename_line()
        renpy.launch_editor([ filename ], line)
        
    # The default keymap. We might also want to put some of this into
    # the launcher.
    km = renpy.Keymap(
        rollback = renpy.rollback,
        screenshot = _screenshot,
        toggle_fullscreen = renpy.toggle_fullscreen,
        toggle_music = renpy.toggle_music,
        toggle_skip = keymap_toggle_skipping,
        fast_skip = fast_skip,
        game_menu = invoke_game_menu,
        hide_windows = renpy.curried_call_in_new_context("_hide_windows"),
        launch_editor = launch_editor,
        dump_styles = dump_styles,
        reload_game = reload_game,
        developer = renpy.curried_call_in_new_context("_developer"),
        quit = renpy.quit_event,
        iconify = renpy.iconify,
        help = _help,
        )

    config.underlay = [ km ]

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

    # Hyperlink functions. Duplicated in _errorhandling.rpym.
    def hyperlink_styler(target):
        return style.hyperlink_text

    def hyperlink_function(target):
        if target.startswith("http:"):
            try:
                import webbrowser
                webbrowser.open(target)
            except:
                pass
        else:
            renpy.call_in_new_context(target)

    style.default.hyperlink_functions = (hyperlink_styler, hyperlink_function, None)

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
            
    def imagemap_auto_function(auto_param, variant):
        rv = auto_param % variant

        if renpy.loadable(rv):
            return rv
        else:
            return None
        
        
    config.imagemap_auto_function = imagemap_auto_function


label _hide_windows:

    if renpy.context()._menu:
        return
    
    if _windows_hidden:
        return

    python:
        _windows_hidden = True
        ui.saybehavior(dismiss=['dismiss', 'hide_windows'])
        ui.interact(suppress_overlay=True, suppress_window=True)
        _windows_hidden = False

    return

    
# This code here handles check for the correct version of the Ren'Py module.
                         
label _save_reload_game:
    python hide:
        renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))
        renpy.music.stop()
        
        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Saving game...",
                size=32, xalign=0.5, yalign=0.5, color=(255, 255, 255, 255))

        renpy.pause(0)

        renpy.save("_reload-1", "reload save game")
        
        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading script...",
                size=32, xalign=0.5, yalign=0.5, color=(255, 255, 255, 255))

        renpy.pause(0)
        
        renpy.utter_restart()

label _load_reload_game:
    
    if not renpy.can_load("_reload-1"):
        return 

    python hide:
        renpy.rename_save("_reload-1", "_reload-2")

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading game...",
                size=32, xalign=0.5, yalign=0.5, color=(255, 255, 255, 255))

        ui.pausebehavior(0)
        ui.interact(suppress_underlay=True, suppress_overlay=True)
        
        renpy.load("_reload-2")

    return

init -1001:
    image text = renpy.ParameterizedText(style="centered_text")

    # Lock the library object.
    $ config.locked = True


# Implement config.default_fullscreen and config.default_text_cps.
init 1180 python:

    if not persistent._set_preferences:
        persistent._set_preferences = True
        
        if config.default_fullscreen is not None:
            _preferences.fullscreen = config.default_fullscreen

        if config.default_text_cps is not None:
            _preferences.text_cps = config.default_text_cps

        if config.default_afm_time is not None:
            _preferences.afm_time = config.default_afm_time
            
    if config.default_afm_enable is not None:
        _preferences.afm_enable = config.default_afm_enable
        _preferences.using_afm_enable = True
    else:
        _preferences.afm_enable = True
        _preferences.using_afm_enable = False
    

        
##############################################################################
# Code that originated in 00gamemenu.rpy
init -1180 python:

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

    # Transition that's used after the game is loaded.
    config.after_load_transition = None
    
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
    
    style.error_root = Style(style.default)
    style.error_title = Style(style.default)
    style.error_body = Style(style.default)

    def _show_exception(title, message):

        ui.window(style='error_root')
        ui.vbox()

        ui.text(title, style='error_title')
        ui.text("")
        ui.text(message, style='error_body')
        ui.text("")
        ui.text(_(u"Please click to continue."), style='error_body')

        ui.close()

        ui.saybehavior()

        ui.interact()

    def _enter_menu():
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


##############################################################################
# Code that originated in 00mainmenu.rpy

init -1180 python hide:

    # menus: Music to play at the main menu.
    config.main_menu_music = None

    # advanced: Callbacks to run at start.
    config.start_callbacks = [ ]


# This fixes up the context, if necessary, then calls the real
# after_load.
label _after_load:
    $ renpy.context()._menu = False
    $ renpy.context()._main_menu = False

    if config.after_load_transition:
        $ renpy.transition(config.after_load_transition, force=True)
    
    if renpy.has_label("after_load"):
        jump expression "after_load"
    else:
        return

    
# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    python hide:
        renpy.context()._menu = False
        renpy.context()._main_menu = False
        
        for i in config.start_callbacks:
            i()

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

init 1180 python hide:
    
    def create_automatic_images():
    
        seps = config.automatic_images

        if seps is True:
            seps = [ ' ', '/', '_' ]
            
        for dir, fn in renpy.loader.listdirfiles():

            if fn.startswith("_"):
                continue

            # Only .png and .jpg
            if not fn.lower().endswith(".png") and not fn.lower().endswith(".jpg"):
                continue

            # Strip the extension, replace slashes.
            shortfn = fn[:-4].replace("\\", "/")
            
            # Determine the name.
            name = ( shortfn, )
            for sep in seps:
                name = tuple(j for i in name for j in i.split(sep))

            # Strip name components.
            while name:
                for i in config.automatic_images_strip:
                    if name[0] == i:
                        name = name[1:]
                        break
                else:
                    break
                
            # Only names of 2 components or more.
            if len(name) < 2:
                continue
            
            # Reject if it already exists.
            if name in renpy.display.image.images:
                continue

            renpy.image(name, fn)

    if config.automatic_images:
        create_automatic_images()


# Load the developer screen, if necessary.
init 1180 python hide:

    if config.developer:
        renpy.load_module("_developer")

# Entry point for the developer screen. The rest of it is loaded from
# _developer.rpym
label _developer:

    if not config.developer:
        return

    $ _enter_menu()

    jump expression "_developer_screen"

