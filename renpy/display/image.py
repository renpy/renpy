import renpy
import pygame

class ImageCache(object):

    def __init__(self):

        # A monotonically increasing time.
        self.time = 0

        # A map from image filename to surface.
        self.surface_map = { }

        # A map from image filename to last access time.
        self.time_map = { }

        # The list of things we want to preload.
        self.preloads = [ ]
        

    def tick(self):
        self.time += 1
        self.preloads = [ ]
        
    # Forces an image load, regardless of if the cache is full or not.
    def load_image(self, fn):
        self.time_map[fn] = self.time

        if fn in self.surface_map:
            return self.surface_map[fn]

        if fn in self.preloads:
            self.preloads.remove(fn)

        im = pygame.image.load(renpy.loader.load(fn), fn)
        im = im.convert_alpha()

        iw, ih = im.get_size()

        surf = renpy.display.surface.Surface(iw, ih)
        surf.blit(im, (0, 0))

        self.surface_map[fn] = surf

        if renpy.config.debug_image_cache:
            print "Image cache:", self.surface_map.keys()

        return surf
        
    # Queues an image to be preloaded if not already loaded and there's
    # room in the cache for it.
    def preload_image(self, fn):
        self.time_map[fn] = self.time

        if fn in self.surface_map:
            return

        if fn not in self.preloads:
            self.preloads.append(fn)


    # This tries to ensure that there are n empty spaces in the image
    # cache. Returns the number of empty spaces that are actually in
    # the image cache. (A number that may be negative.)
    def clear_image_cache(self, n):

        rv = renpy.config.image_cache_size - len(self.surface_map)

        if rv >= n:
            return rv
        
        # The number of images to remove. (This is the amount we are over
        # the cache limit + the number of images we have been requested to
        # pull.)
        num_to_remove = len(self.surface_map) - renpy.config.image_cache_size + n

        time_files = [ (self.time_map[fn], fn) for fn in self.surface_map ]
        time_files = [ (time, fn) for time, fn in time_files if time != self.time ]
        time_files.sort()
        time_files = time_files[:num_to_remove]

        for time, fn in time_files:
            del self.surface_map[fn]
            del self.time_map[fn]

        if renpy.config.debug_image_cache:
            print "Image cache:", self.surface_map.keys()

        rv = renpy.config.image_cache_size - len(self.surface_map)

        return rv

    def needs_preload(self):
        """
        Returns True if calling preload would do anything.
        """

        return self.preloads and True

    def preload(self):

        # If we have nothing to preload, bail early.
        if not self.preloads:
            return

        # Try to clear up enough space for the preloads.
        avail = self.clear_image_cache(len(self.preloads))

        if avail < 0:
            avail = 0
    
        self.preloads = self.preloads[:avail]

        # If no space is available, bail here.
        if not self.preloads:
            return

        # Get the first thing to preload.
        fn = self.preloads[0]

        # Actually load the image.
        self.load_image(fn)

cache = ImageCache()

class Image(renpy.display.core.Displayable):
    """
    Returns a Displayable that is an image that is loaded from a file
    on disk.
    """

    def __init__(self, filename):
        """
        @param filename: The filename that the image is loaded from. Many common file formats are supported.
        """
        
        self.filename = filename

    def render(self, w, h, st, tt):
        return cache.load_image(self.filename)  

    def get_placement(self):
        return renpy.game.style.image_placement

    def predict(self, callback):
        callback(self.filename)

class UncachedImage(renpy.display.core.Displayable):
    """
    An image that is loaded immediately and not cached.
    """

    def __init__(self, file, hint=None, scale=None):
        self.surf = pygame.image.load(file, hint)

        if scale:
            self.surf = pygame.transform.scale(self.surf, scale)

    def get_placement(self):
        return renpy.game.style.image_placement

    def render(self, w, h, st, tt):
        sw, sh = self.surf.get_size()
        rv = renpy.display.surface.Surface(sw, sh)
        rv.blit(self.surf, (0, 0))

        return rv

    # Should never be called, but what the hey?
    def predict(self, callback):
        callback(self.filename)

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
    Returns a Displayable that is solid, and filled with a single
    color. A Solid expands to fill all the space allocated to it,
    making it suitable for use as a background.
    """

    def __init__(self, color):
        """
        @param color: An RGBA tuple, giving the color that the display will be filled with.
        """
        
        self.color = color

    def render(self, width, height, st, tt):

        rv = renpy.display.surface.Surface(width, height)
        rv.fill(self.color)

        return rv
        

# class Scale(renpy.display.core.Displayable):
#     """
#     Scales the child down to the specified size.
#     """

#     def __init__(self, child, width, height):
#         self.child = child
#         self.width = width
#         self.height = height

#     def get_placement(self):
#         return self.child.get_placement()

#     def render(self, w, h, st, tt):

#         surf = self.child.render(w, h, st, tt)

#         scaled = pygame.transform.scale(surf.pygame_surface(),
#                                         (self.width, self.height))

#         rv = renpy.display.surface.Surface(self.width, self.height)
#         rv.blit(scaled, (0, 0))

#         return rv
        
        
        
    
