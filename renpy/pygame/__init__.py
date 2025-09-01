# Copyright 2014 Tom Rothamel <tom@rothamel.us>
# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from __future__ import division, print_function, absolute_import

import sys
import importlib


# Lists of functions that are called on init and quit.
init_functions = [ ]
quit_functions = [ ]


def register_init(fn):
    init_functions.append(fn)
    return fn


def register_quit(fn):
    quit_functions.append(fn)
    return fn


def init():
    numpass = 0
    numfail = 0

    for i in init_functions:
        try:
            i()
            numpass += 1
        except:
            numfail += 1

    return numpass, numfail


def quit():  # @ReservedAssignment
    for i in quit_functions:
        try:
            i()
        except:
            pass


# Import core modules.
from renpy.pygame.error import *

from renpy.pygame.surface import Surface
from renpy.pygame.rect import Rect

import renpy.pygame.color
import renpy.pygame.display
import renpy.pygame.event
import renpy.pygame.key
import renpy.pygame.locals  # @ReservedAssignment
import renpy.pygame.time
import renpy.pygame.version
import renpy.pygame.locals as constants
import renpy.pygame.controller
import renpy.pygame.draw
import renpy.pygame.image
import renpy.pygame.joystick
import renpy.pygame.mouse
import renpy.pygame.power
import renpy.pygame.transform
import renpy.pygame.scrap
import renpy.pygame.sysfont


# Fill this module with locals.
from renpy.pygame.locals import *


def import_as_pygame():
    """
    Imports pygame_sdl2 as pygame, so that running the 'import pygame.whatever'
    statement will import renpy.pygame.whatever instead.
    """

    import os
    import warnings

    if "pygame" in sys.modules:
        warnings.warn("Pygame has already been imported, import_as_pygame may not work.", stacklevel=2)

    if "pygame_sdl2" in sys.modules:
        warnings.warn("Pygame SDL2 has already been imported, import_as_pygame may not work.", stacklevel=2)

    for name, mod in list(sys.modules.items()):
        if name.startswith('renpy.pygame'):
            suffix = name[len('renpy.pygame'):]
        else:
            continue

        sys.modules["pygame" + suffix] = mod
        sys.modules["pygame_sdl2" + suffix] = mod

    sys.modules['pygame.constants'] = constants
    sys.modules['pygame_sdl2.constants'] = constants


def get_sdl_byteorder():
    return BYTEORDER


def get_sdl_version():
    return SDL_VERSION_TUPLE


def get_platform():
    return renpy.pygame.display.get_platform()

# We have new-style buffers, but not the pygame.newbuffer module.
HAVE_NEWBUF = False
