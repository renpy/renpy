# -*- python -*-

# cdef extern class pygame.Surface:
#    pass

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
                    

    
import pygame

def version():
    return 4008005

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



core_init()
