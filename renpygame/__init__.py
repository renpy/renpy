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

# The version of renpygame we're dealing with.
renpygame_version = 1002

import sys
import pygame

Overlay = pygame.Overlay
Rect = pygame.Rect
Surface = pygame.Surface
get_error = pygame.get_error
get_sdl_version = pygame.get_sdl_version
error = pygame.error

def init():
    """
    Doesn't actually do anything, since Ren'Py takes care of initializing
    pygame. Returns (6, 0) to mimic pygame.
    """

    return (6, 0)

quit_callbacks = [ ]

def quit():
    """
    Doesn't do anything except run the quit callbacks registered using
    register_quit.
    """

    global quit_callbacks
    
    for i in quit_callbacks:
        i()

    quit_callbacks = [ ]

def register_quit(callback):
    quit_callbacks.insert(0, callback)

# Importing the other modules.
import renpygame.color #@UnresolvedImport
import renpygame.constants #@UnresolvedImport
import renpygame.cursors #@UnresolvedImport
import renpygame.display #@UnresolvedImport
import renpygame.draw #@UnresolvedImport
import renpygame.event #@UnresolvedImport
import renpygame.font #@UnresolvedImport
import renpygame.image #@UnresolvedImport
import renpygame.locals #@UnresolvedImport
import renpygame.joystick #@UnresolvedImport
import renpygame.key #@UnresolvedImport
import renpygame.mixer #@UnresolvedImport
import renpygame.mixer.music #@UnresolvedImport
import renpygame.mouse #@UnresolvedImport
import renpygame.sprite #@UnresolvedImport
import renpygame.time #@UnresolvedImport
import renpygame.transform #@UnresolvedImport

# Needs to be from renpygame, so we get the right constant.
from renpygame.constants import *

