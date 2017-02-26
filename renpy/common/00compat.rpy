# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

init -1900 python:

    # This is called when script_version is set, to immediately
    # run code in response to a script_version change.
    def _set_script_version(version):

        if version is None:
            return

        if version <= (5, 6, 0):
            config.check_properties = False

        if version <= (6, 5, 0):
            layout.compat()

        if version <= (6, 9, 1):
            store.library = store.config

        if version <= (6, 9, 3):

            # Before 6.10, these were positions, rather than transforms.
            store.left = Position(xalign=0.0)
            store.center = Position(xalign=0.5)
            store.truecenter = Position(xalign=0.5, yalign=0.5)
            store.right = Position(xalign=1.0)
            store.offscreenleft = Position(xpos=0.0, xanchor=1.0)
            store.offscreenright = Position(xpos=1.0, xanchor=0.0)

        if version <= (6, 10, 2):
            # Before 6.11, we used the image placement to handle
            # the location of things on the screen.
            style.image_placement.xpos = 0.5
            style.image_placement.ypos = 1.0
            style.image_placement.xanchor = 0.5
            style.image_placement.yanchor = 1.0

            config.transform_uses_child_position = False
            config.default_transform = None
            config.start_scene_black = True

        if version <= (6, 11, 0):
            config.movetransition_respects_offsets = False

        if version <= (6, 11, 2):
            config.imagereference_respects_position = True
            config.predict_screens = False
            config.choice_screen_chosen = False

        if version <= (6, 12, 0):
            config.keep_running_transform = False
            config.image_attributes = False
            config.new_character_image_argument = False
            config.save_physical_size = False

        if version <= (6, 12, 2):
            style.default.language = "western"
            style.default.layout = "greedy"
            config.new_substitutions = False
            config.broken_line_spacing = True

        if (6, 12, 2) < version <= (6, 13, 8):
            config.old_substitutions = False

        if version <= (6, 13, 12):
            global MoveTransition
            MoveTransition = OldMoveTransition

            define.move_transitions = define.old_move_transitions

            define.move_transitions("move", 0.5)
            define.move_transitions("ease", 0.5, _ease_time_warp, _ease_in_time_warp, _ease_out_time_warp)

        if version <= (6, 14, 1):
            config.key_repeat = None

        if version <= (6, 15, 7):
            MusicRoom.loop_compat = True

        if version <= (6, 17, 0):
            config.keymap['toggle_music'] = [ 'm' ]

        if version <= (6, 17, 4):
            config.default_sound_loop = False

        if version <= (6, 18, 0):
            config.predict_screen_statements = False
            config.transition_screens = False

        if version <= (6, 99, 1):
            config.images_directory = None
            config.preserve_zorder = False

        if version <= (6, 99, 5):
            config.wrap_shown_transforms = False
            config.search_prefixes = [ "" ]

        if version <= (6, 99, 6):
            config.dynamic_images = False

        if version <= (6, 99, 8):
            if config.developer == "auto":
                config.developer = False

            config.play_channel = "sound"

        if version <= (6, 99, 8):
            config.help_screen = None
            config.confirm_screen = False

        if version <= (6, 99, 10):
            config.new_translate_order = False
            config.old_say_args = True
            config.window_auto_hide.remove("call screen")
            config.quit_action = ui.gamemenus("_quit_prompt")
            config.enforce_window_max_size = False
            config.splashscreen_suppress_overlay = False

        if version <= (6, 99, 12, 3):
            config.prefix_viewport_scrollbar_styles = False


    # The version of Ren'Py this script is intended for, or
    # None if it's intended for the current version.
    config.script_version = None

init -1000 python hide:
    try:
        import ast
        script_version = renpy.file("script_version.txt").read()
        config.script_version = ast.literal_eval(script_version)
        renpy.write_log("Set script version to: %r", config.script_version)
    except:
        pass

init 1900 python hide::

    # This returns true if the script_version is <= the
    # script_version supplied. Give it the last script version
    # where an old version was used.
    def compat(x, y, z):
        return config.script_version and config.script_version <= (x, y, z)

    # Compat for changes to with-callback.
    if compat(5, 4, 5):
        if config.with_callback:
            def compat_with_function(trans, paired, old=config.with_callback):
                old(trans)
                return trans

            config.with_callback = compat_with_function

    if not config.sound:
        config.has_sound = False
        config.has_music = False
        config.has_voice = False

    # Compat for SFont recoloring.
    if compat(5, 1, 1):
        config.recolor_sfonts = False

    if compat(5, 5, 4):
        config.implicit_with_none = False

    # Compat for changes to button look.
    if compat(5, 5, 4):
        style.button.setdefault(xpos=0.5, xanchor=0.5)
        style.menu_button.clear()
        style.menu_button_text.clear()

    if compat(5, 6, 6):
        config.reject_midi = False

    if compat(6, 2, 0):
        config.reject_backslash = False

    if compat(6, 9, 0):
        style.motion.clear()

    if compat(6, 10, 2):
        if 'screens' not in config.layers:
            config.layers.append('screens')

    if "Fullscreen" in config.translations:
        fs = _("Fullscreen")
        config.translations.setdefault("Fullscreen 4:3", fs + " 4:3")
        config.translations.setdefault("Fullscreen 16:9", fs + " 16:9")
        config.translations.setdefault("Fullscreen 16:10", fs + " 16:10")

    for i in layout.compat_funcs:
        i()

    if config.hyperlink_styler or config.hyperlink_callback or config.hyperlink_focus:
        style.default.hyperlink_functions = (config.hyperlink_styler, config.hyperlink_callback, config.hyperlink_focus)

    if compat(6, 15, 7):
        config.has_quicksave = False
        config.quit_action = ui.gamemenus("_confirm_quit")
        config.default_afm_enable = None


