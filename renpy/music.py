# This module contains code that handles the playing of music.

import pygame
import renpy

# Information about the currently playing track.
current_music = None

def music_start(filename, loops=-1, startpos=0.0):
    """
    This starts music playing. If a music track is already playing,
    stops that track in favor of this one.

    @param filename: The file that the music will be played from. This
    is relative to the game directory, and must be a real file (so it
    cannot be stored in an archive.)

    @param loops: The number of times the music will loop after it
    finishes playing. If negative, the music will loop indefinitely.
    Please note that even once the song has finished, rollback or load
    may cause it to start playing again. So it may not be safe to have
    this set to a non-negative value.

    @param startpos: The number of seconds into the music to start playing.
    """

    music_stop()
    renpy.game.context().scene_lists.music = (filename, loops, startpos)
    restore()


def music_stop():
    """
    Stops the currently playing music track.
    """

    renpy.game.context().scene_lists.music = None
    restore()

def restore():
    """
    This makes sure that the current music matches the music found in
    the context.
    """

    global current_music

    new_music = renpy.game.context().scene_lists.music

    if not renpy.game.preferences.music:
        new_music = None

    if current_music == new_music:
        return


    current_music = new_music

    # Usually, ignore errors.
    try:        
        if not new_music:
            pygame.mixer.music.stop()
        else:
            fn, loops, startpos = new_music
            pygame.mixer.music.load(renpy.game.basepath + "/" + fn)
            pygame.mixer.music.play(loops, startpos)

    except pygame.error, e:
        if renpy.config.debug:
            raise
        else:
            print "Error while trying to play music:", str(e)
