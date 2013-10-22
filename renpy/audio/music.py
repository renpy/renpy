# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.audio

# A list of music channels.
music_channels = [ ]

# A list of channels for which set_music has been called, either way.
music_set = [ ]

from renpy.audio.audio import get_channel, get_serial

# Part of the public api:
from renpy.audio.audio import register_channel, alias_channel
register_channel; alias_channel

def play(filenames, channel="music", loop=None, fadeout=None, synchro_start=False, fadein=0, tight=None, if_changed=False):
    """
    :doc: audio

    This stops the music currently playing on the numbered channel, dequeues
    any queued music, and begins playing the specified file or files.

    `filenames`
        This may be a single file, or a list of files to be played.

    `channel`
        The channel to play the sound on.
    
    `loop`
        If this is True, the tracks will loop while they are the last thing
        in the queue. 

    `fadeout`
        If not None, this is a time in seconds to fade for. Otherwise the
        fadeout time is taken from config.fade_music.

    `synchro_start`
        If synchro_start is given, all the channels that have had play
        called on them with synchro_start set to True will be started at
        the same time, in a sample accurate manner.

    `fadein`
        This is the number of seconds to fade the music in for, on the
        first loop only.

    `tight`
        If this is True, then fadeouts will span into the next-queued sound.

    `if_changed`
        If this is True, and the music file is currently playing,
        then it will not be stopped/faded out and faded back in again, but
        instead will be kept playing. (This will always queue up an additional
        loop of the music.)
    """

    if renpy.game.context().init_phase:
        raise Exception("Can't play music during init phase.")

    if filenames is None:
        return

    if isinstance(filenames, basestring):
        filenames = [ filenames ]

    try:
        c = get_channel(channel)
        ctx = c.context

        if loop is None:
            loop = c.default_loop

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
            ctx.last_filenames = [ ]
            ctx.last_tight = False

    except:
        if renpy.config.debug_sound:
            raise


def queue(filenames, channel="music", loop=None, clear_queue=True, fadein=0, tight=None):
    """
    :doc: audio

    This queues the given filenames on the specified channel.

    `filenames`
        This may be a single file, or a list of files to be played.

    `channel`
        The channel to play the sound on.
    
    `loop`
        If this is True, the tracks will loop while they are the last thing
        in the queue. 

    `clear_queue`
        If True, then the queue is cleared, making these files the files that
        are played when the currently playing file finishes. If it is False,
        then these files are placed at the back of the queue. In either case,
        if no music is playing these files begin playing immediately.

    `fadein`
        This is the number of seconds to fade the music in for, on the
        first loop only.

    `tight`
        If this is True, then fadeouts will span into the next-queued sound.
    """

    if renpy.game.context().init_phase:
        raise Exception("Can't play music during init phase.")

    if filenames is None:
        filenames = [ ]
        loop = False

    if isinstance(filenames, basestring):
        filenames = [ filenames ]

    try:

        c = get_channel(channel)
        ctx = c.context

        if loop is None:
            loop = c.default_loop

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
            ctx.last_filenames = [ ]
            ctx.last_tight = False

    except:
        if renpy.config.debug_sound:
            raise

def playable(filename, channel="music"):
    """
    Return true if the given filename is playable on the channel. This
    takes into account the prefix and suffix.
    """

    c = get_channel(channel)

    return renpy.loader.loadable(c.file_prefix + filename + c.file_suffix)


def stop(channel="music", fadeout=None):
    """
    :doc: audio

    This stops the music that is currently playing, and dequeues all
    queued music. If fadeout is None, the music is faded out for the
    time given in config.fade_music, otherwise it is faded for fadeout
    seconds.

    This sets the last queued file to None.

    `channel`
        The channel to stop the sound on. 

    `fadeout`
        If not None, this is a time in seconds to fade for. Otherwise the
        fadeout time is taken from config.fade_music.


    """

    if renpy.game.context().init_phase:
        return

    try:
        c = get_channel(channel)
        ctx = c.context

        if fadeout is None:
            fadeout = renpy.config.fade_music

        c.fadeout(fadeout)

        t = get_serial()
        ctx.last_changed = t
        c.last_changed = t
        ctx.last_filenames = [ ]
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

    c.default_loop = flag
    c.default_loop_set = True

def get_delay(time, channel="music"):
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

def get_playing(channel="music"):
    """
    :doc: audio

    Returns true if the given channel is playing.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        return c.get_playing()
    except:
        if renpy.config.debug_sound:
            raise

        return None

def is_playing(channel="music"):
    """
    :doc: audio

    Returns True if the channel is currently playing a sound, False if
    it is not, or if the sound system isn't working.
    """

    return (get_playing(channel=channel) is not None)


def set_volume(volume, delay=0, channel="music"):
    """
    :doc: audio

    Sets the volume of this channel, as a fraction of the volume of the
    mixer controlling the channel.

    `volume`
        This is a number between 0.0 and 1.0, and is interpreted as a fraction
        of the mixer volume for the channel.

    `delay`
        It takes delay seconds to change/fade the volume from the old to
        the new value. This value is persisted into saves, and participates
        in rollback.

    `channel`
        The channel to be set
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        c.set_secondary_volume(volume, delay)
    except:
        if renpy.config.debug_sound:
            raise

def set_pan(pan, delay, channel="music"):
    """
    :doc: audio

    Sets the pan of this channel.

    `pan`
        A number between -1 and 1 that control the placement of the audio.
        If this is -1, then all audio is sent to the left channel.
        If it's 0, then the two channels are equally balanced. If it's 1,
        then all audio is sent to the right ear. 

    `delay`
        The amount of time it takes for the panning to occur.

    `channel`
        The channel the panning takes place on. This can be a sound or a music
        channel. Often, this is channel 7, the default music channel. 
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        c.set_pan(pan, delay)
    except:
        if renpy.config.debug_sound:
            raise

def set_queue_empty_callback(callback, channel="music"):
    """
    :doc: audio

    This sets a callback that is called when the queue is empty. This
    callback is called when the queue first becomes empty, and at
    least once per interaction while the queue is empty.

    The callback is called with no parameters. It can queue sounds by
    calling renpy.music.queue with the appropriate arguments. Please
    note that the callback may be called while a sound is playing, as
    long as a queue slot is empty.
    """
    try:
        c = renpy.audio.audio.get_channel(channel)
        c.callback = callback
    except:
        if renpy.config.debug_sound:
            raise

def set_mixer(channel, mixer, default=False):
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

        if not default or c.mixer is None:
            c.mixer = mixer

    except:
        if renpy.config.debug_sound:
            raise

def channel_defined(channel):
    """
    Returns True if the channel exists, or False otherwise.
    """

    try:
        renpy.audio.audio.get_channel(channel)
        return True
    except:
        return False


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

