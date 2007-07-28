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
import pygame

current_filename = None
current_loops = 0

def load(filename):
    global current_filename
    current_filename = filename

def play(loops=0, start=0.0):
    """
    RPG: Starts music playing. Loops is treated specially. If zero,
    the music plays to completion. If non-zero, it loops forever.
    Start is ignored.
    """
    
    global current_loops
    current_loops = loops
    
    renpy.audio.music.play(current_filename, loop=loops)

def rewind():
    renpy.audio.music.play(current_filename, loop=loops)
    
def stop():
    renpy.audio.music.stop()

def pause():
    """
    RPG: Does nothing.
    """

def unpause():
    """
    RPG: Does nothing.
    """

def fadeout(time):
    renpy.audio.music.stop(fadeout=time/1000.0)

def set_volume(*args, **kwargs):
    """
    RPG: Does nothing.
    """

def get_volume():
    """
    RPG: Does nothing, returns 1.0
    """

    return 1.0

def get_busy():
    return renpy.sound.is_playing(7)

def get_pos():
    """
    Does nothing, returns 0.
    """
    
    return 0

def queue(filename):
    """
    RPG: Queues the given filename for playback after the current filename
    finishes.
    """

    global current_filename
    current_filename = filename
    
    renpy.audio.music.queue(filename)

def set_endevent(event=None):
    """
    Does nothing.
    """

def get_endevent():
    """
    Does nothing, returns renpygame.NOEVENT
    """
    return renpygame.NOEVENT

    
