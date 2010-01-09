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
from renpy.display.render import render, Render


Image = renpy.display.im.image

def wrap_render(child, w, h, st, at):
    rend = render(child, w, h, st, at)
    rv = Render(rend.width, rend.height)
    rv.blit(rend, (0, 0))
    return rv
            

class UncachedImage(renpy.display.core.Displayable):
    """
    An image that is loaded immediately and not cached.
    """

    def __init__(self, file, hint=None, scale=None, style='image_placement',
                 **properties):

        super(UncachedImage, self).__init__(style=style, **properties)

        self.surf = renpy.display.pgrender.load_image(file, hint)

        if scale:
            renpy.display.render.blit_lock.acquire()
            self.surf = renpy.display.pgrender.transform_scale(self.surf, scale)
            renpy.display.render.blit_lock.release()
            
        renpy.display.render.mutated_surface(self.surf)

    def render(self, w, h, st, at):
        sw, sh = self.surf.get_size()
        rv = renpy.display.render.Render(sw, sh)
        rv.blit(self.surf, (0, 0))

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

    def get_parameterized(self):
        if self.param_target:
            return self.param_target.get_parameterized()

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


    def hide(self, st, at):
        if not self.target:
            self.find_target()

        return self.target.hide(st, at)

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
    Returns a Displayable that is solid, and filled with a single
    color. A Solid expands to fill all the space allocated to it,
    making it suitable for use as a background.
    """
    def __init__(self, color, **properties):
        """
        @param color: An RGBA tuple, giving the color that the display
        will be filled with.
        """
        
        super(Solid, self).__init__(**properties)

        if color is not None:
            self.color = renpy.easy.color(color)
        else:
            self.color = None
            
    def render(self, width, height, st, at):

        color = self.color or self.style.color
        
        si = renpy.display.im.SolidImage(color,
                                         width,
                                         height)

        return wrap_render(si, width, height, st, at)
        
class Frame(renpy.display.core.Displayable):
    """
    Returns a Displayable that is a frame, based on the supplied image
    filename. A frame is an image that is automatically rescaled to
    the size allocated to it. The image has borders that are only
    scaled in one axis. The region within xborder pixels of the left
    and right borders is only scaled in the y direction, while the
    region within yborder pixels of the top and bottom axis is scaled
    only in the x direction. The corners are not scaled at all, while
    the center of the image is scaled in both x and y directions.
    """

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.bilinear = False
    
    def __init__(self, image, xborder, yborder, bilinear=False, tile=False, **properties):
        """
        @param image: The image (which may be a filename or image
        object) that will be scaled.

        @param xborder: The number of pixels in the x direction to use as
        a border.

        @param yborder: The number of pixels in the y direction to use as
        a border.

        @param tile: If true, instead of scaling a region, we tile that
        region.

        For better performance, have the image share a dimension
        length in common with the size the frame will be rendered
        at. We detect this and avoid scaling if possible.
        """

        super(Frame, self).__init__(**properties)

        self.image = Image(image)
        self.xborder = xborder
        self.yborder = yborder
        self.tile = tile
        self.bilinear = bilinear

    def render(self, width, height, st, at):

        fi = renpy.display.im.FrameImage(self.image,
                                         self.xborder,
                                         self.yborder,
                                         width,
                                         height,
                                         self.tile,
                                         self.bilinear)

        return wrap_render(fi, width, height, st, at)

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
