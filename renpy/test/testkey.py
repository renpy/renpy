# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import renpy.pygame as pygame

import renpy
from renpy.test.testast import Node

code_to_unicode = {
    pygame.K_UNKNOWN: "",
    pygame.K_RETURN: "\n",
    pygame.K_ESCAPE: "",
    pygame.K_BACKSPACE: "\b",
    pygame.K_TAB: "\t",
    pygame.K_SPACE: " ",
    pygame.K_EXCLAIM: "!",
    pygame.K_QUOTEDBL: '"',
    pygame.K_HASH: "#",
    pygame.K_PERCENT: "%",
    pygame.K_DOLLAR: "$",
    pygame.K_AMPERSAND: "&",
    pygame.K_QUOTE: "'",
    pygame.K_LEFTPAREN: "(",
    pygame.K_RIGHTPAREN: ")",
    pygame.K_ASTERISK: "*",
    pygame.K_PLUS: "+",
    pygame.K_COMMA: ",",
    pygame.K_MINUS: "-",
    pygame.K_PERIOD: ".",
    pygame.K_SLASH: "/",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_COLON: ":",
    pygame.K_SEMICOLON: ";",
    pygame.K_LESS: "<",
    pygame.K_EQUALS: ":",
    pygame.K_GREATER: ">",
    pygame.K_QUESTION: "?",
    pygame.K_AT: "@",
    pygame.K_LEFTBRACKET: "[",
    pygame.K_BACKSLASH: "\\",
    pygame.K_RIGHTBRACKET: "]",
    pygame.K_CARET: "^",
    pygame.K_UNDERSCORE: "_",
    pygame.K_BACKQUOTE: "`",
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",
    pygame.K_CAPSLOCK: "",
    pygame.K_F1: "",
    pygame.K_F2: "",
    pygame.K_F3: "",
    pygame.K_F4: "",
    pygame.K_F5: "",
    pygame.K_F6: "",
    pygame.K_F7: "",
    pygame.K_F8: "",
    pygame.K_F9: "",
    pygame.K_F10: "",
    pygame.K_F11: "",
    pygame.K_F12: "",
    pygame.K_PRINTSCREEN: "",
    pygame.K_SCROLLLOCK: "",
    pygame.K_PAUSE: "",
    pygame.K_INSERT: "",
    pygame.K_HOME: "",
    pygame.K_PAGEUP: "",
    pygame.K_DELETE: "",
    pygame.K_END: "",
    pygame.K_PAGEDOWN: "",
    pygame.K_RIGHT: "",
    pygame.K_LEFT: "",
    pygame.K_DOWN: "",
    pygame.K_UP: "",
    pygame.K_NUMLOCKCLEAR: "",
    pygame.K_KP_DIVIDE: "/",
    pygame.K_KP_MULTIPLY: "*",
    pygame.K_KP_MINUS: "-",
    pygame.K_KP_PLUS: "+",
    pygame.K_KP_ENTER: "\n",
    pygame.K_KP_1: "1",
    pygame.K_KP_2: "2",
    pygame.K_KP_3: "3",
    pygame.K_KP_4: "4",
    pygame.K_KP_5: "5",
    pygame.K_KP_6: "6",
    pygame.K_KP_7: "7",
    pygame.K_KP_8: "8",
    pygame.K_KP_9: "9",
    pygame.K_KP_0: "0",
    pygame.K_KP_PERIOD: ".",
    pygame.K_APPLICATION: "",
    pygame.K_POWER: "",
    pygame.K_KP_EQUALS: ":",
    pygame.K_F13: "",
    pygame.K_F14: "",
    pygame.K_F15: "",
    pygame.K_F16: "",
    pygame.K_F17: "",
    pygame.K_F18: "",
    pygame.K_F19: "",
    pygame.K_F20: "",
    pygame.K_F21: "",
    pygame.K_F22: "",
    pygame.K_F23: "",
    pygame.K_F24: "",
    pygame.K_EXECUTE: "",
    pygame.K_HELP: "",
    pygame.K_MENU: "",
    pygame.K_SELECT: "",
    pygame.K_STOP: "",
    pygame.K_AGAIN: "",
    pygame.K_UNDO: "",
    pygame.K_CUT: "",
    pygame.K_COPY: "",
    pygame.K_PASTE: "",
    pygame.K_FIND: "",
    pygame.K_MUTE: "",
    pygame.K_VOLUMEUP: "",
    pygame.K_VOLUMEDOWN: "",
    pygame.K_KP_COMMA: "",
    pygame.K_KP_EQUALSAS400: "",
    pygame.K_ALTERASE: "",
    pygame.K_SYSREQ: "",
    pygame.K_CANCEL: "",
    pygame.K_CLEAR: "",
    pygame.K_PRIOR: "",
    pygame.K_RETURN2: "",
    pygame.K_SEPARATOR: "",
    pygame.K_OUT: "",
    pygame.K_OPER: "",
    pygame.K_CLEARAGAIN: "",
    pygame.K_CRSEL: "",
    pygame.K_EXSEL: "",
    pygame.K_KP_00: "",
    pygame.K_KP_000: "",
    pygame.K_THOUSANDSSEPARATOR: "",
    pygame.K_DECIMALSEPARATOR: "",
    pygame.K_CURRENCYUNIT: "",
    pygame.K_CURRENCYSUBUNIT: "",
    pygame.K_KP_LEFTPAREN: "",
    pygame.K_KP_RIGHTPAREN: "",
    pygame.K_KP_LEFTBRACE: "",
    pygame.K_KP_RIGHTBRACE: "",
    pygame.K_KP_TAB: "",
    pygame.K_KP_BACKSPACE: "",
    pygame.K_KP_A: "",
    pygame.K_KP_B: "",
    pygame.K_KP_C: "",
    pygame.K_KP_D: "",
    pygame.K_KP_E: "",
    pygame.K_KP_F: "",
    pygame.K_KP_XOR: "",
    pygame.K_KP_POWER: "",
    pygame.K_KP_PERCENT: "",
    pygame.K_KP_LESS: "",
    pygame.K_KP_GREATER: "",
    pygame.K_KP_AMPERSAND: "",
    pygame.K_KP_DBLAMPERSAND: "",
    pygame.K_KP_VERTICALBAR: "",
    pygame.K_KP_DBLVERTICALBAR: "",
    pygame.K_KP_COLON: "",
    pygame.K_KP_HASH: "",
    pygame.K_KP_SPACE: "",
    pygame.K_KP_AT: "",
    pygame.K_KP_EXCLAM: "",
    pygame.K_KP_MEMSTORE: "",
    pygame.K_KP_MEMRECALL: "",
    pygame.K_KP_MEMCLEAR: "",
    pygame.K_KP_MEMADD: "",
    pygame.K_KP_MEMSUBTRACT: "",
    pygame.K_KP_MEMMULTIPLY: "",
    pygame.K_KP_MEMDIVIDE: "",
    pygame.K_KP_PLUSMINUS: "",
    pygame.K_KP_CLEAR: "",
    pygame.K_KP_CLEARENTRY: "",
    pygame.K_KP_BINARY: "",
    pygame.K_KP_OCTAL: "",
    pygame.K_KP_DECIMAL: "",
    pygame.K_KP_HEXADECIMAL: "",
    pygame.K_LCTRL: "",
    pygame.K_LSHIFT: "",
    pygame.K_LALT: "",
    pygame.K_LGUI: "",
    pygame.K_RCTRL: "",
    pygame.K_RSHIFT: "",
    pygame.K_RALT: "",
    pygame.K_RGUI: "",
    pygame.K_MODE: "",
    pygame.K_AUDIONEXT: "",
    pygame.K_AUDIOPREV: "",
    pygame.K_AUDIOSTOP: "",
    pygame.K_AUDIOPLAY: "",
    pygame.K_AUDIOMUTE: "",
    pygame.K_MEDIASELECT: "",
    pygame.K_WWW: "",
    pygame.K_MAIL: "",
    pygame.K_CALCULATOR: "",
    pygame.K_COMPUTER: "",
    pygame.K_AC_SEARCH: "",
    pygame.K_AC_HOME: "",
    pygame.K_AC_BACK: "",
    pygame.K_AC_FORWARD: "",
    pygame.K_AC_STOP: "",
    pygame.K_AC_REFRESH: "",
    pygame.K_AC_BOOKMARKS: "",
    pygame.K_BRIGHTNESSDOWN: "",
    pygame.K_BRIGHTNESSUP: "",
    pygame.K_DISPLAYSWITCH: "",
    pygame.K_KBDILLUMTOGGLE: "",
    pygame.K_KBDILLUMDOWN: "",
    pygame.K_KBDILLUMUP: "",
    pygame.K_EJECT: "",
    pygame.K_SLEEP: "",
}

unicode_to_code = {}
for k, v in sorted(code_to_unicode.items()):
    if v and (v not in unicode_to_code):
        unicode_to_code[v] = k


def get_keycode(node: Node, keysym: str) -> tuple[int, str | None, int]:
    """
    Returns the keycode, unicode character, and modifier flags for a given keysym.
    If the keysym is not recognized, an exception is raised.
    """

    c = keysym.split("_")

    mods = 0

    while c:
        if c[0] == "shift":
            mods |= pygame.KMOD_LSHIFT
            c.pop(0)
        elif c[0] == "ctrl":
            mods |= pygame.KMOD_LCTRL
            c.pop(0)
        elif c[0] == "alt":
            mods |= pygame.KMOD_LALT
            c.pop(0)
        elif c[0] == "meta":
            mods |= pygame.KMOD_LMETA
            c.pop(0)
        else:
            break

    key = "_".join(c)

    if key in unicode_to_code:
        if ord(key) >= 32:
            u = key
        else:
            u = None

        code = unicode_to_code[key]

    elif key.lower() in unicode_to_code:
        u = key
        code = unicode_to_code[key.lower()]
        mods |= pygame.KMOD_LSHIFT

    else:
        code = getattr(pygame, key, None)

        if code is None:
            raise Exception("Could not find keysym {!r} at {}:{}.".format(keysym, node.filename, node.linenumber))

        u = code_to_unicode.get(code, "")

        if not u:
            u = None
        elif ord(u) < 32:
            u = None

    return code, u, mods


def down(node: Node, keysym: str) -> None:
    """
    Posts a KEYDOWN event for the given keysym, which is a string like "ctrl_K_a".
    """
    code, u, mods = get_keycode(node, keysym)

    if pygame.key.text_input:
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, unicode="", key=code, scancode=code, mod=mods, repeat=False, test=True
            )
        )

        pygame.event.post(pygame.event.Event(pygame.TEXTINPUT, text=u, test=True))

    else:
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, unicode=u, key=code, scancode=code, mod=mods, repeat=False, test=True
            )
        )


def up(node: Node, keysym: str) -> None:
    """
    Posts a KEYUP event for the given keysym, which is a string like "ctrl_K_a".
    """
    code, _, mods = get_keycode(node, keysym)

    pygame.event.post(
        pygame.event.Event(pygame.KEYUP, key=code, scancode=code, mod=mods, repeat=False, test=True)
    )


def queue_keysym(node: Node, name: str) -> None:
    """
    Trigger a keysym event, which is a string like "ctrl_K_a" or "mouseup_1"
    or an event name in `config.keymap` like "skip" or "dismiss".
    """

    if name in renpy.config.keymap:
        renpy.exports.queue_event(name)
        return

    elif "pad_" in name:
        parts = name.split("_")

        control = parts[-2]
        state = parts[-1]
        repeat = parts[0] == "repeat"

        renpy.display.controller.post_event(control, state, repeat)
        return

    down(node, name)
    up(node, name)

#         keysym = config.keymap[keysym][0]
#     return keysym
