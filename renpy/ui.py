# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# The current widget. (Should never become None.)
current = 'transient'

# A stack of current widgets and/or layers.
current_stack = [ ]

# True if the current widget should be used at most once.
current_once = False

# A stack of open ui.ats.
at_stack = [ ]

def interact(type='misc', **kwargs):
    # Docs in wiki.
    
    if renpy.config.skipping == "fast":
        renpy.config.skipping = None

    if current_stack:
        raise Exception("ui.interact called with non-empty widget/layer stack. Did you forget a ui.close() somewhere?")

    if at_stack:
        raise Exception("ui.interact called with non-empty at stack.")
    
    renpy.game.context().info._current_interact_type = type
    rv = renpy.game.interface.interact(**kwargs)
    renpy.game.context().mark_seen()
    renpy.game.context().info._last_interact_type = type
    return rv

def add(w, make_current=False, once=False):

    w = renpy.easy.displayable(w)

    global current
    global current_once

    atw = w 
    
    while at_stack:
        atw = at_stack.pop()(atw)
    
    if isinstance(current, str):
        renpy.game.context(-1).scene_lists.add(current, atw)
    else:
        current.add(atw)

    if current_once:
        current_once = False
        close()

    current_once = once

    if make_current:
        current_stack.append(current)
        current = w

    return w

def remove(d):
    
    if not isinstance(current, basestring):
        raise Exception("ui.remove only works directly on a layer.")

    renpy.game.context(-1).scene_lists.remove(current, d)
    

def at(a):
    at_stack.append(a)

def clear():

    if isinstance(current, basestring):
        renpy.game.context(-1).scene_lists.clear(current)
    else:
        raise Exception("ui.clear cannot be called when a widget is open.")
    

def layer(name):

    global current_once
    global current

    if not isinstance(current, str):
        raise Exception("Opening a layer while a widget is open is not allowed.")

    if name not in renpy.config.layers and name not in renpy.config.top_layers:
        raise Exception("'%s' is not a known layer." % name)

    current_stack.append(current)
    current_once = False
    current = name

def close(d=None):

    global current

    if not current_stack:
        raise Exception("ui.close() called to close the last open layer or widget.")

    if current_once:
        raise Exception("ui.close() called when expecting a widget.")

    if d is not None and d is not current:
        raise Exception("ui.close() closed %r, not expected %r." % (current, d))
    
    current = current_stack.pop()

def reopen(w, clear):

    global current
    
    current_stack.append(current)
    current = w

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



def keymousebehavior():
    """
    As of 4.8, this does nothing, but is retained for compatability.
    """

    return

def keymap(**kwargs):
    return add(renpy.display.behavior.Keymap(**kwargs))

def saybehavior(*args, **kwargs):
    return add(renpy.display.behavior.SayBehavior(*args, **kwargs))

def pausebehavior(delay, result=False):

    return add(renpy.display.behavior.PauseBehavior(delay, result))

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
                def clicked(val=val):
                    return val

            button = getattr(renpy.game.style, button)[label]
            text = getattr(renpy.game.style, text)[label]
                
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

def imagemap(ground, selected, hotspots, unselected=None,
             style='imagemap', button_style='imagemap_button',
             **properties):

    rv = fixed(style=style, **properties)

    if not unselected:
        unselected = ground

    image(ground)

    for x0, y0, x1, y1, result in hotspots:

        imagebutton(renpy.display.layout.LiveCrop((x0, y0, x1 - x0, y1 - y0), unselected),
                    renpy.display.layout.LiveCrop((x0, y0, x1 - x0, y1 - y0), selected),
                    clicked=returns(result),
                    style=button_style,
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

def viewport(**properties):
    return add(renpy.display.layout.Viewport(**properties), True, True)


def conditional(condition):

    return add(renpy.display.behavior.Conditional(condition), True, True)

def timer(delay, function, repeat=False, args=(), kwargs={}):

    return add(renpy.display.behavior.Timer(delay, function, repeat=repeat, args=args, kwargs=kwargs))

def _returns(v):

    return v

returns = renpy.curry.curry(_returns)


def _jumps(label):

    raise renpy.game.JumpException(label)

jumps = renpy.curry.curry(_jumps)


def _jumpsoutofcontext(label):

    raise renpy.game.JumpOutException(label)

jumpsoutofcontext = renpy.curry.curry(_jumpsoutofcontext)

def callsinnewcontext(*args, **kwargs):
    return renpy.exports.curried_call_in_new_context(*args, **kwargs)

def invokesinnewcontext(*args, **kwargs):
    return renpy.exports.curried_invoke_in_new_context(*args, **kwargs)
