# This file contains functions that are exported to the script namespace.
# Functions defined in this file can be updated by the user to change
# their behavior, while functions imported in are probably best left
# alone as part of the api.

import renpy

from renpy.display.layout import *
from renpy.display.text import *
from renpy.display.behavior import *
from renpy.display.image import *

from renpy.curry import curry
from renpy.music import music_start, music_stop
from renpy.loadsave import *

import time
import random

# This is a map from image name to a Displayable object corresponding
# to that image name.
images = { }

def checkpoint():
    """
    Marks the current statement as a checkpoint, which is a place
    where rolling back can stop when the user asks for a rollback.
    """

    renpy.game.log.checkpoint()

def interact(*widgets):

    for i in widgets:
        scene_list_add('transient', i)

    return renpy.game.interface.interact()

def scene_lists(index=-1):
    """
    Returns either the current scenelists object, or the one for the
    context at the given index.
    """

    return renpy.game.context(index).scene_lists

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

    if listname not in ('master', 'transient'):
        raise Exception("Scene list '%s' doesn't exist." % listname)

    scene_lists().add(listname, displayable, key)

def show(at_disp, with_disp=None, key=None):
    """
    Shows the displayable, as if it was added to a scene list with the show command.

    @param at_disp: The displayable that is added to the screen as if
    it was the result of the at clause in the show statement.

    @param with_displ: The displayable that is added to the screen as
    if it was the result of the with clause in the show statement. If
    None, then this is taken from the at command.

    @param key: The key that is used to remove this displayable from
    the scene list, or None if there is no key.
    """

    if not with_disp:
        with_disp = at_disp

    scene_list_add('master', at_disp, key)
    scene_list_add('transient', at_disp, key)

def hide(key):
    """
    Removes items named with the given key from the scene lists.
    """

    sls = scene_lists()
    sls.remove('master', key)
    sls.remove('transient', key)

def scene():
    """
    This clears the scene lists, as if the scene statement executed.
    """

    sls = scene_lists()
    sls.clear('master')
    sls.clear('transient')
        
def set_overlay(overlay_list):
    """
    Sets the overlay list that will be used to display things at the
    top of the screen. Clearing out the scene lists will not change
    what's displayed in the overlay.

    @param overlay_list: A list of displayables that will be displayed
    above the current scene.
    """

    scene_lists().set_overlay(overlay_list)
    

def menu(items, set_expr, window_style='menu_window'):
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
    rv = display_menu(items, window_style=window_style)

    # If we have a set, fill it in with the label of the chosen item.
    if set is not None and rv is not None:
        for label, value in items:
            if value == rv:
                set.append(label)

    return rv

def display_menu(items, window_style='menu_window'):

    menu = Menu(items)
    win = Window(menu, style=window_style)

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
    what = what % renpy.game.store

    if who is None:
        display_say(who, what, what_style='say_thought')
    elif isinstance(who, (str, unicode)):
        display_say(who, what, what_style='say_dialogue')
    else:
        who.say(what)
        
def display_say(who, what, who_style='say_label',
                what_style='say_dialogue',
                window_style='say_window', **properties):
    """
    @param who: Who is saying the dialogue, or None if it's not being
    said by anyone.

    @param what: What is being said.
    """
    

    import renpy.display.layout as layout
    import renpy.display.text as text
    import renpy.display.behavior as behavior

    if who is None:
        who = ""
    else:
        who = who + ": "

    vbox = layout.VBox(padding=10)

    label = text.Text(who, style=who_style, **properties)
    vbox.add(label)

    line = text.Text(what, style=what_style)
    vbox.add(line)

    window = layout.Window(vbox, style=window_style)
    saybehavior = behavior.SayBehavior(window)

    scene_list_add('transient', saybehavior)

    interact()
    checkpoint()

def pause(delay=None):
    """
    When called, this pauses and waits for the user to click before
    advancing the script.
    """

    null = renpy.display.layout.Null()
    sayb = renpy.display.behavior.SayBehavior(null, delay=delay)

    scene_list_add('transient', sayb)
    
    interact()
    

def rollback():
    """
    Rolls the state of the game back to the last checkpoint.
    """

    if renpy.config.rollback_enabled:
        renpy.game.log.complete()
        renpy.game.log.rollback(1)

def toggle_fullscreen():
    """
    Toggles the fullscreen mode.
    """

    renpy.game.preferences.fullscreen = not renpy.game.preferences.fullscreen

def toggle_music():
    """
    Toggles the playing of music.
    """

    renpy.game.preferences.music = not renpy.game.preferences.music
     
def has_label(name):
    """
    Returns true if name is a valid label in the program, or false
    otherwise.
    """

    return renpy.game.script.has_label(name)

def take_screenshot(scale):
    """
    This causes a screenshot to be taken. This screenshot will be
    saved with a savegame when the game is saved.
    """

    renpy.game.interface.take_screenshot(scale)

def full_restart():
    """
    This causes a full restart of Ren'Py. This clears the store and
    configuration, and re-runs init before branching off to
    start. It's very close to what happens when we quit out and re-run
    the interpreter, save for some caches not being cleared.
    """

    raise renpy.game.FullRestartException()

def quit():
    """
    This causes Ren'Py to exit entirely.
    """

    raise renpy.game.QuitException()

def jump(label):
    """
    Causes the current statement to end, and control to jump to the given
    label.
    """

    raise renpy.game.JumpException(label)

call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(renpy.game.call_in_new_context)
