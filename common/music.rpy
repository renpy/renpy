# This file contains code to manage the playing of music. It's here,
# in an rpy file, because we now optionally let the user override all
# of this to implement his or her own music system, using calls to
# various functions found in audio.

init -1000:
  python hide:

     # config.debug_sound = True

     # This becomes renpy.music_start.
     def music_start(filename, loops=-1, fadeout=None):
         """
            This starts music playing. If a music track is already
            playing, this pauses that music track in favor of this
            one.

            @param filename: The file that the music will be played from.
            This is relative to the game directory, and must be a real
            file (so it cannot be stored in an archive).

            @param loops: The number of times the music will loop
            after it finishes playing for the first time. This is
            made somewhat less accurate by rollback and loading. If
            this number is less than zero, the song will loop
            forever.

            @param fadeout: If this parameter is not None, it is
            interpreted as a time in seconds, which gives how long
            it will take to fade out the currently playing music.
            """

         if loops >= 0:
             loops += 1

         ctx = renpy.context()
         ctx._music_name = filename
         ctx._music_loops = loops

         if fadeout and audio.music_enabled() and not config.skipping:
             audio.music_fadeout(fadeout)
         
     def music_stop(fadeout=None):
         """
            This stops the currently playing music track.

            @param fadeout: If this parameter is not None, it is
            interpreted as a time in seconds, which gives how long
            it will take to fade out the currently playing music.
            """

         ctx = renpy.context()
         ctx._music_name = None
         ctx._music_loops = None

         if fadeout and audio.music_enabled() and not config.skipping:
             audio.music_fadeout(fadeout)
         
     renpy.music_start = music_start
     renpy.music_stop = music_stop

     # This is called once for each interaction, to ensure that the
     # music is appropriate for that interaction.     
     def music_interact():

         if not audio.music_enabled():
             return

         ctx = renpy.context()

         if not hasattr(ctx, '_music_name'):
             ctx._music_name = None
             ctx._music_loops = None

         playing, queued = audio.music_filenames()

         # If music is disabled, ensure that it is stopped.
         if not _preferences.music:
             if playing:
                 audio.music_stop()

             return

         # If we do not match what is playing, stop what's currently
         # playing and get ready to play something else.
         if ctx._music_name != playing:

             # If we're not playing anything, immediately start the
             # new track by calling music_end_event.
             if not playing:
                 config.music_end_event()

             # Otherwise, we will start a fade to the new music if no
             # such fade is already in progress, and we're not skipping.
             elif not audio.music_fading() and not config.skipping:
                 audio.music_fadeout(config.fade_music)                 

     # This is called whenever a track of music ends, or also from the
     # above when we want to start a new track when nothing else is
     # playing.
     def music_end_event():

         if not _preferences.music:
             return

         ctx = renpy.context()
         playing, queued = audio.music_filenames()

         if not hasattr(ctx, '_music_name'):
             ctx._music_name = None
             ctx._music_loops = None
             
         if not ctx._music_name:
             return

         if not playing and ctx._music_loops:
             ctx._music_loops -= 1
             audio.music_play(ctx._music_name)

         if not queued and ctx._music_loops:
             ctx._music_loops -= 1
             audio.music_queue(ctx._music_name)

     config.interact_callbacks.append(music_interact)
     config.music_end_event = music_end_event

     

