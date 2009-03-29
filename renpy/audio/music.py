# Copyright 2004-2009 PyTom <pytom@bishoujo.us>
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

from renpy.audio.audio import get_channel, get_serial

# Part of the public api:
from renpy.audio.audio import register_channel, alias_channel

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
        ctx = c.context
        
        c.dequeue()

        if fadeout is None:
            fadeout = renpy.config.fade_music

        if if_changed and c.get_playing() in filenames:
            fadein = 0
        else:
            c.fadeout(fadeout)

        c.enqueue(filenames, loop=loop, synchro_start=synchro_start, fadein=fadein, tight=tight)
        
        t = get_serial()
        ctx.last_changed = t
        c.last_changed = t

        if loop:
            ctx.last_filenames = filenames            
            ctx.last_tight = tight            
        else:
            ctx.last_filenames = None
            ctx.last_tight = False
        
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
        ctx = c.context
        
        if clear_queue:
            c.dequeue(True)

        c.enqueue(filenames, loop=loop, fadein=fadein, tight=tight)
        
        t = get_serial()
        ctx.last_changed = t
        c.last_changed = t

        if loop:
            ctx.last_filenames = filenames
            ctx.last_tight = tight
        else:
            ctx.last_filenames = None
            ctx.last_tight = False
        
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
        ctx = c.context
        
        c.dequeue()

        if fadeout is None:
            fadeout = renpy.config.fade_music

        c.fadeout(fadeout)        
        
        t = get_serial()
        ctx.last_changed = t
        c.last_changed = t
        ctx.last_filenames = None
        ctx.last_tight = False
        
    except:
        if renpy.config.debug_sound:
            raise

    
def set_music(channel, flag, default=False):
    """
    Determines if channel will loop by default.
    """

    c = get_channel(channel)

    if default and c.default_loop_set:
        return

    c.default_loop = Flag
    c.default_loop_set = True
    
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
    Returns true if the given channel is playing.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        return c.get_playing()

    except:
        if renpy.config.debug_sound:
            raise

        return None


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

