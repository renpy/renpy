# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

import renpy
import renpy.pygame as pygame

from renpy.display.render import render


# A list of cache images we've already written.
cached = set()


class ImageMapCrop(renpy.display.displayable.Displayable):
    """
    This handles the cropping of uncached imagemap components.
    """

    def __init__(self, child, rect):
        super(ImageMapCrop, self).__init__()

        self.child = child
        self.rect = rect

    def visit(self):
        return [self.child]

    def render(self, width, height, st, at):
        cr = render(self.child, renpy.config.screen_width, renpy.config.screen_height, st, at)
        return cr.subsurface(self.rect)


class ImageCacheCrop(renpy.display.displayable.Displayable):
    """
    This handles the cropping of an imagemap component.
    """

    def __init__(self, cache, index):
        super(ImageCacheCrop, self).__init__()

    def render(self, width, height, st, at):
        return renpy.display.render.Render(0, 0)


class ImageMapCache(renpy.object.Object):
    """
    This previously would cache an image map into a single image. That's not
    necessary anymore, so all this does is crop images.
    """

    def __init__(self, enable):
        enable = False
        self.enable = enable

    def crop(self, d, rect):
        return ImageMapCrop(d, rect)

    def finish(self):
        return
