# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

# This module deals with pygame-specific rendering tasks.

import pygame
import renpy

# This class is used to make a copy of a pygame module's functions. We
# can then access those functions, and be relatively sure that those
# have not changed.
class ModuleProxy(object):
    def __init__(self, module):
        self.__dict__.update(module.__dict__)

opygame = ModuleProxy(pygame)
opygame.display = ModuleProxy(pygame.display) # W0201
opygame.transform = ModuleProxy(pygame.transform) # W0201
opygame.image = ModuleProxy(pygame.image) # W0201


# Sample surfaces, with and without alpha.
sample_alpha = None
sample_noalpha = None

def set_mode(resolution, flags=0, depth=0):
    """
    Sets the mode of the pygame screen, and creates the sample
    surfaces.
    """

    global sample_alpha
    global sample_noalpha
    
    rv = opygame.display.set_mode(resolution, flags, depth)

    s = opygame.Surface((10, 10))
    sample_alpha = s.convert_alpha(rv)
    sample_noalpha = s.convert(rv)

    return rv
    
set_mode_unscaled = set_mode

class Surface(opygame.Surface):
    """
    This allows us to wrap around pygame's surface, to change
    its mode, as necessary.
    """

    def convert_alpha(self, surface=None):
        return copy_surface_unscaled(self, True)

    def convert(self, surface=None):
        return copy_surface(self, False)

    def copy(self):
        return copy_surface(self, self)
    

def surface((width, height), alpha):
    """
    Constructs a new surface. The allocated surface is actually a subsurface
    of a surface that has a 1 pixel border in all directions.

    `alpha` - True if the new surface should have an alpha channel.
    """

    if isinstance(alpha, opygame.Surface):
        alpha = alpha.get_masks()[3]
    
    if alpha:
        sample = sample_alpha
    else:
        sample = sample_noalpha

    # We might not have initialized properly yet. This is enough
    # to get us underway.
    if sample is None:
        sample = opygame.Surface((2, 2), opygame.SRCALPHA, 32)
        
    surf = Surface((width + 2, height + 2), 0, sample)
    return surf.subsurface((1, 1, width, height)) # E1101

surface_unscaled = surface


def copy_surface(surf, alpha=True):
    """
    Creates a copy of the surface.
    """
    
    rv = surface_unscaled(surf.get_size(), alpha)

    renpy.display.render.blit_lock.acquire()
    rv.blit(surf, (0, 0))
    renpy.display.render.blit_lock.release()

    return rv

copy_surface_unscaled = copy_surface


# Wrapper around image loading.

def load_image(f, filename):
    surf = opygame.image.load(f, filename)
    return copy_surface_unscaled(surf)

load_image_unscaled = load_image


# Wrapper around functions we use from pygame.surface.

def flip(surf, horizontal, vertical):
    surf = opygame.transform.flip(surf, horizontal, vertical)
    return copy_surface_unscaled(surf)

flip_unscaled = flip


def rotozoom(surf, angle, zoom):

    surf = opygame.transform.rotozoom(surf, angle, zoom)
    return copy_surface_unscaled(surf)

rotozoom_unscaled = rotozoom


def transform_scale(surf, size):
    surf = opygame.transform.scale(surf, size)
    return copy_surface_unscaled(surf, surf)

transform_scale_unscaled = transform_scale


def transform_rotate(surf, angle):
    surf = opygame.transform.rotate(surf, angle)
    return copy_surface(surf)

transform_rotate_unscaled = transform_rotate



