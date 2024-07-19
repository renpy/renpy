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
)


from renpy.exports.statementexports import (
    imagemap,
    pause,
)

def movie_cutscene(filename, delay=None, loops=0, stop_music=True):
    """
    :doc: movie_cutscene

    This displays a movie cutscene for the specified number of
    seconds. The user can click to interrupt the cutscene.
    Overlays and Underlays are disabled for the duration of the cutscene.

    `filename`
        The name of a file containing any movie playable by Ren'Py.

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

    Causes a transition to occur. This is the Python equivalent of the
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

    if not (renpy.game.preferences.transitions or always): # type: ignore
        trans = None

    renpy.exports.mode('with')

    if isinstance(trans, dict):

        for k, v in trans.items():
            if k is None:
                continue

            renpy.exports.transition(v, layer=k)

        if None not in trans:
            return

        trans = trans[None]

    return renpy.game.interface.do_with(trans, paired, clear=clear)


globals()["with"] = with_statement


def rollback(force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=True, current_label=None):
    """
    :doc: rollback
    :args: (force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=True)

    Rolls the state of the game back to the last checkpoint.

    `force`
        If true, the rollback will occur in all circumstances. Otherwise,
        the rollback will only occur if rollback is enabled in the store,
        context, and config.

    `checkpoints`
        Ren'Py will roll back through this many calls to renpy.checkpoint. It
        will roll back as far as it can, subject to this condition.

    `defer`
        If true, the call will be deferred until control returns to the main
        context.

    `greedy`
        If true, rollback will finish just after the previous checkpoint.
        If false, rollback finish just before the current checkpoint.

    `label`
        If not None, a label that is called when rollback completes.

    `abnormal`
        If true, the default, script executed after the transition is run in
        an abnormal mode that skips transitions that would have otherwise
        occured. Abnormal mode ends when an interaction begins.
    """

    if defer and not renpy.game.log.log:
        return

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
    renpy.game.log.rollback(checkpoints, greedy=greedy, label=label, force=(force is True), abnormal=abnormal, current_label=current_label)


def toggle_fullscreen():
    """
    :undocumented:
    Toggles the fullscreen mode.
    """

    renpy.game.preferences.fullscreen = not renpy.game.preferences.fullscreen # type: ignore


def toggle_music():
    """
    :undocumented:
    Does nothing.
    """


@renpy_pure
def has_label(name):
    """
    :doc: label

    Returns true if `name` is a valid label in the program, or false
    otherwise.

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

    for i in renpy.game.script.namemap:
        if isinstance(i, basestring):
            rv.append(i)

    return renpy.revertable.RevertableSet(rv)


def take_screenshot(scale=None, background=False):
    """
    :doc: loadsave
    :args: ()

    Causes a screenshot to be taken. This screenshot will be saved as part of
    a saved game.
    """

    if scale is None:
        scale = (renpy.config.thumbnail_width, renpy.config.thumbnail_height)

    renpy.game.interface.take_screenshot(scale, background=background)


def full_restart(transition=False, label="_invoke_main_menu", target="_main_menu", save=False):
    """
    :doc: other
    :args: (transition=False, *, save=False)

    Causes Ren'Py to restart, returning the user to the main menu.

    `transition`
        If given, the transition to run, or None to not run a transition.
        False uses :var:`config.end_game_transition`.

    `save`
        If true, the game is saved in :var:`_quit_slot` before Ren'Py
        restarts and returns the user to the main menu.
    """

    if save and (renpy.store._quit_slot is not None):
        renpy.loadsave.save(renpy.store._quit_slot, getattr(renpy.store, "save_name", ""))

    if transition is False:
        transition = renpy.config.end_game_transition

    raise renpy.game.FullRestartException((transition, label, target)) # type: ignore


def utter_restart(keep_renderer=False):
    """
    :undocumented: Used in the implementation of shift+R.

    Causes an utter restart of Ren'Py. This reloads the script and
    re-runs initialization.
    """

    renpy.session["_keep_renderer"] = keep_renderer

    raise renpy.game.UtterRestartException()

def reload_script():
    """
    :doc: reload

    Causes Ren'Py to save the game, reload the script, and then load the
    save.

    This should only be called during development. It works on Windows, macOS,
    and Linux, but may not work on other platforms.
    """

    # Avoid reloading in a replay.
    if renpy.store._in_replay:
        return

    s = get_screen("menu")

    session = renpy.session
    session["_reload"] = True

    # If one of these variables is already in session, we're recovering from
    # a failed reload.
    if ("_reload_screen" in session) or ("_main_menu_screen" in session):
        utter_restart()

    if not renpy.store.main_menu:

        if s is not None:
            session["_reload_screen"] = s.screen_name[0]
            session["_reload_screen_args"] = s.scope.get("_args", ())
            session["_reload_screen_kwargs"] = s.scope.get("_kwargs", { })

        renpy.game.call_in_new_context("_save_reload_game")

    else:

        if s is not None:
            session["_main_menu_screen"] = s.screen_name[0]
            session["_main_menu_screen_args"] = s.scope.get("_args", ())
            session["_main_menu_screen_kwargs"] = s.scope.get("_kwargs", { })

        utter_restart()


def quit(relaunch=False, status=0, save=False): # @ReservedAssignment
    """
    :doc: other

    This causes Ren'Py to exit entirely.

    `relaunch`
        If true, Ren'Py will run a second copy of itself before quitting.

    `status`
        The status code Ren'Py will return to the operating system.
        Generally, 0 is success, and positive integers are failure.

    `save`
        If true, the game is saved in :var:`_quit_slot` before Ren'Py
        terminates.
    """

    if save and (renpy.store._quit_slot is not None):
        renpy.loadsave.save(renpy.store._quit_slot, getattr(renpy.store, "save_name", ""))

    if has_label("quit"):
        call_in_new_context("quit")

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
    :doc: context

    Causes control to leave the current context, and then to be
    transferred in the parent context to the given label.
    """

    raise renpy.game.JumpOutException(label)


def call(label, *args, **kwargs):
    """
    :doc: se_call
    :args: (label, *args, from_current=False, **kwargs)

    Causes the current Ren'Py statement to terminate, and a jump to a
    `label` to occur. When the jump returns, control will be passed
    to the statement following the current statement.

    The label must be either of the form "global_name" or "global_name.local_name".
    The form ".local_name" is not allowed.

    `from_current`
        If true, control will return to the current statement, rather than
        the statement following the current statement. (This will lead to
        the current statement being run twice. This must be passed as a
        keyword argument.)
    """

    from_current = kwargs.pop("from_current", False)
    raise renpy.game.CallException(label, args, kwargs, from_current=from_current)


def return_statement(value=None):
    """
    :doc: se_call

    Causes Ren'Py to return from the current Ren'Py-level call.
    """

    renpy.store._return = value
    jump("_renpy_return")


def warp_to_line(warp_spec):
    """
    :doc: debug

    This takes as an argument a filename:linenumber pair, and tries to warp to
    the statement before that line number.

    This works samely as the `--warp` command.
    """

    renpy.warp.warp_spec = warp_spec
    full_restart()


def screenshot(filename):
    """
    :doc: screenshot

    Saves a screenshot in `filename`.

    Returns True if the screenshot was saved successfully, False if saving
    failed for some reason.

    The :var:`config.screenshot_pattern` and :var:`_screenshot_pattern`
    variables control the file the screenshot is saved in.
    """

    return renpy.game.interface.save_screenshot(filename)


def screenshot_to_bytes(size):
    """
    :doc: screenshot

    Returns a screenshot as a bytes object, that can be passed to im.Data().
    The bytes will be a png-format image, such that::

        $ data = renpy.screenshot_to_bytes((640, 360))
        show expression im.Data(data, "screenshot.png"):
            align (0, 0)

    Will show the image. The bytes objects returned can be stored in save
    files and persistent data. However, these may be large, and care should
    be taken to not include too many.

    `size`
        The size the screenshot will be resized to. If None, the screenshot
        will be resized, and hence will be the size of the player's window,
        without any letterbars.

    This function may be slow, and so it's intended for save-like screenshots,
    and not realtime effects.
    """

    return renpy.game.interface.screenshot_to_bytes(size)


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

    if isinstance(trans, dict):
        for ly, t in trans.items():
            transition(t, layer=ly, always=always, force=force)
        return

    if (not always) and not renpy.game.preferences.transitions: # type: ignore
        trans = None

    if renpy.config.skipping:
        trans = None

    renpy.game.interface.set_transition(trans, layer, force=force)


def get_transition(layer=None):
    """
    :doc: other

    Gets the transition for `layer`, or the entire scene if
    `layer` is None. This returns the transition that is queued up
    to run during the next interaction, or None if no such
    transition exists.

    Use :func:`renpy.get_ongoing_transition` to get the transition that is
    in progress.
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
def loadable(filename, directory=None, tl=True):
    """
    :doc: file

    Returns True if the given filename is loadable, meaning that it
    can be loaded from the disk or from inside an archive. Returns
    False if this is not the case.

    `directory`
        If not None, a directory to search in if the file is not found
        in the game directory. This will be prepended to filename, and
        the search tried again.
    `tl`
        If True, a translation subdirectory will be considered as well.
    """

    return renpy.loader.loadable(filename, tl=tl, directory=directory)


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
    except Exception:
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
    except Exception:
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
    Deprecated music stop function, retained for compatibility. Use
    renpy.music.stop() instead.
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
    the logfile (if not already open), formats the message to :var:`config.log_width`
    columns, and prints it to the logfile.
    """

    global logfile

    if not renpy.config.log:
        return

    if msg is None:
        return

    try:
        msg = unicode(msg)
    except Exception:
        pass

    try:

        if not logfile:
            import os
            if renpy.config.clear_log:
                file_mode = "w"
            else:
                file_mode = "a"
            logfile = open(os.path.join(renpy.config.basedir, renpy.config.log), file_mode)

            if not logfile.tell():
                logfile.write("\ufeff")

        import textwrap

        wrapped = [ ]

        for line in msg.split('\n'):
            line = textwrap.fill(line, renpy.config.log_width)
            line = unicode(line)
            wrapped.append(line)

        wrapped = '\n'.join(wrapped)

        logfile.write(wrapped + "\n")
        logfile.flush()

    except Exception:
        renpy.config.log = None


def force_full_redraw():
    """
    :undocumented:

    Forces the screen to be redrawn in full. Call this after using pygame
    to redraw the screen directly.
    """

    # This had been used for the software renderer, but gl rendering redraws
    # the screen every frame, so it's removed.
    return


def do_reshow_say(who, what, interact=False, *args, **kwargs):

    if who is not None:
        who = renpy.python.py_eval(who)

    say(who, what, *args, interact=interact, **kwargs)


curried_do_reshow_say = curry(do_reshow_say)


def get_reshow_say(**kwargs):
    kw = dict(renpy.store._last_say_kwargs)
    kw.update(kwargs)

    return curried_do_reshow_say(
        renpy.store._last_say_who,
        renpy.store._last_say_what,
        renpy.store._last_say_args,
        **kw)


def reshow_say(**kwargs):
    get_reshow_say()(**kwargs)


def current_interact_type():
    return getattr(renpy.game.context().info, "_current_interact_type", None)


def last_interact_type():
    return getattr(renpy.game.context().info, "_last_interact_type", None)


def dynamic(*variables, **kwargs):
    """
    :doc: label

    This can be given one or more variable names as arguments. This makes the
    variables dynamically scoped to the current call. When the call returns, the
    variables will be reset to the value they had when this function was called.

    Variables in :ref:`named stores <named-stores>` are supported.

    If the variables are given as keyword arguments, the value of the argument
    is assigned to the variable name.

    Example calls are::

        $ renpy.dynamic("x", "y", "z")
        $ renpy.dynamic("mystore.serial_number")
        $ renpy.dynamic(players=2, score=0)
    """

    variables = variables + tuple(kwargs)
    renpy.game.context().make_dynamic(variables)

    for k, v in kwargs.items():
        setattr(renpy.store, k, v)


def context_dynamic(*variables):
    """
    :doc: context

    This can be given one or more variable names as arguments. This makes the
    variables dynamically scoped to the current context. When returning to the
    prior context, the variables will be reset to the value they had when this
    function was called.

    Variables in :ref:`named stores <named-stores>` are supported.

    Example calls are::

        $ renpy.context_dynamic("x", "y", "z")
        $ renpy.context_dynamic("mystore.serial_number")
    """

    renpy.game.context().make_dynamic(variables, context=True)


def seen_label(label):
    """
    :doc: label

    Returns true if the named label has executed at least once on the current user's
    system, and false otherwise. This can be used to unlock scene galleries, for
    example.
    """
    return label in renpy.game.persistent._seen_ever # type: ignore


def mark_label_seen(label):
    """
    :doc: label

    Marks the named label as if it has been already executed on the current user's
    system.
    """
    renpy.game.persistent._seen_ever[str(label)] = True # type: ignore


def mark_label_unseen(label):
    """
    :doc: label

    Marks the named label as if it has not been executed on the current user's
    system yet.
    """
    if label in renpy.game.persistent._seen_ever: # type: ignore
        del renpy.game.persistent._seen_ever[label] # type: ignore


def seen_audio(filename):
    """
    :doc: audio

    Returns True if the given filename has been played at least once on the current
    user's system.
    """
    filename = re.sub(r'^<.*?>', '', filename)

    return filename in renpy.game.persistent._seen_audio # type: ignore


def mark_audio_seen(filename):
    """
    :doc: audio

    Marks the given filename as if it has been already played on the current user's
    system.
    """
    filename = re.sub(r'^<.*?>', '', filename)

    renpy.game.persistent._seen_audio[filename] = True # type: ignore


def mark_audio_unseen(filename):
    """
    :doc: audio

    Marks the given filename as if it has not been played on the current user's
    system yet.
    """
    filename = re.sub(r'^<.*?>', '', filename)

    if filename in renpy.game.persistent._seen_audio: # type: ignore
        del renpy.game.persistent._seen_audio[filename] # type: ignore


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

    return name in renpy.game.persistent._seen_images # type: ignore


def mark_image_seen(name):
    """
    :doc: image_func

    Marks the named image as if it has been already displayed on the current user's
    system.
    """
    if not isinstance(name, tuple):
        name = tuple(name.split())

    renpy.game.persistent._seen_images[tuple(str(i) for i in name)] = True


def mark_image_unseen(name):
    """
    :doc: image_func

    Marks the named image as if it has not been displayed on the current user's
    system yet.
    """
    if not isinstance(name, tuple):
        name = tuple(name.split())

    if name in renpy.game.persistent._seen_images: # type: ignore
        del renpy.game.persistent._seen_images[name] # type: ignore


def open_file(fn, encoding=None, directory=None): # @ReservedAssignment
    """
    :doc: file

    Returns a read-only file-like object that accesses the file named `fn`. The file is
    accessed using Ren'Py's standard search method, and may reside in the game directory,
    in an RPA archive, or as an Android asset.

    The object supports a wide subset of the fields and methods found on Python's
    standard file object, opened in binary mode. (Basically, all of the methods that
    are sensible for a read-only file.)

    `encoding`
        If given, the file is open in text mode with the given encoding.
        If None, the default, the encoding is taken from :var:`config.open_file_encoding`.
        If False, the file is opened in binary mode.

    `directory`
        If not None, a directory to search in if the file is not found
        in the game directory. This will be prepended to filename, and
        the search tried again.
    """

    rv = renpy.loader.load(fn, directory=directory)

    if encoding is None:
        encoding = renpy.config.open_file_encoding

    if encoding:
        rv = io.TextIOWrapper(rv, encoding=encoding, errors="surrogateescape") # type: ignore

    return rv

def file(fn, encoding=None):
    """
    :doc: file

    An alias for :func:`renpy.open_file`, for compatibility with older
    versions of Ren'Py.
    """

    return open_file(fn, encoding=encoding)

def notl_file(fn): # @ReservedAssignment
    """
    :undocumented:

    Like file, but doesn't search the translation prefix.
    """
    return renpy.loader.load(fn, tl=False)


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


def get_at_list(name, layer=None):
    """
    :doc: se_images

    Returns the list of transforms being applied to the image with tag `name`
    on `layer`. Returns an empty list if no transforms are being applied, or
    None if the image is not shown.

    If `layer` is None, uses the default layer for the given tag.
    """

    if isinstance(name, basestring):
        name = tuple(name.split())

    tag = name[0]
    layer = default_layer(layer, tag)

    transforms = renpy.game.context().scene_lists.at_list[layer].get(tag, None)

    if transforms is None:
        return None

    return list(transforms)


def show_layer_at(at_list, layer='master', reset=True, camera=False):
    """
    :doc: se_images
    :name: renpy.show_layer_at

    The Python equivalent of the ``show layer`` `layer` ``at`` `at_list`
    statement. If `camera` is True, the equivalent of the ``camera`` statement.

    `reset`
        If true, the transform state is reset to the start when it is shown.
        If false, the transform state is persisted, allowing the new transform
        to update that state.
    """

    at_list = renpy.easy.to_list(at_list)

    renpy.game.context().scene_lists.set_layer_at_list(layer, at_list, reset=reset, camera=camera)


layer_at_list = show_layer_at


def free_memory():
    """
    :doc: other

    Attempts to free some memory. Useful before running a renpygame-based
    minigame.
    """

    force_full_redraw()
    renpy.display.interface.kill_textures()
    renpy.display.interface.kill_surfaces()
    renpy.text.font.free_memory()

    gc.collect(2)

    if gc.garbage:
        del gc.garbage[:]


def flush_cache_file(fn):
    """
    :doc: image_func

    This flushes all image cache entries that refer to the file `fn`.  This
    may be called when an image file changes on disk to force Ren'Py to
    use the new version.
    """

    renpy.display.im.cache.flush_file(fn)


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
curried_call_in_new_context = curry(call_in_new_context)
invoke_in_new_context = renpy.game.invoke_in_new_context
curried_invoke_in_new_context = curry(invoke_in_new_context)
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
    """
    :doc: lint

    Reports `msg`, a string, as as error for the user. This is logged as a
    parse or lint error when approprate, and otherwise it is raised as an
    exception.
    """

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

    Returns the scry object for the current statement. Returns None if
    there are no statements executing.

    The scry object tells Ren'Py about things that must be true in the
    future of the current statement. Right now, the scry object has the
    following fields:

    `nvl_clear`
        Is true if an ``nvl clear`` statement will execute before the
        next interaction.

    `say`
        Is true if an ``say`` statement will execute before the
        next interaction.

    `menu_with_caption`
        Is true if a ``menu`` statement with a caption will execute
        before the next interaction.

    `who`
        If a ``say`` or ``menu-with-caption`` statement will execute
        before the next interaction, this is the character object it will use.

    The scry object has a next() method, which returns the scry object of
    the statement after the current one, if only one statement will execute
    after the this one. Otherwise, it returns None.

    .. warning::

        Like other similar functions, the object this returns is meant to be used
        in the short term after the function is called. Including it in save data
        or making it participate in rollback is not advised.
    """

    name = renpy.game.context().current

    if name is None:
        return None

    node = renpy.game.script.lookup(name)
    return node.scry()


@renpy_pure
def munged_filename():
    return renpy.lexer.munge_filename(get_filename_line()[0])

# Module loading stuff.


loaded_modules = set()


def load_module(name, **kwargs):
    """
    :doc: other
    :args: (name)

    This loads the Ren'Py module named name. A Ren'Py module consists of Ren'Py script
    that is loaded into the usual (store) namespace, contained in a file named
    name.rpym or name.rpymc. If a .rpym file exists, and is newer than the
    corresponding .rpymc file, it is loaded and a new .rpymc file is created.

    All of the init blocks (and other init-phase code) in the module are run
    before this function returns. An error is raised if the module name cannot
    be found, or is ambiguous.

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
    renpy.store.__dict__.update(kwargs) # @UndefinedVariable

    for _prio, node in initcode: # @UnusedVariable
        if isinstance(node, renpy.ast.Node):
            renpy.game.context().run(node)
        else:
            node()

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

        stmts, initcode = renpy.game.script.load_string(filename, str(s))

        if stmts is None:
            return None

        context = renpy.execution.Context(False)
        context.init_phase = True
        renpy.game.contexts.append(context)

        for _prio, node in initcode:
            if isinstance(node, renpy.ast.Node):
                renpy.game.context().run(node)
            else:
                node()

        context.pop_all_dynamic()
        renpy.game.contexts.pop()

        renpy.config.locked = old_locked

        renpy.game.script.analyze()

        return stmts[0].name

    finally:
        renpy.game.exception_info = old_exception_info


def load_language(language):
    """
    :undocumented:

    (Here because of commonality with load_string and load_module.)

    Load the script files in tl/language, if not loaded. Runs any
    init code found during the process.
    """

    if language is None:
        return

    if not renpy.config.defer_tl_scripts:
        return

    if language in renpy.game.script.load_languages:
        return

    old_exception_info = renpy.game.exception_info

    try:

        old_locked = renpy.config.locked
        renpy.config.locked = False

        renpy.game.script.load_languages.add(language)

        initcode = renpy.game.script.load_script()

        context = renpy.execution.Context(False)
        context.init_phase = True
        renpy.game.contexts.append(context)

        for _prio, node in initcode:
            if isinstance(node, renpy.ast.Node):
                renpy.game.context().run(node)
            else:
                node()

        context.pop_all_dynamic()
        renpy.game.contexts.pop()

        renpy.config.locked = old_locked

        if not renpy.game.context().init_phase:
            renpy.game.script.analyze()

        renpy.game.script.update_bytecode()

    finally:
        renpy.game.exception_info = old_exception_info


def include_module(name):
    """
    :doc: other

    Similar to :func:`renpy.load_module`, but instead of loading the module right away,
    inserts it into the init queue somewhere after the current AST node.

    The module may not contain init blocks lower than the block that includes the module.
    For example, if your module contains an init 10 block, the latest you can load it is
    init 10.

    Module loading may only occur from inside an init block.
    """

    if not renpy.game.context().init_phase:
        raise Exception("Module loading is only allowed in init code.")

    renpy.game.script.include_module(name)


def pop_call():
    """
    :doc: label
    :name: renpy.pop_call

    Pops the current call from the call stack, without returning to the
    location. Also reverts the values of :func:`dynamic <renpy.dynamic>`
    variables, the same way the Ren'Py return statement would.

    This can be used if a label that is called decides not to return
    to its caller.
    """

    renpy.game.context().pop_call()


pop_return = pop_call


def call_stack_depth():
    """
    :doc: label

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
        call_in_new_context("_game_menu", _game_menu_screen=screen)


def shown_window():
    """
    :doc: other

    Call this to indicate that the window has been shown. This interacts
    with the "window show" statement, which shows an empty window whenever
    this functions has not been called during an interaction.
    """

    renpy.game.context().scene_lists.shown_window = True


class placement(renpy.revertable.RevertableObject):

    def __init__(self, p):
        super(placement, self).__init__()

        self.xpos = p[0]
        self.ypos = p[1]
        self.xanchor = p[2]
        self.yanchor = p[3]
        self.xoffset = p[4]
        self.yoffset = p[5]
        self.subpixel = p[6]

    @property
    def pos(self):
        return self.xpos, self.ypos

    @property
    def anchor(self):
        return self.xanchor, self.yanchor

    @property
    def offset(self):
        return self.xoffset, self.yoffset


def get_placement(d):
    """
    :doc: image_func

    This gets the placement of displayable d. There's very little warranty on this
    information, as it might change when the displayable is rendered, and might not
    exist until the displayable is first rendered.

    This returns an object with the following fields, each corresponding to a style
    property:

    * pos
    * xpos
    * ypos
    * anchor
    * xanchor
    * yanchor
    * offset
    * xoffset
    * yoffset
    * subpixel
    """
    p = d.get_placement()

    return placement(p)


def get_image_bounds(tag, width=None, height=None, layer=None):
    """
    :doc: image_func

    If an image with `tag` exists on `layer`, returns the bounding box of
    that image. Returns None if the image is not found.

    The bounding box is an (x, y, width, height) tuple. The components of
    the tuples are expressed in pixels, and may be floating point numbers.

    `width`, `height`
        The width and height of the area that contains the image. If None,
        defaults the width and height of the screen, respectively.

    `layer`
        If None, uses the default layer for `tag`.
    """

    tag = tag.split()[0]
    layer = default_layer(layer, tag)

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

def is_pixel_opaque(d, width, height, st, at, x, y):
    """
    :doc: udd_utility

    Returns whether the pixel at (x, y) is opaque when this displayable
    is rendered by ``renpy.render(d, width, height, st, at)``.
    """

    # Uses the caching features of renpy.render, as opposed to d.render.
    return bool(render(renpy.easy.displayable(d), width, height, st, at).is_pixel_opaque(x, y))


class Displayable(renpy.display.displayable.Displayable, renpy.revertable.RevertableObject):
    pass


class Container(renpy.display.layout.Container, renpy.revertable.RevertableObject):
    _list_type = renpy.revertable.RevertableList


def get_roll_forward():
    return renpy.game.interface.shown_window


def cache_pin(*args):
    """
    :undocumented: Cache pinning has been removed.
    """

def cache_unpin(*args):
    """
    :undocumented: Cache pinning has been removed
    """


def expand_predict(d):
    """
    :undocumented:

    Use the fnmatch function to expland `d` for the purposes of prediction.
    """

    if not isinstance(d, basestring):
        return [ d ]

    if not "*" in d:
        return [ d ]

    if "." in d:
        l = list_files(False)
    else:
        l = list_images()

    return fnmatch.filter(l, d)


def start_predict(*args):
    """
    :doc: image_func

    This function takes one or more displayables as arguments. It causes
    Ren'Py to predict those displayables during every interaction until
    the displayables are removed by :func:`renpy.stop_predict`.

    If a displayable name is a string containing one or more \\*
    characters, the asterisks are used as a wildcard pattern. If there
    is at least one . in the string, the pattern is matched against
    filenames, otherwise it is matched against image names.

    For example::

        $ renpy.start_predict("eileen *")

    starts predicting all images with the name eileen, while::

        $ renpy.start_predict("images/concert*.*")

    matches all files starting with concert in the images directory.

    Prediction will occur during normal gameplay. To wait for prediction
    to complete, use the `predict` argument to :func:`renpy.pause`.
    """

    new_predict = renpy.revertable.RevertableSet(renpy.store._predict_set)

    for i in args:
        for d in expand_predict(i):
            d = renpy.easy.displayable(d)
            new_predict.add(d)

    renpy.store._predict_set = new_predict


def stop_predict(*args):
    """
    :doc: image_func

    This function takes one or more displayables as arguments. It causes
    Ren'Py to stop predicting those displayables during every interaction.

    Wildcard patterns can be used as described in :func:`renpy.start_predict`.
    """

    new_predict = renpy.revertable.RevertableSet(renpy.store._predict_set)

    for i in args:
        for d in expand_predict(i):
            d = renpy.easy.displayable(d)
            new_predict.discard(d)

    renpy.store._predict_set = new_predict


def start_predict_screen(_screen_name, *args, **kwargs):
    """
    :doc: screens

    Causes Ren'Py to start predicting the screen named `_screen_name`
    with the given arguments. This replaces any previous prediction
    of `_screen_name`. To stop predicting a screen, call :func:`renpy.stop_predict_screen`.

    Prediction will occur during normal gameplay. To wait for prediction
    to complete, use the `predict` argument to :func:`renpy.pause`.
    """

    new_predict = renpy.revertable.RevertableDict(renpy.store._predict_screen)
    new_predict[_screen_name] = (args, kwargs)
    renpy.store._predict_screen = new_predict


def stop_predict_screen(name):
    """
    :doc: screens

    Causes Ren'Py to stop predicting the screen named `name`.
    """

    new_predict = renpy.revertable.RevertableDict(renpy.store._predict_screen)
    new_predict.pop(name, None)
    renpy.store._predict_screen = new_predict


def call_screen(_screen_name, *args, **kwargs):
    """
    :doc: screens
    :args: (_screen_name, *args, _with_none=True, _mode="screen", **kwargs)

    The programmatic equivalent of the call screen statement.

    This shows `_screen_name` as a screen, then causes an interaction
    to occur. The screen is hidden at the end of the interaction, and
    the result of the interaction is returned.

    Positional arguments, and keyword arguments that do not begin with
    _ are passed to the screen.

    If `_with_none` is false, "with None" is not run at the end of end
    of the interaction.

    If `_mode` is passed, it will be the mode of this interaction,
    otherwise the mode will be "screen".
    """

    mode = kwargs.pop("_mode", "screen")
    renpy.exports.mode(mode)

    with_none = kwargs.pop("_with_none", renpy.config.implicit_with_none)

    show_screen(_screen_name, *args, _transient=True, **kwargs)

    roll_forward = renpy.exports.roll_forward_info()

    # If roll
    can_roll_forward = renpy.display.screen.get_screen_roll_forward(_screen_name)

    if can_roll_forward is None:
        can_roll_forward = renpy.config.call_screen_roll_forward

    if not can_roll_forward:
        roll_forward = None

    try:
        rv = renpy.ui.interact(mouse="screen", type="screen", roll_forward=roll_forward)
    except (renpy.game.JumpException, renpy.game.CallException) as e:
        rv = e

    renpy.exports.checkpoint(rv)

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

    for _dir, fn in renpy.loader.listdirfiles(common):
        if fn.startswith("saves/"):
            continue

        rv.append(fn)

    rv.sort()

    return rv


def get_renderer_info():
    """
    :doc: other

    Returns a dictionary, giving information about the renderer Ren'Py is
    currently using. Defined keys are:

    ``"renderer"``
        A string giving the name of the renderer that is in use.

    ``"resizable"``
        True if and only if the window is resizable.

    ``"additive"``
        True if and only if the renderer supports additive blending.

    ``"model"``
        Present and true if model-based rendering is supported.

    Other, renderer-specific, keys may also exist. The dictionary should
    be treated as immutable. This should only be called once the display
    has been started (that is, after the init phase has finished).
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
    :undocumented:

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

    This function just calls :var:`config.notify`, allowing its implementation
    to be replaced by assigning a new function to that variable.
    """

    renpy.config.notify(message)


def display_notify(message):
    """
    :doc: other

    The default implementation of :func:`renpy.notify`.
    """

    hide_screen('notify')
    show_screen('notify', message=message)
    renpy.display.tts.notify_text = renpy.text.extras.filter_alt_text(message)

    restart_interaction()


@renpy_pure
def variant(name):
    """
    :doc: screens

    Returns true if `name` is a screen variant that corresponds to the
    context in which Ren'Py is currently executing. See :ref:`screen-variants`
    for more details. This function can be used as the condition in an
    if statement to switch behavior based on the selected screen variant.

    `name` can also be a list of variants, in which case this function
    returns True if any of the variants would.
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

    if duration < 0.01:
        duration = 0.01

    if renpy.android:
        import android # @UnresolvedImport
        android.vibrate(duration)


def get_say_attributes():
    """
    :doc: other

    Gets the attributes associated with the current say statement, or
    None if no attributes are associated with this statement.

    This is only valid when executing or predicting a say statement.
    """

    return renpy.game.context().say_attributes


def get_side_image(prefix_tag, image_tag=None, not_showing=None, layer=None):
    """
    :doc: side

    This attempts to find an image to show as the side image.

    It begins by determining a set of image attributes. If `image_tag` is
    given, it gets the image attributes from the tag. Otherwise, it gets
    them from the image property suplied to the currently showing character.
    If no attributes are available, this returns None.

    It then looks up an image with the tag `prefix_tag`, and attributes
    consisting of:

    * An image tag (either from `image_tag` or the image property supplied
      to the currently showing character).
    * The attributes.

    If such an image exists, it's returned.

    `not_showing`
        If not showing is True, this only returns a side image if an image
        with the tag that the attributes are taken from is not currently
        being shown. If False, it will always return an image, if possible.
        If None, takes the value from :var:`config.side_image_only_not_showing`.

    `layer`
        If given, the layer to look for the image tag and attributes on. If
        None, uses the default layer for the tag.
    """

    if not_showing is None:
        not_showing = renpy.config.side_image_only_not_showing

    images = renpy.game.context().images

    if image_tag is not None:
        image_layer = default_layer(layer, image_tag)
        attrs = (image_tag,) + images.get_attributes(image_layer, image_tag)

        if renpy.config.side_image_requires_attributes and (len(attrs) < 2):
            return None

    else:

        # Character will compute the appropriate attributes, and stores it
        # in _side_image_attributes.
        attrs = renpy.store._side_image_attributes

    if not attrs:
        return None

    attr_layer = default_layer(layer, attrs)

    if not_showing and images.showing(attr_layer, (attrs[0],)):
        return None

    required = [ attrs[0] ]
    optional = list(attrs[1:])

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


def get_ongoing_transition(layer=None):
    """
    :doc: other

    Returns the transition that is currently ongoing.

    `layer`
        If None, the top-level transition is returned. Otherwise, this should be a string giving a layer name,
        in which case the transition for that layer is returned.
    """

    return renpy.display.interface.get_ongoing_transition(layer)


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
