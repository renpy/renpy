# This file contains functions that are exported to the script namespace.
# Functions defined in this file can be updated by the user to change
# their behavior, while functions imported in are probably best left
# alone as part of the api.

import renpy

# Many of these shouldn't be used directly.
from renpy.display.layout import *
from renpy.display.text import *
from renpy.display.behavior import *
from renpy.display.image import *

from renpy.curry import curry
from renpy.music import music_start, music_stop
from renpy.sound import play
from renpy.loadsave import *
from renpy.python import py_eval as eval
from renpy.python import rng as random

import time

# This is a map from image name to a Displayable object corresponding
# to that image name.
images = { }

def checkpoint():
    """
    Marks the current statement as a checkpoint, which is a place
    where rolling back can stop when the user asks for a rollback.
    """

    renpy.game.log.checkpoint()

def interact(*widgets, **kwargs):
    return renpy.game.interface.interact(transient=widgets, **kwargs)

def scene_lists(index=-1):
    """
    Returns either the current scenelists object, or the one for the
    context at the given index.
    """

    return renpy.game.context(index).scene_lists

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
        
def watch(expression, style='default', **properties):
    """
    This watches the given python expression, by displaying it in the
    upper-right corner of the screen (although position properties
    can change that). The expression should always be
    defined, never throwing an exception.

    A watch will not persist through a save or restart.
    """

    def overlay_func():
        return [ renpy.display.text.Text(renpy.python.py_eval(expression),
                                         style=style, **properties) ]

    renpy.config.overlay_functions.append(overlay_func)

def input(prompt, default='', length=None):
    """
    This pops up a window requesting that the user enter in some text.
    It returns the entered text.

    @param prompt: A prompt that is used to ask the user for the text.

    @param default: A default for the text that this input can return.

    @param length: If given, a limit to the amount of text that this
    function will return.
    """

    vbox = renpy.display.layout.VBox()
    win = renpy.display.layout.Window(vbox, style='input_window')

    vbox.add(renpy.display.text.Text(prompt, style='input_prompt'))
    vbox.add(renpy.display.behavior.Input(default, length=length, style='input_text'))

    return interact(win)

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
    """
    Displays a menu containing the given items, returning the value of
    the item the user selects.

    @param items: A list of tuples that are the items to be added to
    this menu. The first element of a tuple is a string that is used
    for this menuitem. The second element is the value to be returned
    if this item is selected, or None if this item is a non-selectable
    caption.
    """

    renpy.ui.window(style=window_style)
    renpy.ui.menu(items)

    rv = interact()
    checkpoint()

    return rv


def say(who, what):
    """
    This is the core of the say command. If the who parameter is None
    or a string, it is passed directly to display_say. Otherwise, the
    say method is called on the who object with what as a parameter.
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
                window_style='say_window',
                who_prefix='',
                who_suffix=': ',
                what_prefix='',
                what_suffix='',
                **properties):
    """
    @param who: Who is saying the dialogue, or None if it's not being
    said by anyone.

    @param what: What is being said.

    For documentation of the various prefixes, suffixes, and styles,
    please read the documentation for Character.
    """
    
    if who is not None:
        who = who_prefix + who + who_suffix

    what = what_prefix + what + what_suffix

    renpy.ui.window(style=window_style)
    renpy.ui.vbox(padding=10)

    if who is not None:
        renpy.ui.text(who, style=who_style, **properties)

    renpy.ui.text(what, style=what_style, slow=True)
    renpy.ui.close()

    renpy.ui.saybehavior()

    interact()
    checkpoint()

def imagemap(ground, selected, hotspots, unselected=None, overlays=False,
             style='imagemap', **properties):
    """
    Displays an imagemap. An image map consists of two images and a
    list of hotspots that are defined on that image. When the user
    clicks on a hotspot, the value associated with that hotspot is
    returned.

    @param ground: The name of the file containing the ground
    image. The ground image is displayed for areas that are not part
    of any hotspots.

    @param selected: The name of the file containing the selected
    image. This image is displayed in hotspots when the mouse is over
    them.

    @param hotspots: A list of tuples defining the hotspots in this
    image map. Each tuple has the format (x0, y0, x1, y1, result).
    (x0, y0) gives the coordinates of the upper-left corner of the
    hotspot, (x1, y1) gives the lower-right corner, and result gives
    the value returned from this function if the mouse is clicked in
    the hotspot.

    @param unselected: If provided, then it is the name of a file
    containing the image that's used to fill in hotspots that are not
    selected as part of any image. If not provided, the ground image
    is used instead.
 
    @param overlays: If True, overlays are displayed when this imagemap
    is active. If False, the overlays are suppressed.
    """

    renpy.ui.imagemap(ground, selected, hotspots, unselected=unselected,
                      style=style, **properties)

    renpy.ui.keymousebehavior()

    rv = interact(suppress_overlay=(not overlays))
    checkpoint()
    return rv
    

def pause(delay=None, music=None):
    """
    When called, this pauses and waits for the user to click before
    advancing the script.

    @param delay: The number of seconds to delay.

    @param music: If supplied, this gives the number of seconds into
    the background music that we will delay until. If music is
    playing, this takes precedence, otherwise the delay parameter
    take precedence.

    Returns True if the pause was interrupted by the user hitting a key
    or clicking a mouse, or False if the pause was ended by the appointed
    time being reached.
    """

    if music is not None:
        newdelay = renpy.music.music_delay(music)

        if newdelay is not None:
            delay = newdelay

    sayb = renpy.display.behavior.SayBehavior(delay=delay)
    scene_list_add('transient', sayb)
    
    return interact()

def with(trans):
    """
    Behaves identically to a with statement. The only reason to use this
    over a Ren'Py with statement is to get at the return code, which is
    True if the transition was interrupted, or False otherwise.
    """

    # Code basically copied from ast.With.execute.
    if not trans:
        renpy.game.interface.with_none()
        return False
    else:
        if renpy.game.preferences.transitions:
            renpy.game.interface.set_transition(trans)
            return renpy.game.interface.interact(show_mouse=False,
                                                 trans_pause=True,
                                                 suppress_overlay=True)
        else:
            return False

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

def screenshot(filename):
    """
    Saves a screenshot in the named filename.
    """
    
    renpy.game.interface.display.save_screenshot(filename)
    
def windows():
    """
    Returns true if we're running on Windows. This is generally used as a
    test when setting styles.
    """

    import sys
    return hasattr(sys, 'winver')

def transition(trans):
    """
    Sets the transition that will be used for the next
    interaction. This is useful when the next interaction doesn't take
    a with clause, as is the case with pause, input, and imagemap.
    """

    if trans is None:
        renpy.game.interface.with_none()
    else:
        renpy.game.interface.set_transition(trans)

call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(renpy.game.call_in_new_context)

