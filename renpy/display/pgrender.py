# Copyright 2004-2009 PyTom <pytom@bishoujo.us>
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
    
    rv = pygame.display.set_mode(resolution, flags, depth)

    s = pygame.Surface((10, 10))
    sample_alpha = s.convert_alpha(rv)
    sample_noalpha = s.convert(rv)

    return rv
    
set_mode_unscaled = set_mode
    

def surface((width, height), alpha):
    """
    Constructs a new surface. The allocated surface is actually a subsurface
    of a surface that has a 1 pixel border in all directions.

    `alpha` - True if the new surface should have an alpha channel.
    """

    if alpha:
        sample = sample_alpha
    else:
        sample = sample_noalpha
            
    surf = pygame.Surface((width + 2, height + 2), 0, sample)
    return surf.subsurface((1, 1, width, height))

surface_unscaled = surface


def copy_surface(surf):
    """
    Creates a copy of the surface. The copy will have an alpha channel.
    """
    
    rv = surface(surf.get_size(), True)

    renpy.display.render.blit_lock.acquire()
    rv.blit(surf, (0, 0))
    renpy.display.render.blit_lock.release()

    return rv

copy_surface_unscaled = copy_surface


# Wrapper around image loading.

def load_image(f, filename):
    surf = pygame.image.load(f, filename)
    return copy_surface(surf)

load_image_unscaled = load_image


# Wrapper around functions we use from pygame.surface.

def flip(surf, horizontal, vertical):
    surf = pygame.transform.flip(surf, horizontal, vertical)
    return copy_surface(surf)

flip_unscaled = flip


def rotozoom(surf, angle, zoom):

    surf = pygame.transform.rotozoom(surf, angle, zoom)
    return copy_surface(surf)

rotozoom_unscaled = rotozoom


