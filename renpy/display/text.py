import pygame
from pygame.constants import *

import re
import renpy
import sys

_font_cache = { }

# TODO: Something sane if the font file can't be found.
def get_font(fn, size, bold=False, italics=False, underline=False):
    from renpy.loader import transfn

    if (fn, size, bold, italics, underline) in _font_cache:
        return _font_cache[(fn, size, bold, italics, underline)]

    try:
        rv = pygame.font.Font(transfn(fn), size)
        rv.set_bold(bold)
        rv.set_italic(italics)
    except:
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
        return font.size(text)[0], font.get_linesize()

    def render(self, text, antialias, color, use_colors):

        if use_colors and self.color:
            color = self.color

        font = self.get_font()

        rv = font.render(text, antialias, color)
        renpy.display.render.mutated_surface(rv)
        return rv

class Text(renpy.display.core.Displayable):
    """
    A displayable that can format and display text on the screen.
    """

    nosave = [ 'laidout', 'laidout_lineheights', 'laidout_width', 'laidout_height', 'width' ]

    def after_setstate(self):
        self.laidout = None

    def __init__(self, text, slow=False, style='default', **properties):
        """
        @param text: The text that will be displayed on the screen.

        @param slow: If True, the text will be slowly typed onto the screen.

        @param style: A style that will be applied to the text.

        @param properties: Additional properties that are applied to the text.
        """

        super(Text, self).__init__()

        self.text = text
        self.style = renpy.style.Style(style, properties)
        self.slow = slow

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

    def _update(self):
        """
        This is called after this widget has been updated by
        set_text or set_style.
        """        

        self.laidout = None
        renpy.display.render.redraw(self, 0)

    def event(self, ev, x, y):
        """
        Space, Enter, or Click ends slow, if it's enabled.
        """

        if not self.slow:
            return None

        if renpy.display.behavior.map_event(ev, "dismiss"):

            self.slow = False
            raise renpy.display.core.IgnoreEvent()

    def layout(self, width):
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
        # line_height_fudge.
        lineheight = 0

        # A list of same.
        lineheights = [ ]

        # The width of the current line.
        linewidth = 0

        # The maximum linewidth.
        maxwidth = 0

        # The current text.
        cur = ""

        # The width, in pixels, of cur.
        curwidth = 0

        # The remaining width of the line, not including the text in
        # cur.
        remwidth = width - indent()

        for i in re.split(r'( |\{[^{]+\}|\{\{|\n)', self.text):

            # Newline.
            if i == "\n":
                if cur:
                    line.append((TextStyle(tsl[-1]), cur))                    
                    maxwidth = max(maxwidth, linewidth + curwidth)
                    cur = ""
                
                lines.append(line)
                lineheights.append(lineheight)
                
                line = [ ]
                linewidth = 0
                curwidth, lineheight = tsl[-1].sizes(" ")
                remwidth = width - indent()

                continue

            elif i == "{{":
                i = "{"
                # We want to render this like a word, so no continue.

            elif i.startswith("{"):

                # Are we closing a tag?
                if i.startswith("{/"):
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

                if i == "{b}":
                    tsl[-1].bold = True

                elif i == "{i}":
                    tsl[-1].italic = True

                elif i == "{u}":
                    tsl[-1].underline = True

                elif i == "{plain}":
                    tsl[-1].bold = False
                    tsl[-1].italic = False
                    tsl[-1].underline = False

                elif i.startswith("{size"):

                    m = re.match(r'\{size=(\+|-|)(\d+)\}', i)

                    if not m:
                        raise Exception('Size tag %s could not be parsed.' % i)

                    if m.group(1) == '+':
                        tsl[-1].size += int(m.group(2))
                    elif m.group(1) == '-':
                        tsl[-1].size -= int(m.group(2))
                    else:
                        tsl[-1].size = int(m.group(2))                    

                elif i.startswith("{color"):

                    m = re.match(r'\{color=(\#?[a-fA-F0-9]+)\}', i)

                    if not m:
                        raise Exception('Color tag %s could not be parsed.' % i)

                    tsl[-1].color = color(m.group(1))

                else:
                    raise Exception("Text tag %s was not recognized. Case and spacing matter here.")

                continue

            elif i == ' ':
                # Spaces always get appended to the end of a line. So they
                # will never show up at the start of a line, unless they're
                # after a newline or at the start of a string.

                cur += i
                curwidth, lh = tsl[-1].sizes(cur)
                lineheight = max(lh, lineheight)
                
                continue

            # If we made it here, then we have normal text.

            # We must have at least one word or something else in the
            # line before we care about wrapping.
            if not cur and not line:
                cur = i                
                curwidth, lineheight = tsl[-1].sizes(cur)
                continue

            # Should we wrap?
            curwidth, lh = tsl[-1].sizes(cur + i)

            if curwidth > remwidth:
                line.append((TextStyle(tsl[-1]), cur))
                lines.append(line)

                maxwidth = max(maxwidth, linewidth)
                
                line = [ ]
                lineheights.append(lineheight)
                
                cur = i
                curwidth, lineheight = tsl[-1].sizes(cur)                
                remwidth = width - indent()
                linewidth = 0
            else:
                cur = cur + i
                lineheight = max(lh, lineheight)

        # We're done. Let's close up.

        if len(tsl) != 1:
            exception("A tag was left open at the end of the text.")
            
        if cur:
            line.append((tsl[-1], cur))
            maxwidth = max(maxwidth, curwidth)

        if line:
            lines.append(line)
            lineheights.append(lineheight)


        self.laidout = lines
        self.laidout_lineheights = lineheights
        self.laidout_width = max(maxwidth, self.style.minwidth)
        self.laidout_height = sum(lineheights) + len(lineheights) * self.style.line_height_fudge

    def render_pass(self, r, xo, yo, color, user_colors, length):
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
        line_height_fudge = self.style.line_height_fudge
        
        for line, line_height in zip(self.laidout, self.laidout_lineheights):
            x = xo + indent
            indent = rest_indent

            max_ascent = 0

            for ts, text in line:
                max_ascent = max(ts.get_ascent(), max_ascent)

            for ts, text in line:
                
                length -= len(text)
                if length < 0:
                    text = text[:length]
                
                surf = ts.render(text, antialias, color, user_colors)
                sw, sh = surf.get_size()

                r.blit(surf, (x, y + max_ascent - ts.get_ascent()))

                x = x + sw

                if length <= 0:
                    return False

            y = y + line_height + line_height_fudge

        return True
            
    def render(self, width, height, st):

        if self.slow and renpy.config.annoying_text_cps and not renpy.game.preferences.fast_text:
            length = int(st * renpy.config.annoying_text_cps)
        else:
            length = sys.maxint
            self.slow = False

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
                
        self.layout(width - absxo)
            
        rv = renpy.display.render.Render(self.laidout_width + absxo, self.laidout_height + absxo)

        if self.style.drop_shadow:
            self.render_pass(rv, dsxo, dsyo, self.style.drop_shadow_color, False, length)

        self.slow = not self.render_pass(rv, xo, yo, self.style.color, True, length)

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

class OldText(renpy.display.core.Displayable):
    """
    A Displayable that can display text on the screen.
    """
    
    
    """ 
    @ivar style: The style that is used to display the text.
    @ivar text: The text that is being displayed.

    The following aren't serialized, but are reconstructed the first
    time this is redrawn:

    @ivar laidout: The text, split into a list of strings where each
    string happens to be one line on the screen.

    @ivar height: The height of the laid-out text.
    @ivar width: The width of the laid-out text.
    
    """

    def __init__(self, text, slow=False, style='default', **properties):
        """
        @param text: The text that will be displayed on the screen.

        @param slow: If True, the text will be slowly typed onto the screen.

        @param style: A style that will be applied to the text.

        @param properties: Additional properties that are applied to the text.
        """

        super(Text, self).__init__()

        self.text = text
        self.style = renpy.style.Style(style, properties)
        self.slow = slow

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

    def _update(self):
        """
        This is called after this widget has been updated by
        set_text or set_style.
        """

        try:
            del self.laidout
            del self.width
            del self.height
        except AttributeError:
            pass

    def layout(self, width):
        """
        Called to split the text into a string with newline characters
        at line endings where wrapping has occured.
        """
        
        font = get_font(self.style.font, self.style.size)

        lines = [ ]
        pars = self.text.split('\n')

        lh = 0

        maxwidth = 0

        # The indent of the current line.
        indent = self.style.first_indent
        

        for p in pars:
            words = p.split(' ')
            
            line = ""

            for w in words:

                # Each line must have at least one word on it.
                if not line:
                    line = w
                    lw, lh = font.size(line)
                    maxwidth = max(maxwidth, lw)                    
                    continue


                lw, lh = font.size(line + " " + w)

                if lw + indent < width:
                    line += " " + w
                    maxwidth = max(maxwidth, lw)
                else:
                    lines.append(line)
                    line = w
                    indent = self.style.rest_indent

            lines.append(line)


        self.laidout = "\n".join(lines)
        self.height = len(lines) * (font.get_linesize() + self.style.line_height_fudge)
        self.width = max(maxwidth, self.style.minwidth)

        
    def render(self, width, height, st):

        if self.style.drop_shadow:
            dsxo, dsyo = self.style.drop_shadow
        else:
            dsxo, dsyo = 0, 0

        if not hasattr(self, "laidout"):
            self.layout(width - dsxo)

        surf = renpy.display.render.Render(self.width + dsxo, self.height + dsyo)
        font = get_font(self.style.font, self.style.size)

        laidout = self.laidout

        # Annoying text hack.
        if self.slow and renpy.config.annoying_text_cps and not renpy.game.preferences.fast_text:
            chars = int(st * renpy.config.annoying_text_cps)
            if chars < len(laidout):
                laidout = laidout[:chars]
                renpy.display.render.redraw(self, 0)
            else:
                self.slow = False
        else:
            self.slow = False


        lines = laidout.split('\n')

        first_indent = self.style.first_indent
        rest_indent = self.style.rest_indent


        # Common rendering code.
        def render_lines(x, y, color):

            y += self.style.text_y_fudge

            indent = first_indent

            for l in lines:
                ls = font.render(l, self.style.antialias, color)
                renpy.display.render.mutated_surface(ls)

                lw, lh = ls.get_size()
                lw += indent

                xo = int((self.width - lw) * self.style.textalign)
                surf.blit(ls, (x + xo + indent, y + font.get_descent()))

                y += font.get_linesize() + self.style.line_height_fudge
                indent = rest_indent
                



        # Render drop-shadow.
        if self.style.drop_shadow:
            render_lines(dsxo, dsyo, self.style.drop_shadow_color)

        # Render foreground.
        render_lines(0, 0, self.style.color)

        return surf

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
        

