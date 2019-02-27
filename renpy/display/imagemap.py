# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# This file handles imagemap caching.

from __future__ import print_function

import pygame_sdl2 as pygame
import renpy.display

from renpy.display.render import render

import hashlib

# A list of cache images we've already written.
cached = set()


class ImageMapCrop(renpy.display.core.Displayable):
    """
    This handles the cropping of uncached imagemap components.
    """

    def __init__(self, child, rect):
        super(ImageMapCrop, self).__init__()

        self.child = child
        self.rect = rect

    def visit(self):
        return [ self.child ]

    def render(self, width, height, st, at):
        cr = render(self.child, width, height, st, at)
        return cr.subsurface(self.rect)


class ImageCacheCrop(renpy.display.core.Displayable):
    """
    This handles the cropping of an imagemap component.
    """

    def __init__(self, cache, index):
        super(ImageCacheCrop, self).__init__()

        # The cache object we're associated with.
        self.cache = cache

        # The index of
        self.index = index

    def visit(self):
        return self.cache.visit(self.index)

    def render(self, width, height, st, at):
        return self.cache.render(self.index, width, height, st, at)


class ImageMapCache(renpy.object.Object):

    def __init__(self, enable):
        self.md5 = hashlib.md5()

        # A list of (image, rect) tuples. The index in this list is used
        # as a unique identifier for an ImageCacheCrop object.
        self.imagerect = [ ]

        # A map from (image, rect) to ImageCacheCrop object.
        self.hotspots = { }

        # A list of (width, height, index) tuples.
        self.areas = [ ]

        # The image containing our children.
        self.cache = None

        # A list that, for each hotspot, gives the rectangle in the cache
        # image corresponding to that hotspot.
        self.cache_rect = None

        # The size of the cache.
        self.cache_width = None
        self.cache_height = None

        # Temporarily disabled.
        enable = False

        self.enable = enable

    def visit(self, index):
        if self.cache is not None:
            return [ self.cache ]
        else:
            return [ self.imagerect[index][0] ]

    def crop(self, d, rect):
        if not isinstance(d, renpy.display.im.ImageBase) or \
                not renpy.config.imagemap_cache or \
                not self.enable:
            return ImageMapCrop(d, rect)

        key = (d, rect)
        rv = self.hotspots.get(key, None)
        if rv is not None:
            return rv

        self.md5.update(repr(d.identity))
        self.md5.update(repr(rect))

        index = len(self.imagerect)
        rv = ImageCacheCrop(self, index)

        self.imagerect.append(key)
        self.hotspots[key] = rv
        self.areas.append((rect[2] + 2, rect[3] + 2, index))

        return rv

    def layout(self):
        self.areas.sort()
        self.areas.reverse()
        self.cache_rect = [ None ] * len(self.areas)

        # The width of the cache image.
        width = self.areas[0][0]

        x = 0
        y = 0
        line_height = 0

        for w, h, i in self.areas:

            if x + w > width:
                y += line_height
                line_height = 0
                x = 0

            self.cache_rect[i] = (x+1, y+1, w-2, h-2)

            x += w
            if line_height < h:
                line_height = h

        self.cache_width = width
        self.cache_height = y + line_height

    def write_cache(self, filename):

        if filename in cached:
            return

        cached.add(filename)

        if renpy.loader.loadable(filename):
            return

        fn = renpy.loader.get_path(filename)

        cache = pygame.Surface((self.cache_width, self.cache_height), pygame.SRCALPHA, 32)

        for i, (d, rect) in enumerate(self.imagerect):
            x, y, _w, _h = self.cache_rect[i]

            surf = renpy.display.im.cache.get(d).subsurface(rect)
            cache.blit(surf, (x, y))

        pygame.image.save(cache, renpy.exports.fsencode(fn))

    def image_file_hash(self):
        """
        Returns a hash of the contents of the image files. (As an integer.)
        """

        rv = 0

        for i in self.imagerect:
            rv += i[0].get_hash()

        return rv & 0x7fffffff

    def finish(self):
        if not self.areas:
            return

        filename = "im-%s-%x.png" % (self.md5.hexdigest(), self.image_file_hash())

        if renpy.game.preferences.language:
            filename = renpy.game.preferences.language + "-" + filename

        filename = "cache/" + filename

        self.md5 = None

        self.layout()

        if renpy.config.developer:
            try:
                self.write_cache(filename)
            except:
                pass

        if renpy.loader.loadable(filename):
            self.cache = renpy.display.im.Image(filename)

    def render(self, index, width, height, st, at):
        if self.cache is None:
            d, rect = self.imagerect[index]
            return render(d, width, height, st, at).subsurface(rect)

        return render(self.cache, width, height, st, at).subsurface(self.cache_rect[index])
