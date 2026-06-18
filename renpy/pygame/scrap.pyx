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

from .error import error

try:
    import emscripten
except ImportError:
    emscripten = None

def init():
    pass

def quit():
    pass

SCRAP_TEXT = "text/plain"

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

def get_data(mime_type):
    """
    Returns the clipboard data for the given MIME type as bytes.
    """
    cdef size_t size = 0
    cdef void *data = SDL_GetClipboardData(mime_type.encode("utf-8"), &size)

    if data == NULL:
        raise error()

    rv = bytes((<char *>data)[:size])
    SDL_free(data)

    return rv

def get_types():
    return [SCRAP_TEXT]

def get_mime_types():
    """
    Returns the list of MIME types currently available in the clipboard.
    """
    cdef size_t num_mime_types = 0
    cdef char **mime_types = SDL_GetClipboardMimeTypes(&num_mime_types)

    if mime_types == NULL:
        return []

    rv = []

    cdef size_t i
    for i in range(num_mime_types):
        if mime_types[i] != NULL:
            rv.append(bytes(mime_types[i]).decode("utf-8"))

    SDL_free(mime_types)

    return rv

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

    SDL_SetPrimarySelectionText(data)

def contains(type):
    if type != SCRAP_TEXT:
        return False

    return SDL_HasClipboardText()

def lost():
    return False

def set_mode(mode):
    pass
