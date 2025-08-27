# Copyright 2014 Patrick Dawson <pat@dw.is>
# Copyright 2014 Tom Rothamel <tom@rothamel.us>
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
from pygame_sdl2.surface cimport Surface

cdef class Window:
    # Allow weak references.
    cdef object __weakref__

    cdef SDL_Window *window
    cdef SDL_Surface *window_surface
    cdef public Surface surface

    # The OpenGL context corresponding to this window.
    cdef SDL_GLContext gl_context

    # The flags the window was created with.
    cdef Uint32 create_flags

cdef Window main_window = None
