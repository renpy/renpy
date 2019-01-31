# -*- python -*-
# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

def version():
    return (6, 12, 0)

from sdl2 cimport *
from pygame_sdl2 cimport *

cdef extern from "renpy.h":

    void core_init()
    void subpixel_init()

    void save_png_core(object, SDL_RWops *, int)

    void pixellate32_core(object, object, int, int, int, int)
    void pixellate24_core(object, object, int, int, int, int)

    void map32_core(object, object,
                    char *,
                    char *,
                    char *,
                    char *)

    void map24_core(object, object,
                    char *,
                    char *,
                    char *)

    void linmap32_core(object, object,
                    int,
                    int,
                    int,
                    int)

    void linmap24_core(object, object,
                    int,
                    int,
                    int)

    void blur32_core(object, object, object, float, float)
    void blur24_core(object, object, object, float, float)

    void linblur32_core(object, object, int, int)
    void linblur24_core(object, object, int, int)

    void alphamunge_core(object, object, int, int, int, char *)

    void scale32_core(object, object,
                      float, float, float, float,
                      float, float, float, float,
                      int)

    void scale24_core(object, object,
                      float, float, float, float,
                      float, float, float, float)

    void transform32_core(object, object,
                          float, float, float, float, float, float,
                          int, float, int)

    void blend32_core(object, object, object, int)

    void imageblend32_core(object, object, object, object, int, char *)

    void colormatrix32_core(object, object,
                            float, float, float, float, float,
                            float, float, float, float, float,
                            float, float, float, float, float,
                            float, float, float, float, float)

    void staticgray_core(object, object,
                         int, int, int, int, int, char *)

    int subpixel32(object, object, float, float, int)

    void PyErr_Clear()


import pygame

PygameSurface = pygame.Surface

def save_png(surf, file, compress=-1):

    if not isinstance(surf, PygameSurface):
        raise Exception("save_png requires a pygame Surface as its first argument.")

    save_png_core(surf, RWopsFromPython(file), compress)


def pixellate(pysrc, pydst, avgwidth, avgheight, outwidth, outheight):

    if not isinstance(pysrc, PygameSurface):
        raise Exception("pixellate requires a pygame Surface as its first argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("pixellate requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("pixellate requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("pixellate requires both surfaces have the same bitsize.")

    # pysrc.lock()
    # pydst.lock()

    if pysrc.get_bitsize() == 32:
        pixellate32_core(pysrc, pydst, avgwidth, avgheight, outwidth, outheight)
    else:
        pixellate24_core(pysrc, pydst, avgwidth, avgheight, outwidth, outheight)

    # pydst.unlock()
    # pysrc.unlock()


# Please note that r, g, b, and a are not necessarily red, green, blue
# and alpha. Instead, they are the first through fourth byte of data.
# The mapping between byte and color/alpha varies from system to
# system, and needs to be determined at a higher level.
def map(pysrc, pydst, r, g, b, a): # @ReservedAssignment

    if not isinstance(pysrc, PygameSurface):
        raise Exception("map requires a pygame Surface as its first argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("map requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("map requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("map requires both surfaces have the same bitsize.")

    if pydst.get_size() != pysrc.get_size():
        raise Exception("map requires both surfaces have the same size.")

    # pysrc.lock()
    # pydst.lock()

    if pysrc.get_bitsize() == 32:
        map32_core(pysrc, pydst, r, g, b, a)
    else:
        map24_core(pysrc, pydst, r, g, b)

    # pydst.unlock()
    # pysrc.unlock()

# Please note that r, g, b, and a are not necessarily red, green, blue
# and alpha. Instead, they are the first through fourth byte of data.
# The mapping between byte and color/alpha varies from system to
# system, and needs to be determined at a higher level.
def linmap(pysrc, pydst, r, g, b, a):

    if not isinstance(pysrc, PygameSurface):
        raise Exception("map requires a pygame Surface as its first argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("map requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("map requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("map requires both surfaces have the same bitsize.")

    if pydst.get_size() != pysrc.get_size():
        raise Exception("map requires both surfaces have the same size.")

    # pysrc.lock()
    # pydst.lock()

    if pysrc.get_bitsize() == 32:
        linmap32_core(pysrc, pydst, r, g, b, a)
    else:
        linmap24_core(pysrc, pydst, r, g, b)

    # pydst.unlock()
    # pysrc.unlock()


def blur(pysrc, pywrk, pydst, xrad, yrad=None):

    if not isinstance(pysrc, PygameSurface):
        raise Exception("blur requires a pygame Surface as its first argument.")

    if not isinstance(pywrk, PygameSurface):
        raise Exception("blur requires a pygame Surface as its second argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("blur requires a pygame Surface as its third argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("blur requires a 24 or 32 bit surface.")

    if pywrk.get_bitsize() != pysrc.get_bitsize() \
            or pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("blur requires all surfaces have the same bitsize.")

    if pywrk.get_size() != pysrc.get_size() \
            or pydst.get_size() != pysrc.get_size():
        raise Exception("blur requires all surfaces have the same size.")

    if yrad is None:
        yrad = xrad

    if xrad < 0 or yrad < 0:
        raise Exception("blur requires a positive radius.")

#     pysrc.lock()
#     pywrk.lock()
#     pydst.lock()

    if pysrc.get_bitsize() == 32:
        blur32_core(pysrc, pywrk, pydst, xrad, yrad)
    else:
        blur24_core(pysrc, pywrk, pydst, xrad, yrad)

#     pydst.unlock()
#     pywrk.unlock()
#     pysrc.unlock()


def linblur(pysrc, pydst, radius, vertical=0):

    if not isinstance(pysrc, PygameSurface):
        raise Exception("linblur requires a pygame Surface as its first argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("linblur requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("linblur requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("linblur requires both surfaces have the same bitsize.")

    if pydst.get_size() != pysrc.get_size():
        raise Exception("linblur requires both surfaces have the same size.")

    if radius < 1:
        raise Exception("linblur requires a non-zero radius.")

#     pysrc.lock()
#     pydst.lock()

    if pysrc.get_bitsize() == 32:
        linblur32_core(pysrc, pydst, radius, vertical)
    else:
        linblur24_core(pysrc, pydst, radius, vertical)

#     pydst.unlock()
#     pysrc.unlock()


def alpha_munge(pysrc, pydst, srcchan, dstchan, amap):

    if not isinstance(pysrc, PygameSurface):
        raise Exception("alpha_munge requires a pygame Surface as its first argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("alpha_munge requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("alpha_munge requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("alpha_munge requires both surfaces have the same bitsize.")

    if pydst.get_size() != pysrc.get_size():
        raise Exception("alpha_munge requires both surfaces have the same size.")


    if pysrc.get_bitsize() == 24:
        bytes = 3
    else:
        bytes = 4

    # pysrc.lock()
    # pydst.lock()

    alphamunge_core(pysrc, pydst, bytes, srcchan, dstchan, amap)

    # pydst.unlock()
    # pysrc.unlock()


# def stretch(pysrc, pydst, rect):

#     if not isinstance(pysrc, PygameSurface):
#         raise Exception("stretch requires a pygame Surface as its first argument.")

#     if not isinstance(pydst, PygameSurface):
#         raise Exception("stretch requires a pygame Surface as its second argument.")

#     if pydst.get_bitsize() != pysrc.get_bitsize():
#         raise Exception("stretch requires both surfaces have the same bitsize.")

#     if rect:
#         x, y, w, h = rect
#     else:
#         x, y = 0, 0
#         w, h = pysrc.get_size()

#     return stretch_core(pysrc, pydst, x, y, w, h)


def bilinear(pysrc, pydst,
             source_xoff=0.0, source_yoff=0.0, source_width=None, source_height=None,
             dest_xoff=0.0, dest_yoff=0.0, dest_width=None, dest_height=None,
             precise=0):

    if not isinstance(pysrc, PygameSurface):
        raise Exception("bilinear requires a pygame Surface as its first argument.")

    if not isinstance(pydst, PygameSurface):
        raise Exception("bilinear requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("bilinear requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("bilinear requires both surfaces have the same bitsize.")

    if source_width is None or source_height is None:
        source_width, source_height = pysrc.get_size()

    if dest_width is None or dest_height is None:
        dest_width, dest_height = pydst.get_size()

    # pysrc.lock()
    # pydst.lock()

    if pysrc.get_bitsize() == 32:
        scale32_core(pysrc, pydst,
                     source_xoff, source_yoff, source_width, source_height,
                     dest_xoff, dest_yoff, dest_width, dest_height, precise)

    else:
        scale24_core(pysrc, pydst,
                     source_xoff, source_yoff, source_width, source_height,
                     dest_xoff, dest_yoff, dest_width, dest_height)


    # pydst.unlock()
    # pysrc.unlock()


def check(surf):
    if not isinstance(surf, PygameSurface):
        raise Exception("Surface must be a pygame surface.")

    if surf.get_bitsize() != 32:
        raise Exception("Surface must be 32-bit.")


def transform(pysrc, pydst,
              corner_x, corner_y,
              xdx, ydx, xdy, ydy, a=1.0, precise=0):

    check(pysrc)
    check(pydst)

    # pysrc.lock()
    # pydst.lock()

    transform32_core(pysrc, pydst,
                     corner_x, corner_y,
                     xdx, ydx,
                     xdy, ydy,
                     pysrc.get_shifts()[3], a, precise)

    # pydst.unlock()
    # pysrc.unlock()


def blend(pysrca, pysrcb, pydst, alpha):

    check(pysrca)
    check(pysrcb)
    check(pydst)

    # pysrca.lock()
    # pysrcb.lock()
    # pydst.lock()

    blend32_core(pysrca, pysrcb, pydst, alpha)

    # pydst.unlock()
    # pysrcb.unlock()
    # pysrca.unlock()

def imageblend(pysrca, pysrcb, pydst, pyimg, aoff, amap):
    check(pysrca)
    check(pysrcb)
    check(pydst)
    check(pyimg)

    # pysrca.lock()
    # pysrcb.lock()
    # pydst.lock()
    # pyimg.lock()

    imageblend32_core(pysrca, pysrcb, pydst, pyimg, aoff, amap)

    # pyimg.unlock()
    # pydst.unlock()
    # pysrcb.unlock()
    # pysrca.unlock()

def colormatrix(pysrc, pydst,
                c00, c01, c02, c03, c04,
                c10, c11, c12, c13, c14,
                c20, c21, c22, c23, c24,
                c30, c31, c32, c33, c34):

    check(pysrc)
    check(pydst)

    # pysrc.lock()
    # pydst.lock()

    colormatrix32_core(pysrc, pydst,
                       c00, c01, c02, c03, c04,
                       c10, c11, c12, c13, c14,
                       c20, c21, c22, c23, c24,
                       c30, c31, c32, c33, c34)

    # pydst.unlock()
    # pysrc.unlock()


def staticgray(pysrc, pydst, rmul, gmul, bmul, amul, shift, vmap):
    PyErr_Clear()
    staticgray_core(pysrc, pydst, rmul, gmul, bmul, amul, shift, vmap)


def subpixel(pysrc, pydst, xoffset, yoffset, shift):

    if subpixel32(pysrc, pydst, xoffset, yoffset, shift):
        return

    pydst.blit(pysrc, (int(xoffset), int(yoffset)))


# Be sure to update scale.py when adding something new here!

import_pygame_sdl2()
core_init()
subpixel_init()
