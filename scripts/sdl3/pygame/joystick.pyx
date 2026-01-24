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

from .sdl cimport *

from .error import error

def init():

    from .display import sdl_main_init

    sdl_main_init()

    if not SDL_InitSubSystem(SDL_INIT_JOYSTICK):
        raise error()

def quit(): # @ReservedAssignment
    SDL_QuitSubSystem(SDL_INIT_JOYSTICK)

def get_init():
    return SDL_WasInit(SDL_INIT_JOYSTICK) != 0


def get_joystick_ids():
    """
    Returns a list of joystic ids currently connected to the system.
    """

    cdef int i, n
    cdef list rv = []

    cdef const SDL_JoystickID *joysticks = SDL_GetJoysticks(&n)
    if joysticks != NULL:
        for i in range(n):
            rv.append(joysticks[i])

    return rv


def get_count():
    return len(get_joystick_ids())


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
            self.joystick = SDL_OpenJoystick(self.joyid)
            if self.joystick == NULL:
                raise error()

    def quit(self): # @ReservedAssignment
        if self.joystick != NULL:
            SDL_CloseJoystick(self.joystick)
            self.joystick = NULL

    def get_init(self):
        if self.joystick:
            return True
        else:
            return False

    def get_id(self):
        return self.joyid

    def get_name(self):
        cdef char *rv

        if self.joystick == NULL:
            raise error("joystick not initialized")

        rv = SDL_GetJoystickName(self.joystick)

        if rv:
            return rv.decode("utf-8")
        else:
            return None

    def get_numaxes(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_GetNumJoystickAxes(self.joystick)

    def get_numballs(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_GetNumJoystickBalls(self.joystick)

    def get_numbuttons(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_GetNumJoystickButtons(self.joystick)

    def get_numhats(self):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_GetNumJoystickHats(self.joystick)

    def get_axis(self, axis_number):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_GetJoystickAxis(self.joystick, axis_number) / 32768.0

    def get_ball(self, ball_number):
        cdef int dx, dy

        if self.joystick == NULL:
            raise error("joystick not initialized")

        if SDL_GetJoystickBall(self.joystick, ball_number, &dx, &dy) == 0:
            return (dx, dy)
        else:
            raise error()

    def get_button(self, button):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        return SDL_GetJoystickButton(self.joystick, button)

    def get_hat(self, hat_number):
        if self.joystick == NULL:
            raise error("joystick not initialized")

        state = SDL_GetJoystickHat(self.joystick, hat_number)
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
