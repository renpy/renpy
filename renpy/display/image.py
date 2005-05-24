# This file contains some miscellanious displayables that involve images.
# Most of the guts of this file have been moved into im.py, with only some
# of the stuff thar uses images remaining.

import renpy
from renpy.display.render import render

import pygame
from pygame.constants import *

Image = renpy.display.im.image

class UncachedImage(renpy.display.core.Displayable):
    """
    An image that is loaded immediately and not cached.
    """

    def __init__(self, file, hint=None, scale=None, style='image_placement',
                 **properties):

        super(UncachedImage, self).__init__()

        self.surf = pygame.image.load(file, hint)
        self.surf = self.surf.convert_alpha()

        if scale:
            self.surf = pygame.transform.scale(self.surf, scale)

        renpy.display.render.mutated_surface(self.surf)

        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def render(self, w, h, st):
        sw, sh = self.surf.get_size()
        rv = renpy.display.render.Render(sw, sh)
        rv.blit(self.surf, (0, 0))

        return rv

    # Should never be called, but what the hey?
    def predict(self, callback):
        return None

class ImageReference(renpy.display.core.Displayable):
    """
    This is a reference to an image or animation that is kept
    in exports.images.

    @ivar name: The name of the image.

    Not serialized:

    @ivar target: If defined, a pointer to the thing that name resolves to.
    """

    nosave = [ 'target' ]

    def __init__(self, name):
        super(ImageReference, self).__init__()

        self.name = name

    def find_target(self):
        import renpy.exports as exports

        name = self.name
        parameters = [ ]

        def error(msg):
            self.target = renpy.display.text.Text(msg, color=(255, 0, 0, 255))

            if renpy.config.debug:
                raise Exception(msg)

            
        # Scan through, searching for an image (defined with an
        # input statement) that is a prefix of the given name.
        while name:
            if name in exports.images:
                target = exports.images[name]

                try:
                    self.target = target.parameterize(name, parameters)
                except Exception, e:
                    if renpy.config.debug:
                        raise

                    error(str(e))

                return

            else:
                parameters.insert(0, name[-1])
                name = name[:-1]

        error("Image '%s' not found." % ' '.join(self.name))
        
        
    def render(self, width, height, st):
        if not hasattr(self, 'target'):
            self.find_target()

        return render(self.target, width, height, st)

    def get_placement(self):
        if not hasattr(self, 'target'):
            self.find_target()

        return self.target.get_placement()

    def predict(self, callback):
        if not hasattr(self, 'target'):
            self.find_target()

        self.target.predict(callback)
    
    
class Solid(renpy.display.core.Displayable):
    """
    Returns a Displayable that is solid, and filled with a single
    color. A Solid expands to fill all the space allocated to it,
    making it suitable for use as a background.
    """

    def __init__(self, color):
        """
        @param color: An RGBA tuple, giving the color that the display
        will be filled with.
        """
        
        super(Solid, self).__init__()
        self.color = color

    def render(self, width, height, st):

        si = renpy.display.im.SolidImage(self.color,
                                         width,
                                         height)

        return render(si, width, height, st)
        
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

    def __init__(self, image, xborder, yborder):
        """
        @param image: The image (which may be a filename or image
        object) that will be scaled.

        @param xborder: The number of pixels in the x direction to use as
        a border.

        @param yborder: The number of pixels in the y direction to use as
        a border.

        For better performance, have the image share a dimension
        length in common with the size the frame will be rendered
        at. We detect this and avoid scaling if possible.
        """

        super(Frame, self).__init__()

        self.image = Image(image)
        self.xborder = xborder
        self.yborder = yborder

    def render(self, width, height, st):

        fi = renpy.display.im.FrameImage(self.image,
                                         self.xborder,
                                         self.yborder,
                                         width,
                                         height)

        return render(fi, width, height, st)

    def predict(self, callback):
        self.image.predict(callback)

# This class has been replaced with a function in anim.
class OldAnimation(renpy.display.core.Displayable):
    """
    A Displayable that draws an animation, which is a series of images
    that are displayed with time delays between them.
    """

    def __init__(self, *args):
        """
        Odd (first, third, fifth, etc.) arguments to Animation are
        interpreted as image filenames, while even arguments are the
        time to delay between each image. If the number of arguments
        is odd, the animation will stop with the last image (well,
        actually delay for a year before looping). Otherwise, the
        animation will restart after the final delay time.
        """

        super(Animation, self).__init__(style='image_placement')

        self.images = [ ]
        self.delays = [ ]

        for i, arg in enumerate(args):

            if i % 2 == 0:
                self.images.append(Image(arg))
            else:
                self.delays.append(arg)

        if len(self.images) > len(self.delays):
            self.delays.append(365.25 * 86400.0) # One year, give or take.
                
    def render(self, width, height, st):

        t = st % sum(self.delays)

        for image, delay in zip(self.images, self.delays):
            if t < delay:
                renpy.display.render.redraw(self, delay - t)

                im = render(image, width, height, st)
                width, height = im.get_size()
                rv = renpy.display.render.Render(width, height)
                rv.blit(im, (0, 0))

                return rv
            
            else:
                t = t - delay

    def predict(self, callback):
        for i in self.images:
            i.predict(callback)

    def get_placement(self):
        return renpy.game.style.image_placement

                
class ImageButton(renpy.display.behavior.Button):
    """
    Used to implement the guts of an image button.
    """

    def __init__(self, idle_image, hover_image,
                 style='image_button',
                 image_style='image_button_image',
                 clicked=None, hovered=None, **properties):

        self.idle_image = Image(idle_image, style=image_style)
        self.idle_image.style.set_prefix("idle_")
        self.hover_image = Image(hover_image, style=image_style)
        self.hover_image.style.set_prefix("hover_")

        super(ImageButton, self).__init__(self.idle_image,
                                          style=style,
                                          clicked=clicked,
                                          hovered=hovered,
                                          **properties)
        
    def predict(self, callback):
        self.idle_image.predict(callback)
        self.hover_image.predict(callback)

    def focus(self, default=False):
        self.child = self.hover_image
        super(ImageButton, self).focus(default=default)

    def unfocus(self):
        self.child = self.idle_image
        super(ImageButton, self).unfocus()

