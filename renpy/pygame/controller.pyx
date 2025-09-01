# Copyright 2015 Tom Rothamel <tom@rothamel.us>
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
from renpy.pygame.rwobject cimport to_rwops
from renpy.pygame import register_init, register_quit

@register_init
def init():
    """
    Initializes game controller support.
    """

    renpy.pygame.display.sdl_main_init()

    if SDL_InitSubSystem(SDL_INIT_GAMECONTROLLER):
        raise error()

@register_quit
def quit(): # @ReservedAssignment
    """
    Shuts down game controller support.
    """

    SDL_QuitSubSystem(SDL_INIT_GAMECONTROLLER)

def get_init():
    """
    Returns true if game controller support has been initialized.
    """

    return SDL_WasInit(SDL_INIT_GAMECONTROLLER) != 0

def get_count():
    """
    Returns the number of joysticks and game controllers connected to the
    system. This is one more than the maximum index that can be passed to
    Controller. While every game controller is a joystick, not every joystick
    is a game controller. To check that index `i` corresponds to a game
    controller, use code such as::

        if renpy.pygame.controller.Controller(i).is_controller():
            ...
    """

    return SDL_NumJoysticks()


def add_mapping(mapping):
    """
    Adds a game controller mapping from the string in `mapping`.
    """

    if SDL_GameControllerAddMapping(mapping) == -1:
        raise error()

def add_mappings(mapping_file):
    """
    Adds game controller mappings from `mapping_file`, which can be a string
    filename or a file-like object. This file should be gamecontrollerdb.txt,
    downloaded from:

    https://raw.githubusercontent.com/gabomdq/SDL_GameControllerDB/master/gamecontrollerdb.txt

    This should be called before creating a Controller object. It can be called
    multiple times to add multiple database files.
    """

    cdef SDL_RWops *rwops = to_rwops(mapping_file)

    if SDL_GameControllerAddMappingsFromRW(rwops, 1) == -1:
        raise error()

def get_axis_from_string(name):
    """
    Returns the axis number of the controller axis with `name`, or
    pygame.CONTROLLER_AXIS_INVALID if `name` is not known.
    """

    if not isinstance(name, bytes):
        name = name.encode("utf-8")

    return SDL_GameControllerGetAxisFromString(name)

def get_button_from_string(name):
    """
    Returns the button number of the controller button with `name`, or
    pygame.CONTROLLER_BUTTON_INVALID if `name` is not known.
    """

    if not isinstance(name, bytes):
        name = name.encode("utf-8")

    return SDL_GameControllerGetButtonFromString(name)

def get_string_for_axis(axis):
    """
    Returns a string describing the controller axis `axis`, which must be
    an integer. Returns None if the axis is not known.
    """

    cdef const char *rv = SDL_GameControllerGetStringForAxis(axis)

    if rv != NULL:
        return rv.decode("utf-8")
    else:
        return None

def get_string_for_button(button):
    """
    Returns a string describing the controller button `button`, which must be
    an integer. Returns None if the button is not known.
    """

    cdef const char *rv = SDL_GameControllerGetStringForButton(button)

    if rv != NULL:
        return rv.decode("utf-8")
    else:
        return None


cdef class Controller:
    # Allow weak references.
    cdef object __weakref__

    cdef SDL_GameController *controller
    cdef int index
    cdef public int instance_id

    def __cinit__(self):
        self.controller = NULL

    def __init__(self, index):
        """
        Represents a game controller object corresponding to the joystick
        with `index`.
        """

        self.index = index

    def init(self):
        """
        Opens the game controller, causing it to begin sending events.
        """

        self.instance_id = SDL_JoystickGetDeviceInstanceID(self.index)

        if self.controller == NULL:
            self.controller = SDL_GameControllerOpen(self.index)
            if self.controller == NULL:
                raise error()

    def quit(self): # @ReservedAssignment
        """
        Closes the game controller, preventing it from sending events.
        """

        if self.controller and SDL_GameControllerGetAttached(self.controller):
            SDL_GameControllerClose(self.controller)
            self.controller = NULL

    def get_init(self):
        """
        Returns true if the controller has been initialized, false otherwise.
        """

        if self.controller:
            return True
        else:
            return False

    def get_axis(self, axis):
        """
        Returns the value of `axis`, which is one of the pygame.CONTROLLER_AXIS
        constants.

        Axes return values from -32768 to 32678, triggers return 0 to 32768. 0 is
        returned on failure.
        """

        if self.controller == NULL:
            raise error("controller not initialized.")

        return SDL_GameControllerGetAxis(self.controller, axis)


    def get_button(self, button):
        """
        Returns the value of `button`, which must be one of the pygame.CONTROLLER_BUTTON
        constants.

        Returns 1 if the button is pressed, 0 if not or the button does not exist.
        """

        if self.controller == NULL:
            raise error("controller not initialized.")

        return SDL_GameControllerGetButton(self.controller, button)

    def get_name(self):
        """
        Returns an implementation-dependent name for this game controller,
        or None if no name could be found.
        """

        cdef const char *rv = SDL_GameControllerNameForIndex(self.index)

        if rv == NULL:
            return None

        return rv.decode("utf-8")

    def is_controller(self):
        """
        Returns true if this Controller object corresponds to a supported
        game controller, or False otherwise.
        """

        return SDL_IsGameController(self.index)

    def get_guid_string(self):
        """
        Returns the guid string corresponding to this controller.
        """

        cdef SDL_JoystickGUID guid
        cdef char s[33]

        guid = SDL_JoystickGetDeviceGUID(self.index)
        SDL_JoystickGetGUIDString(guid, s, 33)

        return s.decode("utf-8")
