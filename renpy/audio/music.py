# The public API for music in games.

import time
import renpy

# The music channels.
music_channels = [ 3, 4, 5, 6, 7 ]

def get_info():
    """
    Returns the info object. If the music fields are not on it, then
    add them.
    """

    info = renpy.game.context().info

    if getattr(info, "_music_last_file", None) is None:
        info._music_last_file = renpy.python.RevertableDict()

    if getattr(info, "_music_last_changed", None) is None:
        info._music_last_changed = renpy.python.RevertableDict()

    if getattr(info, "_music_volumes", None) is None:
        info._music_volumes = renpy.python.RevertableDict()

    return info
    
def get_channel(channel):
    if not channel in music_channels:
        raise Exception("Channel %d is not a music channel." % channel)
    
    c = renpy.audio.audio.get_channel(channel)
    return c

def play(filename, channel=7, loop=True, fadeout=None, synchro_start=False):
    """
    This stops the music currently playing on the numbered channel, dequeues
    any queued music, and begins playing the specified filename. If loop
    is True, the track will loop while it is still the last thing in
    the queue. If fadeout is None, the fadeout time is taken from
    config.fade_music, otherwise it is a time in seconds to fade for.

    If synchro_start is given, all the channels that have had play
    called on them with synchro_start set to True will be started at
    the same time, in a sample accurate manner.

    The filename given becomes the last queued file if loop is
    True. If loop is False, then the last queued file is set to None.
    """    

    try:        
        c = get_channel(channel)
        info = get_info()

        c.dequeue()

        if fadeout is None:
            fadeout = renpy.config.fade_music

        c.fadeout(fadeout)        
        c.enqueue(filename, loop=loop, synchro_start=synchro_start)
        
        t = time.time()
        info._music_last_changed[channel] = t
        c.music_last_changed = t

        if loop:
            info._music_last_file[channel] = filename
        else:
            info._music_last_file[channel] = None
        
    except:
        if renpy.config.debug_sound:
            raise
    
    

def queue(filename, channel=7, loop=True, clear_queue=True):
    """
    This queues the given filename on the specified channel. If
    clear_queue is True, then the queue is cleared, making this file
    the file that is played when the currently playing music
    finishes. If it is False, then this file is placed at the back of
    the queue. In either case, if no music is playing this music
    begins playing immediately.

    If loop is True, then this music will repeat as long as it is the
    last element of the queue.

    The filename given becomes the last queued file if loop is
    True. If loop is False, then the last queued file is set to None.
    """

    try:        
        c = get_channel(channel)
        info = get_info()

        if clear_queue:
            c.dequeue()

        c.enqueue(filename, loop=loop)
        
        t = time.time()
        info._music_last_changed[channel] = t
        c.music_last_changed = t

        if loop:
            info._music_last_file[channel] = filename
        else:
            info._music_last_file[channel] = None
        
    except:
        if renpy.config.debug_sound:
            raise

def stop(channel=7, fadeout=None):
    """
    This stops the music that is currently playing, and dequeues all
    queued music. If fadeout is None, the music is faded out for the
    time given in config.fade_music, otherwise it is faded for fadeout
    seconds.
    
    This sets the last queued file to None.
    """

    try:        
        c = get_channel(channel)
        info = get_info()

        c.dequeue()

        if fadeout is None:
            fadeout = renpy.config.fade_music

        c.fadeout(fadeout)        
        
        t = time.time()
        info._music_last_changed[channel] = t
        c.music_last_changed = t
        info._music_last_file[channel] = None
        
    except:
        if renpy.config.debug_sound:
            raise


def set_volume(volume, channel=7):
    """
    This sets the volume of the given channel. The volume is a number
    between 0 and 1.0, and is interpreted as a fraction of the mixer
    volume for the channel.

    This value is persisted, and takes effect immediately. It also
    participates in rollback.
    """

    try:        
        c = get_channel(channel)
        info = get_info()


        c.set_volume(channel, volume)
        info._music_volumes[channel] = volume
        
    except:
        if renpy.config.debug_sound:
            raise

    
def set_music(channel, flag):
    """
    This should be called to indicate if the given channel should be
    treated as a music channel. If the flag is True, the channel will
    be treated as a music channel, if False, the channel will be
    treated as a sound effects channel. Please note that this will not
    change the mixer controlling the channel. Use
    renpy.sound.set_mixer to do that.

    By default, channels 3-7 are considered music channels.
    """

    if not 0 <= channel < renpy.audio.audio.NUM_CHANNELS:
        raise Exception("Not a music channel.")

    if flag:
        if channel in music_channels:
            music_channels.remove(channel)
    else:
        if channel not in music_channels:
            music_channels.append(channel)

def get_delay(time, channel=7):
    """
    Returns the number of seconds left until the given time in the
    music.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)

        t = c.get_pos()

        if not t or t < 0:
            return None

        if t > time:
            return 0

        return time - t

    except:
        if renpy.config.debug_sound:
            raise

        return None
            
    

def interact():
    """
    This is the music change logic that is called at least once per
    interaction.
    """

    try:

        info = get_info()

        for i in music_channels:
            c = renpy.audio.audio.get_channel(i)

            # If we're in the same music change, then do nothing with the
            # music.
            if c.music_last_changed == info._music_last_changed.get(i, 0):
                continue

            file = info._music_last_file.get(i, None)
            c.dequeue()

            if file != c.get_playing():
                c.fadeout(renpy.config.fade_music)

            if file:
                c.enqueue(file, loop=True, synchro_start=True)

            c.music_last_changed = info._music_last_changed.get(i, 0) 
        
    except:
        if renpy.config.debug_sound:
            raise

# Music change logic:

# Use the queueing time to determine what should or should not be
# queued


# m_filename - music filename from info object
# m_loop - music loop from info object
# c_filename - music filename from channel
# c_filename - music loop from channel

# if m_filename == c_filename and m_loop == c_loop:
#     do nothing, the music is right.

# otherwise,
#     dequeue music from the channel.

# if m_filename != c_playing_filename:
#     stop the music with fade. The music is wrong, change it.

# if m_loop:
#     queue m_filename looping

