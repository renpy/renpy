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

def flip():
    renpy.game.interface.display.full_redraw = True
    pygame.display.flip()

def gl_get_attribute(flag):
    """
    RPG: Not supported under renpy.
    """

    raise Exception("Not supported.")

def gl_set_attribute(flag):
    """
    RPG: Not supported under renpy.
    """

    raise Exception("Not supported.")

def init():
    """
    RPG: Does nothing, since Ren'Py will have already inited the
    display subsystem.
    """

def list_modes(depth=32, flags=0):
    """
    RPG: If the depth is 32 or 0, returns the size of the Ren'Py window.
    Otherwise, returns an empty list.
    """

    if depth == 32 or depth == 0:
        return [ pygame.display.get_surface().get_size() ]

    return [ ]

def mode_ok(size, flags=0, depth=32):
    """
    RPG: The mode is ok iff it is the mode we're already in. Otherwise,
    it's not ok, and we return 0.
    """

    size = tuple(size)
    
    if size == pygame.display.get_surface().get_size():
        return 32
    else:
        return 0

def quit():
    """
    RPG: Does nothing.
    """

def set_caption(title, icontitle=""):
    """
    RPG: Does nothing.
    """

set_gamma = pygame.display.set_gamma
set_gamma_ramp = pygame.display.set_gamma_ramp

def set_icon(surface):
    """
    RPG: Does nothing.
    """

def set_mode(size, flags=0, depth=0):
    """
    RPG: Returns the current screen surface. ''size'' must be the size of
    the screen given to Ren'Py. ''flags'' and ''depth'' are ignored,
    with depth defaulting to 32.
    """

    screen = pygame.display.get_surface()
    
    if tuple(size) != screen.get_size():
        raise Exception("Renpygame can only set the screen size to the Ren'Py screen size.")

    return screen

def set_palette(l):
    """
    RPG: Not supported under Ren'Py.
    """

    raise Exception("Not supported.")

def toggle_fullscreen():
    """
    RPG: Not supported under Ren'Py.
    """

    raise Exception("Not supported.")

def update(rectstyle=None):
    renpy.game.interface.display.full_redraw = True
    pygame.time.set_timer(renpy.display.core.REDRAW, 0)
    pygame.time.set_timer(renpy.display.core.TIMEEVENT, 0)
    

    if rectstyle is not None:
        pygame.display.update(rectstyle)
    else:
        pygame.display.update()


