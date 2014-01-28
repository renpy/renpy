# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display

class Screen(renpy.object.Object):
    """
    A screen is a collection of widgets that are displayed together.
    This class stores information about the screen.
    """

    def __init__(self,
                 name,
                 function,
                 modal="False",
                 zorder="0",
                 tag=None,
                 predict=None,
                 variant=None,
                 parameters=False):

        # The name of this screen.
        if isinstance(name, basestring):
            name = tuple(name.split())

        self.name = name

        screens[name[0], variant] = self

        # The function that is called to display this screen.
        self.function = function

        # Expression: Are we modal? (A modal screen ignores screens under it.)
        self.modal = modal

        # Expression: Our zorder.
        self.zorder = zorder

        # The tag associated with the screen.
        self.tag = tag or name[0]

        # Can this screen be predicted?
        if predict is None:
            predict = renpy.config.predict_screens

        self.predict = predict

        # True if this screen takes parameters via _args and _kwargs.
        self.parameters = parameters


class ScreenDisplayable(renpy.display.layout.Container):
    """
    A screen is a collection of widgets that are displayed together. This
    class is responsible for managing the display of a screen.
    """

    nosave = [ 'screen', 'child', 'transforms', 'widgets', 'old_widgets', 'old_transforms' ]

    restarting = False

    def after_setstate(self):
        self.screen = get_screen_variant(self.screen_name[0])
        self.child = None
        self.transforms = { }
        self.widgets = { }
        self.old_widgets = None
        self.old_transforms = None

    def __init__(self, screen, tag, layer, widget_properties={}, scope={}, **properties):

        super(ScreenDisplayable, self).__init__(**properties)

        # Stash the properties, so we can re-create the screen.
        self.properties = properties

        # The screen, and it's name. (The name is used to look up the
        # screen on save.)
        self.screen = screen
        self.screen_name = screen.name

        # The tag and layer screen was displayed with.
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

        # A map from name to the widget with that name.
        self.widgets = { }

        if tag and layer:
            old_screen = get_screen(tag, layer)
        else:
            old_screen = None

        # A map from name to the transform with that name. (This is
        # taken from the old version of the screen, if it exists.
        if old_screen is not None:
            self.transforms = old_screen.transforms
        else:
            self.transforms = { }

        # What widgets and transforms were the last time this screen was
        # updated. Used to communicate with the ui module, and only
        # valid during an update - not used at other times.
        self.old_widgets = None
        self.old_transforms = None

        # Should we transfer data from the old_screen? This becomes
        # true once this screen finishes updating for the first time,
        # and also while we're using something.
        self.old_transfers = (old_screen and old_screen.screen_name == self.screen_name)

        # The current transform event, and the last transform event to
        # be processed.
        self.current_transform_event = None

        # A dict-set of widgets (by id) that have been hidden from us.
        self.hidden_widgets = { }

        # Are we hiding?
        self.hiding = False

        # Are we restarting?
        self.restarting = False

        # Modal and zorder.
        self.modal = renpy.python.py_eval(self.screen.modal, locals=self.scope)
        self.zorder = renpy.python.py_eval(self.screen.zorder, locals=self.scope)

    def __unicode__(self):
        return "Screen {}".format(" ".join(self.screen_name))

    def visit(self):
        return [ self.child ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        self.update()

    def set_transform_event(self, event):
        super(ScreenDisplayable, self).set_transform_event(event)
        self.current_transform_event = event

    def find_focusable(self, callback, focus_name):
        if self.child and not self.hiding:
            self.child.find_focusable(callback, focus_name)

    def _hide(self, st, at, kind):

        if self.hiding:
            hid = self
        else:
            hid = ScreenDisplayable(self.screen, self.tag, self.layer, self.widget_properties, self.scope, **self.properties)
            hid.transforms = self.transforms.copy()
            hid.widgets = self.widgets.copy()
            hid.old_transfers = True

        hid.hiding = True

        hid.current_transform_event = kind
        hid.update()

        renpy.display.render.redraw(hid, 0)

        rv = None

        # Compute the reverse of transforms and widgets.
        reverse_transforms = dict((id(v), k) for k, v in hid.transforms.iteritems())
        reverse_widgets = dict((id(v), k) for k, v in hid.widgets.iteritems())

        # Assumption: the only displayables that can keep us around
        # are Transforms that handle hide.

        # Iterate over our immediate children, trying to hide them.
        for d in list(hid.child.children):

            id_d = id(d)

            # If we have a transform, call its _hide method. If that comes
            # back non-None, store the new transform, and keep us alive.
            #
            # Otherwise, remove the child.
            name = reverse_transforms.get(id_d, None)

            if name is not None:
                c = d._hide(st, at, kind)

                if c is not None:
                    hid.transforms[name] = c
                    rv = hid
                else:
                    hid.hidden_widgets[name] = True
                    hid.child.remove(d)

                continue

            # Remove any non-transform children.
            name = reverse_widgets.get(id_d, None)

            if name is not None:
                hid.hidden_widgets[name] = True
                hid.child.remove(d)

        return rv

    def update(self):

        # If we're restarting, do not update - the update can use variables
        # that are no longer in scope.
        if self.restarting:
            if not self.child:
                self.child = renpy.display.layout.Null()

            return self.widgets

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
        self.child = renpy.ui.fixed(focus="_screen_" + "_".join(self.screen_name))
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
        self.old_transfers = True

        if self.current_transform_event:

            for i in self.child.children:
                i.set_transform_event(self.current_transform_event)

            self.current_transform_event = None

        return self.widgets

    def render(self, w, h, st, at):

        if not self.child:
            self.update()

        child = renpy.display.render.render(self.child, w, h, st, at)

        rv = renpy.display.render.Render(w, h)

        rv.blit(child, (0, 0), focus=not self.hiding, main=not self.hiding)
        rv.modal = self.modal and not self.hiding

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

        if self.modal:
            raise renpy.display.layout.IgnoreLayers()


# The name of the screen that is currently being displayed, or
# None if no screen is being currently displayed.
_current_screen = None

# A map from (screen_name, variant) tuples to screen.
screens = { }

def get_screen_variant(name):
    """
    Get a variant screen object for `name`.
    """

    for i in renpy.config.variants:
        rv = screens.get((name, i), None)
        if rv is not None:
            return rv

    return None

def define_screen(*args, **kwargs):
    """
    :doc: screens
    :args: (name, function, modal="False", zorder="0", tag=None, variant=None)

    Defines a screen with `name`, which should be a string.

    `function`
        The function that is called to display the screen. The
        function is called with the screen scope as keyword
        arguments. It should ignore additional keyword arguments.

        The function should call the ui functions to add things to the
        screen.

    `modal`
        A string that, when evaluated, determines of the created
        screen should be modal. A modal screen prevents screens
        underneath it from receiving input events.

    `zorder`
        A string that, when evaluated, should be an integer. The integer
        controls the order in which screens are displayed. A screen
        with a greater zorder number is displayed above screens with a
        lesser zorder number.

    `tag`
        The tag associated with this screen. When the screen is shown,
        it replaces any other screen with the same tag. The tag
        defaults to the name of the screen.

    `predict`
        If true, this screen can be loaded for image prediction. If false,
        it can't. Defaults to true.

    `variant`
        String. Gives the variant of the screen to use.

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

    if not name:
        return False

    if get_screen_variant(name[0]):
        return True
    else:
        return False

def show_screen(_screen_name, *_args, **kwargs):
    """
    :doc: screens

    The programmatic equivalent of the show screen statement.

    Shows the named screen. This takes the following keyword arguments:

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

    _layer = kwargs.pop("_layer", "screens")
    _tag = kwargs.pop("_tag", None)
    _widget_properties = kwargs.pop("_widget_properties", {})
    _transient = kwargs.pop("_transient", False)

    name = _screen_name

    if not isinstance(name, tuple):
        name = tuple(name.split())

    screen = get_screen_variant(name[0])

    if screen is None:
        raise Exception("Screen %s is not known.\n" % (name[0],))

    if _tag is None:
        _tag = screen.tag

    scope = { }

    if screen.parameters:
        scope["_kwargs" ] = kwargs
        scope["_args"] = _args
    else:
        scope.update(kwargs)

    d = ScreenDisplayable(screen, _tag, _layer, _widget_properties, scope)
    renpy.exports.show(name, tag=_tag, what=d, layer=_layer, zorder=d.zorder, transient=_transient, munge_name=False)


def predict_screen(_screen_name, *_args, **kwargs):
    """
    Predicts the displayables that make up the given screen.

    `_screen_name`
        The name of the  screen to show.
    `_widget_properties`
        A map from the id of a widget to a property name -> property
        value map. When a widget with that id is shown by the screen,
        the specified properties are added to it.

    Keyword arguments not beginning with underscore (_) are used to
    initialize the screen's scope.
    """

    _widget_properties = kwargs.pop("_widget_properties", {})
    _scope = kwargs.pop

    kwargs["_kwargs" ] = kwargs.copy()
    kwargs["_args"] = _args

    name = _screen_name

    if renpy.config.debug_image_cache:
        renpy.display.ic_log.write("Predict screen %s", name)

    if not isinstance(name, tuple):
        name = tuple(name.split())

    screen = get_screen_variant(name[0])

    scope = { }

    if screen.parameters:
        scope["_kwargs" ] = kwargs
        scope["_args"] = _args
    else:
        scope.update(kwargs)

    try:

        if screen is None:
            raise Exception("Screen %s is not known.\n" % (name[0],))

        if not screen.predict:
            return

        d = ScreenDisplayable(screen, None, None, _widget_properties, scope)

        d.update()
        renpy.display.predict.displayable(d)

    except:
        if renpy.config.debug_image_cache:
            import traceback

            print "While predicting screen", screen
            traceback.print_exc()

    renpy.ui.reset()


def hide_screen(tag, layer='screens'):
    """
    :doc: screens

    The programmatic equivalent of the hide screen statement.

    Hides the screen with `tag` on `layer`.
    """

    screen = get_screen(tag, layer)

    if screen is not None:
        renpy.exports.hide(screen.tag, layer=layer)

def use_screen(_screen_name, *_args, **kwargs):

    _name = kwargs.pop("_name", ())
    _scope = kwargs.pop("_scope", { })

    name = _screen_name

    if not isinstance(name, tuple):
        name = tuple(name.split())

    screen = get_screen_variant(name[0])

    if screen is None:
        raise Exception("Screen %r is not known." % name)

    old_transfers = _current_screen.old_transfers
    _current_screen.old_transfers = True

    scope = _scope.copy()

    if screen.parameters:
        scope["_kwargs"] = kwargs
        scope["_args"] = _args
    else:
        scope.update(kwargs)

    scope["_scope"] = scope
    scope["_name"] = (_name, name)

    screen.function(**scope)

    _current_screen.old_transfers = old_transfers

def current_screen():
    return _current_screen

def get_widget(screen, id, layer='screens'): #@ReservedAssignment
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

def before_restart():
    """
    This is called before Ren'Py restarts to put the screens into restart
    mode, which prevents crashes due to variables being used that are no
    longer defined.
    """

    for k, layer in renpy.display.interface.old_scene.iteritems():
        if k is None:
            continue

        for i in layer.children:
            if isinstance(i, ScreenDisplayable):
                i.restarting = True

