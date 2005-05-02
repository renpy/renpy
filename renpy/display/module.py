# This file mediates access to the _renpy module, which is a C module that
# allows us to enhance the feature set of pygame in a renpy specific way.

import pygame
from pygame.constants import *

try:
    import _renpy
    version = _renpy.version()
except:
    # If for any reason we can't import the module, we have a version
    # number of 0.
    version = 0


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

        if dst.get_flags() & SRCALPHA != src.get_flags() & SRCALPHA:
            raise Exception("Surface alphas do not match.")

        if dst.get_flags() & SRCALPHA:
            use_alpha = True
        else:
            use_alpha = False

        if use_alpha:

            if src.get_bitsize() != 32:
                source = src.convert(32, SRCALPHA)
            else:
                source = src

            if dst.get_bitsize() != 32:
                target = pygame.Surface(dst.get_size(), SRCALPHA, 32)
            else:
                target = dst

        else:

            if src.get_bitsize() != 24:
                source = src.convert(24)
            else:
                source = src

            if dst.get_bitsize() != 24:
                target = pygame.Surface(dst.get_size(), 0, 24)
            else:
                target = dst

        _renpy.pixellate(source, target, avgwidth, avgheight, outwidth, outheight)

        if target is not dst:
            dst.blit(target, (0, 0))

    
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

    

