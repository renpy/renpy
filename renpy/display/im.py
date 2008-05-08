# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# This file contains the new image code, which includes provisions for
# size-based caching and constructing images from operations (like
# cropping and scaling).

import renpy
import random
import math
import zipfile
import cStringIO

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

        if not image.cache:
            surf = image.load()
            renpy.display.render.mutated_surface(surf)
            return surf
            

        if image in self.cache:
            ce = self.cache[image]
            new = False

            
        else:

            ce = CacheEntry(image, image.load())
            self.total_cache_size += ce.size
            self.cache[image] = ce

            # Indicate that this surface had changed.
            renpy.display.render.mutated_surface(ce.surf)

            if renpy.config.debug_image_cache:
                print "IC Added %r (%.02f%%)" % (ce.what, 100.0 * self.total_cache_size / self.cache_limit())

            new = True


        # Move it into the current generation.
        if ce.time != self.time:
            ce.time = self.time
            self.size_of_current_generation += ce.size

        # RLE detection. (ce.size is used to check that we're not
        # 0 pixels big.)
        if new and id(ce.surf) not in rle_cache and ce.size:
            rle = image.rle
            surf = ce.surf

            # If we don't know if the image is RLE or not, guess.
            # Only do so if the image has an alpha channel.
            if rle is None and surf.get_masks()[3]:
                sw, sh = surf.get_size()

                for i in range(0, 10):
                    if surf.get_at((random.randint(0, sw-1),
                                    random.randint(0, sh-1)))[3] == 0:
                        rle = True
                        break

            if rle:
                rle_surf = ce.surf.convert_alpha()
                rle_surf.set_alpha(255, RLEACCEL)
                rle_cache[id(ce.surf)] = rle_surf
                renpy.display.render.mutated_surface(ce.surf)
                if renpy.config.debug_image_cache:
                    print "Added to rle cache:", image


        # Done... return the surface.
        return ce.surf

    # This kills off a given cache entry.
    def kill(self, ce):

        # Should never happen... but...
        if ce.time == self.time:
            self.size_of_current_generation -= ce.size

        self.total_cache_size -= ce.size
        del self.cache[ce.what]

        if id(ce.surf) in rle_cache:
            del rle_cache[id(ce.surf)]

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

# A map from id(cached surface) to rle version of cached surface.
rle_cache = { }

def free_memory():
    """
    Frees some memory.
    """

    global cache
    cache = Cache()
    rle_cache.clear()


class ImageBase(renpy.display.core.Displayable):
    """
    This is the base class for all of the various kinds of images that
    we can possibly have.
    """

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.cache = True
    
    def __init__(self, *args, **properties):

        self.rle = properties.pop('rle', None)
        self.cache = properties.pop('cache', True)
            
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

    def load(self, unscaled=False):
        try:

            if unscaled:
                surf = renpy.display.scale.image_load_unscaled(renpy.loader.load(self.filename), self.filename)
            else:
                surf = pygame.image.load(renpy.loader.load(self.filename), self.filename)

            if surf.get_masks()[3] or surf.get_colorkey():
                surf = surf.convert_alpha()
            else:
                surf = surf.convert()   

            return surf

        except Exception, e:

            if renpy.config.missing_image_callback:
                im = renpy.config.missing_image_callback(self.filename)
                if im is None:
                    raise e

                return im.load()

            raise
        
    def predict_files(self):

        if renpy.loader.loadable(self.filename):
            return [ self.filename ]
        else:
            if renpy.config.missing_image_callback:
                im = renpy.config.missing_image_callback(self.filename)
                if im is not None:
                    return im.predict_files()

            return [ ]

class ZipFileImage(ImageBase):

    def __init__(self, zipfilename, filename, mtime=0, **properties):
        super(ZipFileImage, self).__init__(zipfilename, filename, mtime, **properties)

        self.zipfilename = zipfilename
        self.filename = filename

    def load(self):
        zf = zipfile.ZipFile(self.zipfilename, 'r')
        sio = cStringIO.StringIO(zf.read(self.filename))
        rv = pygame.image.load(sio, self.filename)
        zf.close()

        return rv

    def predict_files(self):
        return [ ]
        
    
        
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

    def __init__(self, im, xborder, yborder, width, height, tile, bilinear):
        """
        @param image: The image that will be used as the base of this
        frame.

        @param xborder: The number of pixels in the x direction to use as
        a border.

        @param yborder: The number of pixels in the y direction to use as
        a border.

        @param width: The width we are being rendered at.

        @param height: The height we are being rendered at.

        @param tile: Should we tile? If False, we scale.
        """

        im = image(im)

        super(FrameImage, self).__init__(im, xborder, yborder, width, height, tile, bilinear)

        self.image = im
        self.xborder = xborder
        self.yborder = yborder
        self.width = int(width)
        self.height = int(height)
        self.tile = tile
        self.bilinear = bilinear
        
        if self.width < self.xborder * 2:
            # raise Exception("Frame width is too small for its border.")
            self.xborder = self.width / 2
            
        if self.height < self.yborder * 2:
            # raise Exception("Frame height is too small for its border.")
            self.yborder = self.height / 2
            

    def load(self):

        dw = self.width
        dh = self.height

        dest = pygame.Surface((dw, dh), 0,
                              renpy.game.interface.display.sample_surface)
        
        rv = dest

        source = cache.get(self.image)

        dest = renpy.display.scale.real(dest)
        source = renpy.display.scale.real(source)
        
        xb = renpy.display.scale.scale(self.xborder)
        yb = renpy.display.scale.scale(self.yborder)
        
        sw, sh = source.get_size()
        dw, dh = dest.get_size()
    

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

            # Scale or tile if we have to.
            if dstsize != srcsize:
                if self.tile:
                    tilew, tileh = srcsize
                    dstw, dsth = dstsize

                    surf2 = pygame.Surface(dstsize, 0, surf)

                    for y in range(0, dsth, tileh):
                        for x in range(0, dstw, tilew):
                            surf2.blit(surf, (x, y))


                    surf = surf2 

                else:
                    if self.bilinear and renpy.display.module.can_bilinear_scale:
                        surf2 = renpy.display.scale.real_bilinear(surf, dstsize)
                    else:
                        surf2 = renpy.display.scale.real_transform_scale(surf, dstsize)

                    surf = surf2
                        
            # Blit.
            dest.blit(surf, (dx0, dy0))

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
        return rv

class SolidImage(ImageBase):
    """
    This is an image that is a solid rectangle with a given size. It's
    used to implement Solid.
    """

    def __init__(self, color, width, height):
        super(SolidImage, self).__init__(color, width, height)
        self.color = color
        self.width = int(width)
        self.height = int(height)

    def load(self):

        if self.color[3] != 255:
            sample = renpy.game.interface.display.sample_surface
        else:
            sample = renpy.game.interface.display.window
        
        rv = pygame.Surface((self.width, self.height), 0,
                            sample)
        rv.fill(self.color)

        return rv  

class Scale(ImageBase):
    """
    This is an image manipulator that scales another image manipulator
    to the specified width and height.
    """

    def __init__(self, im, width, height, bilinear=True, **properties):

        bilinear = bilinear and renpy.display.module.can_bilinear_scale

        im = image(im)
        super(Scale, self).__init__(im, width, height, bilinear, **properties)

        self.image = im
        self.width = width
        self.height = height
        self.bilinear = bilinear

    def load(self):

        if self.bilinear:
            surf = cache.get(self.image)
            rv = pygame.Surface((self.width, self.height), 0, surf)
            renpy.display.module.bilinear_scale(surf, rv)
            return rv

        else:
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


ramp_cache = { }


def ramp(start, end):
    """
    Returns a 256 character linear ramp, where the first character has
    the value start and the last character has the value end. Such a
    ramp can be used as a map argument of im.Map.
    """

    rv = ramp_cache.get((start, end), None)
    if rv is None:

        chars = [ ]

        for i in range(0, 256):
            i = i / 255.0
            chars.append(chr(int( end * i + start * (1.0 - i) ) ) )
            
        rv = "".join(chars)
        ramp_cache[start, end] = rv

    return rv

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

class Twocolor(ImageBase):
    """
    This takes as arguments two colors, white and black. The image is
    mapped such that pixels in white have the white color, pixels in
    black have the black color, and shades of gray are linearly
    interpolated inbetween.  The alpha channel is mapped linearly
    between 0 and the alpha found in the white color, the black
    color's alpha is ignored.
    """

    def __init__(self, im, white, black, force_alpha=False, **properties):

        white = renpy.easy.color(white)
        black = renpy.easy.color(black)

        im = image(im)

        super(Twocolor, self).__init__(im, white, black, force_alpha, **properties)
        
        self.image = im
        self.white = white
        self.black = black

        self.force_alpha = force_alpha

    def load(self):

        surf = cache.get(self.image)

        if not renpy.display.module.can_twomap:
            return surf

        if self.force_alpha and not (surf.get_masks()[3]):
            surf = surf.convert_alpha()

        rv = pygame.Surface(surf.get_size(), surf.get_flags(), surf)

        renpy.display.module.twomap(surf, rv,
                                    self.white, self.black)

        return rv

    def predict_files(self):
        return self.image.predict_files()


class Recolor(ImageBase):
    """
    This adjusts the colors of the image that is its child. It takes as an
    argument 4 numbers between 0 and 255, and maps each channel of the image
    linearly between 0 and the supplied color.
    """

    def __init__(self, im, rmul=255, gmul=255, bmul=255,
                 amul=255, force_alpha=False, **properties):

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

class MatrixColor(ImageBase):
    """
    This applies a 20 element matrix, that turns the color vector:
    [ r, g, b, a, 1 ] into [ r, g, b, a ].
    """

    def __init__(self, im, matrix, **properties):

        im = image(im)

        if len(matrix) != 20 and len(matrix) != 25:
            raise Exception("ColorMatrix expects a 20 or 25 element matrix, got %d elements." % len(matrix))

        matrix = tuple(matrix)        
        super(MatrixColor, self).__init__(im, matrix, **properties)
        
        self.image = im
        self.matrix = matrix
        
    def load(self):

        surf = cache.get(self.image)

        if not renpy.display.module.can_colormatrix:
            return surf

        if not (surf.get_masks()[3]):
            surf = surf.convert_alpha()

        rv = pygame.Surface(surf.get_size(), surf.get_flags(), surf)

        renpy.display.module.colormatrix(surf, rv, self.matrix)
        
        return rv

    def predict_files(self):
        return self.image.predict_files()

class matrix(tuple):
    """
    This class represents a 5x5 mathematical matrix.
    """

    def __new__(cls, *args):

        if len(args) == 1:
            args = tuple(args[0])

        if len(args) == 20:
            args = args + (0, 0, 0, 0, 1)

        if len(args) != 25:
            raise Exception("Matrix expects to be given 20 or 25 entries, not %d." % len(args))

        return tuple.__new__(cls, args)
    
    def mul(self, a, b):

        if not isinstance(a, matrix):
            a = matrix(a)

        if not isinstance(b, matrix):
            b = matrix(b)
            
        result = [ 0 ] * 25
        for y in range(0, 5):
            for x in range(0, 5):
                for i in range(0, 5):
                    result[x + y * 5] += a[x + i * 5] * b[i + y * 5]
                    
        return matrix(result)

    def scalar_mul(self, other):
        other = float(other)
        return matrix([ i * other for i in self ])

    def vector_mul(self, o):
        
        return (o[0]*self[0] + o[1]*self[1] + o[2]*self[2] + o[3]*self[3] + self[4],
                o[0]*self[5] + o[1]*self[6] + o[2]*self[7] + o[3]*self[8] + self[9],
                o[0]*self[10] + o[1]*self[11] + o[2]*self[12] + o[3]*self[13] + self[14],
                o[0]*self[15] + o[1]*self[16] + o[2]*self[17] + o[3]*self[18] + self[19],
                1)

                 
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = float(other)
            return matrix([ i + other for i in self ])

        other = matrix(other)
        return matrix([ i + j for i, j in zip(self, other)])

    __radd__ = __add__

    def __sub__(self, other):
        return self + other * -1

    def __rsub__(self, other):
        return self * -1 + other
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.scalar_mul(other)

        return self.mul(self, other)
    
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.scalar_mul(other)
        
        return self.mul(other, self)

    def __repr__(self):
        return """\
im.matrix(%f, %f, %f, %f, %f.
          %f, %f, %f, %f, %f,
          %f, %f, %f, %f, %f,
          %f, %f, %f, %f, %f,
          %f, %f, %f, %f, %f)""" % self

    
    def identity():
        return matrix(1, 0, 0, 0, 0,
                      0, 1, 0, 0, 0,
                      0, 0, 1, 0, 0,
                      0, 0, 0, 1, 0)

    identity = staticmethod(identity)

    def saturation(level, desat=(0.2126, 0.7152, 0.0722)):

        r, g, b = desat
        
        def I(a, b):
            return a + (b - a) * level

        return matrix(I(r, 1), I(g, 0), I(b, 0), 0, 0,
                      I(r, 0), I(g, 1), I(b, 0), 0, 0,
                      I(r, 0), I(g, 0), I(b, 1), 0, 0,
                      0, 0, 0, 1, 0)

    saturation = staticmethod(saturation)
    
    def desaturate():
        return matrix.saturation(0.0)
    
    desaturate = staticmethod(desaturate)

    
    def tint(r, g, b):
        return matrix(r, 0, 0, 0, 0,
                      0, g, 0, 0, 0,
                      0, 0, b, 0, 0,
                      0, 0, 0, 1, 0)

    tint = staticmethod(tint)

    def invert():
        return matrix(-1, 0, 0, 0, 1,
                      0, -1, 0, 0, 1,
                      0, 0, -1, 0, 1,
                      0, 0, 0, 1, 0)

    invert = staticmethod(invert)

    def brightness(b):
        return matrix(1, 0, 0, 0, b,
                      0, 1, 0, 0, b,
                      0, 0, 1, 0, b,
                      0, 0, 0, 1, 0)

    brightness = staticmethod(brightness)

    def opacity(o):
        return matrix(1, 0, 0, 0, 0,
                      0, 1, 0, 0, 0,
                      0, 0, 1, 0, 0,
                      0, 0, 0, o, 0)

    opacity = staticmethod(opacity)

    def contrast(c):
        return matrix.brightness(-.5) * matrix.tint(c, c, c) * matrix.brightness(.5) 


    # from http://www.gskinner.com/blog/archives/2005/09/flash_8_source.html
    def hue(h):
        h = h * math.pi / 180
        cosVal = math.cos(h)
        sinVal = math.sin(h)
        lumR = 0.213;
        lumG = 0.715;
        lumB = 0.072;
        return matrix(
            lumR+cosVal*(1-lumR)+sinVal*(-lumR),lumG+cosVal*(-lumG)+sinVal*(-lumG),lumB+cosVal*(-lumB)+sinVal*(1-lumB),0,0,
            lumR+cosVal*(-lumR)+sinVal*(0.143),lumG+cosVal*(1-lumG)+sinVal*(0.140),lumB+cosVal*(-lumB)+sinVal*(-0.283),0,0,
            lumR+cosVal*(-lumR)+sinVal*(-(1-lumR)),lumG+cosVal*(-lumG)+sinVal*(lumG),lumB+cosVal*(1-lumB)+sinVal*(lumB),0,0,
            0,0,0,1,0,
            0,0,0,0,1
            )

    hue = staticmethod(hue)

    
def Grayscale(im, desat=(0.2126, 0.7152, 0.0722)):
    return MatrixColor(im, matrix.saturation(0.0, desat))

def Sepia(im, tint=(1.0, .94, .76), desat=(0.2126, 0.7152, 0.0722)):
    return MatrixColor(im, matrix.saturation(0.0, desat) * matrix.tint(tint[0], tint[1], tint[2]))
    
def Color(im, color):
    """
    This recolors the supplied image, mapping colors such that black is
    black and white is the supplied color.
    """

    r, g, b, a = renpy.easy.color(color)

    return Recolor(im, r, g, b, a)


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

        rv = pygame.Surface(size, 0, surf)

        for y in range(0, height, sh):
            for x in range(0, width, sw):
                rv.blit(surf, (x, y))

        return rv

    def predict_files(self):
        return self.image.predict_files()

class AlphaMask(ImageBase):

    def __init__(self, base, mask, **properties):
        super(AlphaMask, self).__init__(base, mask, **properties)

        self.base = image(base)
        self.mask = image(mask)

    def load(self):

        basesurf = cache.get(self.base)
        masksurf = cache.get(self.mask)

        if basesurf.get_size() != masksurf.get_size():
            raise Exception("AlphaMask surfaces must be the same size.")

        rv = pygame.Surface(basesurf.get_size(), 0, renpy.game.interface.display.sample_surface)
        # rv.fill((0, 255, 0, 0))
        
        if renpy.display.module.can_imageblend and 1:
            renpy.display.module.imageblend(rv, basesurf, rv, masksurf, identity)

        return rv
            
    def predict_files(self):
        return self.base.predict_files() + self.mask.predict_files()
        
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

    if isinstance(arg, renpy.display.image.ImageReference):
        arg.find_target()
        return image(arg.target, loose=loose, **properties)
        
    
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
