# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:

    ##########################################################################
    # Audio actions.

    class Play(Action):
        """
         :doc: audio_action

         Causes an audio file to be played on a given channel.

         `channel`
             The channel to play the sound on.
         `file`
             The file to play.

         Any keyword arguments are passed to :func:`renpy.music.play`
         """

        def __init__(self, channel, file, **kwargs):
            self.channel = channel
            self.file = file
            self.kwargs = kwargs
            self.selected = self.get_selected()

        def __call__(self):
            renpy.music.play(self.file, channel=self.channel, **self.kwargs)
            renpy.restart_interaction()

        def get_selected(self):
            return renpy.music.get_playing(self.channel) == self.file

        def periodic(self, st):
            if self.selected != self.get_selected():
                renpy.restart_interaction()

            return .1


    class Queue(Action):
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


    class Stop(Action):
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

    class SetMixer(Action):
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

