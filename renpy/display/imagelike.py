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

import renpy.display
from renpy.display.render import render, Render, Matrix2D

# This file contains displayables that are image-like, because they take
# up a rectangular area of the screen, and do not respond to input.

class Solid(renpy.display.core.Displayable):
    """
    :doc: disp_imagelike

    A displayable that fills the area its assigned with `color`.

    ::
    
        image white = Solid("#fff")
    
    """

    def __init__(self, color, **properties):

        super(Solid, self).__init__(**properties)

        if color is not None:
            self.color = renpy.easy.color(color)
        else:
            self.color = None

    def visit(self):
        if self.color:
            return [ renpy.display.im.SolidImage(self.color, 4, 4) ]
        else:
            return [ ]
        
    def render(self, width, height, st, at):

        color = self.color or self.style.color
        
        rv = Render(width, height)

        if color is None or width <= 0 or height <= 0:
            return rv

        SIZE = 10
        
        si = renpy.display.im.SolidImage(color, SIZE, SIZE)
        sr = render(si, SIZE, SIZE, st, at)

        rv.forward = Matrix2D(1.0 * SIZE / width, 0, 0, 1.0 * SIZE / height)
        rv.reverse = Matrix2D(1.0 * width / SIZE, 0, 0, 1.0 * height / SIZE)
        rv.blit(sr, (0, 0))

        return rv
        
class Frame(renpy.display.core.Displayable):
    """
    :doc: disp_imagelike
    :args: (image, xborder, yborder, tile=False, **properties)
    
    A displayable that resizes an image to fill the available area,
    while preserving the width and height of its borders.  is often
    used as the background of a window or button.

    .. figure:: frame_example.png

        Using a frame to resize an image to double its size.

    `image`
        An image manipulator that will be resized by this frame.

    `xborder`
        The width of the border on the left and right sides of the 
        image.

    `yborder`
        The height of the border on the top and bottom sides of the
        image.

    `tile`
        If true, tiling is used to resize sections of the image,
        rather than scaling.

    ::

         # Resize the background of the text window if it's too small.         
         init python:
             style.window.background = Frame("frame.png", 10, 10)
        """
        
    __version__ = 1

    def __init__(self, image, xborder, yborder, bilinear=True, tile=False, **properties):
        super(Frame, self).__init__(**properties)

        self.image = renpy.easy.displayable(image)
        self.xborder = xborder
        self.yborder = yborder
        self.tile = tile

    def render(self, width, height, st, at):

        crend = render(self.image, width, height, st, at)

        if isinstance(renpy.display.draw, renpy.display.swdraw.SWDraw):
            return self.sw_render(crend, width, height)

        def draw(x0, x1, y0, y1):

            # Compute the coordinates of the left, right, top, and
            # bottom sides of the region, for both the source and
            # destination surfaces.

            # left side.
            if x0 >= 0:
                dx0 = x0
                sx0 = x0
            else:
                dx0 = dw + x0
                sx0 = sw + x0

            # right side.
            if x1 > 0:
                dx1 = x1
                sx1 = x1
            else:
                dx1 = dw + x1
                sx1 = sw + x1

            # top side.
            if y0 >= 0:
                dy0 = y0
                sy0 = y0
            else:
                dy0 = dh + y0
                sy0 = sh + y0
        
            # bottom side
            if y1 > 0:
                dy1 = y1
                sy1 = y1
            else:
                dy1 = dh + y1
                sy1 = sh + y1

            # Quick exit.
            if sx0 == sx1 or sy0 == sy1:
                return
            
            # Compute sizes.
            csw = sx1 - sx0
            csh = sy1 - sy0
            cdw = dx1 - dx0
            cdh = dy1 - dy0

            if csw <= 0 or csh <= 0 or cdh <= 0 or cdw <= 0:
                return
            
            # Get a subsurface.
            cr = crend.subsurface((sx0, sy0, csw, csh))
                        
            # Scale or tile if we have to.
            if csw != cdw or csh != cdh:

                if self.tile:
                    newcr = Render(cdw, cdh)
                    newcr.clipping = True
                    
                    for x in xrange(0, cdw, csw):
                        for y in xrange(0, cdh, csh):
                            newcr.blit(cr, (x, y))

                    cr = newcr
                    
                else:
                    
                    newcr = Render(cdw, cdh)
                    newcr.forward = Matrix2D(1.0 * csw / cdw, 0, 0, 1.0 * csh / cdh)
                    newcr.reverse = Matrix2D(1.0 * cdw / csw, 0, 0, 1.0 * cdh / csh)
                    newcr.blit(cr, (0, 0))

                    cr = newcr

            # Blit.
            rv.blit(cr, (dx0, dy0))
            return
        

        sw, sh = crend.get_size()
        dw = int(width)
        dh = int(height)
        
        xb = min(self.xborder, sw / 2 - 1, width / 2 - 1)
        yb = min(self.yborder, sh / 2 - 1, height / 2 - 1) 
        
        rv = Render(dw, dh)

        self.draw_pattern(draw, xb, yb)
        
        return rv

    def draw_pattern(self, draw, xb, yb):
        # Top row.
        if yb:

            if xb:
                draw(0, xb, 0, yb)

            draw(xb, -xb, 0, yb)

            if xb:
                draw(-xb, 0, 0, yb)

        # Middle row.
        if xb:
            draw(0, xb, yb, -yb)

        draw(xb, -xb, yb, -yb)

        if xb:
            draw(-xb, 0, yb, -yb)

        # Bottom row.
        if yb:
            if xb:
                draw(0, xb, -yb, 0)

            draw(xb, -xb, -yb, 0)

            if xb:
                draw(-xb, 0, -yb, 0)

        
    
    def sw_render(self, crend, width, height):

        source = crend.render_to_texture(True)

        dw = int(width)
        dh = int(height)

        dest = renpy.display.pgrender.surface((dw, dh), True)
        rv = dest

        dest = renpy.display.scale.real(dest)
        source = renpy.display.scale.real(source)
        
        xb = renpy.display.scale.scale(self.xborder)
        yb = renpy.display.scale.scale(self.yborder)

        sw, sh = source.get_size()
        dw, dh = dest.get_size()

        xb = min(xb, sw / 2 - 1, dw / 2 - 1)
        yb = min(yb, sh / 2 - 1, dh / 2 - 1) 

        def draw(x0, x1, y0, y1):

            # Compute the coordinates of the left, right, top, and
            # bottom sides of the region, for both the source and
            # destination surfaces.

            # left side.
            if x0 >= 0:
                dx0 = x0
                sx0 = x0
            else:
                dx0 = dw + x0
                sx0 = sw + x0
        
            # right side.
            if x1 > 0:
                dx1 = x1
                sx1 = x1
            else:
                dx1 = dw + x1
                sx1 = sw + x1

            # top side.
            if y0 >= 0:
                dy0 = y0
                sy0 = y0
            else:
                dy0 = dh + y0
                sy0 = sh + y0
        
            # bottom side
            if y1 > 0:
                dy1 = y1
                sy1 = y1
            else:
                dy1 = dh + y1

                sy1 = sh + y1

            # Quick exit.
            if sx0 == sx1 or sy0 == sy1 or dx1 <= dx0 or dy1 <= dy0:
                return

            # Compute sizes.
            srcsize = (sx1 - sx0, sy1 - sy0)
            dstsize = (int(dx1 - dx0), int(dy1 - dy0))

            
            
            # Get a subsurface.
            surf = source.subsurface((sx0, sy0, srcsize[0], srcsize[1]))

            # Scale or tile if we have to.
            if dstsize != srcsize:
                if self.tile:
                    tilew, tileh = srcsize
                    dstw, dsth = dstsize

                    surf2 = renpy.display.pgrender.surface_unscaled(dstsize, surf)

                    for y in range(0, dsth, tileh):
                        for x in range(0, dstw, tilew):
                            surf2.blit(surf, (x, y))

                    surf = surf2 

                else:
                    surf2 = renpy.display.scale.real_transform_scale(surf, dstsize)
                    surf = surf2
                        
            # Blit.
            dest.blit(surf, (dx0, dy0))

        self.draw_pattern(draw, xb, yb)

        rrv = renpy.display.render.Render(width, height)
        rrv.blit(rv, (0, 0))
        rrv.depends_on(crend)
                      
        # And, finish up.
        return rrv
    
    def visit(self):
        return [ self.image ]


