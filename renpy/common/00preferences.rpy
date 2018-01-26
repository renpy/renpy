# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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
        def __init__(self, factor):
            self.width = int(factor * config.screen_width)
            self.height = int(factor * config.screen_height)

        def __call__(self):
            renpy.set_physical_size((self.width, self.height))
            renpy.restart_interaction()

        def get_sensitive(self):
            if self.width == config.screen_width and self.height == config.screen_height:
                return True

            return renpy.get_renderer_info()["resizable"]

        def get_selected(self):
            if _preferences.fullscreen:
                return False

            return (self.width, self.height) == renpy.get_physical_size()

    _m1_00screen__DisplayAction = __DisplayAction

    config.always_has_joystick = False

    @renpy.pure
    class _DisplayReset(Action, DictEquality):
        """
        Causes the display to restart after a preference that needs it has been
        changed.
        """

        def __call__(self):
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

         * Preference("automatic move", "enable") - Enable automatic mouse mode.
         * Preference("automatic move", "disable") - Disable automatic mouse mode.
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
         * Preference("mixer <mixer> mute", "toggle") - Toggle mute of specified mixer.

         * Preference("all mute", "enable") - Mute all mixers.
         * Preference("all mute", "disable") - Unmute all mixers.
         * Preference("all mute", "toggle") - Toggle mute of all mixers.

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

         * Preference("clipboard voicing", "enable") - Enables clipboard-voicing.
         * Preference("clipboard voicing", "disable") - Disable clipboard-voicing.
         * Preference("clipboard voicing", "toggle") - Toggles clipboard-voicing.

         * Preference("debug voicing", "enable") - Enables self.-voicing debug
         * Preference("debug voicing", "disable") - Disable self-voicing debug.
         * Preference("debug voicing", "toggle") - Toggles self-voicing debug.

         * Preference("rollback side", "left") - Touching the left side of the screen causes rollback.
         * Preference("rollback side", "right") - Touching the right side of the screen causes rollback.
         * Preference("rollback side", "disable") - Touching the screen will not cause rollback.

         * Preference("gl powersave", True) - Drop framerate to allow for power savings.
         * Preference("gl powersave", False) - Do not drop framerate to allow for power savings.
         * Preference("gl powersave", "auto") - Enable powersave when running on battery.

         * Preference("gl framerate", None) - Runs at the display framerate.
         * Preference("gl framerate", 60) - Runs at the given framerate.

         * Preference("gl tearing", True) - Tears rather than skipping frames.
         * Preference("gl tearing", False) - Skips frames rather than tearing.

         Values that can be used with bars are:

         * Preference("text speed")
         * Preference("auto-forward time")
         * Preference("music volume")
         * Preference("sound volume")
         * Preference("voice volume")
         * Preference("mixer <mixer> volume")

         The `range` parameter can be given to give the range of certain bars.
         For "text speed", it defaults to 200 cps. For "auto-forward time", it
         defaults to 30.0 seconds per chunk of text. (These are maximums, not
         defaults.)
         """

        name = name.lower()

        if isinstance(value, basestring):
            value = value.lower()

        def get():

            if name == "display":
                if value == "fullscreen":
                    return SetField(_preferences, "fullscreen", True)
                elif value == "window":
                    return __DisplayAction(1.0)
                elif value == "any window":
                    return SetField(_preferences, "fullscreen", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "fullscreen")
                elif isinstance(value, (int, float)):
                    return __DisplayAction(value)

            elif name == "transitions":

                if value == "all":
                    return SetField(_preferences, "transitions", 2)
                elif value == "some":
                    return SetField(_preferences, "transitions", 1)
                elif value == "none":
                    return SetField(_preferences, "transitions", 0)
                elif value == "toggle":
                    return ToggleField(_preferences, "transitions", true_value=2, false_value=0)

            elif name == "video sprites":

                if value == "show":
                    return SetField(_preferences, "video_image_fallback", False)
                elif value == "hide":
                    return SetField(_preferences, "video_image_fallback", True)
                elif value == "toggle":
                    return ToggleField(_preferences, "video_image_fallback")

            elif name == "show empty window":

                if value == "show":
                    return SetField(_preferences, "show_empty_window", True)
                elif value == "hide":
                    return SetField(_preferences, "show_empty_window", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "show_empty_window")

            elif name == "text speed":

                if value is None:
                    bar_range = range or 200
                    return FieldValue(_preferences, "text_cps", range=bar_range * 1.0, max_is_zero=True, style="slider")
                elif isinstance(value, int):
                    return SetField(_preferences, "text_cps", value)

            elif name == "joystick" or name == "joystick...":

                if renpy.display.joystick.enabled or config.always_has_joystick:
                    return ShowMenu("joystick_preferences")
                else:
                    return None

            elif name == "skip":

                if value == "all messages" or value == "all":
                    return SetField(_preferences, "skip_unseen", True)
                elif value == "seen messages" or value == "seen":
                    return SetField(_preferences, "skip_unseen", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "skip_unseen")

            elif name == "begin skipping":

                return Skip()

            elif name == "after choices":

                if value == "keep skipping" or value == "keep" or value == "skip":
                    return SetField(_preferences, "skip_after_choices", True)
                elif value == "stop skipping" or value == "stop":
                    return SetField(_preferences, "skip_after_choices", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "skip_after_choices")

            elif name == "auto-forward time":

                if value is None:

                    bar_range = range or 30.0

                    if config.default_afm_enable is None:
                        return FieldValue(_preferences, "afm_time", range=bar_range, max_is_zero=True, style="slider")
                    else:
                        return FieldValue(_preferences, "afm_time", range=bar_range - .1, style="slider", offset=.1)

                elif isinstance(value, int):
                    return SetField(_preferences, "afm_time", value)

            elif name == "auto-forward":

                if value == "enable":
                    return SetField(_preferences, "afm_enable", True)
                elif value == "disable":
                    return SetField(_preferences, "afm_enable", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "afm_enable")

            elif name == "auto-forward after click":

                if value == "enable":
                    return SetField(_preferences, "afm_after_click", True)
                elif value == "disable":
                    return SetField(_preferences, "afm_after_click", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "afm_after_click")

            elif name == "automatic move":

                if value == "enable":
                    return SetField(_preferences, "mouse_move", True)
                elif value == "disable":
                    return SetField(_preferences, "mouse_move", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "mouse_move")

            elif name == "wait for voice":

                if value == "enable":
                    return SetField(_preferences, "wait_voice", True)
                elif value == "disable":
                    return SetField(_preferences, "wait_voice", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "wait_voice")

            elif name == "voice sustain":

                if value == "enable":
                    return SetField(_preferences, "voice_sustain", True)
                elif value == "disable":
                    return SetField(_preferences, "voice_sustain", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "voice_sustain")

            elif name == "self voicing":

                if value == "enable":
                    return SetField(_preferences, "self_voicing", True)
                elif value == "disable":
                    return SetField(_preferences, "self_voicing", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "self_voicing")

            elif name == "clipboard voicing":

                if value == "enable":
                    return SetField(_preferences, "self_voicing", "clipboard")
                elif value == "disable":
                    return SetField(_preferences, "self_voicing", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "self_voicing", true_value="clipboard")

            elif name == "debug voicing":

                if value == "enable":
                    return SetField(_preferences, "self_voicing", "debug")
                elif value == "disable":
                    return SetField(_preferences, "self_voicing", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "self_voicing", true_value="debug")

            elif name == "emphasize audio":

                if value == "enable":
                    return SetField(_preferences, "emphasize_audio", True)
                elif value == "disable":
                    return SetField(_preferences, "emphasize_audio", False)
                elif value == "toggle":
                    return ToggleField(_preferences, "emphasize_audio")

            elif name == "rollback side":

                if value in [ "left", "right", "disable" ]:
                    if renpy.mobile:
                        field = "mobile_rollback_side"
                    else:
                        field = "desktop_rollback_side"

                    return SetField(_preferences, field, value)

            elif name == "gl powersave":
                if value == "toggle":
                    return [ ToggleField(_preferences, "gl_powersave"), _DisplayReset() ]
                else:
                    return [ SetField(_preferences, "gl_powersave", value), _DisplayReset() ]

            elif name == "gl framerate":
                return [ SetField(_preferences, "gl_framerate", value), _DisplayReset() ]

            elif name == "gl tearing":
                return [ SetField(_preferences, "gl_tearing", value), _DisplayReset() ]

            mixer_names = {
                "music" : "music",
                "sound" : "sfx",
                "voice" : "voice",
                "all" : _preferences.get_all_mixers(),
            }

            n = name.split()

            if n[-1] == "volume":
                if len(n) == 3 and n[0] == "mixer":
                    mixer = n[1]
                elif len(n) == 2:
                    mixer = mixer_names.get(n[0], n[0])

                if value is None:
                    return MixerValue(mixer)
                else:
                    return SetMixer(mixer, value)

            if n[-1] == "mute":
                if len(n) == 3 and n[0] == "mixer":
                    mixer = n[1]
                elif len(n) == 2:
                    mixer = mixer_names.get(n[0], n[0])

                if value == "enable":
                    return SetMute(mixer, True)
                elif value == "disable":
                    return SetMute(mixer, False)
                elif value == "toggle":
                    return ToggleMute(mixer)

            else:
                raise Exception("Preference(%r, %r) is unknown." % (name , value))

        rv = get()

        if rv is not None:
            rv.alt = name + " [text]"

        return rv


    def __show_self_voicing():
        has_screen = renpy.get_screen("_self_voicing")

        if _preferences.self_voicing and not has_screen:
            renpy.show_screen("_self_voicing")
        elif not _preferences.self_voicing and has_screen:
            renpy.hide_screen("_self_voicing")

        if _preferences.self_voicing and config.self_voicing_stops_afm:
            if _preferences.using_afm_enable:
                _preferences.afm_enable = False
            else:
                _preferences.afm_time = 0

    config.interact_callbacks.append(__show_self_voicing)

init -1500 python:

    import os
    config.self_voicing_stops_afm = not ("RENPY_SELF_VOICING_AFM" in os.environ)


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
