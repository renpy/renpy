# Copyright 2007 PyTom <pytom@bishoujo.us>
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

import renpy
import time
import pygame

# The ren'py.sound channels corresponding to pygame channels.
channels = [ 0, 1, 2]

# A map from pygame channel to channel objects.
chanobjs = { }

# The number of reserved channels.
reserved = 0

def init(*args, **kwargs):
    """
    RPG: Does nothing. Ren'Py will have initialized the sound system before
    game start.
    """

def pre_init(*args, **kwargs):
    """
    RPG: Does nothing. Ren'Py will have initialized the sound system before
    game start.
    """

def quit():
    """
    RPG: Does nothing.
    """

def get_init():
    return (renpy.config.sound_sample_rate, -16, 2)

def stop():
    for i in chanobjs.values():
        i.stop()

def pause():
    """
    RPG: Does nothing.
    """

def unpause():
    """
    RPG: Does nothing.
    """

def fadeout(time):
    for i in chanobjs.values():
        i.fadeout(time)

def set_num_channels(num):
    """
    RPG: Does nothing.
    """

def get_num_channels():
    return len(channels)

def set_reserved(num):
    global reserved
    reserved = num

def get_channel(i):
    rv = chanobjs.get(i, None)
    if rv is None:
        rv = chanobjs[i] = Channel(i)

    return rv
    
def find_channel(force=False):

    times = [ ]
    
    for i in range(reserved, len(channels)):
        c = get_channel(i)
        if not c.get_busy():
            return c

        times.append((c.start_time, c))

    if not force:
        return None
    else:
        return min(times)[1]
    
    
    
def get_busy():
    for c in chanobjs.values():
        if c.get_busy():
            return True

    return False

class Sound(object):

    def __init__(self, filename):
        self.filename = filename
        self.channel = None
        
    def play(self, loops=0):
        """
        RPG: Maxtime is not supported. 
        """

        channel = find_channel(True)
        channel.play(self, loops)
        return channel

    def stop(self):
        for i in chanobj.values():
            if i.get_sound() is self:
                i.stop()

    def set_volume(self, *args, **kwargs):
        """
        RPG: Does nothing.
        """

    def get_volume(self):
        """
        RPG: Does nothing, always returns 1.0
        """

        return 1.0
    
    def get_num_channels(self):
        rv = 0
        
        for i in chanobj.values():
            if i.get_sound() is self:
                rv += 1

        return rv
        
class Channel(object):
    def __init__(self, channel):
        self.channel = channel
        self.renpy_channel = channels[channel] 
        self.start_time = 0
        self.sound = None
        
    def get_busy(self):
        return renpy.audio.sound.is_playing(self.renpy_channel)

    def play(self, sound, loops=0):
        """
        RPG: Plays the given sound loops+1 times. Does not support the time
        argument.
        """

        self.start_time = time.time()
        self.sound = sound

        renpy.audio.sound.play(sound.filename, channel=self.renpy_channel)

        for i in range(0, loops):
            renpy.audio.sound.queue(sound.filename, clear_queue=None, channel=self.renpy_channel)

    def stop(self):
        renpy.audio.sound.stop(channel=self.renpy_channel)
        
    def pause(self):
        """
        RPG: Does nothing.
        """

    def unpause(self):
        """
        RPG: Does nothing.
        """

    def fadeout(self, time):
        renpy.audio.sound.stop(channel=self.renpy_channel, fadeout=time/1000.0)

    def set_volume(self, *args, **kwargs):
        """
        RPG: Does nothing.
        """

    def get_volume(self):
        """
        RPG: Does nothing.
        """

        return 1.0

    def get_sound(self):
        if self.get_busy:
            return self.sound
        else:
            return None

    def queue(self, sound):
        """
        RPG: Queues the given sound.
        """
        self.start_time = time.time()
        self.sound = sound

        renpy.audio.sound.queue(sound.filename, channel=self.renpy_channel)

    def get_queue(self, sound):
        """
        RPG: Not implemented properly. Returns the currently playing sound, if any.
        """
        
        return self.get_sound()
        
    def set_endevent(self, event=None):
        """
        RPG: Does nothing.
        """

    def get_endevent(self):
        """
        RPG: Returns renpygame.NOEVENT
        """

        return renpygame.NOEVENT
