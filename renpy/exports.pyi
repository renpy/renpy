# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import annotations

# Export other undocumented API as renpy.renpy[.exports]
import renpy as renpy

import builtins
import ctypes
from typing import Any, BinaryIO, Callable, Final, Iterable, Iterator, Literal, Mapping, NoReturn, Sequence, TypeVar, overload
from renpy.display.core import absolute


# Public API imports

# renpy.pyanalysis
pure = renpy.pyanalysis.pure
const = renpy.pyanalysis.const
not_const = renpy.pyanalysis.not_const


# renpy.text
ParameterizedText = renpy.text.extras.ParameterizedText
filter_text_tags = renpy.text.extras.filter_text_tags
check_text_tags = renpy.text.extras.check_text_tags

register_sfont = renpy.text.font.register_sfont
register_mudgefont = renpy.text.font.register_mudgefont
register_bmfont = renpy.text.font.register_bmfont

BASELINE = renpy.text.text.BASELINE

language_tailor = renpy.text.textsupport.language_tailor
TEXT_TAG = renpy.text.textsupport.TAG
TEXT_TEXT = renpy.text.textsupport.TEXT
TEXT_PARAGRAPH = renpy.text.textsupport.PARAGRAPH
TEXT_DISPLAYABLE = renpy.text.textsupport.DISPLAYABLE


# renpy.display
Render = renpy.display.render.Render
render = renpy.display.render.render
IgnoreEvent = renpy.display.core.IgnoreEvent
redraw = renpy.display.render.redraw


# New context stuff
call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(renpy.game.call_in_new_context)
invoke_in_new_context = renpy.game.invoke_in_new_context
curried_invoke_in_new_context = renpy.curry.curry(renpy.game.invoke_in_new_context)
call_replay = renpy.game.call_replay


# Type declarations
_ImageName = str | tuple[str, ...]
_Character = renpy.character.ADVCharacter
_TransitionLike = renpy.display.transition.Transition | None
_DisplayableLike = renpy.display.core.Displayable | str
_AtTransform = Callable[..., renpy.display.core.Displayable]
_T = TypeVar("_T")


# renpy.compat
PY2: Literal[False]
open = builtins.open
basestring = (str, )
str = builtins.str
pystr = builtins.str
range = builtins.range
round = builtins.round
chr = builtins.chr
unicode = builtins.str
def bord(s: str | bytes, /) -> int: ...
def bchr(s: int, /) -> bytes: ...
def tobytes(s: str | bytes, /) -> bytes: ...


# Constants
bits: Final[int]
version_string: Final[str]
version_only: Final[str]
version_name: Final[str]
version_tuple: Final[tuple[str, str, str, str]]
license: Final[str]


# Platform constants
platform: Final[bool]
windows: Final[bool]
macintosh: Final[bool]
linux: Final[bool]
android: Final[bool]
ios: Final[bool]
emscripten: Final[bool]
mobile: Final[bool]


def roll_forward_info() -> Any | None:
    ...


def in_rollback() -> bool:
    ...


def can_rollback() -> bool:
    ...


def in_fixed_rollback() -> bool:
    ...


def checkpoint(data: Any | None = None, hard: bool = True) -> None:
    ...


def block_rollback() -> None:
    ...


def suspend_rollback(flag: bool) -> None:
    ...


def fix_rollback() -> None:
    ...


def retain_after_load() -> None:
    ...


def image(name: str, d: _DisplayableLike) -> None:
    ...


def copy_images(old: str, new: str) -> None:
    ...


def can_show(name: _ImageName, layer: str | None = None, tag: str | None = None) -> tuple[str, ...] | None:
    ...


def showing(name: _ImageName, layer: str | None = None) -> bool:
    ...


def get_showing_tags(layer: str = 'master', sort: bool = False) -> set[str] | list[str]:
    ...


def get_hidden_tags(layer: str = 'master') -> set[str]:
    ...


# Case `if_hidden` omitted
@overload
def get_attributes(tag: str, layer: str | None = None, if_hidden: None = None) -> tuple[str, ...] | None:
    ...


@overload
def get_attributes(tag: str, layer: str | None = None, if_hidden: _T = None) -> tuple[str, ...] | _T:
    ...


def clear_attributes(tag: str, layer: str | None = None) -> None:
    ...


def set_tag_attributes(name: _ImageName, layer: str | None = None) -> None:
    ...


def show(
    name: _ImageName,
    at_list: Sequence[_AtTransform] = [],
    layer: str | None = None,
    what: str | renpy.display.core.Displayable | None = None,
    zorder: int | None = None,
    tag: str | None = None,
    behind: Sequence[str] = []
) -> None:
    ...


def hide(name: _ImageName, layer: str | None = None) -> None:
    ...


def scene(layer: str = 'master') -> None:
    ...


def input(
    prompt: str,
    default: str = '',
    allow: str | None = None,
    exclude: str | None = '{}',
    length: int | None = None,
    pixel_width: int | None = None,
    screen: str = "input",
    mask: str | None = None,
    copypaste: bool = True,
    **kwargs: Any,
) -> str:
    ...


def choice_for_skipping() -> None:
    ...


def display_menu(items: Iterable[tuple[str, Any]], *, interact: bool = True, screen: str = "choice") -> Any | None:
    ...


def say(who: _Character | str | None, what: str, *args: Any, **kwargs: Any) -> None:
    ...


def pause(delay: float | None = None, *, hard: bool = False, predict: bool = False, modal: bool = True) -> bool:
    ...


def movie_cutscene(filename: str, delay: float | None = None, loops: int = 0, stop_music: bool = True) -> bool:
    ...


def with_statement(trans: _TransitionLike | Mapping[str | None, _TransitionLike], always: bool = False) -> bool:
    ...


def rollback(
    force: bool = False,
    checkpoints: int = 1,
    defer: bool = False,
    greedy: bool = True,
    label: str | None = None,
    abnormal: bool = True
) -> None:
    ...


def has_label(name: str | tuple[Any, ...]) -> bool:
    ...


def get_all_labels() -> set[str]:
    ...


def take_screenshot(scale: tuple[int, int] | None = None, background: bool = False) -> None:
    ...


def full_restart(
    transition: _TransitionLike | Literal[False] = False,
    label: str = "_invoke_main_menu",
    target: str = "_main_menu",
    save: bool = False
) -> NoReturn:
    ...


def reload_script() -> NoReturn:
    ...


def quit(relaunch: bool = False, status: int = 0, save: bool = False) -> NoReturn:
    ...


def jump(label: str) -> NoReturn:
    ...


def jump_out_of_context(label: str) -> NoReturn:
    ...


def call(label: str, *args: Any, from_current: bool = False, **kwargs: Any) -> NoReturn:
    ...


def return_statement(value: Any = None) -> NoReturn:
    ...


def warp_to_line(warp_spec: str) -> NoReturn:
    ...


def screenshot(filename: str) -> None:
    ...


def screenshot_to_bytes(size: tuple[int, int] | None) -> bytes:
    ...


def version(tuple: bool = False) -> str | tuple[str, str, str, str]:
    ...


def transition(trans: _TransitionLike, layer: str | None = None, always: bool = False, force: bool = False) -> None:
    ...


def get_transition(layer: str | None = None) -> _TransitionLike:
    ...


def clear_game_runtime() -> None:
    ...


def get_game_runtime() -> float:
    ...


def loadable(filename: str) -> bool:
    ...


def exists(filename: str) -> bool:
    ...


def restart_interaction() -> None:
    ...


def context() -> dict[str, Any]:
    ...


def context_nesting_level() -> int:
    ...


def get_filename_line() -> tuple[str, int]:
    ...


def log(msg: str) -> None:
    ...


def dynamic(*variables: str, **kwargs: Any) -> None:
    ...


def context_dynamic(*variables: str) -> None:
    ...


def seen_label(label: str) -> bool:
    ...


def mark_label_seen(label: str) -> None:
    ...


def mark_label_unseen(label: str) -> None:
    ...


def seen_audio(filename: str) -> bool:
    ...


def mark_audio_seen(filename: str) -> None:
    ...


def mark_audio_unseen(filename: str) -> None:
    ...


def seen_image(name: _ImageName) -> bool:
    ...


def mark_image_seen(name: _ImageName) -> None:
    ...


def mark_image_unseen(name: _ImageName) -> None:
    ...


def open_file(fn: str, encoding: str | Literal[False] | None = None) -> BinaryIO:
    ...


def image_size(im: str | renpy.display.im.ImageBase) -> tuple[int, int]:
    ...


def get_at_list(name: _ImageName, layer: str | None = None) -> list[_AtTransform] | None:
    ...


def show_layer_at(
        at_list: Iterable[_AtTransform],
        layer: str = 'master', reset: bool = True, camera: bool = False) -> None:
    ...


def free_memory() -> None:
    ...


def flush_cache_file(fn: str) -> None:
    ...


def quit_event() -> None:
    ...


def iconify() -> None:
    ...


def error(msg: str) -> None:
    ...


def timeout(seconds: float) -> None:
    ...


def end_interaction(value: Any | None) -> None:
    ...


def scry():
    ...
    # TODO


# Module loading stuff.
def load_module(name: str) -> None:
    ...


def load_string(s: str, filename: str = "<string>") -> str | tuple[Any, ...]:
    ...


def pop_call() -> None:
    ...


def call_stack_depth() -> int:
    ...


def shown_window() -> None:
    ...


class placement:
    xpos: int | float | absolute | None
    ypos: int | float | absolute | None
    xanchor: int | float | None
    yanchor: int | float | None
    xoffset: int
    yoffset: int
    subpixel: bool

    @property
    def pos(self) -> tuple[int | float | absolute | None, int | float | absolute | None]:
        ...

    @property
    def anchor(self) -> tuple[int | float | None, int | float | None]:
        ...

    @property
    def offset(self) -> tuple[int, int]:
        ...


def get_placement(d: renpy.display.core.Displayable) -> placement:
    ...


def get_image_bounds(
    tag: str,
    width: int | None = None,
    height: int | None = None,
    layer: str | None = None
) -> tuple[int | float, int | float, int | float, int | float]:
    ...


# User-Defined Displayable stuff.
class Displayable(renpy.display.core.Displayable, renpy.revertable.RevertableObject):
    pass


class Container(renpy.display.layout.Container, renpy.revertable.RevertableObject):
    _list_type = renpy.revertable.RevertableList


def start_predict(*args: str) -> None:
    ...


def stop_predict(*args: str) -> None:
    ...


def start_predict_screen(_screen_name: str, *args: Any, **kwargs: Any) -> None:
    ...


def stop_predict_screen(name: str) -> None:
    ...


def call_screen(
    _screen_name: str,
    *args: Any,
    _mode: str = "screen",
    _with_none: bool | None = None,
    **kwargs: Any
) -> Any:
    ...


def list_files(common: bool = False) -> list[str]:
    ...


def get_renderer_info():
    ...
    # TODO


def mode(mode: str) -> None:
    ...


def get_mode() -> str | None:
    ...


def notify(message: str) -> None:
    ...


def display_notify(message: str) -> None:
    ...


def variant(name: str) -> bool:
    ...


def vibrate(duration: float) -> None:
    ...


def get_say_attributes() -> tuple[str, ...] | None:
    ...


def get_side_image(
    prefix_tag: str,
    image_tag: str | None = None,
    not_showing: bool | None = None,
    layer: str | None = None
) -> tuple[str, ...] | None:
    ...


def get_physical_size() -> tuple[int, int]:
    ...


def set_physical_size(size: tuple[int, int]) -> None:
    ...


def reset_physical_size() -> None:
    ...


def fsencode(s: str | bytes, force: bool = False) -> bytes:
    ...


def fsdecode(s: str | bytes) -> str:
    ...


def get_image_load_log(age: float | None = None) -> Iterator[tuple[float, str, bool]]:
    ...


def end_replay() -> None:
    ...


def save_persistent() -> None:
    ...


def is_seen(ever: bool = True) -> bool:
    ...


def get_mouse_pos() -> tuple[int, int]:
    ...


def set_mouse_pos(x: int, y: int, duration: float = 0) -> None:
    ...


def set_autoreload(autoreload: bool) -> None:
    ...


def get_autoreload() -> bool:
    ...


def count_dialogue_blocks() -> int:
    ...


def count_seen_dialogue_blocks() -> int:
    ...


def count_newly_seen_dialogue_blocks() -> int:
    ...


def substitute(s: str, scope: Mapping[str, Any] | None = None, translate: bool = True) -> str:
    ...


def munge(name: str, filename: str | None = None) -> str:
    ...


def get_return_stack() -> list[str | tuple[Any, ...]]:
    ...


def set_return_stack(stack: list[str | tuple[Any, ...]]) -> None:
    ...


def invoke_in_thread(fn: Callable[..., None], *args: Any, **kwargs: Any) -> None:
    ...


def cancel_gesture() -> None:
    ...


def predicting() -> bool:
    ...


def add_layer(layer: str, above: str | None = None, below: str | None = None, menu_clear: bool = True) -> None:
    ...


def maximum_framerate(t: float) -> None:
    ...


def is_start_interact() -> bool:
    ...


def play(filename: str | None, channel: str | None = None, **kwargs: Any) -> None:
    ...


def get_refresh_rate(precision: float = 5) -> float:
    ...


def get_identifier_checkpoints(identifier: str) -> int | None:
    ...


def get_adjustment(bar_value: renpy.ui.BarValue) -> renpy.display.behavior.Adjustment:
    ...


def get_skipping() -> Literal["slow"] | Literal["fast"] | None:
    ...


def get_on_battery() -> bool:
    ...


def get_say_image_tag() -> str | None:
    ...


def is_skipping() -> bool:
    ...


def is_init_phase() -> bool:
    ...


def add_to_all_stores(name: str, value: Any) -> None:
    ...


def get_zorder_list(layer: str) -> list[tuple[str, int]]:
    ...


def change_zorder(layer: str, tag: str, zorder: int) -> None:
    ...


def get_sdl_dll() -> ctypes.CDLL | None:
    ...


def get_sdl_window_pointer() -> ctypes.c_void_p | None:
    ...


def is_mouse_visible() -> bool:
    ...


def get_mouse_name(interaction: bool = False) -> str:
    ...


def set_focus(screen: str, id: str, layer: str = "screens") -> None:
    ...


def check_permission(permission: str) -> bool:
    ...


def request_permission(permission: str) -> bool:
    ...
