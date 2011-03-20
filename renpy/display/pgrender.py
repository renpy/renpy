# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

# This module wraps the pygame surface class (and associated functions).

import sys
import pygame
import renpy.display

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

def set_rgba_masks():
    """
    This rebuilds the sample surfaces, to ones that use the given
    masks.
    """

    # Annoyingly, the value for the big mask seems to vary from
    # platform to platform. So we read it out of a surface.
    
    global sample_alpha
    global sample_noalpha

    # Create a sample surface.
    s = opygame.Surface((10, 10), 0, 32)
    sample_alpha = s.convert_alpha()

    # Sort the components by absolute value.
    masks = list(sample_alpha.get_masks())
    masks.sort(key=lambda a : abs(a))

    # Choose the masks.
    if sys.byteorder == 'big':
        masks = ( masks[3], masks[2], masks[1], masks[0] )
    else:
        masks = ( masks[0], masks[1], masks[2], masks[3] )

    # Create the sample surface.
    sample_alpha = opygame.Surface((10, 10), 0, 32, masks)
    sample_noalpha = opygame.Surface((10, 10), 0, 32, masks[:3] + (0,))
    

class Surface(opygame.Surface):
    """
    This allows us to wrap around pygame's surface, to change
    its mode, as necessary.
    """

    opaque = False
    
    def is_opaque(self):
        return self.opaque
    
    def convert_alpha(self, surface=None):
        return copy_surface_unscaled(self, True)

    def convert(self, surface=None):
        return copy_surface(self, False)

    def copy(self):
        return copy_surface(self, self)

    def subsurface(self, rect):
        rv = opygame.Surface.subsurface(self, rect)
        return rv

    

def surface((width, height), alpha):
    """
    Constructs a new surface. The allocated surface is actually a subsurface
    of a surface that has a 2 pixel border in all directions.

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
        sample = opygame.Surface((4, 4), opygame.SRCALPHA, 32)
        
    surf = Surface((width + 4, height + 4), 0, sample)
    return surf.subsurface((2, 2, width, height)) # E1101

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



