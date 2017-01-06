# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

# This module wraps the pygame surface class (and associated functions). It
# ensures that returned surfaces have a 2px border around them.

import sys
import pygame_sdl2 as pygame
import threading
import renpy.display
import renpy.audio


# Sample surfaces, with and without alpha.
sample_alpha = None
sample_noalpha = None


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
    s = pygame.Surface((10, 10), 0, 32)
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
    sample_alpha = pygame.Surface((10, 10), 0, 32, masks)
    sample_noalpha = pygame.Surface((10, 10), 0, 32, masks[:3] + (0,))

    renpy.audio.audio.sample_surfaces(sample_noalpha, sample_alpha)


class Surface(pygame.Surface):
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
        rv = pygame.Surface.subsurface(self, rect)
        return rv


def surface((width, height), alpha):
    """
    Constructs a new surface. The allocated surface is actually a subsurface
    of a surface that has a 2 pixel border in all directions.

    `alpha` - True if the new surface should have an alpha channel.
    """

    if isinstance(alpha, pygame.Surface):
        alpha = alpha.get_masks()[3]

    if alpha:
        sample = sample_alpha
    else:
        sample = sample_noalpha

    # We might not have initialized properly yet. This is enough
    # to get us underway.
    if sample is None:
        sample = pygame.Surface((4, 4), pygame.SRCALPHA, 32)

    surf = Surface((width + 4, height + 4), 0, sample)
    return surf.subsurface((2, 2, width, height))  # E1101

surface_unscaled = surface


def copy_surface(surf, alpha=True):
    """
    Creates a copy of the surface.
    """

    rv = surface_unscaled(surf.get_size(), alpha)
    renpy.display.accelerator.nogil_copy(surf, rv)  # @UndefinedVariable
    return rv

copy_surface_unscaled = copy_surface


# Wrapper around image loading.

# Formats we can load reentrantly.
safe_formats = { "png", "jpg", "jpeg", "webp" }

# Lock used for loading unsafe formats.
image_load_lock = threading.RLock()


def load_image(f, filename):
    global count

    _basename, _dot, ext = filename.rpartition('.')

    try:

        if ext.lower() in safe_formats:
            surf = pygame.image.load(f, renpy.exports.fsencode(filename))
        else:

            # Non-whitelisted formats may not be able to load in a reentrant
            # fashion.
            with image_load_lock:
                surf = pygame.image.load(f, renpy.exports.fsencode(filename))

    except Exception as e:
        raise Exception("Could not load image {!r}: {!r}".format(filename, e))

    rv = copy_surface_unscaled(surf)
    return rv

load_image_unscaled = load_image


# Wrapper around functions we use from pygame.surface.

def flip(surf, horizontal, vertical):
    surf = pygame.transform.flip(surf, horizontal, vertical)
    return copy_surface_unscaled(surf)

flip_unscaled = flip


def rotozoom(surf, angle, zoom):

    surf = pygame.transform.rotozoom(surf, angle, zoom)
    return copy_surface_unscaled(surf)

rotozoom_unscaled = rotozoom


def transform_scale(surf, size):
    surf = pygame.transform.scale(surf, size)
    return copy_surface_unscaled(surf, surf)

transform_scale_unscaled = transform_scale


def transform_rotate(surf, angle):
    surf = pygame.transform.rotate(surf, angle)
    return copy_surface(surf)

transform_rotate_unscaled = transform_rotate
