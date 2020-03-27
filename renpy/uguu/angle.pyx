from sdl2 cimport SDL_GL_LoadLibrary, SDL_GL_UnloadLibrary

cdef bint angle_loaded = False

import sys
import os

def load_gl():
    """
    Tells uguu to load the default GL or GLES implementation.
    """

    global angle_loaded

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

    if not angle_loaded:
        return

    for i in sys.path:
        dll = os.path.join(i, "libEGL.dll")
        if os.path.exists(dll):
            break
    else:
        return

    SDL_GL_UnloadLibrary()
    SDL_GL_LoadLibrary(dll)

    angle_loaded = True


