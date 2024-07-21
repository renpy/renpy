# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains functions that are exported to the script namespace as
# the renpy namespace. (So renpy.say, renpy.pause, and so on.)

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import gc
import io
import re
import time
import sys
import threading
import fnmatch
import os

if PY2:
    from urllib import urlencode as _urlencode
else:
    from urllib.parse import urlencode as _urlencode

import renpy

from renpy.pyanalysis import const, pure, not_const

try:
    import emscripten
except ImportError:
    pass

import pygame_sdl2

from renpy.exports.commonexports import renpy_pure

from renpy.text.extras import ParameterizedText, filter_text_tags
from renpy.text.font import register_sfont, register_mudgefont, register_bmfont
from renpy.text.text import language_tailor, BASELINE
from renpy.display.behavior import Keymap
from renpy.display.behavior import run, run as run_action, run_unhovered, run_periodic
from renpy.display.behavior import map_event, queue_event, clear_keymap_cache
from renpy.display.behavior import is_selected, is_sensitive

from renpy.display.minigame import Minigame
from renpy.display.screen import define_screen, show_screen, hide_screen, use_screen, current_screen
from renpy.display.screen import has_screen, get_screen, get_displayable, get_widget, ScreenProfile as profile_screen
from renpy.display.screen import get_displayable_properties, get_widget_properties
from renpy.display.screen import get_screen_variable, set_screen_variable

from renpy.display.focus import focus_coordinates, capture_focus, clear_capture_focus, get_focus_rect
from renpy.display.predict import screen as predict_screen

from renpy.display.image import image_exists, image_exists as has_image, list_images
from renpy.display.image import get_available_image_tags, get_available_image_attributes, check_image_attributes, get_ordered_image_attributes
from renpy.display.image import get_registered_image

from renpy.display.im import load_surface, load_image, load_rgba

from renpy.display.tts import speak as alt, speak_extra_alt

from renpy.curry import curry, partial
from renpy.display.video import movie_start_fullscreen, movie_start_displayable, movie_stop

from renpy.loadsave import load, save, list_saved_games, can_load, rename_save, copy_save, unlink_save, scan_saved_game
from renpy.loadsave import list_slots, newest_slot, slot_mtime, slot_json, slot_screenshot, force_autosave

from renpy.savetoken import get_save_token_keys

from renpy.python import py_eval as eval
from renpy.rollback import rng as random
from renpy.atl import atl_warper
from renpy.easy import predict, displayable, split_properties
from renpy.lexer import unelide_filename
from renpy.parser import get_parse_errors

from renpy.translation import change_language, known_languages, translate_string, get_translation_identifier, get_translation_info
from renpy.translation.generation import generic_filter as transform_text

from renpy.persistent import register_persistent

from renpy.character import show_display_say, predict_show_display_say, display_say

import renpy.audio.sound as sound
import renpy.audio.music as music

from renpy.statements import register as register_statement
from renpy.text.extras import check_text_tags

from renpy.memory import profile_memory, diff_memory, profile_rollback

from renpy.text.font import variable_font_info
from renpy.text.textsupport import TAG as TEXT_TAG, TEXT as TEXT_TEXT, PARAGRAPH as TEXT_PARAGRAPH, DISPLAYABLE as TEXT_DISPLAYABLE
from renpy.text.shader import TextShader, register_textshader

from renpy.execution import not_infinite_loop, reset_all_contexts

from renpy.sl2.slparser import CustomParser as register_sl_statement, register_sl_displayable

from renpy.ast import eval_who

from renpy.loader import add_python_directory

from renpy.lint import try_compile, try_eval

from renpy.gl2.gl2shadercache import register_shader
from renpy.gl2.live2d import has_live2d

from renpy.bootstrap import get_alternate_base

from renpy.ui import Choice

renpy_pure("ParameterizedText")
renpy_pure("Keymap")
renpy_pure("has_screen")
renpy_pure("image_exists")
renpy_pure("curry")
renpy_pure("partial")
renpy_pure("unelide_filename")
renpy_pure("known_languages")
renpy_pure("check_text_tags")
renpy_pure("filter_text_tags")
renpy_pure("split_properties")


# The number of bits in the architecture.
if sys.maxsize > (2 << 32):
    bits = 64
else:
    bits = 32


from renpy.exports.commonexports import (
    renpy_pure,
)

from renpy.exports.rollbackexports import (
    roll_forward_info,
    roll_forward_core,
    in_rollback,
    can_rollback,
    in_fixed_rollback,
    checkpoint,
    block_rollback,
    suspend_rollback,
    fix_rollback,
    retain_after_load,
    rollback,
    get_roll_forward,
)


from renpy.exports.displayexports import (
    scene_lists,
    count_displayables_in_layer,
    image,
    copy_images,
    default_layer,
    can_show,
    showing,
    get_showing_tags,
    get_hidden_tags,
    get_attributes,
    clear_attributes,
    _find_image,
    predict_show,
    set_tag_attributes,
    show,
    hide,
    scene,
    toggle_fullscreen,
    take_screenshot,
    screenshot,
    screenshot_to_bytes,
    transition,
    get_transition,
    get_ongoing_transition,
    restart_interaction,
    force_full_redraw,
    image_size,
    get_at_list,
    show_layer_at,
    layer_at_list,
    free_memory,
    easy_displayable,
    quit_event,
    iconify,
    timeout,
    end_interaction,
    shown_window,
    placement,
    get_placement,
    get_image_bounds,
    Render,
    render,
    IgnoreEvent,
    redraw,
    is_pixel_opaque,
    Displayable,
    Container,
    get_renderer_info,
    display_reset,
    flush_cache_file,
)


from renpy.exports.inputexports import (
    web_input,
    input,
)


from renpy.exports.fetchexports import (
    FetchError,
    fetch_pause,
    fetch_requests,
    fetch_emscripten,
    fetch,
    proxies
)


# The arguments and keyword arguments for the current menu call.
menu_args = None
menu_kwargs = None


from renpy.exports.menuexports import (
    get_menu_args,
    menu,
    choice_for_skipping,
    predict_menu,
    MenuEntry,
    display_menu,
)


from renpy.exports.sayexports import (
    TagQuotingDict,
    tag_quoting_dict,
    predict_say,
    scry_say,
    say,
    do_reshow_say,
    curried_do_reshow_say,
    get_reshow_say,
    reshow_say,
    get_say_attributes,
    get_side_image,
)


from renpy.exports.statementexports import (
    imagemap,
    pause,
    with_statement,
    jump,
    call,
    return_statement,
    call_screen,
)

globals()["with"] = with_statement


from renpy.exports.mediaexports import (
    movie_cutscene,
    toggle_music,
    music_start,
    music_stop,
)


from renpy.exports.scriptexports import (
    has_label,
    get_all_labels,
    munged_filename,
    load_module,
    load_string,
    load_language,
    include_module,
)


from renpy.exports.restartexports import (
    full_restart,
    utter_restart,
    reload_script,
    quit,
)


from renpy.exports.debugexports import (
    warp_to_line,
    get_filename_line,
    log,
    push_error_handler,
    pop_error_handler,
    error,
)


from renpy.exports.loaderexports import (
    loadable,
    exists,
    open_file,
    file,
    notl_file,
    list_files,
)


from renpy.exports.loadsaveexports import (
    clear_game_runtime,
    get_game_runtime
)


from renpy.exports.contextexports import (
    context,
    context_nesting_level,
    jump_out_of_context,
    current_interact_type,
    last_interact_type,
    dynamic,
    context_dynamic,
    call_in_new_context,
    curried_call_in_new_context,
    invoke_in_new_context,
    curried_invoke_in_new_context,
    call_replay,
    scry,
    pop_call,
    pop_return,
    call_stack_depth,
    game_menu,
    mode,
    get_mode,
)

from renpy.exports.persistentexports import (
    seen_label,
    mark_label_seen,
    mark_label_unseen,
    seen_audio,
    mark_audio_seen,
    mark_audio_unseen,
    seen_image,
    mark_image_seen,
    mark_image_unseen,
)

from renpy.exports.predictexports import (
    cache_pin,
    cache_unpin,
    expand_predict,
    start_predict,
    stop_predict,
    start_predict_screen,
    stop_predict_screen,
)

from renpy.exports.actionexports import (
    notify,
    display_notify,
)

from renpy.exports.platformexports import (
    variant,
    vibrate,
)

@renpy_pure
def version(tuple=False): # @ReservedAssignment
    """
    :doc: renpy_version

    If `tuple` is false, returns a string containing "Ren'Py ", followed by
    the current version of Ren'Py.

    If `tuple` is true, returns a tuple giving each component of the
    version as an integer.
    """

    if tuple:
        return renpy.version_tuple

    return renpy.version


version_string = renpy.version
version_only = renpy.version_only
version_name = renpy.version_name
version_tuple = renpy.version_tuple
license = "" # @ReservedAssignment

try:
    import platform as _platform
    platform = "-".join(_platform.platform().split("-")[:2])
except Exception:
    if renpy.android:
        platform = "Android"
    elif renpy.ios:
        platform = "iOS"
    else:
        platform = "Unknown"




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

    width = int(size[0])
    height = int(size[1])

    renpy.game.preferences.fullscreen = False # type: ignore

    if get_renderer_info()["resizable"]:

        renpy.game.preferences.physical_size = (width, height) # type: ignore

        if renpy.display.draw is not None:
            renpy.display.draw.resize()


def reset_physical_size():
    """
    :doc: other

    Attempts to set the size of the physical window to the size specified
    using :var:`renpy.config.physical_height` and :var:`renpy.config.physical_width`,
    or the size set using :var:`renpy.config.screen_width` and :var:`renpy.config.screen_height`
    if not set.
    """

    set_physical_size((renpy.config.physical_width or renpy.config.screen_width, renpy.config.physical_height or renpy.config.screen_height))


@renpy_pure
def fsencode(s, force=False): # type: (str, bool) -> str
    """
    :doc: file_rare
    :name: renpy.fsencode

    Converts s from unicode to the filesystem encoding.
    """

    if (not PY2) and (not force):
        return s

    if not isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.encode(fsencoding) # type: ignore


@renpy_pure
def fsdecode(s): # type: (bytes|str) -> str
    """
    :doc: file_rare
    :name: renpy.fsdecode

    Converts s from filesystem encoding to unicode.
    """

    if isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.decode(fsencoding)


from renpy.editor import launch_editor # @UnusedImport


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
    :doc: reload

    Sets the autoreload flag, which determines if the game will be
    automatically reloaded after file changes. Autoreload will not be
    fully enabled until the game is reloaded with :func:`renpy.reload_script`.
    """

    renpy.autoreload = autoreload


def get_autoreload():
    """
    :doc: reload

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
    """

    return renpy.game.seen_translates_count


def count_newly_seen_dialogue_blocks():
    """
    :doc: other

    Returns the number of dialogue blocks the user has seen for the first time
    during this session.
    """

    return renpy.game.new_translates_count


def substitute(s, scope=None, translate=True):
    """
    :doc: text_utility

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

    if not name.startswith("__"):
        return name

    if name.endswith("__"):
        return name

    if filename is None:
        filename = sys._getframe(1).f_code.co_filename

    return renpy.lexer.munge_filename(filename) + name[2:]


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

    The most common use of this is to use::

        renpy.set_return_stack([])

    to clear the return stack.
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

    This thread is very limited in what it can do with the Ren'Py API.
    Changing store variables is allowed, as are calling calling the following
    functions:

    * :func:`renpy.restart_interaction`
    * :func:`renpy.invoke_in_main_thread`
    * :func:`renpy.queue_event`

    Most other portions of the Ren'Py API are expected to be called from
    the main thread.

    This does not work on the web platform, except for immediately returning
    without an error.
    """

    if renpy.emscripten:
        return

    def run():
        try:
            fn(*args, **kwargs)
        except Exception:
            import traceback
            traceback.print_exc()

        restart_interaction()

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()


def invoke_in_main_thread(fn, *args, **kwargs):
    """
    :doc: other

    This runs the given function with the given arguments in the main
    thread. The function runs in an interaction context similar to an
    event handler. This is meant to be called from a separate thread,
    whose creation is handled by :func:`renpy.invoke_in_thread`.

    If a single thread schedules multiple functions to be invoked, it is guaranteed
    that they will be run in the order in which they have been scheduled::

        def ran_in_a_thread():
            renpy.invoke_in_main_thread(a)
            renpy.invoke_in_main_thread(b)

    In this example, it is guaranteed that ``a`` will return before
    ``b`` is called. The order of calls made from different threads is not
    guaranteed.

    This may not be called during the init phase.
    """

    if renpy.game.context().init_phase:
        raise Exception("invoke_in_main_thread may not be called during the init phase.")

    renpy.display.interface.invoke_queue.append((fn, args, kwargs))


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

    `start`
        This is true at the start of the game, and false at other
        times.
    """

    for i in renpy.ast.default_statements:
        i.execute_default(start)

    for i in renpy.config.after_default_callbacks:
        i()

def write_log(s, *args):
    """
    :undocumented:

    Writes to log.txt.
    """

    renpy.display.log.write(s, *args)


def predicting():
    """
    :doc: other

    Returns true if Ren'Py is currently in a predicting phase.
    """

    return renpy.display.predict.predicting


def get_line_log():
    """
    :undocumented:

    Returns the list of lines that have been shown since the last time
    :func:`renpy.clear_line_log` was called.
    """

    return renpy.game.context().line_log[:]


def clear_line_log():
    """
    :undocumented:

    Clears the line log.
    """

    renpy.game.context().line_log = [ ]


def add_layer(layer, above=None, below=None, menu_clear=True, sticky=None):
    """
    :doc: image_func

    Adds a new layer to the screen. If the layer already exists, this
    function does nothing.

    One of `behind` or `above` must be given.

    `layer`
        A string giving the name of the new layer to add.

    `above`
        If not None, a string giving the name of a layer the new layer will
        be placed above.

    `below`
        If not None, a string giving the name of a layer the new layer will
        be placed below.

    `menu_clear`
        If true, this layer will be cleared when entering the game menu
        context, and restored when leaving it.

    `sticky`
        If true, any tags added to this layer will have it become their
        default layer until they are hidden. If None, this layer will be
        sticky only if other sticky layers already exist.
    """

    layers = renpy.config.layers

    if layer in renpy.config.layers:
        return

    if (above is not None) and (below is not None):
        raise Exception("The above and below arguments to renpy.add_layer are mutually exclusive.")

    elif above is not None:
        try:
            index = layers.index(above) + 1
        except ValueError:
            raise Exception("Layer '%s' does not exist." % above)

    elif below is not None:
        try:
            index = layers.index(below)
        except ValueError:
            raise Exception("Layer '%s' does not exist." % below)

    else:
        raise Exception("The renpy.add_layer function requires either the above or below argument.")

    layers.insert(index, layer)

    if menu_clear:
        renpy.config.menu_clear_layers.append(layer) # type: ignore # Set in 00gamemenu.rpy.

    if sticky or sticky is None and renpy.config.sticky_layers:
        renpy.config.sticky_layers.append(layer)


def maximum_framerate(t):
    """
    :doc: other

    Forces Ren'Py to draw the screen at the maximum framerate for `t` seconds.
    If `t` is None, cancels the maximum framerate request.
    """

    if renpy.display.interface is not None:
        renpy.display.interface.maximum_framerate(t)
    else:
        if t is None:
            renpy.display.core.initial_maximum_framerate = 0
        else:
            renpy.display.core.initial_maximum_framerate = max(renpy.display.core.initial_maximum_framerate, t)


def is_start_interact():
    """
    :doc: other

    Returns true if restart_interaction has not been called during the current
    interaction. This can be used to determine if the interaction is just being
    started, or has been restarted.
    """

    return renpy.display.interface.start_interact


def play(filename, channel=None, **kwargs):
    """
    :doc: audio

    Plays a sound effect. If `channel` is None, it defaults to
    :var:`config.play_channel`. This is used to play sounds defined in
    styles, :propref:`hover_sound` and :propref:`activate_sound`.
    """

    if filename is None:
        return

    if channel is None:
        channel = renpy.config.play_channel

    renpy.audio.music.play(filename, channel=channel, loop=False, **kwargs)


def get_editable_input_value():
    """
    :undocumented:

    Returns the current input value, and a flag that is true if it is editable.
    and false otherwise.
    """

    return renpy.display.behavior.current_input_value, renpy.display.behavior.input_value_active


def set_editable_input_value(input_value, editable):
    """
    :undocumented:

    Sets the currently active input value, and if it should be marked as
    editable.
    """

    renpy.display.behavior.current_input_value = input_value
    renpy.display.behavior.input_value_active = editable


def get_refresh_rate(precision=5):
    """
    :doc: other

    Returns the refresh rate of the current screen, as a floating-point
    number of frames per second.

    `precision`
        The raw data Ren'Py gets is the number of frames per second rounded down
        to the nearest integer. This means that a monitor that runs at 59.95
        frames per second will be reported at 59 fps. The precision argument
        then further reduces the precision of this reading, such that the only valid
        readings are multiples of the precision.

        Since all monitor framerates tend to be multiples of 5 (25, 30, 60,
        75, and 120), this likely will improve accuracy. Setting precision
        to 1 disables this.
    """

    if PY2:
        precision = float(precision)

    info = renpy.display.get_info()
    rv = info.refresh_rate # type: ignore
    rv = round(rv / precision) * precision

    return rv


def get_identifier_checkpoints(identifier):
    """
    :doc: rollback

    Given a rollback_identifier from a HistoryEntry object, returns the number
    of checkpoints that need to be passed to :func:`renpy.rollback` to reach
    that identifier. Returns None of the identifier is not in the rollback
    history.
    """

    return renpy.game.log.get_identifier_checkpoints(identifier)


def get_adjustment(bar_value):
    """
    :doc: screens

    Given `bar_value`, a :class:`BarValue`, returns the :func:`ui.adjustment`
    it uses. The adjustment has the following attributes defined:

    .. attribute:: value

        The current value of the bar.

    .. attribute:: range

        The current range of the bar.
    """

    return bar_value.get_adjustment()


def get_skipping():
    """
    :doc: other

    Returns "slow" if the Ren'Py is skipping, "fast" if Ren'Py is fast skipping,
    and None if it is not skipping.
    """

    return renpy.config.skipping


def get_texture_size():
    """
    :undocumented:

    Returns the number of bytes of memory locked up in OpenGL textures and the
    number of textures that are defined.
    """

    return renpy.display.draw.get_texture_size()


old_battery = False


def get_on_battery():
    """
    :doc: other

    Returns True if Ren'Py is running on a device that is powered by an internal
    battery, or False if the device is being charged by some external source.
    """

    global old_battery

    pi = pygame_sdl2.power.get_power_info() # @UndefinedVariable

    if pi.state == pygame_sdl2.POWERSTATE_UNKNOWN: # @UndefinedVariable
        return old_battery
    elif pi.state == pygame_sdl2.POWERSTATE_ON_BATTERY: # @UndefinedVariable
        old_battery = True
        return True
    else:
        old_battery = False
        return False


def get_say_image_tag():
    """
    :doc: image_func

    Returns the tag corresponding to the currently speaking character (the
    `image` argument given to that character). Returns None if no character
    is speaking or the current speaking character does not have a corresponding
    image tag.
    """

    if renpy.store._side_image_attributes is None:
        return None

    return renpy.store._side_image_attributes[0]


class LastSay():
    """
    :undocumented:
    Object containing info about the last dialogue line.
    Returned by the last_say function.
    """

    def __init__(self, who, what, args, kwargs):
        self._who = who
        self.what = what
        self.args = args
        self.kwargs = kwargs

    @property
    def who(self):
        return eval_who(self._who)

def last_say():
    """
    :doc: other

    Returns an object containing information about the last say statement.

    While this can be called during a say statement, if the say statement is using
    a normal Character, the information will be about the *current* say statement,
    instead of the preceding one.

    `who`
        The speaker. This is usually a :func:`Character` object, but this
        is not required.

    `what`
        A string with the dialogue spoken. This may be None if dialogue
        hasn't been shown yet, for example at the start of the game.

    `args`
        A tuple of arguments passed to the last say statement.

    `kwargs`
        A dictionary of keyword arguments passed to the last say statement.

    .. warning::

        Like other similar functions, the object this returns is meant to be used
        in the short term after the function is called. Including it in save data
        or making it participate in rollback is not advised.
    """

    return LastSay(
        who = renpy.store._last_say_who,
        what = renpy.store._last_say_what,
        args = renpy.store._last_say_args,
        kwargs = renpy.store._last_say_kwargs,
    )

def is_skipping():
    """
    :doc: other

    Returns True if Ren'Py is currently skipping (in fast or slow skip mode),
    or False otherwise.
    """

    return not not renpy.config.skipping


def is_init_phase():
    """
    :doc: other

    Returns True if Ren'Py is currently executing init code, or False otherwise.
    """

    return renpy.game.context().init_phase


def add_to_all_stores(name, value):
    """
    :doc: other

    Adds the `value` by the `name` to all creator defined namespaces. If the name
    already exist in that namespace - do nothing for it.

    This function may only be run from inside an init block. It is an
    error to run this function once the game has started.
    """

    if not is_init_phase():
        raise Exception("add_to_all_stores is only allowed in init code.")

    for _k, ns in renpy.python.store_dicts.items():

        if name not in ns:
            ns[name] = value


def get_zorder_list(layer):
    """
    :doc: image_func

    Returns a list of (tag, zorder) pairs for `layer`.
    """

    return scene_lists().get_zorder_list(layer)


def change_zorder(layer, tag, zorder):
    """
    :doc: image_func

    Changes the zorder of `tag` on `layer` to `zorder`.
    """

    return scene_lists().change_zorder(layer, tag, zorder)


sdl_dll = False


def get_sdl_dll():
    """
    :doc: sdl

    Returns a ctypes.cdll object that refers to the library that contains
    the instance of SDL2 that Ren'Py is using. If this fails, None is returned.
    """

    global sdl_dll

    if sdl_dll is not False:
        return sdl_dll

    try:

        lib = os.path.dirname(sys.executable) + "/"

        DLLS = [ None, lib + "librenpython.dll", lib + "librenpython.dylib", lib + "librenpython.so", "librenpython.so", "SDL2.dll", "libSDL2.dylib", "libSDL2-2.0.so.0" ]

        import ctypes

        for i in DLLS:
            try:
                # Look for the DLL.
                dll = ctypes.cdll[i]
                # See if it has SDL_GetError..
                dll.SDL_GetError
            except Exception as e:
                continue

            sdl_dll = dll
            return dll

    except Exception:
        pass

    sdl_dll = None
    return None


def get_sdl_window_pointer():
    """
    :doc: sdl

    :rtype: ctypes.c_void_p | None

    Returns a pointer to the main window, or None if the main window is not
    displayed (or some other problem occurs).
    """

    try:
        window = pygame_sdl2.display.get_window()

        if window is None:
            return None

        return window.get_sdl_window_pointer()

    except Exception:
        return None


def is_mouse_visible():
    """
    :doc: other

    Returns True if the mouse cursor is visible, False otherwise.
    """

    if not renpy.display.interface:
        return True

    if not renpy.display.interface.mouse_focused:
        return False

    return renpy.display.interface.is_mouse_visible()


def get_mouse_name(interaction=False):
    """
    :doc: other

    Returns the name of the mouse that should be shown.


    `interaction`
        If true, get a mouse name that is based on the type of interaction
        occuring. (This is rarely useful.)
    """

    if not renpy.display.interface:
        return 'default'

    return renpy.display.interface.get_mouse_name(interaction=interaction)


def set_focus(screen, id, layer="screens"): # @ReservedAssignment
    """
    :doc: screens

    This attempts to focus the displayable with `id` in the screen `screen`.
    Focusing will fail if the displayable isn't found, the window isn't
    focused, or something else is grabbing focus.

    The focus may change if the mouse moves, even slightly, after this call
    is processed.
    """

    renpy.display.focus.override = (screen, id, layer)
    renpy.display.interface.last_event = None
    restart_interaction()


def check_permission(permission):
    """
    :doc: android_permission

    Checks to see if an Android permission has been granted to this application.

    `permission`
        A string giving the name of the permission, for example, "android.permission.WRITE_EXTERNAL_STORAGE".

    Returns true if the permission has been granted, false if it has not or if called on
    a non-Android platform.
    """

    if not renpy.android:
        return False

    from jnius import autoclass
    PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
    activity = PythonSDLActivity.mActivity

    try:
        return activity.checkSelfPermission(permission) == 0 # PackageManager.PERMISSION_GRANTED
    except Exception:
        return False


def request_permission(permission):
    """
    :doc: android_permission

    Asks Android to grant a permission to this application. The user may be
    prompted to grant the permission.

    `permission`
        A string giving the name of the permission, for example, "android.permission.WRITE_EXTERNAL_STORAGE".

    Returns true if the permission has been granted, false if not or if called on a
    non-Android platform.
    """

    if not renpy.android:
        return False

    return get_sdl_dll().SDL_AndroidRequestPermission(permission.encode("utf-8")) # type: ignore


def clear_retain(layer="screens", prefix="_retain"):
    """
    :doc: other

    Clears all retained screens
    """

    for i in get_showing_tags(layer):
        if i.startswith(prefix):
            hide_screen(i)


def confirm(message):
    """
    :doc: other

    This causes the a yes/no prompt screen with the given message
    to be displayed, and dismissed when the player hits yes or no.

    Returns True if the player hits yes, and False if the player hits no.

    `message`
        The message that will be displayed.

    See :func:`Confirm` for a similar Action.
    """
    Return = renpy.store.Return
    renpy.store.layout.yesno_screen(message, yes=Return(True), no=Return(False))
    return renpy.ui.interact()


def can_fullscreen():
    """
    :doc: other

    Returns True if the current platform supports fullscreen mode, False
    otherwise.
    """

    return renpy.display.can_fullscreen

def render_to_surface(d, width=None, height=None, st=0.0, at=None, resize=False):
    """
    :doc: screenshot

    This takes a displayable or Render, and returns a pygame_sdl2 surface. The render is performed by
    Ren'Py's display system, such that if the window is upscaled the render will be upscaled as well.

    `d`
        The displayable or Render to render. If a Render, `width`, `height`, `st`, and `at` are ignored.

    `width`
        The width to offer `d`, in virtual pixesl. If None, :var:`config.screen_width`.

    `height`
        The height to offer `d`, in virtual pixels. If None, :var:`config.screen_height`.

    `st`
        The time of the render, in the shown timebase.

    `at`
        The time of the rendem in the animation timebase. If None, `st` is used.

    `resize`
        If True, the surface will be resized to the virtual size of the displayable or render. This
        may lower the quality of the result.

    This function may only be called after the Ren'Py display system has started, so it can't be
    called during the init phase or before the first interaction.
    """

    if width is None:
        width = renpy.config.screen_width

    if height is None:
        height = renpy.config.screen_height

    if at is None:
        at = st


    if not isinstance(d, Render):
        d = renpy.easy.displayable(d)
        d = renpy.display.render.render(d, width, height, st, at)

    rv = renpy.display.draw.screenshot(d)

    if resize:
        return renpy.display.scale.smoothscale(rv, (d.width, d.height))
    else:
        return rv


def render_to_file(d, filename, width=None, height=None, st=0.0, at=None, resize=False):
    """
    :doc: screenshot

    Renders a displayable or Render, and saves the result of that render to a file. The render is performed by
    Ren'Py's display system, such that if the window is upscaled the render will be upscaled as well.

    `d`
        The displayable or Render to render. If a Render, `width`, `height`, `st`, and `at` are ignored.

    `filename`
        A string, giving the name of the file to save the render to. This is interpreted as relative
        to the base directory. This must end with .png.

    `width`
        The width to offer `d`, in virtual pixesl. If None, :var:`config.screen_width`.

    `height`
        The height to offer `d`, in virtual pixels. If None, :var:`config.screen_height`.

    `st`
        The time of the render, in the shown timebase.

    `at`
        The time of the rendem in the animation timebase. If None, `st` is used.

    `resize`
        If True, the image will be resized to the virtual size of the displayable or render. This
        may lower the quality of the result.

    This function may only be called after the Ren'Py display system has started, so it can't be
    called during the init phase or before the first interaction.

    Ren'Py not rescan files while the game is running, so this shouldn't be used to sythesize
    assets that are used as part of the game.
    """

    filename = os.path.join(renpy.config.basedir, filename)
    surface = render_to_surface(d, width, height, st, at, resize)
    pygame_sdl2.image.save(surface, filename)


import sys

for i in sys.modules:
    if i.startswith("renpy.exports"):
        mod = sys.modules[i]

        for k in dir(mod):
            if k not in globals():
                print(i, k)
