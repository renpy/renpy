# cdef extern class pygame.Surface:
#    pass

cdef extern from "renpy.h":
    void core_init()
    
    void pixellate32_core(object, object, int, int, int, int)
    void pixellate24_core(object, object, int, int, int, int)

import pygame

def version():
    return 40008002

def pixellate(pysrc, pydst, avgwidth, avgheight, outwidth, outheight):

    if not isinstance(pysrc, pygame.Surface):
        raise Exception("pixellate requires a pygame Surface as its first argument.")

    if not isinstance(pydst, pygame.Surface):
        raise Exception("pixellate requires a pygame Surface as its second argument.")

    if pysrc.get_bitsize() not in (24, 32):
        raise Exception("pixellate requires a 24 or 32 bit surface.")

    if pydst.get_bitsize() != pysrc.get_bitsize():
        raise Exception("pixellate required both surfaces have the same bitsize.")

    pysrc.lock()
    pydst.lock()

    if pysrc.get_bitsize() == 32:
        pixellate32_core(pysrc, pydst, avgwidth, avgheight, outwidth, outheight)
    else:
        pixellate24_core(pysrc, pydst, avgwidth, avgheight, outwidth, outheight)

    pydst.unlock()
    pysrc.unlock()

core_init()
