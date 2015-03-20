﻿# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

init -1600 python:

    config.keymap = dict(

        # Bindings present almost everywhere, unless explicitly
        # disabled.
        rollback = [ 'K_PAGEUP', 'repeat_K_PAGEUP', 'K_AC_BACK', 'mousedown_4', 'joy_rollback' ],
        screenshot = [ 's' ],
        toggle_fullscreen = [ 'f', 'alt_K_RETURN', 'alt_K_KP_ENTER', 'K_F11' ],
        game_menu = [ 'K_ESCAPE', 'K_MENU', 'mouseup_3', 'joy_menu' ],
        hide_windows = [ 'mouseup_2', 'h', 'joy_hide' ],
        launch_editor = [ 'E' ],
        dump_styles = [ ],
        reload_game = [ 'R' ],
        inspector = [ 'I' ],
        full_inspector = [ 'alt_I' ],
        developer = [ 'D' ],
        quit = [ ],
        iconify = [ ],
        help = [ 'K_F1', 'meta_shift_/' ],
        choose_renderer = [ 'G' ],
        progress_screen = [ 'alt_P' ],

        # Accessibility.
        self_voicing = [ 'v', 'V' ],
        clipboard_voicing = [ 'C' ],

        # Say.
        rollforward = [ 'mousedown_5', 'K_PAGEDOWN', 'repeat_K_PAGEDOWN' ],
        dismiss = [ 'mouseup_1', 'K_RETURN', 'K_SPACE', 'K_KP_ENTER', 'joy_dismiss' ],

        # Pause.
        dismiss_hard_pause = [ ],

        # Focus.
        focus_left = [ 'K_LEFT', 'repeat_K_LEFT', 'joy_left' ],
        focus_right = [ 'K_RIGHT', 'repeat_K_RIGHT', 'joy_right' ],
        focus_up = [ 'K_UP', 'repeat_K_UP', 'joy_up' ],
        focus_down = [ 'K_DOWN', 'repeat_K_DOWN', 'joy_down' ],

        # Button.
        button_ignore = [ 'mousedown_1' ],
        button_select = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
        button_alternate = [ 'mouseup_3' ],
        button_alternate_ignore = [ 'mousedown_3' ],

        # Input.
        input_backspace = [ 'K_BACKSPACE', 'repeat_K_BACKSPACE' ],
        input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],
        input_left = [ 'K_LEFT', 'repeat_K_LEFT' ],
        input_right = [ 'K_RIGHT', 'repeat_K_RIGHT' ],
        input_delete = [ 'K_DELETE', 'repeat_K_DELETE' ],

        # Viewport.
        viewport_up = [ 'mousedown_4' ],
        viewport_down = [ 'mousedown_5' ],
        viewport_drag_start = [ 'mousedown_1' ],
        viewport_drag_end = [ 'mouseup_1' ],

        # These keys control skipping.
        skip = [ 'K_LCTRL', 'K_RCTRL', 'joy_holdskip' ],
        toggle_skip = [ 'K_TAB', 'joy_toggleskip' ],
        fast_skip = [ '>' ],

        # Bar.
        bar_activate = [ 'mousedown_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
        bar_deactivate = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'joy_dismiss' ],
        bar_left = [ 'K_LEFT', 'repeat_K_LEFT', 'joy_left' ],
        bar_right = [ 'K_RIGHT', 'repeat_K_RIGHT', 'joy_right' ],
        bar_up = [ 'K_UP', 'repeat_K_UP', 'joy_up' ],
        bar_down = [ 'K_DOWN', 'repeat_K_DOWN', 'joy_down' ],

        # Delete a save.
        save_delete = [ 'K_DELETE' ],

        # Draggable.
        drag_activate = [ 'mousedown_1' ],
        drag_deactivate = [ 'mouseup_1' ],

        # Debug console.
        console = [ 'shift_O' ],
        console_older = [ 'K_UP', 'repeat_K_UP' ],
        console_newer = [ 'K_DOWN', 'repeat_K_DOWN'],

        # Ignored (kept for backwards compatibility).
        toggle_music = [ 'm' ],

        # Profile commands.
        profile_once = [ 'K_F8' ],
        memory_profile = [ 'K_F7' ],

        )

    config.default_keymap = { k : list(v) for k, v in config.keymap.items() }

    # Should we use the autoreload system?
    config.autoreload = True

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

    toggle_skipping = _toggle_skipping

    def _keymap_toggle_skipping():
        if renpy.context()._menu:
            return

        _toggle_skipping()

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
    del os

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
        renpy.notify(__("Saved screenshot as %s.") % fn)

    config.screenshot_callback = _screenshot_callback

    def _fast_skip():
        if not config.fast_skipping and not config.developer:
            return

        Skip(fast=True, confirm=not config.developer)()

    def _reload_game():
        if not config.developer:
            return

        if not config.autoreload:
            renpy.call_in_new_context("_save_reload_game")
            return

        if renpy.get_autoreload():
            renpy.set_autoreload(False)
            renpy.restart_interaction()
        else:
            renpy.set_autoreload(True)
            renpy.call_in_new_context("_save_reload_game")

    def _launch_editor():
        if not config.developer:
            return

        filename, line = renpy.get_filename_line()
        renpy.launch_editor([ filename ], line)

    def _developer():

        if not config.developer:
            return

        renpy.show_screen("_developer")
        renpy.restart_interaction()

    def _profile_once():
        renpy.display.interface.profile_once = True
        renpy.restart_interaction()

    def _memory_profile():
        renpy.memory.diff_memory()

    def _progress_screen():
        if renpy.context_nesting_level():
            return

        if renpy.get_screen("_progress"):
            renpy.hide_screen("_progress")
        else:
            renpy.show_screen("_progress")

        renpy.restart_interaction()

screen _progress:
    $ seen = renpy.count_seen_dialogue_blocks()
    $ total = renpy.count_dialogue_blocks()

    drag:
        draggable True
        focus_mask None
        xpos 0
        ypos 0

        text "[seen]/[total]":
            size 14
            color "#fff"
            outlines [ (1, "#000", 0, 0) ]

init -1100 python:

    # The default keymap. We might also want to put some of this into
    # the launcher.
    km = renpy.Keymap(
        rollback = renpy.rollback,
        screenshot = _screenshot,
        toggle_fullscreen = renpy.toggle_fullscreen,
        toggle_skip = _keymap_toggle_skipping,
        fast_skip = _fast_skip,
        game_menu = _invoke_game_menu,
        hide_windows = renpy.curried_call_in_new_context("_hide_windows"),
        launch_editor = _launch_editor,
        reload_game = _reload_game,
        developer = _developer,
        quit = renpy.quit_event,
        iconify = renpy.iconify,
        help = _help,
        choose_renderer = renpy.curried_call_in_new_context("_choose_renderer"),
        console = _console.enter,
        profile_once = _profile_once,
        memory_profile = _memory_profile,
        self_voicing = Preference("self voicing", "toggle"),
        clipboard_voicing = Preference("clipboard voicing", "toggle"),
        progress_screen = _progress_screen,
        )

    config.underlay = [ km ]

    del km


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
        renpy.music.stop()

        if renpy.can_load("_reload-1"):
            renpy.utter_restart()

        renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Saving game...",
                size=32, xalign=0.5, yalign=0.5, color="#fff", style="_text")

        renpy.pause(0)

        renpy.save("_reload-1", "reload save game")

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading script...",
                size=32, xalign=0.5, yalign=0.5, color="#fff", style="_text")

        renpy.pause(0)

        renpy.utter_restart()

label _load_reload_game:

    if not renpy.can_load("_reload-1"):
        return

    python hide:
        renpy.rename_save("_reload-1", "_reload-2")

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading game...",
                size=32, xalign=0.5, yalign=0.5, color="#fff", style="_text")

        ui.pausebehavior(0)
        ui.interact(suppress_underlay=True, suppress_overlay=True)

        renpy.load("_reload-2")

    return
