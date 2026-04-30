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

from sdl2 cimport *
from renpy.pygame.display cimport main_window
from renpy.pygame.surface cimport Surface

def init():
    global active_cursor
    active_cursor = None

def quit():
    global active_cursor
    active_cursor = None

def reset():
    SDL_SetCursor(SDL_GetDefaultCursor())
    global active_cursor
    active_cursor = None

def get_pressed():
    cdef Uint32 state = SDL_GetMouseState(NULL, NULL)
    return (1 if state & SDL_BUTTON_LMASK else 0,
            1 if state & SDL_BUTTON_MMASK else 0,
            1 if state & SDL_BUTTON_RMASK else 0)

def get_pos():
    cdef int x, y
    SDL_GetMouseState(&x, &y)
    return (x, y)

def get_rel():
    cdef int x, y
    SDL_GetRelativeMouseState(&x, &y)
    return (x, y)

def set_pos(pos):
    (x, y) = pos
    SDL_WarpMouseInWindow(NULL, x, y)

def set_visible(visible):
    SDL_ShowCursor(1 if visible else 0)

    if SDL_GetWindowGrab(main_window.window) == SDL_ENABLE:
        SDL_SetRelativeMouseMode(SDL_FALSE if visible else SDL_TRUE)

def get_focused():
    return SDL_GetMouseFocus() != NULL

def set_cursor(size, hotspot, xormasks, andmasks):
    # Does anyone use this? SDL2 has much improved custom cursor support.
    pass

def get_cursor():
    return None

# The ColorCursor that is currently in use.
active_cursor = False

cdef class ColorCursor(object):

    cdef SDL_Cursor *cursor

    def __init__(self, Surface surface, x, y):
        self.cursor = SDL_CreateColorCursor(surface.surface, x, y)

    def __dealloc__(self):
        SDL_FreeCursor(self.cursor)

    def activate(self):
        global active_cursor
        if active_cursor is not self:
            active_cursor = self
            SDL_SetCursor(self.cursor)
