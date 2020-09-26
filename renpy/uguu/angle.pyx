from sdl2 cimport SDL_GL_LoadLibrary, SDL_GL_UnloadLibrary

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
        return

    SDL_GL_UnloadLibrary()
    SDL_GL_LoadLibrary(NULL)

    angle_loaded = False

def load_angle():
    """
    Tells uguu to load the ANGLE implementation.
    """

    global angle_loaded

    if angle_loaded:
        return

    for i in sys.path:
        dll = os.path.join(i, "libEGL.dll")
        if os.path.exists(dll):
            break
    else:
        renpy.display.log.write("Could not find angle DLL.")
        return

    renpy.display.log.write("Using ANGLE DLL: %s", dll)

    SDL_GL_UnloadLibrary()
    SDL_GL_LoadLibrary(dll)

    angle_loaded = True


