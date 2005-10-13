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

    if filename is None:
        return

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
    channel. By default, there are two mixers, 'sfx' and
    'music'. 'sfx' is on channels 0 to 3, and 'music'
    on 3 to 7. The voice module calls this function to set channel 2 to voice.
    You can create your own mixer, but will need to add a preference if you
    wish to allow the user to set it.

    This function should only be called in an init block.
    """

    try:        
        c = renpy.audio.audio.get_channel(channel)
        c.mixer = mixer
    except:
        if renpy.config.debug_sound:
            raise

def set_queue_empty_callback(callback, channel=0):
    """
    This sets a callback that is called when the queue is empty. This
    callback is called when the queue first becomes empty, and at
    least once per interaction while the queue is empty.

    The callback is called with no parameters. It can queue sounds by
    calling renpy.sound.queue with the appropriate arguments. Please
    note that the callback may be called while a sound is playing, as
    long as a queue slot is empty.
    """
    try:        
        c = renpy.audio.audio.get_channel(channel)
        c.callback = callback
    except:
        if renpy.config.debug_sound:
            raise

def set_volume(volume, channel=0):
    """
    Sets the volume of this channel, as a fraction of the volume of the
    mixer controlling the channel.

    This volume is not persisted or rolled-back, as are volumes set with
    renpy.music.set_volume for music channels.
    """

    try:        
        c = renpy.audio.audio.get_channel(channel)
        c.set_volume(volume)
    except:
        if renpy.config.debug_sound:
            raise
    
def is_playing(channel=0):
    """
    Returns True if the channel is currently playing a sound, False if
    it is not, or if the sound system isn't working.
    
    This works with both sound and music channels, although it's intended
    for the former.
    """

    try:        
        c = renpy.audio.audio.get_channel(channel)
        return c.playing
    except:
        if renpy.config.debug_sound:
            raise
        else:
            return False
