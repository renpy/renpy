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

import sets

import renpy

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

    def __init__(self, displayable):
        self.displayable = displayable

    def add(self, d, key):
        self.displayable.add(d)

    def close(self, d):
        stack.pop()

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


# Called at the end of the init phase.
def _ready():
    global stack
    stack = [ Layer('master') ]

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
    
def add(w, many=False, one=False):

    global current
    global current_once
    global add_tag
    
    w = renpy.easy.displayable(w)
    w = w.parameterize('displayable', [ ])
    
    atw = w 
    
    while at_stack:
        atf = at_stack.pop()
        if isinstance(atf, renpy.display.motion.Transform):
            atw = atf(child=atw)
        else:
            atw = atf(atw)

    stack[-1].add(atw, add_tag)

    if one:
        stack.append(One(w))
    elif many:
        stack.append(Many(w))
        
    add_tag = None
    
    return w

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

def null(**properties):

    return add(renpy.display.layout.Null(**properties))

def text(label, **properties):

    return add(renpy.display.text.Text(label, **properties))

def hbox(spacing=None, style='hbox', **properties):

    return add(renpy.display.layout.MultiBox(spacing=spacing, layout="horizontal", style=style, **properties), True)

def vbox(spacing=None, style='vbox', **properties):

    return add(renpy.display.layout.MultiBox(spacing=spacing, layout="vertical", style=style, **properties), True)

def grid(cols, rows, padding=0, transpose=False, **properties):

    return add(renpy.display.layout.Grid(cols, rows, padding, transpose=transpose, **properties), True)

def fixed(**properties):

    rv = renpy.display.layout.MultiBox(layout='fixed', **properties)
    add(rv, True)

    return rv

def side(positions, **properties):
    rv = renpy.display.layout.Side(positions, **properties)
    add(rv, True)

    return rv

def sizer(maxwidth=None, maxheight=None, **properties):
    
    return add(renpy.display.layout.Container(xmaximum=maxwidth, ymaximum=maxheight, **properties),
               True, True)

def window(**properties):

    return add(renpy.display.layout.Window(None, **properties), True, True)

def frame(**properties):

    properties.setdefault('style', 'frame')

    return add(renpy.display.layout.Window(None, **properties), True, True)

# As of 4.8, this does nothing, but is retained for compatability.
def keymousebehavior():
    return

def keymap(**kwargs):
    return add(renpy.display.behavior.Keymap(**kwargs))

def saybehavior(*args, **kwargs):
    return add(renpy.display.behavior.SayBehavior(*args, **kwargs))

def pausebehavior(delay, result=False):
    return add(renpy.display.behavior.PauseBehavior(delay, result))

def soundstopbehavior(channel, result=False):
    return add(renpy.display.behavior.SoundStopBehavior(channel, result))

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
                chosen = renpy.game.persistent._chosen.setdefault(location, sets.Set())
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

    renpy.ui.close()

    # return add(renpy.display.behavior.Menu(menuitems, **properties))

def input(default, length=None, allow=None, exclude='{}', **properties):

    return add(renpy.display.behavior.Input(default, length=length, allow=allow, exclude=exclude, **properties))

def image(im, **properties):

    return add(renpy.display.im.image(im, loose=True, **properties))

def imagemap(ground,
             selected,
             hotspots,
             unselected=None,
             style='imagemap',
             button_style='imagemap_button',
             **properties):

    if isinstance(button_style, basestring):
        button_style = getattr(renpy.game.style, button_style)
    
    rv = fixed(style=style, **properties)

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

    return rv
                                            
def button(clicked=None, **properties):

    return add(renpy.display.behavior.Button(None, clicked=clicked,
                                      **properties), True, True)

def textbutton(text, clicked=None, text_style='button_text', **properties):

    return add(renpy.display.behavior.TextButton(text, clicked=clicked,
                                                 text_style=text_style,
                                                 **properties))
def imagebutton(idle_image,
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
    
    return add(renpy.display.image.ImageButton(
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
            **properties))

def adjustment(range=1, value=0, step=None, page=0, changed=None):
    return renpy.display.behavior.Adjustment(range=range, value=value, step=step, page=page, changed=changed)

def bar(*args, **properties):

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

    return add(renpy.display.behavior.Bar(range, value, width, height,
                                          **properties))
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

def autobar(range, start, end, time, **properties):
    return add(renpy.display.layout.DynamicDisplayable(autobar_interpolate(range, start, end, time, **properties)))

def transform(**properties):
    return add(renpy.display.layout.Transform(**properties), True, True)

def viewport(**properties):
    return add(renpy.display.layout.Viewport(**properties), True, True)

def conditional(condition):
    return add(renpy.display.behavior.Conditional(condition), True, True)

def timer(delay, function, repeat=False, args=(), kwargs={}):
    return add(renpy.display.behavior.Timer(delay, function, repeat=repeat, args=args, kwargs=kwargs))

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
