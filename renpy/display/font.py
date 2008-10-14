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

import pygame
from pygame.constants import *

import xml.etree.ElementTree as etree

try:
    import _renpy_font
    pygame.font = _renpy_font
except:
    pass

import renpy

# This contains a map from (fn, size, bold, italics, underline) to the
# unloaded font object corresponding to that specification. 
fonts = { }

# This contains a map from (fn, size, bold, italics, underline) to the
# loaded font object corresponding to that specification.
font_cache = { }

class ImageFont(object):

    def size(self, text):
        w = 0

        if not text:
            return (0, self.height)
        
        for a, b in zip(text, text[1:]):
            w += self.sizes[a] + self.kerns.get(a + b, self.default_kern)

        w += self.sizes[text[-1]]

        return (w, self.height)
            
    def render(self, text, antialias, color, black_color=(0, 0, 0, 255), background=None):
        surf = pygame.Surface(self.size(text), 0,
                              renpy.game.interface.display.sample_surface)

        if not text:
            return surf

        x = 0
        y = 0
        
        for a, b in zip(text, text[1:]):
            surf.blit(self.chars[a], (x, y))
            x += self.sizes[a] + self.kerns.get(a + b, self.default_kern)

        surf.blit(self.chars[text[-1]], (x, y))

        if renpy.config.recolor_sfonts and \
               (color != (255, 255, 255, 255) or black_color != (0, 0, 0, 255) ) and \
               renpy.display.module.can_twomap:

            newsurf = pygame.Surface(surf.get_size(), surf.get_flags(), surf)
            renpy.display.module.twomap(surf, newsurf, color, black_color)
            renpy.display.render.mutated_surface(newsurf)

            surf = newsurf

        return surf

    def get_linesize(self):
        return self.height 

    def get_height(self):
        return self.height

    def get_ascent(self):
        return self.height

    def get_descent(self):
        return 0


class SFont(ImageFont):

    def __init__(self,
                 filename,
                 spacewidth,
                 default_kern,
                 kerns,
                 charset):

        self.filename = filename
        self.spacewidth = spacewidth
        self.default_kern = default_kern
        self.kerns = kerns
        self.charset = charset

    def load(self):

        # Map from character to subsurface.
        self.chars = { }

        # Map from character to width, height.
        self.sizes = { }

        # Load in the image.
        surf = renpy.display.im.Image(self.filename).load(unscaled=True)
        self.surf = surf

        sw, sh = surf.get_size()
        height = sh
        self.height = height

        # Create space characters.
        self.chars[u' '] = pygame.Surface((self.spacewidth, height), 0, surf)
        self.sizes[u' '] = self.spacewidth
        self.chars[u'\u00a0'] = self.chars[u' ']
        self.sizes[u'\u00a0'] = self.sizes[u' ']

        # The color key used to separate characters.
        i = 0
        while True:
            key = surf.get_at((i, 0))
            if key[3] != 0:
                break
            i += 1

        ci = 0

        # Find real characters, create them.
        while i < sw and ci < len(self.charset):

            if surf.get_at((i, 0)) != key:
                start = i
                i += 1

                while i < sw:
                    if surf.get_at((i, 0)) == key:
                        break

                    i += 1

                c = self.charset[ci]
                ci += 1

                ss = surf.subsurface((start, 0, i - start, height))
                ss = renpy.display.scale.surface_scale(ss)
                
                self.chars[c] = ss
                self.sizes[c] = i - start


            i += 1

def register_sfont(name=None, size=None, bold=False, italics=False, underline=False, 
                   filename=None, spacewidth=10, default_kern=0, kerns={},
                   charset=u"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"):
    """
    This registers an SFont with the given details. Please note that
    size, bold, italic, and underline are all advisory (used for matching), and
    do not change the appearance of the font.

    @param name: The name of the font being registered.
    @param size: The size of the font being registered.
    @param bold: The boldness of the font being registered.
    @param italics: The italicness of the font being registered.
    @param underline: The underline of the font being registered.

    @param filename: The file containing the sfont image.
    @param spacewidth: The width of a space character.
    @param default_kern: The default kern spacing between characters.
    @param kerns: A map from two-character strings to the kern that should
    be used between those characters.
    @param charset: The character set of the font. A string containing characters
    in the order in which they are found in the image.
    """
   
    if name is None or size is None or filename is None:
        raise Exception("When registering an SFont, the font name, font size, and filename are required.")

    sf = SFont(filename, spacewidth, default_kern, kerns, charset)
    fonts[(name, size, bold, italics, underline)] = sf



def load_ttf(fn, size, bold, italics, underline, expand):

    try:
        rv = pygame.font.Font(renpy.loader.load(fn), size)
        rv.set_bold(bold)
        rv.set_italic(italics)
    except:
        # Let's try to find the font on our own.
        fonts = [ i.strip().lower() for i in fn.split(",") ]

        pygame.sysfont.initsysfonts()

        rv = None

        for k, v in pygame.sysfont.Sysfonts.iteritems():
            for flags, ffn in v.iteritems():
                for i in fonts:
                    if ffn.lower().endswith(i):
                        rv = pygame.font.Font(ffn, size)
                        rv.set_bold(bold)
                        rv.set_italic(italics)
                        break
                if rv:
                    break
            if rv:
                break
        else:
            # Let pygame try to find the font for us.
            rv = pygame.font.SysFont(fn, size, bold, italics)

    rv.set_underline(underline)

    try:
        rv.set_expand(expand)
    except AttributeError:
        pass
    
    return rv
    

def get_font(origfn, size, origbold=False, origitalics=False, underline=False, expand=0):

    rv = font_cache.get((origfn, size, origbold, origitalics, underline, expand), None)
    if rv is not None:
        return rv

    t = (origfn, origbold, origitalics)
    fn, bold, italics = renpy.config.font_replacement_map.get(t, t)

    rv = fonts.get((fn, size, bold, italics, underline), None)
    if rv is not None:
        rv.load()
    else:
        try:
            rv = load_ttf(fn, size, bold, italics, underline, expand)
        except:
            if renpy.config.debug:
                raise
            raise Exception("Could not find font: %r" % ((fn, size, bold, italics, underline), ))

    font_cache[(origfn, size, origbold, origitalics, underline, expand)] = rv

    return rv

def free_memory():
    """
    Clears the font cache.
    """

    font_cache.clear()
