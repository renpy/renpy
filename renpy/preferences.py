# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import copy
import math

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
    "pad_lefty_neg" : [ "focus_up", "bar_up" ],
    "pad_righty_neg" : [ "focus_up", "bar_up" ],

    "pad_dpdown_press" : [ "focus_down", "bar_down" ],
    "pad_lefty_pos" : [ "focus_down", "bar_down" ],
    "pad_righty_pos" : [ "focus_down", "bar_down" ],
}

all_preferences = [ ]


class Preference(object):
    """
    Represents information about a preference.
    """

    def __init__(self, name, default, types=None):
        self.name = name
        self.default = default
        self.types = types if types else type(default)

        all_preferences.append(self)


Preference("fullscreen", False)
Preference("skip_unseen", False)
Preference("text_cps", 0, (int, float))
Preference("afm_time", 0, (int, float))
Preference("afm_enable", False)
Preference("using_afm_enable", False)
Preference("voice_sustain", False)
Preference("mouse_move", True)
Preference("show_empty_window", True)

# Should we wait for the voice to stop?
Preference("wait_voice", True)

# Should we disengage auto-forward mode after a click?
Preference("afm_after_click", False)

# 2 - All transitions.
# 1 - Only non-default transitions.
# 0 - No transitions.
Preference("transitions", 2)

# Should video sprites always default to provided displayables if possible?
Preference("video_image_fallback", False)

Preference("skip_after_choices", False)

# A map from channel name to the current volume (between 0 and 1).
Preference("volumes", { })

# Not used anymore.
Preference("mute", { })

# Joystick mappings.
Preference("joymap", { })

# The size of the window, or None if we don't know it yet.
Preference("physical_size", None, (tuple, type(None)))

# The virtual size at the time self.physical_size was set.
Preference("virtual_size", None, (tuple, type(None)))

# The graphics renderer we use.
Preference("renderer", "auto")

# Should we do a performance test on startup?
Preference("performance_test", True)

# The language we use for translations.
Preference("language", None, (str, type(None)))

# Should we self-voice?
Preference("self_voicing", False, (bool, str, type(None)))

# The amount to drop the volume of non-voice mixers when self voicing is
# enabled.
Preference("self_voicing_volume_drop", 0.5)

# Should we emphasize audio?
Preference("emphasize_audio", False)

# Is the gamepad enabled?
Preference("pad_enabled", True)

# The side of the screen used for rollback. ("left", "right", or "disable")
Preference("mobile_rollback_side", "disable")
Preference("desktop_rollback_side", "disable")

# Should OpenGL do npot?
Preference("gl_npot", True)

# Should we try to save power by limiting how often we draw frames?
Preference("gl_powersave", True)

# The target framerate, used to set the swap interval.
Preference("gl_framerate", None, (int, type(None)))

# Do we allow tearing?
Preference("gl_tearing", False)

# The font transformation used.
Preference("font_transform", None, (type(None), str))

# An adjustment applied to font size.
Preference("font_size", 1.0)

# An adjustment applied to font line spacing.
Preference("font_line_spacing", 1.0)

# Do we forcefully use a system cursor?
Preference("system_cursor", False)

# Do we force high contrast text?
Preference("high_contrast", False)

# Should sound continue playing when the window is minimized?
Preference("audio_when_minimized", True)

# Should sound continue playing when the window is not focused?
Preference("audio_when_unfocused", True)

# Should a progressive web app preload all files into the browser cache?
Preference("web_cache_preload", False)

# Should the voice continue to play after the user enters the game menu.
Preference("voice_after_game_menu", False)

# Should the game be maximized?
Preference("maximized", False)

class Preferences(renpy.object.Object):
    """
    Stores preferences that will one day be persisted.
    """
    __version__ = len(all_preferences) + 2

    # Default values, for typing purposes.
    if 1 == 0:

        fullscreen = False
        skip_unseen = False
        text_cps = 0
        afm_time = 0
        afm_enable = True
        using_afm_enable = False
        voice_sustain = False
        mouse_move = False
        show_empty_window = True
        wait_voice = True
        afm_after_click = False
        transitions = 2
        video_image_fallback = False
        skip_after_choices = False
        volumes = {}
        mute = {}
        joymap = {}
        physical_size = None
        virtual_size = None
        renderer = u'auto'
        performance_test = True
        language = None
        self_voicing = False
        self_voicing_volume_drop = 0.5
        emphasize_audio = False
        pad_enabled = True
        mobile_rollback_side = u'disable'
        desktop_rollback_side = u'disable'
        gl_npot = True
        gl_powersave = True
        gl_framerate = None
        gl_tearing = False
        font_transform = None
        font_size = 1.0
        font_line_spacing = 1.0
        system_cursor = False
        high_contrast = False
        audio_when_minimized = True
        audio_when_unfocused = True
        web_cache_preload = False
        voice_after_game_menu = False
        maximized = False

    def init(self):
        """
        Initializes the preference that have not been set.
        """

        for p in all_preferences:
            if not hasattr(self, p.name):
                setattr(self, p.name, copy.copy(p.default))

    def check(self):
        """
        Checks that preferences have the right types.
        """

        if self.gl_powersave == "auto":
            self.gl_powersave = True

        error = None

        for p in all_preferences:

            v = getattr(self, p.name, None)

            if isinstance(v, bytes):
                v = v.decode("utf-8")

            if not isinstance(v, p.types):
                error = "Preference {} has wrong type. {!r} is not of type {!r}.".format(p.name, v, p.types)
                setattr(self, p.name, copy.copy(p.default))

        return error

    def after_upgrade(self, version):
        self.init()

    def __init__(self):
        self.init()

    def set_volume(self, mixer, volume):
        if not renpy.config.preserve_volume_when_muted and volume != 0:
            self.mute[mixer] = False

        self.volumes[mixer] = volume

    def get_volume(self, mixer):
        if mixer not in self.volumes:
            return 0.0

        if not renpy.config.preserve_volume_when_muted and self.mute.get(mixer, False):
            return 0.0

        return self.volumes[mixer]

    def set_mixer(self, mixer, volume):
        if volume > 0:
            volume = renpy.config.volume_db_range * volume - renpy.config.volume_db_range
            volume = 10 ** (volume / 20)

        self.set_volume(mixer, volume)

    def get_mixer(self, mixer):
        rv = self.get_volume(mixer)

        if rv == 0:
            return 0

        rv = 20 * math.log10(rv)
        rv = (rv + renpy.config.volume_db_range) / renpy.config.volume_db_range

        return rv

    def set_mute(self, mixer, mute):
        self.mute[mixer] = mute

        if not renpy.config.preserve_volume_when_muted:
            if (not mute) and (self.volumes.get(mixer, 1.0) == 0.0):
                self.volumes[mixer] = 1.0

    def get_mute(self, mixer):
        if mixer not in self.volumes:
            return False

        return self.mute[mixer]

    def init_mixers(self):
        for i in renpy.audio.music.get_all_mixers() + ["main", "voice"]:
            self.volumes.setdefault(i, 1.0)
            self.mute.setdefault(i, False)

    def get_all_mixers(self):
        return renpy.audio.music.get_all_mixers()

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return not (self == other)


renpy.game.Preferences = Preferences # type: ignore
renpy.game.preferences = Preferences()
