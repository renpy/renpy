# Copyright 2004-2006 PyTom <pytom@bishoujo.us>
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

import re
import renpy
import sys

# A list of text tags, mapping from the text tag prefix to if it
# requires a closing tag.
text_tags = dict(
    image=False,
    p=False,
    w=False,
    fast=False,
    b=True,
    i=True,
    u=True,
    a=True,
    plain=True,
    font=True,
    color=True,
    size=True)

# This contains a map from (fn, size, bold, italics, underline) to the
# unloaded font object corresponding to that specification. 
fonts = { }

# This contains a map from (fn, size, bold, italics, underline) to the
# loaded font object corresponding to that specification.
font_cache = { }


class SFont(object):

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
        surf = renpy.display.im.load_image(self.filename)
        self.surf = surf

        surf.lock()

        sw, sh = surf.get_size()
        height = sh - 1
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
                self.chars[c] = surf.subsurface((start, 1, i - start, height))
                self.sizes[c] = i - start


            i += 1

        surf.unlock()

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



def load_ttf(fn, size, bold, italics, underline):

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
    return rv
    

# TODO: Something sane if the font file can't be found.
def get_font(fn, size, bold=False, italics=False, underline=False):
    from renpy.loader import transfn

    if (fn, bold, italics) in renpy.config.font_replacement_map:
        fn, bold, italics = renpy.config.font_replacement_map[fn, bold, italics]

    if (fn, size, bold, italics, underline) in font_cache:
        return font_cache[(fn, size, bold, italics, underline)]

    rv = fonts.get((fn, size, bold, italics, underline), None)
    if rv is not None:
        rv.load()
    else:
        try:
            rv = load_ttf(fn, size, bold, italics, underline)
        except:
            if renpy.config.debug:
                raise
            raise Exception("Could not find font: %r" % ((fn, size, bold, italics, underline), ))

    font_cache[(fn, size, bold, italics, underline)] = rv

    return rv

def color(s):
    """
    This function converts a hexcode into a color/alpha tuple. Leading
    # marks are ignored. Colors can be rgb or rgba, with each element having
    either one or two digits. (So the strings can be 3, 4, 6, or 8 digits long,
    not including the optional #.) A missing alpha is interpreted as 255,
    fully opaque.

    For example, color('#123a') returns (17, 34, 51, 170), while
    color('c0c0c0') returns (192, 192, 192, 255).
    """

    if s[0] == '#':
        s = s[1:]

    if len(s) == 6:
        r = int(s[0]+s[1], 16)
        g = int(s[2]+s[3], 16)
        b = int(s[4]+s[5], 16)
        a = 255
    elif len(s) == 8:
        r = int(s[0]+s[1], 16)
        g = int(s[2]+s[3], 16)
        b = int(s[4]+s[5], 16)
        a = int(s[6]+s[7], 16)
    elif len(s) == 3:
        r = int(s[0], 16) * 0x11
        g = int(s[1], 16) * 0x11
        b = int(s[2], 16) * 0x11
        a = 255
    elif len(s) == 4:
        r = int(s[0], 16) * 0x11
        g = int(s[1], 16) * 0x11
        b = int(s[2], 16) * 0x11
        a = int(s[3], 16) * 0x11
    else:
        raise Exception("Argument to color() must be 3, 4, 6, or 8 hex digits long.")

    return (r, g, b, a)

class TextStyle(object):
    """
    This is used to represent the style of text that will be displayed
    on the screen.
    """

    def __init__(self, source=None):
        if source is not None:
            vars(self).update(vars(source))

        # Width cache.
        self.wcache = { }
        
    def update(self):
        self.f = get_font(self.font, self.size, self.bold, self.italic, self.underline)

    def get_font(self):
        return self.f

    def get_ascent(self):
        return self.f.get_ascent()

    def get_width(self, text):

        rv = self.wcache.get(text, None)
        if rv is None:
            rv = self.f.size(text)[0]
            self.wcache[rv] = text
        return rv

    def sizes(self, text):
        return self.get_width(text), self.f.get_ascent() - self.f.get_descent()

    def render(self, text, antialias, color, black_color, use_colors, time, at):

        if use_colors:
            color = self.color or color
            black_color = self.black_color or black_color
            
        font = self.f

        if isinstance(font, SFont):
            rv = font.render(text, antialias, color, black_color)

        else:
            r, g, b, a = color
            color = (r, g, b, 255)

            surf = font.render(text, antialias, color)

            if a != 255 and renpy.display.module.can_linmap:

                if not surf.get_masks()[3]:
                    surf = surf.convert_alpha()

                rv = pygame.Surface(surf.get_size(), surf.get_flags(), surf)

                renpy.display.module.linmap(surf, rv, 256, 256, 256, a + 1)
            
            else:
                rv = surf

        renpy.display.render.mutated_surface(rv)
        return rv, rv.get_size()

    def length(self, text):
        return len(text)
    
class WidgetStyle(object):
    """
    Represents the style of a widget.
    """

    def __init__(self, ts, widget, width, time):

        self.height = ts.sizes(" ")[1]
        self.ascent = ts.get_ascent()

        # The widget we will render.
        self.widget = widget
        self.owidth = width

        surf = renpy.display.render.render(widget, width, self.height, time, time)
        self.width, _ = surf.get_size()

    def update(self):
        pass

    def get_ascent(self):
        return self.ascent

    def get_width(self, widget):
        return self.width

    def sizes(self, widget):
        return self.width, self.height

    def render(self, widget, antialias, color, black_color, foreground, st, at):

        # If in the foreground
        if foreground:
            return renpy.display.render.render(widget, self.owidth, self.height, st, at), (self.width, self.height)
        else:
            return None, (self.width, self.height)
        
    def length(self, text):
        return 1

text_regexp = re.compile(ur"""(?x)
      (?P<space>[ \u200b])
    | \{(?P<tag>[^{}]+)\}
    | (?P<untag>\{\{)
    | (?P<newline>\n)
    | (?P<word>[^ \n\{]+)
    """)
    
def text_tokenizer(s, style):
    """
    This functions is used to tokenize text. It's called when laying
    out a Text widget, and is given the string that is the text of the
    widget, and the style associated with the widget.

    It's expected to yield some number of pairs. In each pair, the
    first element is the kind of token found, and the second element
    is the text corresponding to that token. The following token
    types are defined:

    "newline" -- A newline, which when encountered starts a new line.

    "word" -- A word of text. A line will never be broken inside of
    a word.

    "space" -- A space. Spaces are always placed on the current line,
    and will never be placed as the start of a line.
    
    "tag" -- A text tag. If encountered, the second element should be
    the name of the tag, without any enclosing braces.
    """

    for m in text_regexp.finditer(s):

        if m.group('space'):
            yield 'space', m.group('space')
        elif m.group('word'):
            yield 'word', m.group('word')
        elif m.group('tag'):
            yield 'tag', m.group('tag')
        elif m.group('untag'):
            yield 'word', '{'
        elif m.group('newline'):
            yield 'newline', m.group('newline')
    
def input_tokenizer(l, style, pauses=None):
    """
    This tokenizes the input into a list of lists of tokens, where
    each token is a pair giving the type of token and the text of the
    token.
    """

    if isinstance(l, basestring):
        l = [ l ]

    rv = [ ]
    
    for s in l:

        if isinstance(s, basestring):
            sl = [ ]
            for type, text in renpy.config.text_tokenizer(s, style):
                if type == "tag" and text == "p":
                    sl.append(("tag", "w"))
                    sl.append(("newline", "\n"))
                else:
                    sl.append((type, text))

            rv.append(sl)
                

        elif isinstance(s, renpy.display.core.Displayable):
            rv.append([ ("widget", s) ])
        
        else:
            raise Exception("Couldn't figure out how to tokenize " + repr(s))

    return rv


def layout_width(triples):
    """
    Returns the width of the given list of triples. Cache
    should be a dictionary, which is used to cache results.
    """

    rv = 0

    curts = None
    cur = None
            
    for type, ts, i in triples:
        if ts is not curts:
            if curts:
                rv += curts.get_width(cur)
            curts = ts
            cur = i
        else:
            cur += i

    if curts:
        rv += curts.get_width(cur)
    return rv
    

def greedy_text_layout(triples, width, style):
    """
    Breaks the text up into rows. 

    @param triples: The text to be laid out. This is a list of
    (type, text/widgetstyle, data) triples.

    @param width: The width we want to layout to.

    @param style: The style of the text widget.
    """
    
    lines = [ ]
    line = [ ]

    target = width - style.first_indent
    
    for triple in triples:

        type, ts, i = triple

        if type == "newline":
            lines.append(line)
            line = [ triple ]
            target = width - style.rest_indent

            continue

        if type == "space":
            if not line and lines:
                continue
            line.append(triple)
            continue

        else:
            if layout_width(line + [ triple ]) > target:
                lines.append(line)
                line = [ triple ]
                target = width - style.rest_indent
            else:
                line.append(triple)
                
    lines.append(line)

    # Remove trailing whitespace, except on the last line, where it
    # might be intentional.
    for l in lines[:-1]:
        if l and l[-1][0] == "space":
            l.pop()

    return lines


def subtitle_text_layout_core(triples, width, style, soft, n):

    sizecache = { }

    lines = [ ]
    line = [ ]

    target = width

    total = soft * n
    linesoft = total / n

    for triple in triples:

        type, ts, i = triple

        if type == "newline":
            raise Exception("Subtitles may not contain newlines.")

            continue

        if type == "space":
            if not line:
                continue
            line.append(triple)
            continue

        else:
            lw = layout_width(line + [ triple ])

            if lw > target:

                n -= 1
                if n > 0:

                    if line and line[-1][0] == "space":
                        line.pop()

                    total -= layout_width(line)
                    linesoft = total / n
                else:
                    linesoft = soft

                lines.append(line)
                line = [ triple ]
                target = width
            else:
                line.append(triple)

                if lw > linesoft:

                    n -= 1
                    if n > 0:
                        total -= lw
                        linesoft = total / n
                    else:
                        linesoft = soft

                    lines.append(line)
                    line = [ ]
                    target = width

    lines.append(line)

    # Remove trailing whitespace.
    for l in lines:
        if l and l[-1][0] == "space":
            l.pop()

        if l and l[0][0] == "space":
            l.pop(0)


    return lines


def subtitle_text_layout(triples, width, style):

    softwidth = style.subtitle_width
    if isinstance(softwidth, float):
        softwidth = int(softwidth * width)

    sumwidths = layout_width(triples)

    i = 1
    while sumwidths / i > min(width, softwidth):
        i += 1

    while True:
        rv = subtitle_text_layout_core(triples, width, style, sumwidths / i, i)
        if len(rv) == i:
            break
        i += 1

    return rv

def text_layout(triples, width, style):

    if style.layout == "subtitle":
        return subtitle_text_layout(triples, width, style)
    else:
        return greedy_text_layout(triples, width, style)


class Text(renpy.display.core.Displayable):
    """
    A displayable that can format and display text on the screen.
    """

    nosave = [ 'laidout', 'laidout_lineheights', 'laidout_linewidths',
               'laidout_width', 'laidout_height', 'laidout_start',
               'laidout_length', 'width', 'tokens', 'children',
               'child_pos']

    def after_setstate(self):
        self._update()

    def __init__(self, text, slow=False, slow_done=None,
                 slow_speed=None, slow_start=0, slow_abortable=False,
                 pause=None, tokenized=False, style='default', **properties):
        """
        @param text: The text that will be displayed on the screen.

        @param slow: If True, the text will be slowly typed onto the screen.

        @param style: A style that will be applied to the text.

        @param properties: Additional properties that are applied to the text.

        @param pause: If not None, then we display up to the pauseth pause (0-numbered.)

        @param slow_done: A callback that occurs when slow text is done.

        @param slow_speed: The speed of slow text. If none, it's taken from
        the preferences.

        @param slow_offset: The offset into the text to start the slow text.

        @param slow_abortable: If True, clicking aborts the slow text.

        @param tokenized: True if the text is already tokenized.

        """

        super(Text, self).__init__()

        self.text = text        
        self.style = renpy.style.Style(style, properties)
        self.pause = pause
        self.keep_pausing = False
        self.tokenized = tokenized

        self._update(redraw=False)

        self.slow = slow
        self.slow_done = slow_done
        self.slow_start = slow_start
        self.slow_speed = slow_speed
        self.slow_abortable = slow_abortable

        self.laidout = None
        self.child_pos = [ ]


    def set_text(self, new_text):
        """
        Changes the text display by this object to new_text.
        """

        self.text = new_text
        self._update()

    def set_style(self, style):
        """
        Changes the style assocated with this object.
        """

        self.style = style
        self._update()
        
    def _update(self, redraw=True):
        """
        This is called after this widget has been updated by
        set_text or set_style.
        """        

        self.laidout = None
        self.child_pos = [ ]
        
        if self.text:
            text = self.text
        else:
            text = u" "

        if not self.tokenized:
            self.tokens = input_tokenizer(text, self.style)
        else:
            self.tokens = self.text

        if self.pause is not None:
            pause = self.pause
            l = [ ]
            
            for i in self.tokens[0]:
                l.append(i)

                if i == ("tag", "w"):
                    if pause == 0:
                        self.keep_pausing |= True
                        break                    
                    else:
                        pause -= 1

            self.tokens[0] = l

        # Postprocess the tokens list to create widgets, as necessary.

        self.children = [ ]
        newtokens = [ ]
        
        for tl in self.tokens:
            ntl = [ ]

            tliter = iter(tl)

            for kind, i in tliter:


                if kind == "tag" and i.startswith("image="):

                    m = re.match(r'image=(.*)', i)

                    if not m:
                        raise Exception('Image tag %s could not be parsed.' % i)

                    i = renpy.display.im.image(m.group(1))
                    ntl.append(("widget", i))
                    self.children.append(i)
                    
                elif kind == "tag" and i.startswith("a="):

                    label_tokens  = [ ]

                    for kkind, ii in tliter:
                        if kkind == "tag" and ii == "/a":
                            break

                        label_tokens.append((kkind, ii))

                    def clicked(target=i[2:]):
                        return renpy.config.hyperlink_callback(target)

                    label = Text([ label_tokens ], tokenized=True, style='hyperlink_text')
                    i = renpy.display.behavior.Button(label, style='hyperlink', clicked=clicked, focus='hyperlinks')
                    ntl.append(("widget", i))
                    self.children.append(i)

                else:
                    if kind == "widget":
                        self.children.append(i)
                    
                    ntl.append((kind, i))

            newtokens.append(ntl)

        self.tokens = newtokens
                    
        if redraw:
            renpy.display.render.redraw(self, 0)


    def event(self, ev, x, y, st):
        """
        Space, Enter, or Click ends slow, if it's enabled.
        """

        if self.slow and self.slow_abortable and renpy.display.behavior.map_event(ev, "dismiss"):
            self.slow = False
            raise renpy.display.core.IgnoreEvent()

        for child, xo, yo in self.child_pos:
            rv = child.event(ev, x - xo, y - yo, st)
            if rv is not None:
                return rv

    def visit(self):
        return self.children

    def layout(self, width, time):
        """
        This lays out the text of this widget. It sets self.laidout,
        self.laidout_lineheights, self.laidout_width, and
        self.laidout_height.
        """

        if self.laidout and self.width == width:
            return

        # Set this, so caching works.
        self.width = width

        # We are building this list of triples, which will be passed
        # to text_layout.
        triples = [ ]

        # The default style.
        tsl = [ TextStyle() ]
        tsl[-1].font = self.style.font
        tsl[-1].size = self.style.size
        tsl[-1].bold = self.style.bold
        tsl[-1].italic = self.style.italic
        tsl[-1].underline = self.style.underline
        tsl[-1].color = None
        tsl[-1].black_color = None
        tsl[-1].update()


        if not self.text:
            text = " "
        else:
            text = self.text

        # for i in re.split(r'( |\{[^{}]+\}|\{\{|\n)', text):

        tokens = [ ]
        for l in self.tokens:
            tokens.extend(l)

        ti = iter(tokens)

        for kind, i in ti:

            # Newline.
            if kind == "newline":
                triples.append(("newline", tsl[-1], ""))                
                continue

            elif kind == "tag":

                # Are we closing a tag?
                if i.startswith("/"):

                    tsl.pop()

                    if not tsl:
                        raise Exception("Closing tag %s does not match an open tag." % i)

                    continue

                # Otherwise, we're opening a new tag.
                tsl.append(TextStyle(tsl[-1]))

                if i == "w":
                    # Automatically closes.
                    tsl.pop()

                elif i == "fast":
                    # Automatically closes.
                    tsl.pop()

                    triples.append(("start", tsl[-1], ""))
                    
                elif i == "b":
                    tsl[-1].bold = True
                    tsl[-1].update()

                elif i == "i":
                    tsl[-1].italic = True
                    tsl[-1].update()

                elif i == "u":
                    tsl[-1].underline = True
                    tsl[-1].update()

                elif i == "plain":
                    tsl[-1].bold = False
                    tsl[-1].italic = False
                    tsl[-1].underline = False
                    tsl[-1].update()

                elif i.startswith("font"):
                    m = re.match(r'font=(.*)', i)

                    if not m:
                        raise Exception('Font tag %s could not be parsed.' % i)

                    tsl[-1].font = m.group(1)
                    tsl[-1].update()

                elif i.startswith("size"):

                    m = re.match(r'size=(\+|-|)(\d+)', i)

                    if not m:
                        raise Exception('Size tag %s could not be parsed.' % i)

                    if m.group(1) == '+':
                        tsl[-1].size += int(m.group(2))
                    elif m.group(1) == '-':
                        tsl[-1].size -= int(m.group(2))
                    else:
                        tsl[-1].size = int(m.group(2))                    
                    tsl[-1].update()

                elif i.startswith("color"):

                    m = re.match(r'color=(\#?[a-fA-F0-9]+)', i)

                    if not m:
                        raise Exception('Color tag %s could not be parsed.' % i)

                    tsl[-1].color = color(m.group(1))
                    tsl[-1].update()
                    
                else:
                    raise Exception("Text tag %s was not recognized. Case and spacing matter here." % i)

                # Since the kind can change.
                if kind == "tag":
                    continue

            elif kind == "space":
                # Spaces always get appended to the end of a line. So they
                # will never show up at the start of a line, unless they're
                # after a newline or at the start of a string.

                triples.append(("space", tsl[-1], i))
                
                continue

            elif kind == "word":
                triples.append(("word", tsl[-1], i))


            elif kind == "widget":
                pass
            
            else:
                raise Exception("Unknown text token kind %s." % kind)

            if kind == "widget":

                wstyle = WidgetStyle(tsl[-1], i, width, time)
                triples.append(("word", wstyle, i))
                            
        # We're done matching tags.

        if len(tsl) != 1:
            Exception("A tag was left open at the end of the text.")


        # Give text_layout a list of triples, get back a list of lists of
        # triples, one per line.
        linetriples = renpy.config.text_layout(triples, width, self.style)


        # Now, we need to go through these lines, to generate the data
        # we need to render text.

        self.laidout = [ ]
        self.laidout_lineheights = [ ]
        self.laidout_linewidths = [ ]
        self.laidout_length = 0
        self.laidout_start = 0
        self.laidout_width = self.style.min_width
        self.laidout_height = 0

        # Add something to empty lines.
        for l in linetriples:
            if not l:
                l.append(('word', tsl[-1], ' '))

        for l in linetriples:

            line = [ ]
            oldts = None
            cur = None
            
            for kind, ts, i in l:

                if kind == "start":
                    self.laidout_start = self.laidout_length
                    continue

                try:
                    self.laidout_length += len(i)
                except:
                    self.laidout_length += ts.length(i)

                if ts is not oldts:
                    if oldts is not None:
                        line.append((oldts, cur))

                    oldts = ts
                    cur = i
                else:
                    cur += i

            if oldts:
                line.append((oldts, cur))

            width = 0
            height = 0

            for ts, i in line:

                # This is a special case to handle mostly-blank lines introduced
                # by newlines.
                if len(line) == 1 and i == "":
                    i = " "

                w, h = ts.sizes(i)

                width += w
                height = max(height, h)

            self.laidout.append(line)
            self.laidout_linewidths.append(width)
            self.laidout_lineheights.append(height)
            self.laidout_width = max(width, self.laidout_width)
            self.laidout_height += height + self.style.line_spacing

            # For the newline.
            self.laidout_length += 1


    def get_simple_length(self):
        """
        Returns a simple length of the text in the first segment of
        the tokens. Doesn't use the same algorithm as get_laidout_length,
        so isn't suitable for slow_start.
        """

        rv = 0

        for tl in self.tokens:
            for type, text in tl:
                if type == "newline":
                    rv += len(text)
                elif type == "word":
                    rv += len(text)
                elif type == "space":
                    rv += len(text)
                elif type == "widget":
                    rv += 1
                elif type == "tag" and text == "fast":
                    rv = 0

        return rv

    def get_keep_pausing(self):
        """
        If true, we have text beyond the pause number indicated.
        """

        return self.keep_pausing

    def get_laidout_length(self):
        """
        The (reasonably arbitrary) length this text field was laidout
        to. This can only be called after the text field was drawn
        (that is, after it has been on the screen for an interaction
        with the user. Otherwise, it returns sys.maxint.
        """

        if not self.laidout:
            import sys
            return sys.maxint

        return self.laidout_length

            

    def render_pass(self, r, offsets, color, black_color, user_colors, length, time, at, child_pos):
        """
        Renders the text to r at the offsets. Color is the base color,
        and user_colors controls if the user can override those colors.

        Returns True if all characters were rendered, or False if a
        length restriction stopped some from being rendered.
        """

        y = 0
        indent = self.style.first_indent
        rest_indent = self.style.rest_indent
        antialias = self.style.antialias
        line_spacing = self.style.line_spacing
        
        for line, line_height, line_width in zip(self.laidout, self.laidout_lineheights, self.laidout_linewidths):
            x = indent + self.style.text_align * (self.laidout_width - line_width)
            indent = rest_indent

            max_ascent = 0

            for ts, text in line:
                max_ascent = max(ts.get_ascent(), max_ascent)

            for ts, text in line:
                
                length -= ts.length(text)

                if length < 0:
                    if isinstance(text, (str, unicode)):
                        text = text[:length]
                    else:
                        return False

                surf, (sw, sh) = ts.render(text, antialias, color, black_color, user_colors, time, at)

                actual_y = y + max_ascent - ts.get_ascent()

                for xo, yo in offsets:

                    if surf:
                        r.blit(surf, (x + xo, actual_y + yo))

                    if not isinstance(text, (str, unicode)):
                        child_pos.append((text, x + xo, actual_y + yo))
                
                x = x + sw

                if length <= 0:
                    return False

            length -= 1

            y = y + line_height + line_spacing

        return True
            

    def render(self, width, height, st, at):

        speed = self.slow_speed or renpy.game.preferences.text_cps

        dslist = self.style.drop_shadow

        if dslist is None:
            dslist = [ ]
        elif not isinstance(dslist, list):
            dslist = [ dslist ]

        mindsx = 0
        mindsy = 0
        maxdsx = 0
        maxdsy = 0

        for dsx, dsy in dslist:
            mindsx = min(mindsx, dsx)
            mindsy = min(mindsy, dsy)
            maxdsx = max(maxdsx, dsx)
            maxdsy = max(maxdsy, dsy)

        # minds{x,y} are negative (or 0), maxds{x,y} are positive (or 0).
            
        self.layout(width + mindsx - maxdsx, st)
            
        if self.slow and speed:
            start = max(self.slow_start, self.laidout_start)
            length = start + int(st * speed)
        else:
            length = sys.maxint
            self.slow = False

            if self.slow_done:
                self.slow_done()

        rv = renpy.display.render.Render(self.laidout_width - mindsx + maxdsx, self.laidout_height - mindsy + maxdsy)

        if dslist:
            dsoffsets = [ (dsxo - mindsx, dsyo - mindsy) for dsxo, dsyo in dslist ]
            self.render_pass(rv, dsoffsets, self.style.drop_shadow_color, self.style.drop_shadow_color, False, length, st, at, [ ])

        self.child_pos = [ ]

        if self.render_pass(rv, [ (-mindsx, -mindsy) ], self.style.color, self.style.black_color, True, length, st, at, self.child_pos):
            if self.slow:
                self.slow = False
                if self.slow_done:
                    self.slow_done()

        if self.slow:
            renpy.display.render.redraw(self, 0)

        return rv


class ParameterizedText(object):
    """
    This can be used as an image. When used, this image is expected to
    have a single parameter, a string which is rendered as the image.
    """

    def __init__(self, style='default', **properties):
        self.style = style
        self.properties = properties

    def parameterize(self, name, parameters):

        if len(parameters) != 1:
            raise Exception("'%s' takes a single string parameter." %
                            ' '.join(name))

        param = parameters[0]
        string = renpy.python.py_eval(param)

        return Text(string, style=self.style, **self.properties)
        
    def predict(self, callback):
        return
    
# This checks the text tags in a string to be sure they are all matched, and
# properly nested. It returns an error message, or None if the line is okay.
def check_text_tags(s):
    tokens = renpy.config.text_tokenizer(s, None)

    tag_stack = [ ]

    for type, text in tokens:
        if type != "tag":
            continue

        # Closing tag.
        if text[0] == '/':
            if not tag_stack:
                return "Close text tag '%s' does not match an open text tag." % text

            if tag_stack[-1] != text[1:]:
                return "Close text tag '%s' does not match open text tag '%s'." % (text, tag_stack[-1])

            tag_stack.pop()
            continue
                
        # Strip off arguments for open tags.
        if text.find('=') != -1:
            text = text[:text.find('=')]
        
        if text not in text_tags:
            return "Text tag '%s' is not known." % text
        
        if text_tags[text]:
            tag_stack.append(text)

    if tag_stack:
        return "One or more text tags were left open at the end of the string: " + ", ".join([ "'" + i + "'" for i in tag_stack])

    return None
