import pygame
from pygame.constants import *

import re
import renpy
import sys

_font_cache = { }

# TODO: Something sane if the font file can't be found.
def get_font(fn, size, bold=False, italics=False, underline=False):
    from renpy.loader import transfn

    if (fn, bold, italics) in renpy.config.font_replacement_map:
        fn, bold, italics = renpy.config.font_replacement_map[fn, bold, italics]

    if (fn, size, bold, italics, underline) in _font_cache:
        return _font_cache[(fn, size, bold, italics, underline)]

    try:
        rv = pygame.font.Font(transfn(fn), size)
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

    _font_cache[(fn, size, bold, italics, underline)] = rv

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

    def get_font(self):
        return get_font(self.font, self.size, self.bold, self.italic, self.underline)

    def get_ascent(self):
        return self.get_font().get_ascent()
    
    def sizes(self, text):
        font = self.get_font()
        # print font.get_ascent() - font.get_descent(), font.get_height(), font.get_linesize()
        return font.size(text)[0], font.get_ascent() - font.get_descent()

    def render(self, text, antialias, color, use_colors, time):

        if use_colors and self.color:
            color = self.color

        r, g, b, a = color
        color = (r, g, b, 255)

        font = self.get_font()

        surf = font.render(text, antialias, color)

        if a != 255 and renpy.display.module.can_map:

            if not surf.get_masks()[3]:
                surf = surf.convert_alpha()

            rv = pygame.Surface(surf.get_size(), surf.get_flags(), surf)
            alpha = renpy.display.im.ramp(0, a)
            identity = renpy.display.im.identity

            renpy.display.module.map(surf, rv, identity, identity, identity, alpha)
            
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

        surf = renpy.display.render.render(widget, self.height, width, time)
        self.width, _ = surf.get_size()

    def get_ascent(self):
        return self.ascent

    def sizes(self, widget):
        return self.width, self.height

    def render(self, widget, antialias, color, foreground, time):

        # If in the foreground
        if foreground:
            return renpy.display.render.render(widget, self.owidth, self.height, time), (self.width, self.height)
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

class Text(renpy.display.core.Displayable):
    """
    A displayable that can format and display text on the screen.
    """

    nosave = [ 'laidout', 'laidout_lineheights', 'laidout_linewidths',
               'laidout_width', 'laidout_height', 'laidout_start',
               'laidout_length', 'width', 'tokens' ]

    def after_setstate(self):
        self._update()

    def __init__(self, text, slow=False, slow_done=None,
                 slow_speed=None, slow_start=0, slow_abortable=False,
                 pause=None, style='default', **properties):
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

        """

        super(Text, self).__init__()

        self.text = text        
        self.style = renpy.style.Style(style, properties)
        self.pause = pause
        self.keep_pausing = False

        self._update(redraw=False)

        self.slow = slow
        self.slow_done = slow_done
        self.slow_start = slow_start
        self.slow_speed = slow_speed
        

        self.laidout = None

    def get_placement(self):
        return self.style

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

        if self.text:
            text = self.text
        else:
            text = " "

        self.tokens = input_tokenizer(text, self.style)

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

        if redraw:
            renpy.display.render.redraw(self, 0)

    def event(self, ev, x, y):
        """
        Space, Enter, or Click ends slow, if it's enabled.
        """

        if not self.slow:
            return None

        if not self.slow_abortable:
            return None

        if renpy.display.behavior.map_event(ev, "dismiss"):

            self.slow = False
            raise renpy.display.core.IgnoreEvent()

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

        def indent():
            if lines:
                return self.style.rest_indent
            else:
                return self.style.first_indent


        tsl = [ TextStyle() ]
        tsl[-1].font = self.style.font
        tsl[-1].size = self.style.size
        tsl[-1].bold = self.style.bold
        tsl[-1].italic = self.style.italic
        tsl[-1].underline = self.style.underline
        tsl[-1].color = None

        lines = [ ]
        line = [ ]

        # The height of the current line, in pixels, not including
        # line_spacing.
        lineheight = 0

        # A list of same.
        lineheights = [ ]

        # The width of the current line.
        linewidth = 0

        # A list of the same.
        linewidths = [ ]

        # The maximum linewidth.
        maxwidth = 0

        # The length of the laidout text.
        laidout_length = 0

        # Where we should start the slow effect from on the laidout text.
        laidout_start = 0

        # The current text.
        cur = ""

        # The width, in pixels, of cur.
        curwidth = 0

        # The remaining width of the line, not including the text in
        # cur.
        remwidth = width - indent()

        if not self.text:
            text = " "
        else:
            text = self.text

        # for i in re.split(r'( |\{[^{}]+\}|\{\{|\n)', text):

        tokens = [ ]
        for l in self.tokens:
            tokens.extend(l)

        for kind, i in tokens:

            # Newline.
            if kind == "newline":

                if cur:
                    line.append((TextStyle(tsl[-1]), cur))                    
                    maxwidth = max(maxwidth, linewidth + curwidth)
                    cur = ""
                
                lines.append(line)
                lineheights.append(lineheight)
                linewidths.append(curwidth)
                
                line = [ ]
                linewidth = 0
                curwidth, lineheight = tsl[-1].sizes(" ")
                remwidth = width - indent()

                continue

            elif kind == "tag":

                # Are we closing a tag?
                if i.startswith("/"):
                    if cur:
                        line.append((TextStyle(tsl[-1]), cur))
                        cur = ""
                        remwidth -= curwidth
                        linewidth += curwidth
                        curwidth = 0

                    tsl.pop()

                    if not tsl:
                        raise Exception("Closing tag %s does not match an open tag." % i)

                    continue

                # Otherwise, we're opening a new tag.

                # Mark up any text that uses an old style.
                if cur:
                    line.append((TextStyle(tsl[-1]), cur))
                    cur = ""
                    remwidth -= curwidth
                    linewidth += curwidth
                    curwidth = 0

                tsl.append(TextStyle(tsl[-1]))

                if i == "w":
                    # Automatically closes.
                    tsl.pop()

                elif i == "fast":
                    # Automatically closes.
                    tsl.pop()

                    laidout_start = laidout_length
                    
                elif i == "b":
                    tsl[-1].bold = True

                elif i == "i":
                    tsl[-1].italic = True

                elif i == "u":
                    tsl[-1].underline = True

                elif i == "plain":
                    tsl[-1].bold = False
                    tsl[-1].italic = False
                    tsl[-1].underline = False

                elif i.startswith("font"):
                    m = re.match(r'font=(.*)', i)

                    if not m:
                        raise Exception('Font tag %s could not be parsed.' % i)

                    tsl[-1].font = m.group(1)

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

                elif i.startswith("color"):

                    m = re.match(r'color=(\#?[a-fA-F0-9]+)', i)

                    if not m:
                        raise Exception('Color tag %s could not be parsed.' % i)

                    tsl[-1].color = color(m.group(1))

                elif i.startswith("image"):

                    m = re.match(r'image=(.*)', i)

                    if not m:
                        raise Exception('Image tag %s could not be parsed.' % i)

                    kind = "widget"
                    i = renpy.display.im.image(m.group(1))

                    # The tag automatically closes.
                    tsl.pop()
                    
                else:
                    raise Exception("Text tag %s was not recognized. Case and spacing matter here." % i)

                # Since the kind can change.
                if kind == "tag":
                    continue

            elif kind == "space":
                # Spaces always get appended to the end of a line. So they
                # will never show up at the start of a line, unless they're
                # after a newline or at the start of a string.

                cur += i
                curwidth, lh = tsl[-1].sizes(cur)
                lineheight = max(lh, lineheight)

                laidout_length += len(i)
                
                continue

            elif kind == "word":

                # If we made it here, then we have normal text.

                laidout_length += len(i)

                # We must have at least one word or something else in the
                # line before we care about wrapping.
                if not cur and not line:
                    cur = i                
                    curwidth, lineheight = tsl[-1].sizes(cur)
                    continue

                # Should we wrap?
                oldcurwidth = curwidth
                curwidth, lh = tsl[-1].sizes(cur + i)

                if curwidth > remwidth:
                    line.append((TextStyle(tsl[-1]), cur))
                    lines.append(line)

                    maxwidth = max(maxwidth, linewidth)

                    line = [ ]
                    lineheights.append(lineheight)

                    linewidths.append(width + oldcurwidth - remwidth)

                    cur = i
                    curwidth, lineheight = tsl[-1].sizes(cur)                
                    remwidth = width - indent()
                    linewidth = 0
                else:
                    cur = cur + i
                    lineheight = max(lh, lineheight)


                continue

            elif kind == "widget":
                pass
            
            else:
                raise Exception("Unknown text token kind %s." % kind)

            if kind == "widget":

                laidout_length += 1

                # Here, we have a widget that we can render.

                # Close off an existing line, if it's open.
                if cur:

                    line.append((TextStyle(tsl[-1]), cur))
                    cur = ""
                    remwidth -= curwidth
                    linewidth += curwidth
                    curwidth = 0

                wstyle = WidgetStyle(tsl[-1], i, width, time)
                wwidth, wheight = wstyle.sizes(i)

                # If we're bigger then the remaining width on a non-empty line.
                if line and wwidth > remwidth:
                    lines.append(line)
                    maxwidth = max(maxwidth, linewidth)
                    lineheights.append(lineheight)
                    linewidths.append(width - remwidth)
                    
                    line = [ (wstyle, i) ]

                    remwidth = width - indent() - wwidth
                    linewidth = wwidth
                    lineheight = wheight

                else:
                    line.append((wstyle, i))
                    linewidth -= wwidth
                    lineheight = max(lineheight, wheight)

            

        # We're done. Let's close up.

        if len(tsl) != 1:
            exception("A tag was left open at the end of the text.")
            
        if cur:
            line.append((tsl[-1], cur))
            maxwidth = max(maxwidth, curwidth)

        if line:
            lines.append(line)
            lineheights.append(lineheight)
            linewidths.append(linewidth + curwidth)

        laidout_length += len(lines)

        self.laidout = lines
        self.laidout_lineheights = lineheights
        self.laidout_linewidths = linewidths
        self.laidout_width = max(max(linewidths), self.style.minwidth)
        self.laidout_height = sum(lineheights) + len(lineheights) * self.style.line_spacing
        self.laidout_length = laidout_length
        self.laidout_start = laidout_start

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

            

    def render_pass(self, r, xo, yo, color, user_colors, length, time):
        """
        Renders the text to r at xo, yo. Color is the base color,
        and user_colors controls if the user can override those colors.

        Returns True if all characters were rendered, or False if a
        length restriction stopped some from being rendered.
        """

        y = yo
        indent = self.style.first_indent
        rest_indent = self.style.rest_indent
        antialias = self.style.antialias
        line_spacing = self.style.line_spacing
        
        for line, line_height, line_width in zip(self.laidout, self.laidout_lineheights, self.laidout_linewidths):
            x = xo + indent + self.style.textalign * (self.laidout_width - line_width)
            indent = rest_indent

            max_ascent = 0

            for ts, text in line:
                max_ascent = max(ts.get_ascent(), max_ascent)

            for ts, text in line:
                
                length -= ts.length(text)

                if length < 0:
                    text = text[:length]
                
                surf, (sw, sh) = ts.render(text, antialias, color, user_colors, time)
                # sw, sh = surf.get_size()

                if surf:
                    r.blit(surf, (x, y + max_ascent - ts.get_ascent()))

                x = x + sw

                if length <= 0:
                    return False

            length -= 1

            y = y + line_height + line_spacing

        return True
            
    def render(self, width, height, st):

        speed = self.slow_speed or renpy.game.preferences.text_cps


        if self.style.drop_shadow:
            dsxo, dsyo = self.style.drop_shadow

            absxo = abs(dsxo)
            absyo = abs(dsyo)

            width -= absxo

            if dsxo < 0:
                xo = -dsxo
                dsxo = 0
            else:
                xo = 0

            if dsyo < 0:
                yo = -dsyo
                dsyo = 0
            else:
                yo = 0
        else:
            absxo = 0
            absyo = 0
            dsxo = 0
            dsyo = 0
            xo = 0
            yo = 0

                
        self.layout(width - absxo, st)
            
        if self.slow and speed:
            start = max(self.slow_start, self.laidout_start)
            length = start + int(st * speed)
        else:
            length = sys.maxint
            self.slow = False

            if self.slow_done:
                self.slow_done()

        rv = renpy.display.render.Render(self.laidout_width + absxo, self.laidout_height + absyo)

        if self.style.drop_shadow:
            self.render_pass(rv, dsxo, dsyo, self.style.drop_shadow_color, False, length, st)

        if self.render_pass(rv, xo, yo, self.style.color, True, length, st):
            if self.slow:
                self.slow = False
                if self.slow_done:
                    self.slow_done()

        if self.slow:
            renpy.display.render.redraw(self, 0)

        return rv

    def event(self, ev, x, y):
        """
        Space, Enter, or Click ends slow, if it's enabled.
        """

        if not self.slow:
            return None

        if renpy.display.behavior.map_event(ev, "dismiss"):

            self.slow = False
            raise renpy.display.core.IgnoreEvent()


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
