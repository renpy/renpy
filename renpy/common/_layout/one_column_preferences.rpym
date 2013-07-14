# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('preferences')

    # Load the common code.
    renpy.load_module("_layout/classic_preferences_common")

    # Create styles.
    style.prefs_column = Style(style.vbox, help="the single preferences column")

    style.prefs_frame.set_parent(style.menu_frame)
    style.prefs_pref_frame.set_parent(style.default)

    # Adjust styles.
    style.prefs_frame_box.box_layout = 'vertical'

    style.prefs_frame.xalign = 0.0
    style.prefs_frame.ypos = 10
    style.prefs_frame.xmargin = 10

    style.prefs_slider.xmaximum = 200
    style.prefs_slider.xalign = 1.0

    style.prefs_volume_slider.xmaximum = 200
    style.prefs_volume_slider.xalign = 1.0
    style.prefs_volume_box.xalign = 1.0
    style.prefs_volume_box.box_layout = 'horizontal'

    style.prefs_pref_box.xfill = True
    style.prefs_pref_box.box_layout = 'horizontal'
    style.prefs_pref_choicebox.box_layout = 'horizontal'
    style.prefs_pref_choicebox.xalign = 1.0

    style.prefs_jump.xfill = True

    style.prefs_column.box_spacing = 5

    style.soundtest_button.xalign = 1.0
    style.prefs_jump_button.xalign = 1.0

    config.translations["Fullscreen 16:9"] = "16:9"
    config.translations["Fullscreen 16:10"] = "16:10"

    config.soundtest_before_volume = True


    # Place preferences into groups.
    config.preferences['prefs_column'] = [
        config.all_preferences[u'Display'],
        config.all_preferences[u'Transitions'],
        config.all_preferences[u'Skip'],
        config.all_preferences[u'Begin Skipping'],
        config.all_preferences[u'After Choices'],
        config.all_preferences[u'Text Speed'],
        config.all_preferences[u'Auto-Forward Time'],
        config.all_preferences[u'Music Volume'],
        config.all_preferences[u'Sound Volume'],
        config.all_preferences[u'Voice Volume'],
        config.all_preferences[u'Joystick...'],
        ]


label preferences_screen:

    $ _prefs_screen_run(config.preferences)

    jump preferences_screen

