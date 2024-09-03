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

import renpy
import pygame_sdl2

try:
    import emscripten
except ImportError:
    pass

import renpy.audio.sound as sound
import renpy.audio.music as music

from renpy.ast import (
    eval_who,
)

from renpy.atl import (
    atl_warper,
)

from renpy.bootstrap import (
    get_alternate_base,
)

from renpy.character import (
    display_say,
    predict_show_display_say,
    show_display_say,
)

from renpy.curry import (
    curry,
    partial,
)

from renpy.display.behavior import (
    Keymap,
    clear_keymap_cache,
    is_selected,
    is_sensitive,
    map_event,
    queue_event,
    run,
    run as run_action,
    run_periodic,
    run_unhovered,
)

from renpy.display.focus import (
    capture_focus,
    clear_capture_focus,
    focus_coordinates,
    get_focus_rect,
)

from renpy.display.im import (
    load_image,
    load_rgba,
    load_surface,
)

from renpy.display.image import (
    check_image_attributes,
    get_available_image_attributes,
    get_available_image_tags,
    get_ordered_image_attributes,
    get_registered_image,
    image_exists,
    image_exists as has_image,
    list_images,
)

from renpy.display.minigame import (
    Minigame,
)

from renpy.display.predict import (
    screen as predict_screen,
)

from renpy.display.screen import (
    ScreenProfile as profile_screen,
    current_screen,
    define_screen,
    get_displayable,
    get_displayable_properties,
    get_screen,
    get_screen_variable,
    get_widget,
    get_widget_properties,
    has_screen,
    hide_screen,
    set_screen_variable,
    show_screen,
    use_screen,
)

from renpy.display.tts import (
    speak as alt,
    speak_extra_alt,
)

from renpy.display.video import (
    movie_start_displayable,
    movie_start_fullscreen,
    movie_stop,
)

from renpy.easy import (
    displayable,
    predict,
    split_properties,
)

from renpy.editor import (
    launch_editor,
)

from renpy.execution import (
    not_infinite_loop,
    reset_all_contexts,
)

from renpy.exports.commonexports import (
    renpy_pure,
)

from renpy.gl2.gl2shadercache import (
    register_shader,
)

from renpy.gl2.live2d import (
    has_live2d,
)

from renpy.lexer import (
    unelide_filename,
)

from renpy.lint import (
    try_compile,
    try_eval,
)

from renpy.loader import (
    add_python_directory,
)

from renpy.loadsave import (
    can_load,
    copy_save,
    force_autosave,
    list_saved_games,
    list_slots,
    load,
    newest_slot,
    rename_save,
    save,
    scan_saved_game,
    slot_json,
    slot_mtime,
    slot_screenshot,
    unlink_save,
)

from renpy.memory import (
    diff_memory,
    profile_memory,
    profile_rollback,
)

from renpy.parser import (
    get_parse_errors,
)

from renpy.persistent import (
    register_persistent,
)

from renpy.pyanalysis import (
    const,
    not_const,
    pure,
)

from renpy.python import (
    py_eval as eval,
)

from renpy.rollback import (
    rng as random,
)

from renpy.savetoken import (
    get_save_token_keys,
)

from renpy.sl2.slparser import (
    CustomParser as register_sl_statement,
    register_sl_displayable,
)

from renpy.statements import (
    register as register_statement,
)

from renpy.text.extras import (
    ParameterizedText,
    check_text_tags,
    filter_text_tags,
)

from renpy.text.font import (
    register_bmfont,
    register_mudgefont,
    register_sfont,
    variable_font_info,
)

from renpy.text.shader import (
    TextShader,
    register_textshader,
)

from renpy.text.text import (
    BASELINE,
    language_tailor,
)

from renpy.text.textsupport import (
    DISPLAYABLE as TEXT_DISPLAYABLE,
    PARAGRAPH as TEXT_PARAGRAPH,
    TAG as TEXT_TAG,
    TEXT as TEXT_TEXT,
)

from renpy.translation import (
    change_language,
    get_translation_identifier,
    get_translation_info,
    known_languages,
    translate_string,
)

from renpy.translation.generation import (
    generic_filter as transform_text,
)

from renpy.ui import (
    Choice,
)


renpy_pure("check_text_tags")
renpy_pure("curry")
renpy_pure("filter_text_tags")
renpy_pure("has_screen")
renpy_pure("image_exists")
renpy_pure("Keymap")
renpy_pure("known_languages")
renpy_pure("ParameterizedText")
renpy_pure("partial")
renpy_pure("split_properties")
renpy_pure("unelide_filename")

from renpy.exports.actionexports import (
    confirm,
    display_notify,
    notify,
)

from renpy.exports.contextexports import (
    add_to_all_stores,
    call_in_new_context,
    call_replay,
    call_stack_depth,
    clear_game_runtime,
    clear_line_log,
    context_dynamic,
    context_nesting_level,
    context,
    current_interact_type,
    curried_call_in_new_context,
    curried_invoke_in_new_context,
    dynamic,
    end_replay,
    game_menu,
    get_game_runtime,
    get_line_log,
    get_mode,
    get_return_stack,
    get_skipping,
    invoke_in_new_context,
    is_init_phase,
    is_skipping,
    jump_out_of_context,
    last_interact_type,
    mode,
    pop_call,
    pop_return,
    scry,
    set_return_stack,
    stop_skipping,
)

from renpy.exports.debugexports import (
    error,
    get_filename_line,
    log,
    pop_error_handler,
    push_error_handler,
    warp_to_line,
    write_log
)

from renpy.exports.displayexports import (
    _find_image,
    add_layer,
    can_fullscreen,
    can_show,
    cancel_gesture,
    change_zorder,
    clear_attributes,
    clear_retain,
    Container,
    copy_images,
    count_displayables_in_layer,
    default_layer,
    display_reset,
    Displayable,
    easy_displayable,
    end_interaction,
    flush_cache_file,
    force_full_redraw,
    free_memory,
    get_adjustment,
    get_at_list,
    get_attributes,
    get_hidden_tags,
    get_image_bounds,
    get_image_load_log,
    get_mouse_name,
    get_mouse_pos,
    get_ongoing_transition,
    get_physical_size,
    get_placement,
    get_refresh_rate,
    get_renderer_info,
    get_showing_tags,
    get_texture_size,
    get_transition,
    get_zorder_list,
    hide,
    iconify,
    IgnoreEvent,
    image_size,
    image,
    is_mouse_visible,
    is_pixel_opaque,
    is_start_interact,
    layer_at_list,
    maximum_framerate,
    placement,
    predict_show,
    quit_event,
    redraw,
    render_to_file,
    render_to_surface,
    render,
    Render,
    reset_physical_size,
    restart_interaction,
    scene_lists,
    scene,
    screenshot_to_bytes,
    screenshot,
    set_focus,
    set_mouse_pos,
    set_physical_size,
    set_tag_attributes,
    show_layer_at,
    show,
    showing,
    shown_window,
    take_screenshot,
    timeout,
    toggle_fullscreen,
    transition,
)

from renpy.exports.fetchexports import (
    fetch_emscripten,
    fetch_pause,
    fetch_requests,
    fetch,
    FetchError,
    proxies
)

from renpy.exports.inputexports import (
    get_editable_input_value,
    input,
    set_editable_input_value,
    web_input,
)

from renpy.exports.loaderexports import (
    exists,
    file,
    fsdecode,
    fsencode,
    list_files,
    loadable,
    munge,
    notl_file,
    open_file,
)

from renpy.exports.mediaexports import (
    movie_cutscene,
    music_start,
    music_stop,
    play,
    toggle_music,
)

# The arguments and keyword arguments for the current menu call.
menu_args = None
menu_kwargs = None

from renpy.exports.menuexports import (
    choice_for_skipping,
    display_menu,
    get_menu_args,
    menu,
    MenuEntry,
    predict_menu,
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
    check_permission,
    get_on_battery,
    get_sdl_dll,
    get_sdl_window_pointer,
    invoke_in_main_thread,
    invoke_in_thread,
    request_permission,
    variant,
    vibrate,
    open_url,
)

from renpy.exports.predictexports import (
    cache_pin,
    cache_unpin,
    expand_predict,
    predicting,
    start_predict_screen,
    start_predict,
    stop_predict_screen,
    stop_predict,
)

from renpy.exports.restartexports import (
    full_restart,
    get_autoreload,
    quit,
    reload_script,
    set_autoreload,
    utter_restart,
)

from renpy.exports.rollbackexports import (
    block_rollback,
    can_rollback,
    checkpoint,
    fix_rollback,
    get_identifier_checkpoints,
    get_roll_forward,
    in_fixed_rollback,
    in_rollback,
    retain_after_load,
    roll_forward_core,
    roll_forward_info,
    rollback,
    suspend_rollback,
)

from renpy.exports.sayexports import (
    count_dialogue_blocks,
    count_newly_seen_dialogue_blocks,
    count_seen_dialogue_blocks,
    curried_do_reshow_say,
    do_reshow_say,
    get_reshow_say,
    get_say_attributes,
    get_say_image_tag,
    get_side_image,
    last_say,
    LastSay,
    predict_say,
    reshow_say,
    say,
    scry_say,
    substitute,
    tag_quoting_dict,
    TagQuotingDict,
)

from renpy.exports.scriptexports import (
    get_all_labels,
    has_label,
    include_module,
    load_language,
    load_module,
    load_string,
    munged_filename,
)

from renpy.exports.statementexports import (
    call_screen,
    call,
    execute_default_statement,
    imagemap,
    jump,
    pause,
    return_statement,
    with_statement,
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
license = ""


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
