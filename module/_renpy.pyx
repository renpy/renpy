# -*- python -*-
# Copyright 2005 PyTom <pytom@bishoujo.us>

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

cdef extern from "renpy.h":
    void core_init()
    
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

    void xblur32_core(object, object, int)
    
    void alphamunge_core(object, object, int, int, int, char *)

    # int stretch_core(object, object, int, int, int, int)


import pygame

def version():
    return 5003003

def pixellate(pysrc, pydst, avgwidth, avgheight, outwidth, outheight):

    if not isinstance(pysrc, pygame.Surface):
        raise Exception("pixellate requires a pygame Surface as its first argument.")

    if not isinstance(pydst, pygame.Surface):
        raise Exception("pixellate requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("pixellate requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("pixellate requires both surfaces have the same bitsize.")

    pysrc.lock()
    pydst.lock()

    if pysrc.get_bitsize() == 32:
        pixellate32_core(pysrc, pydst, avgwidth, avgheight, outwidth, outheight)
    else:
        pixellate24_core(pysrc, pydst, avgwidth, avgheight, outwidth, outheight)

    pydst.unlock()
    pysrc.unlock()


# Please note that r, g, b, and a are not necessarily red, green, blue
# and alpha. Instead, they are the first through fourth byte of data.
# The mapping between byte and color/alpha varies from system to
# system, and needs to be determined at a higher level.
def map(pysrc, pydst, r, g, b, a):

    if not isinstance(pysrc, pygame.Surface):
        raise Exception("map requires a pygame Surface as its first argument.")

    if not isinstance(pydst, pygame.Surface):
        raise Exception("map requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("map requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("map requires both surfaces have the same bitsize.")

    if pydst.get_size() != pysrc.get_size():
        raise Exception("map requires both surfaces have the same size.")

    pysrc.lock()
    pydst.lock()

    if pysrc.get_bitsize() == 32:
        map32_core(pysrc, pydst, r, g, b, a)
    else:
        map24_core(pysrc, pydst, r, g, b)

    pydst.unlock()
    pysrc.unlock()

def alpha_munge(pysrc, pydst, srcchan, dstchan, amap):

    if not isinstance(pysrc, pygame.Surface):
        raise Exception("alpha_munge requires a pygame Surface as its first argument.")

    if not isinstance(pydst, pygame.Surface):
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

    pysrc.lock()
    pydst.lock()

    alphamunge_core(pysrc, pydst, bytes, srcchan, dstchan, amap)

    pydst.unlock()
    pysrc.unlock()

    


# def xblur(pysrc, pydst, radius):

#     if not isinstance(pysrc, pygame.Surface):
#         raise Exception("blur requires a pygame Surface as its first argument.")

#     if not isinstance(pydst, pygame.Surface):
#         raise Exception("blur requires a pygame Surface as its second argument.")

#     if pysrc.get_bitsize() not in (24, 32):
#         raise Exception("blur requires a 24 or 32 bit surface.")

#     if pydst.get_bitsize() != pysrc.get_bitsize():
#         raise Exception("blur requires both surfaces have the same bitsize.")

#     if pydst.get_size() != pysrc.get_size():
#         raise Exception("blur requires both surfaces have the same size.")

#     pysrc.lock()
#     pydst.lock()

#     if pysrc.get_bitsize() == 32:
#         xblur32_core(pysrc, pydst, radius)
#     else:
#         # blur24_core(pysrc, pydst, radius)
#         assert False


#     pydst.unlock()
#     pysrc.unlock()


# def stretch(pysrc, pydst, rect):

#     if not isinstance(pysrc, pygame.Surface):
#         raise Exception("stretch requires a pygame Surface as its first argument.")

#     if not isinstance(pydst, pygame.Surface):
#         raise Exception("stretch requires a pygame Surface as its second argument.")

#     if pydst.get_bitsize() != pysrc.get_bitsize():
#         raise Exception("stretch requires both surfaces have the same bitsize.")

#     if rect:
#         x, y, w, h = rect
#     else:
#         x, y = 0, 0
#         w, h = pysrc.get_size()

#     return stretch_core(pysrc, pydst, x, y, w, h)
    

core_init()
