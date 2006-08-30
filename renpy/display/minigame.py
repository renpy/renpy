# The minigame API.

# A map from (text, font, size, color, bold, italics, underline) -> surface.
# This one is for the old frame.
old_text_cache = { }

# A map from (text, font, size, color, bold, italics, underline) -> surface.
# This is for the new frame.
new_text_cache = { }

class Minigame(renpy.display.core.object):
    
    def __init__(self, render_callback, event_callback):
        self.render_callback = render_callback
        self.event_callback = event_callback

    def render(self, width, height, st, at):

        global old_text_cache
        global new_text_cache

        rv = renpy.display.render.Render(width, height)
        self.render_callback(self, st)

        old_text_cache = new_text_cache
        new_text_cache = { }

        return rv

    def event(self, ev, x, y, st):
        return self.event_callback(ev, x, y, st)

    def run(self):
        renpy.ui.add(self)
        return renpy.ui.interact()

    def load_image(self, image):
        return renpy.display.im.load_image(image)

    def mutated_surface(self, surf):
        renpy.display.render.mutated_surface(surf)

    def render_text(text, font, size, color, bold=False, italics=False, underline=False, antialias=True):
        color = renpy.easy.color(color)

        key = (text, font, size, color, bold, italics, underline, antialias)
        rv = old_text_cache.get(key, None)

        if rv is None:

            font = renpy.display.text.get_font(text, font, size, bold=bold, italics=italics, underline=underline)
            rv = font.render(text, antialias, color)
            self.mutated_surface(rv)

        old_text_cache[key] = rv
        new_text_cache[key] = rv
        return rv

    def redraw(self):
        renpy.display.render.redraw(self, 0)

    def timeout(self, seconds):
        renpy.game.interface.timeout(seconds)

    def load(self, filename):
        return renpy.loader.load(filename)
    
