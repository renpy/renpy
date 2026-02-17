# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from libcpp cimport bool

from .sdl cimport *
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from .display cimport Window, main_window
from .rect cimport to_sdl_rect

from .error import error


cdef class KeyboardState:
    # Allow weak references.
    cdef object __weakref__

    cdef uint8_t *data
    cdef int numkeys

    def __cinit__(self):
        self.data = NULL

    def __dealloc__(self):
        if self.data != NULL:
            free(self.data)

    def __init__(self):
        cdef const bool *state = SDL_GetKeyboardState(&self.numkeys)
        if state == NULL:
            raise error()

        # Take a snapshot of the current state, rather than saving the pointer.
        self.data = <uint8_t*>malloc(self.numkeys)
        memcpy(self.data, state, self.numkeys)

    def __getitem__(self, int key):
        if <int> SDLK_DELETE < key < <int> SDLK_CAPSLOCK:
            raise IndexError("Out of range.")

        cdef int sc = <int>SDL_GetScancodeFromKey(key, NULL)
        if sc > self.numkeys:
            raise IndexError("Out of range.")

        return self.data[sc]


def get_focused():
    return SDL_GetKeyboardFocus() != NULL

def get_pressed():
    """ No longer returns a tuple. Use the returned object to check for
        individual keys, but don't loop through it. """

    return KeyboardState()

def get_mods():
    return SDL_GetModState()

def set_mods(state):
    SDL_SetModState(state)

def set_repeat(delay=0, interval=0):
    # Not possible with SDL2.
    pass

def get_repeat():
    # Not possible with SDL2.
    return (0,0)

def name(key):
    return SDL_GetKeyName(key)

text_input = False

def start_text_input():
    global text_input
    text_input = True

    if SDL_HasScreenKeyboardSupport():
        SDL_StartTextInput(main_window.window)

def stop_text_input():
    global text_input
    text_input = False

    if SDL_HasScreenKeyboardSupport():
        SDL_StopTextInput(main_window.window)

def set_text_input_rect(rect):
    cdef SDL_Rect sdl_rect

    if rect is not None:
        to_sdl_rect(rect, &sdl_rect)
        SDL_SetTextInputArea(main_window.window, &sdl_rect, 0)
    else:
        SDL_SetTextInputArea(main_window.window, NULL, 0)

def has_screen_keyboard_support():
    return SDL_HasScreenKeyboardSupport()

def is_screen_keyboard_shown(Window window=None):
    if window is None:
        window = main_window

    return SDL_ScreenKeyboardShown(window.window)
