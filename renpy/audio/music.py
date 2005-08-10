# The public API for music in games.

# The music channels.
music_channels = [ 3, 4, 5, 6, 7 ]

def info():
    """
    Returns the info object. If the music fields are not on it, then
    add them.
    """

    info = renpy.game.context().info

    if getattr(info, "_music_last", None) is None:
        info._music_last = renpy.python.RevertableDict()
        return info

    if getattr(info, "_music_volumes", None) is None:
        info._music_volumes = renpy.python.RevertableDict()

    return info
    

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

def stop(channel=7, fadeout=None):
    """
    This stops the music that is currently playing. If fadeout is
    None, the music is faded out for the time given in
    config.fade_music, otherwise it is faded for fadeout seconds.
    
    This sets the last queued file to None.
    """

def set_volume(volume, channel=7):
    """
    This sets the volume of the given channel. The volume is a number
    between 0 and 1.0, and is interpreted as a fraction of the mixer
    volume for the channel.

    This value is persisted, and takes effect immediately. It also
    participates in rollback.
    """

def set_queue_empty_callback(callback, channel=7):
    """
    This sets a callback that is called when the queue is empty. This
    callback is called when the queue first becomes empty, and at
    least once per interaction while the queue is empty.

    The callback is called with no parameters. It can queue music by
    calling renpy.music.queue with the appropriate arguments. Please
    note that it may be called while music is playing, as long as a
    queue slot is empty.
    """
    
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
