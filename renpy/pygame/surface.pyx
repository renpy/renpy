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

from libc.string cimport memmove
from sdl2 cimport *

from renpy.pygame.color cimport map_color, get_color
from renpy.pygame.rect cimport to_sdl_rect
from renpy.pygame.rect import Rect

from renpy.pygame.error import error
from renpy.pygame.locals import SRCALPHA
import renpy.pygame

import warnings

cdef extern from "pygame/surface.h" nogil:
    int pygame_Blit (SDL_Surface * src, SDL_Rect * srcrect,
                 SDL_Surface * dst, SDL_Rect * dstrect, int the_args);

cdef void move_pixels(Uint8 *src, Uint8 *dst, int h, int span, int srcpitch, int dstpitch) noexcept nogil:
    if src < dst:
        src += (h - 1) * srcpitch;
        dst += (h - 1) * dstpitch;
        srcpitch = -srcpitch;
        dstpitch = -dstpitch;

    while h:
        h -= 1
        memmove(dst, src, span);
        src += srcpitch;
        dst += dstpitch;

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

            SDL_FreeSurface(self.surface)
            return
        elif self.window_surface:
            return
        elif self.parent:
            SDL_FreeSurface(self.surface)
            return

        warnings.warn("Memory leak via Surface in renpy.pygame.")

    def __sizeof__(self):
        if self.surface and self.owns_surface:
            return self.surface.pitch * self.surface.h
        else:
            return 0

    def __init__(self, size, flags=0, depth=32, masks=None):

        self.locklist = None
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

        cdef Uint32 Rmask, Gmask, Bmask, Amask
        cdef SDL_Surface *sample
        cdef Surface pysample
        cdef int depth_int

        if masks is not None:
            Rmask, Gmask, Bmask, Amask = masks
            depth_int = depth

        elif isinstance(depth, Surface):

            pysample = depth
            sample = pysample.surface
            Rmask = sample.format.Rmask
            Gmask = sample.format.Gmask
            Bmask = sample.format.Bmask
            Amask = sample.format.Amask
            depth_int = sample.format.BitsPerPixel

        else:

            pysample = renpy.pygame.display.get_surface()

            if pysample and pysample.surface.format.BitsPerPixel == 32:
                sample = pysample.surface
                Rmask = sample.format.Rmask
                Gmask = sample.format.Gmask
                Bmask = sample.format.Bmask
                Amask = sample.format.Amask

            else:

                # RGB(A)
                if SDL_BYTEORDER == SDL_BIG_ENDIAN:
                    Rmask = 0xff000000
                    Gmask = 0x00ff0000
                    Bmask = 0x0000ff00
                    Amask = 0
                else:
                    Rmask = 0x000000ff
                    Gmask = 0x0000ff00
                    Bmask = 0x00ff0000
                    Amask = 0

            if (flags & SRCALPHA):
                if not Amask:
                    Amask = 0xffffffff & ~(Rmask | Gmask | Bmask)
            else:
                Amask = 0

            depth_int = 32

        cdef SDL_Surface *surface

        with nogil:
            surface = SDL_CreateRGBSurface(0, w, h, depth_int, Rmask, Gmask, Bmask, Amask)

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
        return "<Surface({}x{}x{})>".format(self.surface.w, self.surface.h, self.surface.format.BitsPerPixel)

    def blit(self, Surface source, dest, area=None, int special_flags=0):
        cdef SDL_Rect dest_rect
        cdef SDL_Rect area_rect
        cdef SDL_Rect *area_ptr = NULL

        cdef Surface temp

        cdef int err
        cdef Uint32 key
        cdef Uint8 alpha
        cdef bint colorkey

        colorkey = (SDL_GetColorKey(source.surface, &key) == 0)

        if not source.surface.format.Amask:
            if SDL_GetSurfaceAlphaMod(source.surface, &alpha):
                raise error()

            if alpha != 255 and (self.surface.format.Amask or colorkey):

                if area:
                    source = source.subsurface(area)
                    area = None

                if SDL_SetSurfaceBlendMode(source.surface, SDL_BLENDMODE_NONE):
                    raise error()
                temp = Surface(source.get_size(), SRCALPHA)

                with nogil:
                    err = SDL_UpperBlit(source.surface, NULL, temp.surface, NULL)

                if err:
                    raise error()

                source = temp
                colorkey = False

        if colorkey:
            if SDL_SetSurfaceBlendMode(source.surface, SDL_BLENDMODE_NONE):
                raise error()
        else:
            if SDL_SetSurfaceBlendMode(source.surface, SDL_BLENDMODE_BLEND):
                raise error()

        to_sdl_rect(dest, &dest_rect, "dest")

        if area is not None:
            to_sdl_rect(area, &area_rect, "area")
            area_ptr = &area_rect

        with nogil:

            if source.surface.format.Amask or special_flags:
                err = pygame_Blit(source.surface, area_ptr, self.surface, &dest_rect, special_flags)
            else:
                err = SDL_UpperBlit(source.surface, area_ptr, self.surface, &dest_rect)

        if err:
            raise error()

        dirty = Rect(dest[0], dest[1], source.surface.w, source.surface.h)
        return dirty.clip(self.get_rect())

    def convert(self, surface=None):
        if not isinstance(surface, Surface):
            surface = renpy.pygame.display.get_surface()

        cdef SDL_PixelFormat *sample_format

        if surface is None:
            sample_format = SDL_AllocFormat(SDL_PIXELFORMAT_BGRX8888)
        else:
            sample_format = (<Surface> surface).surface.format

        cdef Uint32 amask
        cdef Uint32 rmask
        cdef Uint32 gmask
        cdef Uint32 bmask

        cdef Uint32 pixel_format
        cdef SDL_Surface *new_surface

        # If the sample surface has alpha, use it.
        if not sample_format.Amask:
            use_format = sample_format

            with nogil:
                new_surface = SDL_ConvertSurface(self.surface, sample_format, 0)

            if not new_surface:
                raise error()

        else:

            rmask = sample_format.Rmask
            gmask = sample_format.Gmask
            bmask = sample_format.Bmask
            amask = 0

            pixel_format = SDL_MasksToPixelFormatEnum(32, rmask, gmask, bmask, amask)

            with nogil:
                new_surface = SDL_ConvertSurfaceFormat(self.surface, pixel_format, 0)

            if not new_surface:
                raise error()

        cdef Surface rv = Surface(())
        rv.take_surface(new_surface)

        return rv

    def convert_alpha(self, Surface surface=None):
        if surface is None:
            surface = renpy.pygame.display.get_surface()

        cdef SDL_PixelFormat *sample_format

        if surface is None:
            sample_format = SDL_AllocFormat(SDL_PIXELFORMAT_BGRA8888)
        else:
            sample_format = (<Surface> surface).surface.format

        cdef Uint32 amask = 0xff000000
        cdef Uint32 rmask = 0x00ff0000
        cdef Uint32 gmask = 0x0000ff00
        cdef Uint32 bmask = 0x000000ff

        cdef Uint32 pixel_format
        cdef SDL_Surface *new_surface

        # If the sample surface has alpha, use it.
        if sample_format.Amask:
            use_format = sample_format

            with nogil:
                new_surface = SDL_ConvertSurface(self.surface, sample_format, 0)

            if not new_surface:
                raise error()

        else:

            if sample_format.BytesPerPixel == 4:
                rmask = sample_format.Rmask
                gmask = sample_format.Gmask
                bmask = sample_format.Bmask
                amask = 0xffffffff & ~(rmask | gmask | bmask)

            pixel_format = SDL_MasksToPixelFormatEnum(32, rmask, gmask, bmask, amask)

            with nogil:
                new_surface = SDL_ConvertSurfaceFormat(self.surface, pixel_format, 0)

            if not new_surface:
                raise error()

        cdef Surface rv = Surface(())
        rv.take_surface(new_surface)

        return rv

    def copy(self):
        if self.surface.format.Amask:
            return self.convert_alpha(self)
        else:
            return self.convert(self)

    def fill(self, color, rect=None, special_flags=0):

        cdef SDL_Rect sdl_rect
        cdef Uint32 pixel = map_color(self.surface, color)
        cdef int err

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
                err = SDL_FillRect(self.surface, &sdl_rect, pixel)

            if err:
                raise error()

            return Rect(sdl_rect.x, sdl_rect.y, sdl_rect.w, sdl_rect.h)

        else:
            with nogil:
                err = SDL_FillRect(self.surface, NULL, pixel)

            if err:
                raise error()

            return Rect(0, 0, self.surface.w, self.surface.h)


    def scroll(self, int dx=0, int dy=0):
        cdef int srcx, destx, move_width
        cdef int srcy, desty, move_height

        cdef int width = self.surface.w
        cdef int height = self.surface.h

        cdef int per_pixel = self.surface.format.BytesPerPixel

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

        self.lock()

        with nogil:
            move_pixels(
                srcptr,
                destptr,
                move_height,
                move_width * per_pixel,
                self.surface.pitch,
                self.surface.pitch)

        self.unlock()

    def set_colorkey(self, color, flags=0):

        if color is None:
            if SDL_SetColorKey(self.surface, SDL_FALSE, 0):
                raise error()

        else:
            if SDL_SetColorKey(self.surface, SDL_TRUE, map_color(self.surface, color)):
                raise error()

    def get_colorkey(self):
        cdef Uint32 key

        if SDL_GetColorKey(self.surface, &key):
            return None

        return get_color(key, self.surface)

    def set_alpha(self, value, flags=0):
        if value is None:
            value = 255
            self.has_alpha = False
        else:
            self.has_alpha = True

        if SDL_SetSurfaceAlphaMod(self.surface, value):
            raise error()

    def get_alpha(self):
        cdef Uint8 rv

        if self.has_alpha or self.surface.format.Amask:

            if SDL_GetSurfaceAlphaMod(self.surface, &rv):
                raise error()

            return rv

        else:
            return None

    def lock(self, lock=None):
        cdef Surface root = self

        while root.parent:
            root = root.parent

        if lock is None:
            lock = self

        if root.locklist is None:
            root.locklist = [ ]

        root.locklist.append(lock)

        if SDL_LockSurface(root.surface):
            raise error()

    def unlock(self, lock=None):
        cdef Surface root = self

        while root.parent:
            root = root.parent

        if lock is None:
            lock = self

        if root.locklist is None:
            root.locklist = [ ]

        root.locklist.remove(lock)

        SDL_UnlockSurface(root.surface)

    def mustlock(self):
        cdef Surface root = self

        while root.parent:
            root = root.parent

        return SDL_MUSTLOCK(root.surface)

    def get_locked(self):
        if self.locklist:
            return True

    def get_locks(self):
        cdef Surface root = self

        while root.parent:
            root = root.parent

        if root.locklist is None:
            root.locklist = [ ]

        return root.locklist

    def get_at(self, pos):
        cdef int x, y
        cdef Uint8 *p

        x, y = pos

        if not (0 <= x < self.surface.w) or not (0 <= y < self.surface.h):
            raise IndexError("Position outside surface.")

        if self.surface.format.BytesPerPixel != 4:
            raise error("Surface has unsupported bytesize.")

        self.lock()

        p = <Uint8 *> self.surface.pixels
        p += y * self.surface.pitch
        p += x * 4

        cdef Uint32 pixel = (<Uint32 *> p)[0]

        self.unlock()

        return get_color(pixel, self.surface)

    def set_at(self, pos, color):
        cdef int x, y
        cdef Uint8 *p
        cdef Uint32 pixel

        x, y = pos

        if not (0 <= x < self.surface.w) or not (0 <= y < self.surface.h):
            raise ValueError("Position outside surface.")

        if self.surface.format.BytesPerPixel != 4:
            raise error("Surface has unsupported bytesize.")

        pixel = map_color(self.surface, color)

        self.lock()

        p = <Uint8 *> self.surface.pixels
        p += y * self.surface.pitch
        p += x * 4

        (<Uint32 *> p)[0] = pixel

        self.unlock()

    def get_at_mapped(self, pos):
        cdef int x, y
        cdef Uint8 *p

        x, y = pos

        if not (0 <= x < self.surface.w) or not (0 <= y < self.surface.h):
            raise ValueError("Position outside surface.")

        if self.surface.format.BytesPerPixel != 4:
            raise error("Surface has unsupported bytesize.")

        self.lock()

        p = <Uint8 *> self.surface.pixels
        p += y * self.surface.pitch
        p += x * 4

        cdef Uint32 pixel = (<Uint32 *> p)[0]

        self.unlock()

        return pixel

    def map_rgb(self, color):
        return map_color(self.surface, color)

    def unmap_rgb(self, pixel):
        return get_color(pixel, self.surface)

    def set_clip(self, rect):
        cdef SDL_Rect sdl_rect

        if rect is None:
            SDL_SetClipRect(self.surface, NULL)
        else:
            to_sdl_rect(rect, &sdl_rect)
            SDL_SetClipRect(self.surface, &sdl_rect)

    def get_clip(self):
        cdef SDL_Rect sdl_rect

        SDL_GetClipRect(self.surface, &sdl_rect)

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

        cdef Uint8 *pixels = <Uint8 *> self.surface.pixels
        pixels += sdl_rect.y * self.surface.pitch
        pixels += sdl_rect.x * self.surface.format.BytesPerPixel

        cdef SDL_Surface *new_surface = SDL_CreateRGBSurfaceFrom(
            pixels,
            sdl_rect.w,
            sdl_rect.h,
            self.surface.format.BitsPerPixel,
            self.surface.pitch,
            self.surface.format.Rmask,
            self.surface.format.Gmask,
            self.surface.format.Bmask,
            self.surface.format.Amask)

        if not new_surface:
            raise error()

        cdef Surface rv = Surface(())

        rv.surface = new_surface
        rv.parent = self
        rv.offset_x = sdl_rect.x
        rv.offset_y = sdl_rect.y

        if self.has_alpha:
            rv.set_alpha(self.get_alpha())

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
        return self.surface.format.BitsPerPixel

    def get_bytesize(self):
        return self.surface.format.BytesPerPixel

    def get_flags(self):

        if self.get_window_flags:
            rv = self.get_window_flags()
        else:
            rv = 0

        if self.surface.format.Amask or self.has_alpha:
            rv = rv | SRCALPHA

        return rv

    def get_pitch(self):
        return self.surface.pitch

    def get_masks(self):
        cdef SDL_PixelFormat *format = self.surface.format
        return (format.Rmask, format.Gmask, format.Bmask, format.Amask)

    def set_masks(self, masks):
        warnings.warn("Surface.set_masks is not supported.")

    def get_shifts(self):
        cdef SDL_PixelFormat *format = self.surface.format
        return (format.Rshift, format.Gshift, format.Bshift, format.Ashift)

    def set_shifts(self, shifts):
        warnings.warn("Surface.set_shifts is not supported.")

    def get_shifts(self):
        cdef SDL_PixelFormat *format = self.surface.format
        return (format.Rshift, format.Gshift, format.Bshift, format.Ashift)

    def get_losses(self):
        cdef SDL_PixelFormat *format = self.surface.format
        return (format.Rloss, format.Gloss, format.Bloss, format.Aloss)

    def get_bounding_rect(self, min_alpha=1):

        cdef Uint32 amask = self.surface.format.Amask
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

        self.lock()

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

                for 0 <= y < self.surface.h:
                    row = <Uint32*> (pixels + self.surface.pitch * y)

                    for 0 <= x < self.surface.w:

                        if (row[x] & amask) >= amin:

                            if minx > x:
                                minx = x
                            if miny > y:
                                miny = y
                            if maxx < x:
                                maxx = x
                            if maxy < y:
                                maxy = y

        self.unlock()

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
        if len(data) != self.surface.w * self.surface.h * self.surface.format.BytesPerPixel:
            raise ValueError("The data must fill the surface.")

        cdef Uint8 *d = <Uint8 *> data
        cdef Uint8 *pixels = <Uint8 *> self.surface.pixels

        cdef int i

        for 0 <= i < self.surface.h:
            memmove(pixels, d, self.surface.w * self.surface.format.BytesPerPixel)
            d += self.surface.w * self.surface.format.BytesPerPixel
            pixels += self.surface.pitch

cdef SDL_Surface *PySurface_AsSurface(surface):
    return (<Surface> surface).surface

cdef api object PySurface_New(SDL_Surface *surf):
    cdef Surface rv = Surface(())
    rv.take_surface(surf)
    return rv
