# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

init -1500 python:

    @renpy.pure
    class __DisplayAction(Action, DictEquality):

        factor = 1.0

        def __init__(self, factor):
            self.factor = factor

        def get_size(self):

            width = renpy.config.physical_width or renpy.config.screen_width
            height = renpy.config.physical_height or renpy.config.screen_height

            w = int(self.factor * width)
            h = int(self.factor * height)

            rv = (w, h)

            max_window_size = renpy.get_renderer_info().get("max_window_size", rv)

            if w > max_window_size[0]:
                rv = max_window_size

            return rv

        def __call__(self):
            renpy.set_physical_size(self.get_size())
            renpy.restart_interaction()

        def get_sensitive(self):
            if self.factor == 1.0:
                return True

            return renpy.get_renderer_info()["resizable"]

        def get_selected(self):
            if _preferences.fullscreen:
                return False

            return self.get_size() == renpy.get_physical_size()

    _m1_00screen__DisplayAction = __DisplayAction


    @renpy.pure
    class __ResetPreferences(Action, DictEquality):

        def __call__(self):
            _preferences.reset()
            _preferences.init_mixers()
            persistent._preference_default = { }
            renpy.exports.execute_default_statement()
            _apply_default_preferences()
            renpy.restart_interaction()


    config.always_has_joystick = False

    @renpy.pure
    class _DisplayReset(Action, DictEquality):
        """
        Causes the display to restart after a preference that needs it has been
        changed.
        """

        def __call__(self):
            renpy.free_memory()
            renpy.display.interface.display_reset = True

    @renpy.pure
    def Preference(name, value=None, range=None):
        """
        :doc: preference_action

        This constructs the appropriate action or value from a preference.
        The preference name should be the name given in the standard
        menus, while the value should be either the name of a choice,
        "toggle" to cycle through choices, a specific value, or left off
        in the case of buttons.

        Actions that can be used with buttons and hotspots are:

        * Preference("display", "fullscreen") - displays in fullscreen mode.
        * Preference("display", "window") - displays in windowed mode at 1x normal size.
        * Preference("display", 2.0) - displays in windowed mode at 2.0x normal size.
        * Preference("display", "any window") - displays in windowed mode at the previous size.
        * Preference("display", "toggle") - toggle display mode.

        * Preference("transitions", "all") - show all transitions.
        * Preference("transitions", "none") - do not show transitions.
        * Preference("transitions", "toggle") - toggle transitions.

        * Preference("video sprites", "show") - show all video sprites.
        * Preference("video sprites", "hide") - fall back to images where possible.
        * Preference("video sprites", "toggle") - toggle image fallback behavior.

        * Preference("show empty window", "show") - Allow the "window show" and "window auto" statement to show an empty window outside of the say statement.
        * Preference("show empty window", "hide") - Prevent the above.
        * Preference("show empty window", "toggle") - Toggle the above.

        * Preference("text speed", 0) - make text appear instantaneously.
        * Preference("text speed", 142) - set text speed to 142 characters per second.

        * Preference("joystick") - Show the joystick preferences.

        * Preference("skip", "seen") - Only skip seen messages.
        * Preference("skip", "all") - Skip unseen messages.
        * Preference("skip", "toggle") - Toggle between skip seen and skip all.

        * Preference("begin skipping") - Starts skipping.

        * Preference("after choices", "skip") - Skip after choices.
        * Preference("after choices", "stop") - Stop skipping after choices.
        * Preference("after choices", "toggle") - Toggle skipping after choices.

        * Preference("auto-forward time", 0) - Set the auto-forward time to infinite.
        * Preference("auto-forward time", 10) - Set the auto-forward time (unit is seconds per 250 characters).

        * Preference("auto-forward", "enable") - Enable auto-forward mode.
        * Preference("auto-forward", "disable") - Disable auto-forward mode.
        * Preference("auto-forward", "toggle") - Toggle auto-forward mode.

        * Preference("auto-forward after click", "enable") - Remain in auto-forward mode after a click.
        * Preference("auto-forward after click", "disable") - Disable auto-forward mode after a click.
        * Preference("auto-forward after click", "toggle") - Toggle auto-forward after click.

        * Preference("automatic move", "enable") - Allow Ren'Py to move the mouse automatically using the :func:`MouseMove` action.
        * Preference("automatic move", "disable") - Disable the :func:`MouseMove` action.
        * Preference("automatic move", "toggle") - Toggle automatic mouse mode.

        * Preference("wait for voice", "enable")  - Wait for the currently playing voice to complete before auto-forwarding.
        * Preference("wait for voice", "disable") - Do not wait for the currently playing voice to complete before auto-forwarding.
        * Preference("wait for voice", "toggle")  - Toggle wait voice.

        * Preference("voice sustain", "enable")  - Sustain voice past the current interaction.
        * Preference("voice sustain", "disable") - Don't sustain voice past the current interaction.
        * Preference("voice sustain", "toggle")  - Toggle voice sustain.

        * Preference("music mute", "enable") - Mute the music mixer.
        * Preference("music mute", "disable") - Un-mute the music mixer.
        * Preference("music mute", "toggle") - Toggle music mute.

        * Preference("sound mute", "enable") - Mute the sound mixer.
        * Preference("sound mute", "disable") - Un-mute the sound mixer.
        * Preference("sound mute", "toggle") - Toggle sound mute.

        * Preference("voice mute", "enable") - Mute the voice mixer.
        * Preference("voice mute", "disable") - Un-mute the voice mixer.
        * Preference("voice mute", "toggle") - Toggle voice mute.

        * Preference("mixer <mixer> mute", "enable") - Mute the specified mixer.
        * Preference("mixer <mixer> mute", "disable") - Unmute the specified mixer.
        * Preference("mixer <mixer> mute", "toggle") - Toggle mute of the specified mixer.

        * Preference("all mute", "enable") - Mute each individual mixer.
        * Preference("all mute", "disable") - Unmute each individual mixer.
        * Preference("all mute", "toggle") - Toggle mute of each individual mixer.

        * Preference("main volume", 0.5) - Set the adjustment applied to all channels.
        * Preference("music volume", 0.5) - Set the music volume.
        * Preference("sound volume", 0.5) - Set the sound volume.
        * Preference("voice volume", 0.5) - Set the voice volume.
        * Preference("mixer <mixer> volume", 0.5) - Set the specified mixer volume.

        * Preference("emphasize audio", "enable") - Emphasize the audio channels found in :var:`config.emphasize_audio_channels`.
        * Preference("emphasize audio", "disable") - Do not emphasize audio channels.
        * Preference("emphasize audio", "toggle") - Toggle emphasize audio.

        * Preference("self voicing", "enable") - Enables self-voicing.
        * Preference("self voicing", "disable") - Disable self-voicing.
        * Preference("self voicing", "toggle") - Toggles self-voicing.

        * Preference("self voicing volume drop", 0.5) - Drops the volume of non-voice mixers when self voicing is active.

        * Preference("clipboard voicing", "enable") - Enables clipboard-voicing.
        * Preference("clipboard voicing", "disable") - Disable clipboard-voicing.
        * Preference("clipboard voicing", "toggle") - Toggles clipboard-voicing.

        * Preference("debug voicing", "enable") - Enables self-voicing debug
        * Preference("debug voicing", "disable") - Disable self-voicing debug.
        * Preference("debug voicing", "toggle") - Toggles self-voicing debug.

        * Preference("rollback side", "left") - Touching the left side of the screen causes rollback.
        * Preference("rollback side", "right") - Touching the right side of the screen causes rollback.
        * Preference("rollback side", "disable") - Touching the screen will not cause rollback.

        * Preference("gl powersave", True) - Drop framerate to allow for power savings.
        * Preference("gl powersave", False) - Do not drop framerate to allow for power savings.

        * Preference("gl framerate", None) - Runs at the display framerate.
        * Preference("gl framerate", 60) - Runs at the given framerate.

        * Preference("gl tearing", True) - Tears rather than skipping frames.
        * Preference("gl tearing", False) - Skips frames rather than tearing.

        * Preference("font transform", "opendyslexic") - Sets the accessibility font transform to opendyslexic.
        * Preference("font transform", "dejavusans") - Sets the accessibility font transform to deja vu sans.
        * Preference("font transform", None) - Disables the accessibility font transform.

        * Preference("font size", 1.0) - Sets the accessibility font size scaling factor.
        * Preference("font line spacing", 1.0) - Sets the accessibility font vertical spacing scaling factor.

        * Preference("system cursor", "disable") - Use the cursor defined in :var:`config.mouse` or :var:`config.mouse_displayable`.
        * Preference("system cursor", "enable") - Use the system cursor, ignoring :var:`config.mouse`.
        * Preference("system cursor", "toggle") - Toggle system cursor.

        * Preference("high contrast text", "enable") - Enables white text on a black background.
        * Preference("high contrast text", "disable") - Disables high contrast text.
        * Preference("high contrast text", "toggle") - Toggles high contrast text.

        * Preference("audio when minimized", "enable") - Enable sounds playing when the window has been minimized.
        * Preference("audio when minimized", "disable") - Disable sounds playing when the window has been minimized.
        * Preference("audio when minimized", "toggle") - Toggle sounds playing when the window has been minimized.

        * Preference("audio when unfocused", "enable") - Enable sounds playing when the window is not in focus.
        * Preference("audio when unfocused", "disable") - Disable sounds playing when the window is not in focus.
        * Preference("audio when unfocused", "toggle") - Toggle sounds playing when the window is not in focus.

        * Preference("web cache preload", "enable") - Will cause the web cache to be preloaded.
        * Preference("web cache preload", "disable") - Will cause the web cache to not be preloaded, and preloaded data to be deleted.
        * Preference("web cache preload", "toggle") - Will toggle the web cache preload state.

        * Preference("voice after game menu", "enable") - Will cause the voice to continue being played when entering the game  menu.
        * Preference("voice after game menu", "disable") - Will cause the voice to stop being played when entering the game menu.
        * Preference("voice after game menu", "toggle") - Will toggle the voice after game menu state.

        * Preference("restore window position", "enable") - Will cause the window position to be restored when the game is started.
        * Preference("restore window position", "disable") - Will cause the window position to not be restored when the game is started.
        * Preference("restore window position", "toggle") - Will toggle the restore window position state.

        Values that can be used with bars are:

        * Preference("text speed")
        * Preference("auto-forward time")
        * Preference("main volume")
        * Preference("music volume")
        * Preference("sound volume")
        * Preference("voice volume")
        * Preference("mixer <mixer> volume")
        * Preference("self voicing volume drop")
        * Preference("font size")
        * Preference("font line spacing")

        The `range` parameter can be given to give the range of certain bars.
        For "text speed", it defaults to 200 cps. For "auto-forward time", it
        defaults to 30.0 seconds per chunk of text. (These are maximums, not
        defaults.)

        Actions that can be used with buttons are:

        * Preference("renderer menu") - Show the renderer menu.
        * Preference("accessibility menu") - Show the accessibility menu.
        * Preference("reset") - Reset preferences to defaults.

        These screens are intended for internal use, and are not customizable.
        """

        name = name.lower()

        if isinstance(value, basestring):
            value = value.lower()

        def get():

            if name == _("display"):
                if value == "fullscreen":
                    if renpy.can_fullscreen():
                        return SetField(_preferences, "fullscreen", True)
                    else:
                        return None

                elif value == "window":
                    if renpy.variant("web"):
                        # Only fullscreen and non-fullscreen modes for Web
                        return SetField(_preferences, "fullscreen", False)
                    else:
                        return __DisplayAction(1.0)
                elif value == "any window":
                    return SetField(_preferences, "fullscreen", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "fullscreen")
                elif isinstance(value, (int, float)):
                    return __DisplayAction(value)

            elif name == _("transitions"):

                if value == "all":
                    return SetField(_preferences, "transitions", 2)
                elif value == "some":
                    return SetField(_preferences, "transitions", 1)
                elif value == "none":
                    return SetField(_preferences, "transitions", 0)
                elif value == "toggle":
                    return ToggleField(_preferences, "transitions", true_value=2, false_value=0), _("skip transitions")

            elif name == _("video sprites"):

                if value == "show":
                    return SetField(_preferences, "video_image_fallback", False)
                elif value == "hide":
                    return SetField(_preferences, "video_image_fallback", True)
                elif value == "toggle":
                    return ToggleField(_preferences, "video_image_fallback")

            elif name == _("show empty window"):

                if value == "show":
                    return SetField(_preferences, "show_empty_window", True)
                elif value == "hide":
                    return SetField(_preferences, "show_empty_window", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "show_empty_window")

            elif name == _("text speed"):

                if value is None:
                    bar_range = range or 200
                    return FieldValue(_preferences, "text_cps", range=bar_range * 1.0, max_is_zero=True, style="slider")
                elif isinstance(value, int):
                    return SetField(_preferences, "text_cps", value)

            elif name == _("joystick") or name == _("joystick..."):

                if renpy.display.joystick.enabled or config.always_has_joystick:
                    return ShowMenu("joystick_preferences")
                else:
                    return None

            elif name == _("skip"):

                if value == "all messages" or value == "all":
                    return SetField(_preferences, "skip_unseen", True), _("skip unseen [text]")

                elif value == "seen messages" or value == "seen":
                    return SetField(_preferences, "skip_unseen", False), _("skip unseen [text]")
                elif value == "toggle":
                    return ToggleField(_preferences, "skip_unseen"), _("skip unseen text")

            elif name == _("begin skipping"):

                return Skip()

            elif name == _("after choices"):

                if value == "keep skipping" or value == "keep" or value == "skip":
                    return SetField(_preferences, "skip_after_choices", True)
                elif value == "stop skipping" or value == "stop":
                    return SetField(_preferences, "skip_after_choices", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "skip_after_choices"), _("skip after choices")

            elif name == _("auto-forward time"):

                if value is None:

                    bar_range = range or 30.0

                    if config.default_afm_enable is None:
                        return FieldValue(_preferences, "afm_time", range=bar_range, max_is_zero=True, style="slider")
                    else:
                        return FieldValue(_preferences, "afm_time", range=bar_range - .1, style="slider", offset=.1)

                elif isinstance(value, int):
                    return SetField(_preferences, "afm_time", value)

            elif name == _("auto-forward"):

                if value == "enable":
                    return SetField(_preferences, "afm_enable", True)
                elif value == "disable":
                    return SetField(_preferences, "afm_enable", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "afm_enable"), _("Auto forward")


            elif name == _("auto-forward after click"):

                if value == "enable":
                    return SetField(_preferences, "afm_after_click", True)
                elif value == "disable":
                    return SetField(_preferences, "afm_after_click", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "afm_after_click")

            elif name == _("automatic move"):

                if value == "enable":
                    return SetField(_preferences, "mouse_move", True)
                elif value == "disable":
                    return SetField(_preferences, "mouse_move", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "mouse_move")

            elif name == _("wait for voice"):

                if value == "enable":
                    return SetField(_preferences, "wait_voice", True)
                elif value == "disable":
                    return SetField(_preferences, "wait_voice", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "wait_voice")

            elif name == _("voice sustain"):

                if value == "enable":
                    return SetField(_preferences, "voice_sustain", True)
                elif value == "disable":
                    return SetField(_preferences, "voice_sustain", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "voice_sustain")

            elif name == _("self voicing"):

                if value == "enable":
                    return SetField(_preferences, "self_voicing", True), _("self voicing enable")
                elif value == "disable":
                    return SetField(_preferences, "self_voicing", False), _("self voicing disable")
                elif value == "toggle":
                    return ToggleField(_preferences, "self_voicing", true_value=True, false_value=False)

            elif name == _("self voicing volume drop"):

                if value is None:
                    bar_range = range or 1.0
                    return FieldValue(_preferences, "self_voicing_volume_drop", range=1.0, style="slider")

                return SetField(_preferences, "self_voicing_volume_drop", value)

            elif name == _("clipboard voicing"):

                if value == "enable":
                    return SetField(_preferences, "self_voicing", "clipboard"), _("clipboard voicing enable")
                elif value == "disable":
                    return SetField(_preferences, "self_voicing", False), _("clipboard voicing disable")
                elif value == "toggle":
                    return ToggleField(_preferences, "self_voicing", true_value="clipboard", false_value=False)

            elif name == _("debug voicing"):

                if value == "enable":
                    return SetField(_preferences, "self_voicing", "debug"), _("debug voicing enable")
                elif value == "disable":
                    return SetField(_preferences, "self_voicing", False), _("debug voicing disable")
                elif value == "toggle":
                    return ToggleField(_preferences, "self_voicing", true_value="debug", false_value=False)

            elif name == _("emphasize audio"):

                if value == "enable":
                    return SetField(_preferences, "emphasize_audio", True)
                elif value == "disable":
                    return SetField(_preferences, "emphasize_audio", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "emphasize_audio")

            elif name == _("rollback side"):

                if value in [ "left", "right", "disable" ]:
                    if renpy.variant("mobile"):
                        field = "mobile_rollback_side"
                    else:
                        field = "desktop_rollback_side"

                    return SetField(_preferences, field, value)

            elif name == _("gl powersave"):
                if value == "toggle":
                    return [ ToggleField(_preferences, "gl_powersave"), _DisplayReset() ]
                else:
                    return [ SetField(_preferences, "gl_powersave", value), _DisplayReset() ]

            elif name == _("gl framerate"):
                return [ SetField(_preferences, "gl_framerate", value), _DisplayReset() ]

            elif name == _("gl tearing"):
                return [ SetField(_preferences, "gl_tearing", value), _DisplayReset() ]

            elif name == _("font transform"):
                return [ SetField(_preferences, "font_transform", value), _DisplayReset() ]

            elif name == _("font size"):

                if value is None:
                    bar_range = range or 1.0
                    return FieldValue(_preferences, "font_size", range=bar_range, style="slider", offset=.5, action=_DisplayReset())

                return [ SetField(_preferences, "font_size", value), _DisplayReset() ]

            elif name == _("font line spacing"):

                if value is None:
                    bar_range = range or 1.0
                    return FieldValue(_preferences, "font_line_spacing", range=bar_range, style="slider", offset=.5, action=_DisplayReset())

                return [ SetField(_preferences, "font_line_spacing", value), _DisplayReset() ]

            elif name == _("system cursor"):

                if value == "enable":
                    return SetField(_preferences, "system_cursor", True)
                elif value == "disable":
                    return SetField(_preferences, "system_cursor", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "system_cursor")

            elif name == _("renderer menu"):
                return renpy.curried_call_in_new_context("_choose_renderer")

            elif name == _("accessibility menu"):
                return ToggleScreen("_accessibility")

            elif name == _("high contrast text"):

                if value == "enable":
                    return [ SetField(_preferences, "high_contrast", True), _DisplayReset() ]
                elif value == "disable":
                    return [ SetField(_preferences, "high_contrast", False), _DisplayReset() ]
                elif value == "toggle":
                    return [ ToggleField(_preferences, "high_contrast"), _DisplayReset() ]

            elif name == _("audio when minimized"):

                if value == "enable":
                    return SetField(_preferences, "audio_when_minimized", True)
                elif value == "disable":
                    return SetField(_preferences, "audio_when_minimized", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "audio_when_minimized")

            elif name == _("audio when unfocused"):

                if value == "enable":
                    return SetField(_preferences, "audio_when_unfocused", True)
                elif value == "disable":
                    return SetField(_preferences, "audio_when_unfocused", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "audio_when_unfocused")

            elif name == _("web cache preload"):

                if not renpy.emscripten:
                    return None

                if value == "enable":
                    return [ SetField(_preferences, "web_cache_preload", True), ExecJS("loadCache()") ]
                elif value == "disable":
                    return [ SetField(_preferences, "web_cache_preload", False), ExecJS("clearCache()") ]
                elif value == "toggle":
                    if _preferences.web_cache_preload:
                        return Preference("web cache preload", "disable")
                    else:
                        return Preference("web cache preload", "enable")

            elif name == _("voice after game menu"):

                if value == "enable":
                    return SetField(_preferences, "voice_after_game_menu", True)
                elif value == "disable":
                    return SetField(_preferences, "voice_after_game_menu", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "voice_after_game_menu")

            elif name == _("restore window position"):

                if value == "enable":
                    return SetField(_preferences, "restore_window_position", True)
                elif value == "disable":
                    return SetField(_preferences, "restore_window_position", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "restore_window_position")

            elif name == _("reset"):
                return __ResetPreferences()

            mixer_names = {
                "main" : "main",
                "music" : "music",
                "sound" : "sfx",
                "voice" : "voice",
                "all" : _preferences.get_all_mixers() + ["main"],
            }

            # Make these available to the translation system
            if False:
                _("main volume")
                _("music volume")
                _("sound volume")
                _("voice volume")
                _("mute main")
                _("mute music")
                _("mute sound")
                _("mute voice")
                _("mute all")

            n = name.split()

            if n[-1] == "volume":
                if len(n) == 3 and n[0] == "mixer":
                    alt = n[1] + " volume"
                    mixer = n[1]
                elif len(n) == 2:
                    alt = n[0] + " volume"
                    mixer = mixer_names.get(n[0], n[0])

                if value is None:
                    return MixerValue(mixer), alt
                else:
                    return SetMixer(mixer, value), __(alt) + " [text]"

            if n[-1] == "mute":
                if len(n) == 3 and n[0] == "mixer":
                    alt = "mute " + n[1]
                    mixer = n[1]
                elif len(n) == 2:
                    alt = "mute " + n[0]
                    mixer = mixer_names.get(n[0], n[0])

                if value == "enable":
                    return SetMute(mixer, True), __(alt) + " [text]"
                elif value == "disable":
                    return SetMute(mixer, False), __(alt) + " [text]"
                elif value == "toggle":
                    return ToggleMute(mixer), alt

            else:
                raise Exception("Preference(%r, %r) is unknown." % (name , value))

        rv = get()

        if rv is not None:

            if isinstance(rv, tuple):
                rv, alt = rv
            else:
                alt = None

            if alt is not None:
                alt = __(alt)
            else:
                alt = __(name) + " [text]"

            if isinstance(rv, list):
                rv[0].alt = alt
            else:
                rv.alt = alt




        return rv


    def __show_self_voicing():
        has_screen = renpy.get_screen("_self_voicing")

        if _preferences.self_voicing and not has_screen:
            renpy.show_screen("_self_voicing")
        elif not _preferences.self_voicing and has_screen:
            renpy.hide_screen("_self_voicing")


    config.interact_callbacks.append(__show_self_voicing)

    # Ignored.
    config.self_voicing_stops_afm = False


init -1500:

    # The screen that we use to indicate that self-voicing is enabled.
    screen _self_voicing():
        zorder 1500

        if _preferences.self_voicing == "clipboard":
            $ message = _("Clipboard voicing enabled. Press 'shift+C' to disable.")
        elif _preferences.self_voicing == "debug":
            $ message = _("Self-voicing would say \"[renpy.display.tts.last]\". Press 'alt+shift+V' to disable.")
        else:
            $ message = _("Self-voicing enabled. Press 'v' to disable.")

        text message:
            alt ""

            xpos 10
            ypos 35
            color "#fff"
            outlines [ (1, "#0008", 0, 0)]
