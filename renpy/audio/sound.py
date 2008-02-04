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

# The public API for sound playback from games.

# TODO: Check to see if SFX are enabled before playing sounds with play or
# queue.

import renpy

def play(filename, channel=0, fadeout=0, fadein=0, tight=False):
    """
    Plays the named file once on the given channel. This will cause any
    playing sound effect to be stopped (after the given fadeout number of
    seconds, if necessary), and the new sound to be played in its
    place. The sound is faded in for the given number of seconds.

    The filename may be that of a file in an archive.

    If tight is True, then a fadeout of this sound will continue into
    the next-queued sound.
    """
    
    if filename is None:
        return

    stop(channel=channel, fadeout=fadeout)

    try:        
        c = renpy.audio.audio.get_channel(channel)
        c.dequeue()
        c.enqueue([ filename ], loop=False, fadein=fadein, tight=tight)
    except:
        if renpy.config.debug_sound:
            raise
    


def queue(filename, channel=0, clear_queue=True, fadein=0, tight=False):
    """
    This causes the named file to be queued to be played on the given
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
            c.dequeue(True)

        c.enqueue([ filename ], loop=False, fadein=fadein, tight=tight)

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
        c.fadeout(fadeout)
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
