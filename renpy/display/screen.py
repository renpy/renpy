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
                 modal=True,
                 layer='screens',
                 hide_delay=0):

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

        # The layer this screen is shown on.
        self.layer = layer
        
        # The scope associated with this statement. This is passed in
        # as keyword arguments to the displayable.
        self.scope = { }

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

        # Are we modal? (A modal screen ignores screens under it.)
        self.modal = False
        
    def __reduce__(self):
        return (unreduce_screen, (self.name, self.scope, self.widget_properties))

    def _get_parameterized(self):
        return self.child
    
    def visit(self):
        return [ self.child ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        self.update()

    def include(self, _name=(), **kwargs):
        """
        This handles the case where this screen is included from another
        screen, in the screen language.
        """

        self.scope = kwargs
        self.scope["_scope"] = self.scope
        self.scope["_name"] = _name
        self.function(**self.scope)

    def set_transform_event(self, event):
        super(Screen, self).set_transform_event(event)

        for i in self.child.children:
            i.set_transform_event(event)

    def _hide(self, st, at, kind):        

        rv = None

        for i in self.transforms:
            c = self.transforms[i]._hide(st, at, kind)

            if c is not None:
                self.transforms[i] = c
                rv = self

        return rv
    
    def update(self):

        global _current_screen
        old_screen = _current_screen
        _current_screen = self.name
        
        renpy.ui.widget_by_id = { }
        renpy.ui.transform_by_id = { }
        renpy.ui.old_transform_by_id = self.transforms
        renpy.ui.widget_properties = self.widget_properties
        
        renpy.ui.detached()
        self.child = renpy.ui.fixed()
        self.children = [ self.child ]
        
        self.scope["_scope"] = self.scope
        self.function(**self.scope)
        
        renpy.ui.close()

        self.child.visit_all(lambda c : c.per_interact())

        rv = renpy.ui.widget_by_id
        self.widgets = renpy.ui.widget_by_id
        self.transforms = renpy.ui.transform_by_id
        
        renpy.ui.widget_by_id = None
        renpy.ui.transform_by_id = None 
        renpy.ui.old_transform_by_id = None
        renpy.ui.widget_properties = None

        _current_screen = old_screen

        return rv
       
    def render(self, w, h, st, at):
        return renpy.display.render.render(self.child, w, h, st, at)

    def get_placement(self):
        return self.child.get_placement()

    def event(self, ev, x, y, st):

        global _current_screen
        old_screen = _current_screen
        _current_screen = self.name
        
        rv = self.child.event(ev, x, y, st)

        _current_screen = old_screen
        
        if rv is not None:
            return rv
        
        if self.modal:
            raise renpy.display.core.IgnoreEvents()
        
    def show(self, widget_properties={ }, **kwargs):

        self.widgets = None
        self.transforms = { }
        self.widget_properties = widget_properties
        self.scope = kwargs

        self.update()

        # Show this screen on the screens layer.
        renpy.exports.show(self.name, layer=self.layer, what=self)

        # Remove everything above 
        renpy.ui.layer(self.layer)
        renpy.ui.remove_above(self.name[0])
        renpy.ui.close()

        
    def hide(self):
        renpy.exports.hide(self.name, layer=self.layer)


# The name of the screen that is currently being displayed, or
# None if no screen is being currently displayed.
_current_screen = None
        
# A map from screen name to screen object.
screens = { }

def unreduce_screen(name, scope, widget_properties):
    """
    Used to unpickle a screen, replacing it with the current
    definition of that screen.
    """

    rv = screens[name]
    rv.scope = scope
    rv.widget_properties = widget_properties

    return rv

def define_screen(*args, **kwargs):
    Screen(*args, **kwargs)

def get_screen(name):
    if not isinstance(name, tuple):
        name = tuple(name.split())

    if not name in screens:
        raise Exception("Screen %r is not known." % (name,) )

    return screens[name]

def has_screen(name):
    if not isinstance(name, tuple):
        name = tuple(name.split())

    return name in screens

def show_screen(name, **kwargs):
    get_screen(name).show(**kwargs)
    
def hide_screen(name):
    get_screen(name).hide()

def include_screen(name, **kwargs):
    get_screen(name).include(**kwargs)

def current_screen():
    return _current_screen

def get_current_screen():
    return get_screen(current_screen)

def get_widget(screen, name):
    rv = get_screen(screen).widgets.get(name, None)

    if rv is None:
        raise Exception("There is no widget with id %r in screen %r." % (name, screen))
        
    return rv
