import renpy
from renpy.display.render import render

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

    def really_load_image(self, fn):
        """
        This is called by load_image, and does the actual loading of
        images. This may be a load of an image, or perhaps the
        compositing of images if fn is a tuple.
        """

        # If fn is not a single filename but a tuple, we composite the
        # elements of the tuple.
        if isinstance(fn, tuple):
            if not tuple:
                raise Exception("Trying to create a composite image from an empty tuple.")

            base = self.load_image(fn[0])

            rv = pygame.Surface(base.get_size(), 0,
                                renpy.game.interface.display.sample_surface)

            rv.blit(base, (0, 0))

            for i in fn[1:]:
                layer = self.load_image(i)
                rv.blit(layer, (0, 0))

            renpy.display.render.mutated_surface(rv)

            return rv

        im = pygame.image.load(renpy.loader.load(fn), fn)

        if im.get_flags() & SRCALPHA:
            im = im.convert_alpha()
        else:
            im = im.convert()

        renpy.display.render.mutated_surface(im)
            
        return im
            
        
    # Forces an image load, regardless of if the cache is full or not.
    def load_image(self, fn):
        self.time_map[fn] = self.time

        if fn in self.surface_map:
            return self.surface_map[fn]

        if fn in self.preloads:
            self.preloads.remove(fn)

        # iw, ih = im.get_size()

        # surf = renpy.display.render.Render(iw, ih)
        # surf.blit(im, (0, 0))

        im = self.really_load_image(fn)

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
        @param filename: The filename that the image is loaded
        from. Many common file formats are supported.

        If the filename is not a single string but instead a tuple of
        strings, the image is considered to be"layered". In this case,
        the image will be the size of the first image in the tuple, and
        other images will be aligned with the upper-left corner of the
        image.
        """

        super(Image, self).__init__()
        
        self.filename = filename
        self.style = renpy.style.Style(style, properties)

    def render(self, w, h, st):
        im = cache.load_image(self.filename)
        w, h = im.get_size()
        rv = renpy.display.render.Render(w, h)
        rv.blit(im, (0, 0))
        return rv

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
            self.target = renpy.display.text.Text(msg,
                                                  color=(255, 0, 0, 255))

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
        @param color: An RGBA tuple, giving the color that the display will be filled with.
        """
        
        super(Solid, self).__init__()
        self.color = color

    def render(self, width, height, st):

        rv = renpy.display.render.Render(width, height)
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

        super(Frame, self).__init__()

        self.filename = filename
        self.xborder = xborder
        self.yborder = yborder


    def render(self, width, height, st):
            
        dest = renpy.display.render.Render(width, height)
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
        return dest

    def predict(self, callback):
        callback(self.filename)
        
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

        super(Animation, self).__init__()

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
                renpy.display.render.redraw(self, delay - t)

                im = cache.load_image(image)
                width, height = im.get_size()
                rv = renpy.display.render.Render(width, height)
                rv.blit(im, (0, 0))

                return rv
            
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


    def __init__(self, ground, selected, hotspots, unselected=None,
                 style='imagemap', **properties):

        super(ImageMap, self).__init__()

        self.ground = ground
        self.selected = selected
        self.hotspots = hotspots

        if not unselected:
            self.unselected = self.ground
        else:
            self.unselected = unselected

        self.active = None

        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    # This doesn't do anything quite yet.
    def predict(self, callback):
        callback(self.ground)
        callback(self.selected)
        callback(self.unselected)

    def render(self, width, height, st):

        ground = cache.load_image(self.ground)
        selected = cache.load_image(self.selected)
        unselected = cache.load_image(self.unselected)

        width, height = ground.get_size()
        rv = renpy.display.render.Render(width, height)
        rv.blit(ground, (0, 0))

        for i, hotspot in enumerate(self.hotspots):

            x0, y0, x1, y1, result = hotspot

            if i == self.active:
                source = selected
            else:
                source = unselected

            subsurface = source.subsurface((x0, y0, x1-x0, y1-y0))
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
            renpy.display.render.redraw(self, 0)

            if active is not None:
                renpy.display.audio.play(self.style.hover_sound)


        if active is None:
            return None

        if renpy.display.behavior.map_event(ev, "imagemap_select"):
            renpy.display.audio.play(self.style.activate_sound)
            return result

        return None
                
class ImageButton(renpy.display.behavior.Button):

    def __init__(self, idle_image, hover_image, style='image_button',
                 image_style='image_button_image',
                 clicked=None, hovered=None):

        self.idle_image = Image(idle_image, style=image_style)
        self.idle_image.style.set_prefix("idle_")
        self.hover_image = Image(hover_image, style=image_style)
        self.hover_image.style.set_prefix("hover_")

        super(ImageButton, self).__init__(self.idle_image,
                                          style=style,
                                          clicked=clicked,
                                          hovered=hovered)


    def predict(self, callback):
        self.idle_image.predict(callback)
        self.hover_image.predict(callback)

    def set_hover(self, hover):
        super(ImageButton, self).set_hover(hover)

        if hover:
            self.child = self.hover_image
        else:
            self.child = self.idle_image

