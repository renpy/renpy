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

    ##########################################################################
    # Audio actions.

    @renpy.pure
    class Play(Action, FieldEquality):
        """
         :doc: audio_action

         Causes an audio file to be played on a given channel.

         `channel`
             The channel to play the sound on.
         `file`
             The file to play.
         `selected`
             If True, buttons using this action will be marked as selected
             if the file is playing on the channel. If False, this action
             will not cause the button to start playing. If None, the button
             is marked selected if the channel is a music channel, and not
             otherwise.

         Any other keyword arguments are passed to :func:`renpy.music.play`.
         """

        equality_fields = ["channel", "file", "kwargs", "can_be_selected" ]

        can_be_selected = False

        def __init__(self, channel, file, selected=None, **kwargs):
            self.channel = channel
            self.file = file
            self.kwargs = kwargs

            if selected is None:
                selected = renpy.music.is_music(channel)

            self.can_be_selected = selected
            self.get_selected()

        def __call__(self):
            renpy.music.play(self.file, channel=self.channel, **self.kwargs)
            renpy.restart_interaction()

        def get_selected(self):
            if not self.can_be_selected:
                self.selected = False
                return False

            self.selected = (renpy.music.get_playing(self.channel) == self.file)
            return self.selected

        def periodic(self, st):
            if not self.can_be_selected:
                return None

            if self.selected != (renpy.music.get_playing(self.channel) == self.file):
                renpy.restart_interaction()

            return .1


    @renpy.pure
    class Queue(Action, DictEquality):
        """
         :doc: audio_action

         Causes an audio file to be queued on a given channel.

         `channel`
             The channel to play the sound on.
         `file`
             The file to play.

         Any keyword arguments are passed to :func:`renpy.music.queue`
         """

        def __init__(self, channel, file, **kwargs):
            self.channel = channel
            self.file = file
            self.kwargs = kwargs

        def __call__(self):
            renpy.music.queue(self.file, channel=self.channel, **self.kwargs)
            renpy.restart_interaction()

    @renpy.pure
    class Stop(Action, DictEquality):
        """
         :doc: audio_action

         Causes an audio channel to be stopped.

         `channel`
             The channel to stop the sound on.

         Any keyword arguments are passed to :func:`renpy.music.stop`
         """

        def __init__(self, channel, **kwargs):
            self.channel = channel
            self.kwargs = kwargs

        def __call__(self):
            renpy.music.stop(channel=self.channel, **self.kwargs)
            renpy.restart_interaction()

    @renpy.pure
    class SetMixer(Action, DictEquality):
        """
        :doc: audio_action

        Sets the volume of `mixer` to `value`.

        `mixer`
            The mixer to set the volume of. A string, usually one of
            "music", "sfx", or "voice".
        `value`
            The value to set the volume to. A number between 0.0 and 1.0,
            inclusive.
        """

        def __init__(self, mixer, volume):
            self.mixer = mixer
            self.volume = volume

        def __call__(self):
            _preferences.set_volume(self.mixer, self.volume)
            renpy.restart_interaction()

        def get_selected(self):
            return _preferences.get_volume(self.mixer) == self.volume

    @renpy.pure
    class SetMute(Action, DictEquality):
        """
        :doc: audio_action

        Sets the mute status of one or more mixers. When a mixer is muted,
        audio channels associated with that mixer will stop playing audio.

        `mixer`
            Either a single string giving a mixer name, or a list of strings
            giving a list of mixers. The strings should be mixer names, usually
            "music", "sfx", or "voice".

        `mute`
            True to mute the mixer, False to ummute it.
        """


        def __init__(self, mixer, mute):
            if isinstance(mixer, basestring):
                mixer = [ mixer ]

            self.mixers = mixer
            self.mute = mute

        def __call__(self):
            for i in self.mixers:
                _preferences.set_mute(i, self.mute)

            renpy.restart_interaction()

        def get_selected(self):
            for i in self.mixers:
                if _preferences.get_mute(i) != self.mute:
                    return False

            return True

    @renpy.pure
    class ToggleMute(Action, DictEquality):
        """
        :doc: audio_action

        Toggles the mute status of one or more mixers.

        `mixer`
            Either a single string giving a mixer name, or a list of strings
            giving a list of mixers. The strings should be mixer names, usually
            "music", "sfx", or "voice".
        """


        def __init__(self, mixer):
            if isinstance(mixer, basestring):
                mixer = [ mixer ]

            self.mixers = mixer

        def __call__(self):
            mute = not self.get_selected()

            for i in self.mixers:
                _preferences.set_mute(i, mute)

            renpy.restart_interaction()

        def get_selected(self):
            for i in self.mixers:
                if not _preferences.get_mute(i):
                    return False

            return True


    @renpy.pure
    class PauseAudio(Action, DictEquality):
        """
        :doc: audio_action

        Sets the pause flag for `channel`.

        If `value` is True, the channel is paused. If False, the channel is
        unpaused. If "toggle", the pause flag will be toggled.
        """


        def __init__(self, channel, value=True):
            self.channel = channel
            self.value = value

        def __call__(self):
            if self.value == "toggle":
                renpy.music.set_pause(not renpy.music.get_pause(self.channel), channel=self.channel)
            else:
                renpy.music.set_pause(self.value, channel=self.channel)

            renpy.restart_interaction()

        def get_selected(self):
            rv = renpy.music.get_pause(channel=self.channel)

            if not self.value:
                rv = not rv

            return rv

