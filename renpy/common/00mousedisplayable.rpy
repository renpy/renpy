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
        """
        :doc: mouse_displayable

        A displayable that wraps a mouse cursor displayable, and causes
        it to move across the screen when the player moves their mouse.

        `cursor`
            A displayable that is used to draw the mouse.

        `x`, `y`
            The coordinates of the hotspot, relative to the upper left
            corner of the mouse, in virtual pixels.

        .. method MouseDisplayable.add(name, cursor, x, y)

            This adds a second cursor, that is used when the `name`
            mouse is displayed. This returns the MouseDisplayable,
            so that calls to this method can be chained.
            """

        def __init__(self, cursor, x, y):

            super(MouseDisplayable, self).__init__()

            self.cursors = { 'default': ( renpy.displayable(cursor), x, y) }

            self.last_cursor = "_default_"
            self.last_cursor_st = 0


        def add(self, name, cursor, x, y):
            self.cursors[name] = ( renpy.displayable(cursor), x, y )
            return self

        def render(self, width, height, st, at):

            # Determine the name of the mouse to use.
            name = renpy.get_mouse_name()

            # If it doesn't exist, use the default.
            if name not in self.cursors:
                name = "default"

            # Adjust st when the cursor changes.
            if name != self.last_cursor:
                self.last_cursor = name
                self.last_cursor_st = st

            st = st - self.last_cursor_st

            # Render this displayable.
            rv = renpy.Render(width, height)

            # If the user is on the screen,
            x, y = renpy.get_mouse_pos()
            d, xo, yo = self.cursors[name]

            if (0 <= x < width) and (0 <= y < height) and renpy.is_mouse_visible():

                cr = renpy.render(d, width, height, st, at)
                rv.subpixel_blit(cr, (x - xo, y - yo))

                # This helps the mouse hide work.
                renpy.redraw(self, 1.0)

            return rv

        def visit(self):
            return [ i[0] for i in self.cursors.values() ]





