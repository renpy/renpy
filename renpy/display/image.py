import renpy
import pygame

_image_cache = { }

def load_image(filename):
    if filename in _image_cache:
        return _image_cache[filename]

    im = pygame.image.load(renpy.loader.load(filename), filename)
    im = im.convert_alpha()

    _image_cache[filename] = im

    return im

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

    def get_placement(self):
        return renpy.game.style.image_placement

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
        import renpy.exports as exports

        if self.name in exports.images:
            self.target = exports.images[self.name]
        else:
            self.target = renpy.display.text.Text("Image %s not found." % repr(self.name), color=(255, 0, 0, 255))
        
        
    def render(self, width, height, st, tt):

        if not hasattr(self, 'target'):
            self.find_target()

        return self.target.render(width, height, st, tt)

    def get_placement(self):
        return self.target.get_placement()
    

class Solid(renpy.display.core.Displayable):
    """
    A class that fills the area allocated to it with a solid color.
    """

    def __init__(self, color):
        self.color = color

    def render(self, width, height, st, tt):

        rv = renpy.display.surface.Surface(width, height)
        rv.fill(self.color)

        return rv
        
