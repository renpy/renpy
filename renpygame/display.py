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

from pygame.display import *

def init():
    """
    RPG: Does nothing, since Ren'Py will have already inited the
    display subsystem.
    """

def quit():
    """
    RPG: Does nothing.
    """

def set_mode(size, flags=0, depth=0):
    """
    RPG: Returns the current screen surface. ''size'' must be the size of
    the screen given to Ren'Py. ''flags'' and ''depth'' are ignored,
    with depth defaulting to 32.
    """
    renpy.game.interface.display_reset = True
    pygame.time.set_timer(renpy.display.core.REDRAW, 0)
    pygame.time.set_timer(renpy.display.core.TIMEEVENT, 0)
    
    return pygame.display.set_mode(size, flags, depth)

