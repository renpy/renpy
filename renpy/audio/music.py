# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# The public API for music in games.

import time
import renpy

# A list of music channels.
music_channels = [ ]

# A list of channels for which set_music has been called, either way.
music_set = [ ]

unique = time.time()
serial = 0

class AttrDict(object):

    def __init__(self, attr):
        self.attr = attr

    def __getitem__(self, item):
        info = renpy.game.context().info
        return getattr(info, self.attr + str(item))

    def __setitem__(self, item, value):
        info = renpy.game.context().info
        setattr(info, self.attr + str(item), value)
        
    def get(self, item, default=None):
        info = renpy.game.context().info
        return getattr(info, self.attr + str(item), default)

_music_last_filenames = AttrDict('_music_last_filenames')
_music_last_tight = AttrDict('_music_last_tight')
_music_last_changed = AttrDict('_music_last_changed')
_music_volumes = AttrDict('_music_volumes')


def get_serial():
    """
    Gets a globally unique serial number for each music change.
    """
    
    global serial
    serial += 1
    return (unique, serial)

    
def get_channel(channel):
    if not channel in music_channels:
        raise Exception("Channel %d is not a music channel." % channel)
    
    c = renpy.audio.audio.get_channel(channel)
    return c

def play(filenames, channel=7, loop=True, fadeout=None, synchro_start=False, fadein=0, tight=False, if_changed=False):
    """
    This stops the music currently playing on the numbered channel, dequeues
    any queued music, and begins playing the specified file or files. If loop
    is True, the tracks will loop while they are the last thing in
    the queue. If fadeout is None, the fadeout time is taken from
    config.fade_music, otherwise it is a time in seconds to fade for.

    Filenames may be a single file, or a list of files.

    Fadein is the number of seconds to fade the music in for, on the
    first loop only.

    If synchro_start is given, all the channels that have had play
    called on them with synchro_start set to True will be started at
    the same time, in a sample accurate manner.

    The filenames given becomes the last queued files if loop is
    True. If loop is False, then there are no last queued files.

    If tight is True, then fadeouts will span into the next-queued sound.
    
    If if_changed is True, and the music file is currently playing,
    then it will not be stopped/faded out and faded back in again, but
    instead will be kept playing. (This will always queue up an additional
    loop of the music.)
    """

    if isinstance(filenames, basestring):
        filenames = [ filenames ]

    try:        
        c = get_channel(channel)

        c.dequeue()

        if fadeout is None:
            fadeout = renpy.config.fade_music

        if if_changed and c.get_playing() in filenames:
            fadein = 0
        else:
            c.fadeout(fadeout)

        c.enqueue(filenames, loop=loop, synchro_start=synchro_start, fadein=fadein, tight=tight)
        
        t = get_serial()
        _music_last_changed[channel] = t
        c.music_last_changed = t

        if loop:
            _music_last_filenames[channel] = filenames            
            _music_last_tight[channel] = tight            
        else:
            _music_last_filenames[channel] = None
            _music_last_tight[channel] = False
        
    except:
        if renpy.config.debug_sound:
            raise
    
    

def queue(filenames, channel=7, loop=True, clear_queue=True, fadein=0, tight=False):
    """
    This queues the given filenames on the specified channel. If
    clear_queue is True, then the queue is cleared, making these files
    the files that are played when the currently playing file
    finishes. If it is False, then these files are placed at the back of
    the queue. In either case, if no music is playing these files
    begin playing immediately.

    Filenames may either be a single filename, or a list of filenames.

    Fadein is the number of seconds to fade the music in for, on the
    first loop only.

    If loop is True, then this music will repeat as long as it is the
    last element of the queue.

    The filenames given becomes the last queued file if loop is
    True. If loop is False, then the last queued file is set to None.

    If tight is True, then fadeouts will span into the next-queued sound.
    """

    if filenames is None:
        filenames = [ ]
        loop = False

    if isinstance(filenames, basestring):
        filenames = [ filenames ]

    try:        
        c = get_channel(channel)

        if clear_queue:
            c.dequeue(True)

        c.enqueue(filenames, loop=loop, fadein=fadein, tight=tight)
        
        t = get_serial()
        _music_last_changed[channel] = t
        c.music_last_changed = t

        if loop:
            _music_last_filenames[channel] = filenames
            _music_last_tight[channel] = tight
        else:
            _music_last_filenames[channel] = None
            _music_last_tight[channel] = False
        
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

        c.dequeue()

        if fadeout is None:
            fadeout = renpy.config.fade_music

        c.fadeout(fadeout)        
        
        t = get_serial()
        _music_last_changed[channel] = t
        c.music_last_changed = t
        _music_last_filenames[channel] = None
        _music_last_tight[channel] = False
        
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

        c.set_volume(volume)
        _music_volumes[channel] = volume
        
    except:
        if renpy.config.debug_sound:
            raise

    
def set_music(channel, flag, default=False):
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

    if default and channel in music_set:
        return

    music_set.append(channel)
    
    if flag:
        if channel not in music_channels:
            music_channels.append(channel)
    else:
        if channel in music_channels:
            music_channels.remove(channel)

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
            
def get_playing(channel=7):
    """
    Returns the number of seconds left until the given time in the
    music.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        return c.get_playing()

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

        for i in music_channels:
            c = renpy.audio.audio.get_channel(i)

            if _music_volumes.get(i, 1.0) != c.chan_volume:
                c.set_volume(_music_volumes.get(i, 1.0))

            # If we're in the same music change, then do nothing with the
            # music.
            if c.music_last_changed == _music_last_changed.get(i, 0):
                continue

            filenames = _music_last_filenames.get(i, None)
            tight = _music_last_tight.get(i, False)

            c.dequeue()
            
            if not filenames or c.get_playing() not in filenames:
                c.fadeout(renpy.config.fade_music)

            if filenames:
                c.enqueue(filenames, loop=True, synchro_start=True, tight=tight)

            c.music_last_changed = _music_last_changed.get(i, 0) 
        
    except:
        if renpy.config.debug_sound:
            raise

# Music change logic:

# Use the queueing time to determine what should or should not be
# queued


# m_filenames - music filenames from info object
# m_loop - music loop from info object
# c_filenames - music filenames from channel
# c_filenames - music loop from channel

# if m_filenames == c_filenames and m_loop == c_loop:
#     do nothing, the music is right.

# otherwise,
#     dequeue music from the channel.

# if m_filenames != c_playing_filenames:
#     stop the music with fade. The music is wrong, change it.

# if m_loop:
#     queue m_filenames looping

