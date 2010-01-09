# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import xml.etree.ElementTree as etree

import _renpy_font
pygame.font = _renpy_font
    
import renpy

# This contains a map from (fn, size, bold, italics, underline) to the
# unloaded font object corresponding to that specification. 
fonts = { }

# This contains a map from (fn, size, bold, italics, underline) to the
# loaded font object corresponding to that specification.
font_cache = { }

class ImageFont(object):

    # ImageFonts are expected to have the following fields defined by
    # a subclass:

    # Font global:
    # height - The line height, the height of each character cell.
    # kerns - The kern between wach pair of characters.
    # default_kern - The default kern.
    # baseline - The y offset of the font baseline.

    # Per-character:
    # width - The width of each character.
    # advance - The advance of each character.
    # offsets - The x and y offsets of each character.
    # chars - A map from a character to the surface containing that character.
    
    def size(self, text):

        if not text:
            return (0, self.height)

        xoff, _ = self.offsets[text[0]]
        w = -xoff
        
        for a, b in zip(text, text[1:]):
            try:
                w += self.advance[a] + self.kerns.get(a + b, self.default_kern)
            except KeyError:
                raise Exception("Character %r not found in %s." % (a, type(self).__name__))
                
        w += self.width[text[-1]]

        return (w, self.height)
            
    def render(self, text, antialias, color, black_color=(0, 0, 0, 255), background=None):

        if not text:
            return renpy.display.pgrender.surface((0, self.height), True)

        xoff, _ = self.offsets[text[0]]
        x = -xoff
        y = 0

        surf = renpy.display.pgrender.surface(self.size(text), True)

        for a, b in zip(text, text[1:]):
            xoff, yoff = self.offsets[a]
            surf.blit(self.chars[a], (x + xoff, y + yoff))
            x += self.advance[a] + self.kerns.get(a + b, self.default_kern)

        xoff, yoff = self.offsets[text[-1]]
        surf.blit(self.chars[text[-1]], (x + xoff, y + yoff))

        if renpy.config.recolor_sfonts and \
               (color != (255, 255, 255, 255) or black_color != (0, 0, 0, 255)):

            newsurf = renpy.display.pgrender.surface(surf.get_size(), True)
            renpy.display.module.twomap(surf, newsurf, color, black_color)

            surf = newsurf

        renpy.display.render.mutated_surface(surf)
        return surf

    def get_linesize(self):
        return self.height + 10

    def get_height(self):
        return self.height

    def get_ascent(self):
        return self.baseline

        
    def get_descent(self):
        return -(self.height - self.baseline)

class SFont(ImageFont):

    def __init__(self,
                 filename,
                 spacewidth,
                 default_kern,
                 kerns,
                 charset):

        super(SFont, self).__init__()
        
        self.filename = filename
        self.spacewidth = spacewidth
        self.default_kern = default_kern
        self.kerns = kerns
        self.charset = charset

    def load(self):

        self.chars = { } # W0201
        self.width = { } # W0201
        self.advance = { } # W0201
        self.offsets = { } # W0201
        
        # Load in the image.
        surf = renpy.display.im.Image(self.filename).load(unscaled=True)

        sw, sh = surf.get_size()
        height = sh
        self.height = height # W0201
        self.baseline = height # W0201
        
        # Create space characters.
        self.chars[u' '] = renpy.display.pgrender.surface((self.spacewidth, height), True)
        self.width[u' '] = self.spacewidth
        self.advance[u' '] = self.spacewidth
        self.offsets[u' '] = (0, 0)

        self.chars[u'\u00a0'] = self.chars[u' ']
        self.width[u'\u00a0'] = self.width[u' ']
        self.advance[u'\u00a0'] = self.advance[u' ']
        self.offsets[u'\u00a0'] = self.offsets[u' ']
        
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
                self.width[c] = i - start
                self.advance[c] = i - start
                self.offsets[c] = (0, 0)

            i += 1


class MudgeFont(ImageFont):

    def __init__(self,
                 filename,
                 xml,
                 spacewidth,
                 default_kern,
                 kerns):

        super(MudgeFont, self).__init__()
        
        self.filename = filename
        self.xml = xml
        self.spacewidth = spacewidth
        self.default_kern = default_kern
        self.kerns = kerns

    def load(self):

        self.chars = { } # W0201
        self.width = { } # W0201
        self.advance = { } # W0201
        self.offsets = { } # W0201
        
        # Load in the image.
        surf = renpy.display.im.Image(self.filename).load(unscaled=True)

        # Parse the xml file.
        tree = etree.fromstring(renpy.loader.load(self.xml).read())

        height = 0
        
        # Find each character.
        for e in tree.findall("char"):

            char = int(e.attrib["id"])
            if char < 0:
                continue

            c = unichr(char)
            x = int(e.attrib["x"])
            y = int(e.attrib["y"])
            w = int(e.attrib["width"])
            h = int(e.attrib["height"])

            ss = surf.subsurface((x, y, w, h))
            ss = renpy.display.scale.surface_scale(ss)
                
            self.chars[c] = ss
            self.width[c] = w
            self.advance[c] = w
            self.offsets[c] = (0, 0)
                        
            height = max(height, h)
        
        self.height = height # W0201
        self.baseline = height # W0201
        
        # Create space characters.
        if u' ' not in self.chars:
            self.chars[u' '] = renpy.display.pgrender.surface((self.spacewidth, height), True)
            self.width[u' '] = self.spacewidth
            self.advance[u' '] = self.spacewidth
            self.offsets[u' '] = (0, 0)
            
            
        if u'\u00a0' not in self.chars:
            self.chars[u'\u00a0'] = self.chars[u' ']
            self.width[u'\u00a0'] = self.width[u' ']
            self.advance[u'\u00a0'] = self.advance[u' ']
            self.offsets[u'\u00a0'] = self.offsets[u' ']

def parse_bmfont_line(l):
    w = ""
    line = [ ]
    
    quote = False
    
    for c in l:
        if c == "\r" or c == "\n":
            continue
        
        if c == " " and not quote:
            if w:
                line.append(w)
                w = ""
            continue

        if c == "\"":
            quote = not quote
            continue

        w += c

    if w:
        line.append(w)

    map = dict(i.split("=", 1) for i in line[1:])
    return line[0], map
            
class BMFont(ImageFont):

    def __init__(self, filename):
        super(BMFont, self).__init__()
        
        self.filename = filename

    def load(self):

        self.chars = { } # W0201
        self.width = { } # W0201
        self.advance = { } # W0201
        self.offsets = { } # W0201
        self.kerns = { } # W0201
        self.default_kern = 0 # W0201
        
        pages = { }

        f = renpy.loader.load(self.filename)
        for l in f:

            kind, args = parse_bmfont_line(l)
            
            if kind == "common":
                self.height = int(args["lineHeight"]) # W0201
                self.baseline = int(args["base"]) # W0201
            elif kind == "page":
                pages[int(args["id"])] = renpy.display.im.Image(args["file"]).load(unscaled=True)
            elif kind == "char":
                c = unichr(int(args["id"]))
                x = int(args["x"])
                y = int(args["y"])
                w = int(args["width"])
                h = int(args["height"])
                xo = int(args["xoffset"])
                yo = int(args["yoffset"])
                xadvance = int(args["xadvance"])
                page = int(args["page"])

                ss = pages[page].subsurface((x, y, w, h))
                ss = renpy.display.scale.surface_scale(ss)

                self.chars[c] = ss
                self.width[c] = w + xo
                self.advance[c] = xadvance
                self.offsets[c] = (xo, yo)
                
        f.close()
        
        if u'\u00a0' not in self.chars:
            self.chars[u'\u00a0'] = self.chars[u' ']
            self.width[u'\u00a0'] = self.width[u' ']
            self.advance[u'\u00a0'] = self.advance[u' ']
            self.offsets[u'\u00a0'] = self.offsets[u' ']
            
            
def register_sfont(name=None, size=None, bold=False, italics=False, underline=False, 
                   filename=None, spacewidth=10, default_kern=0, kerns={},
                   charset=u"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"):

    if name is None or size is None or filename is None:
        raise Exception("When registering an SFont, the font name, font size, and filename are required.")

    sf = SFont(filename, spacewidth, default_kern, kerns, charset)
    fonts[(name, size, bold, italics, underline)] = sf


def register_mudgefont(name=None, size=None, bold=False, italics=False, underline=False, 
                   filename=None, xml=None, spacewidth=10, default_kern=0, kerns={}):
   
    if name is None or size is None or filename is None or xml is None:
        raise Exception("When registering a Mudge Font, the font name, font size, filename, and xml filename are required.")

    mf = MudgeFont(filename, xml, spacewidth, default_kern, kerns)
    fonts[(name, size, bold, italics, underline)] = mf

def register_bmfont(name=None, size=None, bold=False, italics=False, underline=False, 
                    filename=None):

    bmf = BMFont(filename)
    fonts[(name, size, bold, italics, underline)] = bmf

def load_ttf(fn, size, bold, italics, underline, expand):

    # Figure out the font index.
    index = 0

    if "@" in fn:
        index, fn = fn.split("@", 1)
        index = int(index)
    
    try:
        f = renpy.loader.load(fn)
        rv = _renpy_font.Font(f, size, index)

        rv.set_bold(bold)
        rv.set_italic(italics)

    except IOError:
        
        # Let's try to find the font on our own.
        fonts = [ i.strip().lower() for i in fn.split(",") ]

        pygame.sysfont.initsysfonts()

        rv = None

        for k, v in pygame.sysfont.Sysfonts.iteritems():
            for flags, ffn in v.iteritems():
                for i in fonts:
                    if ffn.lower().endswith(i):
                        rv = _renpy_font.Font(ffn, size, index)
                        rv.set_bold(bold)
                        rv.set_italic(italics)
                        break
                if rv:
                    break
            if rv:
                break
        else:
            # Let pygame try to find the font for us.
            rv = pygame.sysfont.SysFont(fn, size, bold, italics)

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
            renpy.game.exception_info = "Finding font: %r" % ((fn, size, bold, italics, underline),)
            raise

    font_cache[(origfn, size, origbold, origitalics, underline, expand)] = rv

    return rv

def free_memory():
    """
    Clears the font cache.
    """

    font_cache.clear()
