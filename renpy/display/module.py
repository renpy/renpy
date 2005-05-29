# This file mediates access to the _renpy module, which is a C module that
# allows us to enhance the feature set of pygame in a renpy specific way.

import pygame
from pygame.constants import *

import sys

try:
    import _renpy
    version = _renpy.version()
except:
    # If for any reason we can't import the module, we have a version
    # number of 0.

    print "The _renpy module was not found. Please read module/README.txt for"
    print "more information."

    version = 0


def convert_and_call(function, src, dst, *args):
    """
    This calls the function with the source and destination
    surface. The surfaces must have the same alpha.

    If the surfaces are not 24 or 32 bits per pixel, or don't have the
    same format, they are converted and then converted back.
    """

    if dst.get_flags() & SRCALPHA != src.get_flags() & SRCALPHA:
        raise Exception("Surface alphas do not match.")

    dstsize = dst.get_bitsize()

    if dst.get_bitsize() in (24, 32):
        target = dst
    else:
        if dst.get_flags() & SRCALPHA:
            target = pygame.Surface(dst.get_size(), SRCALPHA, 32)
        else:
            target = pygame.Surface(dst.get_size(), 0, 24)

    if src.get_bitsize() == target.get_bitsize():
        source = src
    else:
        source = src.convert(target)
    
    function(source, target, *args)

    if target is not dst:
        dst.blit(target, (0, 0))


if version >= 4008002:

    can_pixellate = True

    def pixellate(src, dst, avgwidth, avgheight, outwidth, outheight):
        """
        This pixellates the source surface. First, every pixel in the
        source surface is projected onto a virtual surface, such that
        the average value of every avgwidth x avgheight pixels becomes
        one virtual pixel. It then gets projected back onto the
        destination surface at a ratio of one virtual pixel to every
        outwidth x outheight destination pixels.

        If either src or dst is not a 24 or 32 bit surface, they are
        converted... but that may be a significant performance hit.
        
        The two surfaces must either have the same alpha or no alpha.
        """

        convert_and_call(_renpy.pixellate,
                         src, dst,
                         avgwidth, avgheight,
                         outwidth, outheight)

    
    def scale(s, size):
        """
        Scales down the supplied pygame surface by the given X and Y
        factors.

        Always works, but may not be high quality.
        """

        width, height = s.get_size()

        dx, dy = size

        if s.get_flags() & SRCALPHA:
            d = pygame.Surface((dx, dy), SRCALPHA)
        else:
            d = pygame.Surface((dx, dy), 0)

        pixellate(s, d, width / dx, height / dy, 1, 1)

        return d

else:

    can_pixellate = False

    def scale(s, size):

        return pygame.transform.scale(s, size)




def slow_endian_order(shifts, masks, r, g, b, a):

    has_alpha = masks[3]

    if not has_alpha:

        l = zip(shifts, (r, g, b))
        l.sort()

        if sys.byteorder == 'big':
            l.reverse()

        return [ j for i, j in l] + [ a ]

    
    l = zip(shifts, (r, g, b, a))
    l.sort()

    if sys.byteorder == 'big':
        l.reverse()

    return [ j for i, j in l]

    
endian_order_cache = { }


def endian_order(src, r, g, b, a):
    """
    Returns the four arguments, in endian-order.
    """

    shifts = src.get_shifts()

    try:
        func = endian_order_cache[shifts]

    except KeyError:
        masks = src.get_masks()
        order = slow_endian_order(shifts, masks, 'r', 'g', 'b', 'a')
        func = eval( "lambda r, g, b, a : (" + ", ".join(order) + ")")
        endian_order_cache[shifts] = func

    return func(r, g, b, a)
        
    

if version >= 4008005:

    can_map = True

    def map(src, dst, rmap, gmap, bmap, amap):
        """
        This maps the colors between two surfaces. The various map
        parameters must be 256 character long strings, with the value
        of a character at a given offset being what a particular pixel
        component value is mapped to.
        """

        convert_and_call(_renpy.map,
                         src, dst,
                         *endian_order(dst, rmap, gmap, bmap, amap))


else:

    can_map = False
    

        
