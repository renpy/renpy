#cython: profile=False
# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import renpy
import math
from renpy.display.render cimport Render, Matrix2D, render
from renpy.display.core import absolute

from sdl2 cimport *
from pygame_sdl2 cimport *

import_pygame_sdl2()

################################################################################
# Surface copying
################################################################################


def nogil_copy(src, dest):
    """
    Does a gil-less blit of src to dest, with minimal locking.
    """

    cdef SDL_Surface *src_surf
    cdef SDL_Surface *dst_surf

    src_surf = PySurface_AsSurface(src)
    dest_surf = PySurface_AsSurface(dest)

    with nogil:
        SDL_SetSurfaceBlendMode(src_surf, SDL_BLENDMODE_NONE)
        SDL_UpperBlit(src_surf, NULL, dest_surf, NULL)

################################################################################
# Transform render function
################################################################################

cdef Matrix2D IDENTITY
IDENTITY = renpy.display.render.IDENTITY

# This file contains implementations of methods of classes that
# are found in other files, for performance reasons.

def transform_render(self, widtho, heighto, st, at):

    cdef double rxdx, rxdy, rydx, rydy
    cdef double cosa, sina
    cdef double xo, x1, x2, x3, px
    cdef double yo, y1, y2, y3, py
    cdef float zoom, xzoom, yzoom
    cdef double cw, ch, nw, nh
    cdef Render rv, cr
    cdef double angle
    cdef double alpha
    cdef double width = widtho
    cdef double height = heighto

    # Should we perform clipping?
    clipping = False

    # Prevent time from ticking backwards, as can happen if we replace a
    # transform but keep its state.
    if st + self.st_offset <= self.st:
        self.st_offset = self.st - st
    if at + self.at_offset <= self.at:
        self.at_offset = self.at - at

    self.st = st = st + self.st_offset
    self.at = at = at + self.at_offset

    # Update the state.
    self.update_state()

    # Render the child.
    child = self.child

    if child is None:
        raise Exception("Transform does not have a child.")

    state = self.state

    if state.size:
        widtho, heighto = state.size

    cr = render(child, widtho, heighto, st - self.child_st_base, at)

    width = cr.width
    height = cr.height

    self.child_size = width, height

    # The reverse matrix.
    rxdx = 1
    rxdy = 0
    rydx = 0
    rydy = 1

    xo = 0
    yo = 0

    # Cropping.
    crop = state.crop
    if (state.corner1 is not None) and (crop is None) and (state.corner2 is not None):
        x1, y1 = state.corner1
        x2, y2 = state.corner2

        if x1 > x2:
            x3 = x1
            x1 = x2
            x2 = x3
        if y1 > y2:
            y3 = y1
            y1 = y2
            y2 = y3

        crop = (x1, y1, x2-x1, y2-y1)

    if crop is not None:

        if state.crop_relative:
            x, y, w, h = crop

            def relative(n, base, limit):
                if isinstance(n, (int, absolute)):
                    return n
                else:
                    return min(int(n * base), limit)

            x = relative(x, width, width)
            y = relative(y, height, height)
            w = relative(w, width, width - x)
            h = relative(h, height, height - y)

            crop = (x, y, w, h)

        negative_xo, negative_yo, width, height = crop

        if state.rotate:
            clipcr = Render(width, height)
            clipcr.subpixel_blit(cr, (-negative_xo, -negative_yo))
            clipcr.clipping = True
            cr = clipcr
        else:
            xo = -negative_xo
            yo = -negative_yo
            clipping = True

    # Size.
    size = state.size
    if (size is not None) and (size != (width, height)) and (width != 0) and (height != 0):
        nw, nh = size

        xzoom = 1.0 * nw / width
        yzoom = 1.0 * nh / height

        rxdx = xzoom
        rydy = yzoom

        xo *= xzoom
        yo *= yzoom

        width, height = size

    # zoom
    zoom = state.zoom
    xzoom = zoom * <double> state.xzoom
    yzoom = zoom * <double> state.yzoom

    if xzoom != 1:

        rxdx *= xzoom

        if xzoom < 0:
            width *= -xzoom
        else:
            width *= xzoom

        xo *= xzoom
        # origin corrections for flipping
        if xzoom < 0:
            xo += width

    if yzoom != 1:

        rydy *= yzoom

        if yzoom < 0:
            height *= -yzoom
        else:
            height *= yzoom

        yo *= yzoom
        # origin corrections for flipping
        if yzoom < 0:
            yo += height

    # Rotation.
    rotate = state.rotate
    if rotate is not None:

        cw = width
        ch = height

        angle = rotate * 3.1415926535897931 / 180

        cosa = math.cos(angle)
        sina = math.sin(angle)

        # reverse = Matrix2D(xdx, xdy, ydx, ydy) * reverse

        # We know that at this point, rxdy and rydx are both 0, so
        # we can simplify these formulae a bit.
        rxdy = rydy * -sina
        rydx = rxdx * sina
        rxdx *= cosa
        rydy *= cosa

        # first corner point (changes with flipping)
        px = cw / 2.0
        if xzoom < 0:
            px = -px
        py = ch / 2.0
        if yzoom < 0:
            py = -py

        if state.rotate_pad:
            width = height = math.hypot(cw, ch)

            xo = -px * cosa + py * sina
            yo = -px * sina - py * cosa

        else:
            xo = -px * cosa + py * sina
            yo = -px * sina - py * cosa

            x2 = -px * cosa - py * sina
            y2 = -px * sina + py * cosa

            x3 =  px * cosa - py * sina
            y3 =  px * sina + py * cosa

            x4 =  px * cosa + py * sina
            y4 =  px * sina - py * cosa

            width = max(xo, x2, x3, x4) - min(xo, x2, x3, x4)
            height = max(yo, y2, y3, y4) - min(yo, y2, y3, y4)

        xo += width / 2.0
        yo += height / 2.0

    rv = Render(width, height)

    # Default case - no transformation matrix.
    if rxdx == 1 and rxdy == 0 and rydx == 0 and rydy == 1:
        self.forward = IDENTITY
        self.reverse = IDENTITY

    else:

        self.reverse = rv.reverse = Matrix2D(rxdx, rxdy, rydx, rydy)

        inv_det = rxdx * rydy - rxdy * rydx

        if not inv_det:
            self.forward = rv.forward = Matrix2D(0, 0, 0, 0)
        else:
            self.forward = rv.forward = Matrix2D(
                rydy / inv_det,
                -rxdy / inv_det,
                -rydx / inv_det,
                rxdx / inv_det)

    rv.nearest = state.nearest
    rv.alpha = state.alpha
    rv.over = 1.0 - state.additive
    rv.clipping = clipping

    pos = (xo, yo)

    if state.subpixel:
        rv.subpixel_blit(cr, pos)
    else:
        rv.blit(cr, pos)

    self.offsets = [ pos ]
    self.render_size = (width, height)

    return rv

