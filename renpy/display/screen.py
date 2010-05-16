# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

# TODO: How do we determine which screens should suppress
# input from other screens? What should the default be?

import renpy

class Screen(renpy.display.layout.Container):
    """
    A screen is a collection of widgets that are displayed together. This
    class is responsible for managing the display of a screen.
    """

    def __init__(self,
                 function,
                 predict_function=None,
                 implicit_fixed=True,
                 layer='screens',
                 tag=None):

        super(Screen, self).__init__()
        

        # The function that is called to display this screen.
        self.function = function

        # The function that is called to predict the images that
        # will be used by the screen.
        self.predict_function = predict_function

        # True if the screen should be placed inside an implicit
        # ui.fixed. False if it will create and return the fixed
        # itself.
        self.implicit_fixed = implicit_fixed

        # A tag associated with this screen. When the screen is shown,
        # other screens with the same tag will be hidden.
        self.tag = tag

        # The layer this screen is shown on.
        self.layer = layer
        
        # Keyword arguments given to this screen the last time it was
        # shown.
        self.kwargs = { }

        # The child associated with this screen.
        self.child = None
        
    def visit(self):
        return [ ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        
    def render(self, w, h, st, at):

        if self.implicit_fixed:
            renpy.ui.detached()
            child = renpy.ui.fixed()

            self.function()

            renpy.ui.close()

        else:

            child = self.function(**self.kwargs)
            
        self.child = child
        child.visit_all(lambda c : c.per_interact())

        return renpy.display.render.render(self.child, w, h, st, at)

    def get_placement(self):
        return self.child.get_placement()

    def event(self, ev, x, y, st):
        if self.child:
            return self.child.event(ev, x, y, st)

        
    def show(self, **kwargs):
        # Scan for things with the same name on the layer

        pass

    def hide(self):
        return
