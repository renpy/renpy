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
                 modal=False,
                 zorder=0,
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
        self.modal = modal

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
        
    def __init__(self, screen, tag, layer, widget_properties={}, scope={}, **properties):

        super(ScreenDisplayable, self).__init__(**properties)

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

        # Are we hiding?
        self.hiding = False
        
    def visit(self):
        return [ self.child ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        self.update()

    def set_transform_event(self, event):
        super(ScreenDisplayable, self).set_transform_event(event)        
        self.current_transform_event = event
            
    def _hide(self, st, at, kind):        
        
        self.hiding = True

        self.current_transform_event = kind
        self.update()
        
        renpy.display.render.redraw(self, 0)
                
        rv = None

        for i in self.transforms:
            c = self.transforms[i]._hide(st, at, kind)

            if c is not None:
                self.transforms[i] = c
                rv = self

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
        self.scope["_name"] = 0
         
        self.screen.function(**self.scope)
        
        renpy.ui.close()

        renpy.ui.screen = old_ui_screen
        _current_screen = old_screen
        
        # Visit all the children, to get them started.
        self.child.visit_all(lambda c : c.per_interact())

        # Finish up.
        self.old_widgets = None
        self.old_transforms = None
        
        if self.current_transform_event:

            for i in self.child.children:
                i.set_transform_event(self.current_transform_event)

            self.current_transform_event = None
        
        return self.widgets
       
    def render(self, w, h, st, at):
        if not self.child:
            self.update()

        rv = renpy.display.render.render(self.child, w, h, st, at)
        rv.modal = self.screen.modal

        return rv
        
    def get_placement(self):
        if not self.child:
            self.update()

        return self.child.get_placement()

    def event(self, ev, x, y, st):

        if self.hiding:
            return
        
        global _current_screen
        old_screen = _current_screen
        _current_screen = self
        
        rv = self.child.event(ev, x, y, st)

        _current_screen = old_screen
        
        if rv is not None:
            return rv
        
        if self.screen.modal:
            raise renpy.display.layout.IgnoreLayers() # renpy.display.core.IgnoreEvent()
        


# The name of the screen that is currently being displayed, or
# None if no screen is being currently displayed.
_current_screen = None
        
# A map from screen name to screen object.
screens = { }

def define_screen(*args, **kwargs):
    """
    :doc: screens
    :args: (name, function, modal=True, zorder=0, tag=None)

    Defines a screen with `name`, which should be a string.

    `function`
        The function that is called to display the screen. The
        function is called with the screen scope as keyword
        arguments. It should ignore additional keyword arguments.

        The function should call the ui functions to add things to the
        screen.

    `modal`
        Determines if this screen is modal. A modal screen
        prevents screens underneath it from receiving input events.

    `zorder`
        Controls the order in which screens are displayed. A screen
        with a greater zorder number is displayed above screens with a
        lesser zorder number.

    `tag`
        The tag associated with this screen. When the screen is shown,
        it replaces any other screen with the same tag. The tag
        defaults to the name of the screen.
    """

    Screen(*args, **kwargs)


    
def get_screen(name, layer="screens"):
    """
    :doc: screens
    
    Returns the ScreenDisplayable with the given `tag`, on
    `layer`. If no displayable with the tag is not found, it is
    interpreted as screen name. If it's still not found, None is returned. 
    """

    if isinstance(name, basestring):
        name = tuple(name.split())

    tag = name[0]
    
    sl = renpy.exports.scene_lists()

    sd = sl.get_displayable_by_tag(layer, tag)

    if sd is None:
        sd = sl.get_displayable_by_name(layer, name)
        
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
    :doc: screens
    
    The programmatic equivalent of the show screen statement.

    Shows the named screen.

    `_screen_name`
        The name of the  screen to show.
    `_layer`
        The layer to show the screen on.
    `_tag`
        The tag to show the screen with. If not specified, defaults to
        the tag associated with the screen. It that's not specified,
        defaults to the name of the screen.,
    `_widget_properties`
        A map from the id of a widget to a property name -> property
        value map. When a widget with that id is shown by the screen,
        the specified properties are added to it.
    `_transient`
        If true, the screen will be automatically hidden at the end of
        the current interaction.

    Keyword arguments not beginning with underscore (_) are used to
    initialize the screen's scope.       
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
    """
    :doc: screens

    The programmatic equivalent of the hide screen statement.
    
    Hides the screen with `tag` on `layer`.
    """
    
    tag = tag.split()[0]
    
    renpy.exports.hide(tag, layer=layer)

def use_screen(_screen_name, _name=(), **kwargs):
    
    name = _screen_name
    
    if not isinstance(name, tuple):
        name = tuple(name.split())
    
    if name not in screens:
        raise Exception("Screen %r is not known." % name)

    screen = screens[name]
    
    scope = kwargs["_scope"].copy() or { }
    scope.update(kwargs)
    scope["_scope"] = scope
    scope["_name"] = _name
    screen.function(**scope)

def current_screen():
    return _current_screen

def get_widget(screen, id, layer='screens'):
    """
    :doc: screens

    From the `screen` on `layer`, returns the widget with
    `id`. Returns None if the screen doesn't exist, or there is no
    widget with that id on the screen.
    """

    if screen is None:
        screen = current_screen()
    else:    
        screen = get_screen(screen, layer)

    if not isinstance(screen, ScreenDisplayable):
       return None

    if screen.child is None:
        screen.update()
    
    rv = screen.widgets.get(id, None)        
    return rv
