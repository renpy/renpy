# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.pyanalysis import const, pure, not_const

def renpy_pure(fn):
    """
    Marks renpy.`fn` as a pure function.
    """

    name = fn

    if not isinstance(name, basestring):
        name = fn.__name__

    pure("renpy." + name)

    return fn

from renpy.text.extras import ParameterizedText
from renpy.text.font import register_sfont, register_mudgefont, register_bmfont
from renpy.text.text import language_tailor
from renpy.display.behavior import Keymap
from renpy.display.behavior import run as run_action, run_unhovered, run_periodic
from renpy.display.behavior import map_event, queue_event, clear_keymap_cache

from renpy.display.minigame import Minigame
from renpy.display.screen import define_screen, show_screen, hide_screen, use_screen, current_screen
from renpy.display.screen import has_screen, get_screen, get_widget, ScreenProfile as profile_screen
from renpy.display.focus import focus_coordinates
from renpy.display.predict import screen as predict_screen
from renpy.display.image import image_exists, image_exists as has_image
from renpy.display.im import load_surface, load_image

from renpy.curry import curry, partial
from renpy.audio.sound import play
from renpy.display.video import movie_start_fullscreen, movie_start_displayable, movie_stop

from renpy.loadsave import load, save, list_saved_games, can_load, rename_save, copy_save, unlink_save, scan_saved_game
from renpy.loadsave import list_slots, newest_slot, slot_mtime, slot_json, slot_screenshot, force_autosave

from renpy.python import py_eval as eval
from renpy.python import rng as random
from renpy.atl import atl_warper
from renpy.easy import predict, displayable
from renpy.parser import unelide_filename, get_parse_errors
from renpy.translation import change_language, known_languages

from renpy.persistent import register_persistent

from renpy.character import show_display_say, predict_show_display_say, display_say

import renpy.audio.sound as sound
import renpy.audio.music as music

from renpy.statements import register as register_statement
from renpy.text.extras import check_text_tags

from renpy.memory import profile_memory, diff_memory, profile_rollback

from renpy.text.textsupport import TAG as TEXT_TAG, TEXT as TEXT_TEXT, PARAGRAPH as TEXT_PARAGRAPH, DISPLAYABLE as TEXT_DISPLAYABLE

from renpy.execution import not_infinite_loop

from renpy.sl2.slparser import CustomParser as register_sl_statement

renpy_pure("ParameterizedText")
renpy_pure("Keymap")
renpy_pure("has_screen")
renpy_pure("image_exists")
renpy_pure("curry")
renpy_pure("partial")
renpy_pure("unelide_filename")
renpy_pure("known_languages")
renpy_pure("check_text_tags")

import time
import sys
import threading

def public_api():
    """
    :undocumented:

    This does nothing, except to make warnings about unused imports go away.
    """
    ParameterizedText
    register_sfont, register_mudgefont, register_bmfont
    Keymap
    run_action, run_unhovered, run_periodic, map_event
    Minigame
    curry, partial
    play
    movie_start_fullscreen, movie_start_displayable, movie_stop
    load, save, list_saved_games, can_load, rename_save, copy_save, unlink_save, scan_saved_game
    list_slots, newest_slot, slot_mtime, slot_json, slot_screenshot, force_autosave
    eval
    random
    atl_warper
    show_display_say, predict_show_display_say, display_say
    sound
    music
    time
    define_screen, show_screen, hide_screen, use_screen, has_screen
    current_screen, get_screen, get_widget, profile_screen
    focus_coordinates
    predict, predict_screen
    displayable
    unelide_filename, get_parse_errors
    change_language, known_languages
    language_tailor
    register_persistent
    register_statement
    check_text_tags
    map_event, queue_event, clear_keymap_cache
    const, pure, not_const
    image_exists, has_image
    load_image, load_surface
    profile_memory, diff_memory, profile_rollback
    TEXT_TAG
    TEXT_TEXT
    TEXT_PARAGRAPH
    TEXT_DISPLAYABLE
    not_infinite_loop
    register_sl_statement

del public_api


def roll_forward_info():
    """
    :doc: rollback

    When in rollback, returns the data that was supplied to :func:`renpy.checkpoint`
    the last time this statement executed. Outside of rollback, returns None.
    """

    if not renpy.game.context().rollback:
        return None

    return renpy.game.log.forward_info()


def roll_forward_core(value=None):
    """
    :undocumented:

    To cause a roll_forward to occur, return the value of this function
    from an event handler.
    """

    if value is None:
        value = roll_forward_info()
    if value is None:
        return

    renpy.game.interface.suppress_transition = True
    renpy.game.after_rollback = True
    renpy.game.log.rolled_forward = True

    return value


def in_rollback():
    """
    :doc: rollback

    Returns true if the game has been rolled back.
    """

    return renpy.game.log.in_rollback()


def can_rollback():
    """
    :doc: rollback

    Returns true if we can rollback.
    """

    return renpy.game.log.can_rollback()


def in_fixed_rollback():
    """
    :doc: blockrollback

    Returns true if rollback is currently occurring and the current
    context is before an executed renpy.fix_rollback() statement.
    """

    return renpy.game.log.in_fixed_rollback()


def checkpoint(data=None, keep_rollback=None):
    """
    :doc: rollback
    :args: (data=None)

    Makes the current statement a checkpoint that the user can rollback to. Once
    this function has been called, there should be no more interaction with the
    user in the current statement.

    `data`
        This data is returned by :func:`renpy.roll_forward_info` when the
        game is being rolled back.
    """

    if renpy.store._rollback:
        if keep_rollback is None:
            keep_rollback = renpy.config.keep_rollback_data

        renpy.game.log.checkpoint(data, keep_rollback=keep_rollback)


def block_rollback():
    """
    :doc: blockrollback

    Prevents the game from rolling back to before the current
    statement.
    """

    renpy.game.log.block()


def suspend_rollback(flag):
    """
    :doc: rollback
    :args: (flag)

    Rollback will skip sections of the game where rollback has been
    suspended.

    `flag`:
        When `flag` is true, rollback is suspended. When false,
        rollback is resumed.
    """

    renpy.game.log.suspend_checkpointing(flag)


def fix_rollback():
    """
    :doc: blockrollback

    Prevents the user from changing decisions made before the current
    statement.
    """
    renpy.game.log.fix_rollback()


def retain_after_load():
    """
    :doc: retain_after_load

    Causes data modified between the current statement and the statement
    containing the next checkpoint to be retained when a load occurs.
    """

    renpy.game.log.retain_after_load()


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
    """
    :doc: image_func

    Copies images beginning with one prefix to images beginning with
    another. For example::

        renpy.copy_images("eileen", "eileen2")

    will create an image beginning with "eileen2" for every image beginning
    with "eileen". If "eileen happy" exists, "eileen2 happy" will be
    created.

    `old`
        A space-separated string giving the components of the old image
        name.

    `new`
        A space-separated string giving the components of the new image
        name.

    """

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
    :doc: image_func

    Returns true if an image with the same tag as `name` is showing on
    `layer`

    `image`
        May be a string giving the image name or a tuple giving each
        component of the image name. It may also be a string giving
        only the image tag.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    return renpy.game.context().images.showing(layer, name)

def get_showing_tags(layer='master'):
    """
    :doc: image_func

    Returns the set of image tags that are currently being shown on `layer`
    """

    return renpy.game.context().images.get_showing_tags(layer)

def predict_show(name, layer='master', what=None, tag=None, at_list=[ ]):
    """
    :undocumented:

    Predicts a scene or show statement.

    `name`
        The name of the image to show, a string.

    `layer`
        The layer the image is being show non.

    `what`
        What is being show - if given, overrides `name`.

    `tag`
        The tag of the thing being shown.

    `at_list`
        A list of transforms to apply to the displayable.
    """

    key = tag or name[0]

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

        if not base.find_target():
            return

    for i in at_list:
        if isinstance(i, renpy.display.motion.Transform):
            img = i(child=img)
        else:
            img = i(img)

    renpy.game.context().images.predict_show(layer, name, True)
    renpy.display.predict.displayable(img)


def show(name, at_list=[ ], layer='master', what=None, zorder=None, tag=None, behind=[ ], atl=None, transient=False, munge_name=True):
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
        An integer, the equivalent of the ``zorder`` property. If None, the
        zorder is preserved if it exists, and is otherwise set to 0.

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

    if zorder is None and not renpy.config.preserve_zorder:
        zorder = 0

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
            result = renpy.config.missing_show(name, what, layer)

            if isinstance(result, renpy.display.core.Displayable):
                base = img = result
            elif result:
                return

    for i in at_list:
        if isinstance(i, renpy.display.motion.Transform):
            img = i(child=img)
        else:
            img = i(img)

    # Update the list of images we have ever seen.
    renpy.game.persistent._seen_images[name] = True  # @UndefinedVariable

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


def input(prompt, default='', allow=None, exclude='{}', length=None, with_none=None, pixel_width=None): #@ReservedAssignment
    """
    :doc: input

    Calling this function pops up a window asking the player to enter some
    text. It returns the entered text.

    `prompt`
        A string giving a prompt to display to the player.

    `default`
        A string giving the initial text that will be edited by the player.

    `allow`
        If not None, a string giving a list of characters that will
        be allowed in the text.

    `exclude`
        If not None, if a character is present in this string, it is not
        allowed in the text.

    `length`
        If not None, this must be an integer giving the maximum length
        of the input string.

    `pixel_width`
        If not None, the input is limited to being this many pixels wide,
        in the font used by the input to display text.
    """

    renpy.exports.mode('input')

    roll_forward = renpy.exports.roll_forward_info()
    if not isinstance(roll_forward, basestring):
        roll_forward = None

    # use previous data in rollback
    if roll_forward is not None:
        default = roll_forward

    fixed = in_fixed_rollback();

    if has_screen("input"):
        widget_properties = { }
        widget_properties["input"] = dict(default=default, length=length, allow=allow, exclude=exclude, editable=not fixed, pixel_width=pixel_width)

        show_screen("input", _transient=True, _widget_properties=widget_properties, prompt=prompt)

    else:

        renpy.ui.window(style='input_window')
        renpy.ui.vbox()

        renpy.ui.text(prompt, style='input_prompt')

        inputwidget = renpy.ui.input(default, length=length, style='input_text', allow=allow, exclude=exclude)

        # disable input in fixed rollback
        if fixed:
            inputwidget.disable()

        renpy.ui.close()

    renpy.exports.shown_window()

    if not renpy.game.after_rollback:
        renpy.loadsave.force_autosave(True)

    # use normal "say" click behavior if input can't be changed
    if fixed:
        renpy.ui.saybehavior()

    rv = renpy.ui.interact(mouse='prompt', type="input", roll_forward=roll_forward)
    renpy.exports.checkpoint(rv)

    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv


def menu(items, set_expr):
    """
    :undocumented:

    Displays a menu, and returns to the user the value of the selected
    choice. Also handles conditions and the menuset.
    """

    if renpy.config.old_substitutions:
        def substitute(s):
            return s % tag_quoting_dict
    else:
        def substitute(s):
            return s


    # Filter the list of items to only include ones for which the
    # condition is true.
    items = [ (substitute(label), value)
              for label, condition, value in items
              if renpy.python.py_eval(condition) ]

    # Filter the list of items on the set_expr:
    if set_expr:
        set = renpy.python.py_eval(set_expr) #@ReservedAssignment
        items = [ (label, value)
                  for label, value in items
                  if label not in set ]
    else:
        set = None #@ReservedAssignment

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
    :doc: other

    Tells Ren'Py that a choice is coming up soon. This currently has
    two effects:

    * If Ren'Py is skipping, and the Skip After Choices preferences is set
      to stop skipping, skipping is terminated.

    * An auto-save is triggered.
    """

    if renpy.config.skipping and not renpy.game.preferences.skip_after_choices:
        renpy.config.skipping = None

    if renpy.config.autosave_on_choice and not renpy.game.after_rollback:
        renpy.loadsave.force_autosave(True)



def predict_menu():
    """
    :undocumented:

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
                 type="menu", #@ReservedAssignment
                 predict_only=False,
                 **kwargs):
    """
    :doc: se_menu
    :args: (items, interact=True, screen="choice")

    This displays a menu to the user. `items` should be a list of 2-item tuples.
    In each tuple, the first item is a textual label, and the second item is
    the value to be returned if that item is selected. If the value is None,
    the first item is used as a menu caption.

    This function takes many arguments, of which only a few are documented.
    Except for `items`, all arguments should be given as keyword arguments.

    `interact`
        If false, the menu is displayed, but no interaction is performed.

    `screen`
        The name of the screen used to display the menu.

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

    # The location
    location=renpy.game.context().current

    # change behavior for fixed rollback
    if in_fixed_rollback() and renpy.config.fix_rollback_without_choice:
        renpy.ui.saybehavior()

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
                action = renpy.ui.ChoiceReturn(label, value, location)
            else:
                action = None

            if renpy.config.choice_screen_chosen:
                if action is not None:
                    item_actions.append((label, action, action.get_chosen()))
                else:
                    item_actions.append((label, action, False))
            else:
                item_actions.append((label, action))

            show_screen(screen, items=item_actions, _widget_properties=props, _transient=True, _layer=renpy.config.choice_layer, **scope)

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
        if val is not None:
            log("Choice: " + label)
        else:
            log(label)

    log("")

    if interact:

        rv = renpy.ui.interact(mouse='menu', type=type, roll_forward=roll_forward)

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

        store = renpy.store.__dict__

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
    :undocumented:

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
    :undocumented:

    Called when scry is called on a say statement. Needs to set
    the interacts field.
    """

    try:
        scry.interacts = who.will_interact()
    except:
        scry.interacts = True

def say(who, what, interact=True):
    """
    :doc: se_say

    The equivalent of the say statement.

    `who`
        Either the character that will say something, None for the narrator,
        or a string giving the character name. In the latter case, the
        :func:`say` is used to create the speaking character.

    `what`
        A string giving the line to say. Percent-substitutions are performed
        in this string.

    `interact`
        If true, Ren'Py waits for player input when displaying the dialogue. If
        false, Ren'Py shows the dialogue, but does not perform an interaction.

    This function is rarely necessary, as the following three lines are
    equivalent. ::

        e "Hello, world."
        $ renpy.say(e, "Hello, world.")
        $ e("Hello, world.")
    """

    if renpy.config.old_substitutions:
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
    :undocumented: Use screens already.

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

    if in_fixed_rollback() and renpy.config.fix_rollback_without_choice:
        renpy.ui.saybehavior()

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


def pause(delay=None, music=None, with_none=None, hard=False, checkpoint=None):
    """
    :doc: other

    Causes Ren'Py to pause. Returns true if the user clicked to end the pause,
    or false if the pause timed out or was skipped.

    `delay`
        If given, the number of seconds Ren'Py should pause for.

    `music`
        Retained for compatibility purposes.

    `with_none`
        Determines if a with None clause is executed at the end of the pause.

    `hard`
        If true, a click will not interrupt the pause. Use this sparingly,
        as it's hard to distinguish a hard pause from a crashing game.

    `checkpoint`
        If true, a checkpoint will be set, and players will be able to roll
        back to this statement. If false, no checkpoint will be set. If None,
        a checkpoint will only be set if display is set.
    """


    if checkpoint is None:
        if delay is not None:
            checkpoint = False
        else:
            checkpoint = True

    if renpy.config.skipping == "fast":
        return False

    roll_forward = renpy.exports.roll_forward_info()
    if roll_forward not in [ True, False ]:
        roll_forward = None

    renpy.exports.mode('pause')

    if music is not None:
        newdelay = renpy.audio.music.get_delay(music)

        if newdelay is not None:
            delay = newdelay

    if renpy.game.after_rollback and roll_forward is None:
        delay = 0

    if hard or not renpy.store._dismiss_pause:
        renpy.ui.saybehavior(dismiss='dismiss_hard_pause')
    else:
        renpy.ui.saybehavior()

    if delay is not None:
        renpy.ui.pausebehavior(delay, False)

    rv = renpy.ui.interact(mouse='pause', type='pause', roll_forward=roll_forward)

    if checkpoint:
        renpy.exports.checkpoint(rv, keep_rollback=True)

    if with_none is None:
        with_none = renpy.config.implicit_with_none

    if with_none:
        renpy.game.interface.do_with(None, None)

    return rv


def movie_cutscene(filename, delay=None, loops=0, stop_music=True):
    """
    :doc: movie_cutscene

    This displays an MPEG-1 cutscene for the specified number of
    seconds. The user can click to interrupt the cutscene.
    Overlays and Underlays are disabled for the duration of the cutscene.

    `filename`
        The name of a file containing an MPEG-1 movie.

    `delay`
        The number of seconds to wait before ending the cutscene.
        Normally the length of the movie, in seconds. If None, then the
        delay is computed from the number of loops (that is, loops + 1) *
        the length of the movie. If -1, we wait until the user clicks.

    `loops`
        The number of extra loops to show, -1 to loop forever.

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


def rollback(force=False, checkpoints=1, defer=False, greedy=True, label=None):
    """
    :doc: rollback

    Rolls the state of the game back to the last checkpoint.

    `force`
        If true, the rollback will occur in all circumstances. Otherwise,
        the rollback will only occur if rollback is enabled in the store,
        context, and config.

    `checkpoints`
        Ren'Py will roll back through this many calls to renpy.checkpoint. It
        will roll back as far as it can, subject to this condition.

    `defer`
        If true, the call will be deferred until code from the main context is
        executed.

    `greedy`
        If true, rollback will finish just after the previous checkpoint.
        If false, rollback finish just before the current checkpoint.

    `label`
        If not None, a label that is called when rollback completes.
    """

    if defer and len(renpy.game.contexts) > 1:
        renpy.game.contexts[0].defer_rollback = (force, checkpoints)
        return

    if not force:

        if not renpy.store._rollback:
            return

        if not renpy.game.context().rollback:
            return

        if not renpy.config.rollback_enabled:
            return

    renpy.config.skipping = None
    renpy.game.log.complete()
    renpy.game.log.rollback(checkpoints, greedy=greedy, label=label, force=force)


def toggle_fullscreen():
    """
    :undocumented:
    Toggles the fullscreen mode.
    """

    renpy.game.preferences.fullscreen = not renpy.game.preferences.fullscreen


def toggle_music():
    """
    :undocumented:
    Does nothing.
    """

@renpy_pure
def has_label(name):
    """
    :doc: label

    Returns true if `name` is a valid label the program, or false otherwise.

    `name`
        Should be a string to check for the existence of a label. It can
        also be an opaque tuple giving the name of a non-label statement.
    """

    return renpy.game.script.has_label(name)

@renpy_pure
def get_all_labels():
    """
    :doc: label

    Returns the set of all labels defined in the program, including labels
    defined for internal use in the libraries.
    """
    rv = [ ]

    for i in renpy.game.script.namemap.iterkeys():
        if isinstance(i, basestring):
            rv.append(i)

    return renpy.python.RevertableSet(rv)


def take_screenshot(scale=None, background=False):
    """
    :doc: loadsave

    Causes a screenshot to be taken. This screenshot will be saved as part of
    a save game.
    """

    if scale is None:
        scale = (renpy.config.thumbnail_width, renpy.config.thumbnail_height)

    renpy.game.interface.take_screenshot(scale, background=background)


def full_restart(transition=False, label="_invoke_main_menu", target="_main_menu"):
    """
    :doc: other

    Causes Ren'Py to restart, returning the user to the main menu.

    `transition`
        If given, the transition to run, or None to not run a transition.
        False uses :var:`config.end_game_transition`.
    """

    if transition is False:
        transition = renpy.config.end_game_transition

    raise renpy.game.FullRestartException((transition, label, target))


def utter_restart():
    """
    :undocumented: Used in the implementation of shift+R.

    Causes an utter restart of Ren'Py. This reloads the script and
    re-runs initialization.
    """

    raise renpy.game.UtterRestartException()


def reload_script():
    """
    :doc: other

    Causes Ren'Py to save the game, reload the script, and then load the
    save.
    """

    renpy.game.call_in_new_context("_save_reload_game")


def quit(relaunch=False, status=0): #@ReservedAssignment
    """
    :doc: other

    This causes Ren'Py to exit entirely.

    `relaunch`
        If true, Ren'Py will run a second copy of itself before quitting.

    `status`
        The status code Ren'Py will return to the operating system.
        Generally, 0 is success, and positive integers are failure.
    """

    raise renpy.game.QuitException(relaunch=relaunch, status=status)


def jump(label):
    """
    :doc: se_jump

    Causes the current statement to end, and control to jump to the given
    label.
    """

    raise renpy.game.JumpException(label)


def jump_out_of_context(label):
    """
    :doc: label

    Causes control to leave the current context, and then to be
    transferred in the parent context to the given label.
    """

    raise renpy.game.JumpOutException(label)


def call(label, *args, **kwargs):
    """
    :doc: se_call

    Causes the current Ren'Py statement to terminate, and a jump to a
    `label` to occur. When the jump returns, control will be passed
    to the statement following the current statement.
    """

    raise renpy.game.CallException(label, args, kwargs)

def return_statement():
    """
    :doc: se_call

    Causes Ren'Py to return from the current Ren'Py-level call.
    """

    jump("_renpy_return")


def screenshot(filename):
    """
    :doc: other

    Saves a screenshot in `filename`.
    """

    renpy.game.interface.save_screenshot(filename)

@renpy_pure
def version(tuple=False): #@ReservedAssignment
    """
    :doc: other

    If `tuple` is false, returns a string containing "Ren'Py ", followed by
    the current version of Ren'Py.

    If `tuple` is true, returns a tuple giving each component of the
    version as an integer.
    """

    if tuple:
        return renpy.version_tuple

    return renpy.version


def transition(trans, layer=None, always=False, force=False):
    """
    :doc: other
    :args: (trans, layer=None, always=False)

    Sets the transition that will be used during the next interaction.

    `layer`
        The layer the transition applies to. If None, the transition
        applies to the entire scene.

    `always`
        If false, this respects the transition preference. If true, the
        transition is always run.
    """

    if not always and not renpy.game.preferences.transitions:
        trans = None

    renpy.game.interface.set_transition(trans, layer, force=force)


def get_transition(layer=None):
    """
    :doc: other

    Gets the transition for `layer`, or the entire scene if
    `layer` is None. This returns the transition that is queued up
    to run during the next interaction, or None if no such
    transition exists.
    """

    return renpy.game.interface.transition.get(layer, None)


def clear_game_runtime():
    """
    :doc: other

    Resets the game runtime counter.
    """

    renpy.game.contexts[0].runtime = 0


def get_game_runtime():
    """
    :doc: other

    Returns the game runtime counter.

    The game runtime counter counts the number of seconds that have
    elapsed while waiting for user input in the top-level context.
    (It does not count time spent in the main or game menus.)
    """

    return renpy.game.contexts[0].runtime

@renpy_pure
def loadable(filename):
    """
    :doc: file

    Returns True if the given filename is loadable, meaning that it
    can be loaded from the disk or from inside an archive. Returns
    False if this is not the case.
    """

    return renpy.loader.loadable(filename)


@renpy_pure
def exists(filename):
    """
    :doc: file_rare

    Returns true if the given filename can be found in the
    searchpath. This only works if a physical file exists on disk. It
    won't find the file if it's inside of an archive.

    You almost certainly want to use :func:`renpy.loadable` in preference
    to this function.
    """

    try:
        renpy.loader.transfn(filename)
        return True
    except:
        return False


def restart_interaction():
    """
    :doc: other

    Restarts the current interaction. Among other things, this displays
    images added to the scene, re-evaluates screens, and starts any
    queued transitions.

    This only does anything when called from within an interaction (for
    example, from an action). Outside an interaction, this function has
    no effect.
    """

    try:
        renpy.game.interface.restart_interaction = True
    except:
        pass


def context():
    """
    :doc: context

    Returns an object that is unique to the current context. The object
    is copied when entering a new context, but changes to the copy do
    not change the original.

    The object is saved and participates in rollback.
    """

    return renpy.game.context().info


def context_nesting_level():
    """
    :doc: context

    Returns the nesting level of the current context. This is 0 for the
    outermost context (the context that is saved, loaded, and rolled-back),
    and is non-zero in other contexts, such as menu and replay contexts.
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
    :doc: debug

    Returns a pair giving the filename and line number of the current
    statement.
    """

    n = renpy.game.script.namemap.get(renpy.game.context().current, None)

    if n is None:
        return "unknown", 0
    else:
        return n.filename, n.linenumber


# A file that log logs to.
logfile = None

def log(msg):
    """
    :doc: debug

    If :var:`config.log` is not set, this does nothing. Otherwise, it opens
    the logfile (if not already open), formats the message to 70
    columns, and prints it to the logfile.
    """

    global logfile

    if not renpy.config.log:
        return

    if msg is None:
        return

    try:

        if not logfile:
            import codecs
            logfile = _file(renpy.config.log, "a")

            if not logfile.tell():
                logfile.write(codecs.BOM_UTF8)

        import textwrap

        print >>logfile, textwrap.fill(msg).encode("utf-8")
        logfile.flush()

    except:
        renpy.config.log = None


def force_full_redraw():
    """
    :doc: other

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


def dynamic(*vars): #@ReservedAssignment
    """
    :doc: other

    This can be given one or more variable names as arguments. This makes
    the variables dynamically scoped to the current call. The variables will
    be reset to their original value when the call returns.

    An example call is::

        $ renpy.dynamic("x", "y", "z")
    """

    renpy.game.context().make_dynamic(vars)


def context_dynamic(*vars): #@ReservedAssignment
    """
    :doc: other

    This can be given one or more variable names as arguments. This makes
    the variables dynamically scoped to the current context. The variables will
    be reset to their original value when the call returns.

    An example call is::

        $ renpy.context_dynamic("x", "y", "z")
    """

    renpy.game.context().make_dynamic(vars, context=True)


def seen_label(label):
    """
    :doc: label

    Returns true if the named label has executed at least once on the current user's
    system, and false otherwise. This can be used to unlock scene galleries, for
    example.
    """
    return label in renpy.game.persistent._seen_ever  # @UndefinedVariable


def seen_audio(filename):
    """
    :doc: audio

    Returns True if the given filename has been played at least once on the current
    user's system.
    """
    return filename in renpy.game.persistent._seen_audio  # @UndefinedVariable


def seen_image(name):
    """
    :doc: image_func

    Returns True if the named image has been seen at least once on the user's
    system. An image has been seen if it's been displayed using the show statement,
    scene statement, or :func:`renpy.show` function. (Note that there are cases
    where the user won't actually see the image, like a show immediately followed by
    a hide.)
    """
    if not isinstance(name, tuple):
        name = tuple(name.split())

    return name in renpy.game.persistent._seen_images  # @UndefinedVariable


def file(fn): #@ReservedAssignment
    """
    :doc: file

    Returns a read-only file-like object that accesses the file named `fn`. The file is
    accessed using Ren'Py's standard search method, and may reside in an RPA archive.
    or as an Android asset.

    The object supports a wide subset of the fields and methods found on python's
    standard file object, opened in binary mode. (Basically, all of the methods that
    are sensible for a read-only file.)
    """
    return renpy.loader.load(fn)


@renpy_pure
def image_size(im):
    """
    :doc: file_rare

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
    """
    :doc: se_images

    Returns the list of transforms being applied to the image with tag `name`
    on `layer`. Returns an empty list if no transofrms are being applied, or
    None if the image is not shown.
    """

    if isinstance(name, basestring):
        name = tuple(name.split())

    tag = name[0]

    return renpy.game.context().scene_lists.at_list[layer].get(tag, None)


def show_layer_at(at_list, layer='master'):
    """
    :doc: se_images

    The python equivalent of the ``show layer`` `layer` ``at`` `at_list`
    statement.
    """

    if not isinstance(at_list, list):
        at_list = [ at_list ]

    renpy.game.context().scene_lists.set_layer_at_list(layer, at_list)

layer_at_list = show_layer_at


def free_memory():
    """
    :doc: other

    Attempts to free some memory. Useful before running a renpygame-based
    minigame.
    """
    force_full_redraw()
    renpy.display.interface.kill_textures_and_surfaces()

@renpy_pure
def easy_displayable(d, none=False):
    """
    :undocumented:
    """

    if none:
        return renpy.easy.displayable(d)
    else:
        return renpy.easy.displayable_or_none(d)


def quit_event():
    """
    :doc: other

    Triggers a quit event, as if the player clicked the quit button in the
    window chrome.
    """

    renpy.game.interface.quit_event()


def iconify():
    """
    :doc: other

    Iconifies the game.
    """

    renpy.game.interface.iconify()

# New context stuff.
call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(renpy.game.call_in_new_context)
invoke_in_new_context = renpy.game.invoke_in_new_context
curried_invoke_in_new_context = renpy.curry.curry(renpy.game.invoke_in_new_context)
call_replay = renpy.game.call_replay

renpy_pure("curried_call_in_new_context")
renpy_pure("curried_invoke_in_new_context")


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
    """
    :doc: udd_utility

    Causes an event to be generated before `seconds` seconds have elapsed.
    This ensures that the event method of a user-defined displayable will be
    called.
    """

    renpy.game.interface.timeout(seconds)


def end_interaction(value):
    """
    :doc: udd_utility

    If `value` is not None, immediately ends the current interaction, causing
    the interaction to return `value`. If `value` is None, does nothing.

    This can be called from inside the render and event methods of a
    creator-defined displayable.
    """

    if value is None:
        return

    raise renpy.display.core.EndInteraction(value)


def scry():
    """
    :doc: other

    Returns the scry object for the current statement.

    The scry object tells Ren'Py about things that must be true in the
    future of the current statement. Right now, the scry object has one
    field:

    ``nvl_clear``
        Is true if an ``nvl clear`` statement will execute before the
        next interaction.
    """

    name = renpy.game.context().current
    node = renpy.game.script.lookup(name)
    return node.scry()

@renpy_pure
def munged_filename():
    return renpy.parser.munge_filename(get_filename_line()[0])


# Module loading stuff.

loaded_modules = set()

def load_module(name, **kwargs):
    """
    :doc: other

    This loads the Ren'Py module named name. A Ren'Py module consists of Ren'Py code
    that is loaded into the usual (store) namespace, contained in a file named
    name.rpym or name.rpymc. If a .rpym file exists, and is newer than the
    corresponding .rpymc file, it is loaded and a new .rpymc file is created.

    All init code in the module is run before this function returns. An error is
    raised if the module name cannot be found, or is ambiguous.

    Module loading may only occur from inside an init block.
    """

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


def load_string(s, filename="<string>"):
    """
    :doc: other

    Loads `s` as Ren'Py script that can be called.

    Returns the name of the first statement in s.

    `filename` is the name of the filename that statements in the string will
    appear to be from.
    """

    old_exception_info = renpy.game.exception_info

    try:

        old_locked = renpy.config.locked
        renpy.config.locked = False

        stmts, initcode = renpy.game.script.load_string(filename, unicode(s))

        if stmts is None:
            return None

        context = renpy.execution.Context(False)
        context.init_phase = True
        renpy.game.contexts.append(context)

        for prio, node in initcode: #@UnusedVariable
            renpy.game.context().run(node)

        context.pop_all_dynamic()
        renpy.game.contexts.pop()

        renpy.config.locked = old_locked

        renpy.game.script.analyze()

        return stmts[0].name

    finally:
        renpy.game.exception_info = old_exception_info


def pop_call():
    """
    :doc: other
    :name: renpy.pop_call

    Pops the current call from the call stack, without returning to
    the location.

    This can be used if a label that is called decides not to return
    to its caller.
    """

    renpy.game.context().pop_call()

pop_return = pop_call


def call_stack_depth():
    """
    :doc: other

    Returns the depth of the call stack of the current context - the number
    of calls that have run without being returned from or popped from the
    call stack.
    """

    return len(renpy.game.context().return_stack)


def game_menu(screen=None):
    """
    :undocumented: Probably not what we want in the presence of
    screens.
    """

    if screen is None:
        call_in_new_context("_game_menu")
    else:
        call_in_new_context("_game_menu", screen)


def shown_window():
    """
    :doc: other

    Call this to indicate that the window has been shown. This interacts
    with the "window show" statement, which shows an empty window whenever
    this functions has not been called during an interaction.
    """

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
    """
    :doc: image_func

    This gets the placement of displayable d. There's very little warranty on this
    information, as it might change when the displayable is rendered, and might not
    exist until the displayable is first rendered.

    This returns an object with the following fields, each corresponding to a style
    property:

        * xpos
        * xanchor
        * xoffset
        * ypos
        * yanchor
        * yoffset
        * subpixel
    """
    p = d.get_placement()

    return placement(p)


def get_image_bounds(tag, width=None, height=None, layer='master'):
    """
    :doc: image_func

    If an image with `tag` exists on `layer`, returns the bounding box of
    that image. Returns None if the image is not found.

    The bounding box is an (x, y, width, height) tuple. The components of
    the tuples are expressed in pixels, and may be floating point numbers.

    `width`, `height`
        The width and height of the area that contains the image. If None,
        defaults the width and height of the screen, respectively.
    """

    tag = tag.split()[0]

    if width is None:
        width = renpy.config.screen_width
    if height is None:
        height = renpy.config.screen_height

    return scene_lists().get_image_bounds(layer, tag, width, height)

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
    """
    :undocumented: Cache pin is deprecated.
    """

    new_pins = renpy.python.RevertableSet()

    for i in args:

        im = renpy.easy.displayable(i)

        if not isinstance(im, renpy.display.im.ImageBase):
            raise Exception("Cannot pin non-image-manipulator %r" % im)

        new_pins.add(im)

    renpy.store._cache_pin_set = new_pins | renpy.store._cache_pin_set



def cache_unpin(*args):
    """
    :undocumented: Cache pin is deprecated.
    """

    new_pins = renpy.python.RevertableSet()

    for i in args:

        im = renpy.easy.displayable(i)

        if not isinstance(im, renpy.display.im.ImageBase):
            raise Exception("Cannot unpin non-image-manipulator %r" % im)

        new_pins.add(im)

    renpy.store._cache_pin_set = renpy.store._cache_pin_set - new_pins


def start_predict(*args):
    """
    :doc: image_func

    This function takes one or more displayables as arguments. It causes
    Ren'Py to predict those displayables during every interaction until
    the displayables are removed by :func:`renpy.stop_predict`.
    """

    new_predict = renpy.python.RevertableSet(renpy.store._predict_set)

    for d in args:
        d = renpy.easy.displayable(d)
        new_predict.add(d)

    renpy.store._predict_set = new_predict


def stop_predict(*args):
    """
    :doc: image_func

    This function takes one or more displayables as arguments. It causes
    Ren'Py to stop predicting those displayables during every interaction.
    """

    new_predict = renpy.python.RevertableSet(renpy.store._predict_set)

    for d in args:
        d = renpy.easy.displayable(d)
        new_predict.discard(d)

    renpy.store._predict_set = new_predict


def start_predict_screen(_screen_name, *args, **kwargs):

    """
    :doc: screens

    Causes Ren'Py to start predicting the screen named `_screen_name`
    will be shown with the given arguments. This replaces  any previous prediction
    of `_screen_name`. To stop predicting a screen, call :func:`renpy.stop_predict_screen`.
    """

    new_predict = renpy.python.RevertableDict(renpy.store._predict_screen)
    new_predict[_screen_name] = (args, kwargs)
    renpy.store._predict_screen = new_predict


def stop_predict_screen(name):
    """
    :doc: screens

    Causes Ren'Py to stop predicting the screen named `name` will be shown.
    """

    new_predict = renpy.python.RevertableDict(renpy.store._predict_screen)
    new_predict.pop(name, None)
    renpy.store._predict_screen = new_predict


def call_screen(_screen_name, *args, **kwargs):
    """
    :doc: screens

    The programmatic equivalent of the show screen statement.

    This shows `_screen_name` as a screen, then causes an interaction
    to occur. The screen is hidden at the end of the interaction, and
    the result of the interaction is returned.

    Keyword arguments not beginning with _ are passed to the scope of
    the screen.

    If the keyword argument `_with_none` is false, "with None" is not
    run at the end of end of the interaction.
    """

    renpy.exports.mode('screen')

    show_screen(_screen_name, _transient=True, *args, **kwargs)

    roll_forward = renpy.exports.roll_forward_info()

    try:
        rv = renpy.ui.interact(mouse="screen", type="screen", roll_forward=roll_forward)
    except (renpy.game.JumpException, renpy.game.CallException), e:
        rv = e

    renpy.exports.checkpoint(rv)

    with_none = renpy.config.implicit_with_none

    if "_with_none" in kwargs:
        with_none = kwargs.pop("_with_none")

    if with_none:
        renpy.game.interface.do_with(None, None)

    if isinstance(rv, (renpy.game.JumpException, renpy.game.CallException)):
        raise rv

    return rv

@renpy_pure
def list_files(common=False):
    """
    :doc: file

    Lists the files in the game directory and archive files. Returns
    a list of files, with / as the directory separator.

    `common`
        If true, files in the common directory are included in the
        listing.
    """

    rv = [ ]

    for dir, fn in renpy.loader.listdirfiles(common): #@ReservedAssignment
        if fn.startswith("saves/"):
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

    ``"resizable"``
        True if and only if the window is resizable.

    ``"additive"``
        True if and only if the renderer supports additive blending.

    Other, renderer-specific, keys may also exist. The dictionary should
    be treated as immutable. This should only be called once the display
    has been started (that is, after the init code is finished).
    """

    return renpy.display.draw.info


def display_reset():
    """
    :undocumented: Used internally.

    Causes the display to be restarted at the start of the next interaction.
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

def get_mode():
    """
    :doc: modes

    Returns the current mode, or None if it is not defined.
    """

    ctx = renpy.game.context()

    if not ctx.use_modes:
        return None

    modes = ctx.modes

    return modes[0]

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


@renpy_pure
def variant(name):
    """
    :doc: screens

    Returns true if a `name` is a screen variant that can be chosen
    by Ren'Py. See :ref:`screen-variants` for more details. This function
    can be used as the condition in a python if statement to set up the
    appropriate styles for the selected screen variant.

    `name` can also be a list of variants, in which case this function
    returns True if any of the variants is selected.
    """

    if isinstance(name, basestring):
        return name in renpy.config.variants
    else:
        for n in name:
            if n in renpy.config.variants:
                return True

        return False


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


def get_say_attributes():
    """
    :doc: other

    Gets the attributes associated with the current say statement, or
    None if no attributes are associated with this statement.

    This is only valid when executing or predicting a say statement.
    """

    return renpy.game.context().say_attributes


def get_side_image(prefix_tag, image_tag=None, not_showing=True, layer='master'):
    """
    :doc: other

    This attempts to find an image to show as the side image.

    It begins by determining a set of image attributes. If `image_tag` is
    given, it gets the image attributes from the tag. Otherwise, it gets
    them from the currently showing character.

    It then looks up an image with the tag `prefix_tag` and those attributes,
    and returns it if it exists.

    If not_showing is True, this only returns a side image if the image the
    attributes are taken from is not on the screen.
    """

    images = renpy.game.context().images

    if image_tag is not None:
        attrs = (image_tag,) + images.get_attributes(layer, image_tag)
    else:
        attrs = renpy.store._side_image_attributes

    if not attrs:
        return None

    if not_showing and images.showing(layer, (attrs[0], )):
        return None

    required = set()
    optional = set(attrs)

    return images.choose_image(prefix_tag, required, optional, None)


def get_physical_size():
    """
    :doc: other

    Returns the size of the physical window.
    """

    return renpy.display.draw.get_physical_size()


def set_physical_size(size):
    """
    :doc: other

    Attempts to set the size of the physical window to `size`. This has the
    side effect of taking the screen out of fullscreen mode.
    """

    renpy.game.preferences.fullscreen = False

    if get_renderer_info()["resizable"]:
        renpy.display.draw.quit()
        renpy.display.interface.set_mode(size)

def reset_physical_size():
    """
    :doc: other

    Attempts to set the size of the physical window to the specified values
    in renpy.config. (That is, screen_width and screen_height.) This has the
    side effect of taking the screen out of fullscreen mode.
    """

    renpy.game.preferences.fullscreen = False

    if get_renderer_info()["resizable"]:
        renpy.display.draw.quit()
        renpy.display.interface.set_mode((renpy.config.screen_width, renpy.config.screen_height))


@renpy_pure
def fsencode(s):
    """
    :doc: file_rare
    :name: renpy.fsencode

    Converts s from unicode to the filesystem encoding.
    """

    if not isinstance(s, unicode):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.encode(fsencoding, "replace")


@renpy_pure
def fsdecode(s):
    """
    :doc: file_rare
    :name: renpy.fsdecode

    Converts s from filesystem encoding to unicode.
    """

    if not isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.decode(fsencoding)


from renpy.editor import launch_editor #@UnusedImport


def get_image_load_log(age=None):
    """
    :doc: other

    A generator that yields a log of image loading activity. For the last 100
    image loads, this returns:

    * The time the image was loaded (in seconds since the epoch).
    * The filename of the image that was loaded.
    * A boolean that is true if the image was preloaded, and false if the
      game stalled to load it.

    The entries are ordered from newest to oldest.

    `age`
        If not None, only images that have been loaded in the past `age`
        seconds are included.

    The image load log is only kept if config.developer = True.
    """

    if age is not None:
        deadline = time.time() - age
    else:
        deadline = 0


    for i in renpy.display.im.cache.load_log:
        if i[0] < deadline:
            break

        yield i


def end_replay():
    """
    :doc: replay

    If we're in a replay, ends the replay immediately. Otherwise, does
    nothing.
    """

    if renpy.store._in_replay:
        raise renpy.game.EndReplay()


def save_persistent():
    """
    :doc: persistent

    Saves the persistent data to disk.
    """

    renpy.persistent.update(True)


def is_seen(ever=True):
    """
    :doc: other

    Returns true if the current line has been seen by the player.

    If `ever` is true, we check to see if the line has ever been seen by the
    player. If false, we check if the line has been seen in the current
    play-through.
    """

    return renpy.game.context().seen_current(ever)


def get_mouse_pos():
    """
    :doc: other

    Returns an (x, y) tuple giving the location of the mouse pointer or the
    current touch location. If the device does not support a mouse and is not
    currently being touched, x and y are numbers, but not meaningful.
    """
    return renpy.display.draw.get_mouse_pos()


def set_mouse_pos(x, y, duration=0):
    """
    :doc: other

    Jump the mouse pointer to the location given by arguments x and y.
    If the device does not have a mouse pointer, this does nothing.

    `duration`
        The time it will take to perform the move, in seconds.
        During this time, the mouse may be unresponsive.
    """

    renpy.display.interface.set_mouse_pos(x, y, duration)


def set_autoreload(autoreload):
    """
    :doc: other

    Sets the autoreload flag, which determines if the game will be
    automatically reloaded after file changes. Autoreload will not be
    fully enabled until the game is reloaded with :func:`renpy.utter_restart`.
    """

    renpy.autoreload = autoreload


def get_autoreload():
    """
    :doc: other

    Gets the autoreload flag.
    """

    return renpy.autoreload


def count_dialogue_blocks():
    """
    :doc: other

    Returns the number of dialogue blocks in the game's original language.
    """

    return renpy.game.script.translator.count_translates()


def count_seen_dialogue_blocks():
    """
    :doc: other

    Returns the number of dialogue blocks the user has seen in any play-through
    of the current game.

    This number may be larger than the result of :func:`renpy.count_dialogue_blocks`
    when the script has changed and older dialogue blocks are no longer accessible.
    """

    return len(renpy.game.persistent._seen_translates) # @UndefinedVariable


def substitute(s, scope=None, translate=True):
    """
    :doc: other

    Applies translation and new-style formatting to the string `s`.

    `scope`
        If not None, a scope which is used in formatting, in addition to the
        default store.

    `translate`
        Determines if translation occurs.

    Returns the translated and formatted string.
    """

    return renpy.substitutions.substitute(s, scope=scope, translate=translate)[0]


def munge(name, filename=None):
    """
    :doc: other

    Munges `name`, which must begin with __.

    `filename`
        The filename the name is munged into. If None, the name is munged
        into the filename containing the call to this function.
    """

    if filename is None:
        filename = sys._getframe(1).f_code.co_filename

    if not name.startswith("__"):
        return name

    if name.endswith("__"):
        return name

    return renpy.parser.munge_filename(filename) + name[2:]


def get_return_stack():
    """
    :doc: label

    Returns a list giving the current return stack. The return stack is a
    list of statement names.

    The statement names will be strings (for labels), or opaque tuples (for
    non-label statements).
    """

    return renpy.game.context().get_return_stack()

def set_return_stack(stack):
    """
    :doc: label

    Sets the current return stack. The return stack is a list of statement
    names.

    Statement names may be strings (for labels) or opaque tuples (for
    non-label statements).
    """

    renpy.game.context().set_return_stack(stack)

def invoke_in_thread(fn, *args, **kwargs):
    """
    :doc: other

    Invokes the function `fn` in a background thread, passing it the
    provided arguments and keyword arguments. Restarts the interaction
    once the thread returns.

    This function creates a daemon thread, which will be automatically
    stopped when Ren'Py is shutting down.
    """

    def run():
        try:
            fn(*args, **kwargs)
        except:
            import traceback
            traceback.print_exc()

        restart_interaction()

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

def cancel_gesture():
    """
    :doc: gesture

    Cancels the current gesture, preventing the gesture from being recognized.
    This should be called by displayables that have gesture-like behavior.
    """

    renpy.display.gesture.recognizer.cancel() # @UndefinedVariable

def execute_default_statement(start=False):
    """
    :undocumented:

    Executes the default statement.
    """

    for i in renpy.ast.default_statements:
        i.set_default(start)

def write_log(s, *args):
    """
    :undocumented:

    Writes to log.txt.
    """

    renpy.display.log.write(s, *args)

def predicting():
    """
    :doc: screens

    Returns true if Ren'Py is currently predicting the screen.
    """

    return renpy.display.predict.predicting
