# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
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

from libc.string cimport memmove
from .sdl cimport *

from .color cimport map_color, get_color
from .rect cimport to_sdl_rect
from .rect import Rect

from .error import error
# from pygame.locals import SRCALPHA

import warnings

cdef void move_pixels(Uint8 *src, Uint8 *dst, int h, int span, int srcpitch, int dstpitch) noexcept nogil:
    if src < dst:
        src += (h - 1) * srcpitch
        dst += (h - 1) * dstpitch
        srcpitch = -srcpitch
        dstpitch = -dstpitch

    while h:
        h -= 1
        memmove(dst, src, span)
        src += srcpitch
        dst += dstpitch


# Blend mode constants compatible with pygame.
cdef enum:
    C_BLEND_ADD = 0x1
    C_BLEND_SUB = 0x2
    C_BLEND_MULT = 0x3
    C_BLEND_MIN = 0x4
    C_BLEND_MAX = 0x5
    C_BLEND_RGBA_ADD = 0x6
    C_BLEND_RGBA_SUB = 0x7
    C_BLEND_RGBA_MULT = 0x8
    C_BLEND_RGBA_MIN = 0x9
    C_BLEND_RGBA_MAX = 0x10
    C_BLEND_PREMULTIPLIED = 0x11
    C_BLEND_ALPHA_SDL2 = 0x12

BLEND_ADD = BLEND_RGB_ADD = C_BLEND_ADD
BLEND_SUB = BLEND_RGB_SUB = C_BLEND_SUB
BLEND_MULT = BLEND_RGB_MULT = C_BLEND_MULT
BLEND_MIN = BLEND_RGB_MIN = C_BLEND_MIN
BLEND_MAX = BLEND_RGB_MAX = C_BLEND_MAX

BLEND_RGBA_ADD = C_BLEND_RGBA_ADD
BLEND_RGBA_SUB = C_BLEND_RGBA_SUB
BLEND_RGBA_MULT = C_BLEND_RGBA_MULT
BLEND_RGBA_MIN = C_BLEND_RGBA_MIN
BLEND_RGBA_MAX = C_BLEND_RGBA_MAX

BLEND_PREMULTIPLIED = C_BLEND_PREMULTIPLIED
BLEND_ALPHA_SDL2 = C_BLEND_ALPHA_SDL2

# The total size of all allocated surfaces
total_size = 0

cdef class Surface:

    def __cinit__(self):
        self.surface = NULL
        self.owns_surface = False
        self.window_surface = False
        self.has_alpha = False

    def __dealloc__(self):
        global total_size

        if self.surface and self.owns_surface:
            if total_size:
                total_size -= self.surface.pitch * self.surface.h

            SDL_DestroySurface(self.surface)
            return
        elif self.window_surface:
            return
        elif self.parent:
            SDL_DestroySurface(self.surface)
            return

        warnings.warn("Memory leak via Surface in renpy.pygame.")

    def __sizeof__(self):
        if self.surface and self.owns_surface:
            return self.surface.pitch * self.surface.h
        else:
            return 0

    def __init__(self, size, flags=0, depth=32, masks=None):

        self.parent = None

        self.offset_x = 0
        self.offset_y = 0

        self.get_window_flags = None

        # When size is an empty tuple, we do not create a surface, and
        # expect our caller to set this object up.
        if size == ():
            return

        cdef int w
        cdef int h

        w, h = size
        assert w >= 0
        assert h >= 0

        cdef int depth_int


        cdef SDL_Surface *surface

        with nogil:
            surface = SDL_CreateSurface(w, h, SDL_PIXELFORMAT_RGBA32)

        if not surface:
            raise error()

        self.take_surface(surface)

    cdef void take_surface(self, SDL_Surface *surface):
        if not surface:
            raise error("A null pointer was passed in.")

        self.surface = surface
        self.owns_surface = True

        global total_size

        total_size += self.surface.pitch * self.surface.h

    def __repr__(self):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)
        return "<Surface({}x{}x{})>".format(self.surface.w, self.surface.h, format.bits_per_pixel)

    def blit(self, Surface source, dest, area=None, int special_flags=0):
        cdef SDL_Rect dest_rect
        cdef SDL_Rect area_rect
        cdef SDL_Rect *area_ptr = NULL
        cdef SDL_Rect clip_rect

        cdef Surface source_view
        cdef Surface dest_view

        cdef int success
        cdef int src_x
        cdef int src_y
        cdef int src_w
        cdef int src_h
        cdef int dst_x
        cdef int dst_y
        cdef int left
        cdef int top
        cdef int right
        cdef int bottom
        cdef int out_w
        cdef int out_h

        try:
            if isinstance(dest, Rect):
                dst_x = dest.x
                dst_y = dest.y
            elif len(dest) == 2:
                dst_x, dst_y = dest
            elif len(dest) == 4:
                dst_x, dst_y = dest[0], dest[1]
            else:
                raise TypeError()
        except:
            raise TypeError("Argument dest must be a rect style object.")

        dest_rect.x = dst_x
        dest_rect.y = dst_y
        dest_rect.w = source.surface.w
        dest_rect.h = source.surface.h

        if area is not None:
            to_sdl_rect(area, &area_rect, "area")
            area_ptr = &area_rect
            src_x = area_rect.x
            src_y = area_rect.y
            src_w = area_rect.w
            src_h = area_rect.h
        else:
            src_x = 0
            src_y = 0
            src_w = source.surface.w
            src_h = source.surface.h

        if special_flags:

            # Clip to the source bounds first.
            if src_x < 0:
                dst_x -= src_x
                src_w += src_x
                src_x = 0

            if src_y < 0:
                dst_y -= src_y
                src_h += src_y
                src_y = 0

            if src_x + src_w > source.surface.w:
                src_w = source.surface.w - src_x

            if src_y + src_h > source.surface.h:
                src_h = source.surface.h - src_y

            if src_w <= 0 or src_h <= 0:
                return Rect(0, 0, 0, 0)

            SDL_GetSurfaceClipRect(self.surface, &clip_rect)

            left = max(dst_x, 0, clip_rect.x)
            top = max(dst_y, 0, clip_rect.y)
            right = min(dst_x + src_w, self.surface.w, clip_rect.x + clip_rect.w)
            bottom = min(dst_y + src_h, self.surface.h, clip_rect.y + clip_rect.h)

            if right <= left or bottom <= top:
                return Rect(0, 0, 0, 0)

            src_x += left - dst_x
            src_y += top - dst_y
            out_w = right - left
            out_h = bottom - top

            source_view = source.subsurface((src_x, src_y, out_w, out_h))
            dest_view = self.subsurface((left, top, out_w, out_h))

            # Prevent overlap hazards when source and destination alias.
            if source_view.get_abs_parent() is dest_view.get_abs_parent():
                source_view = source_view.copy()

            dest_view._blend(source_view, special_flags)

            return Rect(left, top, out_w, out_h)

        with nogil:
            SDL_SetSurfaceBlendMode(source.surface, SDL_BLENDMODE_BLEND)
            success = SDL_BlitSurface(source.surface, area_ptr, self.surface, &dest_rect)

        if not success:
            raise error()

        dirty = Rect(dest[0], dest[1], source.surface.w, source.surface.h)
        return dirty.clip(self.get_rect())

    cdef void _blend(self, Surface source, int function):

        cdef int success
        cdef int x
        cdef int y
        cdef int tmp
        cdef int w = self.surface.w
        cdef int h = self.surface.h

        cdef Uint8 *src_pixels
        cdef Uint8 *dst_pixels
        cdef Uint8 *src_row
        cdef Uint8 *dst_row
        cdef Uint8 *sp
        cdef Uint8 *dp

        cdef Uint8 sR
        cdef Uint8 sG
        cdef Uint8 sB
        cdef Uint8 sA
        cdef Uint8 dA

        if source.surface.w != w or source.surface.h != h:
            raise error("source and destination surfaces must be the same size.")

        # These paths assume little-endian 32-bit RGBA surfaces.
        src_pixels = <Uint8 *> source.surface.pixels
        dst_pixels = <Uint8 *> self.surface.pixels

        if function == C_BLEND_ALPHA_SDL2:
            with nogil:
                SDL_SetSurfaceBlendMode(source.surface, SDL_BLENDMODE_BLEND)
                success = SDL_BlitSurface(source.surface, NULL, self.surface, NULL)

            if not success:
                raise error()

        elif function == C_BLEND_ADD:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        tmp = dp[0] + sp[0]
                        dp[0] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = dp[1] + sp[1]
                        dp[1] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = dp[2] + sp[2]
                        dp[2] = <Uint8> (tmp if tmp <= 255 else 255)

        elif function == C_BLEND_SUB:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        tmp = dp[0] - sp[0]
                        dp[0] = <Uint8> (tmp if tmp >= 0 else 0)

                        tmp = dp[1] - sp[1]
                        dp[1] = <Uint8> (tmp if tmp >= 0 else 0)

                        tmp = dp[2] - sp[2]
                        dp[2] = <Uint8> (tmp if tmp >= 0 else 0)

        elif function == C_BLEND_MULT:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        if dp[0] and sp[0]:
                            dp[0] = <Uint8> ((dp[0] * sp[0]) >> 8)
                        else:
                            dp[0] = 0

                        if dp[1] and sp[1]:
                            dp[1] = <Uint8> ((dp[1] * sp[1]) >> 8)
                        else:
                            dp[1] = 0

                        if dp[2] and sp[2]:
                            dp[2] = <Uint8> ((dp[2] * sp[2]) >> 8)
                        else:
                            dp[2] = 0

        elif function == C_BLEND_MIN:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        if sp[0] < dp[0]:
                            dp[0] = sp[0]
                        if sp[1] < dp[1]:
                            dp[1] = sp[1]
                        if sp[2] < dp[2]:
                            dp[2] = sp[2]

        elif function == C_BLEND_MAX:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        if sp[0] > dp[0]:
                            dp[0] = sp[0]
                        if sp[1] > dp[1]:
                            dp[1] = sp[1]
                        if sp[2] > dp[2]:
                            dp[2] = sp[2]

        elif function == C_BLEND_RGBA_ADD:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        tmp = dp[0] + sp[0]
                        dp[0] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = dp[1] + sp[1]
                        dp[1] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = dp[2] + sp[2]
                        dp[2] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = dp[3] + sp[3]
                        dp[3] = <Uint8> (tmp if tmp <= 255 else 255)

        elif function == C_BLEND_RGBA_SUB:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        tmp = dp[0] - sp[0]
                        dp[0] = <Uint8> (tmp if tmp >= 0 else 0)

                        tmp = dp[1] - sp[1]
                        dp[1] = <Uint8> (tmp if tmp >= 0 else 0)

                        tmp = dp[2] - sp[2]
                        dp[2] = <Uint8> (tmp if tmp >= 0 else 0)

                        tmp = dp[3] - sp[3]
                        dp[3] = <Uint8> (tmp if tmp >= 0 else 0)

        elif function == C_BLEND_RGBA_MULT:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        if dp[0] and sp[0]:
                            dp[0] = <Uint8> ((dp[0] * sp[0]) >> 8)
                        else:
                            dp[0] = 0

                        if dp[1] and sp[1]:
                            dp[1] = <Uint8> ((dp[1] * sp[1]) >> 8)
                        else:
                            dp[1] = 0

                        if dp[2] and sp[2]:
                            dp[2] = <Uint8> ((dp[2] * sp[2]) >> 8)
                        else:
                            dp[2] = 0

                        if dp[3] and sp[3]:
                            dp[3] = <Uint8> ((dp[3] * sp[3]) >> 8)
                        else:
                            dp[3] = 0

        elif function == C_BLEND_RGBA_MIN:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        if sp[0] < dp[0]:
                            dp[0] = sp[0]
                        if sp[1] < dp[1]:
                            dp[1] = sp[1]
                        if sp[2] < dp[2]:
                            dp[2] = sp[2]
                        if sp[3] < dp[3]:
                            dp[3] = sp[3]

        elif function == C_BLEND_RGBA_MAX:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        if sp[0] > dp[0]:
                            dp[0] = sp[0]
                        if sp[1] > dp[1]:
                            dp[1] = sp[1]
                        if sp[2] > dp[2]:
                            dp[2] = sp[2]
                        if sp[3] > dp[3]:
                            dp[3] = sp[3]

        elif function == C_BLEND_PREMULTIPLIED:
            with nogil:
                for y in range(h):
                    src_row = src_pixels + y * source.surface.pitch
                    dst_row = dst_pixels + y * self.surface.pitch

                    for x in range(w):
                        sp = src_row + x * 4
                        dp = dst_row + x * 4

                        sR = sp[0]
                        sG = sp[1]
                        sB = sp[2]
                        sA = sp[3]

                        tmp = sR + dp[0] - ((dp[0] * sA) >> 8)
                        dp[0] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = sG + dp[1] - ((dp[1] * sA) >> 8)
                        dp[1] = <Uint8> (tmp if tmp <= 255 else 255)

                        tmp = sB + dp[2] - ((dp[2] * sA) >> 8)
                        dp[2] = <Uint8> (tmp if tmp <= 255 else 255)

                        dA = dp[3]
                        dp[3] = <Uint8> (sA + dA - ((sA * dA) / 255))

        else:
            raise error("unsupported blend mode.")

    def convert(self, surface=None):

        with nogil:
            new_surface = SDL_ConvertSurface(self.surface, SDL_PIXELFORMAT_RGBA32)

        if not new_surface:
            raise error()

        cdef Surface rv = Surface(())
        rv.take_surface(new_surface)

        return rv

    def convert_alpha(self, Surface surface=None):

        with nogil:
            new_surface = SDL_ConvertSurface(self.surface, SDL_PIXELFORMAT_RGBA32)

        if not new_surface:
            raise error()

        cdef Surface rv = Surface(())
        rv.take_surface(new_surface)

        return rv

    def copy(self):
        return self.convert_alpha(self)

    def fill(self, color, rect=None, special_flags=0):

        cdef SDL_Rect sdl_rect
        cdef Uint32 pixel = map_color(self.surface, color)
        cdef int success

        if rect is not None:
            to_sdl_rect(rect, &sdl_rect)

            if sdl_rect.x < 0:
                sdl_rect.w = sdl_rect.w + sdl_rect.x
                sdl_rect.x = 0

            if sdl_rect.y < 0:
                sdl_rect.w = sdl_rect.h + sdl_rect.y
                sdl_rect.y = 0

            if sdl_rect.w <= 0 or sdl_rect.h <= 0:
                return Rect(0, 0, 0, 0)

            with nogil:
                success = SDL_FillSurfaceRect(self.surface, &sdl_rect, pixel)

            if not success:
                raise error()

            return Rect(sdl_rect.x, sdl_rect.y, sdl_rect.w, sdl_rect.h)

        else:
            with nogil:
                success = SDL_FillSurfaceRect(self.surface, NULL, pixel)

            if not success:
                raise error()

            return Rect(0, 0, self.surface.w, self.surface.h)


    def scroll(self, int dx=0, int dy=0):
        cdef int srcx, destx, move_width
        cdef int srcy, desty, move_height

        cdef int width = self.surface.w
        cdef int height = self.surface.h

        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)
        cdef int per_pixel = format.bytes_per_pixel

        if dx >= 0:
            srcx = 0
            destx = dx
            move_width = width - dx
        else:
            srcx = -dx
            destx = 0
            move_width = width + dx

        if dy >= 0:
            srcy = 0
            desty = dy
            move_height = height - dy
        else:
            srcy = -dy
            desty = 0
            move_height = height + dy

        cdef Uint8 *srcptr = <Uint8 *> self.surface.pixels
        cdef Uint8 *destptr = <Uint8 *> self.surface.pixels

        srcptr += srcy * self.surface.pitch + srcx * per_pixel
        destptr += desty * self.surface.pitch + destx * per_pixel

        with nogil:
            move_pixels(
                srcptr,
                destptr,
                move_height,
                move_width * per_pixel,
                self.surface.pitch,
                self.surface.pitch)

    def lock(self, lock=None):
        pass

    def unlock(self, lock=None):
        pass

    def mustlock(self):
        pass

    def get_locked(self):
        return False

    def get_locks(self):
        return [ ]

    def get_at(self, pos):
        cdef int x, y
        cdef Uint8 *p

        x, y = pos

        if not (0 <= x < self.surface.w) or not (0 <= y < self.surface.h):
            raise IndexError("Position outside surface.")

        p = <Uint8 *> self.surface.pixels
        p += y * self.surface.pitch
        p += x * 4

        cdef Uint32 pixel = (<Uint32 *> p)[0]

        return get_color(pixel, self.surface)

    def set_at(self, pos, color):
        cdef int x, y
        cdef Uint8 *p
        cdef Uint32 pixel

        x, y = pos

        if not (0 <= x < self.surface.w) or not (0 <= y < self.surface.h):
            raise ValueError("Position outside surface.")

        pixel = map_color(self.surface, color)

        p = <Uint8 *> self.surface.pixels
        p += y * self.surface.pitch
        p += x * 4

        (<Uint32 *> p)[0] = pixel

    def get_at_mapped(self, pos):
        cdef int x, y
        cdef Uint8 *p

        x, y = pos

        if not (0 <= x < self.surface.w) or not (0 <= y < self.surface.h):
            raise ValueError("Position outside surface.")

        p = <Uint8 *> self.surface.pixels
        p += y * self.surface.pitch
        p += x * 4

        cdef Uint32 pixel = (<Uint32 *> p)[0]

        return pixel

    def map_rgb(self, color):
        return map_color(self.surface, color)

    def unmap_rgb(self, pixel):
        return get_color(pixel, self.surface)

    def set_clip(self, rect):
        cdef SDL_Rect sdl_rect

        if rect is None:
            SDL_SetSurfaceClipRect(self.surface, NULL)
        else:
            to_sdl_rect(rect, &sdl_rect)
            SDL_SetSurfaceClipRect(self.surface, &sdl_rect)

    def get_clip(self):
        cdef SDL_Rect sdl_rect

        SDL_GetSurfaceClipRect(self.surface, &sdl_rect)

        return (sdl_rect.x, sdl_rect.y, sdl_rect.w, sdl_rect.h)

    def subsurface(self, *args):
        cdef SDL_Rect sdl_rect

        if len(args) == 1:
            to_sdl_rect(args[0], &sdl_rect)
        else:
            to_sdl_rect(args, &sdl_rect)

        if sdl_rect.w < 0 or sdl_rect.h < 0:
            raise error("subsurface size must be non-negative.")

        if ((sdl_rect.x < 0)
            or (sdl_rect.y < 0)
            or (sdl_rect.x + sdl_rect.w > self.surface.w)
            or (sdl_rect.y + sdl_rect.h > self.surface.h)):

            raise error("subsurface rectangle outside surface area.")

        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)

        cdef Uint8 *pixels = <Uint8 *> self.surface.pixels
        pixels += sdl_rect.y * self.surface.pitch
        pixels += sdl_rect.x * format.bytes_per_pixel

        cdef SDL_Surface *new_surface = SDL_CreateSurfaceFrom(
            sdl_rect.w,
            sdl_rect.h,
            self.surface.format,
            pixels,
            self.surface.pitch)

        if not new_surface:
            raise error()

        cdef Surface rv = Surface(())

        rv.surface = new_surface
        rv.parent = self
        rv.offset_x = sdl_rect.x
        rv.offset_y = sdl_rect.y

        return rv

    def get_parent(self):
        return self.parent

    def get_abs_parent(self):
        rv = self

        while rv.parent:
            rv = rv.parent

        return rv

    def get_offset(self):
        return (self.offset_x, self.offset_y)

    def get_abs_offset(self):
        cdef Surface surf = self

        cdef int offset_x = 0
        cdef int offset_y = 0

        while surf:
            offset_x += surf.offset_x
            offset_y += surf.offset_y
            surf = surf.parent

        return (offset_x, offset_y)

    def get_size(self):
        return self.surface.w, self.surface.h

    def get_width(self):
        return self.surface.w

    def get_height(self):
        return self.surface.h

    def get_rect(self, **kwargs):
        rv = Rect((0, 0, self.surface.w, self.surface.h))

        for k, v in kwargs.items():
            setattr(rv, k, v)

        return rv

    def get_bitsize(self):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)

        return format.bits_per_pixel

    def get_bytesize(self):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)

        return format.bytes_per_pixel

    def get_flags(self):

        if self.get_window_flags:
            rv = self.get_window_flags()
        else:
            rv = 0

        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)

        if format.Amask != 0:
            rv = rv | 0x80000000 # TODO SRCALPHA

        return rv

    def get_pitch(self):
        return self.surface.pitch

    def get_masks(self):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)
        return (format.Rmask, format.Gmask, format.Bmask, format.Amask)

    def get_shifts(self):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)
        return (format.Rshift, format.Gshift, format.Bshift, format.Ashift)

    def get_losses(self):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)
        return (8-format.Rbits, 8-format.Gbits, 8-format.Bbits, 8-format.Abits)

    def get_bounding_rect(self, min_alpha=1):

        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)

        cdef Uint32 amask = format.Amask
        cdef Uint32 amin = (0x01010101 * min_alpha) & amask

        cdef int x
        cdef int y
        cdef int w
        cdef int h

        cdef int minx = self.surface.w - 1
        cdef int maxx = 0
        cdef int miny = self.surface.h - 1
        cdef int maxy = 0

        cdef Uint32 *row

        cdef Uint32 topleft
        cdef Uint32 botright

        if (not amask) or (self.surface.w == 0) or (self.surface.h == 0):
            return Rect((0, 0, self.surface.w, self.surface.h))


        cdef Uint8 *pixels = <Uint8 *> self.surface.pixels

        with nogil:

            topleft = (<Uint32*> pixels)[0]
            botright = (<Uint32*> (pixels + self.surface.pitch * (self.surface.h - 1)))[self.surface.w - 1]

            if ((topleft & amask) > amin) and ((botright & amask) > amin):

                # Bounding box covers image.

                minx = 0
                miny = 0
                maxx = self.surface.w - 1
                maxy = self.surface.h - 1

            else:

                # Bounding box is smaller than image.

                for y in range(self.surface.h):
                    row = <Uint32*> (pixels + self.surface.pitch * y)

                    for x in range(self.surface.w):

                        if (row[x] & amask) >= amin:

                            if minx > x:
                                minx = x
                            if miny > y:
                                miny = y
                            if maxx < x:
                                maxx = x
                            if maxy < y:
                                maxy = y

        # Totally empty surface.
        if minx > maxx:
            return Rect((0, 0, 0, 0))

        x = minx
        y = miny
        w = min(maxx - minx + 1, self.surface.w - x)
        h = min(maxy - miny + 1, self.surface.h - y)

        return Rect((x, y, w, h))

    def get_view(self, kind='2'):
        raise error("Surface.get_view is not supported.")

    def get_buffer(self):
        cdef Uint8 *pixels = <Uint8 *> self.surface.pixels
        return pixels[self.surface.h * self.surface.pitch]

    property _pixels_address:
        def __get__(self):
            return <Uint64> self.surface.pixels

    def from_data(self, data):
        cdef const SDL_PixelFormatDetails *format = SDL_GetPixelFormatDetails(self.surface.format)

        if len(data) != self.surface.w * self.surface.h * format.bytes_per_pixel:
            raise ValueError("The data must fill the surface.")

        cdef Uint8 *d = <Uint8 *> data
        cdef Uint8 *pixels = <Uint8 *> self.surface.pixels

        cdef int i

        for i in range(self.surface.h):
            memmove(pixels, d, self.surface.w * format.bytes_per_pixel)
            d += self.surface.w * format.bytes_per_pixel
            pixels += self.surface.pitch

cdef api SDL_Surface *PySurface_AsSurface(surface):
    return (<Surface> surface).surface

cdef api object PySurface_New(SDL_Surface *surf):
    cdef Surface rv = Surface(())
    rv.take_surface(surf)
    return rv
