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

from pygame.event import *

def periodic():
    renpy.audio.audio.periodic()

def get(types=None):

    if pygame.event.get([ renpy.display.core.PERIODIC ]):
        periodic()

    if types is not None:
        return pygame.event.get(types)
    else:
        return pygame.event.get()

def peek(types=None):
    
    if pygame.event.get([ renpy.display.core.PERIODIC ]):
        periodic()
    
    if types is not None:
        return pygame.event.peek(types)
    else:
        return pygame.event.peek()

def poll(types=None):
    if pygame.event.get([ renpy.display.core.PERIODIC ]):
        periodic()
    
    return pygame.event.poll()

def wait():

    while True:
        ev = pygame.event.wait()
        if ev.type == renpy.display.core.PERIODIC:
            periodic()
            continue

        return ev

    
