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

import renpy

# The current widget (None to add widgets directly to the
# transient display list.)
current = None

# A stack of current widgets.
current_stack = [ ]

# True if the current widget should be used at most once.
current_once = False

def interact(**kwargs):
    """
    Displays the current scene to the user, waits for a widget to indicate
    a return value, and returns that value to the user.

    Some useful keyword arguments are:

    @param show_mouse: Should the mouse be shown during this
    interaction? Only advisory, as this doesn't work reliably.

    @param suppress_overlay: This suppresses the display of the overlay during
    this interaction.
    """

    if current_stack:
        raise Exception("ui.interact called with non-empty widget stack. Did you forget a ui.close()?")

    return renpy.game.interface.interact(**kwargs)


def add(w, make_current=False, once=False):
    """
    Adds a new widget to the current widget. If make_current is true,
    then the widget is also made the current widget, with the old 
    widget being pushed onto a stack.
    """

    global current
    global current_once

    if current is None:
        renpy.game.context(-1).scene_lists.add('transient', w)
    else:
        current.add(w)

    if current_once:
        current_once = False
        close()

    current_once = once

    if make_current:
        current_stack.append(current)
        current = w

    return w

def close():
    """
    Closes the current widget. This means that we will no longer add
    things to the current widget, but will instead start adding things
    to the parent of that widget, or the screen if the widget has no
    parent. Calling this when there is no current widget will lead to
    an exception being thrown.
    """

    global current

    if current is None:
        raise Exception("ui.close() called when there is no open widget.")

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

    @param label: The text that will be displayed on the screen. 

    It uses font properties.
    """

    return add(renpy.display.text.Text(label, **properties))

def hbox(padding=0, **properties):
    """
    This creates a layout that places widgets next to each other, from
    left to right. New widgets are added to this hbox until ui.close()
    is called.

    @param padding: The number of pixels to leave between widgets.
    """

    return add(renpy.display.layout.HBox(padding, **properties), True)

def vbox(padding=0, **properties):
    """
    This creates a layout that places widgets next to each other, from
    top to bottom. New widgets are added to this vbox until ui.close()
    is called.

    @param padding: The number of pixels to leave between widgets.
    """

    return add(renpy.display.layout.VBox(padding, **properties), True)

def fixed(**properties):
    """
    This creates a layout that places widgets at fixed locations
    relative to the origin of the enclosing widget. New widgets are
    added to this widget.
    """

    rv = renpy.display.layout.Fixed(**properties)
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

    return add(renpy.display.layout.Sizer(maxwidth, maxheight, None, **properties),
               True, True)

    
def window(**properties):
    """
    A window contains a single widget. It draws that window atop a
    background and with appropriate amounts of margin and padding,
    taken from the window properties supplied to this call. The next
    widget created is added to this window.
    """

    return add(renpy.display.layout.Window(None, **properties), True, True)

def keymousebehavior():
    """
    This is a psuedo-widget that adds the keymouse behavior to the
    screen. The keymouse behavior allows the mouse to be controlled
    by the keyboard. This widget should not be added to any other
    widget, but should instead be only added to the screen itself.
    """

    return add(renpy.display.behavior.KeymouseBehavior())

def saybehavior():
    """
    This is a psuedo-widget that adds the say behavior to the
    screen. The say behavior is to return True if the left mouse is
    clicked or enter is pressed. It also returns true in various other
    cases if the current statement has already been seen. This widget
    should not be added to any other widget, but should instead be
    only added to the screen itself.
    """

    return add(renpy.display.behavior.SayBehavior())

def menu(menuitems, **properties):
    """
    This creates a new menu widget. Unlike the menu statement or
    renpy.menu function, this menu widget is not enclosed in any sort
    of window. You'd have to do that yourself, if it is desired.

    @param menuitems: A list of tuples that are the items to be added
    to this menu. The first element of a tuple is a string that is
    used for this menuitem. The second element is the value to be
    returned from renpy.interact() if this item is selected, or None
    if this item is a non-selectable caption.
    """

    return add(renpy.display.behavior.Menu(menuitems, **properties))


def image(filename, **properties):
    """
    This loads an image from the given file, and displays it as a
    widget.
    """

    return add(renpy.display.image.Image(filename, **properties))

def imagemap(ground, selected, hotspots, unselected=None,
             **properties):
    """
    This is the widget that implements imagemaps. Parameters are
    roughtly the same as renpy.imagemap. The value of the hotspot is
    returned when renpy.interact() returns.
    """

    return add(renpy.display.image.ImageMap(ground, selected,
                                            hotspots, unselected,
                                            **properties))
                                            

def button(clicked=None, **properties):
    """
    This creates a button that can be clicked by the user. When this
    button is clicked or otherwise selected, the function supplied as
    the clicked argument is called. If it returns a value, that value
    is returned from renpy.interact().

    Buttons created with this function contain another widget,
    specifically the next widget to be added. As a convenience, one
    can use ui.textbutton to create a button with a text label.

    @param clicked: A function that is called when this button is
    clicked.
    """

    return add(renpy.display.behavior.Button(None, clicked=clicked,
                                      **properties), True, True)

def textbutton(text, clicked=None, text_style='button_text', **properties):
    """
    This creates a button that is labelled with some text. When the
    button is clicked or otherwise selected, the function supplied as
    the clicked argument is called. If it returns a value, that value
    is returned from renpy.interact().

    @param text: The text of this button.

    @param clicked: A function that is called when this button is
    clicked.

    @param text_style: The style that is used for button text.
    """

    return add(renpy.display.behavior.TextButton(text, clicked=clicked,
                                                 text_style=text_style,
                                                 **properties))

def imagebutton(idle_image, hover_image, clicked=None,
                image_style='image_button_image', **properties):

    """
    This creates a button that contains two images. The first is the
    idle image, which is used when the mouse is not over the image,
    while the second is the hover image, which is used when the mouse
    is over the image. If the button is clicked or otherwise selected,
    then the clicked argument is called. If it returns a value, that
    value is returned from renpy.interact().

    @param idle_image: The file name of the image used when this
    button is idle.

    @param hover_image: The file name of the image used when this
    button is hovered.

    @param clicked: The function that is called when this button is
    clicked.

    @param image_style: The style that is applied to the images that
    are used as part of the imagebutton.
    """
    
    return add(renpy.display.image.ImageButton(idle_image,
                                               hover_image,
                                               clicked=clicked,
                                               image_style=image_style,
                                               **properties))

def bar(width, height, range, value, clicked=None, **properties):
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
    renpy.interact().

    For best results, if clicked is set then width should be at least
    twice as big as range.
    """

    return add(renpy.display.behavior.Bar(width, height, range, value,
                                          clicked=clicked, **properties))
    

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

