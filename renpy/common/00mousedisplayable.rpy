# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

init -1500 python:

    class MouseDisplayable(renpy.Displayable):

        def __init__(self, cursor, x, y):
            """
            :doc: mouse_displayable

            A displayable that wraps a mouse cursor displayable, and causes
            it to move across the screen when the player moves their mouse.

            `cursor`
                The mouse cursor image.

            `x`, `y`
                The coordinates of the hotspot, relative to the upper left
                corner of the mouse, in virtual pixels.
            """

            super(MouseDisplayable, self).__init__()

            self.cursor = renpy.displayable(cursor)
            self.x = x
            self.y = y

        def render(self, width, height, st, at):

            rv = renpy.Render(width, height)

            x, y = renpy.get_mouse_pos()

            if (0 <= x < width) and (0 <= y < height) and renpy.is_mouse_visible():

                cr = renpy.render(self.cursor, width, height, st, at)
                rv.subpixel_blit(cr, (x - self.x, y - self.y))

                # This helps the mouse hide work.
                renpy.redraw(self, 1.0)

            return rv

        def visit(self):
            return [ self.cursor ]





