import pygame
from pygame.constants import *

import renpy.display.surface
import renpy.config as config
import renpy.display.core as core

_font_cache = { }

def get_font(fn, size):
    from renpy.loader import transfn

    if (fn, size) in _font_cache:
        return _font_cache[(fn, size)]

    rv = pygame.font.Font(transfn(fn), size)
    _font_cache[(fn, size)] = rv

    return rv
    

class Text(core.Displayable):
    """
    @ivar color: The base color of the text.
    @ivar font: The filename of the text font.
    @ivar size: The size of the text.
    @ivar ds_offset: The offset of the dropshadow.
    @ivar ds_color: The color of the dropshadow.
    @ivar text: The text that is being displayed.

    The following aren't serialized, but are reconstructed the first
    time this is redrawn:

    @ivar laidout: The text, split into a list of strings where each
    string happens to be one line on the screen.

    @ivar height: The height of the laid-out text.
    @ivar width: The width of the laid-out text.
    
    """

    def __init__(self, text, color=None, font=None, size=None,
                 ds_offset=None, ds_color=None):

        self.color = color or config.text_color
        self.font = font or config.text_font
        self.size = size or config.text_size
        self.ds_offset = ds_offset or config.text_dropshadow_offset
        self.ds_color = ds_color or config.text_dropshadow_color
        self.text = text

    def update(self):
        """
        This needs to be called after this object is updated, to be
        sure that the changes take effect on the next redraw.
        """

        try:
            del self.laidout
            del self.height
        except AttributeError:
            pass

    def layout(self, width):

        font = get_font(self.font, self.size)

        lines = [ ]
        pars = self.text.split('\n')

        lh = 0

        maxwidth = 0

        for p in pars:
            words = p.split()
            
            line = ""

            for w in words:

                # Each line must have at least one word on it.
                if not line:
                    line = w
                    lw, lh = font.size(line)
                    maxwidth = max(maxwidth, lw)                    
                    continue


                lw, lh = font.size(line + " " + w)

                if lw < width:
                    line += " " + w
                    maxwidth = max(maxwidth, lw)
                else:
                    lines.append(line)
                    line = w

            lines.append(line)


        self.laidout = "\n".join(lines)
        self.height = len(lines) * font.get_linesize()
        self.width = maxwidth

        
    def render(self, width, height, st, wt):

        dsxo, dsyo = self.ds_offset

        if not hasattr(self, "laidout"):
            self.layout(width - dsxo)

        surf = renpy.display.surface.surface((self.width + dsxo, self.height + dsyo), SRCALPHA, 32)
        font = get_font(self.font, self.size)

        lines = self.laidout.split('\n')

        # Common rendering code.
        def render_lines(x, y, color):
            for l in lines:
                ls = font.render(l, True, color)
                surf.blit(ls, (x, y + font.get_descent()))
                y += font.get_linesize()

        fudge = 1

        # Render drop-shadow.
        if self.ds_color:
            render_lines(dsxo, dsyo + fudge, self.ds_color)

        # Render foreground.
        render_lines(0, 0 + fudge, self.color)

        return surf
    
    
            
