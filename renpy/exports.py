# This file contains functions that are exported to the script namespace.
# Functions defined in this file can be updated by the user to change
# their behavior, while functions imported in are probably best left
# alone as part of the api.

import renpy.game as game
import renpy.config as config
import renpy.python
import renpy.curry

from renpy.display.layout import *
from renpy.display.text import *
from renpy.display.behavior import *

def checkpoint():
    """
    Marks the current statement as a checkpoint, which is a place
    where rolling back can stop when the user asks for a rollback.
    """

    game.log.checkpoint()

def interact():
    return game.interface.interact()

def scene_lists(index=-1):
    """
    Returns either the current scenelists object, or the one for the
    context at the given index.
    """

    return game.context(index).scene_lists

def show_list(list):
    """
    Replaces the contents of the master and transient scene
    lists with the Displayables found in the provided list.
    """

    scene_lists().replace_lists(list)
    

def scene_list_add(listname, displayable, key=None):
    """
    Adds the displayable to the named scene list, with the
    given key if one is provided.

    @param listname: One of 'master' or 'transient'.
    """

    if listname not in ('master', 'transient', 'overlay', 'empty'):
        raise Exception("Scene list '%s' doesn't exist." % listname)

    scene_lists().add(listname, displayable, key)
    

# This is a map from image name to a Displayable object corresponding
# to that image name.
images = { }

def menu(items, set_expr):
    """
    Displays a menu, and returns to the user the value of the selected
    choice. Also handles conditions and the menuset.
    """

    # Filter the list of items to only include ones for which the
    # condition is true.
    items = [ (label, value)
              for label, condition, value in items
              if renpy.python.py_eval(condition) ]

    # Filter the list of items on the set_expr:
    if set_expr:
        set = renpy.python.py_eval(set_expr)
        items = [ (label, value)
                  for label, value in items
                  if label not in set ]
    else:
        set = None

    # Check to see if there's at least one choice in set of items:
    choices = [ value for label, value in items if value is not None ]

    # If not, bail out.
    if not choices:
        return None

    # Show the menu.
    rv = display_menu(items)

    # If we have a set, fill it in with the label of the chosen item.
    if set is not None and rv is not None:
        for label, value in items:
            if value == rv:
                set.append(label)

    return rv

def display_menu(items):

    menu = Menu(items)
    win = Window(menu, **config.menu_window_properties)

    scene_list_add('transient', win)

    rv = interact()
    checkpoint()

    return rv


def say(who, what):
    """
    This is the core of the say command. If the who parameter is None or
    a string, it is passed directly to do_say. Otherwise, the say method
    is called on the who object with what as a parameter.
    """

    # Interpolate variables.
    what = what % game.store

    if who is None or isinstance(who, (str, unicode)):
        display_say(who, what)
    else:
        who.say(what)
        
def display_say(who, what, color=None):

    import renpy.display.layout as layout
    import renpy.display.text as text
    import renpy.display.behavior as behavior

    if who is None:
        who = ""
    else:
        who = who + ": "

    vbox = layout.VBox(padding=10)

    label = text.Text(who, color=color)
    vbox.add(label)

    line = text.Text(what)
    vbox.add(line)

    window = layout.Window(vbox, **config.say_window_properties)
    saybehavior = behavior.SayBehavior(window)

    scene_list_add('transient', saybehavior)

    interact()
    checkpoint()

def rollback():
    """
    Rolls the state of the game back to the last checkpoint.
    """

    if config.rollback_enabled:
        game.log.complete()
        game.log.rollback(1)

def toggle_fullscreen():
    """
    Toggles the fullscreen mode.
    """

    config.fullscreen = not config.fullscreen
     
def has_label(name):
    """
    Returns true if name is a valid label in the program, or false
    otherwise.
    """

    return game.script.has_label(name)

def screenshot(filename="screenshot.bmp"):
    """
    Takes a screenshot, and saves it in the given filename.
    """

    game.interface.display.screenshot(filename)

curried_call_in_new_context = renpy.curry.curry(game.call_in_new_context)
    
