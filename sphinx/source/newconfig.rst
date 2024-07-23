=======================
Configuration Variables
=======================

Configuration variables control the behavior of Ren'Py's implementation,
allowing Ren'Py itself to be customized in a myriad of ways. These range from
the common (such as changing the screen size) to the obscure (adding new
kinds of archive files).

Ren'Py's implementation makes the assumption that, once the GUI system has
initialized, configuration variables will not change. Changing configuration
variables outside of ``init`` blocks can lead to undefined behavior.
Configuration variables are not part of the save data.

Most configuration variables are easily set using a ``define`` statement::

    define config.rollback_enabled = False

Dict and list variables can be populated using ``define`` or in an
``init python`` block::

    define config.preload_fonts += ["OrthodoxHerbertarian.ttf"]
    define config.adjust_attributes["eileen"] = eileen_adjust_function

    init python hide:
        def inter_cbk():
            # this is a terrible callback
            renpy.notify("Interacting !")

        config.interact_callbacks.append(inter_cbk)



Project Info
------------

.. var:: config.name
.. var:: config.version
.. var:: config.window_icon
.. var:: config.window_title

Auto-Forward Mode
------------------

.. var:: config.afm_bonus
.. var:: config.afm_callback
.. var:: config.afm_characters
.. var:: config.afm_voice_delay

Callbacks
---------

These take functions that are called when certain events occur. These are not the only
callbacks - ones corresponding to more specific features are listed in the section on
that feature.

.. var:: config.after_default_callbacks
.. var:: config.context_callback
.. var:: config.start_callbacks
.. var:: config.python_callbacks
.. var:: config.python_exit_callbacks
.. var:: config.periodic_callbacks
.. var:: config.start_interact_callbacks
.. var:: config.interact_callbacks
.. var:: config.statement_callbacks
.. var:: config.scene_callbacks
.. var:: config.label_callbacks
.. var:: config.with_callback


Characters and Dialogue
-----------------------

.. var:: config.character_id_prefixes
.. var:: config.all_character_callbacks
.. var:: config.character_callback
.. var:: config.say_arguments_callback
.. var:: config.say_allow_dismiss
.. var:: config.say_sustain_callbacks

Choice Menus
------------

.. var:: config.menu_arguments_callback
.. var:: config.menu_include_disabled
.. var:: config.menu_window_subtitle
.. var:: config.narrator_menu
.. var:: config.auto_choice_delay

Display
-------

.. var:: config.gl_clear_color
.. var:: config.gl_lod_bias
.. var:: config.gl_test_image
.. var:: config.gl_resize
.. var:: config.screen_height
.. var:: config.screen_width
.. var:: config.physical_height
.. var:: config.physical_width
.. var:: config.adjust_view_size
.. var:: config.nearest_neighbor
.. var:: config.display_start_callbacks
.. var:: config.shader_part_filter
.. var:: config.minimum_presplash_time

File I/O
--------

.. var:: config.file_open_callback
.. var:: config.open_file_encoding

History
-------

.. var:: config.history_callbacks
.. var:: config.history_length
.. var:: config.history_current_dialogue

Input, Focus, and Events
------------------------

.. var:: config.keymap
.. var:: config.pad_bindings
.. var:: config.controller_blocklist
.. var:: config.longpress_duration
.. var:: config.longpress_radius
.. var:: config.longpress_vibrate
.. var:: config.script_version
.. var:: config.allow_screensaver
.. var:: config.input_caret_blink
.. var:: config.pass_controller_events
.. var:: config.pass_joystick_events
.. var:: config.web_input
.. var:: config.focus_crossrange_penalty


Layered Images
--------------

.. var:: config.layeredimage_offer_screen

Layers
------

.. var:: config.sticky_layers
.. var:: config.top_layers
.. var:: config.transient_layers
.. var:: config.default_tag_layer
.. var:: config.tag_layer
.. var:: config.layer_transforms
.. var:: config.say_layer
.. var:: config.bottom_layers
.. var:: config.choice_layer
.. var:: config.clear_layers
.. var:: config.context_clear_layers
.. var:: config.detached_layers
.. var:: config.interface_layer
.. var:: config.layer_clipping
.. var:: config.layers
.. var:: config.overlay_layers

Media (Music, Sound, and Video)
-------------------------------

.. var:: config.audio_filename_callback
.. var:: config.auto_channels
.. var:: config.auto_movie_channel
.. var:: config.single_movie_channel
.. var:: config.skip_sounds
.. var:: config.webaudio_required_types
.. var:: config.main_menu_stop_channels
.. var:: config.mipmap_movies
.. var:: config.movie_mixer
.. var:: config.web_video_base
.. var:: config.web_video_prompt
.. var:: config.context_fadein_music
.. var:: config.context_fadeout_music
.. var:: config.fadeout_audio
.. var:: config.play_channel
.. var:: config.enter_sound
.. var:: config.exit_sound
.. var:: config.sound
.. var:: config.sound_sample_rate
.. var:: config.game_menu_music
.. var:: config.main_menu_music
.. var:: config.main_menu_music_fadein
.. var:: config.preserve_volume_when_muted

Mouse
-----

.. var:: config.mouse
.. var:: config.mouse_displayable
.. var:: config.mouse_focus_clickthrough
.. var:: config.mouse_hide_time

Paths
-----

.. var:: config.gamedir
.. var:: config.searchpath
.. var:: config.savedir
.. var:: config.archives
.. var:: config.search_prefixes

Quit
----

.. var:: config.quit_on_mobile_background
.. var:: config.quit_action
.. var:: config.quit_callbacks

Replay
------

.. var:: config.after_replay_callback
.. var:: config.replay_scope

Rollback
--------

.. var:: config.fix_rollback_without_choice
.. var:: config.ex_rollback_classes
.. var:: config.hard_rollback_limit
.. var:: config.rollback_enabled
.. var:: config.rollback_length
.. var:: config.rollback_side_size
.. var:: config.call_screen_roll_forward
.. var:: config.pause_after_rollback

Saving and Loading
------------------

.. var:: config.after_load_callbacks
.. var:: config.auto_load
.. var:: config.load_failed_label
.. var:: config.loadable_callback
.. var:: config.has_autosave
.. var:: config.save_directory
.. var:: config.save
.. var:: config.save_dump
.. var:: config.save_on_mobile_background
.. var:: config.save_persistent
.. var:: config.save_physical_size
.. var:: config.quicksave_slots
.. var:: config.autosave_callback
.. var:: config.autosave_prefix_callback
.. var:: config.autosave_slots
.. var:: config.autosave_frequency
.. var:: config.autosave_on_choice
.. var:: config.autosave_on_quit
.. var:: config.autosave_on_input
.. var:: config.save_json_callbacks
.. var:: config.save_token_keys
.. var:: config.file_slotname_callback
.. var:: config.thumbnail_height
.. var:: config.thumbnail_width

Screen Language
---------------

.. var:: config.always_shown_screens
.. var:: config.menu_clear_layers
.. var:: config.overlay_screens
.. var:: config.variants
.. var:: config.help
.. var:: config.help_screen
.. var:: config.keep_side_render_order
.. var:: config.imagemap_auto_function
.. var:: config.per_frame_screens
.. var:: config.transition_screens
.. var:: config.context_copy_remove_screens
.. var:: config.notify

Screenshots
-----------

.. var:: config.pre_screenshot_actions
.. var:: config.screenshot_callback
.. var:: config.screenshot_crop
.. var:: config.screenshot_pattern

Self-Voicing / Text to Speech
-----------------------------

.. var:: config.tts_voice
.. var:: config.tts_substitutions

Showing Images
--------------

.. var:: config.adjust_attributes
.. var:: config.default_attribute_callbacks
.. var:: config.speaking_attribute
.. var:: config.cache_surfaces
.. var:: config.conditionswitch_predict_all
.. var:: config.default_transform
.. var:: config.displayable_prefix
.. var:: config.image_cache_size
.. var:: config.image_cache_size_mb
.. var:: config.max_texture_size
.. var:: config.optimize_texture_bounds
.. var:: config.tag_transform
.. var:: config.tag_zorder
.. var:: config.keep_running_transform
.. var:: config.transform_uses_child_position
.. var:: config.predict_statements
.. var:: config.show
.. var:: config.hide
.. var:: config.scene

Skipping
--------

.. var:: config.skip_delay
.. var:: config.skip_indicator
.. var:: config.allow_skipping
.. var:: config.fast_skipping

Text and Fonts
--------------

.. var:: config.replace_text
.. var:: config.mipmap_text
.. var:: config.font_hinting
.. var:: config.font_name_map
.. var:: config.font_replacement_map
.. var:: config.new_substitutions
.. var:: config.say_menu_text_filter
.. var:: config.old_substitutions
.. var:: config.textshader_callbacks # Same as above
.. var:: config.hyperlink_handlers
.. var:: config.hyperlink_protocol
.. var:: config.preload_fonts

Transitions
-----------

.. var:: config.adv_nvl_transition
.. var:: config.after_load_transition
.. var:: config.end_game_transition
.. var:: config.end_splash_transition
.. var:: config.enter_replay_transition
.. var:: config.enter_transition
.. var:: config.enter_yesno_transition
.. var:: config.exit_replay_transition
.. var:: config.exit_transition
.. var:: config.exit_yesno_transition
.. var:: config.game_main_transition
.. var:: config.intra_transition
.. var:: config.nvl_adv_transition
.. var:: config.say_attribute_transition
.. var:: config.say_attribute_transition_callback
.. var:: config.say_attribute_transition_layer
.. var:: config.window_hide_transition
.. var:: config.window_show_transition
.. var:: config.pause_with_transition

Transition Control
------------------

.. var:: config.implicit_with_none
.. var:: config.overlay_during_with
.. var:: config.load_before_transition
.. var:: config.mipmap_dissolves

Translation
-----------

.. var:: config.default_language
.. var:: config.defer_styles
.. var:: config.defer_tl_scripts
.. var:: config.enable_language_autodetect
.. var:: config.locale_to_language_function
.. var:: config.new_translate_order
.. var:: config.translate_clean_stores
.. var:: config.translate_ignore_who


Voice
-----

.. var:: config.voice_filename_format
.. var:: config.auto_voice
.. var:: config.emphasize_audio_channels
.. var:: config.emphasize_audio_time
.. var:: config.emphasize_audio_volume

Window Management
-----------------

.. var:: config.window
.. var:: config.empty_window
.. var:: config.window_auto_hide
.. var:: config.window_auto_show
.. var:: config.choice_empty_window
.. var:: config.window_auto_hide
.. var:: config.window_auto_show
.. var:: config.choice_empty_window

Developer
---------

Compatibility
^^^^^^^^^^^^^

.. var:: config.label_overrides
.. var:: config.script_version

Development
^^^^^^^^^^^

.. var:: config.developer
.. var:: config.console

Debugging
^^^^^^^^^

.. var:: config.log
.. var:: config.log_events
.. var:: config.log_width
.. var:: config.clear_log
.. var:: config.missing_image_callback
.. var:: config.missing_label_callback
.. var:: config.return_not_found_label
.. var:: config.debug_image_cache
.. var:: config.debug_prediction
.. var:: config.debug_sound
.. var:: config.debug_text_overflow
.. var:: config.disable_input
.. var:: config.lint_character_statistics
.. var:: config.lint_hooks
.. var:: config.exception_handler
.. var:: config.raise_image_exceptions
.. var:: config.raise_image_load_exceptions
.. var:: config.profile
.. var:: config.profile_init

Garbage Collection
^^^^^^^^^^^^^^^^^^

.. var:: config.manage_gc
.. var:: config.gc_thresholds
.. var:: config.idle_gc_count
.. var:: config.gc_print_unreachable

Reload
^^^^^^

.. var:: config.autoreload
.. var:: config.reload_modules
