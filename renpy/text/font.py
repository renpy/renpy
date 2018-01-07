# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

import pygame_sdl2 as pygame

try:
    import xml.etree.ElementTree as etree
except:
    pass

import renpy.display
import renpy.text.ftfont as ftfont
import renpy.text.textsupport as textsupport

ftfont.init()  # @UndefinedVariable

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)


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
            g = textsupport.Glyph()  # @UndefinedVariable

            g.character = ord(c)
            g.ascent = self.height
            g.line_spacing = self.height

            width = self.width.get(c, None)
            if width is None:
                raise Exception("Character {0!r} not found in image-based font.".format(c))

            g.width = self.width[c]
            g.advance = self.advance[c]

            rv.append(g)

        # Compute kerning.
        for i in range(len(s) - 1):
            kern = self.kerns.get(s[i] + s[i+1], self.default_kern)
            rv[i].advance += kern

        return rv

    def bounds(self, glyphs, bounds):
        return bounds

    def draw(self, target, xo, yo, color, glyphs, underline, strikethrough, black_color):

        if black_color is None:
            return

        for g in glyphs:
            c = unichr(g.character)

            cxo, cyo = self.offsets[c]
            x = g.x + xo + cxo
            y = g.y + yo + cyo - g.ascent

            char_surf = self.chars[c]

            if renpy.config.recolor_sfonts:
                if color != WHITE or black_color != BLACK:
                    new_surf = renpy.display.pgrender.surface(char_surf.get_size(), True)
                    renpy.display.module.twomap(char_surf, new_surf, color, black_color)

                    char_surf = new_surf

            target.blit(char_surf, (x, y))


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

        self.chars = { }  # W0201
        self.width = { }  # W0201
        self.advance = { }  # W0201
        self.offsets = { }  # W0201

        # Load in the image.
        surf = renpy.display.im.Image(self.filename).load(unscaled=True)

        sw, sh = surf.get_size()
        height = sh
        self.height = height  # W0201
        self.baseline = height  # W0201

        # Create space characters.
        self.chars[u' '] = renpy.display.pgrender.surface((self.spacewidth, height), True)
        self.width[u' '] = self.spacewidth
        self.advance[u' '] = self.spacewidth
        self.offsets[u' '] = (0, 0)

        self.chars[u'\u200b'] = renpy.display.pgrender.surface((0, height), True)
        self.width[u'\u200b'] = 0
        self.advance[u'\u200b'] = 0
        self.offsets[u'\u200b'] = (0, 0)

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

        self.chars = { }  # W0201
        self.width = { }  # W0201
        self.advance = { }  # W0201
        self.offsets = { }  # W0201

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

        self.height = height  # W0201
        self.baseline = height  # W0201

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

        self.chars[u'\u200b'] = renpy.display.pgrender.surface((0, height), True)
        self.width[u'\u200b'] = 0
        self.advance[u'\u200b'] = 0
        self.offsets[u'\u200b'] = (0, 0)


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

    map = dict(i.split("=", 1) for i in line[1:])  # @ReservedAssignment
    return line[0], map


class BMFont(ImageFont):

    def __init__(self, filename):
        super(BMFont, self).__init__()

        self.filename = filename

    def load(self):

        self.chars = { }  # W0201
        self.width = { }  # W0201
        self.advance = { }  # W0201
        self.offsets = { }  # W0201
        self.kerns = { }  # W0201
        self.default_kern = 0  # W0201

        pages = { }

        f = renpy.loader.load(self.filename)
        for l in f:

            kind, args = parse_bmfont_line(l)

            if kind == "common":
                self.height = int(args["lineHeight"])  # W0201
                self.baseline = int(args["base"])  # W0201
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

        self.chars[u'\u200b'] = renpy.display.pgrender.surface((0, self.height), True)
        self.width[u'\u200b'] = 0
        self.advance[u'\u200b'] = 0
        self.offsets[u'\u200b'] = (0, 0)


class ScaledImageFont(ImageFont):
    """
    Represents an imagefont scaled by a given factor.
    """

    def __init__(self, parent, factor):

        def scale(n):
            return int(round(n * factor))

        self.height = scale(parent.height)
        self.baseline = scale(parent.baseline)
        self.default_kern = scale(parent.default_kern)

        self.width = { k : scale(v) for k, v in parent.width.iteritems() }
        self.advance = { k : scale(v) for k, v in parent.advance.iteritems() }
        self.offsets = { k : (scale(v[0]), scale(v[1])) for k, v in parent.offsets.iteritems() }
        self.kerns = { k : scale(v) for k, v in parent.kerns.iteritems() }

        self.chars = { }

        for k, v in parent.chars.iteritems():
            w, h = v.get_size()
            nw = scale(w)
            nh = scale(h)
            self.chars[k] = renpy.display.scale.smoothscale(v, (nw, nh))


def register_sfont(name=None, size=None, bold=False, italics=False, underline=False,
                   filename=None, spacewidth=10, default_kern=0, kerns={},
                   charset=u"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"):
    """
    :doc: image_fonts

    This registers an SFont with the given details. Please note that size, bold,
    italic, and underline are all advisory (used for matching), and do not
    change the appearance of the font.

    `More information about SFont. <http://www.linux-games.com/sfont/>`_

    `name`
        The name of the font being registered, a string.

    `size`
        The size of the font being registered, an integer.

    `bold`
        The boldness of the font being registered, a boolean.

    `italics`
        The italicness of the font being registered, a boolean.

    `underline`
        An ignored parameter.

    `filename`
        The file containing the sfont image, a string.

    `spacewidth`
        The width of a space character, an integer in pixels.

    `default_kern`
        The default kern spacing between characters, in pixels.

    `kerns`
        A map from two-character strings to the kern that should be used between
        those characters.

    `charset` - The character set of the font. A string containing characters in
        the order in which they are found in the image. The default character
        set for a SFont is::

            ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
            @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _
            ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
    """

    if name is None or size is None or filename is None:
        raise Exception("When registering an SFont, the font name, font size, and filename are required.")

    sf = SFont(filename, spacewidth, default_kern, kerns, charset)
    image_fonts[(name, size, bold, italics)] = sf


def register_mudgefont(name=None, size=None, bold=False, italics=False, underline=False,
                       filename=None, xml=None, spacewidth=10, default_kern=0, kerns={}):
    """
    :doc: image_fonts

    This registers a MudgeFont with the given details. Please note that size,
    bold, italic, and underline are all advisory (used for matching), and do not
    change the appearance of the font.

    Please see the `MudgeFont home page <http://www.larryhastings.com/programming/mudgefont/>`_
    for the tool that creates MudgeFonts. Ren'Py assumes that character codes
    found in the MudgeFont xml file are unicode character numbers, and ignores
    negative character codes.

    `name`
        The name of the font being registered, a string.

    `size`
        The size of the font being registered, an integer.

    `bold`
        The boldness of the font being registered, a boolean.

    `italics`
        The italicness of the font being registered, a boolean.

    `underline`
        An ignored parameter.

    `filename`
        The file containing the MudgeFont image, a string. The image is usually
        a TGA file, but could be a PNG or other format that Ren'Py supports.

    `xml`
        The xml file containing information generated by the MudgeFont tool.

    `spacewidth`
        The width of a space character, an integer in pixels.

    `default_kern`
        The default kern spacing between characters, in pixels.

    `kerns`
        A map from two-character strings to the kern that should be used between
        those characters.
    """

    if name is None or size is None or filename is None or xml is None:
        raise Exception("When registering a Mudge Font, the font name, font size, filename, and xml filename are required.")

    mf = MudgeFont(filename, xml, spacewidth, default_kern, kerns)
    image_fonts[(name, size, bold, italics)] = mf


def register_bmfont(name=None, size=None, bold=False, italics=False, underline=False,
                    filename=None):
    """
    :doc: image_fonts

    This registers a BMFont with the given details. Please note that size, bold,
    italic, and underline are all advisory (used for matching), and do not
    change the appearance of the font.

    Please see the `BMFont home page <http://www.angelcode.com/products/bmfont/>`_
    for the tool that creates BMFonts. Ren'Py expects that the filename
    parameter will be to a file in the BMFont text format, that describes a
    32-bit font. The Alpha channel should contain the font information, while
    the Red, Green, and Blue channels should be set to one. The image files,
    kerning, and other control information is read out of the BMFont file.

    We recommend including Latin and General Punctuation as part of your BMFont,
    to ensure all of the Ren'Py interface can render.

    `name`
        The name of the font being registered, a string.

    `size`
        The size of the font being registered, an integer.

    `bold`
        The boldness of the font being registered, a boolean.

    `italics`
        The italicness of the font being registered, a boolean.

    `underline`
        An ignored parameter.

    `filename`
        The file containing BMFont control information.
    """

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

        if (not renpy.config.developer) or renpy.config.allow_sysfonts:

            # Let's try to find the font on our own.
            fonts = [ i.strip().lower() for i in fn.split(",") ]

            pygame.sysfont.initsysfonts()

            for v in pygame.sysfont.Sysfonts.itervalues():
                if v is not None:
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

    rv = ftfont.FTFace(font_file, index)  # @UndefinedVariable

    face_cache[orig_fn] = rv

    return rv


# Caches of fonts.
image_fonts = { }

# A cache of scaled image fonts.
scaled_image_fonts = { }

# A cache of scaled faces.
font_cache = { }

# The last_scale we last accessed fonts at. (Used to clear caches.)
last_scale = 1.0


def get_font(fn, size, bold, italics, outline, antialias, vertical, hinting, scale):

    # If the scale changed, invalidate caches of scaled fonts.
    global last_scale

    if (scale != 1.0) and (scale != last_scale):
        scaled_image_fonts.clear()
        font_cache.clear()
        last_scale = scale

    # Perform replacement.
    t = (fn, bold, italics)
    fn, bold, italics = renpy.config.font_replacement_map.get(t, t)

    # Image fonts.
    key = (fn, size, bold, italics)

    rv = image_fonts.get(key, None)
    if rv is not None:

        if scale != 1.0:
            if key in scaled_image_fonts:
                rv = scaled_image_fonts[key]
            else:
                rv = ScaledImageFont(rv, scale)
                scaled_image_fonts[key] = rv

        return rv

    # Check for a cached TTF.
    key = (fn, size, bold, italics, outline, antialias, vertical, hinting, scale)

    rv = font_cache.get(key, None)
    if rv is not None:
        return rv

    # Load a TTF.
    face = load_face(fn)
    rv = ftfont.FTFont(face, int(size * scale), bold, italics, outline, antialias, vertical, hinting)  # @UndefinedVariable

    font_cache[key] = rv

    return rv


def free_memory():
    """
    Clears the font cache.
    """

    scaled_image_fonts.clear()
    font_cache.clear()


def load_fonts():
    for i in image_fonts.itervalues():
        i.load()

    for i in renpy.config.preload_fonts:
        load_face(i)


class FontGroup(object):
    """
    :doc: font_group
    :args: ()

    A group of fonts that can be used as a single font.
    """

    def __init__(self):

        # A list of font names we know of.
        self.fonts = [ ]

        # A map from character to the index of the font it's part of.
        self.cache = { }

        # A list of (index, start, end) tuples.
        self.patterns = [ ]

    def add(self, font, start, end):
        """
        :doc: font_group

        Associates a range of characters with a `font`.

        `start`
            The start of the range. This may be a single-character string, or
            an integer giving a unicode code point.

        `end`
            The end of the range. This may be a single-character string, or an
            integer giving a unicode code point.

        When multiple .add() calls include the same character, the first call
        takes precedence.

        This returns the FontGroup, so that multiple calls to .add() can be
        chained together.
        """

        if not isinstance(start, int):
            start = ord(start)

        if not isinstance(end, int):
            end = ord(end)

        if end < start:
            raise Exception("In FontGroup.add, the start of a character range must be before the end of the range.")

        if font not in self.fonts:
            self.fonts.append(font)

        index = self.fonts.index(font)

        self.patterns.append((index, start, end))

        return self

    def segment(self, s):
        """
        Segments `s` into fonts. Generates (font, string) tuples.
        """

        mark = 0
        pos = 0

        old_index = 0

        cache = self.cache

        for c in s:

            index = cache.get(c, None)

            if index is None:
                n = ord(c)

                for index, start, end in self.patterns:
                    if start <= n <= end:
                        break
                else:
                    raise Exception("Character U+{0:04x} not found in FontGroup".format(n))

                cache[c] = index

            if index != old_index:
                if pos:
                    yield self.fonts[old_index], s[mark:pos]

                old_index = index
                mark = pos

            pos += 1

        yield self.fonts[old_index], s[mark:]
