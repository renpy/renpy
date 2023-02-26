# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

python early in icon:

    from store import im, Image, Color, Text

    # The path to the icons.
    path = [ '', 'icons/' ]

    class Icon(renpy.Displayable):

        def __init__(self, name, style="icon", **properties):
            super(Icon, self).__init__(style=style, **properties)

            self.name = name

        def find_image(self, prefix):

            for p in path:
                fn = p + prefix + self.name + ".png"
                if renpy.loadable(fn, directory="images"):
                    return fn

            for p in path:
                fn = p + self.name + ".png"

                if renpy.loadable(fn, directory="images"):
                    c = self.style.color

                    if c is not None:
                        c = Color(self.style.color)
                        return im.Recolor(fn, c[0], c[1], c[2], c[3])
                    else:
                        c = Image(fn)

            return Text('icon {}'.format(self.name))

        def render(self, width, height, st, at):
            d = self.find_image(self.style.prefix)
            cr = renpy.render(d, width, height, st, at)
            cw, ch = cr.get_size()

            scale = min(1.0 * width / cw, 1.0 * height / ch)

            rv = renpy.Render(cw * scale, ch * scale)
            rv.zoom(scale, scale)
            rv.blit(cr, (0, 0))

            return rv

        STATES = [
            "insensitive_",
            "idle_",
            "hover_",
            "selected_idle_",
            "selected_hover_",
            ]

        def visit(self):
            return [ self.find_image(p) for p in Icon.STATES ]

    # Register the icon with screen language.
    renpy.register_sl_displayable("icon", Icon, 0, "icon") \
        .add_positional("name") \
        .add_style_property("color")
