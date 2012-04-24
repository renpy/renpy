# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file contains the code to implement Ren'Py's music room function,
# which consists of the ability to set up a playlist (the aforementioned
# "music room"), and then a series of actions that let the player 
# navigate through the music room.

init -1135 python:

    class __MusicRoomPlay(Action):
        """
        The action returned by MusicRoom.Play when called with a file.
        """
                
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
                renpy.restart_interaction()

            return .1
    
    class MusicRoom(object):
        """
        :doc: music_room class
        
        A music room that contains a series of songs that can be unlocked
        by the user, and actions that can play entries from the list in
        order.
        """
        
        def __init__(self, channel="music", fadeout=0.0, fadein=0.0):
            """
            `channel`
                The channel that this music room will operate on.

            `fadeout`
                The number of seconds it takes to fade out the old
                music when changing tracks.
                
            `fadein`
                The number of seconds it takes to fade in the new
                music when changing tracks.
            """
    
            self.channel = channel
            self.fadeout = fadeout
            self.fadein = fadein
            
            # The list of strings giving the titles of songs that make up the
            # playlist.
            self.playlist = [ ]
            
            # A set of filenames, so we can quickly check if a valid filename
            # has been provided.
            self.filenames = set()
            
            # The set of songs that are always unlocked.
            self.always_unlocked = set()
            
            
        def add(self, filename, always_unlocked=False):
            """
            :doc: music_room method
            
            Adds the music file `filename` to this music room. The music room
            will play unlocked files in the order that they are added to the
            room.
            
            `always_unlocked`
                If true, the music file will be always unlocked. This allows
                the file to show up in the music room before it has been 
                played in the game.
            """
            
            self.playlist.append(filename)
            self.filenames.add(filename)
            
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
        
        def unlocked_playlist(self):
            """
            Returns a list of filenames in the playlist that have been 
            unlocked.
            """
            
            return [ i for i in self.playlist if self.is_unlocked(i) ]
        
        def play(self, filename=None, offset=0):
            """
            Starts the music room playing. The file we start playing with is 
            selected in two steps. 

            If `filename` is an unlocked file, we start by playing it.
            Otherwise, we start by playing the currently playing file, and if
            that doesn't exist or isn't unlocked, we start with the first file.

            We then apply `offset`. If `offset` is positive, we advance that many
            files, otherwise we go back that many files.
            
            The selected file is then played.                
        
            """
            
            playlist = self.unlocked_playlist()
            
            if not playlist:
                return
            
            if filename is None:
                filename = renpy.music.get_playing(channel=self.channel)
            
            try:
                idx = playlist.index(filename)
            except ValueError:
                idx = 0
                
            idx = (idx + offset) % len(playlist)
            
            playlist = playlist[idx:] + playlist[:idx]
            
            renpy.music.play(playlist, channel=self.channel, fadeout=self.fadeout, fadein=self.fadein)
            
        def stop(self):
            """
            Stops the music from playing.
            """
            
            renpy.music.stop(channel=self.channel, fadeout=self.fadeout)
            
        def next(self):
            """
            Plays the next file in the playlist.
            """

            return self.play(None, 1)
            
        def previous(self):
            """
            Plays the previous file in the playlist.
            """
            
            return self.play(None, -1)
            
        def Play(self, filename=None):
            """
            :doc: music_room method
                        
            Causes the music room to start playing. If `filename` is given, that
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
        
        def Stop(self):
            """
            :doc: music_room method
            
            Stops the music.
            """
            
            return self.stop
            
        
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
