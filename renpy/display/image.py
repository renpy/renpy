import renpy
import pygame
from pygame.constants import *

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

        # iw, ih = im.get_size()

        # surf = renpy.display.surface.Surface(iw, ih)
        # surf.blit(im, (0, 0))

        self.surface_map[fn] = im

        if renpy.config.debug_image_cache:
            print "Image cache:", self.surface_map.keys()

        return im
        
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
        try:
            self.load_image(fn)
        except:
            if renpy.config.debug:
                raise

cache = ImageCache()

class Image(renpy.display.core.Displayable):
    """
    Returns a Displayable that is an image that is loaded from a file
    on disk.
    """

    def __init__(self, filename, style='image_placement', **properties):
        """
        @param filename: The filename that the image is loaded from. Many common file formats are supported.
        """
        
        self.filename = filename
        self.style = renpy.style.Style(style, properties)

    def render(self, w, h, st):
        return cache.load_image(self.filename)  

    def get_placement(self):
        return self.style

    def predict(self, callback):
        callback(self.filename)

class UncachedImage(renpy.display.core.Displayable):
    """
    An image that is loaded immediately and not cached.
    """

    def __init__(self, file, hint=None, scale=None, style='image_placement',
                 **properties):
        self.surf = pygame.image.load(file, hint)

        if scale:
            self.surf = pygame.transform.scale(self.surf, scale)

        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def render(self, w, h, st):
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

    def __init__(self, name, style='image_placement', **properties):
        self.name = name
        self.style = renpy.style.Style(style, properties)

    def find_target(self):
        import renpy.exports as exports

        if self.name in exports.images:
            self.target = exports.images[self.name]
        else:
            self.target = renpy.display.text.Text("Image %s not found." % repr(self.name), color=(255, 0, 0, 255))
        
        
    def render(self, width, height, st):

        if not hasattr(self, 'target'):
            self.find_target()

        return self.target.render(width, height, st)

    def get_placement(self):
        return self.style
    
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

    def render(self, width, height, st):

        rv = renpy.display.surface.Surface(width, height)
        rv.fill(self.color)

        return rv
        
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

    nosave = [ 'cache' ]

    def __init__(self, filename, xborder, yborder):
        """
        @param filename: The file that the original image will be read from.

        @param xborder: The number of pixels in the x direction to use as
        a border.

        @param yborder: The number of pixels in the y direction to use as
        a border.

        For better performance, have the image file share a dimension
        length in common with the size the frame will be rendered
        at. We detect this and avoid scaling if possible.
        """

        self.filename = filename
        self.xborder = xborder
        self.yborder = yborder


    def render(self, width, height, st):


        if hasattr(self, 'cache'):
            if self.cache.get_size() == (width, height):
                return self.cache
            
        dest = renpy.display.surface.Surface(width, height)
        dw, dh = width, height

        source = cache.load_image(self.filename)
        sw, sh = source.get_size()

        def draw(x0, x1, y0, y1):

            # Quick exit.
            if x0 == x1 or y0 == y1:
                return

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

            # Compute sizes.
            srcsize = (sx1 - sx0, sy1 - sy0)
            dstsize = (dx1 - dx0, dy1 - dy0)

            # Get a subsurface.
            surf = source.subsurface((sx0, sy0, srcsize[0], srcsize[1]))

            # Scale if we have to.
            if dstsize != srcsize:
                surf = pygame.transform.scale(surf, dstsize)

            # Blit.
            dest.blit(surf, (dx0, dy0))

        xb = self.xborder
        yb = self.yborder

        # Top row.
        draw(0, xb, 0, yb)
        draw(xb, -xb, 0, yb)
        draw(-xb, 0, 0, yb)

        # Middle row.
        draw(0, xb, yb, -yb)
        draw(xb, -xb, yb, -yb)
        draw(-xb, 0, yb, -yb)

        # Bottom row.
        draw(0, xb, -yb, 0)
        draw(xb, -xb, -yb, 0)
        draw(-xb, 0, -yb, 0)
        
        # And, finish up.
        self.cache = dest
        return dest
        
class Animation(renpy.display.core.Displayable):
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

        self.images = [ ]
        self.delays = [ ]

        for i, arg in enumerate(args):

            if i % 2 == 0:
                self.images.append(arg)
            else:
                self.delays.append(arg)

        if len(self.images) > len(self.delays):
            self.delays.append(365.25 * 86400.0) # One year, give or take.
                
    def render(self, width, height, st):

        t = st % sum(self.delays)

        for image, delay in zip(self.images, self.delays):
            if t < delay:
                renpy.game.interface.redraw(delay - t)
                return cache.load_image(image)
            else:
                t = t - delay

    def predict(self, callback):
        for i in self.images:
            callback(i)

    def get_placement(self):
        return renpy.game.style.image_placement

class ImageMap(renpy.display.core.Displayable):
    """
    The displayable that implements renpy.imagemap.
    """


    def __init__(self, ground, selected, hotspots,
                 style='image_placement', **properties):

        self.ground = ground
        self.selected = selected
        self.hotspots = hotspots
        self.active = None

        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def predict(self, callback):
        callback(i.ground)
        callback(i.selected)

    def render(self, width, height, st):

        ground = cache.load_image(self.ground)
        selected = cache.load_image(self.selected)

        width, height = ground.get_size()
        rv = renpy.display.surface.Surface(width, height)
        rv.blit(ground, (0, 0))

        if self.active is not None:
            x0, y0, x1, y1, result = self.hotspots[self.active]

            subsurface = selected.subsurface((x0, y0, x1-x0, y1-y0))
            rv.blit(subsurface, (x0, y0))

        return rv
        
    def event(self, ev, x, y):

        old_active = self.active
        active = None

        for i, (x0, y0, x1, y1, result) in enumerate(self.hotspots):
            if x >= x0 and x <= x1 and y >= y0 and y <= y1:
                active = i
                break

        # result stays set.

        if old_active != active:
            self.active = active
            renpy.game.interface.redraw(0)

        if active is None:
            return None

        if (ev.type == MOUSEBUTTONDOWN and ev.button == 1) or \
           (ev.type == KEYDOWN and ev.key == K_RETURN):

            return result

        return None
                
            
        
