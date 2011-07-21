# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

try:
    import xml.etree.ElementTree as etree
except:
    pass
    
import renpy.display
import renpy.text.ftfont as ftfont
import renpy.text.textsupport as textsupport

ftfont.init()

class ImageFont(object):

    # ImageFonts are expected to have the following fields defined by
    # a subclass:

    # Font global:
    # height - The line height, the height of each character cell.
    # kerns - The kern between each pair of characters.
    # default_kern - The default kern.
    # baseline - The y offset of the font baseline.

    # Per-character:
    # width - The width of each character.
    # advance - The advance of each character.
    # offsets - The x and y offsets of each character.
    # chars - A map from a character to the surface containing that character.
    
    
    def glyphs(self, s):
        
        rv = [ ]
        
        if not s:
            return rv
        
        for c in s:
            g = textsupport.Glyph()
            
            g.character = ord(c)
            g.ascent = self.height
            g.line_spacing = self.height

            width = self.width.get(c, None)
            if width is None:
                raise Exception("Character {0!r} not found in image-based font.".format(c))
            
            g.width = self.width[c]
            g.advance = self.width[c]
            
            rv.append(g)
            
        # TODO: Kerning.
        
        return rv
    
    def draw(self, target, xo, yo, color, glyphs, underline, strikethrough):
        
        for g in glyphs:
            c = unichr(g.character)
            
            cxo, cyo = self.offsets[c]
            x = g.x + xo + cxo
            y = g.y + yo + cyo - g.ascent
            
            # TODO: Tinting as necessary.
            
            target.blit(self.chars[c], (x, y))

#===============================================================================
#    
#    def size(self, text):
# 
#        if not text:
#            return (0, self.height)
# 
#        xoff, _ = self.offsets[text[0]]
#        w = -xoff
#        
#        for a, b in zip(text, text[1:]):
#            try:
#                w += self.advance[a] + self.kerns.get(a + b, self.default_kern)
#            except KeyError:
#                raise Exception("Character %r not found in %s." % (a, type(self).__name__))
#                
#        w += self.width[text[-1]]
# 
#        return (w, self.height)
#            
#    def render(self, text, antialias, color, black_color=(0, 0, 0, 255), background=None):
# 
#        if not text:
#            return renpy.display.pgrender.surface((0, self.height), True)
# 
#        xoff, _ = self.offsets[text[0]]
#        x = -xoff
#        y = 0
# 
#        surf = renpy.display.pgrender.surface(self.size(text), True)
# 
#        for a, b in zip(text, text[1:]):
#            xoff, yoff = self.offsets[a]
#            surf.blit(self.chars[a], (x + xoff, y + yoff))
#            x += self.advance[a] + self.kerns.get(a + b, self.default_kern)
# 
#        xoff, yoff = self.offsets[text[-1]]
#        surf.blit(self.chars[text[-1]], (x + xoff, y + yoff))
# 
#        if renpy.config.recolor_sfonts and \
#               (color != (255, 255, 255, 255) or black_color != (0, 0, 0, 255)):
# 
#            newsurf = renpy.display.pgrender.surface(surf.get_size(), True)
#            renpy.display.module.twomap(surf, newsurf, color, black_color)
# 
#            surf = newsurf
# 
#        renpy.display.render.mutated_surface(surf)
#        return surf
# 
#    def get_linesize(self):
#        return self.height + 10
# 
#    def get_height(self):
#        return self.height
# 
#    def get_ascent(self):
#        return self.baseline
# 
#        
#    def get_descent(self):
#        return -(self.height - self.baseline)
#===============================================================================

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
    image_fonts[(name, size, bold, italics)] = sf

def register_mudgefont(name=None, size=None, bold=False, italics=False, underline=False, 
                   filename=None, xml=None, spacewidth=10, default_kern=0, kerns={}):
   
    if name is None or size is None or filename is None or xml is None:
        raise Exception("When registering a Mudge Font, the font name, font size, filename, and xml filename are required.")

    mf = MudgeFont(filename, xml, spacewidth, default_kern, kerns)
    image_fonts[(name, size, bold, italics)] = mf

def register_bmfont(name=None, size=None, bold=False, italics=False, underline=False, 
                    filename=None):

    bmf = BMFont(filename)
    image_fonts[(name, size, bold, italics)] = bmf

# A map from face name to ftfont.FTFace
face_cache = { }

def load_face(fn):

    if fn in face_cache:
        return face_cache[fn]

    orig_fn = fn

    # Figure out the font index.
    index = 0

    if "@" in fn:
        index, fn = fn.split("@", 1)
        index = int(index)
    
    font_file = None
    
    try:
        font_file = renpy.loader.load(fn)
    except IOError:
        
        # Let's try to find the font on our own.
        fonts = [ i.strip().lower() for i in fn.split(",") ]

        pygame.sysfont.initsysfonts()

        for v in pygame.sysfont.Sysfonts.itervalues():
            for _flags, ffn in v.iteritems():
                for i in fonts:
                    if ffn.lower().endswith(i):
                        font_file = file(ffn, "rb")
                        break
            
                if font_file:
                    break

            if font_file:
                break

            
    if font_file is None:
        raise Exception("Could not find font {0!r}.".format(orig_fn))
    
    rv = ftfont.FTFace(font_file, index)
    
    face_cache[orig_fn] = rv
    
    return rv
    
# Caches of fonts.
image_fonts = { }
font_cache = { }


loaded = False


def get_font(fn, size, bold, italics, outline, antialias):
    
    t = (fn, bold, italics)
    fn, bold, italics = renpy.config.font_replacement_map.get(t, t)

    # TODO: Move to an init method.
    global loaded
    for i in image_fonts.itervalues():
        i.load()

    rv = image_fonts.get((fn, size, bold, italics), None)
    if rv is not None:
        return rv

    key = (fn, size, bold, italics, outline, antialias)
    rv = font_cache.get(key, None)
    if rv is not None:
        return rv
    
    # If we made it here, we need to load a ttf.
    face = load_face(fn)

    rv = ftfont.FTFont(face, size, bold, italics, outline, antialias)
    
    font_cache[key] = rv
    
    return rv

def free_memory():
    """
    Clears the font cache.
    """

    font_cache.clear()
    face_cache.clear()
    
