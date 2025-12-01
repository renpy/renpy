# Copyright 2014 Tom Rothamel <tom@rothamel.us>
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

from pygame.sdl cimport *

cdef Uint32 map_color(SDL_Surface *surface, color) except? 0xaabbccdd
cdef object get_color(Uint32 pixel, SDL_Surface *surface)
cdef to_sdl_color(color, SDL_Color *out)

cdef class Color:
    # Allow weak references.
    cdef object __weakref__

    cdef public Uint8 r, g, b, a
    cdef uint8_t length

    cdef from_rgba(self, Uint8 r, Uint8 g, Uint8 b, Uint8 a)
    cdef from_name(self, c)
    cdef from_hex(self, c)
