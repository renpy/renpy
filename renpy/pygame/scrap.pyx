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

from renpy.pygame.error import error
from renpy.pygame.locals import SCRAP_TEXT

try:
    import emscripten
except ImportError:
    emscripten = None

def init():
    pass

def get(type):
    cdef char *text = NULL
    if type == SCRAP_TEXT:
        text = SDL_GetClipboardText()
        if text == NULL:
            raise error()
        rv = bytes(text)
        SDL_free(text)
        return rv
    else:
        raise error("Not implemented.")

def get_types():
    return [SCRAP_TEXT]

def put(type, data):
    if type != SCRAP_TEXT:
        raise error("Not implemented.")

    if emscripten is not None:
        # SDL_SetClipboardText() is not implemented for Web
        import re
        text = data.decode('utf-8')
        script = 'navigator.clipboard.writeText(`%s`)' % (re.sub(r'([\\`$])', r'\\\1', text),)
        emscripten.run_script(script)
        return

    data = bytes(data)

    if SDL_SetClipboardText(data) != 0:
        raise error()

def contains(type):
    if type != SCRAP_TEXT:
        return False

    return SDL_HasClipboardText() == SDL_TRUE

def lost():
    return False

def set_mode(mode):
    pass

_types = """
SCRAP_TEXT : int
"""
