# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import *

import pygame_sdl2

code_to_unicode = {
    pygame_sdl2.K_UNKNOWN : "",
    pygame_sdl2.K_RETURN : "\n",
    pygame_sdl2.K_ESCAPE : "\e",
    pygame_sdl2.K_BACKSPACE : "\b",
    pygame_sdl2.K_TAB : "\t",
    pygame_sdl2.K_SPACE : " ",
    pygame_sdl2.K_EXCLAIM : "!",
    pygame_sdl2.K_QUOTEDBL : "\"",
    pygame_sdl2.K_HASH : "#",
    pygame_sdl2.K_PERCENT : "%",
    pygame_sdl2.K_DOLLAR : "$",
    pygame_sdl2.K_AMPERSAND : "&",
    pygame_sdl2.K_QUOTE : "'",
    pygame_sdl2.K_LEFTPAREN : "(",
    pygame_sdl2.K_RIGHTPAREN : ")",
    pygame_sdl2.K_ASTERISK : "*",
    pygame_sdl2.K_PLUS : "+",
    pygame_sdl2.K_COMMA : ",",
    pygame_sdl2.K_MINUS : "-",
    pygame_sdl2.K_PERIOD : ".",
    pygame_sdl2.K_SLASH : "/",
    pygame_sdl2.K_0 : "0",
    pygame_sdl2.K_1 : "1",
    pygame_sdl2.K_2 : "2",
    pygame_sdl2.K_3 : "3",
    pygame_sdl2.K_4 : "4",
    pygame_sdl2.K_5 : "5",
    pygame_sdl2.K_6 : "6",
    pygame_sdl2.K_7 : "7",
    pygame_sdl2.K_8 : "8",
    pygame_sdl2.K_9 : "9",
    pygame_sdl2.K_COLON : ":",
    pygame_sdl2.K_SEMICOLON : ";",
    pygame_sdl2.K_LESS : "<",
    pygame_sdl2.K_EQUALS : ":",
    pygame_sdl2.K_GREATER : ">",
    pygame_sdl2.K_QUESTION : "?",
    pygame_sdl2.K_AT : "@",
    pygame_sdl2.K_LEFTBRACKET : "[",
    pygame_sdl2.K_BACKSLASH : "\\",
    pygame_sdl2.K_RIGHTBRACKET : "]",
    pygame_sdl2.K_CARET : "^",
    pygame_sdl2.K_UNDERSCORE : "_",
    pygame_sdl2.K_BACKQUOTE : "`",
    pygame_sdl2.K_a : "a",
    pygame_sdl2.K_b : "b",
    pygame_sdl2.K_c : "c",
    pygame_sdl2.K_d : "d",
    pygame_sdl2.K_e : "e",
    pygame_sdl2.K_f : "f",
    pygame_sdl2.K_g : "g",
    pygame_sdl2.K_h : "h",
    pygame_sdl2.K_i : "i",
    pygame_sdl2.K_j : "j",
    pygame_sdl2.K_k : "k",
    pygame_sdl2.K_l : "l",
    pygame_sdl2.K_m : "m",
    pygame_sdl2.K_n : "n",
    pygame_sdl2.K_o : "o",
    pygame_sdl2.K_p : "p",
    pygame_sdl2.K_q : "q",
    pygame_sdl2.K_r : "r",
    pygame_sdl2.K_s : "s",
    pygame_sdl2.K_t : "t",
    pygame_sdl2.K_u : "u",
    pygame_sdl2.K_v : "v",
    pygame_sdl2.K_w : "w",
    pygame_sdl2.K_x : "x",
    pygame_sdl2.K_y : "y",
    pygame_sdl2.K_z : "z",
    pygame_sdl2.K_CAPSLOCK : "",
    pygame_sdl2.K_F1 : "",
    pygame_sdl2.K_F2 : "",
    pygame_sdl2.K_F3 : "",
    pygame_sdl2.K_F4 : "",
    pygame_sdl2.K_F5 : "",
    pygame_sdl2.K_F6 : "",
    pygame_sdl2.K_F7 : "",
    pygame_sdl2.K_F8 : "",
    pygame_sdl2.K_F9 : "",
    pygame_sdl2.K_F10 : "",
    pygame_sdl2.K_F11 : "",
    pygame_sdl2.K_F12 : "",
    pygame_sdl2.K_PRINTSCREEN : "",
    pygame_sdl2.K_SCROLLLOCK : "",
    pygame_sdl2.K_PAUSE : "",
    pygame_sdl2.K_INSERT : "",
    pygame_sdl2.K_HOME : "",
    pygame_sdl2.K_PAGEUP : "",
    pygame_sdl2.K_DELETE : "",
    pygame_sdl2.K_END : "",
    pygame_sdl2.K_PAGEDOWN : "",
    pygame_sdl2.K_RIGHT : "",
    pygame_sdl2.K_LEFT : "",
    pygame_sdl2.K_DOWN : "",
    pygame_sdl2.K_UP : "",
    pygame_sdl2.K_NUMLOCKCLEAR : "",
    pygame_sdl2.K_KP_DIVIDE : "/",
    pygame_sdl2.K_KP_MULTIPLY : "*",
    pygame_sdl2.K_KP_MINUS : "-",
    pygame_sdl2.K_KP_PLUS : "+",
    pygame_sdl2.K_KP_ENTER : "\n",
    pygame_sdl2.K_KP_1 : "1",
    pygame_sdl2.K_KP_2 : "2",
    pygame_sdl2.K_KP_3 : "3",
    pygame_sdl2.K_KP_4 : "4",
    pygame_sdl2.K_KP_5 : "5",
    pygame_sdl2.K_KP_6 : "6",
    pygame_sdl2.K_KP_7 : "7",
    pygame_sdl2.K_KP_8 : "8",
    pygame_sdl2.K_KP_9 : "9",
    pygame_sdl2.K_KP_0 : "0",
    pygame_sdl2.K_KP_PERIOD : ".",
    pygame_sdl2.K_APPLICATION : "",
    pygame_sdl2.K_POWER : "",
    pygame_sdl2.K_KP_EQUALS : ":",
    pygame_sdl2.K_F13 : "",
    pygame_sdl2.K_F14 : "",
    pygame_sdl2.K_F15 : "",
    pygame_sdl2.K_F16 : "",
    pygame_sdl2.K_F17 : "",
    pygame_sdl2.K_F18 : "",
    pygame_sdl2.K_F19 : "",
    pygame_sdl2.K_F20 : "",
    pygame_sdl2.K_F21 : "",
    pygame_sdl2.K_F22 : "",
    pygame_sdl2.K_F23 : "",
    pygame_sdl2.K_F24 : "",
    pygame_sdl2.K_EXECUTE : "",
    pygame_sdl2.K_HELP : "",
    pygame_sdl2.K_MENU : "",
    pygame_sdl2.K_SELECT : "",
    pygame_sdl2.K_STOP : "",
    pygame_sdl2.K_AGAIN : "",
    pygame_sdl2.K_UNDO : "",
    pygame_sdl2.K_CUT : "",
    pygame_sdl2.K_COPY : "",
    pygame_sdl2.K_PASTE : "",
    pygame_sdl2.K_FIND : "",
    pygame_sdl2.K_MUTE : "",
    pygame_sdl2.K_VOLUMEUP : "",
    pygame_sdl2.K_VOLUMEDOWN : "",
    pygame_sdl2.K_KP_COMMA : "",
    pygame_sdl2.K_KP_EQUALSAS400 : "",
    pygame_sdl2.K_ALTERASE : "",
    pygame_sdl2.K_SYSREQ : "",
    pygame_sdl2.K_CANCEL : "",
    pygame_sdl2.K_CLEAR : "",
    pygame_sdl2.K_PRIOR : "",
    pygame_sdl2.K_RETURN2 : "",
    pygame_sdl2.K_SEPARATOR : "",
    pygame_sdl2.K_OUT : "",
    pygame_sdl2.K_OPER : "",
    pygame_sdl2.K_CLEARAGAIN : "",
    pygame_sdl2.K_CRSEL : "",
    pygame_sdl2.K_EXSEL : "",
    pygame_sdl2.K_KP_00 : "",
    pygame_sdl2.K_KP_000 : "",
    pygame_sdl2.K_THOUSANDSSEPARATOR : "",
    pygame_sdl2.K_DECIMALSEPARATOR : "",
    pygame_sdl2.K_CURRENCYUNIT : "",
    pygame_sdl2.K_CURRENCYSUBUNIT : "",
    pygame_sdl2.K_KP_LEFTPAREN : "",
    pygame_sdl2.K_KP_RIGHTPAREN : "",
    pygame_sdl2.K_KP_LEFTBRACE : "",
    pygame_sdl2.K_KP_RIGHTBRACE : "",
    pygame_sdl2.K_KP_TAB : "",
    pygame_sdl2.K_KP_BACKSPACE : "",
    pygame_sdl2.K_KP_A : "",
    pygame_sdl2.K_KP_B : "",
    pygame_sdl2.K_KP_C : "",
    pygame_sdl2.K_KP_D : "",
    pygame_sdl2.K_KP_E : "",
    pygame_sdl2.K_KP_F : "",
    pygame_sdl2.K_KP_XOR : "",
    pygame_sdl2.K_KP_POWER : "",
    pygame_sdl2.K_KP_PERCENT : "",
    pygame_sdl2.K_KP_LESS : "",
    pygame_sdl2.K_KP_GREATER : "",
    pygame_sdl2.K_KP_AMPERSAND : "",
    pygame_sdl2.K_KP_DBLAMPERSAND : "",
    pygame_sdl2.K_KP_VERTICALBAR : "",
    pygame_sdl2.K_KP_DBLVERTICALBAR : "",
    pygame_sdl2.K_KP_COLON : "",
    pygame_sdl2.K_KP_HASH : "",
    pygame_sdl2.K_KP_SPACE : "",
    pygame_sdl2.K_KP_AT : "",
    pygame_sdl2.K_KP_EXCLAM : "",
    pygame_sdl2.K_KP_MEMSTORE : "",
    pygame_sdl2.K_KP_MEMRECALL : "",
    pygame_sdl2.K_KP_MEMCLEAR : "",
    pygame_sdl2.K_KP_MEMADD : "",
    pygame_sdl2.K_KP_MEMSUBTRACT : "",
    pygame_sdl2.K_KP_MEMMULTIPLY : "",
    pygame_sdl2.K_KP_MEMDIVIDE : "",
    pygame_sdl2.K_KP_PLUSMINUS : "",
    pygame_sdl2.K_KP_CLEAR : "",
    pygame_sdl2.K_KP_CLEARENTRY : "",
    pygame_sdl2.K_KP_BINARY : "",
    pygame_sdl2.K_KP_OCTAL : "",
    pygame_sdl2.K_KP_DECIMAL : "",
    pygame_sdl2.K_KP_HEXADECIMAL : "",
    pygame_sdl2.K_LCTRL : "",
    pygame_sdl2.K_LSHIFT : "",
    pygame_sdl2.K_LALT : "",
    pygame_sdl2.K_LGUI : "",
    pygame_sdl2.K_RCTRL : "",
    pygame_sdl2.K_RSHIFT : "",
    pygame_sdl2.K_RALT : "",
    pygame_sdl2.K_RGUI : "",
    pygame_sdl2.K_MODE : "",
    pygame_sdl2.K_AUDIONEXT : "",
    pygame_sdl2.K_AUDIOPREV : "",
    pygame_sdl2.K_AUDIOSTOP : "",
    pygame_sdl2.K_AUDIOPLAY : "",
    pygame_sdl2.K_AUDIOMUTE : "",
    pygame_sdl2.K_MEDIASELECT : "",
    pygame_sdl2.K_WWW : "",
    pygame_sdl2.K_MAIL : "",
    pygame_sdl2.K_CALCULATOR : "",
    pygame_sdl2.K_COMPUTER : "",
    pygame_sdl2.K_AC_SEARCH : "",
    pygame_sdl2.K_AC_HOME : "",
    pygame_sdl2.K_AC_BACK : "",
    pygame_sdl2.K_AC_FORWARD : "",
    pygame_sdl2.K_AC_STOP : "",
    pygame_sdl2.K_AC_REFRESH : "",
    pygame_sdl2.K_AC_BOOKMARKS : "",
    pygame_sdl2.K_BRIGHTNESSDOWN : "",
    pygame_sdl2.K_BRIGHTNESSUP : "",
    pygame_sdl2.K_DISPLAYSWITCH : "",
    pygame_sdl2.K_KBDILLUMTOGGLE : "",
    pygame_sdl2.K_KBDILLUMDOWN : "",
    pygame_sdl2.K_KBDILLUMUP : "",
    pygame_sdl2.K_EJECT : "",
    pygame_sdl2.K_SLEEP : "",
}

unicode_to_code = { }
for k, v in sorted(code_to_unicode.items()):
    if v and (v not in unicode_to_code):
        unicode_to_code[v] = k


def get_keycode(node, keysym):

    c = keysym.split("_")

    mods = 0

    while c:
        if c[0] == "shift":
            mods |= pygame_sdl2.KMOD_LSHIFT
            c.pop(0)
        elif c[0] == "ctrl":
            mods |= pygame_sdl2.KMOD_LCTRL
            c.pop(0)
        elif c[0] == "alt":
            mods |= pygame_sdl2.KMOD_LALT
            c.pop(0)
        elif c[0] == "meta":
            mods |= pygame_sdl2.KMOD_LMETA
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
        mods |= pygame_sdl2.KMOD_LSHIFT

    else:
        code = getattr(pygame_sdl2, "K_" + key, None)

        if code is None:
            raise Exception("Could not find keysym {!r} at {}:{}.".format(keysym, node.filename, node.linenumber))

        u = code_to_unicode.get(code, "")

        if not u:
            u = None
        elif ord(u) < 32:
            u = None

    return code, u, mods


def down(node, keysym):
    code, u, mods = get_keycode(node, keysym)

    if pygame_sdl2.key.text_input:
        pygame_sdl2.event.post(pygame_sdl2.event.Event(
            pygame_sdl2.KEYDOWN,
            unicode='',
            key=code,
            scancode=code,
            mod=mods,
            repeat=False,
            test=True))

        pygame_sdl2.event.post(pygame_sdl2.event.Event(
            pygame_sdl2.TEXTINPUT,
            text=u,
            test=True))

    else:

        pygame_sdl2.event.post(pygame_sdl2.event.Event(
            pygame_sdl2.KEYDOWN,
            unicode=u,
            key=code,
            scancode=code,
            mod=mods,
            repeat=False,
            test=True))


def up(node, keysym):
    code, _, mods = get_keycode(node, keysym)

    pygame_sdl2.event.post(pygame_sdl2.event.Event(
        pygame_sdl2.KEYUP,
        key=code,
        scancode=code,
        mod=mods,
        repeat=False,
        test=True))
