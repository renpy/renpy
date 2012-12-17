# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1600 python:

    # Are the windows currently hidden?
    _windows_hidden = False

    def _toggle_skipping():

        if not config.skipping:
            config.skipping = "slow"
        else:
            config.skipping = None

        if renpy.context()._menu:
            renpy.jump("_noisy_return")
        else:            
            renpy.restart_interaction()

    def _keymap_toggle_skipping():
        if renpy.context()._menu:
            return

        toggle_skipping()
            
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


    import os
    config.screenshot_pattern = os.environ.get("RENPY_SCREENSHOT_PATTERN", "screenshot%04d.png")

    # Called to make a screenshot happen.
    def _screenshot():
        import os.path
        import os
        import __main__
        
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
            fn = os.path.join(dest, config.screenshot_pattern % i)
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

    def _dump_styles():
        if config.developer:
            renpy.style.write_text("styles.txt")
            

    def _fast_skip():
        if config.fast_skipping or config.developer:
            config.skipping = "fast"

        if renpy.context()._menu:
            renpy.jump("_noisy_return")

    def _reload_game():
        if not config.developer:
            return

        renpy.call_in_new_context("_save_reload_game")

    def _launch_editor():
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
        toggle_skip = _keymap_toggle_skipping,
        fast_skip = _fast_skip,
        game_menu = _invoke_game_menu,
        hide_windows = renpy.curried_call_in_new_context("_hide_windows"),
        launch_editor = _launch_editor,
        dump_styles = _dump_styles,
        reload_game = _reload_game,
        developer = renpy.curried_call_in_new_context("_developer"),
        quit = renpy.quit_event,
        iconify = renpy.iconify,
        help = _help,
        choose_renderer = renpy.curried_call_in_new_context("_choose_renderer"),
        )

    config.underlay = [ km ]


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