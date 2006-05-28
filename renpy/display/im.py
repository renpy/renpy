# This file contains the new image code, which includes provisions for
# size-based caching and constructing images from operations (like
# cropping and scaling).

import renpy

import pygame
from pygame.constants import *

# This is an entry in the image cache.
class CacheEntry(object):

    def __init__(self, what, surf):

        # The object that is being cached (which needs to be
        # hashable and comparable).
        self.what = what

        # The pygame surface corresponding to the cached object.
        self.surf = surf 

        # The size of this image.
        w, h = surf.get_size()
        self.size = w * h

        # The time when this cache entry was last used.
        self.time = 0

# This is the singleton image cache.
class Cache(object):

    def __init__(self):

        # The current arbitrary time. (Increments by one for each
        # interaction.)
        self.time = 0

        # A map from Image object to CacheEntry.
        self.cache = { }

        # A list of Image objects that we want to preload.
        self.preloads = [ ]

        # False if this is not the first preload in this tick.
        self.first_preload_in_tick = True

        # The total size of the current generation of images.
        self.size_of_current_generation = 0

        # The total size of everything in the cache.
        self.total_cache_size = 0

    # Returns the maximum size of the cache, after which we start
    # tossing things out.
    def cache_limit(self):
        return renpy.config.image_cache_size * renpy.config.screen_width * renpy.config.screen_height

    # Increments time, and clears the list of images to be
    # preloaded.
    def tick(self):
        self.time += 1
        self.preloads = [ ]
        self.first_preload_in_tick = True
        self.size_of_current_generation = 0

        if renpy.config.debug_image_cache:
            print "IC ----"

    # Called to report that a given image would like to be preloaded.
    def preload_image(self, image):
        if renpy.config.debug_image_cache:
            print "IC Request Preload", image

        if not isinstance(image, ImageBase):
            if renpy.config.debug_image_cache:
                print "IC Can't preload non image: ", image
            else:
                return

            
        self.preloads.append(image)

    # Do we need to preload an image?
    def needs_preload(self):
        return (self.preloads and True) or self.first_preload_in_tick

    # This returns the pygame surface corresponding to the provided
    # image. It also takes care of updating the age of images in the
    # cache to be current, and maintaining the size of the current
    # generation of images.
    def get(self, image):

        if not isinstance(image, ImageBase):
            raise Exception("Expected an image of some sort, but got" + str(image) + ".")
            

        if image in self.cache:
            ce = self.cache[image]

            if ce.time == self.time:
                return ce.surf
        else:
            ce = CacheEntry(image, image.load())
            self.total_cache_size += ce.size
            self.cache[image] = ce

            # Indicate that this surface had changed.
            renpy.display.render.mutated_surface(ce.surf)

            if renpy.config.debug_image_cache:
                print "IC Added", ce.what


        # Move it into the current generation.
        ce.time = self.time
        self.size_of_current_generation += ce.size

        return ce.surf

    # This kills off a given cache entry.
    def kill(self, ce):

        # Should never happen... but...
        if ce.time == self.time:
            self.size_of_current_generation -= ce.size

        self.total_cache_size -= ce.size
        del self.cache[ce.what]

        if renpy.config.debug_image_cache:
            print "IC Removed", ce.what

    # Calling this cleans out the image cache if it has gotten too large.
    def cleanout(self):
        cache_limit = self.cache_limit()

        # If we're within the limit, return.
        if self.total_cache_size <= cache_limit:
            return

        # If we're outside the cache limit, we need to go and start
        # killing off some of the entries until we're back inside it.
        
        # A list of time, cache_entry pairs.
        ace = [ (ce.time, ce) for ce in self.cache.itervalues() ]
        ace.sort()

        while ace and self.total_cache_size > cache_limit:

            time, ce = ace.pop(0)
        
            if time == self.time:
                # If we're bigger than the limit, and there's nothing
                # to remove, we should stop the preloading right away.

                self.preloads = [ ]
                break


            # Otherwise, kill off the given cache entry.
            self.kill(ce)

        if renpy.config.debug_image_cache:
            print "IC is:", self.cache.keys()
            print "IC size:", self.total_cache_size, "/", cache_limit


    # This actually performs preloading.
    def preload(self):

        if self.first_preload_in_tick:
            self.first_preload_in_tick = False

            # Triage into stuff that's already in the cache and should
            # be kept there, and stuff that isn't there already.

            new_preloads = [ ]

            for i in self.preloads:
                if i in self.cache:
                    self.get(i)
                else:
                    new_preloads.append(i)

            self.preloads = new_preloads

            # Clean out the cache.
            self.cleanout()

            # Return after doing said triage.
            return

        # Otherwise, new_preloads contains things that aren't in the
        # cache already. So load one of them into the cache, maybe.

        cache_limit = self.cache_limit()

        # If the size of the current generation is bigger than the
        # total cache size, stop preloading.
        if self.size_of_current_generation > cache_limit:
            self.preloads = [ ]
            return

        # Otherwise, preload the next image.
        image = self.preloads.pop(0)
        self.get(image)

        # And, we're done.
        self.cleanout()
        
cache = Cache()


class ImageBase(renpy.display.core.Displayable):
    """
    This is the base class for all of the various kinds of images that
    we can possibly have.
    """

    def __init__(self, *args, **properties):

        properties.setdefault('style', 'image')

        super(ImageBase, self).__init__(**properties)
        self.identity = (type(self).__name__, ) + args


    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other):

        if not isinstance(other, ImageBase):
            return False
        
        return self.identity == other.identity

    def __repr__(self):
        return "<" + " ".join([repr(i) for i in self.identity]) + ">"
        
    def load(self):
        """
        This function is called by the image cache code to cause this
        image to be loaded. It's expected that children of this class
        would override this.
        """

        assert False
        
    def render(self, w, h, st, at):
        im = cache.get(self)
        w, h = im.get_size()
        rv = renpy.display.render.Render(w, h)
        rv.blit(im, (0, 0))
        return rv

    def predict_one(self, callback):
        callback(self)

    def predict_files(self):
        """
        Returns a list of files that will be accessed when this image
        operation is performed.
        """

        return [ ]

class Image(ImageBase):
    """
    This image manipulator loads an image from a file.
    """

    def __init__(self, filename, **properties):
        """
        @param filename: The filename that the image will be loaded from.
        """

        super(Image, self).__init__(filename, **properties)
        self.filename = filename

    def load(self):
        im = pygame.image.load(renpy.loader.load(self.filename), self.filename)

        if im.get_masks()[3]:
            im = im.convert_alpha()
            im.set_alpha(255, pygame.RLEACCEL)
            im.lock()
            im.unlock()
        else:
            im = im.convert()   

        return im

    def predict_files(self):
        return [ self.filename ]

class Composite(ImageBase):
    """
    This image manipulator composites one or more images together.
    """

    def __init__(self, size, *args, **properties):
        """
        This takes a variable number of arguments. The first argument
        is size, which is either the desired size of the image (in
        pixels), or None to indicate that the size should be the size of
        the first image.

        It then takes an even number of further arguments. (For an odd
        number of total arguments.) The second and other even numbered
        arguments contain position tuples, while the third and further
        odd-numbered arguments give images (or image
        manipulators). A position argument gives the position of the
        image immediately following it, with the position expressed as
        a tuple giving an offset from the upper-left corner of the
        image.  The images are composited in bottom-to-top order, with
        the last image being closest to the user.
        """

        super(Composite, self).__init__(size, *args, **properties)

        if len(args) % 2 != 0:
            raise Exception("Composite requires an odd number of arguments.")

        self.size = size
        self.positions = args[0::2]
        self.images = [ image(i) for i in args[1::2] ]

    def load(self):

        if self.size:
            size = self.size
        else:
            size = cache.get(self.images[0]).get_size()

        rv = pygame.Surface(size, 0,
                            renpy.game.interface.display.sample_surface)

        for pos, im in zip(self.positions, self.images):
            rv.blit(cache.get(im), pos)

        return rv

    def predict_files(self):

        rv = [ ]

        for i in self.images:
            rv.extend(i.predict_files())

        return rv

class FrameImage(ImageBase):
    """
    This is an image that implements a frame with a given size. Instances
    of this are used by the frame object to return a new frame when
    such a new frame is needed.
    """

    def __init__(self, im, xborder, yborder, width, height):
        """
        @param image: The image that will be used as the base of this
        frame.

        @param xborder: The number of pixels in the x direction to use as
        a border.

        @param yborder: The number of pixels in the y direction to use as
        a border.

        @param width: The width we are being rendered at.

        @param height: The height we are being rendered at.
        """

        im = image(im)

        super(FrameImage, self).__init__(im, xborder, yborder, width, height)

        self.image = im
        self.xborder = xborder
        self.yborder = yborder
        self.width = int(width)
        self.height = int(height)

    def load(self):

        dw = self.width
        dh = self.height

        dest = pygame.Surface((dw, dh), 0,
                              renpy.game.interface.display.sample_surface)
        
        source = cache.get(self.image)
        sw, sh = source.get_size()

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

class SolidImage(ImageBase):
    """
    This is an image that is a solid rectangle with a given size. It's
    used to implement Solid.
    """

    def __init__(self, color, width, height):
        super(SolidImage, self).__init__(color, width, height)
        self.color = color
        self.width = width
        self.height = height

    def load(self):
        
        rv = pygame.Surface((self.width, self.height), 0,
                            renpy.game.interface.display.sample_surface)
        rv.fill(self.color)

        return rv

class Scale(ImageBase):
    """
    This is an image manipulator that scales another image manipulator
    to the specified width and height. This scalling is unfiltered, so
    you can expect your image to look a bit jagged.
    """

    def __init__(self, im, width, height, **properties):

        im = image(im)
        super(Scale, self).__init__(im, width, height, **properties)

        self.image = im
        self.width = width
        self.height = height

    def load(self):
        return pygame.transform.scale(cache.get(self.image),
                                      (self.width, self.height))

    def predict_files(self):
        return self.image.predict_files()


class Flip(ImageBase):
    """
    This is an image manipulator that can flip the image horizontally or vertically.
    """

    def __init__(self, im, horizontal=False, vertical=False, **properties):
        """
        @param im: The image to be rotozoomed.

        @param horizontal: True to flip the image horizontally.

        @param vertical: True to flip the image vertically.
        """

        if not (horizontal or vertical):
            raise Exception("im.Flip must be called with a true value for horizontal or vertical.")

        im = image(im)
        super(Flip, self).__init__(im, horizontal, vertical, **properties)

    

        self.image = im
        self.horizontal = horizontal
        self.vertical = vertical

    def load(self):

        

        rv = pygame.transform.flip(cache.get(self.image),
                                   self.horizontal, self.vertical)
        return rv

    def predict_files(self):
        return self.image.predict_files()

    
    

class Rotozoom(ImageBase):
    """
    This is an image manipulator that is a smooth rotation and zoom of another image manipulator.
    """

    def __init__(self, im, angle, zoom, **properties):
        """
        @param im: The image to be rotozoomed.

        @param angle: The number of degrees counterclockwise the image is
        to be rotated.

        @param zoom: The zoom factor. Numbers that are greater than 1.0
        lead to the image becoming larger.
        """

        im = image(im)
        super(Rotozoom, self).__init__(im, angle, zoom, **properties)

        self.image = im
        self.angle = angle
        self.zoom = zoom

    def load(self):

        rv = pygame.transform.rotozoom(cache.get(self.image),
                                       self.angle, self.zoom)
        return rv

    def predict_files(self):
        return self.image.predict_files()

        
        
class Crop(ImageBase):
    """
    This crops the image that is its child.
    """

    def __init__(self, im, x, y, w, h, **properties):

        im = image(im)

        super(Crop, self).__init__(im, x, y, w, h, **properties)

        self.image = im
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def load(self):
        return cache.get(self.image).subsurface((self.x, self.y,
                                                 self.w, self.h))

    def predict_files(self):
        return self.image.predict_files()



def ramp(start, end):
    """
    Returns a 256 character linear ramp, where the first character has
    the value start and the last character has the value end. Such a
    ramp can be used as a map argument of im.Map.
    """

    chars = [ ]

    for i in range(0, 256):
        i = i / 255.0
        chars.append(chr(int( end * i + start * (1.0 - i) ) ) )

    return "".join(chars)


identity = ramp(0, 255)

class Map(ImageBase):
    """
    This adjusts the colors of the image that is its child. It takes
    as arguments 4 256 character strings. If a pixel channel has a
    value of 192, then the value of the 192nd character in the string
    is used for the mapped pixel component.
    """

    def __init__(self, im, rmap=identity, gmap=identity, bmap=identity,
                 amap=identity, force_alpha=False, **properties):

        im = image(im)

        super(Map, self).__init__(im, rmap, gmap, bmap, amap, force_alpha, **properties)
        
        self.image = im
        self.rmap = rmap
        self.gmap = gmap
        self.bmap = bmap
        self.amap = amap

        self.force_alpha = force_alpha

    def load(self):

        surf = cache.get(self.image)

        if not renpy.display.module.can_map:
            return surf

        if self.force_alpha and not (surf.get_masks()[3]):
            surf = surf.convert_alpha()

        rv = pygame.Surface(surf.get_size(), surf.get_flags(), surf)

        renpy.display.module.map(surf, rv,
                                 self.rmap, self.gmap, self.bmap, self.amap)

        return rv

    def predict_files(self):
        return self.image.predict_files()

class Recolor(ImageBase):
    """
    This adjusts the colors of the image that is its child. It takes as an
    argument 4 numbers between 0 and 255, and maps each channel of the image
    linearly between 0 and the supplied color.
    """

    def __init__(self, im, rmul=identity, gmul=identity, bmul=identity,
                 amul=identity, force_alpha=False, **properties):

        im = image(im)

        super(Recolor, self).__init__(im, rmul, gmul, bmul, amul, force_alpha, **properties)
        
        self.image = im
        self.rmul = rmul + 1
        self.gmul = gmul + 1
        self.bmul = bmul + 1
        self.amul = amul + 1

        self.force_alpha = force_alpha

    def load(self):

        surf = cache.get(self.image)

        if not renpy.display.module.can_linmap:
            return surf

        if self.force_alpha and not (surf.get_masks()[3]):
            surf = surf.convert_alpha()

        rv = pygame.Surface(surf.get_size(), surf.get_flags(), surf)

        renpy.display.module.linmap(surf, rv,
                                    self.rmul, self.gmul, self.bmul, self.amul)

        return rv

    def predict_files(self):
        return self.image.predict_files()

def Alpha(image, alpha, **properties):
    """
    Returns an alpha-mapped version of the image. Alpha is the maximum
    alpha that this image can have, a number between 0.0 (fully
    transparent) and 1.0 (opaque).

    If an image already has an alpha channel, values in that alpha
    channel are reduced as appropriate.
    """

    return Recolor(image, 255, 255, 255, int(255 * alpha), force_alpha=True, **properties)

class Tile(ImageBase):
    """
    This tiles the image, repeating it vertically and horizontally
    until it is as large as the specified size. If no size is given,
    then the size defaults to the size of the screen.
    """

    def __init__(self, im, size=None, **properties):

        im = image(im)

        super(Tile, self).__init__(im, size, **properties)
        self.image = im
        self.size = size

    def load(self):

        size = self.size

        if size is None:
            size = (renpy.config.screen_width, renpy.config.screen_height)

        surf = cache.get(self.image)

        width, height = size
        sw, sh = surf.get_size()

        rv = pygame.Surface(size, 0,
                            renpy.game.interface.display.sample_surface)

        for y in range(0, height, sh):
            for x in range(0, width, sw):
                rv.blit(surf, (x, y))

        return rv

    def predict_files(self):
        return self.image.predict_files()
    

def image(arg, loose=False, **properties):
    """
    This takes as input one of a number of ways of specifying an
    image, and returns the Displayable image object that has been so
    specified. Specifically, this can take as input:

    <ul>
    <li> An image object. In that case, it's returned unchanged.</li>
    <li> A string. If a string is given, then the string is interpreted
    as a filename, and what is returned is an im.Image object, which
    loads the image from disk.</li>
    <li> A tuple. If this is the case, then what is returned is an
    im.Composite object, which aligns the upper-left corner of all
    of the images supplied as arguments. </li>
    </ul>

    If the loose argument is False, then this will report an error if an
    arbitrary argument is given. If it's True, then the argument is passed
    through unchanged.
    """

    if isinstance(arg, ImageBase):
        return arg

    elif isinstance(arg, basestring):
        return Image(arg, **properties)

    elif isinstance(arg, tuple):
        params = [ ]

        for i in arg:
            params.append((0, 0))
            params.append(i)

        return Composite(None, *params)

    if loose:
        return arg

    if isinstance(arg, renpy.display.core.Displayable):
        raise Exception("Expected an image, but got a general displayable.")
    else:
        raise Exception("Could not construct image from argument.")
    
def load_image(fn):
    """
    This loads an image from the given filename, using the cache.
    """

    return cache.get(image(fn))
