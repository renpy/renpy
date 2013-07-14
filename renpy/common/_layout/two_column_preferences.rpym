# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('preferences')

    # Load the common code.
    renpy.load_module("_layout/classic_preferences_common")

    # Create styles.
    style.prefs_column = Style(style.vbox, help="columns of preferences")
    style.prefs_left = Style(style.prefs_column, help="the left preference column")
    style.prefs_right = Style(style.prefs_column, help="the right preference column")

    style.prefs_left.xmaximum = 520
    style.prefs_right.xmaximum = 250

    style.prefs_left.xpos = 271
    style.prefs_left.xanchor = 0.5
    style.prefs_left.ypos = 10

    style.prefs_right.xpos = 667
    style.prefs_right.xanchor = 0.5
    style.prefs_right.ypos = 10

    style.prefs_slider.xmaximum = 400
    style.prefs_slider.xalign = 1.0

    style.prefs_volume_slider.xmaximum = 200
    style.prefs_volume_slider.xalign = 1.0

    style.prefs_pref_box.xfill = True
    style.prefs_pref_choicebox.box_layout = 'horizontal'
    style.prefs_pref_choicebox.xalign = 1.0
    style.prefs_volume_box.xalign = 1.0

    style.prefs_jump.xfill = True

    style.prefs_column.box_spacing = 5

    style.prefs_button.set_parent(style.small_button)
    style.prefs_button_text.set_parent(style.small_button_text)

    style.soundtest_button.xalign = 1.0
    style.prefs_jump_button.xalign = 1.0


    config.sample_voice = "18005551212.ogg"

    config.translations["Fullscreen 16:9"] = "16:9"
    config.translations["Fullscreen 16:10"] = "16:10"




    # Place preferences into groups.
    config.preferences['prefs_left'] = [
        config.all_preferences[u'Display'],
        config.all_preferences[u'Transitions'],
        config.all_preferences[u'Skip'],
        config.all_preferences[u'Begin Skipping'],
        config.all_preferences[u'After Choices'],
        config.all_preferences[u'Text Speed'],
        config.all_preferences[u'Auto-Forward Time'],
        ]

    config.preferences['prefs_right'] = [
        config.all_preferences[u'Music Volume'],
        config.all_preferences[u'Sound Volume'],
        config.all_preferences[u'Voice Volume'],
        config.all_preferences[u'Joystick...'],
        ]


label preferences_screen:

    $ _prefs_screen_run(config.preferences)

    jump preferences_screen

