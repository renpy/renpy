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

from sdl2 cimport *
from sdl2_image cimport *
from renpy.pygame.surface cimport *
from renpy.pygame.rwobject cimport to_rwops

from renpy.pygame.error import error

import sys
import os
import renpy.pygame


cdef int image_formats = 0

def init():
    # Attempt to initialize everything. Only fail loudly if all formats fail
    global image_formats
    image_formats = IMG_Init(IMG_INIT_JPG | IMG_INIT_PNG | IMG_INIT_TIF | IMG_INIT_WEBP | IMG_INIT_JXL | IMG_INIT_AVIF)
    if image_formats == 0:
        raise error()

init()

# Make it possible for python to check individual formats
INIT_JPG = IMG_INIT_JPG
INIT_PNG = IMG_INIT_PNG
INIT_TIF = IMG_INIT_TIF
INIT_WEBP = IMG_INIT_WEBP
INIT_JXL = IMG_INIT_JXL
INIT_AVIF = IMG_INIT_AVIF

def has_init(int flags):
    return (flags & image_formats) == flags

def quit(): # @ReservedAssignment
    IMG_Quit()

cdef process_namehint(namehint):
    # Accepts "foo.png", ".png", or "png"

    if not isinstance(namehint, bytes):
        namehint = namehint.encode("ascii", "replace")

    if not namehint:
        return b''

    ext = os.path.splitext(namehint)[1]
    if not ext:
        ext = namehint
    if ext[0] == b'.':
        ext = ext[1:]

    return ext.upper()

def load(fi, namehint="", size=None):
    """
    `size`
        A width, height tuple that specifies the size the image is loaded
        at. This is only supported for SVG images.
    """

    cdef SDL_Surface *img

    cdef SDL_RWops *rwops
    cdef char *ftype

    cdef int width
    cdef int height

    # IMG_Load_RW can't load TGA images.
    if isinstance(fi, str):
        if fi.lower().endswith('.tga'):
            namehint = "TGA"

    rwops = to_rwops(fi)

    if namehint == "":
        with nogil:
            img = IMG_Load_RW(rwops, 1)

    else:
        namehint = process_namehint(namehint)
        ftype = namehint

        if namehint == b".SVG" and size is not None:
            width, height = size

            with nogil:
                img = IMG_LoadSizedSVG_RW(rwops, width, height)

            SDL_RWclose(rwops)

        else:

            with nogil:
                img = IMG_LoadTyped_RW(rwops, 1, ftype)

    if img == NULL:
        raise error()

    cdef Surface surf = Surface(())
    surf.take_surface(img)

    if img.format.BitsPerPixel == 32:
        return surf

    cdef int n = 0
    has_alpha = False

    if img.format.Amask:
        has_alpha = True
    elif (img.format.format >> 24) & SDL_PIXELTYPE_INDEX1:
        has_alpha = True
    elif img.format.palette != NULL:
        # Check for non-opaque palette colors.
        while n < img.format.palette.ncolors:
            if img.format.palette.colors[n].a != 255:
                has_alpha = True
                break
            n += 1

    try:
        if has_alpha:
            return surf.convert_alpha()
        else:
            return surf.convert()
    except error:
        return surf

cdef extern from "pygame/write_jpeg.h":
    int Pygame_SDL2_SaveJPEG(SDL_Surface *, char *, int) nogil

cdef extern from "pygame/write_png.h":
    int Pygame_SDL2_SavePNG(const char *, SDL_Surface *, int) nogil

def save(Surface surface not None, filename, compression=-1):

    if not isinstance(filename, str):
        filename = filename.decode(sys.getfilesystemencoding())

    ext = os.path.splitext(filename)[1]
    ext = ext.upper()
    ext = ext.encode("utf-8")
    err = 0

    utf8_filename = filename.encode("utf-8")

    cdef char *fn = utf8_filename
    cdef SDL_RWops *rwops
    cdef int compression_level = compression

    if ext == b'.PNG':
        with nogil:
            err = Pygame_SDL2_SavePNG(fn, surface.surface, compression_level)
    elif ext == b'.BMP':
        rwops = to_rwops(filename, "wb")
        with nogil:
            err = SDL_SaveBMP_RW(surface.surface, rwops, 1)
    elif ext == b".JPG" or ext == b".JPEG":
        with nogil:
            err = Pygame_SDL2_SaveJPEG(surface.surface, fn, compression_level)
    else:
        raise ValueError("Unsupported format: %s" % ext)

    if err != 0:
        raise error()

def get_extended():
    # This may be called before init.
    return True
