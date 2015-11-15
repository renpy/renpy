# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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
# WITH THE SOFTWARE OR THE USE

import renpy

pad_bindings = {
    "pad_leftshoulder_press" : [ "rollback", ],
    "pad_lefttrigger_pos" : [ "rollback", ],
    "pad_back_press" : [ "rollback", ],

    "pad_guide_press" : [ "game_menu", ],
    "pad_start_press" : [ "game_menu", ],

    "pad_y_press" : [ "hide_windows", ],

    "pad_rightshoulder_press" : [ "rollforward", ],

    "pad_righttrigger_press" : [ "dismiss", "button_select" ],
    "pad_a_press" : [ "dismiss", "button_select" ],
    "pad_b_press" : [ "button_alternate" ],

    "pad_dleft_press" : [ "focus_left", "bar_left" ],
    "pad_leftx_neg" : [ "focus_left", "bar_left" ],
    "pad_rightx_neg" : [ "focus_left", "bar_left" ],

    "pad_dpright_press" : [ "focus_right", "bar_right" ],
    "pad_leftx_pos" : [ "focus_right", "bar_right" ],
    "pad_rightx_pos" : [ "focus_right", "bar_right" ],

    "pad_dpup_press" : [ "focus_up", "bar_up" ],
    "pad_lefty_neg" :  [ "focus_up", "bar_up" ],
    "pad_righty_neg" : [ "focus_up", "bar_up" ],

    "pad_dpdown_press" : [ "focus_down", "bar_down" ],
    "pad_lefty_pos" : [ "focus_down", "bar_down" ],
    "pad_righty_pos" : [ "focus_down", "bar_down" ],
}

class Preferences(renpy.object.Object):
    """
    Stores preferences that will one day be persisted.
    """
    __version__ = 15

    def after_upgrade(self, version):
        if version < 1:
            self.mute_volumes = 0
        if version < 2:
            self.using_afm_enable = False
        if version < 3:
            self.physical_size = None
        if version < 4:
            self.renderer = "auto"
            self.performance_test = True
        if version < 5:
            self.language = None
        if version < 6:
            self.wait_voice = True
        if version < 7:
            self.voice_sustain = False
        if version < 8:
            self.mouse_move = False
        if version < 9:
            self.afm_after_click = False
        if version < 11:
            self.show_empty_window = True
        if version < 13:
            self.self_voicing = False
        if version < 14:
            self.emphasize_audio = False
        if version < 15:
            self.pad_enabled = True

    def __init__(self):
        self.fullscreen = False
        self.skip_unseen = False
        self.text_cps = 0
        self.afm_time = 0
        self.afm_enable = True
        self.voice_sustain = False
        self.mouse_move = False
        self.show_empty_window = True

        # Should we wait for the voice to stop?
        self.wait_voice = True

        # Should we disengage auto-forward mode after a click?
        self.afm_after_click = False

        # 2 - All transitions.
        # 1 - Only non-default transitions.
        # 0 - No transitions.
        self.transitions = 2

        self.skip_after_choices = False

        # Mixer channel info.

        # A map from channel name to the current volume (between 0 and 1).
        self.volumes = { }

        # True if the channel should not play music. False
        # otherwise. (Not used anymore.)
        self.mute = { }

        # Joystick mappings.
        self.joymap = dict()

        # The size of the window, or None if we don't know it yet.
        self.physical_size = None

        # The graphics renderer we use.
        self.renderer = "auto"

        # Should we do a performance test on startup?
        self.performance_test = True

        # The language we use for translations.
        self.language = None

        # Should we self-voice?
        self.self_voicing = False

        # Should we emphasize audio?
        self.emphasize_audio = False

        # Is the gamepad enabled?
        self.pad_enabled = True


    def set_volume(self, mixer, volume):
        if volume != 0:
            self.mute[mixer] = False

        self.volumes[mixer] = volume

    def get_volume(self, mixer):
        if mixer not in self.volumes:
            return 0.0

        if self.mute.get(mixer, False):
            return 0.0

        return self.volumes[mixer]

    def set_mute(self, mixer, mute):
        self.mute[mixer] = mute

        if (not mute) and (self.volumes.get(mixer, 1.0) == 0.0):
            self.volumes[mixer] = 1.0

    def get_mute(self, mixer):
        if mixer not in self.volumes:
            return False

        return self.mute[mixer]

    def init_mixers(self):
        for i in renpy.audio.music.get_all_mixers():
            self.volumes.setdefault(i, 1.0)
            self.mute.setdefault(i, False)

    def get_all_mixers(self):
        return renpy.audio.music.get_all_mixers()

    def __eq__(self, other):
        return True

renpy.game.Preferences = Preferences
renpy.game.preferences = Preferences()
