# This file contains functions that are exported to the script namespace.
# Functions defined in this file can be updated by the user to change
# their behavior, while functions imported in are probably best left
# alone as part of the api.

import renpy

# Many of these shouldn't be used directly.
# from renpy.display.layout import *
from renpy.display.text import ParameterizedText, register_sfont
from renpy.display.behavior import Keymap
# from renpy.display.image import *

from renpy.curry import curry
# from renpy.display.audio import music_start, music_stop
from renpy.audio.sound import play
from renpy.display.video import movie_start_fullscreen, movie_start_displayable, movie_stop
from renpy.loadsave import load, save, saved_games, can_load
from renpy.python import py_eval as eval
from renpy.python import rng as random

import renpy.audio.sound as sound
import renpy.audio.music as music

import time

# This is a map from image name to a Displayable object corresponding
# to that image name.
images = { }

def checkpoint():
    """
    This creates a checkpoint that the user can rollback to. The
    checkpoint is placed at the statement after the last statement
    that interacted with the user. Once this function has been called,
    there should be no more interaction with the user in the current
    statement.
    """

    renpy.game.log.checkpoint()

def block_rollback():
    """
    Prevents the game from rolling back to before the current
    statement.
    """

    renpy.game.log.block()

# def interact(**kwargs):
#    return renpy.game.interface.interact(**kwargs)

def scene_lists(index=-1):
    """
    Returns either the current scenelists object, or the one for the
    context at the given index.
    """

    return renpy.game.context(index).scene_lists

def image(name, img):
    """
    This is used to execute the image statment. It takes as arguments
    an image name and an image object, and associates the image name
    with the image object.

    Like the image statment, this function should only be executed
    in init blocks.

    @param name: The image name, a tuple of strings.
    
    @param img: The displayable that is associated with that name. If this
    is a string or tuple, it is interpreted as an argument to Image.
    """

    if not renpy.game.init_phase:
        raise Exception("Images may only be declared inside init blocks.")

    img = renpy.display.im.image(img, loose=True)

    images[name] = img
    

def show(name, at_list=[ ], layer='master'):
    """
    This is used to execute the show statement, adding the named image
    to the screen as part of the master layer.

    @param name: The name of the image to add to the screen. This is a tuple
    of strings, one string for each component of the image name.

    @param at_list: The at list, a list of functions that are applied
    to the image when shown. The members of the at list need to
    be pickleable if sticky_positions is True.
    """

    sls = scene_lists()
    key = name[0]

    if renpy.config.sticky_positions:        
        if not at_list and key in sls.sticky_positions:
            at_list = sls.sticky_positions[key]

        sls.sticky_positions[key] = at_list

    img = renpy.display.image.ImageReference(name, style='image_placement')
    for i in at_list:
        img = i(img)

    # Update the list of images we have ever seen.
    renpy.game.persistent._seen_images[tuple(name)] = True

    sls.add(layer, img, key)
    

def hide(name, layer='master'):
    """
    This finds items in the master layer that have the same name
    as the first component of the given name, and removes them
    from the master layer. This is used to execute the hide
    statement.
    
    @param name: The name of an image. A tuple of strings, but only
    the first component of this tuple is ever accessed.
    """

    sls = scene_lists()
    key = name[0]
    sls.remove(layer, key)

    if key in sls.sticky_positions:
        del sls.sticky_positions[key]

    

def scene(layer='master'):
    """
    This clears out the master layer. This is used in the execution of
    the scene statment, but only to clear out the layer. If you want
    to then add something new, call renpy.show after this.
    """

    sls = scene_lists()
    sls.clear(layer)
    sls.sticky_positions.clear()
    
        
def watch(expression, style='default', **properties):
    """
    This watches the given python expression, by displaying it in the
    upper-left corner of the screen (although position properties
    can change that). The expression should always be
    defined, never throwing an exception.

    A watch will not persist through a save or restart.
    """

    def overlay_func():
        renpy.ui.text(unicode(renpy.python.py_eval(expression)),
                      style=style, **properties)

    renpy.config.overlay_functions.append(overlay_func)

def input(prompt, default='', allow=None, exclude='{}', length=None):
    """
    This pops up a window requesting that the user enter in some text.
    It returns the entered text.

    @param prompt: A prompt that is used to ask the user for the text.

    @param default: A default for the text that this input can return.

    @param length: If given, a limit to the amount of text that this
    function will return.

    @param allow: If not None, then if an input character is not in this
    string, it is ignored.

    @param exclude: If not None, then if an input character is in this
    set, it is ignored.
    """

    renpy.ui.window(style='input_window')
    renpy.ui.vbox()

    renpy.ui.text(prompt, style='input_prompt')
    renpy.ui.input(default, length=length, style='input_text', allow=allow, exclude=exclude)

    renpy.ui.close()

    return renpy.ui.interact(mouse='prompt')

def menu(items, set_expr):
    """
    Displays a menu, and returns to the user the value of the selected
    choice. Also handles conditions and the menuset.
    """

    # Filter the list of items to only include ones for which the
    # condition is true.
    items = [ (label % tag_quoting_dict, value)
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
    rv = renpy.store.menu(items)

    # If we have a set, fill it in with the label of the chosen item.
    if set is not None and rv is not None:
        for label, value in items:
            if value == rv:
                try:
                    set.append(label)
                except AttributeError:
                    set.add(label)
    return rv

def choice_for_skipping():
    """
    This is called to indicate to the skipping code that we have
    reached a choice. If we're skipping, and if the skip after
    choices preference is not True, then this disables skipping.
    """

    if renpy.config.skipping and not renpy.game.preferences.skip_after_choices:
        renpy.config.skipping = None
    

def predict_menu():
    """
    Predicts widgets that are used by the menu.
    """
    
    return [ renpy.game.style.menu_window.background,
             renpy.game.style.menu_choice_button.background ]

def display_menu(items, window_style='menu_window', interact=True):
    """
    Displays a menu containing the given items, returning the value of
    the item the user selects.

    @param items: A list of tuples that are the items to be added to
    this menu. The first element of a tuple is a string that is used
    for this menuitem. The second element is the value to be returned
    if this item is selected, or None if this item is a non-selectable
    caption.

    @param interact: If True, then an interaction occurs. If False, no suc
    interaction occurs, and the user should call ui.interact() manually.
    """

    choice_for_skipping()

    if renpy.config.auto_choice_delay:
        choices = [ val for label, val in items ]

        while None in choices:
            choices.remove(None)

        renpy.ui.pausebehavior(renpy.config.auto_choice_delay,
                               random.choice(choices))

    renpy.ui.window(style=window_style)
    renpy.ui.menu(items, location=renpy.game.context().current)

    for label, val in items:
        if val:
            log("Choice: " + label)
        else:
            log(label)

    log("")

    if interact:
        rv = renpy.ui.interact(mouse='menu')

        for label, val in items:
            if rv == val:
                log("User chose: " + label)
                break
        else:
            log("No choice chosen.")

        log("")

        checkpoint()
        return rv
    
    return None

class TagQuotingDict(object):
    def __getitem__(self, key):

        store = vars(renpy.store)
        
        if key in store:
            rv = store[key]

            if isinstance(rv, (str, unicode)):
                rv = rv.replace("{", "{{")

            return rv
        else:
            if renpy.config.debug:
                raise Exception("During an interpolation, '%s' was not found as a variable." % key)
            return "<" + key + " unbound>"

tag_quoting_dict = TagQuotingDict()

def say(who, what):
    """
    This is the core of the say command. If the who parameter is None
    or a string, it is passed directly to display_say. Otherwise, the
    say method is called on the who object with what as a parameter.
    """

    # Interpolate variables.
    what = what % tag_quoting_dict

    if who is None:
        who = renpy.store.narrator

    if isinstance(who, (str, unicode)):
        renpy.store.say(who, what)
    else:
        who(what)

def predict_say(who, what):
    """
    This is called to predict the results of a say command.
    """

    if who is None:
        who = renpy.store.narrator

    if isinstance(who, (str, unicode)):
        return renpy.store.predict_say(who, what)
    else:
        predict = getattr(who, 'predict', None)
        if predict:            
            return predict(what)
        else:
            return [ ]
    
        
def predict_display_say(who, what,
                        window_style='say_window',
                        window_properties={},
                        image=False,
                        ctc=None,
                        **kwargs):
    """
    This is the default function used Character to predict images that
    will be used by display_say. It's called with more-or-less the
    same parameters as display_say, and is expected to return a list
    of images used by display_say.
    """

    rv = [ ]

    if "background" in window_properties:
        rv.append(window_properties["background"])
    else:        
        rv.append(getattr(renpy.game.style, window_style).background)

    if image:
        rv.append(renpy.display.im.image(who, True))

    if ctc:
        rv.append(ctc)

    return rv
        
                  
def show_display_say(who, what, who_args={}, what_args={}, window_args={}, image=False, **kwargs):
    """
    This is called (by default) by renpy.display_say to add the
    widgets corresponding to a screen of dialogue to the user. It is
    not expected to be called by the user, but instead to be called by
    display_say, or by a function passed as the show_function argument
    to Character or display_say.

    @param who: The name of the character that is speaking, or None to
    not show this name to the user.

    @param what: What that character is saying. Please not that this
    may not be a string, as it can also be a list containing both text
    and displayables, suitable for use as the first argument of ui.text().

    @param who_args: Additional keyword arguments intended to be
    supplied to the ui.text that creates the who widget of this dialogue.

    @param what_args: Additional keyword arguments intended to be
    supplied to the ui.text that creates the what widget of this dialogue.

    @param window_args: Additional keyword arguments intended to be
    supplied to the ui.window that creates the who widget of this
    dialogue.

    @param image: If True, then who should be interpreted as an image
    or displayable rather than a text string.

    @param kwargs: Additional keyword arguments should be ignored.

    This function is required to return the ui.text() widget
    displaying the what text.
    """

    renpy.ui.window(**window_args)
    renpy.ui.vbox(style='say_vbox')

    if who:
        if image:
            renpy.ui.add(renpy.display.im.image(who, loose=True, **who_args))
        else:
            renpy.ui.text(who, **who_args)

    rv = renpy.ui.text(what, **what_args)
    renpy.ui.close()

    return rv
            
def display_say(who, what, who_style='say_label',
                what_style='say_dialogue',
                window_style='say_window',
                who_prefix='',
                who_suffix=': ',
                what_prefix='',
                what_suffix='',
                interact=True,
                slow=True,
                slow_speed=None,
                slow_abortable=True,
                image=False,
                afm=True,
                ctc=None,
                ctc_position="nestled",
                all_at_once=False,
                what_properties={},
                window_properties={},
                show_function = show_display_say,
                **properties):
    """
    @param who: Who is saying the dialogue, or None if it's not being
    said by anyone.

    @param what: What is being said.

    @param afm: If True, the auto-forwarding mode is enabled. If False,
    it is disabled.

    @param all_at_once: If True, then the text is displayed all at once. (This is forced to true if interact=False.)

    For documentation of the other arguments, please read the
    documentation for Character.
    """

    # If we're in fast skipping mode, don't bother with say
    # statements at all.
    if renpy.config.skipping == "fast":

        # Clears out transients.
        with(None)
        
        return

    # If we're just after a rollback, or skipping, disable slow.
    if renpy.game.after_rollback or renpy.config.skipping:
        slow = False

    what = what_prefix + what + what_suffix

    if not interact:
        all_at_once = True

    if all_at_once:
        pause = None
    else:
        pause = 0

    keep_interacting = True
    slow_start = 0

    # Figure out window args.
    window_args = dict(style=window_style, **window_properties)

    # Figure out who and its arguments.
    if who is not None and not image:
        who = who_prefix + who + who_suffix
        who_args = dict(style=who_style, **properties)
    elif who is not None and image:
        who_args = dict(style=who_style, **properties)
    else:
        who_args = dict()

    while keep_interacting:
                
        # If we're going to do an interaction, then saybehavior needs
        # to be here.
        if interact:            
            behavior = renpy.ui.saybehavior()
        else:
            behavior = None

        # Code to support ctc.
        ctcwhat = [ what ]

        if ctc and ctc_position == "nestled":
            ctcwhat.extend([ " ", ctc ])

        slow_done = None

        if ctc and ctc_position == "fixed":
            def slow_done():
                renpy.ui.add(ctc)
                restart_interaction()

                
        what_args = dict(style=what_style,
                         slow=slow,
                         slow_done=slow_done,
                         slow_abortable=slow_abortable,
                         slow_start=slow_start,
                         pause=pause,
                         slow_speed = None,
                         **what_properties)

        what_text = show_function(who, ctcwhat, who_args=who_args, what_args=what_args, window_args=window_args, image=image)

        if behavior and afm:
            behavior.set_afm_length(what_text.get_simple_length() - slow_start)

        if interact:
            renpy.ui.interact(mouse='say')

        keep_interacting = what_text.get_keep_pausing()

        if keep_interacting:
            slow_start = what_text.get_laidout_length()
            pause += 1

            for i in renpy.config.say_sustain_callbacks:
                i()

    if who and isinstance(who, (str, unicode)):
        log(who)
    log(what)
    log("")

    if interact:
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

    rv = renpy.ui.interact(suppress_overlay=(not overlays), mouse='imagemap')
    checkpoint()
    return rv
    

def pause(delay=None, music=None):
    """
    When called, this pauses and waits for the user to click before
    advancing the script. If given a delay parameter, the Ren'Py will
    wait for that amount of time before continuing, unless a user clicks to
    interrupt the delay.

    @param delay: The number of seconds to delay.

    @param music: If supplied, and music is playing, this takes
    precedence over the delay parameter. It gives a time, in seconds,
    into the playing music track. Ren'Py will pause until the music
    has played up to that point..

    Returns True if the pause was interrupted by the user hitting a key
    or clicking a mouse, or False if the pause was ended by the appointed
    time being reached.
    """

    if renpy.config.skipping == "fast":
        return True

    if music is not None:
        newdelay = renpy.audio.music.get_delay(music)

        if newdelay is not None:
            delay = newdelay

    renpy.ui.saybehavior()

    if delay:
        renpy.ui.pausebehavior(delay, False)

    return renpy.ui.interact(mouse='pause')

def movie_cutscene(filename, delay, loops=0):
    """
    This displays an MPEG-1 cutscene for the specified number of
    seconds. The user can click to interrupt the cutscene.
    Overlays and Underlays are disabled for the duration of the cutscene.

    @param filename: The name of a file containing an MPEG-1 movie.

    @param delay: The number of seconds to wait before ending the cutscene. Normally the length of the movie, in seconds.

    @param loops: The number of extra loops to show, -1 to loop forever.

    Returns True if the movie was terminated by the user, or False if the
    given delay elapsed uninterrupted.
    """

    movie_start_fullscreen(filename, loops=loops)

    renpy.ui.saybehavior()
    renpy.ui.pausebehavior(delay, False)

    rv = renpy.ui.interact(suppress_overlay=True, suppress_underlay=True, show_mouse=False)

    movie_stop()

    return rv
        

def with(trans, paired=None):
    """
    Implements the with statement. One reason to use this over a
    Ren'Py with statement is to get at the return code, which is True
    if the transition was interrupted, or False otherwise.

    @param trans: The transition.

    @param paired: The transition paired with this with one.
    """

    if renpy.config.skipping:
        renpy.game.interface.with_none()
        return False

    if renpy.config.with_callback:
        trans = renpy.config.with_callback(trans, paired)

    if not trans:
        renpy.game.interface.with_none()
        return False
    else:
        if renpy.game.preferences.transitions:
            renpy.game.interface.set_transition(trans)
            return renpy.game.interface.interact(show_mouse=False,
                                                 trans_pause=True,
                                                 suppress_overlay=not renpy.config.overlay_during_with,
                                                 mouse='with')
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

def jump_out_of_context(label):
    """
    Causes control to leave the current context, and then to be
    transferred in the parent context to the given label.
    """

    raise renpy.game.JumpOutException(label)


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

def version():
    """
    Returns a string containing the current version of Ren'Py, prefixed with the
    string "Ren\'Py ".
    """

    return renpy.version

def module_version():
    """
    Returns a number corresponding to the current version of the Ren'Py module,
    or 0 if the module wasn't loaded.
    """

    return renpy.display.module.version

def transition(trans, layer=None):
    """
    Sets the transition that will be used for the next
    interaction. This is useful when the next interaction doesn't take
    a with clause, as is the case with pause, input, and imagemap.

    @param layer: If the layer setting is not None, then the transition
    will be applied only to the layer named. Please note that only some
    transitions can be applied to specific layers.
    """

    if trans is None:
        renpy.game.interface.with_none()
    else:
        renpy.game.interface.set_transition(trans, layer)

def clear_game_runtime():
    """
    Resets the game runtime timer down to 0.

    The game runtime counter counts the number of seconds that have
    elapsed while waiting for user input in the current context. (So
    it doesn't count time spent in the game menu.)
    """
    
    renpy.game.context().runtime = 0

def get_game_runtime():
    """
    Returns the number of seconds that have elapsed in gameplay since
    the last call to clear_game_timer, as a float.

    The game runtime counter counts the number of seconds that have
    elapsed while waiting for user input in the current context. (So
    it doesn't count time spent in the game menu.)
    """

    return renpy.game.context().runtime

def loadable(filename):
    """
    Returns True if the given filename is loadable, meaning that it
    can be loaded from the disk or from inside an archive. Returns
    False if this is not the case.
    """

    return renpy.loader.loadable(filename)

def exists(filename):
    """
    Returns true if the given filename can be found in the
    searchpath. This only works if a physical file exists on disk. It
    won't find the file if it's inside of an archive.
    """

    try:
        renpy.loader.transfn(filename)
        return True
    except:
        return False

def restart_interaction():
    """
    Calling this restarts the current interaction. This will immediately end
    any ongoing transition, and will call all of the overlay functions again.

    This should be called whenever widgets are added or removed over the course
    of an interaction, or when the information used to construct the overlay
    changes.
    """

    renpy.game.interface.restart_interaction = True
    
def context():
    """
    Returns an object that is unique to the current context, that
    participates in rollback and the like.
    """

    return renpy.game.context().info
    
def music_start(filename, loops=True, fadeout=None, fadein=0):
    """
    Deprecated music start function, retained for compatibility. Use
    renpy.music.play() or .queue() instead.
    """

    renpy.audio.music.play(filename, loop=loops, fadeout=fadeout, fadein=fadein)

def music_stop(fadeout=None):
    """
    Deprecated music start function, retained for compatibility. Use
    renpy.music.play() or .queue() instead.
    """

    renpy.audio.music.stop(fadeout=fadeout)

def get_filename_line():
    """
    Returns a pair giving the filename and line number of the current
    statement.
    """

    n = renpy.game.script.namemap[renpy.game.context().current]
    return n.filename, n.linenumber

def launch_editor():
    """
    This causes an editor to be launched at the location of the current
    statement.
    """

    import renpy.subprocess as subprocess

    if not renpy.config.editor:
        return

    filename, line = get_filename_line()
    subs = dict(filename=filename, line=line)
    cmd = renpy.config.editor % subs

    try:
        subprocess.Popen(cmd, shell=True)
    except:
        if renpy.config.debug:
            raise

# A file that log logs to.
logfile = None
    
def log(msg):
    """
    If config.log is not set, this does nothing. Otherwise, it opens
    the logfile (if not already open), formats the message to 70
    columns, and prints it to the logfile.
    """
    
    global logfile

    if not renpy.config.log:
        return

    if msg is None:
        return

    if not logfile:
        import codecs

        logfile = file(renpy.config.log, "a")
        if not logfile.tell():
            logfile.write(codecs.BOM_UTF8)

    import textwrap

    print >>logfile, textwrap.fill(msg).encode("utf-8")
    logfile.flush()
    
def force_full_redraw():
    """
    Forces the screen to be redrawn in full. Call this after using pygame
    to redraw the screen directly.
    """

    renpy.game.interface.display.full_redraw = True

call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(renpy.game.call_in_new_context)

invoke_in_new_context = renpy.game.invoke_in_new_context
