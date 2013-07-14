# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('preferences')

    # Load the common code.
    renpy.load_module("_layout/classic_preferences_common")

    # Create styles.
    style.prefs_column = Style(style.vbox, help="preference columns")
    style.prefs_left = Style(style.prefs_column, help="the left preference column")
    style.prefs_center = Style(style.prefs_column, help="the center preference column")
    style.prefs_right = Style(style.prefs_column, help="the right preference column")

    # Customize styles.
    style.prefs_pref_frame.xfill = True
    style.prefs_column.xanchor = 0.5

    if config.screen_width <= 640:
        style.prefs_pref_box.box_spacing = 6

        style.prefs_column.xmaximum = 200
        style.prefs_column.box_spacing = 5
        style.prefs_frame.top_margin = 5

        style.prefs_left.xpos = 110
        style.prefs_center.xpos = 320
        style.prefs_right.xpos = 530

        style.prefs_slider.xmaximum = 160

    else:
        style.prefs_pref_box.box_spacing = 12

        style.prefs_column.xmaximum = 250
        style.prefs_column.box_spacing = 10
        style.prefs_frame.top_margin = 10

        style.prefs_left.xpos = 137
        style.prefs_center.xpos = 400
        style.prefs_right.xpos = 663

        style.prefs_slider.xmaximum = 200

    style.prefs_pref_box.xfill = True
    style.prefs_volume_box.xfill = True
    style.prefs_pref_choicebox.xfill = True
    style.prefs_button.xalign = 1.0
    style.prefs_jump_button.xalign = 1.0
    style.prefs_slider.xalign = 1.0
    style.soundtest_button.xalign = 1.0

    style.prefs_button.size_group = "prefs"
    style.prefs_jump_button.size_group = "prefs"

    # Place preferences into groups.
    config.preferences['prefs_left'] = [
        config.all_preferences[u'Display'],
        config.all_preferences[u'Transitions'],
        config.all_preferences[u'Text Speed'],
        config.all_preferences[u'Joystick...'],
        ]

    config.preferences['prefs_center'] = [
        config.all_preferences[u'Skip'],
        config.all_preferences[u'Begin Skipping'],
        config.all_preferences[u'After Choices'],
        config.all_preferences[u'Auto-Forward Time'],
        ]

    config.preferences['prefs_right'] = [
        config.all_preferences[u'Music Volume'],
        config.all_preferences[u'Sound Volume'],
        config.all_preferences[u'Voice Volume'],
        ]


label preferences_screen:

    python hide:
        _prefs_screen_run(config.preferences)

    jump preferences_screen

