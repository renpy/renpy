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

from .sdl cimport *
from .sdl_image cimport *
from .surface cimport *
from .iostream cimport open_io

from .error import error

import os

cdef extern from "pygame/write_jpeg.h":
    int Pygame_SDL2_SaveJPEG(SDL_Surface *, const char *, int) nogil

cdef extern from "pygame/write_png.h":
    int Pygame_SDL2_SavePNG(const char *, SDL_Surface *, int) nogil


def init():
    pass


def quit():
    pass


cdef bytes process_namehint(object namehint):
    """
    Reduces `namehint` to an upper-case extension without a leading dot,
    the form SDL_image and `save` expect. Accepts "foo.png", ".png", or
    "png", and returns b"PNG". Returns b"" if there is nothing usable.
    """

    if namehint is None:
        return b""

    cdef bytes hint = os.fsencode(namehint)

    hint = os.path.splitext(hint)[1] or hint

    if hint and hint[0] == b".":
        hint = hint[1:]

    return hint.upper()


def load(fi, namehint="", size=None):
    """
    Loads an image from `fi`, and returns it as a Surface.

    `fi`
        A filename or file-like object to load the image from.

    `namehint`
        If given, should be a string, or string path-like, with or without
        a leading dot, that hints at the format of the image.

    `size`
        A width, height tuple that specifies the size the image is loaded
        at. This is only supported for SVG images.
    """

    cdef SDL_Surface *img
    cdef SDL_Surface *new_surface

    cdef int width
    cdef int height

    # SDL_image detects most formats from the data itself, but some (TGA in
    # particular) have no magic number and can only be found by name.
    if not namehint and isinstance(fi, str):
        namehint = fi

    cdef bytes ext = process_namehint(namehint)
    cdef const char *ext_c = ext
    cdef bint sized_svg = (ext == b"SVG") and (size is not None)

    if sized_svg:
        width, height = size

    cdef SDL_IOStream *iostream = open_io(fi).take()

    try:
        if sized_svg:
            with nogil:
                img = IMG_LoadSizedSVG_IO(iostream, width, height)

        elif ext:
            with nogil:
                img = IMG_LoadTyped_IO(iostream, False, ext_c)

        else:
            with nogil:
                img = IMG_Load_IO(iostream, False)

    finally:
        SDL_CloseIO(iostream)

    if img == NULL:
        raise error()

    if img.format != SDL_PIXELFORMAT_RGBA32:
        new_surface = SDL_ConvertSurface(img, SDL_PIXELFORMAT_RGBA32)
        SDL_DestroySurface(img)
        img = new_surface

        if img == NULL:
            raise error()

    cdef Surface surf = Surface(())
    surf.take_surface(img)

    return surf


def save(Surface surface not None, object filename, int compression=-1):
    """
    Saves `surface` to `filename`, in the format given by the extension of
    `filename`.

    `compression`
        For PNG, the zlib compression level, from 0 to 9. For JPEG, the
        quality, from 0 to 100. If negative, a per-format default is used.
    """

    # SDL takes UTF-8 filenames on every platform.
    cdef bytes fn = os.fsencode(filename)
    cdef const char *fn_c = fn
    cdef str ext = process_namehint(fn).decode("utf-8", "replace")
    cdef SDL_Surface *sdl_surface = surface.sdl_surface
    cdef int err = 0

    if ext == "PNG":
        with nogil:
            err = Pygame_SDL2_SavePNG(fn_c, sdl_surface, compression)
    elif ext in ("JPG", "JPEG"):
        with nogil:
            err = Pygame_SDL2_SaveJPEG(sdl_surface, fn_c, compression)
    elif ext == "BMP":
        with nogil:
            err = not IMG_SaveBMP(sdl_surface, fn_c)
    else:
        raise ValueError(f"Unsupported image format: {ext}")

    if err != 0:
        raise error()


def get_extended() -> bool:
    # This may be called before init.
    return True
