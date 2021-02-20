from sdl2 cimport SDL_GL_LoadLibrary, SDL_GL_UnloadLibrary, SDL_GetError

cdef bint angle_loaded = False

import sys
import os
import renpy

def load_gl():
    """
    Tells uguu to load the default GL or GLES implementation.
    """

    global angle_loaded

    renpy.display.log.write("Using GL DLL.")

    if not angle_loaded:
        return True

    angle_loaded = False

    SDL_GL_UnloadLibrary()
    if SDL_GL_LoadLibrary(NULL):
        renpy.display.log.write("Loading GL DLL: %s", SDL_GetError())
        return False

    return True



def load_angle():
    """
    Tells uguu to load the ANGLE implementation.
    """

    global angle_loaded

    if angle_loaded:
        return True

    for i in sys.path:
        dll = os.path.join(i, "libEGL.dll")
        if os.path.exists(dll):
            break
    else:
        renpy.display.log.write("Could not find angle DLL.")
        return False

    renpy.display.log.write("Using ANGLE DLL: %s", dll)

    angle_loaded = True

    SDL_GL_UnloadLibrary()
    if SDL_GL_LoadLibrary(dll):
        renpy.display.log.write("Loading ANGLE DLL: %s", SDL_GetError())
        return False

    return True




