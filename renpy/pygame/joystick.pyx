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

import renpy.pygame
from renpy.pygame.error import error
from renpy.pygame import register_init, register_quit

@register_init
def init():
    renpy.pygame.display.sdl_main_init()

    if SDL_InitSubSystem(SDL_INIT_JOYSTICK):
        raise error()

@register_quit
def quit(): # @ReservedAssignment
    SDL_QuitSubSystem(SDL_INIT_JOYSTICK)

def get_init():
    return SDL_WasInit(SDL_INIT_JOYSTICK) != 0

def get_count():
    return SDL_NumJoysticks()


cdef class Joystick:
    # Allow weak references.
    cdef object __weakref__

    cdef SDL_Joystick *joystick
    cdef int joyid

    def __cinit__(self):
        self.joystick = NULL

    def __init__(self, id):
        self.joyid = id

    def init(self):
        if self.joystick == NULL:
            self.joystick = SDL_JoystickOpen(self.joyid)
            if self.joystick == NULL:
                raise error()

    def quit(self): # @ReservedAssignment
        if self.joystick != NULL:
            SDL_JoystickClose(self.joystick)
            self.joystick = NULL

    def get_init(self):
        if self.joystick:
            return True
        else:
            return False

    def get_id(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickInstanceID(self.joystick)

    def get_name(self):
        cdef char *rv

        if self.joystick == NULL:
            raise error("joystick not initialized")

        rv = SDL_JoystickName(self.joystick)

        if rv:
            return rv.decode("utf-8")
        else:
            return None

    def get_numaxes(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickNumAxes(self.joystick)

    def get_numballs(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickNumBalls(self.joystick)

    def get_numbuttons(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickNumButtons(self.joystick)

    def get_numhats(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickNumHats(self.joystick)

    def get_axis(self, axis_number):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickGetAxis(self.joystick, axis_number) / 32768.0

    def get_ball(self, ball_number):
        cdef int dx, dy

        if self.joystick == NULL:
            raise error("joystick not initialized")

        if SDL_JoystickGetBall(self.joystick, ball_number, &dx, &dy) == 0:
            return (dx, dy)
        else:
            raise error()

    def get_button(self, button):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_JoystickGetButton(self.joystick, button) == 1

    def get_hat(self, hat_number):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        state = SDL_JoystickGetHat(self.joystick, hat_number)
        hx = hy = 0
        if state & SDL_HAT_LEFT:
            hx = -1
        elif state & SDL_HAT_RIGHT:
            hx = 1

        if state & SDL_HAT_UP:
            hy = 1
        elif state & SDL_HAT_DOWN:
            hy = -1

        return (hx, hy)
