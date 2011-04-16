#cython: profile=False
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

import renpy
import math

from renpy.display.render cimport Render, Matrix2D, render

cdef Matrix2D IDENTITY
IDENTITY = renpy.display.render.IDENTITY

# This file contains implementations of methods of classes that
# are found in other files, for performance reasons.

def transform_render(self, widtho, heighto, st, at):

    cdef double rxdx, rxdy, rydx, rydy
    cdef double nxdx, nxdy, nydx, nydy
    cdef double xdx, xdy, ydx, ydy
    cdef double xo, x1, x2, x3
    cdef double yo, y1, y2, y3
    cdef float zoom, xzoom, yzoom
    cdef double cw, ch, nw, nh
    cdef Render rv, cr
    cdef double angle
    cdef double alpha
    cdef double width = widtho
    cdef double height = heighto
    
    # Should we perform clipping?
    clipping = False

    # Preserve the illusion of linear time.
    if st == 0:
        self.st_offset = self.st
    if at == 0:
        self.at_offset = self.at

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

        if x1 < x2:
            minx = x1
            maxx = x2
        else:
            minx = x2
            maxx = x1

        if y1 < y2:
            miny = y1
            maxy = y2
        else:
            miny = y2
            maxy = y1

        crop = (minx, miny, maxx - minx, maxy - miny)

    if crop is not None:

        negative_xo, negative_yo, width, height = crop
        xo = -negative_xo
        yo = -negative_yo

        clipping = True

        if state.rotate:
            clipcr = Render(width, height)
            clipcr.subpixel_blit(cr, (xo, yo))
            clipcr.clipping = clipping
            xo = yo = 0
            cr = clipcr
            clipping = False

    # Size.
    size = state.size 
    if (size is not None) and (size != (width, height)):
        nw, nh = size
        xzoom = 1.0 * nw / width
        yzoom = 1.0 * nh / height

        rxdx = xzoom
        rydy = yzoom

        xo = xo * xzoom
        yo = yo * yzoom

        width, height = size

    # Rotation.
    rotate = state.rotate
    if rotate is not None:

        cw = width
        ch = height

        angle = rotate * 3.1415926535897931 / 180

        xdx = math.cos(angle)
        xdy = -math.sin(angle)
        ydx = -xdy 
        ydy = xdx 

        # reverse = Matrix2D(xdx, xdy, ydx, ydy) * reverse

        # We know that at this point, rxdy and rydx are both 0, so
        # we can simplify these formulae a bit.            
        nxdx = rxdx * xdx
        rxdy = rxdx * xdy
        rydx = rydy * ydx
        nydy = rydy * ydy

        rxdx = nxdx
        rydy = nydy

        if state.rotate_pad:
            width = height = math.hypot(cw, ch)

            xo = -cw / 2.0 * rxdx + -ch / 2.0 * rxdy
            yo = -cw / 2.0 * rydx + -ch / 2.0 * rydy

        else:
            xo = -cw / 2.0 * rxdx + -ch / 2.0 * rxdy
            yo = -cw / 2.0 * rydx + -ch / 2.0 * rydy

            x2 = -cw / 2.0 * rxdx + ch / 2.0 * rxdy
            y2 = -cw / 2.0 * rydx + ch / 2.0 * rydy

            x3 = cw / 2.0 * rxdx + ch / 2.0 * rxdy
            y3 = cw / 2.0 * rydx + ch / 2.0 * rydy

            x4 = cw / 2.0 * rxdx + -ch / 2.0 * rxdy
            y4 = cw / 2.0 * rydx + -ch / 2.0 * rydy

            width = max(xo, x2, x3, x4) - min(xo, x2, x3, x4) 
            height = max(yo, y2, y3, y4) - min(yo, y2, y3, y4) 

        xo += width / 2.0
        yo += height / 2.0
        
    zoom = state.zoom
    xzoom = zoom * <double> state.xzoom
    yzoom = zoom * <double> state.yzoom
    alpha = state.alpha

    if xzoom != 1 or yzoom != 1:

        nxdx = rxdx * xzoom
        nxdy = rxdy * yzoom
        nydx = rydx * xzoom
        nydy = rydy * yzoom

        rxdx = nxdx
        rxdy = nxdy
        rydx = nydx
        rydy = nydy

        width *= xzoom
        height *= yzoom

        xo *= xzoom
        yo *= yzoom

    rv = Render(width, height)

    # Default case - no transformation matrix.
    if rxdx == 1 and rxdy == 0 and rydx == 0 and rydy == 0:
        self.forward = IDENTITY

    else:
        inv_det = rxdx * rydy - rxdy * rydx

        rv.reverse = Matrix2D(rxdx, rxdy, rydx, rydy)

        if not inv_det:
            self.forward = rv.forward = Matrix2D(0, 0, 0, 0)
        else:
            self.forward = rv.forward = Matrix2D(
                rydy / inv_det,
                -rxdy / inv_det,
                -rydx / inv_det, 
                rxdx / inv_det)

    rv.alpha = alpha
    rv.clipping = clipping

    pos = (xo, yo)
    
    if state.subpixel:
        rv.subpixel_blit(cr, pos)
    else:
        rv.blit(cr, pos)

    self.offsets = [ pos ]

    return rv

