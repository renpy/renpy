# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# The minigame API.

import renpy

# A map from (text, font, size, color, bold, italics, underline) -> surface.
# This one is for the old frame.
old_text_cache = { }

# A map from (text, font, size, color, bold, italics, underline) -> surface.
# This is for the new frame.
new_text_cache = { }

class Minigame(renpy.display.core.Displayable):
    
    def __init__(self, render_callback, event_callback, **properties):
        super(Minigame, self).__init__(**properties)

        self.render_callback = render_callback
        self.event_callback = event_callback

    def render(self, width, height, st, at):

        global old_text_cache
        global new_text_cache

        rv = renpy.display.render.Render(width, height)
        self.render_callback(rv, st)

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

    def render_text(self, text, font, size, color, bold=False, italics=False, underline=False, antialias=True):
        color = renpy.easy.color(color)

        key = (text, font, size, color, bold, italics, underline, antialias)
        rv = old_text_cache.get(key, None)

        if rv is None:

            font = renpy.display.text.get_font(font, size, bold=bold, italics=italics, underline=underline)
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
    
    def ignore_event(self):
        raise renpy.display.core.IgnoreEvent()
