import renpy.display.core
import renpy.game as game
import renpy.loader as loader
import renpy.exports as exports
import renpy.display.text as text
import renpy.display.surface

import pygame
from pygame.constants import *
import pygame.image

_image_cache = { }

def load_image(filename):
    if filename in _image_cache:
        return _image_cache[filename]

    im = pygame.image.load(loader.load(filename), filename)
    hwim = renpy.display.surface.surface(im.get_size(), SRCALPHA, 32)
    hwim.blit(im, (0, 0))
    

    _image_cache[filename] = hwim

    return hwim

class Image(renpy.display.core.Displayable):
    """
    This is an image that we want to display to the user.

    @ivar filename: The filename that this image should be loaded
    from.
    """

    def __init__(self, fn):
        self.filename = fn

    def render(self, w, h, st, tt):
        return load_image(self.filename)  

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
        self.name = name

    def find_target(self):
        if self.name in exports.images:
            self.target = exports.images[self.name]
        else:
            self.target = text.Text("Image %s not found." % repr(self.name), color=(255, 0, 0, 255))
        
        
    def render(self, width, height, st, tt):

        if not hasattr(self, 'target'):
            self.find_target()

        return self.target.render(width, height, st, tt)

class Solid(renpy.display.core.Displayable):
    """
    A class that fills the area allocated to it with a solid color.
    """


    def __init__(self, color):
        self.color = color

    def render(self, width, height, st, tt):

        rv = renpy.display.surface.surface((width, height), SRCALPHA, 32)
        rv.fill(self.color)

        return rv
        
