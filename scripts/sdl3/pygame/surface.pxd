# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2014 Patrick Dawson
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


from pygame.sdl cimport SDL_Surface

cdef class Surface:
    # Allow weak references.
    cdef object __weakref__

    # The SDL surface that corresponds to this surface.
    cdef SDL_Surface* surface

    # True if we own our surface. False if some other Surface owns our
    # surface.
    cdef bint owns_surface

    # True if this surface is owned by a window.
    cdef bint window_surface

    # A list of locks involving the surface.
    cdef object locklist

    # If this surface is a subsurface, the surface this surface is a subsurface
    # of.
    cdef Surface parent

    # If this surface has no parent, self. Otherwise, self.parent.root. The
    # ultimate parent.
    cdef Surface root

    # The offset of this surface within its parent.
    cdef int offset_x
    cdef int offset_y

    # If not None, a function that returns the window flags.
    cdef object get_window_flags

    cdef void take_surface(self, SDL_Surface *)

    cdef bint has_alpha

cdef SDL_Surface *PySurface_AsSurface(object surface)
