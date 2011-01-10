# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

# This file contains some miscellaneous displayables that involve images.
# Most of the guts of this file have been moved into im.py, with only some
# of the stuff thar uses images remaining.

import renpy
from renpy.display.render import render, Render, Matrix2D

Image = renpy.display.im.image

def wrap_render(child, w, h, st, at):
    rend = render(child, w, h, st, at)
    rv = Render(rend.width, rend.height)
    rv.blit(rend, (0, 0))
    return rv

class ImageReference(renpy.display.core.Displayable):
    """
    ImageReference objects are used to reference images by their name,
    which is a tuple of strings corresponding to the name used to define
    the image in an image statment.
    """

    nosave = [ 'target' ]
    target = None
    param_target = None
    
    def __init__(self, name, **properties):
        """
        @param name: A tuple of strings, the name of the image. Or else
        a displayable, containing the image directly.
        """
        
        super(ImageReference, self).__init__(**properties)

        self.name = name

    def _get_parameterized(self):
        if self.param_target:
            return self.param_target._get_parameterized()

        return self
        
    def find_target(self):

        if self.param_target:
            self.target = self.param_target
            return None

        name = self.name

        if isinstance(name, renpy.display.core.Displayable):
            self.target = name
            return True
        
        if not isinstance(name, tuple):
            name = tuple(name.split())
        
        parameters = [ ]

        def error(msg):
            self.target = renpy.display.text.Text(msg, color=(255, 0, 0, 255), xanchor=0, xpos=0, yanchor=0, ypos=0)

            if renpy.config.debug:
                raise Exception(msg)

            
        # Scan through, searching for an image (defined with an
        # input statement) that is a prefix of the given name.
        while name:
            if name in renpy.exports.images:
                target = renpy.exports.images[name]

                try:
                    self.target = target.parameterize(name, parameters)
                    if self.target is not target:
                        self.param_target = self.target

                except Exception, e:
                    if renpy.config.debug:
                        raise

                    error(str(e))

                return True

            else:
                parameters.insert(0, name[-1])
                name = name[:-1]

        error("Image '%s' not found." % ' '.join(self.name))
        return False


    def _hide(self, st, at, kind):
        if not self.target:
            self.find_target()

        return self.target._hide(st, at, kind)

    def set_transform_event(self, event):
        if not self.target:
            self.find_target()

        return self.target.set_transform_event(event)
    
    def event(self, ev, x, y, st):
        if not self.target:
            self.find_target()

        return self.target.event(ev, x, y, st)
        
    def render(self, width, height, st, at):
        if not self.target:
            self.find_target()

        return wrap_render(self.target, width, height, st, at)

    def get_placement(self):
        if not self.target:
            self.find_target()

        if not renpy.config.imagereference_respects_position:
            return self.target.get_placement()
            
        xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = self.target.get_placement()

        if xpos is None:
            xpos = self.style.xpos

        if ypos is None:
            ypos = self.style.ypos

        if xanchor is None:
            xanchor = self.style.xanchor

        if yanchor is None:
            yanchor = self.style.yanchor
            
        return xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel

    def visit(self):
        if not self.target:
            self.find_target()

        return [ self.target ]
    
    
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
        

        crend = render(self.image, width, height, st, at)
        sw, sh = crend.get_size()
        dw = width
        dh = height
        
        xb = self.xborder
        yb = self.yborder

        if xb * 2 >= sw:
            xb = sw / 2 - 1

        if yb * 2 >= sh:
            yb = sh / 2 - 1

        rv = Render(dw, dh)
            
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

        return rv

    def visit(self):
        return [ self.image ]


class ImageButton(renpy.display.behavior.Button):
    """
    Used to implement the guts of an image button.
    """

    def __init__(self,
                 idle_image,
                 hover_image,
                 insensitive_image = None,
                 activate_image = None,
                 selected_idle_image = None,
                 selected_hover_image = None,
                 selected_insensitive_image = None,
                 selected_activate_image = None,                 
                 style='image_button',
                 clicked=None,
                 hovered=None,
                 **properties):

        insensitive_image = insensitive_image or idle_image
        activate_image = activate_image or hover_image

        selected_idle_image = selected_idle_image or idle_image
        selected_hover_image = selected_hover_image or hover_image
        selected_insensitive_image = selected_insensitive_image or insensitive_image
        selected_activate_image = selected_activate_image or activate_image

        self.state_children = dict(
            idle_ = renpy.easy.displayable(idle_image),
            hover_ = renpy.easy.displayable(hover_image),
            insensitive_ = renpy.easy.displayable(insensitive_image),
            activate_ = renpy.easy.displayable(activate_image),

            selected_idle_ = renpy.easy.displayable(selected_idle_image),
            selected_hover_ = renpy.easy.displayable(selected_hover_image),
            selected_insensitive_ = renpy.easy.displayable(selected_insensitive_image),
            selected_activate_ = renpy.easy.displayable(selected_activate_image),
            )

        super(ImageButton, self).__init__(renpy.display.layout.Null(),
                                          style=style,
                                          clicked=clicked,
                                          hovered=hovered,
                                          **properties)
        
    def visit(self):
        return self.state_children.values()

    def get_child(self):
        return self.style.child or self.state_children[self.style.prefix]

