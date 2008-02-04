# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# This file mediates access to the _renpy module, which is a C module that
# allows us to enhance the feature set of pygame in a renpy specific way.

import renpy
import pygame
from pygame.constants import *

import sys

try:
    import _renpy
    version = _renpy.version()

    if version < 5006000:
        print >>sys.stderr, "The _renpy module was found, but is out of date.\nPlease read module/README.txt for more information."
        
except:
    # If for any reason we can't import the module, we have a version
    # number of 0.

    print >>sys.stderr, "The _renpy module was not found. Please read module/README.txt for"
    print >>sys.stderr, "more information."

    version = 0


def convert_and_call(function, src, dst, *args):
    """
    This calls the function with the source and destination
    surface. The surfaces must have the same alpha.

    If the surfaces are not 24 or 32 bits per pixel, or don't have the
    same format, they are converted and then converted back.
    """

    if (dst.get_masks()[3] != 0) != (src.get_masks()[3] != 0):
        raise Exception("Surface alphas do not match.")

    dstsize = dst.get_bitsize()

    if dst.get_bitsize() in (24, 32):
        target = dst
    else:
        if dst.get_masks()[3]:
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
            
        if can_bilinear_scale:
            bilinear_scale(s, d)
        else:
            pixellate(s, d, width / dx, height / dy, 1, 1)

        return d

else:

    can_pixellate = False

    def scale(s, size):

        return pygame.transform.scale(s, size)

# def slow_endian_order(shifts, masks, r, g, b, a):

#     has_alpha = masks[3]

#     if not has_alpha:

#         l = zip(shifts, (r, g, b))
#         l.sort()

#         if sys.byteorder == 'big':
#             l.reverse()

#         return [ j for i, j in l] + [ a ]

    
#     l = zip(shifts, (r, g, b, a))
#     l.sort()

#     if sys.byteorder == 'big':
#         l.reverse()

#     return [ j for i, j in l]

    
# endian_order_cache = { }


# def endian_order(src, r, g, b, a):
#     """
#     Returns the four arguments, in endian-order.
#     """

#     shifts = src.get_shifts()

#     try:
#         func = endian_order_cache[shifts]

#     except KeyError:
#         masks = src.get_masks()
#         order = slow_endian_order(shifts, masks, 'r', 'g', 'b', 'a')
#         func = eval( "lambda r, g, b, a : (" + ", ".join(order) + ")")
#         endian_order_cache[shifts] = func

#     return func(r, g, b, a)
        

# Okay, what we have here are a pair of tables mapping masks to byte offsets
# for 24 and 32 bpp modes. We represent 0xff000000 as positive and negative
# numbers so that it doesn't yield a warning, and so that it works on
# 32 and 64 bit platforms.
if sys.byteorder == 'big':
    bo24 = { 255 : 2, 65280 : 1, 16711680 : 0, }
    bo32 = { 255 : 3, 65280 : 2, 16711680 : 1, 4278190080 : 0, -16777216 : 0, }
else:
    bo24 = { 255 : 0, 65280 : 1, 16711680 : 2, }
    bo32 = { 255 : 0, 65280 : 1, 16711680 : 2, 4278190080 : 3, -16777216 : 3, }


def byte_offset(src):
    """
    Given the surface src, returns a 4-tuple giving the byte offsets
    for the red, green, blue, and alpha components of the pixels in
    the surface. If a component doesn't exist, None is returned.
    """

    if src.get_bytesize() == 3:
        bo = bo24
    else:
        bo = bo32

    return [ bo.get(i, None) for i in src.get_masks() ]


def endian_order(src, r, g, b, a):
    rv = [ a ] * 4

    for i, index_i in zip((r, g, b, a), byte_offset(src)):
        if index_i is not None:
            rv[index_i] = i

    return rv


if version >= 5005000:

    can_linmap = True

    def linmap(src, dst, rmap, gmap, bmap, amap):
        """
        This maps the colors between two surfaces. The various map
        parameters should be fixed-point integers, with 1.0 == 256.
        """
        
        convert_and_call(_renpy.linmap,
                         src, dst,
                         *endian_order(dst, rmap, gmap, bmap, amap))


    save_png = _renpy.save_png

else:

    can_linmap = False

    def save_png(surf, file):
        return
    

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


if can_map or can_linmap:

    can_twomap = True

    def twomap(src, dst, white, black):
        """
        Given colors for white and black, linearly maps things
        appropriately, taking the alpha channel from white.
        """

        wr = white[0]
        wg = white[1]
        wb = white[2]
        wa = white[3]
 
        br = black[0]
        bg = black[1]
        bb = black[2]

        ramp = renpy.display.im.ramp

        if can_linmap and br == 0 and bg == 0 and bb == 0:
            linmap(src, dst,
                   wr + 1,
                   wg + 1,
                   wb + 1,
                   wa + 1)
        else:
            map(src, dst,
                ramp(br, wr),
                ramp(bg, wg),
                ramp(bb, wb),
                ramp(0, wa))

else:

    can_twomap = False
    


if version >= 4008007:

    can_munge = True

    def alpha_munge(src, dst, amap):
        """
        This samples the red channel from src, maps it through amap, and
        place it into the alpha channel of amap.
        """

        if src.get_size() != dst.get_size():
            return

        red = byte_offset(src)[0]
        alpha = byte_offset(dst)[3]

        if red is not None and alpha is not None:
            _renpy.alpha_munge(src, dst, red, alpha, amap)        

else:

    can_munge = False

    def alpha_munge(src, dst, amap):
        return



if version >= 5006000:

    can_bilinear_scale = True

    def bilinear_scale(src, dst, sx=0, sy=0, sw=None, sh=None, dx=0, dy=0, dw=None, dh=None):

        if sw is None:
            sw, sh = src.get_size()
        if dw is None:
            dw, dh = dst.get_size()
            
        while True:

            if sw <= dw * 2 and sh <= dh * 2:
                break

            nsw = max(sw / 2, dw)
            nsh = max(sh / 2, dh)

            nsrc = pygame.Surface((nsw, nsh), src.get_flags())
            _renpy.bilinear(src, nsrc, sx, sy, sw, sh)
            sx = 0
            sy = 0
            sw = nsw
            sh = nsh
            src = nsrc

        _renpy.bilinear(src, dst, sx, sy, sw, sh, dx, dy, dw, dh)
        

    
else:

    can_bilinear_scale = False

    def bilinear_scale(src, dst, sx=0, sy=0, sw=None, sh=None, dx=0, dy=0, dw=None, dh=None):
        return

    

if version >= 5006006:

    can_transform = True
    transform = _renpy.transform

else:

    can_transform = False


    
if version >= 6001000:

    # Note: Blend requires all surfaces to be the same size.
    
    can_blend = True
    blend = _renpy.blend

else:

    can_blend = False


if version >= 6001000:

    # Note: Blend requires all surfaces to be the same size.
    
    can_imageblend = True

    def imageblend(a, b, dst, img, amap):        
        red = byte_offset(img)[0]
        _renpy.imageblend(a, b, dst, img, red, amap)

else:

    can_imageblend = False

if version >= 6002001:

    can_colormatrix = True

    def colormatrix(src, dst, matrix):
        c = [ matrix[0:5], matrix[5:10], matrix[10:15], matrix[15:20] ]
        offs = byte_offset(src)

        o = [ None ] * 4
        for i in range(0, 4):
            o[offs[i]] = i
        
        _renpy.colormatrix(src, dst,
                           c[o[0]][o[0]], c[o[0]][o[1]], c[o[0]][o[2]], c[o[0]][o[3]], c[o[0]][4],    
                           c[o[1]][o[0]], c[o[1]][o[1]], c[o[1]][o[2]], c[o[1]][o[3]], c[o[1]][4],    
                           c[o[2]][o[0]], c[o[2]][o[1]], c[o[2]][o[2]], c[o[2]][o[3]], c[o[2]][4],    
                           c[o[3]][o[0]], c[o[3]][o[1]], c[o[3]][o[2]], c[o[3]][o[3]], c[o[3]][4])

else:
    can_colormatrix = False
