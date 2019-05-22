# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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
        rollback = [ 'K_PAGEUP', 'repeat_K_PAGEUP', 'K_AC_BACK', 'mousedown_4' ],
        screenshot = [ 's', 'alt_K_s', 'alt_shift_K_s' ],
        toggle_afm = [ ],
        toggle_fullscreen = [ 'f', 'alt_K_RETURN', 'alt_K_KP_ENTER', 'K_F11' ],
        game_menu = [ 'K_ESCAPE', 'K_MENU', 'mouseup_3' ],
        hide_windows = [ 'mouseup_2', 'h' ],
        launch_editor = [ 'E' ],
        dump_styles = [ ],
        reload_game = [ 'R', 'alt_shift_K_r' ],
        inspector = [ 'I' ],
        full_inspector = [ 'alt_shift_K_i' ],
        developer = [ 'D', 'alt_shift_K_d' ],
        quit = [ ],
        iconify = [ ],
        help = [ 'K_F1', 'meta_shift_/' ],
        choose_renderer = [ 'G', 'alt_shift_K_g' ],
        progress_screen = [ 'alt_shift_K_p', 'meta_shift_K_p', 'K_F2' ],
        accessibility = [ "K_a" ],

        # Accessibility.
        self_voicing = [ 'v', 'V', 'alt_K_v'  ],
        clipboard_voicing = [ 'C', 'alt_shift_K_c' ],
        debug_voicing = [ 'alt_shift_K_v', 'meta_shift_K_v' ],

        # Say.
        rollforward = [ 'mousedown_5', 'K_PAGEDOWN', 'repeat_K_PAGEDOWN' ],
        dismiss = [ 'mouseup_1', 'K_RETURN', 'K_SPACE', 'K_KP_ENTER', 'K_SELECT' ],
        dismiss_unfocused = [ ],

        # Pause.
        dismiss_hard_pause = [ ],

        # Focus.
        focus_left = [ 'K_LEFT', 'repeat_K_LEFT' ],
        focus_right = [ 'K_RIGHT', 'repeat_K_RIGHT' ],
        focus_up = [ 'K_UP', 'repeat_K_UP' ],
        focus_down = [ 'K_DOWN', 'repeat_K_DOWN' ],

        # Button.
        button_ignore = [ 'mousedown_1' ],
        button_select = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'K_SELECT' ],
        button_alternate = [ 'mouseup_3' ],
        button_alternate_ignore = [ 'mousedown_3' ],

        # Input.
        input_backspace = [ 'K_BACKSPACE', 'repeat_K_BACKSPACE' ],
        input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],
        input_left = [ 'K_LEFT', 'repeat_K_LEFT' ],
        input_right = [ 'K_RIGHT', 'repeat_K_RIGHT' ],
        input_up = [ 'K_UP', 'repeat_K_UP' ],
        input_down = [ 'K_DOWN', 'repeat_K_DOWN' ],
        input_delete = [ 'K_DELETE', 'repeat_K_DELETE' ],
        input_home = [ 'K_HOME' ],
        input_end = [ 'K_END' ],
        input_copy = [ 'ctrl_K_INSERT', 'ctrl_K_c' ],
        input_paste = [ 'shift_K_INSERT', 'ctrl_K_v' ],

        # Viewport.
        viewport_leftarrow = [ 'K_LEFT', 'repeat_K_LEFT' ],
        viewport_rightarrow = [ 'K_RIGHT', 'repeat_K_RIGHT' ],
        viewport_uparrow = [ 'K_UP', 'repeat_K_UP' ],
        viewport_downarrow = [ 'K_DOWN', 'repeat_K_DOWN' ],
        viewport_wheelup = [ 'mousedown_4' ],
        viewport_wheeldown = [ 'mousedown_5' ],
        viewport_drag_start = [ 'mousedown_1' ],
        viewport_drag_end = [ 'mouseup_1' ],
        viewport_pageup = [  'K_PAGEUP', 'repeat_K_PAGEUP' ],
        viewport_pagedown = [  'K_PAGEDOWN', 'repeat_K_PAGEDOWN' ],

        # These keys control skipping.
        skip = [ 'K_LCTRL', 'K_RCTRL' ],
        stop_skipping = [ ],
        toggle_skip = [ 'K_TAB' ],
        fast_skip = [ '>' ],

        # Bar.
        bar_activate = [ 'mousedown_1', 'K_RETURN', 'K_KP_ENTER', 'K_SELECT' ],
        bar_deactivate = [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'K_SELECT' ],
        bar_left = [ 'K_LEFT', 'repeat_K_LEFT' ],
        bar_right = [ 'K_RIGHT', 'repeat_K_RIGHT' ],
        bar_up = [ 'K_UP', 'repeat_K_UP' ],
        bar_down = [ 'K_DOWN', 'repeat_K_DOWN' ],

        # Delete a save.
        save_delete = [ 'K_DELETE' ],

        # Draggable.
        drag_activate = [ 'mousedown_1' ],
        drag_deactivate = [ 'mouseup_1' ],

        # Debug console.
        console = [ 'shift_O', 'alt_shift_K_o' ],
        console_older = [ 'K_UP', 'repeat_K_UP' ],
        console_newer = [ 'K_DOWN', 'repeat_K_DOWN'],

        # Director
        director = [ 'd' ],

        # Ignored (kept for backwards compatibility).
        toggle_music = [ 'm' ],
        viewport_up = [ 'mousedown_4' ],
        viewport_down = [ 'mousedown_5' ],

        # Profile commands.
        performance = [ 'K_F3' ],
        image_load_log = [ 'K_F4' ],
        profile_once = [ 'K_F8' ],
        memory_profile = [ 'K_F7' ],

        )

    config.default_keymap = { k : list(v) for k, v in config.keymap.items() }

    config.pad_bindings = {
        "pad_leftshoulder_press" : [ "rollback", ],
        "pad_lefttrigger_pos" : [ "rollback", ],
        "pad_back_press" : [ "rollback", ],

        "pad_guide_press" : [ "game_menu", ],
        "pad_start_press" : [ "game_menu", ],

        "pad_y_press" : [ "hide_windows", ],

        "pad_rightshoulder_press" : [ "rollforward", ],

        "pad_righttrigger_pos" : [ "dismiss", "button_select", "bar_activate", "bar_deactivate" ],
        "pad_a_press" : [ "dismiss", "button_select", "bar_activate", "bar_deactivate"],
        "pad_b_press" : [ "button_alternate" ],

        "pad_dpleft_press" : [ "focus_left", "bar_left", "viewport_leftarrow" ],
        "pad_leftx_neg" : [ "focus_left", "bar_left", "viewport_leftarrow" ],
        "pad_rightx_neg" : [ "focus_left", "bar_left", "viewport_leftarrow" ],

        "pad_dpright_press" : [ "focus_right", "bar_right", "viewport_rightarrow" ],
        "pad_leftx_pos" : [ "focus_right", "bar_right", "viewport_rightarrow" ],
        "pad_rightx_pos" : [ "focus_right", "bar_right", "viewport_rightarrow" ],

        "pad_dpup_press" : [ "focus_up", "bar_up", "viewport_uparrow" ],
        "pad_lefty_neg" :  [ "focus_up", "bar_up", "viewport_uparrow" ],
        "pad_righty_neg" : [ "focus_up", "bar_up", "viewport_uparrow" ],

        "pad_dpdown_press" : [ "focus_down", "bar_down", "viewport_downarrow" ],
        "pad_lefty_pos" : [ "focus_down", "bar_down", "viewport_downarrow" ],
        "pad_righty_pos" : [ "focus_down", "bar_down", "viewport_downarrow" ],
    }

    # Should we use the autoreload system?
    config.autoreload = True

init -1600 python:

    # Are the windows currently hidden?
    _windows_hidden = False

    def _keymap_toggle_afm():
        if renpy.context()._menu:
            return

        renpy.run(Preference("auto-forward", "toggle"))

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

    config.help_screen = "help"

    def _help(help=None):

        if config.help_screen and renpy.has_screen(config.help_screen):
            renpy.run(ShowMenu(config.help_screen))
            return

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
            import os

            file_path = os.path.join(config.basedir, help)
            if not os.path.isfile(file_path):
                return

            webbrowser.open_new("file:///" + file_path)
        except:
            pass

    import os
    config.screenshot_pattern = os.environ.get(b"RENPY_SCREENSHOT_PATTERN", b"screenshot%04d.png")
    del os

    # Called to make a screenshot happen.
    def _screenshot():
        import os.path
        import os
        import __main__

        dest = config.renpy_base

        if renpy.macapp:
            dest = os.path.expanduser(b"~/Desktop")

        # Try to pick a filename.
        i = 1
        while True:
            fn = os.path.join(dest, config.screenshot_pattern % i)
            if not os.path.exists(fn):
                break
            i += 1

        try:
            if not renpy.screenshot(fn):
                renpy.notify(__("Failed to save screenshot as %s.") % fn)
                return
        except:
            import traceback
            traceback.print_exc()
            renpy.notify(__("Failed to save screenshot as %s.") % fn)
            return

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
            renpy.exports.reload_script()
            return

        if renpy.get_autoreload():
            renpy.set_autoreload(False)
            renpy.restart_interaction()
        else:
            renpy.set_autoreload(True)
            renpy.exports.reload_script()

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
        import os

        if not renpy.experimental:
            return

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
    $ new = renpy.count_newly_seen_dialogue_blocks()
    $ seen = renpy.count_seen_dialogue_blocks()
    $ total = renpy.count_dialogue_blocks()

    drag:
        draggable True
        focus_mask None
        xpos 0
        ypos 0

        text "[new] [seen]/[total]":
            size 14
            color "#fff"
            outlines [ (1, "#000", 0, 0) ]
            alt ""

init -1100 python:

    # The default keymap. We might also want to put some of this into
    # the launcher.
    _default_keymap = renpy.Keymap(
        rollback = renpy.rollback,
        screenshot = _screenshot,
        toggle_fullscreen = renpy.toggle_fullscreen,
        toggle_afm = _keymap_toggle_afm,
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
        debug_voicing = Preference("debug voicing", "toggle"),
        progress_screen = _progress_screen,
        director = director.Start(),
        performance = ToggleScreen("_performance"),
        accessibility = ToggleScreen("_accessibility"),
        )

    config.underlay = [ _default_keymap ]

init 1100 python hide:

    import os

    if "RENPY_DEFAULT_KEYMAP" in os.environ:
        renpy.config.keymap = renpy.config.default_keymap
        config.underlay.insert(0, _default_keymap)


label _hide_windows:

    if renpy.context()._menu:
        return

    if _windows_hidden:
        return

    python:
        _windows_hidden = True
        voice_sustain()
        ui.saybehavior(dismiss=['dismiss', 'hide_windows'])
        ui.interact(suppress_overlay=True, suppress_window=True)
        _windows_hidden = False

    return


label _save_reload_game:
    python hide:

        renpy.music.stop()

        if renpy.can_load("_reload-1"):
            renpy.utter_restart()

        import time
        renpy.session["_reload_time"] = time.time()

        renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Saving game...",
                size=32, xalign=0.5, yalign=0.5, color="#fff", style="_text")

        ui.pausebehavior(0)
        ui.interact(suppress_overlay=True, suppress_underlay=True)

        renpy.save("_reload-1", "reload save game")

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading script...",
                size=32, xalign=0.5, yalign=0.5, color="#fff", style="_text")

        ui.pausebehavior(0)
        ui.interact(suppress_overlay=True, suppress_underlay=True)

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
