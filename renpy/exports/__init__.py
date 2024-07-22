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
    from urllib import urlencode as _urlencode # type: ignore
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

from renpy.editor import launch_editor


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


from renpy.exports.actionexports import (
    notify,
    display_notify,
    confirm,
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
    end_replay,
    get_return_stack,
    set_return_stack,
    get_line_log,
    clear_line_log,
    get_skipping,
    is_skipping,
    is_init_phase,
    add_to_all_stores,
)

from renpy.exports.debugexports import (
    warp_to_line,
    get_filename_line,
    log,
    push_error_handler,
    pop_error_handler,
    error,
    write_log
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
    get_physical_size,
    set_physical_size,
    reset_physical_size,
    get_image_load_log,
    get_mouse_pos,
    set_mouse_pos,
    cancel_gesture,
    add_layer,
    maximum_framerate,
    is_start_interact,
    get_refresh_rate,
    get_adjustment,
    get_texture_size,
    get_zorder_list,
    change_zorder,
    is_mouse_visible,
    get_mouse_name,
    set_focus,
    clear_retain,
    can_fullscreen,
    render_to_surface,
    render_to_file,
)

from renpy.exports.fetchexports import (
    FetchError,
    fetch_pause,
    fetch_requests,
    fetch_emscripten,
    fetch,
    proxies
)

from renpy.exports.inputexports import (
    web_input,
    input,
    get_editable_input_value,
    set_editable_input_value,
)

from renpy.exports.loaderexports import (
    loadable,
    exists,
    open_file,
    file,
    notl_file,
    list_files,
    fsencode,
    fsdecode,
    munge,
)

from renpy.exports.loadsaveexports import (
    clear_game_runtime,
    get_game_runtime
)

from renpy.exports.mediaexports import (
    movie_cutscene,
    toggle_music,
    music_start,
    music_stop,
    play,
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
    save_persistent,
    is_seen,
)

from renpy.exports.platformexports import (
    variant,
    vibrate,
    invoke_in_thread,
    invoke_in_main_thread,
    get_on_battery,
    get_sdl_dll,
    get_sdl_window_pointer,
    check_permission,
    request_permission,
)

from renpy.exports.predictexports import (
    cache_pin,
    cache_unpin,
    expand_predict,
    start_predict,
    stop_predict,
    start_predict_screen,
    stop_predict_screen,
    predicting,
)

from renpy.exports.restartexports import (
    full_restart,
    utter_restart,
    reload_script,
    quit,
    set_autoreload,
    get_autoreload,
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
    get_identifier_checkpoints
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
    count_dialogue_blocks,
    count_seen_dialogue_blocks,
    count_newly_seen_dialogue_blocks,
    substitute,
    get_say_image_tag,
    LastSay,
    last_say,
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

from renpy.exports.statementexports import (
    imagemap,
    pause,
    with_statement,
    jump,
    call,
    return_statement,
    call_screen,
    execute_default_statement,
)

globals()["with"] = with_statement


# The number of bits in the architecture.
if sys.maxsize > (2 << 32):
    bits = 64
else:
    bits = 32


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
