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
        return False

    def get_selected(self):
        return False

    def __call__(self):
        return None
    

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
        
        if d and d != self.name:
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
            for i in self.queue:
                add(i)

        if d is not None:
            raise Exception("Did not expect to close %r." % d)

# A stack of things we can add to.
stack = None

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

def child_fixed():
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
    
def at(a):
    at_stack.append(a)

def clear():
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.clear(layer)

def detached():
    stack.append(Detached())
    
def layer(name):
    stack.append(Layer(name))
    
def close(d=None):

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
        
class Wrapper(renpy.object.Object):

    def __reduce__(self):
        return self.name
    
    def __init__(self, function, one=False, many=False, imagemap=False, **kwargs):

        # The name assigned to this wrapper. This is used to serialize us correctly.
        self.name = None

        # The function to call.
        self.function = function

        # Should we add one or many things to this wrapper?
        self.one = one
        self.many = many or imagemap
        self.imagemap = imagemap
        
        # Default keyword arguments to the function.
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):

        global add_tag

        # Pull out the special kwargs, id and at.
        if "id" in kwargs:
            id = kwargs.pop("id")
        else:
            id = None
            
        if "at" in kwargs:
            at_list = kwargs.pop("at") + at_stack
        else:
            at_list = [ ]
            
        # Figure out the keyword arguments, based on the parameters.
        keyword = self.kwargs.copy()
        keyword.update(kwargs)

        if id is not None:
            keyword.update(renpy.store._widget_properties.get(id, { }))

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
            
        w = renpy.easy.displayable(w)
        w = w.parameterize('displayable', [ ])

        # Wrap the displayable based on the at_list and at_stack.
        atw = w 

        while at_stack:
            at_list.append(at_stack.pop())
        
        for atf in at_list:
            if isinstance(atf, renpy.display.motion.Transform):
                atw = atf(child=atw)
            else:
                atw = atf(atw)

        # Add to the stack.
        stack[-1].add(atw, add_tag)

        # Update the stack, as necessary.
        if self.one:
            stack.append(One(w))
        elif self.many:
            stack.append(Many(w, self.imagemap))

        # If we have an id, record the displayable.
        if id is not None and renpy.store._widget_by_id is not None:
            renpy.store._widget_by_id[id] = w

        # Clear out the add_tag and 
        add_tag = None

        return w


##############################################################################
# Widget functions.
        
def _add(d):
    return d

add = Wrapper(_add)
null = Wrapper(renpy.display.layout.Null)
text = Wrapper(renpy.display.text.Text)
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
                chosen = renpy.game.persistent._chosen.setdefault(location, set)
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
    
input = Wrapper(renpy.display.behavior.Input, exclude='{}')

def _image(im, **properties):
    return renpy.display.im.image(im, loose=True, **properties)

image = Wrapper(_image)

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

def _button(clicked=None, **properties):
    # TODO: Deal with role and enabled automatically, if we can.

    rv = renpy.display.behavior.Button(None, clicked=clicked, **properties)
    return rv

button = Wrapper(_button, one=True)

def _imagebutton(idle_image,
                 hover_image,
                 insensitive_image = None,
                 activate_image = None,
                 selected_idle_image = None,
                 selected_hover_image = None,
                 selected_insensitive_image = None,
                 selected_activate_image = None,    
                 clicked=None,
                 style='image_button',
                 image_style=None,
                 **properties):
    
    return renpy.display.image.ImageButton(
            idle_image,
            hover_image,
            insensitive_image = insensitive_image,
            activate_image = activate_image,
            selected_idle_image = selected_idle_image,
            selected_hover_image = selected_hover_image,
            selected_insensitive_image = selected_insensitive_image,
            selected_activate_image = selected_activate_image,    
            clicked=clicked,
            style=style,
            **properties)
    
imagebutton = Wrapper(_imagebutton)

def textbutton(text, text_style='button_text', **kwargs):
    button(**kwargs)
    text(text, style=text_style)

def adjustment(range=1, value=0, step=None, page=0, changed=None):
    return renpy.display.behavior.Adjustment(range=range, value=value, step=step, page=page, changed=changed)

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

    return renpy.display.behavior.Bar(range, value, width, height, **properties)

bar = Wrapper(_bar, style='bar')
vbar = Wrapper(_bar, style='vbar')
slider = Wrapper(_bar, style='slider')
vslider = Wrapper(_bar, style='vslider')
scrollbar = Wrapper(_bar, style='scrollbar')
vscrollbar = Wrapper(_bar, style='vscrollbar')

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
viewport = Wrapper(renpy.display.layout.Viewport, one=True)
conditional = Wrapper(renpy.display.behavior.Conditional, one=True)
timer = Wrapper(renpy.display.behavior.Timer)


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
        self.hover = selected_hover
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
    insensitive = pick(insensitive, "insensitive", ground)
    idle = pick(idle, "idle", ground)
    selected_idle = pick(selected_idle, "selected_idle", idle)
    hover = pick(hover, "hover", ground)
    selected_hover = pick(selected_hover, "selected_hover", hover)

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

def _hotspot(spot, clicked=None, **properties):

    if not imagemap_stack:
        raise Exception("hotspot expects an imagemap to be defined.")

    imagemap = imagemap_stack[-1]

    x, y, w, h = spot

    idle = imagemap.idle
    hover = imagemap.hover
    role = ""
        
    if isinstance(clicked, Action):

        if not clicked.get_sensitive():
            clicked = None
            idle = imagemap.insensitive
            hover = imagemap.insensitive

        elif clicked.get_selected():
            idle = imagemap.selected_idle
            hover = imagemap.selected_hover
            role = "selected_"

    idle = renpy.display.layout.LiveCrop(spot, idle)
    hover = renpy.display.layout.LiveCrop(spot, hover)
            
    properties.setdefault("xpos", x)
    properties.setdefault("xanchor", 0)
    properties.setdefault("ypos", y)
    properties.setdefault("yanchor", 0)
            
    return renpy.display.image.ImageButton(
        idle,
        hover,
        clicked=clicked,
        role=role,
        **properties)

hotspot = Wrapper(_hotspot, style="hotspot")


    

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
# Postamble

# Update the wrappers to have names.
k, v = None, None
for k, v in globals().iteritems():
    if isinstance(v, Wrapper):
        v.name = k
