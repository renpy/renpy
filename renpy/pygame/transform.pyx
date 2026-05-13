# Copyright 2014 Patrick Dawson <pat@dw.is>
#                Tom Rothamel <tom@rothamel.us>
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
from sdl2_gfx cimport *
from renpy.pygame.color cimport map_color
from renpy.pygame.surface cimport *
from renpy.pygame.error import error


def _diff(Surface dest, Surface a, Surface b, same_color, different_color):
    """
    This is Ren'Py specific, and implements a subset of the pygame threshold API.

    This computes the differences in a and b. Pixels that are the same in a are set to same_color in
    dest, and pixels that are different are set to different_color.

    dest, a, ab and b must all be the same size and format.

    same_color and different_color may be any color accepted by map_color().

    Returns the count of different pixels.
    """

    if dest.get_size() != a.get_size() or dest.get_size() != b.get_size():
        raise error("Surface sizes do not match.")

    cdef SDL_Surface *dest_surf = dest.surface
    cdef SDL_Surface *a_surf = a.surface
    cdef SDL_Surface *b_surf = b.surface

    cdef Uint32 same_c = map_color(dest_surf, same_color)
    cdef Uint32 diff_c = map_color(dest_surf, different_color)

    cdef Uint32 *a_pixel
    cdef Uint32 *a_end

    cdef Uint32 *b_pixel
    cdef Uint32 *dest_pixel

    cdef int y

    cdef int diff_count = 0

    with nogil:
        for y in range(0, a_surf.h):

            a_pixel = <Uint32 *> ((<Uint8 *> a_surf.pixels) + y * a_surf.pitch)
            b_pixel = <Uint32 *> ((<Uint8 *> b_surf.pixels) + y * b_surf.pitch)
            dest_pixel = <Uint32 *> ((<Uint8 *> dest_surf.pixels) + y * dest_surf.pitch)

            a_end = a_pixel + a_surf.w

            while a_pixel < a_end:
                if a_pixel[0] == b_pixel[0]:
                    dest_pixel[0] = same_c
                else:
                    dest_pixel[0] = diff_c
                    diff_count += 1

                a_pixel += 1
                b_pixel += 1
                dest_pixel += 1

    return diff_count

def flip(Surface surface, bint xbool, bint ybool):

    cdef Surface rv = Surface(surface.get_size(), surface.get_flags(), surface)
    cdef SDL_Surface *src = surface.surface
    cdef SDL_Surface *dest = rv.surface

    cdef Uint32 *src_pixel
    cdef Uint32 *src_end

    cdef Uint32 *dest_pixel
    cdef int dest_delta

    cdef int y

    with nogil:
        for y in range(0, src.h):

            src_pixel = <Uint32 *> ((<Uint8 *> src.pixels) + y * src.pitch)
            src_end = src_pixel + src.w

            if ybool:
                dest_pixel = <Uint32 *> ((<Uint8 *> dest.pixels) + (dest.h - y - 1) * dest.pitch)
            else:
                dest_pixel = <Uint32 *> ((<Uint8 *> dest.pixels) + y * dest.pitch)

            if xbool:
                dest_pixel += (src.w - 1)
                dest_delta = -1
            else:
                dest_delta = 1

            while src_pixel < src_end:
                dest_pixel[0] = src_pixel[0]
                src_pixel += 1
                dest_pixel += dest_delta

    return rv


def scale(Surface surface, size, Surface DestSurface=None):
    cdef Surface surf_out
    cdef int err = -1

    if DestSurface == None:
        surf_out = Surface(size, 0, surface)
    else:
        surf_out = DestSurface

    with nogil:
        SDL_SetSurfaceBlendMode(surface.surface, SDL_BLENDMODE_NONE)
        err = SDL_UpperBlitScaled(surface.surface, NULL, surf_out.surface, NULL)

    if err != 0:
        raise error()

    return surf_out

def rotate(Surface surface, angle):
    # rotateSurface90Degrees always returns NULL without setting an error??
    # cdef SDL_Surface *rsurf
    # if angle % 90 == 0:
    #     rsurf = rotateSurface90Degrees(surface.surface, angle / 90)
    #     if rsurf == NULL:
    #        raise error()
    return rotozoom(surface, angle, 1.0, SMOOTHING_OFF)

def rotozoom(Surface surface, double angle, double scale, int smooth=1):
    cdef SDL_Surface *rsurf = NULL
    cdef Surface rv

    with nogil:
        rsurf = rotozoomSurface(surface.surface, angle, scale, smooth)

    if rsurf == NULL:
        raise error()

    rv = Surface(())
    rv.take_surface(rsurf)

    return rv

cdef uint32_t get_at(SDL_Surface *surf, int x, int y) noexcept nogil:
    if x < 0:
        x = 0
    elif x >= surf.w:
        x = surf.w - 1
    if y < 0:
        y = 0
    elif y >= surf.h:
        y = surf.h - 1

    cdef uint32_t *p = <uint32_t*>surf.pixels
    p += y * (surf.pitch // sizeof(uint32_t))
    p += x
    return p[0]

cdef void set_at(SDL_Surface *surf, int x, int y, uint32_t color) noexcept nogil:
    cdef uint32_t *p = <uint32_t*>surf.pixels
    p += y * (surf.pitch // sizeof(uint32_t))
    p += x
    p[0] = color

def scale2x(Surface surface, Surface DestSurface=None):
    cdef int x, y

    cdef uint32_t a, b, c, d, e, f, g, h, i
    cdef uint32_t e0, e1, e2, e3

    if surface.get_bytesize() != 4:
        raise error("Surface has unsupported bytesize.")

    cdef Surface surf_out = DestSurface
    if surf_out == None:
        surf_out = Surface((surface.get_width()*2, surface.get_height()*2), 0, surface)

    surface.lock()
    surf_out.lock()

    cdef int width, height
    width, height = surface.get_size()

    with nogil:
        for x in range(width):
            for y in range(height):
                # Get the surrounding 9 pixels.
                a = get_at(surface.surface, x - 1, y - 1)
                b = get_at(surface.surface, x, y - 1)
                c = get_at(surface.surface, x + 1, y - 1)

                d = get_at(surface.surface, x - 1, y)
                e = get_at(surface.surface, x, y)
                f = get_at(surface.surface, x + 1, y)

                g = get_at(surface.surface, x - 1, y + 1)
                h = get_at(surface.surface, x, y + 1)
                i = get_at(surface.surface, x + 1, y + 1)

                # Expand the center pixel.
                if b != h and d != f:
                    e0 = d if d == b else e
                    e1 = f if b == f else e
                    e2 = d if d == h else e
                    e3 = f if h == f else e
                else:
                    e0 = e1 = e2 = e3 = e

                set_at(surf_out.surface, x*2, y*2, e0)
                set_at(surf_out.surface, (x*2)+1, y*2, e1)
                set_at(surf_out.surface, x*2, (y*2)+1, e2)
                set_at(surf_out.surface, (x*2)+1, (y*2)+1, e3)

    surf_out.unlock()
    surface.unlock()

    return surf_out

def smoothscale(Surface surface, size, Surface DestSurface=None):
    cdef double scale_x = size[0] / <double>surface.surface.w
    cdef double scale_y = size[1] / <double>surface.surface.h

    cdef SDL_Surface *rsurf = NULL
    cdef Surface rv

    with nogil:
        rsurf = rotozoomSurfaceXY(surface.surface, 0.0, scale_x, scale_y, SMOOTHING_ON)

    if rsurf == NULL:
        raise error()

    rv = Surface(())
    rv.take_surface(rsurf)

    # This is inefficient.
    if DestSurface:
        with nogil:
            SDL_SetSurfaceBlendMode(rv.surface, SDL_BLENDMODE_NONE)
            SDL_UpperBlit(rv.surface, NULL, DestSurface.surface, NULL)

    return rv
