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


class MissingModule(object):

    def __init__(self, name, reason):
        self.__name__ = name
        self.reason = reason

    def __getattr__(self, attr):
        raise NotImplementedError(self.reason)


def try_import(name):
    full_name = "pygame_sdl2." + name

    try:
        module = importlib.import_module(full_name)
    except (IOError, ImportError) as e:
        module = MissingModule(full_name, "Could not import {}: {}".format(full_name, str(e)))

    globals()[name] = module
    sys.modules[full_name] = module


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
from pygame_sdl2.error import *

from pygame_sdl2.surface import Surface
from pygame_sdl2.rect import Rect

import pygame_sdl2.color
import pygame_sdl2.display
import pygame_sdl2.event
import pygame_sdl2.key
import pygame_sdl2.locals  # @ReservedAssignment
import pygame_sdl2.time
import pygame_sdl2.version
import pygame_sdl2.locals as constants

# Import optional modules.
try_import("controller")
try_import("draw")
try_import("font")
try_import("image")
try_import("joystick")
try_import("mixer")
try_import("mouse")
try_import("power")
try_import("transform")
try_import("scrap")
try_import("sprite")
try_import("sysfont")

# Optional imports should be included in this function, so they show up
# in packaging tools (like py2exe).


def _optional_imports():
    import pygame_sdl2.compat
    import pygame_sdl2.controller
    import pygame_sdl2.rwobject
    import pygame_sdl2.gfxdraw
    import pygame_sdl2.draw
    import pygame_sdl2.font
    import pygame_sdl2.image
    import pygame_sdl2.joystick
    import pygame_sdl2.mixer
    import pygame_sdl2.mouse
    import pygame_sdl2.power
    import pygame_sdl2.transform
    import pygame_sdl2.scrap
    import pygame_sdl2.sprite
    import pygame_sdl2.sysfont


# Fill this module with locals.
from pygame_sdl2.locals import *


def import_as_pygame():
    """
    Imports pygame_sdl2 as pygame, so that running the 'import pygame.whatever'
    statement will import pygame_sdl2.whatever instead.
    """

    import os
    import warnings

    if "PYGAME_SDL2_USE_PYGAME" in os.environ:
        return

    if "pygame" in sys.modules:
        warnings.warn("Pygame has already been imported, import_as_pygame may not work.", stacklevel=2)

    for name, mod in list(sys.modules.items()):
        name = name.split('.')
        if name[0] != 'pygame_sdl2':
            continue

        name[0] = 'pygame'
        name = ".".join(name)

        sys.modules[name] = mod

    sys.modules['pygame.constants'] = constants


def get_sdl_byteorder():
    return BYTEORDER


def get_sdl_version():
    return SDL_VERSION_TUPLE


get_platform = pygame_sdl2.display.get_platform

# We have new-style buffers, but not the pygame.newbuffer module.
HAVE_NEWBUF = False
