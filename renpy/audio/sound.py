# The public API for sound playback from games.

# TODO: Check to see if SFX are enabled before playing sounds with play or
# queue.

import renpy

def play(filename, channel=0, fadeout=0):
    """
    Plays the named file once on the given channel. This will cause any
    playing sound effect to be stopped (after the given fadeout number of
    seconds, if necessary), and the new sound to be played in its
    place.

    The filename may be that of a file in an archive.
    """

    stop(channel=channel, fadeout=fadeout)
    queue(filename, channel=channel, clear_queue=True)

def queue(filename, channel=0, clear_queue=True):
    """
    This causes the name file to be queued to be played on the given
    channel.  If clear_queue is True, the queue will be cleared before
    playback, so this sound is played immediately after the currently
    playing sound. If False, the channel's queue will not be cleared,
    and the sound will only be played after every other playing sound.
    If no sound is currently playing, then the sound will be played
    immediately.
    """

    try:        
        c = renpy.audio.audio.get_channel(channel)

        if clear_queue:
            c.dequeue()

        c.enqueue(filename, loop=False)

    except:
        if renpy.config.debug_sound:
            raise
    


def stop(channel=0, fadeout=0):
    """
    This dequeues everything from the given channel, and stops the
    currently playing sound. If fadeout is 0, the sound is stopped
    immediately. Otherwise, it is interpreted as a number of seconds
    to fadeout for.
    """

    try:        
        c = renpy.audio.audio.get_channel(channel)
        c.dequeue()
        c.fadeout(int(fadeout * 1000))
    except:
        if renpy.config.debug_sound:
            raise
    


def set_mixer(channel, mixer):
    """
    This sets the name of the mixer associated with a given
    channel. By default, there are three mixers, 'sfx', 'voice', and
    'music'. 'sfx' is on channels 0 and 1, 'voice' on 2, and 'music'
    on 3 to 7. You can create your own mixer, but will need to add it
    to library.mixers yourself if you wish to allow the user to set
    it.

    This function should only be called in an init block.
    """

    try:        
        c = renpy.audio.audio.get_channel(channel)
        c.mixer = mixer
    except:
        if renpy.config.debug_sound:
            raise
    
