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

# This file contains functions that can be used to display a UI on the
# screen.  The UI isn't implemented here (rather, in
# renpy.display). Instead, these functions provide a simple interface
# that allows a user to procedurally create a UI.

# All functions in the is file should be documented in the wiki.

import sys
import renpy


##############################################################################
# Special classes that can be subclassed from the outside.

class Action(renpy.object.Object):
    """
    This can be passed to the clicked method of a button or hotspot. It is
    called when the action is selected. The other methods determine if the
    action should be displayed insensitive or disabled.
    """

    def get_sensitive(self):
        return True

    def get_selected(self):
        return False

    def periodic(self, st):
        return
    
    def __call__(self):
        raise NotImplemented()
    
class BarValue(renpy.object.Object):
    """
    This can be passed to the value method of bar and hotbar.
    """

    def replaces(self, other):
        return

    def periodic(self, st):
        return
    
    def get_adjustment(self):
        raise NotImplemented()

    def get_style(self):
        return "bar", "vbar"

    
##############################################################################
# Things we can add to. These have two methods: add is called with the
# widget we're adding. close is called when the thing is ready to be
# closed.

class Addable(object):
    def get_layer(self):
        return Exception("Operation can only be performed on a layer.")

class Layer(Addable):
    def __init__(self, name):
        self.name = name

    def add(self, d, key):
        renpy.game.context(-1).scene_lists.add(self.name, d, key=key)

    def close(self, d):
        stack.pop()

        if d and d != self.name:
            raise Exception("ui.close closed layer %s, not the expected %r." % (self.name, d))
        
    def get_layer(self):
        return self.name

        
class Many(Addable):
    """
    A widget that takes many children.
    """

    def __init__(self, displayable, imagemap):
        self.displayable = displayable
        self.imagemap = False
        
    def add(self, d, key):
        self.displayable.add(d)

    def close(self, d):
        stack.pop()

        if self.imagemap:
            imagemap_stack.pop()
        
        if d and d != self.displayable:
            raise Exception("ui.close closed %r, not the expected %r." % (self.displayable, d))

class One(Addable):
    """
    A widget that expects exactly one child.
    """
    
    def __init__(self, displayable):
        self.displayable = displayable

    def add(self, d, key):
        self.displayable.add(d)
        stack.pop()
        
    def close(self, d):
        raise Exception("Widget expects a child.")

class Detached(Addable):
    """
    Used to indicate a widget is detached from the stack.
    """

    def add(self, d, key):
        stack.pop()

    def close(self, d):
        raise Exception("Detached expects to be given a child.")
    
class ChildOrFixed(Addable):
    """
    If one widget is added, then it is added directly to our
    parent. Otherwise, a fixed is added to our parent, and all
    the widgets are added to that.
    """

    def __init__(self):
        self.queue = [ ]

    def add(self, d, key):
        self.queue.append(d)

    def close(self, d):
        stack.pop()

        if len(self.queue) == 1:
            add(self.queue[0])
        else:
            fixed()

            for i in self.queue:
                add(i)

            close()
                
        if d is not None:
            raise Exception("Did not expect to close %r." % d)

# A stack of things we can add to.
stack = [ ]

# A stack of open ui.ats.
at_stack = [ ]

# The tag for the displayble being added to the layer.
add_tag = None

# A stack of Imagemap objects.
imagemap_stack = [ ]
            

# Called at the end of the init phase.
def _ready():
    global stack
    stack = [ Layer('transient') ]

renpy.game.post_init.append(_ready)
    
def interact(type='misc', **kwargs):
    # Docs in wiki.

    if stack is None:
        raise Exception("Interaction not allowed during init phase.")
    
    if renpy.config.skipping == "fast":
        renpy.config.skipping = None

    if len(stack) != 1:
        raise Exception("ui.interact called with non-empty widget/layer stack. Did you forget a ui.close() somewhere?")
    
    if at_stack:
        raise Exception("ui.interact called with non-empty at stack.")
    
    renpy.game.context().info._current_interact_type = type
    rv = renpy.game.interface.interact(**kwargs)
    renpy.game.context().mark_seen()
    renpy.game.context().info._last_interact_type = type
    return rv

def tag(name):
    global add_tag
    add_tag = name

def child_or_fixed():
    """
    Causes the current widget to be given child-fixed semantics. This
    means that we will queue up children added to it. If there is one
    child, that child will be added to the widget directly. Otherwise,
    a fixed will be created, and the children will be added to that.
    """

    stack.append(ChildOrFixed())
    
def remove(d):
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.remove(layer, d)

def remove_above(d):
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.remove_above(layer, d)
    
def at(transform):
    """
    :doc: ui
    
    Specifieds a transform that is applied to the next displayable to
    be created. This is largely obsolete, as all UI functions now take
    an `at` argument.
    """
    
    at_stack.append(transform)

def clear():
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.clear(layer)

def detached():
    """
    :doc: ui

    Do not add the next displayable to any later or container. Use this if
    you want to assign the result of a ui function to a variable.
    """
    
    stack.append(Detached())
    
def layer(name):
    """
    :doc: ui

    Adds displayables to the layer named `name`. The later must be
    closed with :func:`ui.close`.
    """

    stack.append(Layer(name))
    
def close(d=None):
    """
    :doc: ui
    :args: ()

    Closes a displayable created with by a UI function. When a
    displayable is closed, we add new displayables to its parent,
    or to the layer if no displayable is open.
    """

    stack[-1].close(d)

    if not stack:
        raise Exception("ui.close() called when no layer or widget is open.")
    
def reopen(w, clear):

    stack.append(Many(w))

    if clear:
        w.children[:] = [ ]

def context_enter(w):
    if isinstance(renpy.ui.stack[-1], renpy.ui.Many) and renpy.ui.stack[-1].displayable is w:
        return

    raise Exception("%r cannot be used as a context manager.", type(w).__name__)

def context_exit(w):
    close(w)


# The screen we're using as we add widgets. None if there isn't a
# screen.
screen = None
    
class Wrapper(renpy.object.Object):

    def __reduce__(self):
        return self.name
    
    def __init__(self, function, one=False, many=False, imagemap=False, replaces=False, **kwargs):

        # The name assigned to this wrapper. This is used to serialize us correctly.
        self.name = None

        # The function to call.
        self.function = function

        # Should we add one or many things to this wrapper?
        self.one = one
        self.many = many or imagemap
        self.imagemap = imagemap

        # Should the function be given the replaces parameter,
        # specifiying the displayable it replaced?
        self.replaces = replaces
        
        # Default keyword arguments to the function.
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):

        global add_tag

        # Pull out the special kwargs, id and at.

        id = kwargs.pop("id", None)

        at_list = kwargs.pop("at", [ ])
        if not isinstance(at_list, list):
            at_list = [ at_list ]
            
        # Figure out the keyword arguments, based on the parameters.

        if self.kwargs:
            keyword = self.kwargs.copy()
            keyword.update(kwargs)
        else:
            keyword = kwargs

        if screen:
            if id in screen.widget_properties:
                keyword.update(screen.widget_properties[id])

            if self.replaces:
                keyword["replaces"] = screen.old_widgets.get(id, None)

        try:
            w = self.function(*args, **keyword)

        # We want to rewrite the type error so that it mentions our name,
        # so the user gcan figure out WTF is going on.
        except TypeError:
            etype, e, tb = sys.exc_info(); etype

            if tb.tb_next is None:
                e.args = (e.args[0].replace("__init__", "ui." + self.name), )

            del tb # Important! Prevents memory leaks via our frame.
            raise

        # Wrap the displayable based on the at_list and at_stack.
        atw = w 

        while at_stack:
            at_list.append(at_stack.pop())
        
        for atf in at_list:
            if isinstance(atf, renpy.display.motion.Transform):
                atw = atf(child=atw)
            else:
                atw = atf(atw)

        # Add to the displayable at the bottom of the stack.

        if stack:
            stack[-1].add(atw, add_tag)
        else:
            raise Exception("Can't add displayable during init phase.")
            
        # Update the stack, as necessary.
        if self.one:
            stack.append(One(w))
        elif self.many:
            stack.append(Many(w, self.imagemap))

        # If we have an id, record the displayable, the transform,
        # and maybe take the state from a previous transform.
        if screen and id is not None:
            screen.widgets[id] = w

            if isinstance(atw, renpy.display.motion.Transform):
                screen.transforms[id] = atw

                oldt = screen.old_transforms.get(id, None)

                if oldt is not None:
                    atw.take_state(oldt)
                    atw.take_execution_state(oldt)

        # Clear out the add_tag.
        add_tag = None

        return w

##############################################################################
# Button support functions
def is_selected(clicked):

    if isinstance(clicked, (list, tuple)):
        return any(is_selected(i) for i in clicked)

    elif isinstance(clicked, Action):
        return clicked.get_selected()

    else:
        return False

def is_sensitive(clicked):

    if isinstance(clicked, (list, tuple)):
        return all(is_sensitive(i) for i in clicked)

    elif isinstance(clicked, Action):
        return clicked.get_sensitive()

    else:
        return True

    

##############################################################################
# Widget functions.
        
def _add(d, **kwargs):
    d = renpy.easy.displayable(d)
    d = d.parameterize('displayable', [ ])
    
    rv = d
    
    if kwargs:
        rv = renpy.display.motion.Transform(child=d, **kwargs)

    return rv

add = Wrapper(_add)

def _image(im, **properties):
    d = renpy.display.im.image(im, loose=True, **properties)
    d = d.parameterize('displayable', [ ])
    return d
    
image = Wrapper(_image)

null = Wrapper(renpy.display.layout.Null)
text = Wrapper(renpy.display.text.Text, replaces=True)
hbox = Wrapper(renpy.display.layout.MultiBox, layout="horizontal", style="hbox", many=True)
vbox = Wrapper(renpy.display.layout.MultiBox, layout="vertical", style="vbox", many=True)
fixed = Wrapper(renpy.display.layout.MultiBox, layout="fixed", many=True)
grid = Wrapper(renpy.display.layout.Grid, many=True)
side = Wrapper(renpy.display.layout.Side, many=True)

def _sizer(maxwidth=None, maxheight=None, **properties):
    return renpy.display.layout.Container(xmaximum=maxwidth, ymaximum=maxheight, **properties)

sizer = Wrapper(_sizer, one=True)
window = Wrapper(renpy.display.layout.Window, one=True, child=None)
frame = Wrapper(renpy.display.layout.Window, style='frame', one=True, child=None)

keymap = Wrapper(renpy.display.behavior.Keymap)
saybehavior = Wrapper(renpy.display.behavior.SayBehavior)
pausebehavior = Wrapper(renpy.display.behavior.PauseBehavior)
soundstopbehavior = Wrapper(renpy.display.behavior.SoundStopBehavior)

def _key(key, action=None):

    if action is None:
        raise Exception("Action is required in ui.key.")
    
    return renpy.display.behavior.Keymap(**{ key : action})

key = Wrapper(_key)

def menu(menuitems,
         style = 'menu',
         caption_style='menu_caption',
         choice_style='menu_choice',
         choice_chosen_style='menu_choice_chosen',
         choice_button_style='menu_choice_button',
         choice_chosen_button_style='menu_choice_chosen_button',
         location=None,
         focus=None,
         default=False,
         **properties):

    # menu is now a conglomeration of other widgets. And bully for it.

    renpy.ui.vbox(style=style, **properties)

    for label, val in menuitems:
        if val is None:
            renpy.ui.text(label, style=caption_style)
        else:

            text = choice_style
            button = choice_button_style
                        
            if location:
                chosen_dict = renpy.game.persistent._chosen

                if location not in chosen_dict or not isinstance(chosen_dict[location], set):
                    chosen_dict[location] = set()

                chosen = chosen_dict[location]
                
                if label in chosen:
                    text = choice_chosen_style
                    button = choice_chosen_button_style

                def clicked(chosen=chosen, label=label, val=val):
                    chosen.add(label)
                    return val
            else:
                clicked = renpy.ui.returns(val)

            if isinstance(button, basestring):
                button = getattr(renpy.game.style, button)
            if isinstance(text, basestring):
                text = getattr(renpy.game.style, text)

            button = button[label]
            text = text[label]
            
            renpy.ui.textbutton(label,
                                style=button,
                                text_style=text,
                                clicked=clicked,
                                focus=focus,
                                default=default)
            
    close()
    
input = Wrapper(renpy.display.behavior.Input, exclude='{}', replaces=True)

def imagemap_compat(ground,
                    selected,
                    hotspots,
                    unselected=None,
                    style='imagemap',
                    button_style='imagemap_button',
                    **properties):

    if isinstance(button_style, basestring):
        button_style = getattr(renpy.game.style, button_style)

    fixed(style=style, **properties)

    if unselected is None:
        unselected = ground

    add(ground)

    for x0, y0, x1, y1, result in hotspots:

        if result is None:
            continue
            
        imagebutton(renpy.display.layout.LiveCrop((x0, y0, x1 - x0, y1 - y0), unselected),
                    renpy.display.layout.LiveCrop((x0, y0, x1 - x0, y1 - y0), selected),
                    clicked=returns(result),
                    style=button_style[result],
                    xpos=x0,
                    xanchor=0,
                    ypos=y0,
                    yanchor=0,
                    focus_mask=True,
                    )

    close()

button = Wrapper(renpy.display.behavior.Button, one=True)

def _imagebutton(idle_image = None,
                 hover_image = None,                 
                 insensitive_image = None,
                 activate_image = None,
                 selected_idle_image = None,
                 selected_hover_image = None,
                 selected_insensitive_image = None,
                 selected_activate_image = None,    
                 idle=None,
                 hover=None,
                 insensitive=None,
                 selected_idle=None,
                 selected_hover=None,
                 selected_insensitive=None,
                 style='image_button',
                 image_style=None,
                 auto=None,
                 **properties):

    def choice(a, b, name):
        if a:
            return a
        if b:
            return b
        if auto is not None:
            return auto % name

        return auto
    
    idle = choice(idle, idle_image, "idle")
    hover = choice(hover, hover_image, "hover")
    insensitive = choice(insensitive, insensitive_image, "insensitive")
    selected_idle = choice(selected_idle, selected_idle_image, "selected_idle")
    selected_hover = choice(selected_hover, selected_hover_image, "selected_hover")
    selected_insensitive = choice(selected_insensitive, selected_insensitive_image, "selected_insensitive")
    
    return renpy.display.image.ImageButton(
            idle,
            hover,
            insensitive_image = insensitive,
            activate_image = activate_image,
            selected_idle_image = selected_idle,
            selected_hover_image = selected_hover,
            selected_insensitive_image = selected_insensitive,
            selected_activate_image = selected_activate_image,    
            style=style,
            **properties)
    
imagebutton = Wrapper(_imagebutton)

def get_text_style(style, default):
    if isinstance(style, basestring):
        base = style
        rest = ()
    else:
        print style
        base = style.name[0]
        rest = style.name[1:]

    base = base + "_text"

    rv = renpy.style.style_map.get(base, None)

    if rv is None:
        rv = renpy.style.style_map[default]

    for i in rest:
        rv = rv[i]

    return rv

def textbutton(label, clicked=None, style='button', text_style=None, **kwargs):

    if text_style is None:
        text_style = get_text_style(style, 'button_text')

    button(style=style, clicked=clicked, **kwargs)
    text(label, style=text_style)

def label(label, style='label', text_style=None, **kwargs):

    if text_style is None:
        text_style = get_text_style(style, 'label_text')

    window(style=style, **kwargs)
    text(label, style=text_style)

adjustment = renpy.display.behavior.Adjustment

def _bar(*args, **properties):

    if len(args) == 4:
        width, height, range, value = args
    if len(args) == 2:
        range, value = args
        width = None
        height = None
    else:
        range = 1
        value = 0
        width = None
        height = None

    if "width" in properties:
        width = properties.pop("width")

    if "height" in properties:
        height  = properties.pop("height")

    if "range" in properties:
        range = properties.pop("range")
         
    if "value" in properties:
        value = properties.pop("value")

    return renpy.display.behavior.Bar(range, value, width, height, **properties)

bar = Wrapper(_bar, style=None, vertical=False, replaces=True)
vbar = Wrapper(_bar, style=None, vertical=True, replaces=True)
slider = Wrapper(_bar, style='slider', replaces=True)
vslider = Wrapper(_bar, style='vslider', replaces=True)
scrollbar = Wrapper(_bar, style='scrollbar', replaces=True)
vscrollbar = Wrapper(_bar, style='vscrollbar', replaces=True)

def _autobar_interpolate(range, start, end, time, st, at, **properties):

    if st > time:
        t = 1.0
        redraw = None
    else:
        t = st / time
        redraw = 0
        
    value = start + t * (end - start)
    return renpy.display.behavior.Bar(range, value, None, None, **properties), redraw

autobar_interpolate = renpy.curry.curry(_autobar_interpolate)

def _autobar(range, start, end, time, **properties):
    return renpy.display.layout.DynamicDisplayable(autobar_interpolate(range, start, end, time, **properties))

autobar = Wrapper(_autobar)
transform = Wrapper(renpy.display.motion.Transform, one=True)
viewport = Wrapper(renpy.display.layout.Viewport, one=True, replaces=True)
conditional = Wrapper(renpy.display.behavior.Conditional, one=True)
timer = Wrapper(renpy.display.behavior.Timer, replaces=True)


##############################################################################
# New-style imagemap related functions.

class Imagemap(object):
    """
    Stores information about the images used by an imagemap.
    """

    def __init__(self, insensitive, idle, selected_idle, hover, selected_hover):
        self.insensitive = insensitive
        self.idle = idle
        self.selected_idle = selected_idle
        self.hover = hover
        self.selected_hover = selected_hover

def _imagemap(ground=None, hover=None, insensitive=None, idle=None, selected_hover=None, selected_idle=None, auto=None, style='imagemap', **properties):

    def pick(variable, name, other):
        if variable:
            return variable

        if auto:
            fn = auto % name
            if renpy.loader.loadable(fn):
                return fn

        if other is not None:
            return other

        raise Exception("Could not find a %s image for imagemap." % name)


    ground = pick(ground, "ground", None)
    idle = pick(idle, "idle", ground)
    selected_idle = pick(selected_idle, "selected_idle", idle)
    hover = pick(hover, "hover", ground)
    selected_hover = pick(selected_hover, "selected_hover", hover)
    insensitive = pick(insensitive, "insensitive", idle)

    imagemap_stack.append(
        Imagemap(
            insensitive,
            idle,
            selected_idle,
            hover,
            selected_hover))

    rv = renpy.display.layout.MultiBox(layout='fixed', **properties)

    if ground:
        rv.add(renpy.easy.displayable(ground))
        
    return rv
    
imagemap = Wrapper(_imagemap, imagemap=True, style='imagemap')

def _hotspot(spot, style='imagemap_button', **properties):

    if not imagemap_stack:
        raise Exception("hotspot expects an imagemap to be defined.")

    imagemap = imagemap_stack[-1]

    x, y, w, h = spot

    idle = imagemap.idle
    hover = imagemap.hover
        
    idle = renpy.display.layout.LiveCrop(spot, idle)
    hover = renpy.display.layout.LiveCrop(spot, hover)
            
    properties.setdefault("xpos", x)
    properties.setdefault("xanchor", 0)
    properties.setdefault("ypos", y)
    properties.setdefault("yanchor", 0)
    properties.setdefault("xminimum", w)
    properties.setdefault("xmaximum", w)
    properties.setdefault("yminimum", h)
    properties.setdefault("ymaximum", h)
    
    return renpy.display.behavior.Button(
        None,
        idle_background=idle,
        hover_background=hover,
        style=style,
        **properties)

hotspot_with_child = Wrapper(_hotspot, style="hotspot", one=True)

def hotspot(*args, **kwargs):
    hotspot_with_child(*args, **kwargs)
    null()

def _hotbar(spot, adjustment=None, range=None, value=None, **properties):

    if isinstance(value, BarValue):
        adjustment = value()
        range = None
        value = None

    if adjustment is None and range is not None and value is not None:
        adjustment = renpy.ui.adjustment(range=range, value=value)
        
    if adjustment is None:
        raise Exception("hotbar requires either an adjustment or a range and value.")

    if not imagemap_stack:
        raise Exception("hotbar expects an imagemap to be defined.")

    imagemap = imagemap_stack[-1]

    x, y, w, h = spot

    properties.setdefault("xpos", x)
    properties.setdefault("ypos", y)
    properties.setdefault("xanchor", 0)
    properties.setdefault("yanchor", 0)

    fore_bar=renpy.display.layout.LiveCrop(spot, imagemap.selected_idle)
    aft_bar=renpy.display.layout.LiveCrop(spot, imagemap.idle)
    hover_fore_bar=renpy.display.layout.LiveCrop(spot, imagemap.selected_hover)
    hover_aft_bar=renpy.display.layout.LiveCrop(spot, imagemap.hover)

    
    if h > w:
        properties.setdefault("bar_vertical", True)
        properties.setdefault("bar_invert", True)

        fore_bar, aft_bar = aft_bar, fore_bar
        hover_fore_bar, hover_aft_bar = hover_aft_bar, hover_fore_bar
        
    return renpy.display.behavior.Bar(
            adjustment=adjustment,
            fore_bar=fore_bar,
            aft_bar=aft_bar,
            hover_fore_bar=hover_fore_bar,
            hover_aft_bar=hover_aft_bar,
            fore_gutter=0,
            aft_gutter=0,
            bar_resizing=False,
            thumb=None,
            thumb_shadow=None,
            thumb_offset=0,
            xmaximum=w,
            ymaximum=h,
            **properties)

hotbar = Wrapper(_hotbar, style="hotbar")
    

##############################################################################
# Curried functions, for use in clicked, hovered, and unhovered.

def _returns(v):

    return v

returns = renpy.curry.curry(_returns)

def _jumps(label, transition=None):

    if isinstance(transition, basestring):
        transition = getattr(renpy.config, transition)

    if transition is not None:
        renpy.exports.transition(transition)
    
    raise renpy.exports.jump(label)

jumps = renpy.curry.curry(_jumps)

def _jumpsoutofcontext(label):

    raise renpy.game.JumpOutException(label)

jumpsoutofcontext = renpy.curry.curry(_jumpsoutofcontext)

def callsinnewcontext(*args, **kwargs):
    return renpy.exports.curried_call_in_new_context(*args, **kwargs)

def invokesinnewcontext(*args, **kwargs):
    return renpy.exports.curried_invoke_in_new_context(*args, **kwargs)

def gamemenus(*args):
    return callsinnewcontext("_game_menu", *args)

##############################################################################
# The on statement.
def on(event, action=[], id=None):
    if renpy.display.screen.current_screen().current_transform_event != event:
        return

    if isinstance(action, (list, tuple)):
        for i in action:
            i()
    else:
        action()


##############################################################################
# Postamble

# Update the wrappers to have names.
k, v = None, None
for k, v in globals().iteritems():
    if isinstance(v, Wrapper):
        v.name = k
