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

class Screen(renpy.object.Object):
    """
    A screen is a collection of widgets that are displayed together.
    This class stores information about the screen.
    """

    def __init__(self,
                 name,
                 function,
                 predict_function=None,
                 modal=True,
                 zorder=0,
                 hide_delay=0,
                 tag=None):
    
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

        # Are we modal? (A modal screen ignores screens under it.)
        self.modal = False

        # Our zorder.
        self.zorder = zorder

        # The tag associated with the screen.
        self.tag = tag or name[0]

class ScreenDisplayable(renpy.display.layout.Container):
    """
    A screen is a collection of widgets that are displayed together. This
    class is responsible for managing the display of a screen.
    """

    no_save = [ 'screen' ]

    def after_setstate(self):
        self.screen = screens[self.screen_name]
        
    def __init__(self, screen, tag, layer, widget_properties={}, scope={}):

        super(ScreenDisplayable, self).__init__()

        # The screen, and it's name. (The name is used to look up the
        # screen on save.)
        self.screen = screen
        self.screen_name = screen.name

        # The tag this and layer screen was displayed with.
        self.tag = tag
        self.layer = layer
        
        # The scope associated with this statement. This is passed in
        # as keyword arguments to the displayable.
        self.scope = renpy.python.RevertableDict(scope)
        
        # The child associated with this screen.
        self.child = None

        # Widget properties given to this screen the last time it was
        # shown.
        self.widget_properties = widget_properties
        

        old_screen = get_screen(tag, layer)
        
        # A map from name to the widget with that name. 
        self.widgets = { }

        # A map from name to the transform with that name. (This is
        # taken from the old version of the screen, if it exists.
        if old_screen:
            self.transforms = old_screen.transforms
        else:            
            self.transforms = { }

        # What widgets and transforms were the last time this screen was
        # updated. Used to communicate with the ui module, and only
        # valid during an update - not used at other times.
        self.old_widgets = None
        self.old_transforms = None

        # The current transform event, and the last transform event to
        # be processed.
        self.current_transform_event = None

        self.update()

    def _get_parameterized(self):
        return self.child
    
    def visit(self):
        return [ self.child ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        self.update()

    def set_transform_event(self, event):
        super(ScreenDisplayable, self).set_transform_event(event)
        
        for i in self.child.children:
            i.set_transform_event(event)

        self.current_transform_event = event
            
    def _hide(self, st, at, kind):        

        rv = None

        for i in self.transforms:
            c = self.transforms[i]._hide(st, at, kind)

            if c is not None:
                self.transforms[i] = c
                rv = self

        self.current_transform_event = kind
        self.update()
        
        return rv
    
    def update(self):

        # Update _current_screen
        global _current_screen
        old_screen = _current_screen
        _current_screen = self

        # Cycle widgets and transforms.
        self.old_widgets = self.widgets
        self.old_transforms = self.transforms
        self.widgets = { }
        self.transforms = { }
        
        # Render the child.
        old_ui_screen = renpy.ui.screen
        renpy.ui.screen = self
        
        renpy.ui.detached()
        self.child = renpy.ui.fixed()
        self.children = [ self.child ]
        
        self.scope["_scope"] = self.scope
        self.screen.function(**self.scope)
        
        renpy.ui.close()

        renpy.ui.screen = old_ui_screen
        
        # Visit all the children, to get them started.
        self.child.visit_all(lambda c : c.per_interact())

        # Finish up.
        self.old_widgets = None
        self.old_transforms = None

        _current_screen = old_screen

        self.current_transform_event = None

        return self.widgets
       
    def render(self, w, h, st, at):
        return renpy.display.render.render(self.child, w, h, st, at)

    def get_placement(self):
        return self.child.get_placement()

    def event(self, ev, x, y, st):

        global _current_screen
        old_screen = _current_screen
        _current_screen = self
        
        rv = self.child.event(ev, x, y, st)

        _current_screen = old_screen
        
        if rv is not None:
            return rv
        
        if self.screen.modal:
            raise renpy.display.core.IgnoreEvents()
        


# The name of the screen that is currently being displayed, or
# None if no screen is being currently displayed.
_current_screen = None
        
# A map from screen name to screen object.
screens = { }

def define_screen(*args, **kwargs):
    Screen(*args, **kwargs)
    
def get_screen(tag, layer="screens"):
    """
    Returns the ScreenDisplayable with the given tag or name, on the
    given layer.
    """

    tag = tag.split()[0]
    sl = renpy.exports.scene_lists()

    sd = sl.get_displayable_by_tag(layer, tag)

    if sd is None:
        sd = sl.get_displayable_by_name(layer, tag)

    return sd

def has_screen(name):
    """
    Returns true if a screen with the given name exists.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    return name in screens


def show_screen(_screen_name, _layer='screens', _tag=None, _widget_properties={}, _transient=False, **kwargs):
    """
    Shows the named screen.
    """

    name = _screen_name
    
    if not isinstance(name, tuple):
        name = tuple(name.split())

    if not name in screens:
        raise Exception("Screen %r is not known.\n", (name,))

    screen = screens[name]

    if _tag is None:
        _tag = screen.tag

    d = ScreenDisplayable(screen, _tag, _layer, _widget_properties, kwargs)    
    renpy.exports.show(name, tag=_tag, what=d, layer=_layer, zorder=screen.zorder, transient=_transient, munge_name=False)

def hide_screen(tag, layer='screens'):

    tag = tag.split()[0]
    
    # TODO: Defer hide.
    renpy.exports.hide(tag, layer=layer)

def include_screen(_screen_name, _name=(), **kwargs):

    name = _screen_name
    
    if not isinstance(name, tuple):
        name = tuple(name.split())
    
    if name not in screens:
        raise Exception("Screen %r is not known." % name)

    screen = screens[name]
    
    scope = kwargs
    scope["_scope"] = scope
    scope["_name"] = _name
    screen.function(**scope)

def current_screen():
    return _current_screen

def get_widget(name, widget_name, layer='screens'):

    screen = get_screen(name, layer)

    if not isinstance(screen, ScreenDisplayable):
        raise Exception("A screen with the tag %r was not found on layer %r." % (name, layer))

    rv = screen.widgets.get(widget_name, None)

    if rv is None:
        raise Exception("There is no widget with id %r in screen %r." % (widget_name, name))
        
    return rv
