# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function
import renpy.display

import math
import zipfile
import cStringIO
import threading
import time


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

        # A lock that must be held when updating the cache.
        self.lock = threading.Condition()

        # A lock that mist be held to notify the preload thread.
        self.preload_lock = threading.Condition()

        # Is the preload_thread alive?
        self.keep_preloading = True

        # A map from image object to surface, only for objects that have
        # been pinned into memory.
        self.pin_cache = { }

        # Images that we tried, and failed, to preload.
        self.preload_blacklist = set()

        # The size of the cache, in pixels.
        self.cache_limit = 0

        # The preload thread.
        self.preload_thread = threading.Thread(target=self.preload_thread_main, name="preloader")
        self.preload_thread.setDaemon(True)
        self.preload_thread.start()

        # Have we been added this tick?
        self.added = set()

        # A list of (time, filename, preload) tuples. This is updated when
        # config.developer is True and an image is loaded. Preload is a
        # flag that is true if the image was loaded from the preload
        # thread. The log is limited to 100 entries, and the newest entry
        # is first.
        #
        # This is only updated when config.developer is True.
        self.load_log = [ ]

    def init(self):
        """
        Updates the cache object to make use of settings that might be provided
        by the game-maker.
        """

        self.cache_limit = renpy.config.image_cache_size * renpy.config.screen_width * renpy.config.screen_height

    def quit(self):  # @ReservedAssignment
        if not self.preload_thread.isAlive():
            return

        with self.preload_lock:
            self.keep_preloading = False
            self.preload_lock.notify()

        self.preload_thread.join()

        self.clear()

    # Clears out the cache.
    def clear(self):

        self.lock.acquire()

        self.preloads = [ ]
        self.pin_cache = { }
        self.cache = { }
        self.first_preload_in_tick = True
        self.size_of_current_generation = 0
        self.total_cache_size = 0

        self.added.clear()

        self.lock.release()

    # Increments time, and clears the list of images to be
    # preloaded.
    def tick(self):

        with self.lock:
            self.time += 1
            self.preloads = [ ]
            self.first_preload_in_tick = True
            self.size_of_current_generation = 0
            self.added.clear()

        if renpy.config.debug_image_cache:
            renpy.display.ic_log.write("----")
            filename, line = renpy.exports.get_filename_line()
            renpy.display.ic_log.write("%s %d", filename, line)

    # The preload thread can deal with this update, so we don't need
    # to lock things.
    def end_tick(self):
        self.preloads = [ ]

    # This returns the pygame surface corresponding to the provided
    # image. It also takes care of updating the age of images in the
    # cache to be current, and maintaining the size of the current
    # generation of images.
    def get(self, image, predict=False, texture=False):

        if not isinstance(image, ImageBase):
            raise Exception("Expected an image of some sort, but got" + str(image) + ".")

        if not image.cache:
            surf = image.load()
            renpy.display.render.mutated_surface(surf)
            return surf

        # First try to grab the image out of the cache without locking it.
        ce = self.cache.get(image, None)

        # Otherwise, we load the image ourselves.
        if ce is None:

            try:
                if image in self.pin_cache:
                    surf = self.pin_cache[image]
                else:
                    if not predict:
                        with renpy.game.ExceptionInfo("While loading %r:", image):
                            surf = image.load()
                    else:
                        surf = image.load()

            except:
                raise

            with self.lock:

                ce = CacheEntry(image, surf)

                if image not in self.cache:
                    self.total_cache_size += ce.size

                self.cache[image] = ce

                # Indicate that this surface had changed.
                renpy.display.render.mutated_surface(ce.surf)

                if renpy.config.debug_image_cache:
                    if predict:
                        renpy.display.ic_log.write("Added %r (%.02f%%)", ce.what, 100.0 * self.total_cache_size / self.cache_limit)
                    else:
                        renpy.display.ic_log.write("Total Miss %r", ce.what)

        # Move it into the current generation. This isn't protected by
        # a lock, so in certain circumstances we could have an
        # inaccurate size - but that will be cured at the end of the
        # current generation.

        if ce.time != self.time:
            ce.time = self.time
            self.size_of_current_generation += ce.size

        # Done... return the surface.
        return ce.surf

    # This kills off a given cache entry.
    def kill(self, ce):

        # Should never happen... but...
        if ce.time == self.time:
            self.size_of_current_generation -= ce.size

        # Let the texture cache know we're not needed.
        renpy.display.draw.mutated_surface(ce.surf)

        self.total_cache_size -= ce.size
        del self.cache[ce.what]

        if renpy.config.debug_image_cache:
            renpy.display.ic_log.write("Removed %r", ce.what)

    def cleanout(self):
        """
        Cleans out the cache, if it's gotten too large. Returns True
        if the cache is smaller than the size limit, or False if it's
        bigger and we don't want to continue preloading.
        """

        # If we're within the limit, return.
        if self.total_cache_size <= self.cache_limit:
            return True

        # If we're outside the cache limit, we need to go and start
        # killing off some of the entries until we're back inside it.

        for ce in sorted(self.cache.itervalues(), key=lambda a : a.time):

            if ce.time == self.time:
                # If we're bigger than the limit, and there's nothing
                # to remove, we should stop the preloading right away.
                return False

            # Otherwise, kill off the given cache entry.
            self.kill(ce)

            # If we're in the limit, we're done.
            if self.total_cache_size <= self.cache_limit:
                break

        return True

    def preload_texture(self, im):
        """
        Preloads `im` into the cache, and loads the corresponding texture
        into the GPU.
        """

        surf = self.get(im, predict=True)
        renpy.display.draw.load_texture(surf)

    # Called to report that a given image would like to be preloaded.
    def preload_image(self, im):

        if not isinstance(im, ImageBase):
            return

        with self.lock:

            if im in self.added:
                return

            self.added.add(im)

            if im in self.cache:
                self.preload_texture(im)
                in_cache = True
            else:
                self.preloads.append(im)
                in_cache = False

        if not in_cache:

            with self.preload_lock:
                self.preload_lock.notify()

        if in_cache and renpy.config.debug_image_cache:
            renpy.display.ic_log.write("Kept %r", im)

    def start_prediction(self):
        """
        Called at the start of prediction, to ensure the thread runs
        at least once to clean out the cache.
        """

        with self.preload_lock:
            self.preload_lock.notify()

    def preload_thread_main(self):

        while self.keep_preloading:

            self.preload_lock.acquire()
            self.preload_lock.wait()
            self.preload_lock.release()

            while self.preloads and self.keep_preloading:

                # If the size of the current generation is bigger than the
                # total cache size, stop preloading.
                with self.lock:

                    # If the cache is overfull, clean it out.
                    if not self.cleanout():

                        if renpy.config.debug_image_cache:
                            for i in self.preloads:
                                renpy.display.ic_log.write("Overfull %r", i)

                        self.preloads = [ ]

                        break

                try:
                    image = self.preloads.pop(0)

                    if image not in self.preload_blacklist:
                        try:
                            self.preload_texture(image)
                        except:
                            self.preload_blacklist.add(image)
                except:
                    pass

            with self.lock:
                self.cleanout()

            # If we have time, preload pinned images.
            if self.keep_preloading and not renpy.game.less_memory:

                workset = set(renpy.store._cache_pin_set)

                # Remove things that are not in the workset from the pin cache,
                # and remove things that are in the workset from pin cache.
                for i in self.pin_cache.keys():

                    if i in workset:
                        workset.remove(i)
                    else:
                        surf = self.pin_cache[i]

                        del self.pin_cache[i]

                # For each image in the worklist...
                for image in workset:

                    if image in self.preload_blacklist:
                        continue

                    # If we have normal preloads, break out.
                    if self.preloads:
                        break

                    try:
                        surf = image.load()
                        self.pin_cache[image] = surf
                        renpy.display.draw.load_texture(surf)
                    except:
                        self.preload_blacklist.add(image)

    def add_load_log(self, filename):

        if not renpy.config.developer:
            return

        preload = (threading.current_thread() is self.preload_thread)

        self.load_log.insert(0, (time.time(), filename, preload))

        while len(self.load_log) > 100:
            self.load_log.pop()


# The cache object.
cache = Cache()


def free_memory():
    """
    Frees some memory.
    """

    renpy.display.draw.free_memory()
    cache.clear()


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

        raise Exception("load method not implemented.")

    def render(self, w, h, st, at):

        im = cache.get(self)
        texture = renpy.display.draw.load_texture(im)

        w, h = im.get_size()
        rv = renpy.display.render.Render(w, h)
        rv.blit(texture, (0, 0))
        return rv

    def predict_one(self):
        renpy.display.predict.image(self)

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

    def __unicode__(self):
        if len(self.filename) < 20:
            return u"Image %r" % self.filename
        else:
            return u"Image \u2026%s" % self.filename[-20:]

    def get_hash(self):
        return renpy.loader.get_hash(self.filename)

    def load(self, unscaled=False):

        cache.add_load_log(self.filename)

        try:

            if unscaled:
                surf = renpy.display.pgrender.load_image_unscaled(renpy.loader.load(self.filename), self.filename)
            else:
                surf = renpy.display.pgrender.load_image(renpy.loader.load(self.filename), self.filename)

            return surf

        except Exception as e:

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

            return [ self.filename ]


class ZipFileImage(ImageBase):

    def __init__(self, zipfilename, filename, mtime=0, **properties):
        super(ZipFileImage, self).__init__(zipfilename, filename, mtime, **properties)

        self.zipfilename = zipfilename
        self.filename = filename

    def load(self):
        try:
            zf = zipfile.ZipFile(self.zipfilename, 'r')
            data = zf.read(self.filename)
            sio = cStringIO.StringIO(data)
            rv = renpy.display.pgrender.load_image(sio, self.filename)
            zf.close()
            return rv
        except:
            return renpy.display.pgrender.surface((2, 2), True)

    def predict_files(self):
        return [ ]


class Composite(ImageBase):
    """
    :doc: im_im

    This image manipulator composites multiple images together to
    form a single image.

    The `size` should be a (width, height) tuple giving the size
    of the composed image.

    The remaining positional arguments are interpreted as groups of
    two. The first argument in a group should be an (x, y) tuple,
    while the second should be an image manipulator. The image
    produced by the image manipulator is composited at the location
    given by the tuple.

    ::

        image girl clothed happy = im.Composite(
            (300, 600),
            (0, 0), "girl_body.png",
            (0, 0), "girl_clothes.png",
            (100, 100), "girl_happy.png"
            )

    """

    def __init__(self, size, *args, **properties):

        super(Composite, self).__init__(size, *args, **properties)

        if len(args) % 2 != 0:
            raise Exception("Composite requires an odd number of arguments.")

        self.size = size
        self.positions = args[0::2]
        self.images = [ image(i) for i in args[1::2] ]

    def get_hash(self):
        rv = 0

        for i in self.images:
            rv += i.get_hash()

        return rv

    def load(self):

        if self.size:
            size = self.size
        else:
            size = cache.get(self.images[0]).get_size()

        rv = renpy.display.pgrender.surface(size, True)

        for pos, im in zip(self.positions, self.images):
            rv.blit(cache.get(im), pos)

        return rv

    def predict_files(self):

        rv = [ ]

        for i in self.images:
            rv.extend(i.predict_files())

        return rv


class Scale(ImageBase):
    """
    :doc: im_im

    An image manipulator that scales `im` (an image manipulator) to
    `width` and `height`.

    If `bilinear` is true, then bilinear interpolation is used for
    the scaling. Otherwise, nearest neighbor interpolation is used.

    ::

        image logo scale = im.Scale("logo.png", 100, 150)
    """

    def __init__(self, im, width, height, bilinear=True, **properties):

        im = image(im)
        super(Scale, self).__init__(im, width, height, bilinear, **properties)

        self.image = im
        self.width = int(width)
        self.height = int(height)
        self.bilinear = bilinear

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        child = cache.get(self.image)

        if self.bilinear:
            try:
                renpy.display.render.blit_lock.acquire()
                rv = renpy.display.scale.smoothscale(child, (self.width, self.height))
            finally:
                renpy.display.render.blit_lock.release()
        else:
            try:
                renpy.display.render.blit_lock.acquire()
                rv = renpy.display.pgrender.transform_scale(child, (self.width, self.height))
            finally:
                renpy.display.render.blit_lock.release()

        return rv

    def predict_files(self):
        return self.image.predict_files()


class FactorScale(ImageBase):
    """
    :doc: im_im

    An image manipulator that scales `im` (a second image manipulator)
    to `width` times its original `width`, and `height` times its
    original height. If `height` is omitted, it defaults to `width`.

    If `bilinear` is true, then bilinear interpolation is used for
    the scaling. Otherwise, nearest neighbor interpolation is used.

    ::

        image logo doubled = im.FactorScale("logo.png", 1.5)
    """

    def __init__(self, im, width, height=None, bilinear=True, **properties):

        if height is None:
            height = width

        im = image(im)
        super(FactorScale, self).__init__(im, width, height, bilinear, **properties)

        self.image = im
        self.width = width
        self.height = height
        self.bilinear = bilinear

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        surf = cache.get(self.image)
        width, height = surf.get_size()

        width = int(width * self.width)
        height = int(height * self.height)

        if self.bilinear:
            try:
                renpy.display.render.blit_lock.acquire()
                rv = renpy.display.scale.smoothscale(surf, (width, height))
            finally:
                renpy.display.render.blit_lock.release()

        else:
            try:
                renpy.display.render.blit_lock.acquire()
                rv = renpy.display.pgrender.transform_scale(surf, (width, height))
            finally:
                renpy.display.render.blit_lock.release()

        return rv

    def predict_files(self):
        return self.image.predict_files()


class Flip(ImageBase):
    """
    :doc: im_im

    An image manipulator that flips `im` (an image manipulator)
    vertically or horizontally.  `vertical` and `horizontal` control
    the directions in which the image is flipped.

    ::

        image eileen flip = im.Flip("eileen_happy.png", vertical=True)
    """

    def __init__(self, im, horizontal=False, vertical=False, **properties):

        if not (horizontal or vertical):
            raise Exception("im.Flip must be called with a true value for horizontal or vertical.")

        im = image(im)
        super(Flip, self).__init__(im, horizontal, vertical, **properties)

        self.image = im
        self.horizontal = horizontal
        self.vertical = vertical

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        child = cache.get(self.image)

        try:
            renpy.display.render.blit_lock.acquire()
            rv = renpy.display.pgrender.flip(child, self.horizontal, self.vertical)
        finally:
            renpy.display.render.blit_lock.release()

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

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        child = cache.get(self.image)

        try:
            renpy.display.render.blit_lock.acquire()
            rv = renpy.display.pgrender.rotozoom(child, self.angle, self.zoom)
        finally:
            renpy.display.render.blit_lock.release()

        return rv

    def predict_files(self):
        return self.image.predict_files()


class Crop(ImageBase):
    """
    :doc: im_im
    :args: (im, rect)

    An image manipulator that crops `rect`, a (x, y, width, height) tuple,
    out of `im`, an image manipulator.

    ::

        image logo crop = im.Crop("logo.png", (0, 0, 100, 307))
    """

    def __init__(self, im, x, y=None, w=None, h=None, **properties):

        im = image(im)

        if y is None:
            (x, y, w, h) = x

        super(Crop, self).__init__(im, x, y, w, h, **properties)

        self.image = im
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_hash(self):
        return self.image.get_hash()

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

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        surf = cache.get(self.image)

        rv = renpy.display.pgrender.surface(surf.get_size(), True)

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

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        surf = cache.get(self.image)

        rv = renpy.display.pgrender.surface(surf.get_size(), True)

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

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        surf = cache.get(self.image)

        rv = renpy.display.pgrender.surface(surf.get_size(), True)

        renpy.display.module.linmap(surf, rv,
                                    self.rmul, self.gmul, self.bmul, self.amul)

        return rv

    def predict_files(self):
        return self.image.predict_files()


class MatrixColor(ImageBase):
    """
    :doc: im_matrixcolor

    An image operator that uses `matrix` to linearly transform the
    image manipulator `im`.

    `Matrix` should be a list, tuple, or :func:`im.matrix` that is 20
    or 25 elements long. If the object has 25 elements, then elements
    past the 20th are ignored.

    When the four components of the source color are R, G, B, and A,
    which range from 0.0 to 1.0; the four components of the transformed
    color are R', G', B', and A', with the same range; and the elements
    of the matrix are named::

        [ a, b, c, d, e,
          f, g, h, i, j,
          k, l, m, n, o,
          p, q, r, s, t ]

    the transformed colors can be computed with the formula::

        R' = (a * R) + (b * G) + (c * B) + (d * A) + e
        G' = (f * R) + (g * G) + (h * B) + (i * A) + j
        B' = (k * R) + (l * G) + (m * B) + (n * A) + o
        A' = (p * R) + (q * G) + (r * B) + (s * A) + t

    The components of the transformed color are clamped to the
    range [0.0, 1.0].
    """

    def __init__(self, im, matrix, **properties):

        im = image(im)

        if len(matrix) != 20 and len(matrix) != 25:
            raise Exception("ColorMatrix expects a 20 or 25 element matrix, got %d elements." % len(matrix))

        matrix = tuple(matrix)
        super(MatrixColor, self).__init__(im, matrix, **properties)

        self.image = im
        self.matrix = matrix

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        surf = cache.get(self.image)

        rv = renpy.display.pgrender.surface(surf.get_size(), True)

        renpy.display.module.colormatrix(surf, rv, self.matrix)

        return rv

    def predict_files(self):
        return self.image.predict_files()


class matrix(tuple):
    """
    :doc: im_matrixcolor

    Constructs an im.matrix object from `matrix`. im.matrix objects
    support The operations supported are matrix multiplication, scalar
    multiplication, element-wise addition, and element-wise
    subtraction. These operations are invoked using the standard
    mathematical operators (\\*, \\*, +, and -, respectively). If two
    im.matrix objects are multiplied, matrix multiplication is
    performed, otherwise scalar multiplication is used.

    `matrix` is a 20 or 25 element list or tuple. If it is 20 elements
    long, it is padded with (0, 0, 0, 0, 1) to make a 5x5 matrix,
    suitable for multiplication.
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

            if isinstance(b, renpy.easy.Color):
                return NotImplemented

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

    @staticmethod
    def identity():
        """
        :doc: im_matrixcolor
        :name: im.matrix.identity

        Returns an identity matrix, one that does not change color or
        alpha.
        """

        return matrix(1, 0, 0, 0, 0,
                      0, 1, 0, 0, 0,
                      0, 0, 1, 0, 0,
                      0, 0, 0, 1, 0)

    @staticmethod
    def saturation(level, desat=(0.2126, 0.7152, 0.0722)):
        """
        :doc: im_matrixcolor
        :name: im.matrix.saturation

        Returns an im.matrix that alters the saturation of an
        image. The alpha channel is untouched.

        `level`
            The amount of saturation in the resulting image. 1.0 is
            the unaltered image, while 0.0 is grayscale.

        `desat`
            This is a 3-element tuple that controls how much of the
            red, green, and blue channels will be placed into all
            three channels of a fully desaturated image. The default
            is based on the constants used for the luminance channel
            of an NTSC television signal. Since the human eye is
            mostly sensitive to green, more of the green channel is
            kept then the other two channels.
        """

        r, g, b = desat

        def I(a, b):
            return a + (b - a) * level

        return matrix(I(r, 1), I(g, 0), I(b, 0), 0, 0,
                      I(r, 0), I(g, 1), I(b, 0), 0, 0,
                      I(r, 0), I(g, 0), I(b, 1), 0, 0,
                      0, 0, 0, 1, 0)

    @staticmethod
    def desaturate():
        """
        :doc: im_matrixcolor
        :name: im.matrix.desaturate

        Returns an im.matrix that desaturates the image (makes it
        grayscale). This is equivalent to calling
        im.matrix.saturation(0).
        """

        return matrix.saturation(0.0)

    @staticmethod
    def tint(r, g, b):
        """
        :doc: im_matrixcolor
        :name: im.matrix.tint

        Returns an im.matrix that tints an image, without changing
        the alpha channel. `r`, `g`, and `b` should be numbers between
        0 and 1, and control what fraction of the given channel is
        placed into the final image. (For example, if `r` is .5, and
        the value of the red channel is 100, the transformed color
        will have a red value of 50.)
        """

        return matrix(r, 0, 0, 0, 0,
                      0, g, 0, 0, 0,
                      0, 0, b, 0, 0,
                      0, 0, 0, 1, 0)

    @staticmethod
    def invert():
        """
        :doc: im_matrixcolor
        :name: im.matrix.invert

        Returns an im.matrix that inverts the red, green, and blue
        channels of the image without changing the alpha channel.
        """

        return matrix(-1, 0, 0, 0, 1,
                      0, -1, 0, 0, 1,
                      0, 0, -1, 0, 1,
                      0, 0, 0, 1, 0)

    @staticmethod
    def brightness(b):
        """
        :doc: im_matrixcolor
        :name: im.matrix.brightness

        Returns an im.matrix that alters the brightness of an image.

        `b`
            The amount of change in image brightness. This should be
            a number between -1 and 1, with -1 the darkest possible
            image and 1 the brightest.
        """

        return matrix(1, 0, 0, 0, b,
                      0, 1, 0, 0, b,
                      0, 0, 1, 0, b,
                      0, 0, 0, 1, 0)

    @staticmethod
    def opacity(o):
        """
        :doc: im_matrixcolor
        :name: im.matrix.opacity

        Returns an im.matrix that alters the opacity of an image. An
        `o` of 0.0 is fully transparent, while 1.0 is fully opaque.
        """

        return matrix(1, 0, 0, 0, 0,
                      0, 1, 0, 0, 0,
                      0, 0, 1, 0, 0,
                      0, 0, 0, o, 0)

    @staticmethod
    def contrast(c):
        """
        :doc: im_matrixcolor
        :name: im.matrix.contrast

        Returns an im.matrix that alters the contrast of an image. `c` should
        be greater than 0.0, with values between 0.0 and 1.0 decreasing contrast, and
        values greater than 1.0 increasing contrast.
        """

        return matrix.brightness(-.5) * matrix.tint(c, c, c) * matrix.brightness(.5)

    # from http://www.gskinner.com/blog/archives/2005/09/flash_8_source.html
    @staticmethod
    def hue(h):
        """
        :doc: im_matrixcolor
        :name: im.matrix.hue

        Returns an im.matrix that rotates the hue by `h` degrees, while
        preserving luminosity.
        """

        h = h * math.pi / 180
        cosVal = math.cos(h)
        sinVal = math.sin(h)
        lumR = 0.213
        lumG = 0.715
        lumB = 0.072
        return matrix(
            lumR+cosVal*(1-lumR)+sinVal*(-lumR), lumG+cosVal*(-lumG)+sinVal*(-lumG), lumB+cosVal*(-lumB)+sinVal*(1-lumB), 0, 0,
            lumR+cosVal*(-lumR)+sinVal*(0.143), lumG+cosVal*(1-lumG)+sinVal*(0.140), lumB+cosVal*(-lumB)+sinVal*(-0.283), 0, 0,
            lumR+cosVal*(-lumR)+sinVal*(-(1-lumR)), lumG+cosVal*(-lumG)+sinVal*(lumG), lumB+cosVal*(1-lumB)+sinVal*(lumB), 0, 0,
            0, 0, 0, 1, 0,
            0, 0, 0, 0, 1
            )

    @staticmethod
    def colorize(black_color, white_color):
        """
        :doc: im_matrixcolor
        :name: im.matrix.colorize

        Returns an im.matrix that colorizes a black and white image.
        `black_color` and `white_color` are Ren'Py style colors, so
        they may be specified as strings or tuples of (0-255) color
        values. ::

            # This makes black colors red, and white colors blue.
            image logo colored = im.MatrixColor(
                "bwlogo.png",
                im.matrix.colorize("#f00", "#00f"))

        """

        (r0, g0, b0, _a0) = renpy.easy.color(black_color)
        (r1, g1, b1, _a1) = renpy.easy.color(white_color)

        r0 /= 255.0
        g0 /= 255.0
        b0 /= 255.0
        r1 /= 255.0
        g1 /= 255.0
        b1 /= 255.0

        return matrix((r1-r0), 0, 0, 0, r0,
                      0, (g1-g0), 0, 0, g0,
                      0, 0, (b1-b0), 0, b0,
                      0, 0, 0, 1, 0)


def Grayscale(im, desat=(0.2126, 0.7152, 0.0722), **properties):
    """
    :doc: im_im
    :args: (im, **properties)

    An image manipulator that creates a desaturated version of the image
    manipulator `im`.
    """

    return MatrixColor(im, matrix.saturation(0.0, desat), **properties)


def Sepia(im, tint=(1.0, .94, .76), desat=(0.2126, 0.7152, 0.0722), **properties):
    """
    :doc: im_im
    :args: (im, **properties)

    An image manipulator that creates a sepia-toned version of the image
    manipulator `im`.
    """

    return MatrixColor(im, matrix.saturation(0.0, desat) * matrix.tint(tint[0], tint[1], tint[2]), **properties)


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
    :doc: im_im

    An image manipulator that tiles the image manipulator `im`, until
    it is `size`.

    `size`
        If not None, a (width, height) tuple. If None, this defaults to
        (:var:`config.screen_width`, :var:`config.screen_height`).
    """

    def __init__(self, im, size=None, **properties):

        im = image(im)

        super(Tile, self).__init__(im, size, **properties)
        self.image = im
        self.size = size

    def get_hash(self):
        return self.image.get_hash()

    def load(self):

        size = self.size

        if size is None:
            size = (renpy.config.screen_width, renpy.config.screen_height)

        surf = cache.get(self.image)

        rv = renpy.display.pgrender.surface(size, True)

        width, height = size
        sw, sh = surf.get_size()

        for y in range(0, height, sh):
            for x in range(0, width, sw):
                rv.blit(surf, (x, y))

        return rv

    def predict_files(self):
        return self.image.predict_files()


class AlphaMask(ImageBase):
    """
    :doc: im_im

    An image manipulator that takes two image manipulators, `base` and
    `mask`, as arguments. It replaces the alpha channel of `base` with
    the red channel of `mask`.

    This is used to provide an image's alpha channel in a second
    image, like having one jpeg for color data, and a second one
    for alpha. In some cases, two jpegs can be smaller than a
    single png file.

    Note that this takes different arguments from :func:`AlphaMask`,
    which uses the mask's alpha channel.
    """

    def __init__(self, base, mask, **properties):
        super(AlphaMask, self).__init__(base, mask, **properties)

        self.base = image(base)
        self.mask = image(mask)

    def get_hash(self):
        return self.base.get_hash() + self.image.get_hash()

    def load(self):

        basesurf = cache.get(self.base)
        masksurf = cache.get(self.mask)

        if basesurf.get_size() != masksurf.get_size():
            raise Exception("AlphaMask surfaces must be the same size.")

        # Used to copy the surface.
        rv = renpy.display.pgrender.copy_surface(basesurf)
        renpy.display.module.alpha_munge(masksurf, rv, identity)

        return rv

    def predict_files(self):
        return self.base.predict_files() + self.mask.predict_files()


def image(arg, loose=False, **properties):
    """
    :doc: im_image
    :name: Image
    :args: (filename, **properties)

    Loads an image from a file. `filename` is a
    string giving the name of the file.

    `filename` should be a JPEG or PNG file with an appropriate
    extension.
    """

    """
    (Actually, the user documentation is a bit misleading, as
     this tries for compatibility with several older forms of
     image specification.)

    If the loose argument is False, then this will report an error if an
    arbitrary argument is given. If it's True, then the argument is passed
    through unchanged.
    """

    if isinstance(arg, ImageBase):
        return arg

    elif isinstance(arg, basestring):
        return Image(arg, **properties)

    elif isinstance(arg, renpy.display.image.ImageReference):
        arg.find_target()
        return image(arg.target, loose=loose, **properties)

    elif isinstance(arg, tuple):
        params = [ ]

        for i in arg:
            params.append((0, 0))
            params.append(i)

        return Composite(None, *params)

    elif loose:
        return arg

    if isinstance(arg, renpy.display.core.Displayable):
        raise Exception("Expected an image, but got a general displayable.")
    else:
        raise Exception("Could not construct image from argument.")


def load_image(im):
    """
    :doc: udd_utility

    Loads the image manipulator `im` using the image cache, and returns a texture.
    """

    surf = cache.get(image(im))
    return renpy.display.draw.load_texture(surf)


def load_surface(im):
    """
    :doc: udd_utility

    Loads the image manipulator `im` using the image cache, and returns a pygame Surface.
    """

    return cache.get(image(im))


def reset_module():
    print("Resetting cache.")

    global cache
    cache = Cache()
