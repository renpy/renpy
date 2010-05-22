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

import renpy

class Screen(renpy.display.layout.Container):
    """
    A screen is a collection of widgets that are displayed together. This
    class is responsible for managing the display of a screen.
    """

    def __init__(self,
                 name,
                 function,
                 predict_function=None,
                 implicit_fixed=True,
                 modal=True,
                 layer='screens'):

        super(Screen, self).__init__()

        # The name of this screen.
        if isinstance(name, basestring):
            name = tuple(name.split())
                
        self.name = name
        screens[name] = self
        
        # The function that is called to display this screen.
        self.function = function

        # The function that is called to predict the images that
        # will be used by the screen.
        self.predict_function = predict_function

        # True if the screen should be placed inside an implicit
        # ui.fixed. False if it will create and return the fixed
        # itself.
        self.implicit_fixed = implicit_fixed

        # The layer this screen is shown on.
        self.layer = layer
        
        # Keyword arguments given to this screen the last time it was
        # shown.
        self.kwargs = { }

        # Widget properties given to this screen the last time it was
        # shown.
        self.widget_properties = { }
        
        # The child associated with this screen.
        self.child = None

        # The transforms used to display the screen.
        self.transforms = { }

        # The widgets used to display the screen. None if we haven't
        # figured that out yet.
        self.widgets = None

        # Do we need to be updated?
        self.needs_update = True
        
    def __reduce__(self):
        return (unreduce_screen, (self.name, self.kwargs, self.widget_properties))

    def visit(self):
        return [ self.child ]

    def per_interact(self):
        self.update()

    def update(self):

        renpy.ui.widget_by_id = { }
        renpy.ui.transform_by_id = { }
        renpy.ui.old_transform_by_id = self.transforms
        renpy.ui.widget_properties = self.widget_properties
        
        if self.implicit_fixed:
            renpy.ui.detached()
            child = renpy.ui.fixed()

            self.function()

            renpy.ui.close()

        else:

            child = self.function(**self.kwargs)

        self.child = child
        child.visit_all(lambda c : c.per_interact())

        rv = renpy.ui.widget_by_id
        self.widgets = renpy.ui.widget_by_id
        self.transforms = renpy.ui.transform_by_id
        
        renpy.ui.widget_by_id = None
        renpy.ui.transform_by_id = None 
        renpy.ui.old_transform_by_id = None
        renpy.ui.widget_properties = None

        return rv
       
    def render(self, w, h, st, at):
        return renpy.display.render.render(self.child, w, h, st, at)

    def get_placement(self):
        return self.child.get_placement()

    def event(self, ev, x, y, st):
        return self.child.event(ev, x, y, st)

        if self.modal:
            raise renpy.display.core.IgnoreEvents()
        
    def show(self, widget_properties={ }, **kwargs):

        self.widgets = None
        self.transforms = { }
        self.widget_properties = widget_properties
        self.kwargs = kwargs

        self.update()

        # Show this screen on the screens layer.
        renpy.exports.show(self.name, layer=self.layer, what=self)

        # Remove everything above 
        renpy.ui.layer(self.layer)
        renpy.ui.remove_above(self.name[0])
        renpy.ui.close()

        
    def hide(self):
        renpy.exports.hide(self.name, layer=self.layer)


# A map from screen name to screen object.
screens = { }

def unreduce_screen(name, kwargs, widget_properties):
    """
    Used to unpickle a screen, replacing it with the current
    definition of that screen.
    """

    rv = screens[name]
    rv.kwargs = kwargs
    rv.widget_properties = widget_properties

    return rv

def define_screen(*args, **kwargs):
    Screen(*args, **kwargs)

def get_screen(name):
    if not isinstance(name, tuple):
        name = tuple(name.split())

    if not name in screens:
        raise Exception("Screen %r is not known." % name)

    return screens[name]
    
def show_screen(name, **kwargs):
    get_screen(name).show(**kwargs)
    
def hide_screen(name):
    get_screen(name).hide()
