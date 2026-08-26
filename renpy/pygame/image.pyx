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

cdef extern from "pygame/write_png.h":
    int Pygame_SDL3_SavePNG_IO(SDL_IOStream *, SDL_Surface *, int) nogil


def init() -> None:
    pass


def quit() -> None:
    pass


cdef bytes process_namehint(object namehint):
    """
    Reduces `namehint` to an upper-case extension without a leading dot,
    the form SDL_image and `save` expect. Accepts "foo.png", ".png", or
    "png", and returns b"PNG". Returns b"" if there is nothing usable.
    """

    if not namehint:
        return b""

    cdef bytes hint = os.fsencode(namehint)

    hint = os.path.splitext(hint)[1] or hint

    if hint and hint[0] == b".":
        hint = hint[1:]

    return hint.upper()


def load(fi: object, namehint: str = "", size: tuple[int, int] | None = None) -> Surface:
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


def save(surface: Surface, file: object, namehint: str = "", *, compression: int = -1) -> None:
    """
    Saves `surface` to `file`, as a PNG, JPEG, or BMP image.

    `file`
        A filename, or a file-like object opened for writing.

    `namehint`
        If given, should be a string, or string path-like, with or without
        a leading dot, that gives the format to save in. When `file` is a
        file-like object, this is the only way to select a format.

    `compression`
        For PNG, the zlib compression level, from 0 to 9. For JPEG, the
        quality, from 0 to 100. If negative, a per-format default is used.
    """

    # SDL_image writes what it's told to - the name is the only hint there is.
    if not namehint and isinstance(file, (str, os.PathLike)):
        namehint = file

    cdef bytes ext = process_namehint(namehint)

    # Check the format before `file` is opened, as opening it truncates it.
    if not ext:
        raise ValueError("Could not determine the image format to save, give a namehint.")
    elif ext not in (b"PNG", b"JPG", b"JPEG", b"BMP"):
        raise ValueError(f"Unsupported image format: {os.fsdecode(namehint)!r}")

    cdef SDL_Surface *sdl_surface = surface.sdl_surface
    cdef bint ok = False
    cdef bint closed = False
    cdef int quality = compression

    cdef SDL_IOStream *iostream = open_io(file, "wb").take()

    try:
        if ext == b"PNG":
            with nogil:
                ok = Pygame_SDL3_SavePNG_IO(iostream, sdl_surface, quality) == 0

        elif ext == b"BMP":
            with nogil:
                ok = IMG_SaveBMP_IO(sdl_surface, iostream, False)

        else:
            quality = 90 if quality < 0 else quality
            with nogil:
                ok = IMG_SaveJPG_IO(sdl_surface, iostream, False, quality)

    finally:
        closed = SDL_CloseIO(iostream)

    if not (ok and closed):
        raise error()


def get_extended() -> bool:
    # This may be called before init.
    return True
