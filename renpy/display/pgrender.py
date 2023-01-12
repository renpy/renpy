# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import sys
import threading

import pygame_sdl2 as pygame
import renpy


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
    masks.sort(key=abs)

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

    def convert_alpha(self, surface=None):
        return copy_surface_unscaled(self, True)

    def convert(self, surface=None):
        return copy_surface(self, False)

    def copy(self):
        return copy_surface(self, self) # type:ignore

    def subsurface(self, rect):
        rv = pygame.Surface.subsurface(self, rect)
        return rv


def surface(rect, alpha): # (tuple, bool|Surface) -> Surface
    """
    Constructs a new surface. The allocated surface is actually a subsurface
    of a surface that has a 2 pixel border in all directions.

    `alpha` - True if the new surface should have an alpha channel.
    """
    (width, height) = rect
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

    surf = Surface((width + 4, height + 4), 0, sample) # type:ignore
    return surf.subsurface((2, 2, width, height))  # E1101


surface_unscaled = surface


def copy_surface(surf, alpha=True): # (Surface, bool|Surface) -> Surface
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


formats = {
    # PNG
    "png": pygame.image.INIT_PNG, # type:ignore
    # JPEG
    "jpg": pygame.image.INIT_JPG, # type:ignore
    "jpeg": pygame.image.INIT_JPG, # type:ignore
    # WebP
    "webp": pygame.image.INIT_WEBP, # type:ignore
    # JPEG-XL
    # "jxl": pygame.image.INIT_JXL, # type:ignore
    # AVIF
    "avif": pygame.image.INIT_AVIF, # type:ignore
    ## There is no real way of checking the below,
    ## but they are built into SDL2_image by default
    "tga": 0,
    "bmp": 0,
    "ico": 0,
    "svg": 0,
}


def load_image(f, filename, size=None):
    """
    `f`
        A file-like object that can be used to load the image.
    `filename`
        The name of the file that is being loaded. Used for hinting what
        kind of image it is.
    `size`
        If given, the image is scaled to this size. This only works for
        SVG images.
    """

    _basename, _dot, ext = filename.rpartition('.')

    try:

        if ext.lower() in safe_formats:
            surf = pygame.image.load(f, renpy.exports.fsencode(filename), size=size)
        else:

            # Non-whitelisted formats may not be able to load in a reentrant
            # fashion.
            with image_load_lock:
                surf = pygame.image.load(f, renpy.exports.fsencode(filename), size=size)

    except Exception as e:

        extra = ""

        if ext.lower() not in formats:
            extra = " ({} files are not supported by Ren'Py)".format(ext)

        elif formats[ext] and (not pygame.image.has_init(formats[ext])): # type:ignore
            extra = " (your SDL2_image library does not support {} files)".format(ext)

        raise Exception("Could not load image {!r}{}: {!r}".format(filename, extra, e))

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
