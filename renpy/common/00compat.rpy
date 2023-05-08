﻿# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

init -1100 python:

    def _compat_versions(version, *args):
        if version <= args[0]:
            return True

        for i in args[1:]:
            if (version[0] == i[0]) and (version <= i):
                return True

        return False

    # This is called when script_version is set, to immediately
    # run code in response to a script_version change.
    def _set_script_version(version):

        if version is None:
            return

        import os

        if "RENPY_EXPERIMENTAL" in os.environ:
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
            if "call screen" in config.window_auto_hide:
                config.window_auto_hide.remove("call screen")
            config.quit_action = ui.gamemenus("_quit_prompt")
            config.enforce_window_max_size = False
            config.splashscreen_suppress_overlay = False

        if version <= (6, 99, 12, 3):
            config.prefix_viewport_scrollbar_styles = False

        if version <= (6, 99, 12, 4):
            config.hyperlink_inherit_size = False
            config.automatic_polar_motion = False
            config.position_viewport_side = False
            config.nw_voice = False
            config.atl_one_frame = False
            config.keep_show_layer_state = False
            config.atl_multiple_events = False

        if version <= (6, 99, 13):
            config.fast_unhandled_event = False
            config.gc_thresholds = (700, 10, 10)
            config.idle_gc_count = 10000
            config.scrollbar_child_size = False

        if version <= (6, 99, 14):
            config.image_cache_size_mb = None
            config.image_cache_size = 16
            config.cache_surfaces = True
            config.optimize_texture_bounds = False

        if version <= (6, 99, 14, 3):
            config.late_images_scan = True
            config.dissolve_force_alpha = False
            config.replay_movie_sprites = False

        if version <= (7, 0, 0):
            config.reject_relative = False
            config.say_attributes_use_side_image = False

        if version <= (7, 1, 0):
            config.menu_showed_window = True
            config.window_auto_show = [ "say" ]
            config.window_auto_hide = [ "scene", "call screen" ]

        if version <= (7, 1, 1):
            config.menu_actions = False

        if version <= (7, 2, 2):
            config.say_attribute_transition_callback_attrs = False
            config.keep_side_render_order = False

        if version <= (7, 3, 0):
            config.force_sound = False

        if version <= (7, 3, 2):
            config.audio_directory = None
            config.early_start_store = True
            config.compat_viewport_minimum = True

        if version <= (7, 3, 5):
            config.side_image_requires_attributes = False
            config.window_functions_set_auto = False
            config.hw_video = True
            config.who_what_sub_compat = 0

        if version <= (7, 4, 0):
            config.pause_with_transition = True

        if version <= (7, 4, 2):
            config.dismiss_blocking_transitions = False

        if version <= (7, 4, 4):
            config.pause_after_rollback = True
            config.gl2 = False
            config.gl_lod_bias = -1.0
            config.who_what_sub_compat = 1

        if version == (7, 4, 5):
            config.scene_clears_layer_at_list = False

        if version <= (7, 4, 6):
            config.adjust_minimums = False
            config.atl_start_on_show = False
            config.input_caret_blink = False

        if version <= (7, 4, 8):
            config.relative_transform_size = False
            config.tts_front_to_back = False

        if version <= (7, 4, 10):
            config.always_unfocus = False

        if version <= (7, 4, 11):
            config.allow_unfull_vpgrids = True
            style.drag.focus_mask = True
            style.default.outline_scaling = "step"
            config.box_skip = False
            config.crop_relative_default = False
            config.layeredimage_offer_screen = False
            config.narrator_menu = False
            config.gui_text_position_properties = False
            config.atl_function_always_blocks = True

        if version <= (7, 4, 11):
            config.modal_blocks_timer = False
            config.modal_blocks_pause = False
        elif _compat_versions(version, (7, 5, 1), (8, 0, 1)):
            config.modal_blocks_timer = True
            config.modal_blocks_pause = False
        elif _compat_versions(version, (7, 5, 2), (8, 0, 2)):
            config.modal_blocks_pause = True
            config.modal_blocks_timer = True

        if _compat_versions(version, (7, 5, 3), (8, 0, 3)):
            config.quadratic_volumes = True
            config.emphasize_audio_volume = 0.5
            config.relative_spacing = False
            config.lenticular_bracket_ruby = False
            config.preserve_volume_when_muted = True
            config.history_current_dialogue = False
            config.scry_extend = False
            config.fadeout_audio = 0.0
            config.at_transform_compare_full_context = True
            config.linear_fades = True

            if version > (6, 99, 5):
                config.search_prefixes.append("images/")

            config.top_layers.remove("top")
            config.bottom_layers.remove("bottom")
            config.context_clear_layers.remove("top")
            config.context_clear_layers.remove("bottom")

            config.sticky_layers.remove("master")

            store._errorhandling._constant = True
            store._gamepad._constant = True
            store._renpysteam._constant = True
            store._warper._constant = True
            store.audio._constant = True
            store.achievement._constant = True
            store.build._constant = True
            store.director._constant = True
            store.iap._constant = True
            store.layeredimage._constant = True
            store.updater._constant = True

    # The version of Ren'Py this script is intended for, or
    # None if it's intended for the current version.
    config.script_version = None

python early hide:
    try:
        import ast
        with renpy.open_file("script_version.txt", "utf-8") as f:
            script_version = f.read()
        script_version = ast.literal_eval(script_version)

        config.early_script_version = script_version
        config.early_developer = not script_version

        if script_version <= (7, 2, 2):
            config.keyword_after_python = True

    except Exception:
        config.early_script_version = None
        config.early_developer = True
        pass


init -1000 python hide:
    import re

    try:
        import ast
        with renpy.open_file("script_version.txt", "utf-8") as f:
            script_version = f.read()
        config.script_version = ast.literal_eval(script_version)
        renpy.write_log("Set script version to: %r", config.script_version)
    except Exception:
        pass

    # 6.99.12.4 didn't add script_version.txt, so we read it from renpy/__init__.py
    # if that exists.
    #
    # For really old version, script_version may not be set, so try to read it out of
    # the renpy that came with the game.
    try:
        if config.script_version is None:
            init_py = os.path.join(renpy.config.basedir, "renpy", "__init__.py")
            with open(init_py, "r") as f:
                data = f.read()

            if "version_tuple = (6, 99, 12, 4, vc_version)" in data:
                config.script_version = (6, 99, 12, 4)
            elif config.renpy_base != config.basedir:
                for l in data.splitlines():
                    m = re.match(r"version = \"Ren'Py ([\.\d]+)", l)
                    if m:
                        config.script_version = tuple(int(i) for i in m.group(1).split("."))



            renpy.write_log("Set script version to: %r (alternate path)", config.script_version)
    except Exception:
        pass


init 1100 python hide:

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

    if config.fade_music is not None:
        config.fadeout_audio = config.fade_music
