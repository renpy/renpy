# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

class Preferences(renpy.object.Object):
    """
    Stores preferences that will one day be persisted.
    """
    __version__ = 11

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
        self.joymap = dict(
            joy_left="Axis 0.0 Negative",
            joy_right="Axis 0.0 Positive",
            joy_up="Axis 0.1 Negative",
            joy_down="Axis 0.1 Positive",
            joy_dismiss="Button 0.0")

        # The size of the window, or None if we don't know it yet.
        self.physical_size = None

        # The graphics renderer we use.
        self.renderer = "auto"

        # Should we do a performance test on startup?
        self.performance_test = True

        # The language we use for translations.
        self.language = None

    def set_volume(self, mixer, volume):
        self.volumes[mixer] = volume

    def get_volume(self, mixer):
        return self.volumes.get(mixer, 0)

    def set_mute(self, mixer, mute):
        self.mute[mixer] = mute

    def get_mute(self, mixer):
        return self.mute[mixer]

    def __eq__(self, other):
        return True

renpy.game.Preferences = Preferences
renpy.game.preferences = Preferences()
