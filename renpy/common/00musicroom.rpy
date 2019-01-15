# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains the code to implement Ren'Py's music room function,
# which consists of the ability to set up a playlist (the aforementioned
# "music room"), and then a series of actions that let the player
# navigate through the music room.

init -1500 python:

    @renpy.pure
    class __MusicRoomPlay(Action, FieldEquality):
        """
        The action returned by MusicRoom.Play when called with a file.
        """

        identity_fields = [ "mr" ]
        equality_fields = [ "filename" ]

        def __init__(self, mr, filename):
            self.mr = mr
            self.filename = filename
            self.selected = self.get_selected()

        def __call__(self):
            self.mr.play(self.filename, 0)

        def get_sensitive(self):
            return self.mr.is_unlocked(self.filename)

        def get_selected(self):
            return renpy.music.get_playing(self.mr.channel) == self.filename

        def periodic(self, st):
            if self.selected != self.get_selected():
                self.selected = self.get_selected()
                renpy.restart_interaction()

            self.mr.periodic(st)

            return .1

    @renpy.pure
    class __MusicRoomRandomPlay(Action, FieldEquality):
        """
        The action returned by MusicRoom.RandomPlay
        """

        identity_fields = [ "mr" ]

        def __init__(self, mr):
            self.mr = mr

        def __call__(self):
            playlist = self.mr.unlocked_playlist()

            if not playlist:
                return

            self.mr.shuffled = None
            self.mr.play(renpy.random.choice(playlist), 0)

    @renpy.pure
    class __MusicRoomTogglePlay(Action, FieldEquality):
        """
        The action returned by MusicRoom.TogglePlay
        """

        identity_fields = [ "mr" ]

        def __init__(self, mr):
            self.mr = mr

        def __call__(self):
            if renpy.music.get_playing(self.mr.channel):
                return self.mr.stop()

            self.mr.shuffled = None
            return self.mr.play()

        def get_selected(self):
            return renpy.music.get_playing(self.mr.channel) is not None


    @renpy.pure
    class __MusicRoomStop(Action, FieldEquality):
        """
        The action returned by MusicRoom.Stop.
        """

        identity_fields = [ "mr" ]

        def __init__(self, mr):
            self.mr = mr
            self.selected = self.get_selected()

        def __call__(self):
            self.mr.stop()

        def get_selected(self):
            return renpy.music.get_playing() is None

        def periodic(self, st):
            if self.selected != self.get_selected():
                self.selected = self.get_selected()
                renpy.restart_interaction()

            self.mr.periodic(st)

            return .1


    class MusicRoom(object):
        """
        :doc: music_room class

        A music room that contains a series of songs that can be unlocked
        by the user, and actions that can play entries from the list in
        order.
        """

        loop = False

        loop_compat = False

        def __init__(self, channel="music", fadeout=0.0, fadein=0.0, loop=True, single_track=False, shuffle=False, stop_action=None):
            """
            `channel`
                The channel that this music room will operate on.

            `fadeout`
                The number of seconds it takes to fade out the old
                music when changing tracks.

            `fadein`
                The number of seconds it takes to fade in the new
                music when changing tracks.

            `loop`
                Determines if playback will loop or stop when it reaches
                the end of the playlist.

            `single_track`
                If true, only a single track will play. If loop is true,
                that track will loop. Otherwise, playback will stop when the
                track finishes.

            `shuffle`
                If true, the tracks are shuffled, and played in the shuffled
                order. If false, the tracks are played in the order they're
                added to the MusicRoom.

            `stop_action`
                An action to run when the music has stopped.

            Single_track and shuffle conflict with each other. Only one should
            be true at a time. (Actions that set single_track and shuffle
            enforce this.)
            """

            self.channel = channel
            self.fadeout = fadeout
            self.fadein = fadein

            # A map from track name (or "" for stopped) to the appropriate
            # action.
            self.action = { "" : stop_action }

            # The last track playing, or "" if we've been stopped.
            self.last_playing = None

            # The list of strings giving the titles of songs that make up the
            # playlist.
            self.playlist = [ ]

            # A shuffled copy of the playlist. (Created on demand when we
            # need it.)
            self.shuffled = None

            # A set of filenames, so we can quickly check if a valid filename
            # has been provided.
            self.filenames = set()

            # The set of songs that are always unlocked.
            self.always_unlocked = set()

            # Should we loop a single track rather than advancing to the next
            # track?
            self.loop = loop

            # Should we play a single track?
            self.single_track = single_track

            # Should we shuffle the playlist?
            if self.single_track:
                self.shuffle = False
            else:
                self.shuffle = shuffle

            # In older versions, loop would loop a single trak.
            if self.loop_compat and loop:
                self.single_track = True

            # The last shown time for the music room.
            self.st = -1

        def periodic(self, st):

            if st == self.st:
                return
            elif st < self.st:
                self.last_playing = None

            self.st = st

            current_playing = renpy.music.get_playing(self.channel)
            if current_playing is None:
                current_playing = ""

            if self.last_playing != current_playing:
                action = self.action.get(current_playing, None)
                renpy.run_action(action)

                self.last_playing = current_playing

        def add(self, filename, always_unlocked=False, action=None):
            """
            :doc: music_room method

            Adds the music file `filename` to this music room. The music room
            will play unlocked files in the order that they are added to the
            room.

            `always_unlocked`
                If true, the music file will be always unlocked. This allows
                the file to show up in the music room before it has been
                played in the game.

            `action`
                This is a action or the list of actions. these are called when this
                file is played.

                For example, These actions is used to change a screen or background, description
                by the playing file.
            """

            self.playlist.append(filename)
            self.filenames.add(filename)

            if action:
                self.action[filename] = action

            if always_unlocked:
                self.always_unlocked.add(filename)

        def is_unlocked(self, filename):
            """
            :doc: music_room method

            Returns true if the filename has been unlocked (or is always
            unlocked), and false if it is still locked.
            """

            if filename in self.always_unlocked:
                return True

            return renpy.seen_audio(filename)

        def unlocked_playlist(self, filename=None):
            """
            Returns a list of filenames in the playlist that have been
            unlocked.
            """

            if self.shuffle:
                if self.shuffled is None or (filename and self.shuffled[0] != filename):
                    import random
                    self.shuffled = list(self.playlist)
                    random.shuffle(self.shuffled)

                    if filename in self.shuffled:
                        self.shuffled.remove(filename)
                        self.shuffled.insert(0, filename)


                playlist = self.shuffled

            else:
                self.shuffled = None
                playlist = self.playlist

            return [ i for i in playlist if self.is_unlocked(i) ]

        def play(self, filename=None, offset=0, queue=False):
            """
            Starts the music room playing. The file we start playing with is
            selected in two steps.

            If `filename` is an unlocked file, we start by playing it.
            Otherwise, we start by playing the currently playing file, and if
            that doesn't exist or isn't unlocked, we start with the first file.

            We then apply `offset`. If `offset` is positive, we advance that many
            files, otherwise we go back that many files.

            If `queue` is true, the music is queued. Otherwise, it is played
            immediately.
            """

            playlist = self.unlocked_playlist(filename)

            if not playlist:
                return

            if filename is None:
                filename = renpy.music.get_playing(channel=self.channel)

            try:
                idx = playlist.index(filename)
            except ValueError:
                idx = 0

            idx = (idx + offset) % len(playlist)

            if self.single_track:
                playlist = [ playlist[idx] ]
            elif self.loop:
                playlist = playlist[idx:] + playlist[:idx]
            else:
                playlist = playlist[idx:]

            if queue:
                renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
            else:
                renpy.music.play(playlist, channel=self.channel, fadeout=self.fadeout, fadein=self.fadein, loop=self.loop)

        def queue_if_playing(self):
            """
            If the music is not playing, do nothing.

            Otherwise, redo the queue such that we have the right tracks
            queued up.
            """

            filename = renpy.music.get_playing(channel=self.channel)
            if filename is None:
                return

            if self.single_track:
                self.play(None, offset=0, queue=True)
            else:
                self.play(None, offset=1, queue=True)


        def stop(self):
            """
            Stops the music from playing.
            """

            renpy.music.stop(channel=self.channel, fadeout=self.fadeout)

        def next(self):
            """
            Plays the next file in the playlist.
            """

            filename = renpy.music.get_playing(channel=self.channel)
            if filename is None:
                return self.play(None, 0)
            else:
                return self.play(None, 1)

        def previous(self):
            """
            Plays the previous file in the playlist.
            """

            return self.play(None, -1)

        def Play(self, filename=None):
            """
            :doc: music_room method

            This action causes the music room to start playing. If `filename` is given, that
            file begins playing. Otherwise, the currently playing file starts
            over (if it's unlocked), or the first file starts playing.

            If `filename` is given, buttons with this action will be insensitive
            while `filename` is locked, and will be selected when `filename`
            is playing.
            """

            if filename is None:
                return self.play

            if filename not in self.filenames:
                raise Exception("{0!r} is not a filename registered with this music room.".format(filename))

            return __MusicRoomPlay(self, filename)

        def RandomPlay(self):
            """
            :doc: music_room method

            This action causes the music room to start playing a randomly selected unlocked
            music track.
            """

            return __MusicRoomRandomPlay(self)

        def TogglePlay(self):
            """
            :doc: music_room method

            If no music is currently playing, this action starts playing the first
            unlocked track. Otherwise, stops the currently playing music.

            This button is selected when any music is playing.
            """
            return __MusicRoomTogglePlay(self)

        def Stop(self):
            """
            :doc: music_room method

            This action stops the music.
            """

            return __MusicRoomStop(self)

        def Next(self):
            """
            :doc: music_room method

            An action that causes the music room to play the next unlocked file
            in the playlist.
            """

            return self.next

        def Previous(self):
            """
            :doc: music_room method

            An action that causes the music room to play the previous unlocked
            file in the playlist.
            """

            return self.previous

        def SetLoop(self, value):
            """
            :doc: music_room method

            This action sets the value of the loop property.
            """

            return [ SetField(self, "loop", value), self.queue_if_playing ]

        def SetSingleTrack(self, value):
            """
            :doc: music_room method

            This action sets the value of the single_track property.
            """

            if value:
                return [SelectedIf(self.single_track), SetField(self, "single_track", value), SetField(self, "shuffle", False), self.queue_if_playing ]
            else:
                return [SelectedIf(not self.single_track), SetField(self, "single_track", value), self.queue_if_playing ]


        def SetShuffle(self, value):
            """
            :doc: music_room method

            This action sets the value of the shuffle property.
            """

            if value:
                return [SelectedIf(self.shuffle), SetField(self, "shuffle", value), SetField(self, "single_track", False), self.queue_if_playing ]
            else:
                return [SelectedIf(not self.shuffle), SetField(self, "shuffle", value), self.queue_if_playing ]

        def ToggleLoop(self):
            """
            :doc: music_room method

            This action toggles the value of the loop property.
            """

            return [ ToggleField(self, "loop"), self.queue_if_playing ]


        def ToggleSingleTrack(self):
            """
            :doc: music_room method

            This action toggles the value of the single_track property.
            """

            return [SelectedIf(self.single_track), ToggleField(self, "single_track"), SetField(self, "shuffle", False), self.queue_if_playing ]

        def ToggleShuffle(self):
            """
            :doc: music_room method

            This action toggles the value of the shuffle property.
            """

            return [SelectedIf(self.shuffle), ToggleField(self, "shuffle"), SetField(self, "single_track", False), self.queue_if_playing ]
