# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
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

# The functions in this file work in terms of a current widget. By
# default, the current widget is the screen. Each call to a function
# creates a new widget, and adds it to the current widget. In
# addition, some calls will also update the current widget, pushing
# the old current widget onto a stack. (For example, boxes and buttons
# all can contain other widgets.) The close function pops things off
# the stack.

# The stack should always be empty when we go to interact with the
# user.

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
    
    rv = renpy.game.interface.interact(**kwargs)
    renpy.game.context().mark_seen()
    renpy.game.context().info._last_interact_type = type
    return rv

def add(w, make_current=False, once=False):
    """
    This is used to add a displayable to the current widget. If
    make_current is True, then the widget is made the current
    widget. If once is True, then the displayable will be made the current
    widget, but only for the next widget to be added.
    """

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

def at(a):
    at_stack.append(a)

def clear():
    """
    Clears the current layer of widgets.
    """

    if isinstance(current, str):
        renpy.game.context(-1).scene_lists.clear(current)
    else:
        raise Exception("ui.clear cannot be called when a widget is open.")
    

def layer(name):
    """
    This causes widgets to be added to the named layer, until a 
    matching call to ui.close().
    """

    global current_once
    global current

    if not isinstance(current, str):
        raise Exception("Opening a layer while a widget is open is not allowed.")

    if name not in renpy.config.layers and name not in renpy.config.top_layers:
        raise Exception("'%s' is not a known layer." % name)

    current_stack.append(current)
    current_once = False
    current = name

def close():
    """
    This closes the currently open widget or layer. If a widget is
    closed, then we start adding to its parent, or the layer if no
    parent is open. If a layer is closed, we return to the previously
    open layer. An error is thrown if we close the last open layer.
    """

    global current

    if not current_stack:
        raise Exception("ui.close() called to close the last open layer or widget.")

    if current_once:
        raise Exception("ui.close() called when expecting a widget.")

    current = current_stack.pop()

def reopen(w, clear):
    """
    Reopens a widget, optionally clearing it. This scares me. Don't
    document it.
    """

    global current
    
    current_stack.append(current)
    current = w

    if clear:
        w.children[:] = [ ]

def null(**properties):
    """
    This widget displays nothing on the screen. Why would one want to
    do this? If a widget requires contents, but you don't have any
    contents to provide it.
    """

    return add(renpy.display.layout.Null(**properties))

def text(label, **properties):
    """
    This creates a widget displaying a text label.

    @param label: The text that will be displayed on the screen. It
    uses font properties. The label can also be a list containing both
    text strings in widgets, in the case of a widget, the widget is
    displayed as if it was text of the enclosing font. The height of
    the area allocated is that of the font, with the width being taked
    from a render of the widget.

    @param slow: If True, text is displayed slowly, controlled by the
    appropriate preference.

    @param slow_speed: If slow is True, then this is the number of cps
    the text is displayed at, overriding the preference.
    
    @param slow_done: If not None and slow is True, this is a callback
    that is called when we're done displaying text on the screen.
    """

    return add(renpy.display.text.Text(label, **properties))

def hbox(spacing=None, style='hbox', **properties):
    """
    This creates a layout that places widgets next to each other, from
    left to right. New widgets are added to this hbox until ui.close()
    is called.

    @param spacing: The number of pixels to leave between widgets. If None,
    take the amount of spacing from the style.
    """

    return add(renpy.display.layout.MultiBox(spacing=spacing, layout="horizontal", style=style, **properties), True)

def vbox(spacing=None, style='vbox', **properties):
    """
    This creates a layout that places widgets next to each other, from
    top to bottom. New widgets are added to this vbox until ui.close()
    is called.

    @param spacing: The number of pixels to leave between widgets. If None,
    take the amount of spacing from the style.
    """

    return add(renpy.display.layout.MultiBox(spacing=spacing, layout="vertical", style=style, **properties), True)

def grid(cols, rows, padding=0, transpose=False, **properties):
    """
    This creates a layout that places widgets in an evenly spaced
    grid. New widgets are added to this grid unil ui.close() is called.
    Widgets are added by going from left to right within a single row,
    and down to the start of the next row when a row is full. All cells
    must be filled (that is, exactly col * rows widgets must be added to
    the grid.)

    The children of this widget should have a fixed size that does not
    vary based on the space allocated to them. Failure to observe this
    restriction could lead to really odd layouts, or things being
    rendered off screen. This condition is relaxed in the appropriate
    dimension if xfill or yfill is set.

    Each cell of the grid is exactly the same size. By default, the
    grid is the smallest size that can accommodate all of its
    children, but it can be expanded to consume all available space in
    a given dimension by setting xfill or yfill to True, as appropriate.
    (Otherwise, xfill and yfill are inherited from the style.)

    @param cols: The number of columns in this grid.
    @param rows: The number of rows in this grid.
    @param padding: The amount of space to leave between rows and columns.
    @param xfill: True if the grid should consume all available width.
    @param yfill: True if the grid should consume all available height.
    @param transpose: If True, grid will fill down columns before filling across rows.    
    """

    return add(renpy.display.layout.Grid(cols, rows, padding, transpose=transpose, **properties), True)

def fixed(**properties):
    """
    This creates a layout that places widgets at fixed locations
    relative to the origin of the enclosing widget. The layout takes
    up the entire area allocated to it. New widgets are added to this
    widget.
    """

    rv = renpy.display.layout.MultiBox(layout='fixed', **properties)
    add(rv, True)

    return rv

def sizer(maxwidth=None, maxheight=None, **properties):
    """
    This is a widget that can shrink the size allocated to the next
    widget added. If maxwidth or maxheight is not None, then the space
    allocated to the child in the appropriate direction is limited to
    the given amount.

    Please note that this only works with child widgets that can have
    a limited area allocated to them (like text), and not with ones
    that use a fixed area (like images).

    @param maxwidth: The maximum width of the child widget, or None to not affect width.

    @param maxheight: The maximum height of the child widget, or None ot not affect height.
    """
    
    return add(renpy.display.layout.Container(xmaximum=maxwidth, ymaximum=maxheight, **properties),
               True, True)

    
def window(**properties):
    """
    A window contains a single widget. It draws that window atop a
    background and with appropriate amounts of margin and padding,
    taken from the window properties supplied to this call. The next
    widget created is added to this window.
    """

    return add(renpy.display.layout.Window(None, **properties), True, True)

def frame(**properties):
    """
    A frame contains a single widget. This is similar to a window, but may
    be styled differently.
    """

    properties.setdefault('style', 'frame')

    return add(renpy.display.layout.Window(None, **properties), True, True)



def keymousebehavior():
    """
    This is a psuedo-widget that adds the keymouse behavior to the
    screen. The keymouse behavior allows the mouse to be controlled
    by the keyboard. This widget should not be added to any other
    widget, but should instead be only added to the screen itself.

    As of 4.8, this does nothing, but is retained for compatability.
    """

    return

def keymap(**kwargs):
    return add(renpy.display.behavior.Keymap(**kwargs))

def saybehavior(*args, **kwargs):
    return add(renpy.display.behavior.SayBehavior(*args, **kwargs))

def pausebehavior(delay, result=False):
    """
    This is a psuedo-widget that adds the pause behavior to the
    screen.  The pause behavior is to return the supplied result when
    the given number of seconds elapses. This widget should not be
    added to any other widget, but should instead be only added to the
    screen itself.

    Please note that this widget will always pause for the given
    amount of time. If you want a pause that can be interrupted by
    the user, add in a saybehavior.

    @param delay: The amount of time to pause, in seconds.

    @param result: The result that will be retuned after the delay time
    elapses.
    """

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
    """
    This creates a new menu widget. Unlike the menu statement or
    renpy.menu function, this menu widget is not enclosed in any sort
    of window. You'd have to do that yourself, if it is desired.

    @param menuitems: A list of tuples that are the items to be added
    to this menu. The first element of a tuple is a string that is
    used for this menuitem. The second element is the value to be
    returned from ui.interact() if this item is selected, or None
    if this item is a non-selectable caption.

    @param location: Some serializable and hashable object that
    represents the location of this menu in the game. (Normally, this
    is the name of the statement executing the menu.) If provided, then
    this logs which menuitems have been chosen, and changes the style
    of those menuitems to the choice_seen_style.
    """

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
    """
    This creats a new input widget. This widget accepts textual input
    until the user hits enter, and then returns that text.

    @param default: The default text that fills the input.

    @param length: If set, the maximum number of characters that will be
    returned by this input.

    @param allow: If not None, then if an input character is not in this
    string, it is ignored.

    @param exclude: If not None, then if an input character is in this
    set, it is ignored.
    """

    return add(renpy.display.behavior.Input(default, length=length, allow=allow, exclude=exclude, **properties))

def image(im, **properties):
    """
    This loads an image, and displays it as a widget. The image may be
    the name of a file containing the image, or an arbitrary displayable.
    """

    return add(renpy.display.im.image(im, loose=True, **properties))

def imagemap(ground, selected, hotspots, unselected=None,
             style='imagemap', button_style='imagemap_button',
             **properties):
    """
    This is called to create imagemaps. Parameters are
    roughtly the same as renpy.imagemap. The value of the hotspot is
    returned when ui.interact() returns.
    """

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
    """
    This creates a button that can be clicked by the user. When this
    button is clicked or otherwise selected, the function supplied as
    the clicked argument is called. If it returns a value, that value
    is returned from ui.interact().

    Buttons created with this function contain another widget,
    specifically the next widget to be added. As a convenience, one
    can use ui.textbutton to create a button with a text label.

    @param clicked: A function that is called when this button is
    clicked.

    @param hovered: A function that is called when this button gains
    focus.

    @param unhovered: A function that is called when this button loses
    focus.

    @param role: The role this button undertakes. This can be the empty
    string, or "selected_".
    """

    return add(renpy.display.behavior.Button(None, clicked=clicked,
                                      **properties), True, True)

def textbutton(text, clicked=None, text_style='button_text', **properties):
    """
    This creates a button that is labelled with some text. When the
    button is clicked or otherwise selected, the function supplied as
    the clicked argument is called. If it returns a value, that value
    is returned from ui.interact().

    @param text: The text of this button.

    @param clicked: A function that is called when this button is
    clicked.

    @param text_style: The style that is used for button text.

    @param role: The role this button undertakes. This can be the empty
    string, or "selected_".
    """

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

    """
    This creates a button that contains two images. The first is the
    idle image, which is used when the mouse is not over the image,
    while the second is the hover image, which is used when the mouse
    is over the image. If the button is clicked or otherwise selected,
    then the clicked argument is called. If it returns a value, that
    value is returned from ui.interact().

    @param idle_image: The file name of the image used when this
    button is idle.

    @param hover_image: The file name of the image used when this
    button is hovered.

    @param clicked: The function that is called when this button is
    clicked.

    @param role: The role this button undertakes. This can be the empty
    string, or "selected_".
    """
    
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

def bar(*args, **properties):
    """
    This creates a bar widget. The bar widget can be used to display data
    in a bar graph format, and optionally to report when the user clicks on
    a location in that bar.

    @param width: The width of the bar. If clicked is set, this includes
    the gutters on either side of the bar.

    @param height: The height of the bar.

    @param range: The range of values this bar can undertake. The bar
    is completely full when its value is this number.

    @param value: The value of this bar. It must be between 0 and range,
    inclusive.

    @clicked clicked: This is called when the mouse is clicked in this
    widget. It is called with a single argument, which is the value
    corresponding to the location at which the mouse button was clicked.
    If this function returns a value, that value is returned from
    ui.interact().

    For best results, if clicked is set then width should be at least
    twice as big as range.
    """

    if len(args) == 4:
        width, height, range, value = args
    else:
        range, value = args
        width = None
        height = None


    return add(renpy.display.behavior.Bar(range, value, width, height,
                                          **properties))

def viewport(**properties):
    return add(renpy.display.layout.Viewport(**properties), True, True)


def conditional(condition):
    """
    This contains a conditional widget, a one-child widget that only
    displays its child if a condition is true.

    The condition MUST NOT change the game state in any way, as it is
    not protected against rollback.
    """

    return add(renpy.display.behavior.Conditional(condition), True, True)

def _returns(v):
    """
    This function returns a function that returns the supplied
    value. It's best used as the clicked argument of the button
    functions.
    """

    return v

returns = renpy.curry.curry(_returns)


def _jumps(label):
    """
    This function returns a function that, when called, causes the
    game to jump to the supplied label. It's best used as the clicked
    argument of the button functions.
    """

    raise renpy.game.JumpException(label)

jumps = renpy.curry.curry(_jumps)


def _jumpsoutofcontext(label):
    """
    This exits the current context, and in the parent context jumps to
    the named label. It's intended to be used as the clicked argument
    to a button.
    """

    raise renpy.game.JumpOutException(label)

jumpsoutofcontext = renpy.curry.curry(_jumpsoutofcontext)
