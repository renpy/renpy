# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import pygame_sdl2 as pygame

try:
    import xml.etree.ElementTree as etree
except Exception:
    pass

import renpy
import renpy.text.ftfont as ftfont
import renpy.text.textsupport as textsupport

ftfont.init() # @UndefinedVariable

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)


def is_zerowidth(char):
    if char == 0x200b: # Zero-width space.
        return True

    if char == 0x200c: # Zero-width non-joiner.
        return True

    if char == 0x200d: # Zero-width joiner.
        return True

    if char == 0x2060: # Word joiner.
        return True

    if char == 0xfeff: # Zero width non-breaking space.
        return True

    return False


class ImageFont(object):

    # ImageFonts are expected to have the following fields defined by
    # a subclass:

    # Font global:
    # height - The line height, the height of each character cell.
    height = 0
    # kerns - The kern between each pair of characters.
    kerns = { } # type: dict[str, float]

    # default_kern - The default kern.
    default_kern = 0.0

    # baseline - The y offset of the font baseline.
    baseline = 0

    # Per-character:
    # width - The width of each character.
    width = {} # type: dict[str, float]

    # advance - The advance of each character.
    advance = {} # type: dict[str, float]

    # offsets - The x and y offsets of each character.
    offsets = { } # type: dict[str, tuple[int, int]]

    # chars - A map from a character to the surface containing that character.
    chars = { } # type: dict[str, pygame.surface.Surface]

    def glyphs(self, s):

        rv = [ ]

        if not s:
            return rv

        for c in s:
            g = textsupport.Glyph() # @UndefinedVariable

            g.character = ord(c)
            g.ascent = self.baseline
            g.line_spacing = self.height

            if not is_zerowidth(g.character):

                width = self.width.get(c, None)
                if width is None:
                    raise Exception("Character {0!r} not found in image-based font.".format(c))

                g.width = self.width[c]
                g.advance = self.advance[c]

            else:
                g.width = 0
                g.advance = 0

            rv.append(g)

        # Compute kerning.
        for i in range(len(s) - 1):
            kern = self.kerns.get(s[i] + s[i + 1], self.default_kern)
            rv[i].advance += kern

        return rv

    def bounds(self, glyphs, bounds):
        return bounds

    def draw(self, target, xo, yo, color, glyphs, underline, strikethrough, black_color):

        if black_color is None:
            return

        for g in glyphs:

            if not g.width:
                continue

            c = chr(g.character)

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
                 charset,
                 baseline=None):

        super(SFont, self).__init__()

        self.filename = filename
        self.spacewidth = spacewidth
        self.default_kern = default_kern
        self.kerns = kerns
        self.charset = charset
        self.baseline = baseline

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
        if self.baseline is None:
            self.baseline = height # W0201
        elif self.baseline < 0:
            # Negative value is the distance from the bottom (vs top)
            self.baseline = height + self.baseline # W0201

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

        self.chars = { } # W0201
        self.width = { } # W0201
        self.advance = { } # W0201
        self.offsets = { } # W0201

        # Load in the image.
        surf = renpy.display.im.Image(self.filename).load(unscaled=True)

        # Parse the xml file.
        with renpy.loader.load(self.xml) as f:
            tree = etree.fromstring(f.read())

        height = 0

        # Find each character.
        for e in tree.findall("char"):

            char = int(e.attrib["id"])
            if char < 0:
                continue

            c = chr(char)
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

    if not line:
        line = [ "" ]

    map = dict(i.split("=", 1) for i in line[1:]) # @ReservedAssignment
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

        with renpy.loader.load(self.filename) as f:
            for l in f:

                kind, args = parse_bmfont_line(l)

                if kind == "common":
                    self.height = int(args["lineHeight"]) # W0201
                    self.baseline = int(args["base"]) # W0201
                elif kind == "page":
                    pages[int(args["id"])] = renpy.display.im.Image(args["file"]).load(unscaled=True)
                elif kind == "char":
                    c = chr(int(args["id"]))
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
                elif kind == "kerning":
                    first = chr(int(args["first"]))
                    second = chr(int(args["second"]))
                    self.kerns[first + second] = int(args["amount"])

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
            return round(n * factor)

        self.height = scale(parent.height)
        self.baseline = scale(parent.baseline)
        self.default_kern = scale(parent.default_kern)

        self.width = { k : scale(v) for k, v in parent.width.items() }
        self.advance = { k : scale(v) for k, v in parent.advance.items() }
        self.offsets = { k : (scale(v[0]), scale(v[1])) for k, v in parent.offsets.items() }
        self.kerns = { k : scale(v) for k, v in parent.kerns.items() }

        self.chars = { }

        for k, v in parent.chars.items():
            w, h = v.get_size()
            nw = scale(w)
            nh = scale(h)
            self.chars[k] = renpy.display.scale.smoothscale(v, (nw, nh))


def register_sfont(name=None, size=None, bold=False, italics=False, underline=False,
                   filename=None, spacewidth=10, baseline=None, default_kern=0, kerns={},
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

    `baseline`
        The distance from the top of the font to the baseline (the invisible
        line letters sit on), an integer in pixels.  If this font is mixed with
        other fonts, their baselines will be aligned.  Negative values indicate
        distance from the bottom of the font instead, and ``None`` means the
        baseline equals the height (i.e., is at the very bottom of the font).

    `default_kern`
        The default kern spacing between characters, in pixels.

    `kerns`
        A map from two-character strings to the kern that should be used between
        those characters.

    `charset`
        The character set of the font. A string containing characters in
        the order in which they are found in the image. The default character
        set for a SFont is::

            ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
            @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \\ ] ^ _
            ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
    """

    if name is None or size is None or filename is None:
        raise Exception("When registering an SFont, the font name, font size, and filename are required.")

    sf = SFont(filename, spacewidth, default_kern, kerns, charset, baseline)
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

            for v in pygame.sysfont.Sysfonts.values(): # type: ignore
                if v is not None:
                    for _flags, ffn in v.items():
                        for i in fonts:
                            if ffn.lower().endswith(i):
                                font_file = open(ffn, "rb")
                                break

                        if font_file:
                            break

                if font_file:
                    break

    if font_file is None:
        raise Exception("Could not find font {0!r}.".format(orig_fn))

    rv = ftfont.FTFace(font_file, index, orig_fn) # @UndefinedVariable

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
    rv = ftfont.FTFont(face, int(size * scale), bold, italics, outline, antialias, vertical, hinting) # @UndefinedVariable

    font_cache[key] = rv

    return rv


def free_memory():
    """
    Clears the font cache.
    """

    scaled_image_fonts.clear()
    font_cache.clear()


def load_fonts():
    for i in image_fonts.values():
        i.load()

    for i in renpy.config.preload_fonts:
        load_face(i)


class FontGroup(object):
    """
    :doc: font_group
    :args: ()

    A group of fonts that can be used as a single font.
    """

    # For compatibility with older instances.
    char_map = dict()

    def __init__(self):

        # A map from character index to font name. None is used for
        # the default font.
        self.map = { }

        # A map from character number to character number, used to implement remap.
        self.char_map = { }

    def add(self, font, start, end, target=None, target_increment=False):
        """
        :doc: font_group

        Associates a range of characters with a `font`.

        `start`
            The start of the range. This may be a single-character string, or
            an integer giving a unicode code point. If start is None, then the
            font is used as the default.

        `end`
            The end of the range. This may be a single-character string, or an
            integer giving a unicode code point. This is ignored if start is
            None.

        `target`
            If given, associates the given range of characters with specific
            characters from the given font, depending on target_increment.
            This may be a single-character string, or an integer giving a
            unicode code point. This is ignored if the character had already
            been added.

        `target_increment`
            If True, the [start, end] range is mapped to the
            [target, target+end-start] range. If False, every character from the
            range is associated with the target character.

        When multiple .add() calls include the same character, the first call
        takes precedence.

        This returns the FontGroup, so that multiple calls to .add() can be
        chained together.
        """

        if start is None:

            if isinstance(font, FontGroup):
                for k, v in font.map.items():
                    if k not in self.map:
                        self.map[k] = v
            else:
                if None not in self.map:
                    self.map[None] = font

            return self

        if not isinstance(start, int):
            start = ord(start)

        if not isinstance(end, int):
            end = ord(end)

        if target and not isinstance(target, int):
            target = ord(target)

        if end < start:
            raise Exception("In FontGroup.add, the start of a character range must be before the end of the range.")

        for i in range(start, end + 1):
            if i not in self.map:
                self.map[i] = font

                if target is not None:
                    self.char_map[i] = target

                    if target_increment:
                        target += 1

        return self

    def remap(self, cha, target):
        """
        :doc: font_group

        Remaps one or a set of characters to a single target character.

        `cha`
            The character or characters to remap. This may be a single-character
            string, or an integer giving a unicode code point, or an iterable of
            either.

        `target`
            The character to remap to. This may be a single-character string, or
            an integer giving a unicode code point.

        Any given character having already been remapped (either with add or with
        remap) will be ignored. However, if the FontGroup has no default font, any
        given character must have been previously added.

        This method also returns the FontGroup, for the same reasons.
        """

        if isinstance(cha, (int)) or isinstance(cha, (str, bytes)) and len(cha) == 1:
            cha = (cha,)

        if not isinstance(target, int):
            target = ord(target)

        for i in cha:
            if not isinstance(i, int):
                i = ord(i)
            if not ((None in self.map) or (i in self.map)):
                raise Exception("Character U+{0:04x} has no font in this FontGroup".format(i))
            if not i in self.char_map:
                # means the character has not already been remapped
                self.char_map[i] = target

        return self

    def segment(self, s):
        """
        Segments `s` into fonts. Generates (font, string) tuples.
        """

        mark = 0
        pos = 0

        font = None
        old_font = None

        if self.char_map:
            s = [ ord(i) for i in s ]
            s = "".join(chr(self.char_map.get(i, i)) for i in s)

        for i, c in enumerate(s):

            n = ord(c)

            font = self.map.get(ord(c), None)

            if font is None:
                font = self.map.get(None, None)

                if font is None:
                    raise Exception("Character U+{0:04x} not found in FontGroup".format(n))

            if font != old_font:
                if pos:
                    yield old_font, s[mark:pos]

                old_font = font
                mark = pos

            pos += 1

        if font is not None:
            yield font, s[mark:]
