import pygame
import renpy

_font_cache = { }

# TODO: Something sane if the font file can't be found.
def get_font(fn, size):
    from renpy.loader import transfn

    if (fn, size) in _font_cache:
        return _font_cache[(fn, size)]

    rv = pygame.font.Font(transfn(fn), size)
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

    def __init__(self, text, style='default', **properties):
        """
        @param text: The text that will be displayed on the screen.

        @param style: A style that will be applied to the text.

        @param properties: Additional properties that are applied to the text.
        """


        self.text = text
        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def set_text(self, new_text):
        """
        Changes the text display by this object to new_text.
        """

        self.text = new_text
        self._update()

    def set_style(self, style, **properties):
        """
        Changes the style assocated with this object.
        """

        self.style = renpy.style.Style(style, properties)
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

        lines = self.laidout.split('\n')

        # Common rendering code.
        def render_lines(x, y, color):
            for l in lines:
                ls = font.render(l, True, color)
                lw, lh = ls.get_size()
                xo = int((self.width - lw) * self.style.textalign)
                surf.blit(ls, (x + xo, y + font.get_descent()))
                y += font.get_linesize() + self.style.line_height_fudge

        fudge = 1

        # Render drop-shadow.
        if self.style.drop_shadow:
            render_lines(dsxo, dsyo + fudge, self.style.drop_shadow_color)

        # Render foreground.
        render_lines(0, 0 + fudge, self.style.color)

        return surf

## Not needed any more.
    
# class ExpressionText(Text):
#     """
#     This is a Displayable that displays the result of an expression on
#     the screen, as text.
#     """

#     def __init__(self, expression, style='default', **properties):
#         """
#         @param expression: An expression that is evaluated to get the
#         text that will be shown on the screen.

#         @param style: A style that will be applied to the text.

#         @param properties: Additional properties that are applied to
#         the text.
#         """

#         super(ExpressionText, self).__init__('', **properties)

#         self.old_value = ''
#         self.expression = expression

#     def render(self, width, height, st):

#         value = renpy.python.py_eval(self.expression)
#         value = str(value)

#         if value != self.old_value:
#             self.old_value = value
#             self.set_text(value)

#         return super(ExpressionText, self).render(width, height, st)
        
