import pygame
from pygame.constants import *

import renpy

_font_cache = { }

# TODO: Something sane if the font file can't be found.
def get_font(fn, size):
    from renpy.loader import transfn

    if (fn, size) in _font_cache:
        return _font_cache[(fn, size)]

    try:
        rv = pygame.font.Font(transfn(fn), size)
    except:
        rv = pygame.font.SysFont(fn, size)

    _font_cache[(fn, size)] = rv

    return rv
    



class Text(renpy.display.core.Displayable):
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

        surf = renpy.display.surface.Surface(self.width + dsxo, self.height + dsyo)
        font = get_font(self.style.font, self.style.size)

        laidout = self.laidout

        # Annoying text hack.
        if self.slow and renpy.config.annoying_text_cps and not renpy.game.preferences.fast_text:
            chars = int(st * renpy.config.annoying_text_cps)
            if chars < len(laidout):
                laidout = laidout[:chars]
                renpy.game.interface.redraw(0)
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
        
