# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains functions that are exported to the script namespace.
# Functions defined in this file can be updated by the user to change
# their behavior, while functions imported in are probably best left
# alone as part of the api.

# Remember the real file.
_file = file

import renpy.display
import renpy.audio

from renpy.display.text import ParameterizedText
from renpy.display.font import register_sfont, register_mudgefont, register_bmfont
from renpy.display.behavior import Keymap
from renpy.display.minigame import Minigame
from renpy.display.screen import define_screen, show_screen, hide_screen, use_screen, current_screen, has_screen, get_screen, get_widget
from renpy.display.focus import focus_coordinates
from renpy.display.predict import screen as predict_screen

from renpy.curry import curry, partial
from renpy.audio.sound import play
from renpy.display.video import movie_start_fullscreen, movie_start_displayable, movie_stop
from renpy.loadsave import load, save, list_saved_games, can_load, rename_save, unlink_save, scan_saved_game
from renpy.python import py_eval as eval
from renpy.python import rng as random
from renpy.atl import atl_warper
from renpy.easy import predict

from renpy.character import show_display_say, predict_show_display_say, display_say

import renpy.audio.sound as sound
import renpy.audio.music as music

import time

def public_api():
    """
    This does nothing, except to make the pyflakes warnings about
    unused imports go away.
    """
    ParameterizedText
    register_sfont, register_mudgefont, register_bmfont
    Keymap
    Minigame
    curry, partial
    play
    movie_start_fullscreen, movie_start_displayable, movie_stop
    load, save, list_saved_games, can_load, rename_save, unlink_save, scan_saved_game
    eval
    random
    atl_warper
    show_display_say, predict_show_display_say, display_say
    sound
    music
    time
    define_screen, show_screen, hide_screen, use_screen, has_screen
    current_screen, get_screen, get_widget
    focus_coordinates
    predict, predict_screen
    
del public_api

import collections

def roll_forward_info():
    return renpy.game.log.forward_info()

def in_rollback():
    return renpy.game.log.in_rollback()

def checkpoint(data=None, keep_rollback=False):
    """
    This creates a checkpoint that the user can rollback to. The
    checkpoint is placed at the statement after the last statement
    that interacted with the user. Once this function has been called,
    there should be no more interaction with the user in the current
    statement.
    """

    if renpy.store._rollback:
        renpy.game.log.checkpoint(data, keep_rollback=keep_rollback)

def block_rollback():
    """
    Prevents the game from rolling back to before the current
    statement.
    """

    renpy.game.log.block()

scene_lists = renpy.display.core.scene_lists
    
def count_displayables_in_layer(layer):
    """
    Returns how many displayables are in the supplied layer.
    """

    sls = scene_lists()

    return len(sls.layers[layer])

def image(name, d):
    """
    :doc: se_images
    
    Defines an image. This function is the python equivalent of the 
    image statement.
    
    `name`
        The name of the image to display, a string.
        
    `d`
        The displayable to associate with that image name.
        
    This function may only be run from inside an init block. It is an
    error to run this function once the game has started.
    """

    if d is None:
        raise Exception("Images may not be declared to be None.")
        
    if not renpy.game.context().init_phase:
        raise Exception("Images may only be declared inside init blocks.")

    if not isinstance(name, tuple):
        name = tuple(name.split())

    d = renpy.easy.displayable(d)
    renpy.display.image.register_image(name, d)

def copy_images(old, new):
    if not isinstance(old, tuple):
        old = tuple(old.split())

    if not isinstance(new, tuple):
        new = tuple(new.split())

    lenold = len(old)
        
    for k, v in renpy.display.image.images.items():
        if len(k) < lenold:
            continue
        
        if k[:lenold] == old:
            renpy.display.image.register_image(new + k[lenold:], v)
    
def showing(name, layer='master'):
    """
    This returns true if an image with the same tag as that found in
    the suppled image name is present on the given layer.

    @param name may be a tuple of strings, or a single string. In the latter
    case, it is split on whitespace to make a tuple. The first element
    of the tuple is used as the image tag.

    @param layer is the name of the layer.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    return renpy.game.context().images.showing(layer, name)

def show(name, at_list=[ ], layer='master', what=None, zorder=0, tag=None, behind=[ ], atl=None, transient=False, munge_name=True):
    """
    :doc: se_images
    :args: (name, at_list=[ ], layer='master', what=None, zorder=0, tag=None, behind=[ ])
    
    Shows an image on a layer. This is the programmatic equivalent of the show
    statement.
    
    `name`
        The name of the image to show, a string.
        
    `at_list`
        A list of transforms that are applied to the image.
        The equivalent of the ``at`` property.
        
    `layer`
        A string, giving the name of the layer on which the image will be shown.
        The equivalent of the ``onlayer`` property.
    
    `what`
        If not None, this is a displayable that will be shown in lieu of 
        looking on the image. (This is the equivalent of the show expression
        statement.) When a `what` parameter is given, `name` can be used to
        associate a tag with the image.
        
    `zorder`
        An integer, the equivalent of the ``zorder`` property.
        
    `tag`
        A string, used to specify the the image tag of the shown image. The
        equivalent of the ``as`` property.
        
    `behind`
        A list of strings, giving image tags that this image is shown behind.
        The equivalent of the ``behind`` property.
    """

    if renpy.game.context().init_phase:
        raise Exception("Show may not run while in init phase.")
    
    if not isinstance(name, tuple):
        name = tuple(name.split())

    sls = scene_lists()
    key = tag or name[0]

    if renpy.config.sticky_positions:        
        if not at_list and key in sls.at_list[layer]:
            at_list = sls.at_list[layer][key]

    if what is None:
        what = name
    elif isinstance(what, basestring):
        what = tuple(what.split())

    if isinstance(what, renpy.display.core.Displayable):
        base = img = what

    else:

        if renpy.config.image_attributes:
            new_what = renpy.game.context().images.apply_attributes(layer, key, name)
            if new_what is not None:
                what = new_what
                name = (key,) + new_what[1:]
                
        base = img = renpy.display.image.ImageReference(what, style='image_placement')
        
        if not base.find_target() and renpy.config.missing_show:
            if renpy.config.missing_show(name, what, layer):
                return
        
    for i in at_list:
        if isinstance(i, renpy.display.motion.Transform):
            img = i(child=img)
        else:
            img = i(img)

    # Update the list of images we have ever seen.
    renpy.game.persistent._seen_images[name] = True

    if tag and munge_name:
        name = (tag,) + name[1:]
    

    if renpy.config.missing_hide:
        renpy.config.missing_hide(name, layer)

    sls.add(layer, img, key, zorder, behind, at_list=at_list, name=name, atl=atl, default_transform=renpy.config.default_transform, transient=transient)
    

def hide(name, layer='master'):
    """
    :doc: se_images
    
    Hides an image from a layer. The python equivalent of the hide statement.
    
    `name`
         The name of the image to hide. Only the image tag is used, and 
         any image with the tag is hidden (the precise name does not matter).
         
    `layer`
         The layer on which this function operates.
    """

    if renpy.game.context().init_phase:
        raise Exception("Hide may not run while in init phase.")

    if not isinstance(name, tuple):
        name = tuple(name.split())

    sls = scene_lists()
    key = name[0]
    sls.remove(layer, key)

    if renpy.config.missing_hide:
        renpy.config.missing_hide(name, layer)
    

def scene(layer='master'):
    """
    :doc: se_images

    Removes all displayables from `layer`. This is equivalent to the scene
    statement, when the scene statement is not given an image to show.

    A full scene statement is equivalent to a call to renpy.scene followed by a
    call to :func:`renpy.show`. For example::
    
        scene bg beach 
        
    is equivalent to::
    
        $ renpy.scene()
        $ renpy.show("bg beach")        
    """

    if renpy.game.context().init_phase:
        raise Exception("Scene may not run while in init phase.")

    sls = scene_lists()
    sls.clear(layer)

    if renpy.config.missing_scene:
        renpy.config.missing_scene(layer)
        
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

def input(prompt, default='', allow=None, exclude='{}', length=None, with_none=None):
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

    @param with_none: If True, performs a with None after the input. If None,
    takes the value from config.implicit_with_none.
    """

    renpy.exports.mode('input')
    
    if has_screen("input"):
        widget_properties = { }
        widget_properties["input"] = dict(default=default, length=length, allow=allow, exclude=exclude)

        show_screen("input", _transient=True, _widget_properties=widget_properties, prompt=prompt)

    else:

        renpy.ui.window(style='input_window')
        renpy.ui.vbox()

        renpy.ui.text(prompt, style='input_prompt')
        renpy.ui.input(default, length=length, style='input_text', allow=allow, exclude=exclude)

        renpy.ui.close()

    renpy.exports.shown_window()
        
    roll_forward = renpy.exports.roll_forward_info()
    if not isinstance(roll_forward, basestring):
        roll_forward = None

    rv = renpy.ui.interact(mouse='prompt', type="input", roll_forward=roll_forward)
    renpy.exports.checkpoint(rv)
    
    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv

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

    # This only makes sense for non-NVL menus. But when we have
    # NVL menus, they're likely to have already been predicted.
    #
    # An item lets us load imagebuttons as necessary.

    if not renpy.config.choice_screen_chosen:
        return
                
    items = [ ("Menu Prediction", True, False) ]
    
    predict_screen(
        "choice",
        items=items,
        )

    
def display_menu(items,
                 window_style='menu_window',
                 interact=True,
                 with_none=None,
                 caption_style='menu_caption',
                 choice_style='menu_choice',
                 choice_chosen_style='menu_choice_chosen',
                 choice_button_style='menu_choice_button',
                 choice_chosen_button_style='menu_choice_chosen_button',
                 scope={ },
                 widget_properties=None,
                 screen="choice",
                 type="menu",
                 predict_only=False,
                 **kwargs):
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

    @param with_none: If True, performs a with None after the input. If None,
    takes the value from config.implicit_with_none.
    """

    if interact:
        renpy.exports.mode(type)    
        choice_for_skipping()

    # The possible choices in the menu.
    choices = [ val for label, val in items ]
    while None in choices:
        choices.remove(None)

    # Roll forward.
    roll_forward = renpy.exports.roll_forward_info()

    if roll_forward not in choices:
        roll_forward = None
        
    # Auto choosing.
    if renpy.config.auto_choice_delay:

        renpy.ui.pausebehavior(renpy.config.auto_choice_delay,
                               random.choice(choices))

    # The chosen dictionary.
    chosen = renpy.game.persistent._chosen
    if chosen is None:
        chosen = renpy.game.persistent._chosen = { }

    # The location
    location=renpy.game.context().current
     
        
    # Show the menu.
    if has_screen(screen):

        item_actions = [ ]

        if widget_properties is None:
            props = { }
        else:
            props = widget_properties
            
        for (label, value) in items:

            if not label:
                value = None

            if value is not None:
                action = renpy.ui.returns(value)
            else:
                action = None
                
            label_chosen = ((location, label) in chosen)
                
            if renpy.config.choice_screen_chosen:
                item_actions.append((label, action, label_chosen))
            else:
                item_actions.append((label, action))

            show_screen(screen, items=item_actions, _widget_properties=props, _transient=True, **scope)

    else:
        renpy.ui.window(style=window_style, focus="menu")
        renpy.ui.menu(items,
                      location=renpy.game.context().current,
                      focus="choices",
                      default=True,
                      caption_style=caption_style,
                      choice_style=choice_style,
                      choice_chosen_style=choice_chosen_style,
                      choice_button_style=choice_button_style,
                      choice_chosen_button_style=choice_chosen_button_style,
                      **kwargs)

    renpy.exports.shown_window()

    # Log the chosen choice.
    for label, val in items:
        if val:
            log("Choice: " + label)
        else:
            log(label)

    log("")

    if interact:
            
        rv = renpy.ui.interact(mouse='menu', type=type, roll_forward=roll_forward)

        # Mark this as chosen.
        for label, val in items:
            if rv == val:
                chosen[(location, label)] = True

        
        for label, val in items:
            if rv == val:
                log("User chose: " + label)
                break
        else:
            log("No choice chosen.")

        log("")

        checkpoint(rv)
        
        if with_none is None:
            with_none = renpy.config.implicit_with_none

        if with_none:
            renpy.game.interface.do_with(None, None)

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

def predict_say(who, what):
    """
    This is called to predict the results of a say command.
    """

    if who is None:
        who = renpy.store.narrator # E1101 @UndefinedVariable

    if isinstance(who, (str, unicode)):
        return renpy.store.predict_say(who, what)

    predict = getattr(who, 'predict', None)
    if predict: 
        predict(what)

def scry_say(who, scry):
    """
    Called when scry is called on a say statement. Needs to set
    the interacts field.
    """
    
    try:
        scry.interacts = who.will_interact()
    except:
        scry.interacts = True
        
def say(who, what, interact=True):
    """
    This is the core of the say command. If the who parameter is None
    or a string, it is passed directly to display_say. Otherwise, the
    say method is called on the who object with what as a parameter.
    """
    
    # Interpolate variables.
    what = what % tag_quoting_dict

    if who is None:
        who = renpy.store.narrator # E1101 @UndefinedVariable

    if isinstance(who, (str, unicode)):
        renpy.store.say(who, what, interact=interact)
    else:
        who(what, interact=interact)

        
def imagemap(ground, selected, hotspots, unselected=None, overlays=False,
             style='imagemap', mouse='imagemap', with_none=None, **properties):
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

    @param with_none: If True, performs a with None after the input. If None,
    takes the value from config.implicit_with_none.
    """

    renpy.exports.mode('imagemap')
    
    renpy.ui.imagemap_compat(ground, selected, hotspots, unselected=unselected,
                             style=style, **properties)

    roll_forward = renpy.exports.roll_forward_info()
    if roll_forward not in [ result for _x0, _y0, _x1, _y1, result in hotspots]:
        roll_forward = None
    
    rv = renpy.ui.interact(suppress_overlay=(not overlays),
                           type='imagemap',
                           mouse=mouse,
                           roll_forward=roll_forward)

    renpy.exports.checkpoint(rv)

    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv
    

def pause(delay=None, music=None, with_none=None, hard=False):
    
    if renpy.config.skipping == "fast":
        return True

    renpy.exports.mode('pause')
    
    if music is not None:
        newdelay = renpy.audio.music.get_delay(music)

        if newdelay is not None:
            delay = newdelay

    if hard:            
        renpy.ui.saybehavior(dismiss='dismiss_hard_pause')
    else:
        renpy.ui.saybehavior()
        
    if delay is not None:
        renpy.ui.pausebehavior(delay, False)

    roll_forward = renpy.exports.roll_forward_info()
    if roll_forward not in [ True, False ]:
        roll_forward = None
    
    rv = renpy.ui.interact(mouse='pause', type='pause', roll_forward=roll_forward)
    renpy.exports.checkpoint(rv, keep_rollback=True)


    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv


def movie_cutscene(filename, delay=None, loops=0, stop_music=True):
    """
    This displays an MPEG-1 cutscene for the specified number of
    seconds. The user can click to interrupt the cutscene.
    Overlays and Underlays are disabled for the duration of the cutscene.

    @param filename: The name of a file containing an MPEG-1 movie.

    @param delay: The number of seconds to wait before ending the cutscene.
    Normally the length of the movie, in seconds. If None, then the
    delay is computed from the number of loops (that is, loops + 1) *
    the length of the movie. If -1, we wait until the user clicks.
    
    @param loops: The number of extra loops to show, -1 to loop forever.

    Returns True if the movie was terminated by the user, or False if the
    given delay elapsed uninterrupted.
    """

    renpy.exports.mode('movie')
    
    if stop_music:
        renpy.audio.audio.set_force_stop("music", True)
    
    movie_start_fullscreen(filename, loops=loops)
    
    renpy.ui.saybehavior()

    if delay is None or delay < 0:
        renpy.ui.soundstopbehavior("movie")
    else:
        renpy.ui.pausebehavior(delay, False)

    if renpy.game.log.forward:
        roll_forward = True
    else:
        roll_forward = None
    
    rv = renpy.ui.interact(suppress_overlay=True,
                           suppress_underlay=True,
                           show_mouse=False,
                           roll_forward=roll_forward)

    # We don't want to put a checkpoint here, as we can't roll back while
    # playing a cutscene.

    movie_stop()

    if stop_music:
        renpy.audio.audio.set_force_stop("music", False)

    return rv
        

def with_statement(trans, always=False, paired=None, clear=True):
    """
    :doc: se_with
    :name: renpy.with_statement
    :args: (trans, always=False)
    
    Causes a transition to occur. This is the python equivalent of the
    with statement.
    
    `trans`
        The transition.
        
    `always`
        If True, the transition will always occur, even if the user has
        disabled transitions.
        
    This function returns true if the user chose to interrupt the transition,
    and false otherwise. 
    """

    if renpy.game.context().init_phase:
        raise Exception("With statements may not run while in init phase.")

    if renpy.config.skipping:
        trans = None

    if not (renpy.game.preferences.transitions or always):
        trans = None

    renpy.exports.mode('with')
        
    return renpy.game.interface.do_with(trans, paired, clear=clear)

globals()["with"] = with_statement

def rollback(force=False):
    """
    Rolls the state of the game back to the last checkpoint.
    """

    if not force:
    
        if not renpy.store._rollback:
            return
        
        if not renpy.game.context().rollback:
            return
    
        if not renpy.config.rollback_enabled:
            return
        
    renpy.config.skipping = None
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

def get_all_labels():
    rv = [ ]

    for i in renpy.game.script.namemap.iterkeys():
        if isinstance(i, basestring):
            rv.append(i)

    return renpy.python.RevertableSet(rv)
    

def take_screenshot(scale=None, background=False):
    """
    This causes a screenshot to be taken. This screenshot will be
    saved with a savegame when the game is saved.
    """

    if scale is None:
        scale = (renpy.config.thumbnail_width, renpy.config.thumbnail_height)
    
    renpy.game.interface.take_screenshot(scale, background=background)

def full_restart(transition=False, label="_invoke_main_menu", target="_main_menu"):
    """
    This causes a full restart of Ren'Py. 
    """

    if transition is False:
        transition = renpy.config.end_game_transition
    
    raise renpy.game.FullRestartException((transition, label, target))

def utter_restart():
    """
    This causes an utter restart of Ren'Py. This reloads the script and
    re-runs initialization.
    """

    raise renpy.game.UtterRestartException()

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
    
    renpy.game.interface.save_screenshot(filename)
    
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

def transition(trans, layer=None, always=False, force=False):
    """
    Sets the transition that will be used for the next
    interaction. This is useful when the next interaction doesn't take
    a with clause, as is the case with pause, input, and imagemap.

    @param layer: If the layer setting is not None, then the transition
    will be applied only to the layer named. Please note that only some
    transitions can be applied to specific layers.
    """

    if not always and not renpy.game.preferences.transitions:
        trans = None

    renpy.game.interface.set_transition(trans, layer, force=force)

def get_transition(layer=None):
    return renpy.game.interface.transition.get(layer, None)
        
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

def context_nesting_level():
    """
    Returns the nesting level of the current context. This is 0 for the
    outermost context (the context that is saved, and in which most of
    the game runs), and greater than zero when in a menu or other nested
    context.
    """

    return len(renpy.game.contexts) - 1
    
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

    n = renpy.game.script.namemap.get(renpy.game.context().current, None)
    
    if n is None:
        return "unknown", 0
    else:
        return n.filename, n.linenumber

def shell_escape(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("\"", "\\\"")
    return s

def split_args(s):

    rv = [ ]
    word = ""
    quoted = False
        
    i = 0
    while i < len(s):
        c = s[i]
        i += 1

        if not quoted and c == ' ' and word:
            if word:
                rv.append(word)
                word = ""
            continue
            
        if c == '"':
            quoted = not quoted
            continue

        if c == '\\':
            c = s[i]
            i += 1

        word += c

    if word:
        rv.append(word)

    return rv

def launch_editor(filenames, line=1, transient=0):
    """
    This causes an editor to be launched at the location of the current
    statement.
    """

    import renpy.subprocess as subprocess
    import os.path

    if not renpy.config.editor:
        return

    if not len(filenames):
        return

    filenames = [ renpy.parser.unelide_filename(i) for i in filenames ]
    filenames = [ shell_escape(os.path.normpath(i)) for i in filenames ]
    filename = filenames[0]

    allfiles = renpy.config.editor_file_separator.join(filenames)
    otherfiles = renpy.config.editor_file_separator.join(filenames[1:])
    
    subs = dict(filename=filename, line=line, allfiles=allfiles, otherfiles=otherfiles)
    if transient and (renpy.config.editor_transient is not None):
        cmd = renpy.config.editor_transient % subs
    else:
        cmd = renpy.config.editor % subs

    cmd = cmd.replace('""', '')

    try:
        subprocess.Popen(split_args(cmd)) # E1101 @UndefinedVariable
        return True
    except:
        if renpy.config.debug:
            raise
        return False

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

        logfile = _file(renpy.config.log, "a")
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

    renpy.game.interface.full_redraw = True

def do_reshow_say(who, what, interact=False):
    
    if who is not None:
        who = renpy.python.py_eval(who)

    say(who, what, interact=interact)

curried_do_reshow_say = curry(do_reshow_say)
    
def get_reshow_say(**kwargs):
    return curried_do_reshow_say(
        renpy.store._last_say_who,
        renpy.store._last_say_what,
        **kwargs)

def reshow_say(**kwargs):
    get_reshow_say()(**kwargs)

def current_interact_type():
    return getattr(renpy.game.context().info, "_current_interact_type", None)

def last_interact_type():
    return getattr(renpy.game.context().info, "_last_interact_type", None)

def dynamic(*vars):
    renpy.game.context().make_dynamic(vars)

def context_dynamic(*vars):
    renpy.game.context().make_dynamic(vars, context=True)
    
def seen_label(label):
    return label in renpy.game.seen_ever

def seen_audio(filename):
    return filename in renpy.game.persistent._seen_audio

def seen_image(name):
    if not isinstance(name, tuple):
        name = tuple(name.split())
    
    return name in renpy.game.persistent._seen_images

def file(fn):
    return renpy.loader.load(fn)

def image_size(im):
    """
    :doc: other

    Given an image manipulator, loads it and returns a (``width``,
    ``height``) tuple giving its size.

    This reads the image in from disk and decompresses it, without
    using the image cache. This can be slow.
    """
    
    # Index the archives, if we haven't already.
    renpy.loader.index_archives()

    im = renpy.easy.displayable(im)

    if not isinstance(im, renpy.display.im.Image):
        raise Exception("renpy.image_size expects it's argument to be an image.")

    surf = im.load()
    return surf.get_size()

def get_at_list(name, layer='master'):
    if isinstance(name, basestring):
        name = tuple(name.split())

    tag = name[0]

    return renpy.game.context().scene_lists.at_list[layer].get(tag, None)

def layer_at_list(at_list, layer='master'):
    renpy.game.context().scene_lists.set_layer_at_list(layer, at_list)

def free_memory():
    force_full_redraw()
    renpy.display.im.free_memory()
    renpy.display.font.free_memory()
    renpy.display.render.free_memory() # @UndefinedVariable

def easy_displayable(d, none=False):
    if none:
        return renpy.easy.displayable(d)
    else:
        return renpy.easy.displayable_or_none(d)

def quit_event():
    renpy.game.interface.quit_event()

def iconify():
    renpy.game.interface.iconify()
    
# New context stuff.
call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(renpy.game.call_in_new_context)
invoke_in_new_context = renpy.game.invoke_in_new_context
curried_invoke_in_new_context = renpy.curry.curry(renpy.game.invoke_in_new_context)

# Error handling stuff.
def _error(msg):
    raise Exception(msg)
    
_error_handlers = [ _error ]
    
def push_error_handler(eh):
    _error_handlers.append(eh)

def pop_error_handler():
    _error_handlers.pop()

def error(msg):
    _error_handlers[-1](msg)
    
def timeout(seconds):
    renpy.game.interface.timeout(seconds)

def scry():
    name = renpy.game.context().current
    node = renpy.game.script.lookup(name)
    return node.scry()

def munged_filename():
    return renpy.parser.munge_filename(get_filename_line()[0])

# Module loading stuff.

loaded_modules = set()

def load_module(name, **kwargs):

    if not renpy.game.context().init_phase:
        raise Exception("Module loading is only allowed in init code.")

    if name in loaded_modules:
        return

    loaded_modules.add(name)
    
    old_locked = renpy.config.locked
    renpy.config.locked = False
    
    initcode = renpy.game.script.load_module(name)

    context = renpy.execution.Context(False)
    context.init_phase = True
    renpy.game.contexts.append(context)
    
    context.make_dynamic(kwargs)
    renpy.store.__dict__.update(kwargs) #@UndefinedVariable
    
    for prio, node in initcode: #@UnusedVariable
        renpy.game.context().run(node)

    context.pop_all_dynamic()
        
    renpy.game.contexts.pop()

    renpy.config.locked = old_locked

def pop_return():
    renpy.game.context().pop_dynamic()
    renpy.game.context().lookup_return(pop=True)
    
def game_menu(screen=None):
    if screen is None:
        call_in_new_context("_game_menu")
    else:
        call_in_new_context("_game_menu", screen)

def shown_window():
    renpy.game.context().scene_lists.shown_window = True

class placement(renpy.python.RevertableObject):
    def __init__(self, p):
        super(placement, self).__init__()

        self.xpos = p[0]
        self.ypos = p[1]
        self.xanchor = p[2]
        self.yanchor = p[3]
        self.xoffset = p[4]
        self.yoffset = p[5]
        self.subpixel = p[6]

def get_placement(d):
    p = d.get_placement()

    return placement(p)
    
# User-Defined Displayable stuff.

Render = renpy.display.render.Render
render = renpy.display.render.render
IgnoreEvent = renpy.display.core.IgnoreEvent
redraw = renpy.display.render.redraw

class Displayable(renpy.display.core.Displayable, renpy.python.RevertableObject):
    pass

class Container(renpy.display.core.Displayable, renpy.python.RevertableObject):
    _list_type = renpy.python.RevertableList
    
def get_roll_forward():
    return renpy.game.interface.shown_window

def cache_pin(*args):
    
    new_pins = renpy.python.RevertableSet()

    for i in args:

        im = renpy.easy.displayable(i)

        if not isinstance(im, renpy.display.im.ImageBase):
            raise Exception("Cannot pin non-image-manipulator %r" % im)

        new_pins.add(im)

    renpy.store._cache_pin_set = new_pins | renpy.store._cache_pin_set 


def cache_unpin(*args):
    
    new_pins = renpy.python.RevertableSet()

    for i in args:

        im = renpy.easy.displayable(i)

        if not isinstance(im, renpy.display.im.ImageBase):
            raise Exception("Cannot unpin non-image-manipulator %r" % im)

        new_pins.add(im)

    renpy.store._cache_pin_set = renpy.store._cache_pin_set - new_pins


# This is a map from a definition to the place where it was
# defined.
definitions = collections.defaultdict(list)

def call_screen(_screen_name, **kwargs):
    """
    :doc: screens

    The programmatic equivalent of the show screen statement.
    
    This shows `_screen_name` as a screen, then causes an interaction
    to occur. The screen is hidden at the end of the interaction, and
    the result of the interaction is returned.

    Keyword arguments not beginning with _ are passed to the scope of
    the screen.
    """

    renpy.exports.mode('screen')
    
    show_screen(_screen_name, _transient=True, **kwargs)

    roll_forward = renpy.exports.roll_forward_info()
    rv = None
    
    try:
        rv = renpy.ui.interact(mouse="screen", type="screen", roll_forward=roll_forward)
        return rv
    
    finally:
        
        renpy.exports.checkpoint(rv)

        with_none = renpy.config.implicit_with_none
        if with_none:
            renpy.game.interface.do_with(None, None)
    
def list_files(common=False):
    """
    :doc: other

    Lists the files in the game directory and archive files. Returns
    a list of files, with / as the directory separator.

    `common`
        If true, files in the common directory are included in the
        listing.
    """

    rv = [ ]
    
    for dir, fn in renpy.loader.listdirfiles():

        if not common and dir == renpy.config.commondir:
            continue

        rv.append(fn)

    return rv
        
def get_renderer_info():
    """
    :doc: other

    Returns a dictionary, giving information about the renderer Ren'Py is
    currently using. The dictionary has one required key:

    ``"renderer"``
        One of ``"gl"`` or ``"sw"``, corresponding to the OpenGL and
        software renderers, respectively.

    ``"resizable``
        True if and only if the window is resizable.

    Other, renderer-specific, keys may also exist. The dictionary should
    be treated as immutable. This should only be called once the display
    has been started (that is, after the init code is finished).
    """

    return renpy.display.draw.info
    
def display_reset():
    """
    Used internally. Causes the display to be restarted at the start of
    the next interaction.
    """
    
    renpy.display.interface.display_reset = True

def mode(mode):
    """
    :doc: modes

    Causes Ren'Py to enter the named mode, or stay in that mode if it's
    already in it.
    """

    ctx = renpy.game.context()

    if not ctx.use_modes:
        return

    modes = ctx.modes

    try:
        ctx.use_modes = False

        if mode != modes[0]:        
            for c in renpy.config.mode_callbacks:
                c(mode, modes)

    finally:
        ctx.use_modes = True            
            
    if mode in modes:
        modes.remove(mode)
    modes.insert(0, mode)

def notify(message):
    """
    :doc: other

    Causes Ren'Py to display the `message` using the notify screen. By
    default, this will cause the message to be dissolved in, displayed
    for two seconds, and dissolved out again.

    This is useful for actions that otherwise wouldn't produce feedback,
    like screenshots or quicksaves.

    Only one notification is displayed at a time. If a second notification
    is displayed, the first notification is replaced.    
    """

    hide_screen('notify')
    show_screen('notify', message=message)
    restart_interaction()

def variant(name):
    """
    :doc: screens

    Returns true if a `name` is a screen variant that can be chosen
    by Ren'Py. See :ref:`screen-variants` for more details. This function
    can be used as the condition in a python if statement to set up the
    appropriate styles for the selected screen variant.
    """

    return name in renpy.config.variants

def vibrate(duration):
    """
    :doc: other

    Causes the device to vibrate for `duration` seconds. Currently, this
    is only supported on Android.
    """

    try:
        import android #@UnresolvedImport
        android.vibrate(duration)
    except:
        pass
    

# The attributes that are applied to the current say statement.
say_attributes = None
    
def get_say_attributes():
    """
    :doc: other

    Gets the attributes associated with the current say statement, or
    None if no attributes are associated with this statement.

    This is only valid when executing or predicting a say statement.
    """

    return say_attributes

side_image_attributes = None

def get_side_image(tag):
    """
    :doc: other
    
    This attempts to find an image to show as the side image. It attempts to
    find an image that begins with tag, and matches side_image_attributes. It
    returns the name of the image (as a tuple of strings) if possible, or 
    None if that's not possible.
    """
    
    if side_image_attributes is None:
        return
    
    images = renpy.game.context().images
    
    required = set()
    optional = set(side_image_attributes)
    
    return images.choose_image(tag, required, optional, None)

def get_physical_size():
    """
    :doc: other
    
    Returns the size of the physical window.
    """
    
    return renpy.display.draw.get_physical_size()

def set_physical_size(size):
    """
    :doc: other
    
    Attempts to set the size of the physical window to size. This has the 
    side effect of taking the screen out of windowed mode.
    """

    renpy.game.preferences.fullscreen = False
    
    if get_renderer_info()["resizable"]:
        renpy.display.interface.set_mode(size)
                